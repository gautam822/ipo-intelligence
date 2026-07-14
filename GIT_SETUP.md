# Pushing this project to GitHub

## First-time setup

```bash
cd ipo-intelligence
git init
git add .
git commit -m "Initial commit: IPO Intelligence System"
```

Create a new repo on github.com (don't initialise with README — you already have one), then:

```bash
git remote add origin https://github.com/<your-username>/<repo-name>.git
git branch -M main
git push -u origin main
```

## What's excluded by .gitignore (and why)

- `venv/` — your local environment, never commit this
- `data/ipo_dataset.csv` and `data/raw_drhp/` — generated/scraped data, regenerate with `python data/generate_dataset.py`
- `artifacts/*.joblib`, `*.npz`, `*.npy` — trained model binaries (can be large); regenerate with the training scripts
- `*.pdf` — sample reports, regenerate anytime
- `.env` — if you create one for API keys, never commit it

## Before pushing, double check no secrets are committed

```bash
git grep -i "sk-ant\|AIzaSy\|gsk_"   # should return nothing
```

If you ever set an API key directly in a file by mistake, remove it and run
`git log --all -- <file>` to make sure it's not in history before pushing publicly.

## Recommended repo description / topics

**Description:** AI-powered IPO analysis system with calibrated XGBoost, SHAP explainability, and a self-correcting reinforcement learning feedback loop.

**Topics:** `machine-learning` `reinforcement-learning` `xgboost` `fintech` `streamlit` `fastapi` `nlp` `shap` `ipo-analysis`
