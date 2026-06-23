"""IPO Intelligence — $100k Premium UI.  streamlit run app/streamlit_app.py"""
import sys, pathlib, json, tempfile
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import streamlit as st
import plotly.graph_objects as go
from pipeline.analyze import IPOAnalyzer
from reports.report_generator import generate_report
from app.theme import (
    CSS, COUNTER_JS,
    VERDICT_COLOR, VERDICT_GLOW, VERDICT_DIM,
    GREEN, RED, AMBER, STEEL, MUTE,
    verdict_hero_html, banner_html, pillar_bar_html, driver_bar_html,
    flag_html, data_bar_html, confidence_dial_svg,
)

st.set_page_config(
    page_title="IPO Intelligence · AI Verdict Engine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(CSS, unsafe_allow_html=True)


@st.cache_resource
def get_analyzer():
    return IPOAnalyzer()
A = get_analyzer()


def plotly_premium(fig, height=240):
    fig.update_layout(
        height=height,
        margin=dict(t=6, b=6, l=6, r=6),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="JetBrains Mono", color="#394150", size=11),
        xaxis=dict(
            color="#394150", tickcolor="rgba(0,0,0,0)",
            gridcolor="rgba(255,255,255,0.04)",
            linecolor="rgba(255,255,255,0.06)",
        ),
        yaxis=dict(visible=False),
        bargap=0.35,
    )
    return fig


# ── top bar ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="ipo-topbar">
  <div class="ipo-topbar-dot"></div>
  <div class="ipo-topbar-logo">IPO <span>Intelligence</span></div>
  <div class="ipo-topbar-badge">XGB + RL · v1.0</div>
  <div class="ipo-topbar-tagline">CALIBRATED ON 700 HISTORICAL IPOs · NOT INVESTMENT ADVICE</div>
</div>
""", unsafe_allow_html=True)


# ── empty / hero state ────────────────────────────────────────────────────────
def render_empty(art_path):
    st.markdown("""
    <div class="hero-section fade-up">
      <div class="hero-eyebrow">
        <span class="hero-eyebrow-dot"></span>
        AI-powered IPO analysis · India
      </div>
      <div class="hero-h1">
        Should you invest<br/>
        <span class="grad">in this IPO?</span>
      </div>
      <div class="hero-sub">
        Type any company name in the sidebar. We scrape DRHP filings,
        run calibrated ML + RL models, and deliver an analyst-grade verdict in seconds.
      </div>
    </div>
    """, unsafe_allow_html=True)

    if (art_path / "metrics.json").exists() and (art_path / "rl_metrics.json").exists():
        m = json.loads((art_path / "metrics.json").read_text())
        r = json.loads((art_path / "rl_metrics.json").read_text())
        ip  = m['invest_precision']
        pa  = m['portfolio_alpha_180d'] * 100
        hr  = m['hit_rate'] * 100
        rl  = r['rl_improvement_pct']
        st.markdown(f"""
        <div class="metric-strip fade-up fade-up-1">
          <div class="metric-cell">
            <div class="metric-val" data-count="{ip:.2f}" data-decimals="2">{ip:.2f}</div>
            <div class="metric-lbl">Invest Precision</div>
          </div>
          <div class="metric-cell">
            <div class="metric-val" style="color:#00D9A3" data-count="{pa:.1f}" data-prefix="+" data-suffix="%" data-decimals="1">+{pa:.1f}%</div>
            <div class="metric-lbl">Portfolio Alpha 180d</div>
          </div>
          <div class="metric-cell">
            <div class="metric-val" data-count="{hr:.0f}" data-suffix="%" data-decimals="0">{hr:.0f}%</div>
            <div class="metric-lbl">Hit Rate</div>
          </div>
          <div class="metric-cell">
            <div class="metric-val" style="color:#00D9A3" data-count="{rl:.1f}" data-prefix="+" data-suffix="%" data-decimals="1">+{rl:.1f}%</div>
            <div class="metric-lbl">RL vs XGB Reward</div>
          </div>
        </div>
        {COUNTER_JS}
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="padding:0 0 16px">
      <p style="font-family:JetBrains Mono;font-size:9px;letter-spacing:0.14em;text-transform:uppercase;
                color:#28303D;text-align:center;margin:0 0 20px">How it works</p>
      <div class="hiw-grid">
        <div class="hiw-card fade-up fade-up-2">
          <span class="hiw-icon">📡</span>
          <div class="hiw-title">Scrape &amp; Fetch</div>
          <div class="hiw-desc">DRHP from SEBI, NSE subscription data, grey market premium, and 35 financial signals scraped in real-time.</div>
        </div>
        <div class="hiw-card fade-up fade-up-3">
          <span class="hiw-icon">🧠</span>
          <div class="hiw-title">ML + RL Verdict</div>
          <div class="hiw-desc">Calibrated XGBoost trained on 700 Indian IPOs, overlaid with a REINFORCE agent that self-corrects from 180-day outcomes.</div>
        </div>
        <div class="hiw-card fade-up fade-up-4">
          <span class="hiw-icon">🔬</span>
          <div class="hiw-title">SHAP Explainability</div>
          <div class="hiw-desc">Every verdict shows exactly which features drove the call. No black box — see the signals behind the score.</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ── result renderer ───────────────────────────────────────────────────────────
def render_result(res, n_fetched=35, about=None, explanation=None, page_url=None):
    if page_url:
        st.markdown(f'<span class="src-link">Source: <a href="{page_url}" target="_blank">{page_url}</a></span>',
                    unsafe_allow_html=True)

    if n_fetched < 35:
        st.markdown(data_bar_html(n_fetched), unsafe_allow_html=True)

    if n_fetched < 8:
        st.markdown(banner_html("crit",
            f"NOT ENOUGH DATA — {n_fetched}/35 SIGNALS",
            "Verdict is mostly historical averages. Check back 2–3 days before listing."),
            unsafe_allow_html=True)
    elif n_fetched < 15:
        st.markdown(banner_html("warn", f"PARTIAL DATA — {n_fetched}/35 SIGNALS",
            "Indicative only — treat as a first read, not a final call."),
            unsafe_allow_html=True)

    # verdict hero
    st.markdown(verdict_hero_html(
        res["verdict"], res["confidence_pct"],
        res["xgb_probabilities"]["invest"], res["company"]),
        unsafe_allow_html=True)

    # about
    if about:
        st.markdown(f"""<div class="g-panel fade-up fade-up-1">
          <div class="g-panel-title">About the company</div>
          <div style="font-size:13.5px;line-height:1.75;color:#9CA3AF">{about}</div>
        </div>""", unsafe_allow_html=True)

    # explanation with bold parsing
    if explanation:
        exp = explanation.replace("**", "\x00", 1)
        while "\x00" in exp:
            exp = exp.replace("\x00", "<b style='color:#E8E6F0'>", 1)
            if "\x00" in exp:
                exp = exp.replace("\x00", "</b>", 1)
        exp = exp.replace("\n\n", "<br/><br/>")
        st.markdown(f"""<div class="g-panel fade-up fade-up-2">
          <div class="g-panel-title">Why {res["verdict"].lower()}? — plain language</div>
          <div style="font-size:13.5px;line-height:1.8;color:#9CA3AF">{exp}</div>
        </div>""", unsafe_allow_html=True)

    left, right = st.columns([1, 1], gap="medium")

    with left:
        # pillar scorecard
        pillar_rows = "".join(
            pillar_bar_html(name, score,
                GREEN if score >= 6.5 else (AMBER if score >= 4 else RED))
            for name, score in res["pillar_scores"].items()
        )
        st.markdown(f'<div class="g-panel fade-up fade-up-3"><div class="g-panel-title">Pillar scorecard</div>{pillar_rows}</div>',
                    unsafe_allow_html=True)

        if res.get("red_flags"):
            flags = "".join(flag_html(f) for f in res["red_flags"])
            st.markdown(f'<div class="g-panel fade-up fade-up-4"><div class="g-panel-title">Red flags</div>{flags}</div>',
                        unsafe_allow_html=True)

    with right:
        # SHAP
        drivers = res["top_drivers"]
        max_abs = max(abs(d["shap"]) for d in drivers) or 1
        driver_rows = "".join(driver_bar_html(d["feature"], d["shap"], max_abs) for d in drivers)
        st.markdown(f'<div class="g-panel fade-up fade-up-3"><div class="g-panel-title">Top model drivers (SHAP)</div>{driver_rows}</div>',
                    unsafe_allow_html=True)

        # probabilities chart
        proba = res["xgb_probabilities"]
        verdicts_list = ["Avoid", "Neutral", "Invest"]
        proba_vals = [proba["avoid"], proba["neutral"], proba["invest"]]
        colors = [RED, AMBER, GREEN]
        fig = go.Figure(go.Bar(
            x=verdicts_list, y=proba_vals,
            marker_color=colors,
            marker_opacity=0.85,
            marker_line_width=0,
            text=[f"{v:.0%}" for v in proba_vals],
            textposition="outside",
            textfont=dict(color="#E8E6F0", size=14, family="JetBrains Mono"),
        ))
        st.markdown('<div class="g-panel fade-up fade-up-4"><div class="g-panel-title">Calibrated probabilities</div>',
                    unsafe_allow_html=True)
        st.plotly_chart(plotly_premium(fig, 220), use_container_width=True,
                        config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

        # nearest comparable
        c = res["nearest_comparable"]
        alpha_color = GREEN if c["alpha_180d"] >= 0 else RED
        st.markdown(f"""<div class="g-panel fade-up fade-up-5">
          <div class="g-panel-title">Nearest historical comparable</div>
          <div class="comp-card">
            <div class="comp-name">{c['company']}</div>
            <div class="comp-meta">{c['sector']} · {c['year']}</div>
            <div class="comp-alpha-lbl">180-day alpha vs Nifty</div>
            <div class="comp-alpha" style="color:{alpha_color}">{c['alpha_180d']:+.1f}%</div>
          </div>
        </div>""", unsafe_allow_html=True)

    # PDF
    pdf = tempfile.mktemp(suffix=".pdf")
    generate_report(res, pdf)
    st.download_button(
        "⬇  Download full PDF report",
        open(pdf, "rb"),
        file_name=f"{res['company']}_report.pdf",
        mime="application/pdf",
        use_container_width=True,
    )
    st.markdown(f'<div class="disclaimer">{res.get("disclaimer","Not investment advice. Model output only — do your own research.")}</div>',
                unsafe_allow_html=True)


# ── sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div style="padding:8px 0 4px"><div style="font-family:Space Grotesk;font-weight:800;font-size:15px;color:#E8E6F0;letter-spacing:-0.03em">IPO <span style="background:linear-gradient(90deg,#4F8EF7,#00D9A3);-webkit-background-clip:text;-webkit-text-fill-color:transparent">Intelligence</span></div></div>',
                unsafe_allow_html=True)

    st.markdown('<div class="sidebar-label">Mode</div>', unsafe_allow_html=True)
    mode = st.radio("", ["Auto-fetch by name", "Manual inputs"], label_visibility="collapsed")

    st.divider()

    if mode == "Manual inputs":
        st.markdown('<div class="sidebar-label">Company</div>', unsafe_allow_html=True)
        company = st.text_input("", "Demo Industries Ltd", label_visibility="collapsed")

        st.markdown('<div class="sidebar-label">Financials</div>', unsafe_allow_html=True)
        f = {}
        f["revenue_cagr_3y"]      = st.slider("Revenue CAGR (3y)",     -0.2, 0.9,  0.25)
        f["pat_margin"]            = st.slider("PAT margin",             -0.25,0.35, 0.10)
        f["ocf_pat_ratio"]         = st.slider("OCF / PAT",             -1.5, 2.5,  0.9)
        f["debt_equity"]           = st.slider("Debt / Equity",          0.0, 6.0,  0.6)
        f["roce"]                  = st.slider("RoCE",                  -0.15,0.6,  0.16)

        st.markdown('<div class="sidebar-label">Valuation &amp; Structure</div>', unsafe_allow_html=True)
        f["pe_vs_peer_median"]     = st.slider("P/E vs peer median",    0.3, 4.0, 1.1)
        f["ofs_pct"]               = st.slider("OFS % of issue",        0.0, 1.0, 0.4)
        f["gcp_pct"]               = st.slider("GCP %",                 0.0, 0.6, 0.1)
        f["promoter_pledge_flag"]  = int(st.checkbox("Promoter pledge"))

        st.markdown('<div class="sidebar-label">Demand &amp; Sentiment</div>', unsafe_allow_html=True)
        f["qib_subscription"]      = st.slider("QIB subscription (x)", 0.1, 200.0, 20.0)
        f["gmp_pct"]               = st.slider("GMP %",               -0.2, 1.2,  0.2)
        f["governance_score"]      = st.slider("Governance score",      1.0, 10.0, 7.0)
        f["bull_regime"]           = int(st.checkbox("Bull market", True))
        run = st.button("Analyse IPO", use_container_width=True)
    else:
        st.markdown('<div class="sidebar-label">Upcoming IPO Name</div>', unsafe_allow_html=True)
        company = st.text_input("", placeholder="e.g. Tata Capital, Swiggy…", label_visibility="collapsed")
        fetch = st.button("Fetch & Analyse", use_container_width=True)

        st.markdown('<div class="sidebar-label">Quick picks</div>', unsafe_allow_html=True)
        for s in ["Tata Capital", "Swiggy", "PhysicsWallah", "NTPC Green", "Hyundai India"]:
            st.markdown(f'<div class="suggestion-chip">→ {s}</div>', unsafe_allow_html=True)


# ── main ──────────────────────────────────────────────────────────────────────
art = pathlib.Path(__file__).resolve().parents[1] / "artifacts"

if mode == "Manual inputs":
    if run:
        with st.spinner("Running model…"):
            res = A.analyze(f, company)
        render_result(res)
    else:
        render_empty(art)
else:
    if fetch and company:
        with st.spinner(f"Searching for '{company}' — scraping DRHP, financials, GMP…"):
            try:
                from pipeline.auto_fetch import fetch_features
                from pipeline.explainer import explain
                features, page, about = fetch_features(company)
                res = A.analyze(features, company)
                ex  = explain(company, res, features, about)
                st.session_state.update({
                    "result": res, "n_fetched": len(features),
                    "about": about or ex["about"],
                    "explanation": ex["explanation"],
                    "page": page,
                })
            except SystemExit as e:
                st.markdown(banner_html("crit", "NOT FOUND", str(e)), unsafe_allow_html=True)
            except Exception as e:
                st.markdown(banner_html("crit", "FETCH FAILED",
                    f"{e} — source may have changed layout, or try Manual mode."),
                    unsafe_allow_html=True)

    if "result" in st.session_state:
        render_result(
            st.session_state["result"],
            st.session_state.get("n_fetched", 35),
            st.session_state.get("about"),
            st.session_state.get("explanation"),
            st.session_state.get("page"),
        )
    else:
        render_empty(art)
