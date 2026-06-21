# IPO Intelligence System

AI-powered IPO analysis with a **self-correcting reinforcement learning loop**. Type a company name → get an analyst-grade report with an INVEST / NEUTRAL / AVOID verdict, calibrated confidence %, pillar scorecard, SHAP explainability, plain-language explanation, red flags, and a nearest historical comparable — in a dark, terminal-inspired UI.

```
DRHP / NSE data ──► Feature vector (35 signals) ──► Calibrated XGBoost ──► RL overlay ──► Verdict + Confidence
                                                          ▲                                      │
                                                          └──── 180-day outcome (reward) ◄───────┘
```

## Results (held-out 2023–24 test set, 700-IPO dataset)

| Metric | Value |
|---|---|
| Invest-call precision | 0.625 |
| Model portfolio alpha (180d, equal-weight Invest calls) | **+21.1%** |
| Hit rate on Invest calls | 80% |
| All-IPO baseline alpha | +5.1% |
| RL agent vs pure XGBoost (mean reward) | **+12.8%** |

## Architecture

| Layer | File | What it does |
|---|---|---|
| Scrapers | `scrapers/scrape_all.py` | SEBI DRHP downloader, pdfplumber section extraction, NSE subscription/price APIs, GMP tracker |
| LLM analyser | `llm/drhp_analyzer.py` | 3 Claude prompt chains: risk-factor severity, use-of-proceeds, governance scoring → JSON features |
| Dataset | `data/generate_dataset.py` | 700 IPOs (2014–24). **Synthetic placeholder** calibrated to real Indian-IPO empirics — swap with scraped data |
| Supervised model | `models/train_xgb.py` | XGBoost, time-based splits (no leakage), isotonic calibration, SHAP, backtest |
| RL layer | `rl/agent.py` | REINFORCE policy warm-started from XGBoost (behavioural cloning), asymmetric reward (confident mistakes ×2 penalty), 50/50 replay vs catastrophic forgetting. Includes `gymnasium` env for SB3 PPO scale-up |
| Orchestrator | `pipeline/analyze.py` | Features → prediction → SHAP drivers → pillar percentiles → red-flag rules → nearest comparable |
| Reports | `reports/report_generator.py` | Analyst-grade PDF via reportlab |
| API | `api/main.py` | FastAPI: `/analyse`, `/analyse/auto` (scrape+predict in one call), `/analyse/pdf`, `/feedback`, `/feedback/by-id`, `/history`, `/metrics` — SQLite-logged prediction history |
| Frontend | `frontend/` | React + Vite + Tailwind. Command-bar search, animated confidence dial, SHAP driver bars, live ticker of recent verdicts, Track Record page, How-it-works page |
| Legacy UI | `app/streamlit_app.py` | Original Streamlit demo — kept for quick local testing without a frontend build step |

## Quickstart

**Backend:**
```bash
pip install -r requirements.txt
python data/generate_dataset.py     # or run scrapers for real data
python models/train_xgb.py
python rl/agent.py
uvicorn api.main:app --reload       # http://localhost:8000
```

**Frontend (new — React + Tailwind, full custom UI):**
```bash
cd frontend
npm install
npm run dev                         # http://localhost:5173, proxies /api -> :8000
```

Open `http://localhost:5173` — the backend must be running on port 8000 for the proxy to work.

**Legacy Streamlit demo (still included, simpler to run):**
```bash
streamlit run app/streamlit_app.py
```

## The self-correction loop

1. New IPO analysed → prediction + confidence logged
2. 180 days post-listing, realised alpha vs Nifty is POSTed to `/feedback`
3. Reward computed (asymmetric — high-confidence wrong calls penalised 2×)
4. Policy weights update via REINFORCE with replay sampling
5. Next prediction reflects the lesson

## Key design decisions (interview talking points)

- **Time-based splits, never random** — random splits leak future market regimes into training
- **Isotonic calibration** — raw XGBoost probabilities aren't trustworthy; "78% confidence" must mean 78% historical accuracy
- **Behavioural-cloning warmstart** — RL from random weights won't converge on ~700 episodes
- **Asymmetric reward** — confident wrong calls are penalised 2×; missing big winners 1.5×
- **Experience replay (50/50 old/new)** — one bear market must not erase bull-market learning
- **Regime feature** — the model knows whether it's a bull or bear cycle

## Honest limitations

- Demo dataset is synthetic (calibrated to real distributions); real edge requires the scraped dataset
- ~60–80 Indian mainboard IPOs/year → slow RL signal; multi-horizon rewards (Day 1/30/180) mitigate
- Confidence = historical calibration, **not a guarantee**. Not investment advice.

## Roadmap

- [ ] Run scrapers, replace synthetic dataset with real 2014–24 DRHP data
- [ ] Wire `llm/drhp_analyzer.py` into the live pipeline (needs `ANTHROPIC_API_KEY`)
- [ ] Upgrade RL to PPO via `stable-baselines3` using the included `IPOEnv`
- [ ] APScheduler job: auto-detect new NSE filings weekly
- [ ] Deploy Streamlit Cloud + log predictions to Supabase
