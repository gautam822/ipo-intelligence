"""
Reinforcement learning layer.

Design:
- State  : 35-dim feature vector of an IPO (same features as XGBoost)
- Action : confidence adjustment on top of the calibrated XGBoost probability.
           The agent learns WHEN to trust / discount the supervised model.
- Reward : realised 180-day alpha vs Nifty, weighted by stated confidence.
           High-confidence wrong calls penalised 2x (asymmetric loss).
- Warmstart: policy initialised from XGBoost outputs (behavioural cloning) —
           avoids RL cold-start on only ~700 episodes.
- Replay : 50/50 sampling of historical + recent episodes to prevent
           catastrophic forgetting across market regimes.

Two implementations:
1. LightPolicyAgent (numpy REINFORCE) — zero heavy deps, used in the demo.
2. gymnasium Env (IPOEnv) — drop-in for stable-baselines3 PPO when you want
   to scale up:   PPO("MlpPolicy", IPOEnv(df, features)).learn(200_000)
"""
import json, pathlib
import numpy as np
import pandas as pd

ART = pathlib.Path(__file__).resolve().parents[1] / "artifacts"


# ----------------------------------------------------------- reward function
def reward(action_conf: float, decision: int, alpha_180d: float) -> float:
    """decision: 2=Invest, 0=Avoid, 1=Neutral. Asymmetric: confident mistakes hurt 2x."""
    if decision == 2:                       # invested
        r = alpha_180d * action_conf
        if alpha_180d < 0:
            r *= 2.0                        # punish confident bad calls harder
    elif decision == 0:                     # avoided
        r = -alpha_180d * action_conf       # reward avoiding losers
        if alpha_180d > 0.10:
            r *= 1.5                        # missing big winners also costs
    else:
        r = -0.01 * action_conf             # mild penalty for fence-sitting confidently
    return float(r)


# ------------------------------------------------- lightweight REINFORCE agent
class LightPolicyAgent:
    """Linear-softmax policy over (state ⊕ xgb_proba). Learns a confidence
    multiplier per regime. Small, interpretable, converges on 700 episodes."""

    def __init__(self, n_features, lr=0.01, seed=42):
        rng = np.random.default_rng(seed)
        self.W = rng.normal(0, 0.01, (n_features + 3, 3))   # +3 xgb probas, 3 actions
        self.lr = lr
        self.replay = []                                     # (x, action, reward)

    @staticmethod
    def _softmax(z):
        z = z - z.max()
        e = np.exp(z)
        return e / e.sum()

    def _x(self, state, xgb_proba):
        return np.concatenate([state, xgb_proba])

    def act(self, state, xgb_proba, temperature=3.0):
        x = self._x(state, xgb_proba)
        p = self._softmax((x @ self.W) / temperature)        # tempered policy
        action = int(np.argmax(p))                           # greedy at inference
        # final confidence = blend of policy and calibrated supervised probability
        confidence = float(0.5 * p[action] + 0.5 * xgb_proba[action])
        return action, confidence, p

    def warmstart(self, X, xgb_probas, epochs=30):
        """Behavioural cloning: imitate calibrated XGBoost before RL begins."""
        targets = xgb_probas.argmax(1)
        for _ in range(epochs):
            for i in range(len(X)):
                x = self._x(X[i], xgb_probas[i])
                p = self._softmax(x @ self.W)
                grad = -np.outer(x, np.eye(3)[targets[i]] - p)
                self.W -= self.lr * grad

    def record_outcome(self, state, xgb_proba, action, alpha_180d):
        """Called when a real post-listing outcome arrives. The feedback loop."""
        x = self._x(state, xgb_proba)
        p = self._softmax(x @ self.W)
        r = reward(p[action], action, alpha_180d)
        self.replay.append((x, action, r))
        self._update()
        return r

    def _update(self, batch=32):
        """REINFORCE update with 50/50 old-new replay sampling."""
        if len(self.replay) < 4:
            return
        half = batch // 2
        recent = self.replay[-half:]
        old_pool = self.replay[:-half] or self.replay
        idx = np.random.default_rng().integers(0, len(old_pool), min(half, len(old_pool)))
        sample = recent + [old_pool[i] for i in idx]
        baseline = np.mean([r for _, _, r in sample])
        for x, a, r in sample:
            p = self._softmax(x @ self.W)
            grad = np.outer(x, np.eye(3)[a] - p) * (r - baseline)
            self.W += self.lr * grad

    def save(self, path=ART / "rl_agent.npz"):
        np.savez(path, W=self.W)

    @classmethod
    def load(cls, n_features, path=ART / "rl_agent.npz"):
        a = cls(n_features)
        a.W = np.load(path)["W"]
        return a


# --------------------------------------------- gymnasium env for SB3 scale-up
try:
    import gymnasium as gym

    class IPOEnv(gym.Env):
        """One episode = one IPO. For stable-baselines3 PPO:
           from stable_baselines3 import PPO
           PPO('MlpPolicy', IPOEnv(df, features)).learn(200_000)"""
        def __init__(self, df: pd.DataFrame, feature_cols):
            super().__init__()
            self.df, self.cols = df.reset_index(drop=True), feature_cols
            self.observation_space = gym.spaces.Box(-np.inf, np.inf, (len(feature_cols),), np.float32)
            self.action_space = gym.spaces.Discrete(3)       # 0 Avoid, 1 Neutral, 2 Invest
            self.i = 0

        def reset(self, seed=None, options=None):
            super().reset(seed=seed)
            self.i = int(np.random.default_rng(seed).integers(0, len(self.df)))
            obs = self.df.loc[self.i, self.cols].values.astype(np.float32)
            return obs, {}

        def step(self, action):
            alpha = float(self.df.loc[self.i, "alpha_180d"])
            r = reward(1.0, int(action), alpha)
            obs = self.df.loc[self.i, self.cols].values.astype(np.float32)
            return obs, r, True, False, {}
except ImportError:
    pass


# --------------------------------------------------------------- train script
def train_rl():
    import joblib
    root = pathlib.Path(__file__).resolve().parents[1]
    df = pd.read_csv(root / "data/ipo_dataset.csv")
    bundle = joblib.load(ART / "model.joblib")
    feats = bundle["features"]

    X = df[feats].values
    # standardise for the linear policy
    mu, sd = X.mean(0), X.std(0) + 1e-9
    Xs = (X - mu) / sd
    np.savez(ART / "rl_scaler.npz", mu=mu, sd=sd)

    probas = bundle["calib"].predict_proba(df[feats])

    tr = (df.year <= 2021).values
    te = (df.year >= 2023).values

    agent = LightPolicyAgent(Xs.shape[1])
    agent.warmstart(Xs[tr], probas[tr])

    # simulate the live loop: predictions arrive, outcomes come back, agent learns
    rewards = []
    order = np.where(tr)[0]
    np.random.default_rng(0).shuffle(order)
    for i in order:
        a, conf, _ = agent.act(Xs[i], probas[i])
        r = agent.record_outcome(Xs[i], probas[i], a, df.alpha_180d.iloc[i])
        rewards.append(r)

    # evaluate on held-out 2023-24
    test_rewards, decisions = [], []
    for i in np.where(te)[0]:
        a, conf, _ = agent.act(Xs[i], probas[i])
        test_rewards.append(reward(conf, a, df.alpha_180d.iloc[i]))
        decisions.append(a)

    # compare vs pure-XGBoost decisions on the same test set
    xgb_rewards = []
    for i in np.where(te)[0]:
        a = int(probas[i].argmax()); conf = float(probas[i].max())
        xgb_rewards.append(reward(conf, a, df.alpha_180d.iloc[i]))

    metrics = {
        "train_mean_reward_last100": round(float(np.mean(rewards[-100:])), 4),
        "test_mean_reward_rl": round(float(np.mean(test_rewards)), 4),
        "test_mean_reward_xgb_only": round(float(np.mean(xgb_rewards)), 4),
        "rl_improvement_pct": round(100 * (np.mean(test_rewards) - np.mean(xgb_rewards))
                                    / (abs(np.mean(xgb_rewards)) + 1e-9), 1),
        "test_invest_calls": int(sum(1 for d in decisions if d == 2)),
    }
    agent.save()
    (ART / "rl_metrics.json").write_text(json.dumps(metrics, indent=2))
    np.save(ART / "rl_reward_curve.npy", np.array(rewards))
    print(json.dumps(metrics, indent=2))
    return metrics

if __name__ == "__main__":
    train_rl()
