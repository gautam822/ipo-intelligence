"""IPO Intelligence — Premium UI. Run: streamlit run app/streamlit_app.py"""
import sys, pathlib, json, tempfile
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import streamlit as st
import plotly.graph_objects as go
from pipeline.analyze import IPOAnalyzer
from reports.report_generator import generate_report
from app.theme import (
    CSS, VERDICT_COLOR, VERDICT_GLOW, GREEN, RED, AMBER, STEEL, MUTE, INK,
    verdict_hero_html, banner_html, pillar_bar_html, driver_bar_html,
    flag_html, data_bar_html,
)


def _render_empty(art_path):
    st.markdown("""
    <div class="hero-empty">
      <div class="hero-title">
        Should you invest<br/>
        <span class="gradient-text">in this IPO?</span>
      </div>
      <div class="hero-sub">
        Type any company name in the sidebar. We scrape the filings,
        run the model, and deliver an analyst-grade verdict in seconds.
      </div>
    </div>
    """, unsafe_allow_html=True)

    if (art_path / "metrics.json").exists() and (art_path / "rl_metrics.json").exists():
        m = json.loads((art_path / "metrics.json").read_text())
        r = json.loads((art_path / "rl_metrics.json").read_text())
        st.markdown(f"""
        <div class="metric-strip">
          <div class="metric-cell">
            <div class="metric-val">{m['invest_precision']:.2f}</div>
            <div class="metric-lbl">Invest precision</div>
          </div>
          <div class="metric-cell">
            <div class="metric-val" style="color:#10B981">{m['portfolio_alpha_180d']:+.1%}</div>
            <div class="metric-lbl">Portfolio alpha (180d)</div>
          </div>
          <div class="metric-cell">
            <div class="metric-val">{m['hit_rate']:.0%}</div>
            <div class="metric-lbl">Hit rate</div>
          </div>
          <div class="metric-cell">
            <div class="metric-val" style="color:#10B981">+{r['rl_improvement_pct']:.1f}%</div>
            <div class="metric-lbl">RL vs XGB reward</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="padding: 0 32px 48px">
      <p style="font-family:JetBrains Mono;font-size:10px;letter-spacing:0.1em;text-transform:uppercase;color:#6B7280;margin:0 0 20px;text-align:center">
        HOW IT WORKS
      </p>
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px">
        <div class="g-panel" style="text-align:center">
          <div style="font-size:28px;margin-bottom:12px">📡</div>
          <div style="font-weight:700;font-size:14px;color:#F0EEE8;margin-bottom:8px">Scrape &amp; Fetch</div>
          <div style="font-size:13px;color:#6B7280;line-height:1.6">DRHP from SEBI, NSE subscription, GMP, and 35 financial signals — real-time.</div>
        </div>
        <div class="g-panel" style="text-align:center">
          <div style="font-size:28px;margin-bottom:12px">🧠</div>
          <div style="font-weight:700;font-size:14px;color:#F0EEE8;margin-bottom:8px">ML + RL Verdict</div>
          <div style="font-size:13px;color:#6B7280;line-height:1.6">Calibrated XGBoost on 700 IPOs, with a REINFORCE agent that self-corrects from outcomes.</div>
        </div>
        <div class="g-panel" style="text-align:center">
          <div style="font-size:28px;margin-bottom:12px">🔬</div>
          <div style="font-weight:700;font-size:14px;color:#F0EEE8;margin-bottom:8px">SHAP Explainability</div>
          <div style="font-size:13px;color:#6B7280;line-height:1.6">Every verdict shows exactly which features drove the call. No black box.</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)


st.set_page_config(
    page_title="IPO Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(CSS, unsafe_allow_html=True)

# ── top bar ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="ipo-brand">
  <span class="wordmark">IPO Intelligence</span>
  <span class="badge">XGB + RL · v1.0</span>
  <span class="tagline">CALIBRATED ON 700 HISTORICAL IPOs · NOT INVESTMENT ADVICE</span>
</div>""", unsafe_allow_html=True)

@st.cache_resource
def get_analyzer():
    return IPOAnalyzer()
A = get_analyzer()


def plotly_glass(fig, height=260):
    fig.update_layout(
        height=height,
        margin=dict(t=8, b=8, l=8, r=8),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="JetBrains Mono", color="#6B7280", size=11),
        xaxis=dict(color="#6B7280", tickcolor="#6B7280", gridcolor="rgba(255,255,255,0.05)"),
        yaxis=dict(visible=False, gridcolor="rgba(255,255,255,0.05)"),
    )
    return fig


def render_result(res, n_fetched=35, about=None, explanation=None, page_url=None):
    # ── source link ──
    if page_url:
        st.markdown(f'<span class="src-link">Source: <a href="{page_url}" target="_blank">{page_url}</a></span>',
                    unsafe_allow_html=True)

    # ── data quality bar ──
    if n_fetched < 35:
        st.markdown(data_bar_html(n_fetched), unsafe_allow_html=True)

    if n_fetched < 8:
        st.markdown(banner_html("crit",
            f"NOT ENOUGH DATA — {n_fetched}/35 SIGNALS FOUND",
            "Verdict is mostly typical-IPO averages. Check back 2–3 days before listing."),
            unsafe_allow_html=True)
    elif n_fetched < 15:
        st.markdown(banner_html("warn", f"PARTIAL DATA — {n_fetched}/35 SIGNALS",
            "Indicative verdict only — treat as a first read, not a final call."),
            unsafe_allow_html=True)

    # ── verdict hero ──
    st.markdown(verdict_hero_html(
        res["verdict"], res["confidence_pct"],
        res["xgb_probabilities"]["invest"], res["company"]),
        unsafe_allow_html=True)

    # ── about + explanation ──
    if about:
        st.markdown(f"""<div class="g-panel">
          <div class="g-panel-title">About the company</div>
          <div style="font-size:14px;line-height:1.75;color:#D1CFC9">{about}</div>
        </div>""", unsafe_allow_html=True)

    if explanation:
        exp_html = explanation.replace("**", "<b>", 1)
        while "**" in exp_html:
            exp_html = exp_html.replace("**", "</b>", 1)
        exp_html = exp_html.replace("\n\n", "<br/><br/>")
        st.markdown(f"""<div class="g-panel">
          <div class="g-panel-title">Why {res["verdict"].lower()}? — plain language</div>
          <div style="font-size:14px;line-height:1.8;color:#D1CFC9">{exp_html}</div>
        </div>""", unsafe_allow_html=True)

    # ── main grid ──
    left, right = st.columns([1, 1], gap="medium")

    with left:
        # pillar scorecard
        pillar_rows = "".join(
            pillar_bar_html(name, score,
                GREEN if score >= 6.5 else (AMBER if score >= 4 else RED))
            for name, score in res["pillar_scores"].items()
        )
        st.markdown(f'<div class="g-panel"><div class="g-panel-title">Pillar scorecard</div>{pillar_rows}</div>',
                    unsafe_allow_html=True)

        # red flags
        if res.get("red_flags"):
            flags_html = "".join(flag_html(f) for f in res["red_flags"])
            st.markdown(f'<div class="g-panel"><div class="g-panel-title">Red flags</div>{flags_html}</div>',
                        unsafe_allow_html=True)

    with right:
        # SHAP drivers
        drivers = res["top_drivers"]
        max_abs = max(abs(d["shap"]) for d in drivers) or 1
        driver_rows = "".join(driver_bar_html(d["feature"], d["shap"], max_abs) for d in drivers)
        st.markdown(f'<div class="g-panel"><div class="g-panel-title">Top model drivers (SHAP)</div>{driver_rows}</div>',
                    unsafe_allow_html=True)

        # calibrated probabilities chart
        proba = res["xgb_probabilities"]
        fig = go.Figure(go.Bar(
            x=["Avoid", "Neutral", "Invest"],
            y=[proba["avoid"], proba["neutral"], proba["invest"]],
            marker_color=[RED, AMBER, GREEN],
            marker_opacity=0.85,
            text=[f"{v:.0%}" for v in [proba["avoid"], proba["neutral"], proba["invest"]]],
            textposition="outside",
            textfont=dict(color="#F0EEE8", size=13, family="JetBrains Mono"),
        ))
        fig.update_traces(marker_line_width=0)
        st.markdown('<div class="g-panel"><div class="g-panel-title">Calibrated probabilities</div>',
                    unsafe_allow_html=True)
        st.plotly_chart(plotly_glass(fig, 220), use_container_width=True,
                        config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

        # nearest comparable
        c = res["nearest_comparable"]
        alpha_color = GREEN if c["alpha_180d"] >= 0 else RED
        st.markdown(f"""<div class="g-panel">
          <div class="g-panel-title">Nearest historical comparable</div>
          <div class="comp-card">
            <div style="font-weight:600;font-size:15px;margin-bottom:4px">{c['company']}</div>
            <div style="font-size:11px;color:#6B7280;font-family:JetBrains Mono;margin-bottom:12px">{c['sector']} · {c['year']}</div>
            <div style="font-size:12px;color:#6B7280;margin-bottom:2px">180-day alpha vs Nifty</div>
            <div class="comp-alpha" style="color:{alpha_color}">{c['alpha_180d']:+.1f}%</div>
          </div>
        </div>""", unsafe_allow_html=True)

    # ── PDF download ──
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


# ── sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p style="font-family:JetBrains Mono;font-size:10px;letter-spacing:0.1em;text-transform:uppercase;color:#6B7280;margin:4px 0 10px">MODE</p>',
                unsafe_allow_html=True)
    mode = st.radio("", ["Auto-fetch by name", "Manual inputs"], label_visibility="collapsed")

    st.markdown("---")

    if mode == "Manual inputs":
        st.markdown('<p style="font-family:JetBrains Mono;font-size:10px;letter-spacing:0.1em;text-transform:uppercase;color:#6B7280;margin:0 0 6px">COMPANY</p>',
                    unsafe_allow_html=True)
        company = st.text_input("", "Demo Industries Ltd", label_visibility="collapsed")

        st.markdown('<p style="font-family:JetBrains Mono;font-size:10px;letter-spacing:0.1em;text-transform:uppercase;color:#6B7280;margin:16px 0 8px">FINANCIALS</p>',
                    unsafe_allow_html=True)
        f = {}
        f["revenue_cagr_3y"]  = st.slider("Revenue CAGR (3y)",    -0.2, 0.9,  0.25)
        f["pat_margin"]        = st.slider("PAT margin",            -0.25, 0.35, 0.10)
        f["ocf_pat_ratio"]     = st.slider("OCF / PAT",             -1.5, 2.5,  0.9)
        f["debt_equity"]       = st.slider("Debt / Equity",          0.0, 6.0,  0.6)
        f["roce"]              = st.slider("RoCE",                  -0.15, 0.6,  0.16)

        st.markdown('<p style="font-family:JetBrains Mono;font-size:10px;letter-spacing:0.1em;text-transform:uppercase;color:#6B7280;margin:16px 0 8px">VALUATION & STRUCTURE</p>',
                    unsafe_allow_html=True)
        f["pe_vs_peer_median"] = st.slider("P/E vs peer median",    0.3, 4.0,  1.1)
        f["ofs_pct"]           = st.slider("OFS % of issue",        0.0, 1.0,  0.4)
        f["gcp_pct"]           = st.slider("General corp. purposes", 0.0, 0.6,  0.1)
        f["promoter_pledge_flag"] = int(st.checkbox("Promoter pledge exists"))

        st.markdown('<p style="font-family:JetBrains Mono;font-size:10px;letter-spacing:0.1em;text-transform:uppercase;color:#6B7280;margin:16px 0 8px">DEMAND & SENTIMENT</p>',
                    unsafe_allow_html=True)
        f["qib_subscription"]  = st.slider("QIB subscription (x)", 0.1, 200.0, 20.0)
        f["gmp_pct"]           = st.slider("Grey market premium %", -0.2, 1.2,  0.2)
        f["governance_score"]  = st.slider("Governance score",       1.0, 10.0, 7.0)
        f["bull_regime"]       = int(st.checkbox("Bull market regime", True))
        run = st.button("Analyse IPO", use_container_width=True)
    else:
        st.markdown('<p style="font-family:JetBrains Mono;font-size:10px;letter-spacing:0.1em;text-transform:uppercase;color:#6B7280;margin:0 0 6px">UPCOMING IPO NAME</p>',
                    unsafe_allow_html=True)
        company = st.text_input("", placeholder="e.g. Tata Capital", label_visibility="collapsed")
        fetch = st.button("Fetch & analyse", use_container_width=True)

        st.markdown("""<div style="margin-top:24px">
          <p style="font-family:JetBrains Mono;font-size:10px;letter-spacing:0.1em;text-transform:uppercase;color:#6B7280;margin:0 0 10px">TRY THESE</p>
        """, unsafe_allow_html=True)
        suggestions = ["Tata Capital", "Swiggy", "PhysicsWallah", "NTPC Green", "Hyundai India"]
        for s in suggestions:
            st.markdown(f'<div style="font-size:12px;color:#9CA3AF;font-family:JetBrains Mono;padding:4px 0;border-bottom:1px solid rgba(255,255,255,0.05)">→ {s}</div>',
                        unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


# ── main area ────────────────────────────────────────────────────────────────
art = pathlib.Path(__file__).resolve().parents[1] / "artifacts"

if mode == "Manual inputs":
    if run:
        res = A.analyze(f, company)
        render_result(res)
    else:
        _render_empty(art)

else:
    if fetch and company:
        with st.spinner(f"Searching for '{company}' across IPO trackers..."):
            try:
                from pipeline.auto_fetch import fetch_features
                from pipeline.explainer import explain
                features, page, about = fetch_features(company)
                res = A.analyze(features, company)
                ex = explain(company, res, features, about)
                st.session_state["result"]      = res
                st.session_state["n_fetched"]   = len(features)
                st.session_state["about"]       = about or ex["about"]
                st.session_state["explanation"] = ex["explanation"]
                st.session_state["page"]        = page
            except SystemExit as e:
                st.markdown(banner_html("crit", "NOT FOUND", str(e)), unsafe_allow_html=True)
            except Exception as e:
                st.markdown(banner_html("crit", "FETCH FAILED",
                    f"{e} — source layout may have changed, or try Manual mode."),
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
        _render_empty(art)
