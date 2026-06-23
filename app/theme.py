"""
IPO Intelligence — Premium Dark Glassmorphism Theme
Cinematic · Animated · Premium $10k quality
"""

INK     = "#080C14"
PANEL   = "rgba(255,255,255,0.04)"
PANEL_2 = "rgba(255,255,255,0.07)"
LINE    = "rgba(255,255,255,0.08)"
PAPER   = "#F0EEE8"
MUTE    = "#6B7280"
GREEN   = "#10B981"
GREEN_DIM = "rgba(16,185,129,0.12)"
GREEN_GLOW = "rgba(16,185,129,0.4)"
RED     = "#EF4444"
RED_DIM = "rgba(239,68,68,0.12)"
RED_GLOW = "rgba(239,68,68,0.4)"
AMBER   = "#F59E0B"
AMBER_DIM = "rgba(245,158,11,0.12)"
AMBER_GLOW = "rgba(245,158,11,0.4)"
STEEL   = "#3B82F6"

VERDICT_COLOR = {"INVEST": GREEN, "AVOID": RED, "NEUTRAL": AMBER}
VERDICT_GLOW  = {"INVEST": GREEN_GLOW, "AVOID": RED_GLOW, "NEUTRAL": AMBER_GLOW}
VERDICT_DIM   = {"INVEST": GREEN_DIM, "AVOID": RED_DIM, "NEUTRAL": AMBER_DIM}

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700;800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
  --ink: #080C14;
  --paper: #F0EEE8;
  --mute: #6B7280;
  --green: #10B981;
  --red: #EF4444;
  --amber: #F59E0B;
  --steel: #3B82F6;
  --line: rgba(255,255,255,0.08);
  --panel: rgba(255,255,255,0.04);
  --panel2: rgba(255,255,255,0.07);
}

/* ── reset & base ── */
*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] {
  font-family: 'Inter', sans-serif;
  -webkit-font-smoothing: antialiased;
}

/* ── kill streamlit chrome ── */
#MainMenu, header[data-testid="stHeader"], footer { visibility: hidden; height: 0; }
.block-container { padding-top: 0 !important; padding-bottom: 0 !important; max-width: 100% !important; }
[data-testid="stAppViewContainer"] { padding: 0; }

/* ── animated background ── */
.stApp {
  background: #080C14 !important;
  background-image:
    radial-gradient(ellipse 80% 50% at 50% -10%, rgba(59,130,246,0.12) 0%, transparent 60%),
    radial-gradient(ellipse 60% 40% at 80% 90%, rgba(16,185,129,0.06) 0%, transparent 50%) !important;
  min-height: 100vh;
}

/* Grid dot pattern overlay */
.stApp::before {
  content: '';
  position: fixed;
  inset: 0;
  background-image: radial-gradient(rgba(255,255,255,0.03) 1px, transparent 1px);
  background-size: 32px 32px;
  pointer-events: none;
  z-index: 0;
}

/* ── sidebar ── */
[data-testid="stSidebar"] {
  background: rgba(8,12,20,0.95) !important;
  border-right: 1px solid var(--line) !important;
  backdrop-filter: blur(20px);
}
[data-testid="stSidebar"] * { color: var(--paper) !important; }
[data-testid="stSidebar"] .stTextInput input {
  background: rgba(255,255,255,0.06) !important;
  border: 1px solid var(--line) !important;
  color: var(--paper) !important;
  font-family: 'JetBrains Mono', monospace !important;
  border-radius: 10px !important;
  transition: border-color 0.2s, box-shadow 0.2s;
}
[data-testid="stSidebar"] .stTextInput input:focus {
  border-color: rgba(59,130,246,0.5) !important;
  box-shadow: 0 0 0 3px rgba(59,130,246,0.1) !important;
}

/* ── buttons ── */
.stButton button {
  background: linear-gradient(135deg, #10B981, #059669) !important;
  color: #020F09 !important;
  border: none !important;
  font-family: 'Space Grotesk', sans-serif !important;
  font-weight: 700 !important;
  border-radius: 12px !important;
  letter-spacing: 0.02em !important;
  transition: all 0.2s !important;
  box-shadow: 0 4px 20px rgba(16,185,129,0.25) !important;
}
.stButton button:hover {
  transform: translateY(-1px) !important;
  box-shadow: 0 8px 30px rgba(16,185,129,0.35) !important;
  filter: brightness(1.08) !important;
}

/* ── download button ── */
.stDownloadButton button {
  background: rgba(255,255,255,0.06) !important;
  color: var(--paper) !important;
  border: 1px solid var(--line) !important;
  font-family: 'Space Grotesk', sans-serif !important;
  font-weight: 600 !important;
  border-radius: 12px !important;
  transition: all 0.2s !important;
}
.stDownloadButton button:hover {
  background: rgba(255,255,255,0.1) !important;
  border-color: rgba(255,255,255,0.2) !important;
}

/* ── typography ── */
h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; color: var(--paper) !important; }
p, label, .stMarkdown { color: var(--paper); }
.mono { font-family: 'JetBrains Mono', monospace; }

/* ── spinner ── */
.stSpinner { color: var(--green) !important; }

/* ── radio ── */
[role="radiogroup"] label { color: var(--paper) !important; }
[role="radiogroup"] [data-baseweb="radio"] div { border-color: var(--green) !important; }

/* ── sliders ── */
[data-baseweb="slider"] [role="slider"] { background: var(--green) !important; }
[data-baseweb="slider"] div[class*="Track"] { background: var(--line) !important; }

/* ── top wordmark bar ── */
.ipo-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 18px 32px 16px;
  border-bottom: 1px solid var(--line);
  background: rgba(8,12,20,0.8);
  backdrop-filter: blur(20px);
  position: sticky;
  top: 0;
  z-index: 100;
}
.ipo-brand .wordmark {
  font-family: 'Space Grotesk', sans-serif;
  font-weight: 800;
  font-size: 18px;
  color: var(--paper);
  letter-spacing: -0.03em;
}
.ipo-brand .badge {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  color: var(--green);
  background: rgba(16,185,129,0.12);
  border: 1px solid rgba(16,185,129,0.3);
  border-radius: 6px;
  padding: 2px 8px;
  letter-spacing: 0.06em;
}
.ipo-brand .tagline {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  color: var(--mute);
  margin-left: auto;
  letter-spacing: 0.05em;
}

/* ── hero / empty state ── */
.hero-empty {
  text-align: center;
  padding: 64px 24px 48px;
}
.hero-empty .hero-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: clamp(32px, 5vw, 56px);
  font-weight: 800;
  letter-spacing: -0.03em;
  line-height: 1.1;
  color: var(--paper);
  margin-bottom: 16px;
}
.hero-empty .hero-title .gradient-text {
  background: linear-gradient(135deg, #10B981 0%, #3B82F6 50%, #8B5CF6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.hero-empty .hero-sub {
  font-size: 17px;
  color: var(--mute);
  max-width: 480px;
  margin: 0 auto 40px;
  line-height: 1.6;
}

/* ── metric card ── */
.metric-strip {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1px;
  background: var(--line);
  border: 1px solid var(--line);
  border-radius: 16px;
  overflow: hidden;
  margin: 0 32px 32px;
}
.metric-cell {
  background: rgba(255,255,255,0.03);
  padding: 20px 24px;
  text-align: center;
  transition: background 0.2s;
}
.metric-cell:hover { background: rgba(255,255,255,0.06); }
.metric-val {
  font-family: 'JetBrains Mono', monospace;
  font-size: 26px;
  font-weight: 600;
  color: var(--paper);
  line-height: 1;
  margin-bottom: 6px;
}
.metric-lbl {
  font-size: 11px;
  color: var(--mute);
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

/* ── glass panel ── */
.g-panel {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 16px;
  padding: 22px 24px;
  margin-bottom: 16px;
  backdrop-filter: blur(10px);
  transition: border-color 0.2s;
}
.g-panel:hover { border-color: rgba(255,255,255,0.13); }
.g-panel-title {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--mute);
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.g-panel-title::before {
  content: '';
  width: 5px; height: 5px;
  border-radius: 50%;
  background: var(--steel);
  display: inline-block;
}

/* ── verdict hero ── */
.verdict-hero {
  border-radius: 20px;
  padding: 32px 36px;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 32px;
  position: relative;
  overflow: hidden;
}
.verdict-hero::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse 60% 80% at 90% 50%, var(--vc-dim) 0%, transparent 70%);
  pointer-events: none;
}
.verdict-hero::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 20px;
  border: 1px solid var(--vc-border);
  pointer-events: none;
}
.verdict-word {
  font-family: 'Space Grotesk', sans-serif;
  font-weight: 800;
  font-size: 52px;
  letter-spacing: -0.03em;
  color: var(--vc);
  line-height: 1;
  text-shadow: 0 0 40px var(--vc-glow);
}
.verdict-company {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  color: var(--mute);
  letter-spacing: 0.08em;
  text-transform: uppercase;
  margin-bottom: 8px;
}
.verdict-sub {
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
  color: var(--paper);
  margin-top: 8px;
  opacity: 0.7;
}

/* ── dial numbers ── */
.dial-num { font-family: 'JetBrains Mono', monospace; font-weight: 600; font-size: 20px; fill: var(--paper); }
.dial-lbl { font-family: 'JetBrains Mono', monospace; font-size: 8px; fill: #6B7280; letter-spacing: 0.06em; }

/* ── pillar bars ── */
.pillar-row {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 10px 0;
  border-bottom: 1px solid rgba(255,255,255,0.05);
}
.pillar-row:last-child { border-bottom: none; }
.pillar-name { font-size: 13px; color: var(--paper); width: 140px; flex-shrink: 0; font-weight: 500; }
.pillar-track { flex: 1; height: 5px; background: rgba(255,255,255,0.06); border-radius: 99px; overflow: hidden; }
.pillar-fill { height: 100%; border-radius: 99px; transition: width 1s ease; }
.pillar-score { font-family: 'JetBrains Mono', monospace; font-size: 12px; color: var(--mute); width: 30px; text-align: right; }

/* ── shap driver bars ── */
.driver {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 7px 0;
}
.driver-label { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: var(--mute); width: 160px; flex-shrink: 0; text-align: right; }
.driver-bar-wrap { flex: 1; height: 20px; position: relative; background: rgba(255,255,255,0.04); border-radius: 4px; }
.driver-bar { position: absolute; top: 0; height: 100%; border-radius: 4px; }

/* ── flag chips ── */
.flag-row {
  display: flex;
  gap: 10px;
  padding: 10px 0;
  border-bottom: 1px solid rgba(255,255,255,0.05);
  font-size: 13px;
}
.flag-row:last-child { border-bottom: none; }
.flag-dot { width: 5px; height: 5px; border-radius: 50%; background: var(--red); margin-top: 7px; flex-shrink: 0; }

/* ── comparable card ── */
.comp-card {
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 12px;
  padding: 16px 18px;
  font-size: 13px;
  color: var(--paper);
}
.comp-alpha { font-family: 'JetBrains Mono', monospace; font-weight: 600; font-size: 18px; }

/* ── banner ── */
.alert-banner {
  border-radius: 12px;
  padding: 14px 18px;
  margin-bottom: 18px;
  font-size: 13.5px;
  line-height: 1.6;
  border: 1px solid;
  display: flex;
  gap: 12px;
  align-items: flex-start;
  backdrop-filter: blur(10px);
}
.alert-banner.crit { background: rgba(239,68,68,0.07); border-color: rgba(239,68,68,0.25); color: #FCA5A5; }
.alert-banner.warn { background: rgba(245,158,11,0.07); border-color: rgba(245,158,11,0.25); color: #FDE68A; }
.alert-banner .icon { font-size: 15px; margin-top: 1px; }
.alert-banner b { color: var(--paper); }

/* ── source link ── */
.src-link { font-family: 'JetBrains Mono', monospace; font-size: 10px; color: var(--mute); margin-bottom: 14px; display: block; }
.src-link a { color: var(--steel); text-decoration: none; }
.src-link a:hover { text-decoration: underline; }

/* ── disclaimer ── */
.disclaimer {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  color: var(--mute);
  line-height: 1.7;
  border-top: 1px solid var(--line);
  padding-top: 14px;
  margin-top: 8px;
  text-align: center;
}

/* ── n-fetched data bar ── */
.data-bar-wrap {
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 10px;
  padding: 10px 16px;
  margin-bottom: 14px;
  display: flex;
  align-items: center;
  gap: 12px;
}
.data-bar-track { flex: 1; height: 4px; background: rgba(255,255,255,0.08); border-radius: 99px; overflow: hidden; }
.data-bar-fill { height: 100%; border-radius: 99px; background: linear-gradient(90deg, #3B82F6, #10B981); }
.data-bar-label { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: var(--mute); white-space: nowrap; }

/* ── scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.2); }
</style>
"""


def confidence_dial_svg(pct: float, color: str, glow: str, size: int = 120) -> str:
    r = size / 2 - 12
    cx = cy = size / 2
    circumference = 2 * 3.14159265 * r
    offset = circumference * (1 - pct / 100)
    return f"""
    <svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <filter id="glow_{color.replace('#','')}">
          <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
          <feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge>
        </filter>
      </defs>
      <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="rgba(255,255,255,0.06)" stroke-width="8"/>
      <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="8"
              stroke-linecap="round"
              stroke-dasharray="{circumference:.1f}"
              stroke-dashoffset="{offset:.1f}"
              transform="rotate(-90 {cx} {cy})"
              filter="url(#glow_{color.replace('#','')})"/>
      <text x="{cx}" y="{cy + 1}" text-anchor="middle" class="dial-num">{pct:.0f}</text>
      <text x="{cx}" y="{cy + 16}" text-anchor="middle" class="dial-lbl">CONFIDENCE</text>
    </svg>"""


def verdict_hero_html(verdict: str, confidence: float, invest_p: float, company: str) -> str:
    color = VERDICT_COLOR[verdict]
    glow  = VERDICT_GLOW[verdict]
    dim   = VERDICT_DIM[verdict]
    border_alpha = "0.35"
    dial  = confidence_dial_svg(confidence, color, glow)
    border_color = color.replace(")", f", {border_alpha})").replace("rgb(", "rgba(") if color.startswith("rgb") else color + "59"
    return f"""
    <div class="verdict-hero"
         style="background:{dim}; --vc:{color}; --vc-dim:{dim}; --vc-glow:{glow}; --vc-border:rgba(255,255,255,0.1);">
      <div style="flex-shrink:0">{dial}</div>
      <div>
        <div class="verdict-company">{company}</div>
        <div class="verdict-word">{verdict}</div>
        <div class="verdict-sub">INVEST PROBABILITY &nbsp;{invest_p:.0%} &nbsp;·&nbsp; CONFIDENCE {confidence:.0f}%</div>
      </div>
    </div>"""


def banner_html(level: str, title: str, body: str) -> str:
    icon = "⚠" if level == "warn" else "✕"
    cls = "warn" if level == "warn" else "crit"
    return f"""<div class="alert-banner {cls}"><span class="icon">{icon}</span>
    <span><b>{title}</b><br/>{body}</span></div>"""


def pillar_bar_html(name: str, score: float, color: str = STEEL) -> str:
    pct = score / 10 * 100
    return f"""<div class="pillar-row">
      <div class="pillar-name">{name}</div>
      <div class="pillar-track"><div class="pillar-fill" style="width:{pct}%;background:{color}"></div></div>
      <div class="pillar-score mono">{score:.1f}</div></div>"""


def driver_bar_html(feature: str, shap_val: float, max_abs: float) -> str:
    color = GREEN if shap_val > 0 else RED
    width = abs(shap_val) / max_abs * 100 if max_abs else 0
    side = "left:50%;" if shap_val > 0 else "right:50%;"
    return f"""<div class="driver">
      <div class="driver-label">{feature}</div>
      <div class="driver-bar-wrap">
        <div class="driver-bar" style="{side}width:{width/2}%;background:{color};opacity:0.85"></div>
      </div></div>"""


def flag_html(text: str) -> str:
    return f'<div class="flag-row"><div class="flag-dot"></div><div style="color:#F0EEE8">{text}</div></div>'


def data_bar_html(n_fetched: int, n_total: int = 35) -> str:
    pct = min(100, n_fetched / n_total * 100)
    quality = "FULL DATA" if n_fetched >= 20 else ("PARTIAL" if n_fetched >= 10 else "LOW DATA")
    qcolor = GREEN if n_fetched >= 20 else (AMBER if n_fetched >= 10 else RED)
    return f"""<div class="data-bar-wrap">
      <span class="data-bar-label" style="color:{qcolor}">{quality}</span>
      <div class="data-bar-track"><div class="data-bar-fill" style="width:{pct}%"></div></div>
      <span class="data-bar-label">{n_fetched}/{n_total} signals</span>
    </div>"""
