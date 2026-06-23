"""IPO Intelligence — Dark Premium UI.  streamlit run app/streamlit_app.py"""
import sys, pathlib, json, tempfile
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import streamlit as st
import plotly.graph_objects as go
from pipeline.analyze import IPOAnalyzer
from reports.report_generator import generate_report
from app.theme import (
    CSS, GREEN, RED, AMBER, ACCENT,
    VERDICT_COLOR, VERDICT_GLOW, VERDICT_DIM,
    verdict_hero_html, banner_html, pillar_bar_html, driver_bar_html,
    flag_html, data_bar_html, confidence_dial_svg,
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
        font=dict(family="JetBrains Mono", color="#6B7280", size=11),
        xaxis=dict(
            showgrid=False, zeroline=False,
            tickcolor="rgba(255,255,255,0.05)",
            linecolor="rgba(255,255,255,0.05)",
            color="#6B7280",
        ),
        yaxis=dict(visible=False),
        bargap=0.3,
    )
    return fig


# ── TOP BAR ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="ipo-topbar">
  <div class="ipo-topbar-dot"></div>
  <div class="ipo-topbar-logo">IPO <span>Intelligence</span></div>
  <div class="ipo-topbar-badge">XGB + RL · v1.0</div>
  <div class="ipo-topbar-tag">700 HISTORICAL IPOs · NOT INVESTMENT ADVICE</div>
</div>
""", unsafe_allow_html=True)


# ── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:18px 0 6px">
      <div style="font-family:'Space Grotesk',sans-serif;font-weight:800;font-size:16px;
                  letter-spacing:-0.04em;color:#F0EEE8">
        IPO <span style="background:linear-gradient(90deg,#818CF8,#34D399);
                         -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                         background-clip:text">Intelligence</span>
      </div>
      <div style="font-family:'JetBrains Mono',monospace;font-size:10px;color:#4B5563;
                  letter-spacing:0.08em;margin-top:5px">AI-POWERED IPO VERDICT ENGINE</div>
    </div>
    """, unsafe_allow_html=True)

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
        f["pat_margin"]           = st.slider("PAT margin",            -0.25, 0.35, 0.10)
        f["ocf_pat_ratio"]        = st.slider("OCF / PAT",             -1.5, 2.5,  0.9)
        f["debt_equity"]          = st.slider("Debt / Equity",          0.0, 6.0,  0.6)
        f["roce"]                 = st.slider("RoCE",                  -0.15, 0.6,  0.16)

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
        run = st.button("⚡ Analyse IPO", use_container_width=True)

    else:
        st.markdown('<span class="sb-label">Company name</span>', unsafe_allow_html=True)
        company = st.text_input("", placeholder="e.g. Tata Capital, Swiggy…", label_visibility="collapsed")
        fetch = st.button("Fetch & Analyse →", use_container_width=True)

        st.markdown('<span class="sb-label">Quick picks</span>', unsafe_allow_html=True)
        for s in ["Tata Capital", "Swiggy", "PhysicsWallah", "NTPC Green", "Hyundai India"]:
            st.markdown(f'<span class="sb-chip">→ {s}</span>', unsafe_allow_html=True)

        st.markdown('<div style="height:28px"></div>', unsafe_allow_html=True)
        st.divider()
        st.markdown("""
        <div style="font-family:'JetBrains Mono',monospace;font-size:9px;color:#374151;
                    line-height:1.9;letter-spacing:0.04em">
          700+ IPOs trained · XGBoost calibrated<br/>
          REINFORCE RL overlay · SHAP explanations<br/>
          Real-time SEBI + GMP + NSE data
        </div>
        """, unsafe_allow_html=True)


# ── METRIC CARD (dark) ───────────────────────────────────────────────────────
def metric_card(label: str, value: str, sub: str = "", color: str = ACCENT):
    return f"""<div class="g-card" style="text-align:center;padding:20px 16px">
  <div style="font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:0.14em;
              text-transform:uppercase;color:#4B5563;margin-bottom:10px">{label}</div>
  <div style="font-family:'JetBrains Mono',monospace;font-size:26px;font-weight:700;
              letter-spacing:-0.03em;color:{color};text-shadow:0 0 20px {color}55;
              line-height:1">{value}</div>
  {f'<div style="font-size:10px;color:#4B5563;margin-top:5px">{sub}</div>' if sub else ''}
</div>"""


# ── EMPTY / HERO STATE ───────────────────────────────────────────────────────
def render_empty(art_path):
    st.markdown("""
    <div class="hero-section">
      <div class="hero-eyebrow">
        <span class="hero-eyebrow-dot"></span>
        AI-powered IPO analysis · India · XGBoost + REINFORCE RL
      </div>
      <div class="hero-h1">Should you invest<br/><span class="grad">in this IPO?</span></div>
      <div class="hero-sub">Type any company name. We scrape SEBI filings, NSE subscription data, and 35 signals — then deliver a verdict in seconds.</div>
    </div>
    """, unsafe_allow_html=True)

    # stat strip
    st.markdown("""<div class="stat-strip">
      <div class="stat-cell"><div class="stat-val">700+</div><div class="stat-lbl">IPOs trained</div></div>
      <div class="stat-cell"><div class="stat-val">80%</div><div class="stat-lbl">Hit rate</div></div>
      <div class="stat-cell"><div class="stat-val">+21%</div><div class="stat-lbl">Alpha 180d</div></div>
      <div class="stat-cell"><div class="stat-val">35</div><div class="stat-lbl">Signals</div></div>
    </div>""", unsafe_allow_html=True)

    # metric cards from artifacts
    if (art_path / "metrics.json").exists() and (art_path / "rl_metrics.json").exists():
        m = json.loads((art_path / "metrics.json").read_text())
        r = json.loads((art_path / "rl_metrics.json").read_text())

        c1, c2, c3, c4 = st.columns(4, gap="small")
        with c1:
            st.markdown(metric_card("Invest Precision", f"{m['invest_precision']:.2f}",
                                    "model accuracy", GREEN), unsafe_allow_html=True)
        with c2:
            st.markdown(metric_card("Portfolio Alpha", f"{m['portfolio_alpha_180d']:+.1%}",
                                    "vs Nifty 180d", GREEN), unsafe_allow_html=True)
        with c3:
            st.markdown(metric_card("Hit Rate", f"{m['hit_rate']:.0%}",
                                    "correct verdicts", ACCENT), unsafe_allow_html=True)
        with c4:
            st.markdown(metric_card("RL Improvement", f"+{r['rl_improvement_pct']:.1f}%",
                                    "vs base XGBoost", ACCENT), unsafe_allow_html=True)

    st.markdown('<div style="height:32px"></div>', unsafe_allow_html=True)

    # how it works
    st.markdown("""<div style="font-family:'JetBrains Mono',monospace;font-size:9px;
      letter-spacing:0.14em;text-transform:uppercase;color:#4B5563;margin-bottom:16px;
      display:flex;align-items:center;gap:8px">
      <span style="width:4px;height:4px;border-radius:50%;background:#818CF8;
                   box-shadow:0 0 6px #818CF8;display:inline-block"></span>
      How it works
    </div>""", unsafe_allow_html=True)

    h1, h2, h3 = st.columns(3, gap="small")
    with h1:
        st.markdown("""<div class="hiw-card">
          <div class="hiw-card-top"></div>
          <span class="hiw-icon">📡</span>
          <div class="hiw-title">Scrape &amp; Fetch</div>
          <div class="hiw-desc">DRHP from SEBI, NSE subscription, grey market premium, and 35 financial signals scraped in real-time.</div>
        </div>""", unsafe_allow_html=True)
    with h2:
        st.markdown("""<div class="hiw-card">
          <div class="hiw-card-top"></div>
          <span class="hiw-icon">🧠</span>
          <div class="hiw-title">ML + RL Verdict</div>
          <div class="hiw-desc">Calibrated XGBoost on 700 Indian IPOs, overlaid with a REINFORCE agent that self-corrects from outcomes.</div>
        </div>""", unsafe_allow_html=True)
    with h3:
        st.markdown("""<div class="hiw-card">
          <div class="hiw-card-top"></div>
          <span class="hiw-icon">🔬</span>
          <div class="hiw-title">SHAP Explainability</div>
          <div class="hiw-desc">Every verdict shows exactly which features drove the call. No black box — total transparency.</div>
        </div>""", unsafe_allow_html=True)


# ── RESULT RENDERER ──────────────────────────────────────────────────────────
def render_result(res, n_fetched=35, about=None, explanation=None, page_url=None):
    if page_url:
        st.markdown(f'<span class="src-link">Source: <a href="{page_url}" target="_blank">{page_url}</a></span>',
                    unsafe_allow_html=True)

    # data signal bar
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

    # probability metric cards
    proba = res["xgb_probabilities"]
    vc = VERDICT_COLOR[res["verdict"]]
    mc1, mc2, mc3, mc4 = st.columns(4, gap="small")
    with mc1:
        st.markdown(metric_card("Confidence", f"{res['confidence_pct']:.0f}%", res["verdict"], vc),
                    unsafe_allow_html=True)
    with mc2:
        st.markdown(metric_card("Invest Prob", f"{proba['invest']:.0%}", "", GREEN),
                    unsafe_allow_html=True)
    with mc3:
        st.markdown(metric_card("Avoid Prob", f"{proba['avoid']:.0%}", "", RED),
                    unsafe_allow_html=True)
    with mc4:
        st.markdown(metric_card("Neutral Prob", f"{proba['neutral']:.0%}", "", AMBER),
                    unsafe_allow_html=True)

    st.markdown('<div style="height:6px"></div>', unsafe_allow_html=True)

    # about
    if about:
        st.markdown(f"""<div class="g-card">
          <div class="g-card-title">About the company</div>
          <div style="font-size:13.5px;line-height:1.8;color:#9CA3AF">{about}</div>
        </div>""", unsafe_allow_html=True)

    # explanation
    if explanation:
        exp = explanation.replace("**", "\x00", 1)
        while "\x00" in exp:
            exp = exp.replace("\x00", "<b style='color:#F0EEE8'>", 1)
            if "\x00" in exp:
                exp = exp.replace("\x00", "</b>", 1)
        exp = exp.replace("\n\n", "<br/><br/>")
        st.markdown(f"""<div class="g-card">
          <div class="g-card-title">Why {res["verdict"].lower()}? — plain language</div>
          <div style="font-size:13.5px;line-height:1.8;color:#9CA3AF">{exp}</div>
        </div>""", unsafe_allow_html=True)

    # two-column: pillar + chart/drivers
    left, right = st.columns([1, 1], gap="medium")

    with left:
        pillar_rows = "".join(
            pillar_bar_html(name, score,
                GREEN if score >= 6.5 else (AMBER if score >= 4 else RED))
            for name, score in res["pillar_scores"].items()
        )
        st.markdown(f"""<div class="g-card">
          <div class="g-card-title">Pillar scorecard</div>
          {pillar_rows}
        </div>""", unsafe_allow_html=True)

        if res.get("red_flags"):
            flags = "".join(flag_html(f) for f in res["red_flags"])
            st.markdown(f"""<div class="g-card">
              <div class="g-card-title">Red flags</div>
              {flags}
            </div>""", unsafe_allow_html=True)

    with right:
        # probability bar chart
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
            textfont=dict(color="#9CA3AF", size=12, family="JetBrains Mono"),
        ))
        st.markdown("""<div class="g-card" style="margin-bottom:16px">
          <div class="g-card-title">Calibrated probabilities</div>""", unsafe_allow_html=True)
        st.plotly_chart(plotly_clean(fig, 200), use_container_width=True,
                        config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

        # SHAP drivers
        drivers = res["top_drivers"]
        max_abs = max(abs(d["shap"]) for d in drivers) or 1
        driver_rows = "".join(driver_bar_html(d["feature"], d["shap"], max_abs) for d in drivers)
        st.markdown(f"""<div class="g-card">
          <div class="g-card-title">Top model drivers (SHAP)</div>
          <div style="display:flex;justify-content:space-between;
                      font-family:'JetBrains Mono',monospace;font-size:9px;
                      color:#374151;margin-bottom:10px;letter-spacing:0.06em">
            <span>← AVOID</span><span>INVEST →</span>
          </div>
          {driver_rows}
        </div>""", unsafe_allow_html=True)

    # comparable + download
    comp_col, dl_col = st.columns([2, 1], gap="medium")

    with comp_col:
        c = res["nearest_comparable"]
        alpha_color = GREEN if c["alpha_180d"] >= 0 else RED
        st.markdown(f"""<div class="g-card">
          <div class="g-card-title">Nearest historical comparable</div>
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
