"""
Train calibrated XGBoost on historical IPO dataset.
Time-based splits: 2014-21 train | 2022 val | 2023-24 test.
Saves: model, calibrator, SHAP explainer, metrics, backtest results.
"""
import json, pathlib, joblib
import numpy as np
import pandas as pd
import shap
from xgboost import XGBClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import classification_report, f1_score

ART = pathlib.Path(__file__).resolve().parents[1] / "artifacts"
ART.mkdir(exist_ok=True)

DROP = ["company", "sector", "alpha_180d", "listing_gain", "label", "nifty_180d_ret"]

def load():
    df = pd.read_csv(pathlib.Path(__file__).resolve().parents[1] / "data/ipo_dataset.csv")
    X = df.drop(columns=DROP)
    return df, X, df["label"].values

def time_splits(df):
    tr = df.year <= 2021
    va = df.year == 2022
    te = df.year >= 2023
    return tr.values, va.values, te.values

def train():
    df, X, y = load()
    tr, va, te = time_splits(df)

    base = XGBClassifier(
        n_estimators=400, max_depth=4, learning_rate=0.05,
        subsample=0.8, colsample_bytree=0.8, reg_lambda=2.0,
        objective="multi:softprob", num_class=3,
        eval_metric="mlogloss", random_state=42,
    )
    base.fit(X[tr], y[tr], eval_set=[(X[va], y[va])], verbose=False)

    # Calibrate on validation year — makes confidence % trustworthy
    try:
        from sklearn.frozen import FrozenEstimator        # sklearn >= 1.6
        calib = CalibratedClassifierCV(FrozenEstimator(base), method="isotonic")
    except ImportError:
        calib = CalibratedClassifierCV(base, method="isotonic", cv="prefit")
    calib.fit(X[va], y[va])

    # ---- Test metrics
    proba = calib.predict_proba(X[te])
    pred = proba.argmax(1)
    report = classification_report(y[te], pred, target_names=["Avoid","Neutral","Invest"], output_dict=True)
    f1_invest = f1_score(y[te], pred, labels=[2], average="macro")

    # ---- Backtest: equal-weight all Invest calls in test years
    test_df = df[te].copy()
    test_df["pred"] = pred
    test_df["conf"] = proba.max(1)
    invest = test_df[test_df.pred == 2]
    port_alpha = invest.alpha_180d.mean() if len(invest) else 0.0
    hit_rate = (invest.alpha_180d > 0).mean() if len(invest) else 0.0
    baseline_alpha = test_df.alpha_180d.mean()

    # ---- SHAP
    explainer = shap.TreeExplainer(base)
    metrics = {
        "f1_invest": round(float(f1_invest), 3),
        "accuracy": round(float(report["accuracy"]), 3),
        "invest_precision": round(float(report["Invest"]["precision"]), 3),
        "invest_recall": round(float(report["Invest"]["recall"]), 3),
        "n_invest_calls_test": int(len(invest)),
        "portfolio_alpha_180d": round(float(port_alpha), 4),
        "hit_rate": round(float(hit_rate), 3),
        "all_ipo_baseline_alpha": round(float(baseline_alpha), 4),
    }

    joblib.dump({"base": base, "calib": calib, "features": list(X.columns)}, ART / "model.joblib")
    joblib.dump(explainer, ART / "shap_explainer.joblib")
    (ART / "metrics.json").write_text(json.dumps(metrics, indent=2))
    test_df.to_csv(ART / "backtest_results.csv", index=False)
    print(json.dumps(metrics, indent=2))
    return metrics

if __name__ == "__main__":
    train()
