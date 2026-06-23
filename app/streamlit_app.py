"""IPO Intelligence — Clean Dashboard UI.  streamlit run app/streamlit_app.py"""
import sys, pathlib, json, tempfile
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import streamlit as st
import plotly.graph_objects as go
from pipeline.analyze import IPOAnalyzer
from reports.report_generator import generate_report
from app.theme import (
    CSS, GREEN, RED, AMBER, PURPLE, WHITE,
    VERDICT_COLOR, VERDICT_BG,
    verdict_hero_html, banner_html, pillar_bar_html, driver_bar_html,
    flag_html, data_bar_html, metric_card_html, confidence_dial_svg,
)

st.set_page_config(
    page_title="IPO Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(CSS, unsafe_allow_html=True)


@st.cache_resource
def get_analyzer():
    return IPOAnalyzer()
A = get_analyzer()


def plotly_clean(fig, height=230):
    fig.update_layout(
        height=height,
        margin=dict(t=6, b=6, l=0, r=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#9CA3AF", size=11),
        xaxis=dict(
            showgrid=False, zeroline=False,
            tickcolor="#E5E7EB", linecolor="#F3F4F6", color="#9CA3AF",
        ),
        yaxis=dict(visible=False),
        bargap=0.3,
    )
    return fig


# ── top bar ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="ipo-topbar">
  <div class="ipo-topbar-logo">IPO <span>Intelligence</span></div>
  <div class="ipo-topbar-badge">XGB + RL · v1.0</div>
  <div class="ipo-topbar-right">CALIBRATED ON 700 HISTORICAL IPOs · NOT INVESTMENT ADVICE</div>
</div>
""", unsafe_allow_html=True)


# ── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div style="padding:12px 0 4px;font-size:15px;font-weight:800;color:#111827;letter-spacing:-0.03em">IPO <span style="color:#7C3AED">Intelligence</span></div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:11px;color:#9CA3AF;margin-bottom:16px">AI-powered IPO verdict engine</div>', unsafe_allow_html=True)

    st.divider()

    st.markdown('<span class="sb-label">Mode</span>', unsafe_allow_html=True)
    mode = st.radio("", ["Auto-fetch by name", "Manual inputs"], label_visibility="collapsed")

    st.divider()

    if mode == "Manual inputs":
        st.markdown('<span class="sb-label">Company name</span>', unsafe_allow_html=True)
        company = st.text_input("", "Demo Industries Ltd", label_visibility="collapsed")

        st.markdown('<span class="sb-label">Financials</span>', unsafe_allow_html=True)
        f = {}
        f["revenue_cagr_3y"]     = st.slider("Revenue CAGR (3y)",    -0.2, 0.9,  0.25)
        f["pat_margin"]           = st.slider("PAT margin",            -0.25,0.35, 0.10)
        f["ocf_pat_ratio"]        = st.slider("OCF / PAT",             -1.5, 2.5,  0.9)
        f["debt_equity"]          = st.slider("Debt / Equity",          0.0, 6.0,  0.6)
        f["roce"]                 = st.slider("RoCE",                  -0.15,0.6,  0.16)

        st.markdown('<span class="sb-label">Valuation &amp; Structure</span>', unsafe_allow_html=True)
        f["pe_vs_peer_median"]    = st.slider("P/E vs peer median",    0.3, 4.0, 1.1)
        f["ofs_pct"]              = st.slider("OFS % of issue",        0.0, 1.0, 0.4)
        f["gcp_pct"]              = st.slider("GCP %",                 0.0, 0.6, 0.1)
        f["promoter_pledge_flag"] = int(st.checkbox("Promoter pledge"))

        st.markdown('<span class="sb-label">Demand &amp; Sentiment</span>', unsafe_allow_html=True)
        f["qib_subscription"]     = st.slider("QIB subscription (x)", 0.1, 200.0, 20.0)
        f["gmp_pct"]              = st.slider("GMP %",                -0.2, 1.2,  0.2)
        f["governance_score"]     = st.slider("Governance score",      1.0, 10.0, 7.0)
        f["bull_regime"]          = int(st.checkbox("Bull market regime", True))
        run = st.button("Analyse IPO", use_container_width=True)

    else:
        st.markdown('<span class="sb-label">Company name</span>', unsafe_allow_html=True)
        company = st.text_input("", placeholder="e.g. Tata Capital, Swiggy…", label_visibility="collapsed")
        fetch = st.button("Fetch & Analyse", use_container_width=True)

        st.markdown('<span class="sb-label">Quick picks</span>', unsafe_allow_html=True)
        for s in ["Tata Capital", "Swiggy", "PhysicsWallah", "NTPC Green", "Hyundai India"]:
            st.markdown(f'<span class="suggestion-chip">→ {s}</span>', unsafe_allow_html=True)


# ── EMPTY / HERO STATE ───────────────────────────────────────────────────────
def render_empty(art_path):
    st.markdown("""
    <div class="hero-section">
      <div class="hero-eyebrow">
        <span class="hero-eyebrow-dot"></span>
        AI-powered IPO analysis · India
      </div>
      <div class="hero-h1">Should you invest<br/><span class="grad">in this IPO?</span></div>
      <div class="hero-sub">Type any company name in the sidebar. We scrape DRHP filings, run calibrated ML + RL, and return an analyst-grade verdict in seconds.</div>
    </div>
    """, unsafe_allow_html=True)

    # metric cards
    if (art_path / "metrics.json").exists() and (art_path / "rl_metrics.json").exists():
        m = json.loads((art_path / "metrics.json").read_text())
        r = json.loads((art_path / "rl_metrics.json").read_text())

        c1, c2, c3, c4 = st.columns(4, gap="small")
        with c1:
            st.markdown(metric_card_html("Invest Precision", f"{m['invest_precision']:.2f}",
                                         "model accuracy", "up"), unsafe_allow_html=True)
        with c2:
            st.markdown(metric_card_html("Portfolio Alpha", f"{m['portfolio_alpha_180d']:+.1%}",
                                         "vs Nifty 180d", "up"), unsafe_allow_html=True)
        with c3:
            st.markdown(metric_card_html("Hit Rate", f"{m['hit_rate']:.0%}",
                                         "correct verdicts", "up"), unsafe_allow_html=True)
        with c4:
            st.markdown(metric_card_html("RL Improvement", f"+{r['rl_improvement_pct']:.1f}%",
                                         "vs base XGBoost", "up"), unsafe_allow_html=True)

        st.markdown('<div style="margin-bottom:28px"></div>', unsafe_allow_html=True)

    # how it works
    st.markdown('<div style="font-size:13px;font-weight:600;color:#111827;margin-bottom:14px">How it works</div>',
                unsafe_allow_html=True)
    h1, h2, h3 = st.columns(3, gap="small")
    with h1:
        st.markdown("""<div class="hiw-card">
          <span class="hiw-icon">📡</span>
          <div class="hiw-title">Scrape &amp; Fetch</div>
          <div class="hiw-desc">DRHP from SEBI, NSE subscription, grey market premium, and 35 financial signals scraped in real-time.</div>
        </div>""", unsafe_allow_html=True)
    with h2:
        st.markdown("""<div class="hiw-card">
          <span class="hiw-icon">🧠</span>
          <div class="hiw-title">ML + RL Verdict</div>
          <div class="hiw-desc">Calibrated XGBoost on 700 Indian IPOs, overlaid with a REINFORCE agent that self-corrects from outcomes.</div>
        </div>""", unsafe_allow_html=True)
    with h3:
        st.markdown("""<div class="hiw-card">
          <span class="hiw-icon">🔬</span>
          <div class="hiw-title">SHAP Explainability</div>
          <div class="hiw-desc">Every verdict shows exactly which features drove the call. No black box — total transparency.</div>
        </div>""", unsafe_allow_html=True)


# ── RESULT RENDERER ───────────────────────────────────────────────────────────
def render_result(res, n_fetched=35, about=None, explanation=None, page_url=None):
    if page_url:
        st.markdown(f'<span class="src-link">Source: <a href="{page_url}" target="_blank">{page_url}</a></span>',
                    unsafe_allow_html=True)

    # data signal bar
    if n_fetched < 35:
        st.markdown(data_bar_html(n_fetched), unsafe_allow_html=True)

    if n_fetched < 8:
        st.markdown(banner_html("crit",
            f"Not enough data — {n_fetched}/35 signals found",
            "Verdict is mostly historical averages. Check back 2–3 days before listing."),
            unsafe_allow_html=True)
    elif n_fetched < 15:
        st.markdown(banner_html("warn", f"Partial data — {n_fetched}/35 signals",
            "Indicative verdict only — treat as a first read, not a final call."),
            unsafe_allow_html=True)

    # verdict hero
    st.markdown(verdict_hero_html(
        res["verdict"], res["confidence_pct"],
        res["xgb_probabilities"]["invest"], res["company"]),
        unsafe_allow_html=True)

    # quick metric strip
    vc = VERDICT_COLOR[res["verdict"]]
    vb = VERDICT_BG[res["verdict"]]
    proba = res["xgb_probabilities"]
    mc1, mc2, mc3, mc4 = st.columns(4, gap="small")
    with mc1:
        st.markdown(metric_card_html("Confidence", f"{res['confidence_pct']:.0f}%",
                                     res["verdict"], "up" if res["verdict"] == "INVEST" else "down"),
                    unsafe_allow_html=True)
    with mc2:
        st.markdown(metric_card_html("Invest probability", f"{proba['invest']:.0%}"), unsafe_allow_html=True)
    with mc3:
        st.markdown(metric_card_html("Avoid probability",  f"{proba['avoid']:.0%}"), unsafe_allow_html=True)
    with mc4:
        st.markdown(metric_card_html("Neutral probability", f"{proba['neutral']:.0%}"), unsafe_allow_html=True)

    st.markdown('<div style="margin-bottom:6px"></div>', unsafe_allow_html=True)

    # about + explanation
    if about:
        st.markdown(f"""<div class="white-card">
          <div style="font-size:12px;font-weight:600;color:#6B7280;letter-spacing:0.05em;text-transform:uppercase;margin-bottom:10px">About the company</div>
          <div style="font-size:13.5px;line-height:1.75;color:#374151">{about}</div>
        </div>""", unsafe_allow_html=True)

    if explanation:
        exp = explanation.replace("**", "\x00", 1)
        while "\x00" in exp:
            exp = exp.replace("\x00", "<b style='color:#111827'>", 1)
            if "\x00" in exp:
                exp = exp.replace("\x00", "</b>", 1)
        exp = exp.replace("\n\n", "<br/><br/>")
        st.markdown(f"""<div class="white-card">
          <div style="font-size:12px;font-weight:600;color:#6B7280;letter-spacing:0.05em;text-transform:uppercase;margin-bottom:10px">Why {res["verdict"].lower()}? — plain language</div>
          <div style="font-size:13.5px;line-height:1.8;color:#374151">{exp}</div>
        </div>""", unsafe_allow_html=True)

    # two column section
    left, right = st.columns([1, 1], gap="medium")

    with left:
        # pillar scorecard
        pillar_rows = "".join(
            pillar_bar_html(name, score,
                GREEN if score >= 6.5 else (AMBER if score >= 4 else RED))
            for name, score in res["pillar_scores"].items()
        )
        st.markdown(f"""<div class="white-card">
          <div class="section-header">
            <span class="section-title">Pillar scorecard</span>
            <span class="section-sub">out of 10</span>
          </div>
          {pillar_rows}
        </div>""", unsafe_allow_html=True)

        # red flags
        if res.get("red_flags"):
            flags = "".join(flag_html(f) for f in res["red_flags"])
            st.markdown(f"""<div class="white-card">
              <div class="section-header"><span class="section-title">Red flags</span></div>
              {flags}
            </div>""", unsafe_allow_html=True)

    with right:
        # probabilities bar chart
        verdicts_list = ["Avoid", "Neutral", "Invest"]
        proba_vals    = [proba["avoid"], proba["neutral"], proba["invest"]]
        bar_colors    = [RED, AMBER, GREEN]
        fig = go.Figure(go.Bar(
            x=verdicts_list,
            y=proba_vals,
            marker_color=bar_colors,
            marker_opacity=0.85,
            marker_line_width=0,
            text=[f"{v:.0%}" for v in proba_vals],
            textposition="outside",
            textfont=dict(color="#374151", size=13, family="Inter", weight=600),
        ))
        st.markdown("""<div class="white-card" style="margin-bottom:16px">
          <div class="section-header">
            <span class="section-title">Calibrated probabilities</span>
          </div>""", unsafe_allow_html=True)
        st.plotly_chart(plotly_clean(fig, 210), use_container_width=True,
                        config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

        # SHAP drivers
        drivers = res["top_drivers"]
        max_abs = max(abs(d["shap"]) for d in drivers) or 1
        driver_rows = "".join(driver_bar_html(d["feature"], d["shap"], max_abs) for d in drivers)
        st.markdown(f"""<div class="white-card">
          <div class="section-header">
            <span class="section-title">Top model drivers (SHAP)</span>
            <span class="section-sub">← avoid &nbsp; invest →</span>
          </div>
          {driver_rows}
        </div>""", unsafe_allow_html=True)

    # comparable + download row
    comp_col, dl_col = st.columns([2, 1], gap="medium")

    with comp_col:
        c = res["nearest_comparable"]
        alpha_color = GREEN if c["alpha_180d"] >= 0 else RED
        st.markdown(f"""<div class="white-card">
          <div class="section-header"><span class="section-title">Nearest historical comparable</span></div>
          <div class="comp-card">
            <div class="comp-name">{c['company']}</div>
            <div class="comp-meta">{c['sector']} · {c['year']}</div>
            <div class="comp-alpha-lbl">180-day alpha vs Nifty</div>
            <div class="comp-alpha" style="color:{alpha_color}">{c['alpha_180d']:+.1f}%</div>
          </div>
        </div>""", unsafe_allow_html=True)

    with dl_col:
        st.markdown('<div style="margin-top:0px">', unsafe_allow_html=True)
        pdf = tempfile.mktemp(suffix=".pdf")
        generate_report(res, pdf)
        st.download_button(
            "⬇  Download PDF report",
            open(pdf, "rb"),
            file_name=f"{res['company']}_report.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="disclaimer">{res.get("disclaimer","Not investment advice. Model output only — do your own research.")}</div>',
                unsafe_allow_html=True)


# ── MAIN ─────────────────────────────────────────────────────────────────────
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
        with st.spinner(f"Fetching data for '{company}'…"):
            try:
                from pipeline.auto_fetch import fetch_features
                from pipeline.explainer import explain
                features, page, about = fetch_features(company)
                res = A.analyze(features, company)
                ex  = explain(company, res, features, about)
                st.session_state.update({
                    "result": res,
                    "n_fetched": len(features),
                    "about": about or ex["about"],
                    "explanation": ex["explanation"],
                    "page": page,
                })
            except SystemExit as e:
                st.markdown(banner_html("crit", "Not found", str(e)), unsafe_allow_html=True)
            except Exception as e:
                st.markdown(banner_html("crit", "Fetch failed",
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
