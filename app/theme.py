"""
IPO Intelligence — Clean Light Dashboard Theme
Inspired by modern SaaS analytics dashboards
Purple accent · White surface · Rounded cards
"""

PURPLE      = "#7C3AED"
PURPLE_LIGHT= "#EDE9FE"
PURPLE_MID  = "#DDD6FE"
PURPLE_SOFT = "#F5F3FF"
GREEN       = "#059669"
GREEN_LIGHT = "#D1FAE5"
RED         = "#DC2626"
RED_LIGHT   = "#FEE2E2"
AMBER       = "#D97706"
AMBER_LIGHT = "#FEF3C7"
GRAY_900    = "#111827"
GRAY_700    = "#374151"
GRAY_500    = "#6B7280"
GRAY_400    = "#9CA3AF"
GRAY_200    = "#E5E7EB"
GRAY_100    = "#F3F4F6"
GRAY_50     = "#F9FAFB"
WHITE       = "#FFFFFF"

VERDICT_COLOR = {"INVEST": GREEN,  "AVOID": RED,  "NEUTRAL": AMBER}
VERDICT_BG    = {"INVEST": GREEN_LIGHT, "AVOID": RED_LIGHT, "NEUTRAL": AMBER_LIGHT}

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif; -webkit-font-smoothing: antialiased; }

/* ── kill streamlit chrome ── */
#MainMenu, header[data-testid="stHeader"], footer { visibility: hidden; height: 0 !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stAppViewContainer"] { padding: 0 !important; }

/* ── page background ── */
.stApp { background: #F8F7FF !important; }

/* ── sidebar ── */
[data-testid="stSidebar"] {
  background: #FFFFFF !important;
  border-right: 1px solid #E5E7EB !important;
}
[data-testid="stSidebar"] * { color: #374151 !important; }
[data-testid="stSidebar"] .stTextInput input {
  background: #F9FAFB !important;
  border: 1px solid #E5E7EB !important;
  color: #111827 !important;
  border-radius: 10px !important;
  font-family: 'Inter', sans-serif !important;
  font-size: 13px !important;
  padding: 10px 14px !important;
  transition: all 0.2s !important;
}
[data-testid="stSidebar"] .stTextInput input:focus {
  border-color: #7C3AED !important;
  box-shadow: 0 0 0 3px rgba(124,58,237,0.1) !important;
  background: #FFFFFF !important;
}
[data-testid="stSidebar"] .stTextInput input::placeholder { color: #9CA3AF !important; }

/* ── primary button ── */
.stButton > button {
  background: #7C3AED !important;
  color: #FFFFFF !important;
  border: none !important;
  font-family: 'Inter', sans-serif !important;
  font-weight: 600 !important;
  font-size: 13.5px !important;
  border-radius: 10px !important;
  padding: 11px 20px !important;
  letter-spacing: 0.01em !important;
  transition: all 0.2s !important;
  box-shadow: 0 1px 3px rgba(124,58,237,0.3), 0 4px 12px rgba(124,58,237,0.15) !important;
}
.stButton > button:hover {
  background: #6D28D9 !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 4px 16px rgba(124,58,237,0.35) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── download button ── */
.stDownloadButton > button {
  background: #FFFFFF !important;
  color: #374151 !important;
  border: 1px solid #E5E7EB !important;
  font-family: 'Inter', sans-serif !important;
  font-weight: 600 !important;
  border-radius: 10px !important;
  transition: all 0.2s !important;
}
.stDownloadButton > button:hover {
  background: #F9FAFB !important;
  border-color: #7C3AED !important;
  color: #7C3AED !important;
}

/* ── radio ── */
[role="radiogroup"] label { color: #374151 !important; font-size: 13px !important; }
[data-baseweb="radio"] [data-checked="true"] div { background: #7C3AED !important; border-color: #7C3AED !important; }

/* ── sliders ── */
[data-baseweb="slider"] [role="slider"] { background: #7C3AED !important; }
[data-baseweb="slider"] div[class*="Track"] div:first-child { background: #7C3AED !important; }

/* ── divider ── */
hr { border-color: #E5E7EB !important; }

/* ── spinner ── */
.stSpinner > div { border-top-color: #7C3AED !important; }

/* ── scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #E5E7EB; border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: #D1D5DB; }

/* ── top bar ── */
.ipo-topbar {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 28px;
  background: #FFFFFF;
  border-bottom: 1px solid #F3F4F6;
  position: sticky;
  top: 0;
  z-index: 100;
}
.ipo-topbar-logo {
  font-weight: 800;
  font-size: 16px;
  color: #111827;
  letter-spacing: -0.03em;
}
.ipo-topbar-logo span { color: #7C3AED; }
.ipo-topbar-badge {
  font-family: 'JetBrains Mono', monospace;
  font-size: 9px;
  letter-spacing: 0.1em;
  color: #7C3AED;
  background: #EDE9FE;
  border-radius: 6px;
  padding: 3px 8px;
  font-weight: 500;
}
.ipo-topbar-right {
  margin-left: auto;
  font-size: 11px;
  color: #9CA3AF;
  font-family: 'JetBrains Mono', monospace;
  letter-spacing: 0.04em;
}

/* ── main content padding ── */
.main-pad { padding: 24px 28px; }

/* ── page heading ── */
.page-title {
  font-size: 22px;
  font-weight: 700;
  color: #111827;
  letter-spacing: -0.02em;
  margin-bottom: 2px;
}
.page-subtitle { font-size: 13px; color: #6B7280; margin-bottom: 24px; }

/* ── metric card ── */
.metric-card {
  background: #FFFFFF;
  border: 1px solid #F3F4F6;
  border-radius: 16px;
  padding: 20px 22px;
  transition: box-shadow 0.2s, border-color 0.2s;
  height: 100%;
}
.metric-card:hover {
  box-shadow: 0 4px 16px rgba(0,0,0,0.06);
  border-color: #E5E7EB;
}
.metric-card-label {
  font-size: 12px;
  color: #6B7280;
  font-weight: 500;
  letter-spacing: 0.01em;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 6px;
}
.metric-card-label .dot {
  width: 6px; height: 6px;
  border-radius: 50%;
  background: #7C3AED;
  display: inline-block;
}
.metric-card-val {
  font-size: 28px;
  font-weight: 700;
  color: #111827;
  letter-spacing: -0.03em;
  line-height: 1;
  margin-bottom: 8px;
}
.metric-card-delta {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  font-weight: 600;
  padding: 3px 8px;
  border-radius: 6px;
}
.metric-card-delta.up   { background: #D1FAE5; color: #059669; }
.metric-card-delta.down { background: #FEE2E2; color: #DC2626; }
.metric-card-delta.neutral { background: #FEF3C7; color: #D97706; }

/* ── section header ── */
.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
}
.section-title {
  font-size: 14px;
  font-weight: 600;
  color: #111827;
  letter-spacing: -0.01em;
}
.section-sub { font-size: 11px; color: #9CA3AF; }

/* ── white card ── */
.white-card {
  background: #FFFFFF;
  border: 1px solid #F3F4F6;
  border-radius: 16px;
  padding: 20px 22px;
  margin-bottom: 16px;
  transition: box-shadow 0.2s;
}
.white-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.05); }

/* ── verdict badge ── */
.verdict-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  padding: 4px 12px;
  border-radius: 8px;
}

/* ── verdict hero ── */
.verdict-hero {
  background: #FFFFFF;
  border: 1px solid #F3F4F6;
  border-radius: 20px;
  padding: 28px 32px;
  display: flex;
  align-items: center;
  gap: 32px;
  margin-bottom: 16px;
  position: relative;
  overflow: hidden;
}
.verdict-hero::before {
  content: '';
  position: absolute;
  right: -40px; top: -40px;
  width: 200px; height: 200px;
  border-radius: 50%;
  background: radial-gradient(circle, var(--vc-soft) 0%, transparent 70%);
  pointer-events: none;
}
.verdict-word {
  font-size: 52px;
  font-weight: 800;
  letter-spacing: -0.04em;
  color: var(--vc);
  line-height: 1;
}
.verdict-company {
  font-size: 11px;
  color: #9CA3AF;
  font-weight: 500;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  margin-bottom: 8px;
}
.verdict-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: var(--vc-soft);
  color: var(--vc);
  font-size: 12px;
  font-weight: 600;
  padding: 5px 12px;
  border-radius: 8px;
  margin-top: 10px;
  margin-right: 8px;
}

/* ── pillar bars ── */
.pillar-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 9px 0;
  border-bottom: 1px solid #F9FAFB;
}
.pillar-row:last-child { border-bottom: none; }
.pillar-name { font-size: 12.5px; color: #374151; font-weight: 500; width: 140px; flex-shrink: 0; }
.pillar-track { flex: 1; height: 6px; background: #F3F4F6; border-radius: 99px; overflow: hidden; }
.pillar-fill  { height: 100%; border-radius: 99px; }
.pillar-score { font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #9CA3AF; width: 28px; text-align: right; }

/* ── driver bars ── */
.driver {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 0;
}
.driver-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  color: #9CA3AF;
  width: 150px;
  flex-shrink: 0;
  text-align: right;
}
.driver-bar-wrap { flex: 1; height: 20px; position: relative; background: #F3F4F6; border-radius: 5px; }
.driver-center   { position: absolute; left: 50%; top: 0; width: 1px; height: 100%; background: #E5E7EB; }
.driver-bar      { position: absolute; top: 2px; height: calc(100% - 4px); border-radius: 4px; }

/* ── flag rows ── */
.flag-row {
  display: flex;
  gap: 10px;
  padding: 9px 0;
  border-bottom: 1px solid #F9FAFB;
  font-size: 13px;
  color: #374151;
  line-height: 1.55;
  align-items: flex-start;
}
.flag-row:last-child { border-bottom: none; }
.flag-dot { width: 5px; height: 5px; border-radius: 50%; background: #DC2626; margin-top: 7px; flex-shrink: 0; }

/* ── comparable card ── */
.comp-card {
  background: #F9FAFB;
  border: 1px solid #F3F4F6;
  border-radius: 12px;
  padding: 16px;
}
.comp-name  { font-weight: 600; font-size: 14px; color: #111827; margin-bottom: 2px; }
.comp-meta  { font-size: 11px; color: #9CA3AF; margin-bottom: 12px; font-family: 'JetBrains Mono', monospace; }
.comp-alpha { font-family: 'JetBrains Mono', monospace; font-weight: 700; font-size: 22px; }
.comp-alpha-lbl { font-size: 10px; color: #9CA3AF; margin-bottom: 3px; }

/* ── alert banners ── */
.alert-banner {
  border-radius: 12px;
  padding: 12px 16px;
  margin-bottom: 14px;
  font-size: 13px;
  line-height: 1.6;
  border: 1px solid;
  display: flex;
  gap: 10px;
  align-items: flex-start;
}
.alert-banner.crit { background: #FEF2F2; border-color: #FECACA; color: #991B1B; }
.alert-banner.warn { background: #FFFBEB; border-color: #FDE68A; color: #92400E; }
.alert-banner b { color: #111827; }

/* ── data signal bar ── */
.data-signal-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  background: #F9FAFB;
  border: 1px solid #F3F4F6;
  border-radius: 10px;
  padding: 9px 14px;
  margin-bottom: 12px;
}
.data-signal-label { font-size: 11px; font-weight: 600; font-family: 'JetBrains Mono', monospace; letter-spacing: 0.05em; white-space: nowrap; }
.data-signal-track { flex: 1; height: 4px; background: #E5E7EB; border-radius: 99px; overflow: hidden; }
.data-signal-fill  { height: 100%; border-radius: 99px; background: linear-gradient(90deg, #7C3AED, #10B981); }
.data-signal-count { font-size: 11px; color: #9CA3AF; font-family: 'JetBrains Mono', monospace; white-space: nowrap; }

/* ── source link ── */
.src-link { font-size: 11px; color: #9CA3AF; display: block; margin-bottom: 10px; }
.src-link a { color: #7C3AED; text-decoration: none; }
.src-link a:hover { text-decoration: underline; }

/* ── disclaimer ── */
.disclaimer {
  font-size: 11px;
  color: #9CA3AF;
  line-height: 1.7;
  border-top: 1px solid #F3F4F6;
  padding-top: 14px;
  margin-top: 10px;
  text-align: center;
  font-family: 'JetBrains Mono', monospace;
}

/* ── hero empty ── */
.hero-section { padding: 36px 0 28px; }
.hero-eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  font-size: 11px;
  font-weight: 600;
  color: #7C3AED;
  background: #EDE9FE;
  border-radius: 99px;
  padding: 5px 14px;
  margin-bottom: 20px;
  letter-spacing: 0.02em;
}
.hero-eyebrow-dot { width: 5px; height: 5px; border-radius: 50%; background: #7C3AED; }
.hero-h1 {
  font-size: clamp(32px, 4vw, 52px);
  font-weight: 800;
  letter-spacing: -0.04em;
  line-height: 1.1;
  color: #111827;
  margin-bottom: 16px;
}
.hero-h1 .grad {
  background: linear-gradient(135deg, #7C3AED 0%, #2563EB 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.hero-sub { font-size: 16px; color: #6B7280; max-width: 500px; line-height: 1.6; margin-bottom: 32px; }

/* ── how it works cards ── */
.hiw-card {
  background: #FFFFFF;
  border: 1px solid #F3F4F6;
  border-radius: 16px;
  padding: 24px 20px;
  transition: all 0.25s ease;
  height: 100%;
}
.hiw-card:hover {
  border-color: #DDD6FE;
  box-shadow: 0 8px 24px rgba(124,58,237,0.08);
  transform: translateY(-2px);
}
.hiw-icon { font-size: 26px; margin-bottom: 14px; display: block; }
.hiw-title { font-size: 14px; font-weight: 700; color: #111827; margin-bottom: 8px; letter-spacing: -0.01em; }
.hiw-desc { font-size: 12.5px; color: #6B7280; line-height: 1.6; }

/* ── sidebar labels ── */
.sb-label {
  font-size: 10px;
  font-weight: 600;
  color: #9CA3AF;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: 16px 0 6px;
  display: block;
}

/* ── suggestion chips ── */
.suggestion-chip {
  display: inline-flex;
  background: #F5F3FF;
  border: 1px solid #DDD6FE;
  border-radius: 8px;
  padding: 4px 10px;
  font-size: 11px;
  color: #7C3AED;
  font-weight: 500;
  margin: 2px 2px;
  cursor: default;
  transition: all 0.15s;
}
.suggestion-chip:hover { background: #EDE9FE; }

/* ── dial ── */
.dial-num { font-family: 'JetBrains Mono', monospace; font-weight: 700; font-size: 20px; fill: #111827; }
.dial-lbl { font-family: 'JetBrains Mono', monospace; font-size: 8px; fill: #9CA3AF; letter-spacing: 0.06em; }
</style>
"""


def confidence_dial_svg(pct: float, color: str, size: int = 110) -> str:
    r = size / 2 - 11
    cx = cy = size / 2
    circ = 2 * 3.14159265 * r
    offset = circ * (1 - pct / 100)
    bg = "#F3F4F6"
    return f"""<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg">
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{bg}" stroke-width="8"/>
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="8"
          stroke-linecap="round"
          stroke-dasharray="{circ:.2f}" stroke-dashoffset="{offset:.2f}"
          transform="rotate(-90 {cx} {cy})"/>
  <text x="{cx}" y="{cy + 2}" text-anchor="middle" class="dial-num">{pct:.0f}</text>
  <text x="{cx}" y="{cy + 17}" text-anchor="middle" class="dial-lbl">CONFIDENCE</text>
</svg>"""


def verdict_hero_html(verdict: str, confidence: float, invest_p: float, company: str) -> str:
    color = VERDICT_COLOR[verdict]
    bg    = VERDICT_BG[verdict]
    dial  = confidence_dial_svg(confidence, color)
    return f"""
<div class="verdict-hero" style="--vc:{color}; --vc-soft:{bg};">
  <div style="flex-shrink:0">{dial}</div>
  <div>
    <div class="verdict-company">{company}</div>
    <div class="verdict-word">{verdict}</div>
    <div style="margin-top:12px;display:flex;flex-wrap:wrap;gap:8px">
      <span class="verdict-pill">Invest prob. {invest_p:.0%}</span>
      <span class="verdict-pill">Confidence {confidence:.0f}%</span>
    </div>
  </div>
</div>"""


def banner_html(level: str, title: str, body: str) -> str:
    icon = "⚠" if level == "warn" else "✕"
    return f"""<div class="alert-banner {level if level == 'warn' else 'crit'}">
  <span style="font-size:14px">{icon}</span>
  <span><b>{title}</b><br/>{body}</span>
</div>"""


def pillar_bar_html(name: str, score: float, color: str) -> str:
    pct = score / 10 * 100
    return f"""<div class="pillar-row">
  <div class="pillar-name">{name}</div>
  <div class="pillar-track"><div class="pillar-fill" style="width:{pct}%;background:{color}"></div></div>
  <div class="pillar-score">{score:.1f}</div>
</div>"""


def driver_bar_html(feature: str, shap_val: float, max_abs: float) -> str:
    color = GREEN if shap_val > 0 else RED
    width = abs(shap_val) / max_abs * 100 if max_abs else 0
    side  = "left:50%;" if shap_val > 0 else "right:50%;"
    return f"""<div class="driver">
  <div class="driver-label">{feature}</div>
  <div class="driver-bar-wrap">
    <div class="driver-center"></div>
    <div class="driver-bar" style="{side}width:{width/2:.1f}%;background:{color};opacity:0.85"></div>
  </div>
</div>"""


def flag_html(text: str) -> str:
    return f'<div class="flag-row"><div class="flag-dot"></div><div>{text}</div></div>'


def data_bar_html(n_fetched: int, n_total: int = 35) -> str:
    pct = min(100, n_fetched / n_total * 100)
    if n_fetched >= 20:
        quality, qcolor = "FULL DATA", GREEN
    elif n_fetched >= 10:
        quality, qcolor = "PARTIAL", AMBER
    else:
        quality, qcolor = "LOW DATA", RED
    return f"""<div class="data-signal-bar">
  <span class="data-signal-label" style="color:{qcolor}">{quality}</span>
  <div class="data-signal-track"><div class="data-signal-fill" style="width:{pct:.0f}%"></div></div>
  <span class="data-signal-count">{n_fetched}/{n_total} signals</span>
</div>"""


def metric_card_html(label: str, value: str, delta: str = None, delta_type: str = "up", icon: str = "") -> str:
    delta_html = ""
    if delta:
        arrow = "↑" if delta_type == "up" else ("↓" if delta_type == "down" else "→")
        delta_html = f'<span class="metric-card-delta {delta_type}">{arrow} {delta}</span>'
    return f"""<div class="metric-card">
  <div class="metric-card-label"><span class="dot"></span>{label}</div>
  <div class="metric-card-val">{value}</div>
  {delta_html}
</div>"""
