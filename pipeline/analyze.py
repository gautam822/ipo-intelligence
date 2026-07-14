"""
Orchestrator: takes an IPO's feature dict -> full analysis result.
In production the feature dict is built by scrapers + llm/drhp_analyzer.
"""
import json, pathlib
import numpy as np
import pandas as pd
import joblib

ROOT = pathlib.Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts"

PILLARS = {
    "Financial Health": ["revenue_cagr_3y","pat_margin","pat_margin_trend","ocf_pat_ratio",
                         "debt_equity","roce","roe","wc_days","debtor_days_trend","interest_coverage"],
    "Valuation": ["pe_vs_peer_median","ev_ebitda_vs_peer","ps_ratio","price_vs_last_pe_round","pb_ratio"],
    "Issue Structure": ["ofs_pct","gcp_pct","promoter_post_holding","promoter_pledge_flag",
                        "fresh_for_debt_pct","issue_size_cr"],
    "Governance": ["governance_score","rpt_intensity","auditor_big4","auditor_qualified",
                   "litigation_severity","risk_factor_severity"],
    "Demand & Sentiment": ["qib_subscription","hni_subscription","retail_subscription",
                           "gmp_pct","news_sentiment","anchor_quality"],
    "Market Regime": ["bull_regime"],
}
HIGHER_BAD = {"debt_equity","wc_days","debtor_days_trend","pe_vs_peer_median","ev_ebitda_vs_peer",
              "ps_ratio","price_vs_last_pe_round","pb_ratio","ofs_pct","gcp_pct","promoter_pledge_flag",
              "fresh_for_debt_pct","rpt_intensity","auditor_qualified","litigation_severity",
              "risk_factor_severity"}
LABELS = {0: "AVOID", 1: "NEUTRAL", 2: "INVEST"}


class IPOAnalyzer:
    def __init__(self):
        self.bundle = joblib.load(ART / "model.joblib")
        self.explainer = joblib.load(ART / "shap_explainer.joblib")
        self.hist = pd.read_csv(ROOT / "data/ipo_dataset.csv")
        self.feats = self.bundle["features"]
        sc = np.load(ART / "rl_scaler.npz")
        self.mu, self.sd = sc["mu"], sc["sd"]
        from rl.agent import LightPolicyAgent
        try:
            self.rl = LightPolicyAgent.load(len(self.feats))
        except FileNotFoundError:
            self.rl = None

    def pillar_scores(self, row: pd.Series) -> dict:
        """Percentile-vs-history score per pillar, 0-10."""
        out = {}
        for pillar, cols in PILLARS.items():
            pcts = []
            for c in cols:
                pct = (self.hist[c] <= row[c]).mean()
                if c in HIGHER_BAD:
                    pct = 1 - pct
                pcts.append(pct)
            out[pillar] = round(float(np.mean(pcts)) * 10, 1)
        return out

    def nearest_comparable(self, x: np.ndarray) -> dict:
        Xh = (self.hist[self.feats].values - self.mu) / self.sd
        d = np.linalg.norm(Xh - (x - self.mu) / self.sd, axis=1)
        i = int(d.argmin())
        r = self.hist.iloc[i]
        return {"company": r.company, "year": int(r.year), "sector": r.sector,
                "alpha_180d": round(float(r.alpha_180d) * 100, 1)}

    def analyze(self, features: dict, company="Unnamed IPO") -> dict:
        row = pd.Series({f: features.get(f, float(self.hist[f].median())) for f in self.feats})
        X = row.values.reshape(1, -1).astype(float)
        df_X = pd.DataFrame(X, columns=self.feats)

        proba = self.bundle["calib"].predict_proba(df_X)[0]
        xgb_decision = int(proba.argmax())

        # RL overlay — agent may discount/boost the supervised call
        if self.rl is not None:
            xs = (X[0] - self.mu) / self.sd
            rl_decision, rl_conf, rl_p = self.rl.act(xs, proba)
            decision, confidence = rl_decision, rl_conf
        else:
            decision, confidence = xgb_decision, float(proba.max())

        # SHAP top drivers
        sv = self.explainer.shap_values(df_X)
        sv_dec = np.array(sv)[..., xgb_decision].flatten() if np.array(sv).ndim == 3 else np.array(sv).flatten()
        order = np.argsort(-np.abs(sv_dec))
        drivers = [{"feature": self.feats[i], "shap": round(float(sv_dec[i]), 4),
                    "value": round(float(row.iloc[i]), 3),
                    "direction": "supports" if sv_dec[i] > 0 else "against"}
                   for i in order[:8]]

        # red flags (rule layer)
        flags = []
        if row.ofs_pct > 0.6: flags.append(f"OFS-heavy issue ({row.ofs_pct:.0%} of total) — insiders exiting")
        if row.gcp_pct > 0.25: flags.append(f"General corporate purposes {row.gcp_pct:.0%} of proceeds (>25% threshold)")
        if row.ocf_pat_ratio < 0.5: flags.append(f"Weak cash conversion — OCF/PAT only {row.ocf_pat_ratio:.2f}")
        if row.promoter_pledge_flag: flags.append("Promoter share pledge detected")
        if row.auditor_qualified: flags.append("Qualified audit opinion in DRHP period")
        if row.pe_vs_peer_median > 1.5: flags.append(f"Priced at {row.pe_vs_peer_median:.1f}x peer median P/E")
        if row.debtor_days_trend > 10: flags.append("Debtor days rising sharply — revenue quality risk")

        return {
            "company": company,
            "verdict": LABELS[decision],
            "confidence_pct": round(confidence * 100, 1),
            "xgb_probabilities": {"avoid": round(float(proba[0]),3),
                                  "neutral": round(float(proba[1]),3),
                                  "invest": round(float(proba[2]),3)},
            "pillar_scores": self.pillar_scores(row),
            "top_drivers": drivers,
            "red_flags": flags or ["No major rule-based red flags detected"],
            "nearest_comparable": self.nearest_comparable(X[0]),
            "disclaimer": ("Confidence reflects historical calibration at this signal profile, "
                           "not a guarantee. Not investment advice."),
        }


if __name__ == "__main__":
    import sys; sys.path.insert(0, str(ROOT))
    a = IPOAnalyzer()
    demo = dict(revenue_cagr_3y=0.32, pat_margin=0.14, ocf_pat_ratio=1.1, debt_equity=0.4,
                roce=0.22, ofs_pct=0.25, gcp_pct=0.10, qib_subscription=45, gmp_pct=0.35,
                governance_score=8, bull_regime=1)
    print(json.dumps(a.analyze(demo, "Demo Industries Ltd"), indent=2))
