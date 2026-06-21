"""IPO Intelligence — terminal-styled demo UI.  Run: streamlit run app/streamlit_app.py"""
import sys, pathlib, json, tempfile
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import streamlit as st
import plotly.graph_objects as go
from pipeline.analyze import IPOAnalyzer
from reports.report_generator import generate_report
from app.theme import (CSS, VERDICT_COLOR, GREEN, RED, AMBER, STEEL, PAPER, MUTE, PANEL, LINE,
                       verdict_hero_html, banner_html, pillar_bar_html, driver_bar_html, flag_html)

st.set_page_config(page_title="IPO Intelligence", layout="wide", initial_sidebar_state="expanded")
st.markdown(CSS, unsafe_allow_html=True)

st.markdown("""
<div class="brand">
  <span class="mark">IPO Intelligence</span>
  <span class="tick">XGB + RL · v1.0</span>
  <span class="sub">CALIBRATED ON 700 HISTORICAL IPOs · NOT INVESTMENT ADVICE</span>
</div>""", unsafe_allow_html=True)

@st.cache_resource
def get_analyzer():
    return IPOAnalyzer()
A = get_analyzer()

def plotly_dark_layout(fig, height=320):
    fig.update_layout(
        height=height, margin=dict(t=10, b=10, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="IBM Plex Mono", color=MUTE, size=11),
    )
    return fig


def render_result(res, n_fetched=35, about=None, explanation=None):
    if n_fetched < 8:
        st.markdown(banner_html("crit",
            f"NOT ENOUGH DATA — {n_fetched}/35 SIGNALS FOUND",
            "The verdict below is unreliable, mostly typical-IPO averages rather than "
            "this company's real numbers. Check back once subscription opens "
            "(2–3 days before listing)."), unsafe_allow_html=True)
    elif n_fetched < 15:
        st.markdown(banner_html("warn", f"PARTIAL DATA — {n_fetched}/35 SIGNALS",
            "Verdict is indicative only — treat as a first read, not a final call."),
            unsafe_allow_html=True)

    st.markdown(verdict_hero_html(res["verdict"], res["confidence_pct"],
                                  res["xgb_probabilities"]["invest"], res["company"]),
               unsafe_allow_html=True)

    if about:
        st.markdown(f'<div class="panel"><div class="panel-title">About the company</div>'
                    f'<div style="font-size:14px;line-height:1.7;color:{PAPER}">{about}</div></div>',
                    unsafe_allow_html=True)
    if explanation:
        exp_html = explanation.replace(chr(10)+chr(10), "<br/><br/>")
        st.markdown(f'<div class="panel"><div class="panel-title">Why {res["verdict"].lower()}? '
                    f'— plain language</div><div style="font-size:14px;line-height:1.8;color:{PAPER}">'
                    f'{exp_html}</div></div>',
                    unsafe_allow_html=True)

    left, right = st.columns([1, 1], gap="medium")
    with left:
        st.markdown('<div class="panel"><div class="panel-title">Pillar scorecard</div>',
                    unsafe_allow_html=True)
        for name, score in res["pillar_scores"].items():
            color = GREEN if score >= 6.5 else (AMBER if score >= 4 else RED)
            st.markdown(pillar_bar_html(name, score, color), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="panel"><div class="panel-title">Red flags</div>',
                    unsafe_allow_html=True)
        for fl in res["red_flags"]:
            st.markdown(flag_html(fl), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="panel"><div class="panel-title">Top model drivers (SHAP)</div>',
                    unsafe_allow_html=True)
        drivers = res["top_drivers"]
        max_abs = max(abs(d["shap"]) for d in drivers) or 1
        for d in drivers:
            st.markdown(driver_bar_html(d["feature"], d["shap"], max_abs), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        c = res["nearest_comparable"]
        alpha_color = GREEN if c["alpha_180d"] >= 0 else RED
        st.markdown(f"""<div class="panel"><div class="panel-title">Nearest historical comparable</div>
          <div class="comp-card">
            <b>{c['company']}</b> · {c['sector']} · {c['year']}<br/>
            <span style="color:{MUTE}">180-day alpha vs Nifty:</span>
            <span class="alpha" style="color:{alpha_color}"> {c['alpha_180d']:+.1f}%</span>
          </div></div>""", unsafe_allow_html=True)

        proba = res["xgb_probabilities"]
        fig = go.Figure(go.Bar(
            x=["Avoid", "Neutral", "Invest"], y=[proba["avoid"], proba["neutral"], proba["invest"]],
            marker_color=[RED, AMBER, GREEN], text=[f"{v:.0%}" for v in proba.values()],
            textposition="outside", textfont=dict(color=PAPER)))
        fig.update_layout(yaxis=dict(visible=False), xaxis=dict(color=PAPER))
        st.markdown('<div class="panel"><div class="panel-title">Calibrated probabilities</div>',
                    unsafe_allow_html=True)
        st.plotly_chart(plotly_dark_layout(fig, 220), use_container_width=True,
                        config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    pdf = tempfile.mktemp(suffix=".pdf")
    generate_report(res, pdf)
    st.download_button("Download full PDF report", open(pdf, "rb"),
                       file_name=f"{res['company']}_report.pdf", mime="application/pdf",
                       use_container_width=True)
    st.markdown(f'<div class="disclaimer">{res["disclaimer"]}</div>', unsafe_allow_html=True)


# ============================================================== sidebar
with st.sidebar:
    st.markdown('<p class="panel-title" style="margin-top:0">Mode</p>', unsafe_allow_html=True)
    mode = st.radio("", ["Auto-fetch by name", "Manual inputs"], label_visibility="collapsed")

    if mode == "Manual inputs":
        st.markdown('<p class="panel-title">Company</p>', unsafe_allow_html=True)
        company = st.text_input("", "Demo Industries Ltd", label_visibility="collapsed")
        st.markdown('<p class="panel-title">Financials</p>', unsafe_allow_html=True)
        f = {}
        f["revenue_cagr_3y"] = st.slider("Revenue CAGR (3y)", -0.2, 0.9, 0.25)
        f["pat_margin"] = st.slider("PAT margin", -0.25, 0.35, 0.10)
        f["ocf_pat_ratio"] = st.slider("OCF / PAT", -1.5, 2.5, 0.9)
        f["debt_equity"] = st.slider("Debt / Equity", 0.0, 6.0, 0.6)
        f["roce"] = st.slider("RoCE", -0.15, 0.6, 0.16)
        st.markdown('<p class="panel-title">Valuation & structure</p>', unsafe_allow_html=True)
        f["pe_vs_peer_median"] = st.slider("P/E vs peer median", 0.3, 4.0, 1.1)
        f["ofs_pct"] = st.slider("OFS % of issue", 0.0, 1.0, 0.4)
        f["gcp_pct"] = st.slider("General corp. purposes %", 0.0, 0.6, 0.1)
        f["promoter_pledge_flag"] = int(st.checkbox("Promoter pledge exists"))
        st.markdown('<p class="panel-title">Demand & sentiment</p>', unsafe_allow_html=True)
        f["qib_subscription"] = st.slider("QIB subscription (x)", 0.1, 200.0, 20.0)
        f["gmp_pct"] = st.slider("Grey market premium %", -0.2, 1.2, 0.2)
        f["governance_score"] = st.slider("Governance score (LLM)", 1.0, 10.0, 7.0)
        f["bull_regime"] = int(st.checkbox("Bull market regime", True))
        run = st.button("Analyse IPO", use_container_width=True)
    else:
        st.markdown('<p class="panel-title">Upcoming IPO name</p>', unsafe_allow_html=True)
        company = st.text_input("", placeholder="e.g. Tata Capital", label_visibility="collapsed")
        fetch = st.button("Fetch & analyse", use_container_width=True)


# ============================================================== main area
if mode == "Manual inputs":
    if run:
        res = A.analyze(f, company)
        render_result(res)
    else:
        st.markdown(f'<div class="panel" style="text-align:center;padding:60px 20px;color:{MUTE}">'
                    'Set parameters in the sidebar and click <b style="color:'+PAPER+'">Analyse IPO</b>'
                    '</div>', unsafe_allow_html=True)
else:
    if fetch and company:
        with st.spinner(f"Searching trackers, scraping data for '{company}'..."):
            try:
                from pipeline.auto_fetch import fetch_features
                from pipeline.explainer import explain
                f, page, about = fetch_features(company)
                res = A.analyze(f, company)
                ex = explain(company, res, f, about)
                st.session_state["result"] = res
                st.session_state["n_fetched"] = len(f)
                st.session_state["about"] = about or ex["about"]
                st.session_state["explanation"] = ex["explanation"]
                st.session_state["page"] = page
            except SystemExit as e:
                st.markdown(banner_html("crit", "NOT FOUND", str(e)), unsafe_allow_html=True)
            except Exception as e:
                st.markdown(banner_html("crit", "FETCH FAILED",
                    f"{e} — source layout may have changed, or try Manual mode."),
                    unsafe_allow_html=True)

    if "result" in st.session_state:
        st.caption(f"Source: {st.session_state.get('page','')}")
        render_result(st.session_state["result"], st.session_state.get("n_fetched", 35),
                     st.session_state.get("about"), st.session_state.get("explanation"))
    else:
        art = pathlib.Path(__file__).resolve().parents[1] / "artifacts"
        st.markdown(f'<div class="panel" style="text-align:center;padding:50px 20px;color:{MUTE}">'
                    'Type an IPO name in the sidebar and click <b style="color:'+PAPER+'">Fetch & analyse</b>'
                    '</div>', unsafe_allow_html=True)
        if (art/"metrics.json").exists():
            m = json.loads((art/"metrics.json").read_text())
            r = json.loads((art/"rl_metrics.json").read_text())
            st.markdown('<div class="panel"><div class="panel-title">Model card — held-out 2023–24 test set</div>',
                       unsafe_allow_html=True)
            c = st.columns(4)
            specs = [("Invest precision", f"{m['invest_precision']:.2f}"),
                     ("Portfolio alpha (180d)", f"{m['portfolio_alpha_180d']:+.1%}"),
                     ("Hit rate", f"{m['hit_rate']:.0%}"),
                     ("RL vs XGB reward", f"+{r['rl_improvement_pct']:.1f}%")]
            for col, (label, val) in zip(c, specs):
                col.markdown(f'<div style="font-family:IBM Plex Mono;font-size:22px;color:{PAPER}">{val}</div>'
                            f'<div style="font-size:11px;color:{MUTE}">{label}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
