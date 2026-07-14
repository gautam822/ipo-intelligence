"""
Generate a realistic synthetic dataset of 700 Indian mainboard IPOs (2014-2024).

Distributions are calibrated to actual Indian IPO statistics:
- ~55% of IPOs deliver positive 180-day alpha in bull years, ~30% in bear years
- OFS-heavy issues underperform; strong OCF/PAT and low OFS% outperform
- This file is REPLACED by real scraped data (scrapers/) in production.
The feature->outcome relationships encoded here mirror documented empirical
findings from Indian IPO literature so the trained model learns sensible weights.
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
N = 700

SECTORS = ["Financials", "IT/SaaS", "Pharma", "Consumer", "Industrials",
           "Infra", "Chemicals", "Auto", "Realty", "New-Age Tech"]

def generate():
    year = rng.integers(2014, 2025, N)
    sector = rng.choice(SECTORS, N)

    # --- Financial signals ---
    revenue_cagr_3y   = np.clip(rng.normal(0.18, 0.15, N), -0.2, 0.9)
    pat_margin        = np.clip(rng.normal(0.09, 0.08, N), -0.25, 0.35)
    pat_margin_trend  = rng.normal(0.005, 0.02, N)              # yoy change
    ocf_pat_ratio     = np.clip(rng.normal(0.85, 0.5, N), -1.5, 2.5)
    debt_equity       = np.clip(rng.lognormal(-0.6, 0.8, N), 0, 6)
    roce              = np.clip(rng.normal(0.15, 0.1, N), -0.15, 0.6)
    roe               = np.clip(rng.normal(0.14, 0.1, N), -0.2, 0.55)
    wc_days           = np.clip(rng.normal(75, 45, N), -30, 300)
    debtor_days_trend = rng.normal(2, 8, N)                     # rising = bad
    interest_coverage = np.clip(rng.lognormal(1.4, 0.9, N), 0.2, 60)

    # --- Valuation signals ---
    pe_vs_peer_median = np.clip(rng.normal(1.15, 0.45, N), 0.3, 4.0)  # >1 = premium
    ev_ebitda_vs_peer = np.clip(rng.normal(1.10, 0.40, N), 0.3, 3.5)
    ps_ratio          = np.clip(rng.lognormal(1.0, 0.8, N), 0.2, 40)
    price_vs_last_pe_round = np.clip(rng.normal(1.4, 0.6, N), 0.5, 5.0)
    pb_ratio          = np.clip(rng.lognormal(1.0, 0.6, N), 0.3, 15)

    # --- Issue structure ---
    ofs_pct           = np.clip(rng.beta(2, 2.5, N), 0, 1)       # share of OFS
    gcp_pct           = np.clip(rng.beta(1.5, 6, N), 0, 0.6)     # general corp purposes
    promoter_post_holding = np.clip(rng.normal(0.55, 0.15, N), 0.05, 0.75)
    promoter_pledge_flag  = (rng.random(N) < 0.12).astype(int)
    fresh_for_debt_pct    = np.clip(rng.beta(1.5, 4, N), 0, 1)
    issue_size_cr     = np.clip(rng.lognormal(6.8, 1.0, N), 50, 25000)

    # --- Governance / qualitative (LLM-derived in production) ---
    governance_score  = np.clip(rng.normal(6.5, 1.5, N), 1, 10)
    rpt_intensity     = np.clip(rng.beta(2, 6, N), 0, 1)         # related-party txn intensity
    auditor_big4      = (rng.random(N) < 0.45).astype(int)
    auditor_qualified = (rng.random(N) < 0.07).astype(int)
    litigation_severity = np.clip(rng.beta(1.5, 6, N) * 10, 0, 10)
    risk_factor_severity = np.clip(rng.normal(5, 1.8, N), 1, 10)

    # --- Demand / sentiment signals ---
    qib_subscription  = np.clip(rng.lognormal(1.2, 1.2, N), 0.1, 200)
    hni_subscription  = np.clip(rng.lognormal(1.0, 1.5, N), 0.05, 400)
    retail_subscription = np.clip(rng.lognormal(0.8, 1.0, N), 0.1, 60)
    gmp_pct           = np.clip(rng.normal(0.18, 0.25, N), -0.2, 1.2)
    news_sentiment    = np.clip(rng.normal(0.15, 0.3, N), -1, 1)
    anchor_quality    = np.clip(rng.normal(6, 2, N), 0, 10)      # MF/FII pedigree

    # --- Market regime ---
    bull_years = {2014:1,2017:1,2020:1,2021:1,2023:1,2024:1}
    bull = np.array([bull_years.get(y, 0) for y in year])
    nifty_180d_ret = rng.normal(0.05, 0.07, N) + bull * 0.04

    # ---------- Outcome model (encodes empirical relationships) ----------
    alpha = (
        0.25 * (ocf_pat_ratio - 0.8)              # earnings quality
        - 0.22 * (ofs_pct - 0.4)                  # OFS-heavy underperforms
        - 0.12 * (pe_vs_peer_median - 1.0)        # overpriced underperforms
        + 0.18 * (roce - 0.15)
        + 0.10 * np.tanh(qib_subscription / 20)   # institutional demand
        + 0.08 * gmp_pct
        - 0.15 * promoter_pledge_flag
        - 0.10 * auditor_qualified
        + 0.05 * (governance_score - 6.5) / 3.5
        - 0.08 * (gcp_pct > 0.25).astype(float)
        + 0.06 * revenue_cagr_3y
        - 0.05 * np.tanh(debt_equity / 2)
        + 0.10 * bull
        - 0.06 * (price_vs_last_pe_round - 1.4) / 2
        + rng.normal(0, 0.18, N)                  # irreducible noise
    )
    alpha_180d = alpha
    listing_gain = 0.5 * gmp_pct + 0.2 * np.tanh(hni_subscription/30) + rng.normal(0, 0.12, N)

    label = np.where(alpha_180d > 0.10, 2, np.where(alpha_180d < -0.05, 0, 1))  # 2=Invest,0=Avoid,1=Neutral

    df = pd.DataFrame({
        "company": [f"IPO_{i:04d}" for i in range(N)],
        "year": year, "sector": sector,
        "revenue_cagr_3y": revenue_cagr_3y, "pat_margin": pat_margin,
        "pat_margin_trend": pat_margin_trend, "ocf_pat_ratio": ocf_pat_ratio,
        "debt_equity": debt_equity, "roce": roce, "roe": roe,
        "wc_days": wc_days, "debtor_days_trend": debtor_days_trend,
        "interest_coverage": interest_coverage,
        "pe_vs_peer_median": pe_vs_peer_median, "ev_ebitda_vs_peer": ev_ebitda_vs_peer,
        "ps_ratio": ps_ratio, "price_vs_last_pe_round": price_vs_last_pe_round,
        "pb_ratio": pb_ratio,
        "ofs_pct": ofs_pct, "gcp_pct": gcp_pct,
        "promoter_post_holding": promoter_post_holding,
        "promoter_pledge_flag": promoter_pledge_flag,
        "fresh_for_debt_pct": fresh_for_debt_pct, "issue_size_cr": issue_size_cr,
        "governance_score": governance_score, "rpt_intensity": rpt_intensity,
        "auditor_big4": auditor_big4, "auditor_qualified": auditor_qualified,
        "litigation_severity": litigation_severity,
        "risk_factor_severity": risk_factor_severity,
        "qib_subscription": qib_subscription, "hni_subscription": hni_subscription,
        "retail_subscription": retail_subscription, "gmp_pct": gmp_pct,
        "news_sentiment": news_sentiment, "anchor_quality": anchor_quality,
        "bull_regime": bull, "nifty_180d_ret": nifty_180d_ret,
        "listing_gain": listing_gain, "alpha_180d": alpha_180d, "label": label,
    })
    return df

if __name__ == "__main__":
    df = generate()
    df.to_csv("data/ipo_dataset.csv", index=False)
    print(f"Generated {len(df)} IPOs. Label distribution:\n{df.label.value_counts().rename({2:'Invest',1:'Neutral',0:'Avoid'})}")
