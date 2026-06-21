"""FastAPI backend.  Run:  uvicorn api.main:app --reload"""
import sys, json, sqlite3, pathlib, tempfile, datetime
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pipeline.analyze import IPOAnalyzer
from reports.report_generator import generate_report

ROOT = pathlib.Path(__file__).resolve().parents[1]
DB = ROOT / "artifacts" / "predictions.db"

app = FastAPI(title="IPO Intelligence API", version="1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
analyzer = IPOAnalyzer()


def _db():
    DB.parent.mkdir(exist_ok=True)
    con = sqlite3.connect(DB)
    con.execute("""CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT, verdict TEXT, confidence REAL,
        invest_proba REAL, n_features INTEGER,
        features_json TEXT, created_at TEXT,
        outcome_alpha REAL, outcome_recorded_at TEXT)""")
    return con

def _log_prediction(company, result, n_features, features):
    con = _db()
    con.execute(
        "INSERT INTO predictions (company, verdict, confidence, invest_proba, n_features, "
        "features_json, created_at) VALUES (?,?,?,?,?,?,?)",
        (company, result["verdict"], result["confidence_pct"],
         result["xgb_probabilities"]["invest"], n_features,
         json.dumps(features), datetime.datetime.utcnow().isoformat()))
    con.commit()
    pid = con.execute("SELECT last_insert_rowid()").fetchone()[0]
    con.close()
    return pid


class IPOFeatures(BaseModel):
    company: str = "Unnamed IPO"
    features: dict

class AutoRequest(BaseModel):
    company: str

class Outcome(BaseModel):
    features: dict
    decision: int
    alpha_180d: float

class OutcomeById(BaseModel):
    prediction_id: int
    alpha_180d: float


@app.post("/analyse")
def analyse(req: IPOFeatures):
    result = analyzer.analyze(req.features, req.company)
    pid = _log_prediction(req.company, result, len(req.features), req.features)
    result["prediction_id"] = pid
    return result


@app.post("/analyse/auto")
def analyse_auto(req: AutoRequest):
    """Name-only analysis: scrape + LLM explain + predict, in one call."""
    from pipeline.auto_fetch import fetch_features
    from pipeline.explainer import explain
    try:
        features, page, about = fetch_features(req.company)
    except SystemExit as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Fetch failed: {e}")

    result = analyzer.analyze(features, req.company)
    ex = explain(req.company, result, features, about)
    pid = _log_prediction(req.company, result, len(features), features)

    missing = [f for f in analyzer.feats if f not in features]
    return {
        **result,
        "prediction_id": pid,
        "source_url": page,
        "n_fetched": len(features),
        "n_total": len(analyzer.feats),
        "features_defaulted": missing,
        "about": about or ex["about"],
        "explanation": ex["explanation"],
    }


@app.post("/analyse/pdf")
def analyse_pdf(req: IPOFeatures):
    result = analyzer.analyze(req.features, req.company)
    out = tempfile.mktemp(suffix=".pdf")
    generate_report(result, out)
    return FileResponse(out, filename=f"{req.company}_report.pdf")


@app.post("/feedback")
def feedback(o: Outcome):
    """Post-listing outcome arrives -> RL agent learns. The self-correction loop."""
    import numpy as np, pandas as pd
    row = pd.Series({f: o.features.get(f, float(analyzer.hist[f].median()))
                     for f in analyzer.feats})
    X = row.values.astype(float)
    xs = (X - analyzer.mu) / analyzer.sd
    proba = analyzer.bundle["calib"].predict_proba(
        pd.DataFrame(X.reshape(1, -1), columns=analyzer.feats))[0]
    r = analyzer.rl.record_outcome(xs, proba, o.decision, o.alpha_180d)
    analyzer.rl.save()
    return {"reward": round(r, 4), "status": "agent updated"}


@app.post("/feedback/by-id")
def feedback_by_id(o: OutcomeById):
    """Record a realised outcome against a logged prediction id."""
    con = _db()
    row = con.execute("SELECT company, verdict, features_json FROM predictions WHERE id=?",
                      (o.prediction_id,)).fetchone()
    if not row:
        con.close()
        raise HTTPException(status_code=404, detail="prediction_id not found")
    company, verdict, features_json = row
    decision = {"AVOID": 0, "NEUTRAL": 1, "INVEST": 2}[verdict]
    features = json.loads(features_json)
    fb = feedback(Outcome(features=features, decision=decision, alpha_180d=o.alpha_180d))
    con.execute("UPDATE predictions SET outcome_alpha=?, outcome_recorded_at=? WHERE id=?",
               (o.alpha_180d, datetime.datetime.utcnow().isoformat(), o.prediction_id))
    con.commit(); con.close()
    return fb


@app.get("/history")
def history(limit: int = 50):
    """All logged predictions — powers the Track Record page."""
    con = _db()
    rows = con.execute(
        "SELECT id, company, verdict, confidence, invest_proba, n_features, created_at, "
        "outcome_alpha FROM predictions ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    con.close()
    keys = ["id","company","verdict","confidence","invest_proba","n_features","created_at","outcome_alpha"]
    return [dict(zip(keys, r)) for r in rows]


@app.get("/metrics")
def metrics():
    art = ROOT / "artifacts"
    model_metrics = json.loads((art/"metrics.json").read_text()) if (art/"metrics.json").exists() else {}
    rl_metrics = json.loads((art/"rl_metrics.json").read_text()) if (art/"rl_metrics.json").exists() else {}
    con = _db()
    total = con.execute("SELECT COUNT(*) FROM predictions").fetchone()[0]
    by_verdict = dict(con.execute(
        "SELECT verdict, COUNT(*) FROM predictions GROUP BY verdict").fetchall())
    con.close()
    return {"model": model_metrics, "rl": rl_metrics,
            "live": {"total_predictions": total, "by_verdict": by_verdict}}


@app.get("/health")
def health():
    return {"status": "ok", "feature_count": len(analyzer.feats)}
