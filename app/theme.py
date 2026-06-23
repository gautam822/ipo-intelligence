"""
IPO Intelligence — Dark Premium Streamlit Theme
Aurora · Glassmorphism · Cinematic
"""

GREEN       = "#34D399"
GREEN_DIM   = "rgba(52,211,153,0.1)"
GREEN_GLOW  = "rgba(52,211,153,0.4)"
RED         = "#FB7185"
RED_DIM     = "rgba(251,113,133,0.1)"
RED_GLOW    = "rgba(251,113,133,0.4)"
AMBER       = "#FBBF24"
AMBER_DIM   = "rgba(251,191,36,0.1)"
AMBER_GLOW  = "rgba(251,191,36,0.4)"
ACCENT      = "#818CF8"
ACCENT_DIM  = "rgba(129,140,248,0.1)"
INK         = "#F0EEE8"
INK2        = "#9CA3AF"
MUTED       = "#4B5563"
BG          = "#08090F"

VERDICT_COLOR = {"INVEST": GREEN, "AVOID": RED, "NEUTRAL": AMBER}
VERDICT_GLOW  = {"INVEST": GREEN_GLOW, "AVOID": RED_GLOW, "NEUTRAL": AMBER_GLOW}
VERDICT_DIM   = {"INVEST": GREEN_DIM,  "AVOID": RED_DIM,  "NEUTRAL": AMBER_DIM}
VERDICT_ICON  = {"INVEST": "↑", "AVOID": "↓", "NEUTRAL": "→"}

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

/* ── RESET ── */
*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif; -webkit-font-smoothing: antialiased; }

/* ── KILL STREAMLIT CHROME ── */
#MainMenu, header[data-testid="stHeader"], footer { visibility: hidden; height: 0 !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stAppViewContainer"] { padding: 0 !important; }

/* ── DARK BACKGROUND + AURORA ── */
.stApp {
  background: #08090F !important;
  min-height: 100vh;
  position: relative;
}
.stApp::before {
  content: '';
  position: fixed;
  inset: 0;
  background:
    radial-gradient(ellipse 120% 60% at 15% -5%,  rgba(99,102,241,0.2) 0%, transparent 55%),
    radial-gradient(ellipse 80%  50% at 85% 100%, rgba(52,211,153,0.12) 0%, transparent 50%),
    radial-gradient(ellipse 60%  40% at 50% 50%,  rgba(139,92,246,0.07) 0%, transparent 60%);
  pointer-events: none;
  z-index: 0;
  animation: aurora 18s ease-in-out infinite alternate;
}
@keyframes aurora {
  0%   { opacity: 1; transform: scale(1); }
  50%  { opacity: 0.8; transform: scale(1.04) rotate(0.3deg); }
  100% { opacity: 1; transform: scale(1); }
}
.stApp::after {
  content: '';
  position: fixed;
  inset: 0;
  background-image: radial-gradient(rgba(255,255,255,0.022) 1px, transparent 1px);
  background-size: 28px 28px;
  pointer-events: none;
  z-index: 0;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
  background: rgba(8,9,15,0.94) !important;
  border-right: 1px solid rgba(255,255,255,0.07) !important;
  backdrop-filter: blur(40px) !important;
  position: relative;
  z-index: 10;
}
[data-testid="stSidebar"] * { color: #F0EEE8 !important; }
[data-testid="stSidebar"] .stTextInput input {
  background: rgba(255,255,255,0.05) !important;
  border: 1px solid rgba(255,255,255,0.1) !important;
  color: #F0EEE8 !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 13.5px !important;
  border-radius: 12px !important;
  padding: 11px 16px !important;
  transition: all 0.25s ease !important;
}
[data-testid="stSidebar"] .stTextInput input:focus {
  border-color: rgba(129,140,248,0.55) !important;
  box-shadow: 0 0 0 3px rgba(129,140,248,0.12), 0 0 24px rgba(129,140,248,0.08) !important;
  background: rgba(255,255,255,0.07) !important;
}
[data-testid="stSidebar"] .stTextInput input::placeholder { color: #4B5563 !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.07) !important; }

/* ── BUTTONS ── */
.stButton > button {
  background: linear-gradient(135deg, #818CF8 0%, #6366F1 100%) !important;
  color: #ffffff !important;
  border: none !important;
  font-family: 'Space Grotesk', sans-serif !important;
  font-weight: 700 !important;
  font-size: 14px !important;
  border-radius: 12px !important;
  padding: 12px 24px !important;
  letter-spacing: 0.02em !important;
  transition: all 0.25s ease !important;
  box-shadow: 0 4px 20px rgba(129,140,248,0.35), 0 1px 3px rgba(0,0,0,0.4) !important;
  position: relative !important;
}
.stButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 32px rgba(129,140,248,0.5), 0 2px 8px rgba(0,0,0,0.4) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

.stDownloadButton > button {
  background: rgba(255,255,255,0.05) !important;
  color: #9CA3AF !important;
  border: 1px solid rgba(255,255,255,0.1) !important;
  font-family: 'Space Grotesk', sans-serif !important;
  font-weight: 600 !important;
  border-radius: 12px !important;
  transition: all 0.2s ease !important;
}
.stDownloadButton > button:hover {
  background: rgba(255,255,255,0.08) !important;
  border-color: rgba(255,255,255,0.2) !important;
  color: #F0EEE8 !important;
}

/* ── RADIO ── */
[role="radiogroup"] label { color: #9CA3AF !important; font-size: 13px !important; }
[data-baseweb="radio"] div { border-color: rgba(255,255,255,0.2) !important; }

/* ── SLIDERS ── */
[data-baseweb="slider"] [role="slider"] {
  background: #818CF8 !important;
  box-shadow: 0 0 12px rgba(129,140,248,0.6) !important;
}
[data-baseweb="slider"] div[class*="Track"] div:first-child { background: #818CF8 !important; }

/* ── SPINNER ── */
.stSpinner > div { border-top-color: #818CF8 !important; }

/* ── DIVIDER ── */
hr { border-color: rgba(255,255,255,0.07) !important; }

/* ── PLOTLY CHART BG ── */
.js-plotly-plot .plotly { background: transparent !important; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.18); }

/* ── TOP BAR ── */
.ipo-topbar {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 15px 32px;
  background: rgba(8,9,15,0.88);
  backdrop-filter: blur(30px) saturate(150%);
  border-bottom: 1px solid rgba(255,255,255,0.07);
  position: sticky;
  top: 0;
  z-index: 200;
}
.ipo-topbar-dot {
  width: 7px; height: 7px;
  border-radius: 50%;
  background: #34D399;
  box-shadow: 0 0 10px #34D399;
  animation: pulse-dot 2s ease-in-out infinite;
}
@keyframes pulse-dot {
  0%, 100% { opacity: 1; transform: scale(1); }
  50%       { opacity: 0.6; transform: scale(0.8); }
}
.ipo-topbar-logo {
  font-family: 'Space Grotesk', sans-serif;
  font-weight: 800;
  font-size: 17px;
  color: #F0EEE8;
  letter-spacing: -0.04em;
}
.ipo-topbar-logo span {
  background: linear-gradient(90deg, #818CF8, #34D399);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.ipo-topbar-badge {
  font-family: 'JetBrains Mono', monospace;
  font-size: 9px;
  letter-spacing: 0.12em;
  color: #818CF8;
  background: rgba(129,140,248,0.1);
  border: 1px solid rgba(129,140,248,0.25);
  border-radius: 6px;
  padding: 3px 9px;
}
.ipo-topbar-tag {
  font-family: 'JetBrains Mono', monospace;
  font-size: 9px;
  color: #4B5563;
  letter-spacing: 0.06em;
  margin-left: auto;
}

/* ── HERO ── */
.hero-section {
  text-align: center;
  padding: 60px 24px 48px;
  position: relative;
  z-index: 1;
}
.hero-eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: #818CF8;
  background: rgba(129,140,248,0.08);
  border: 1px solid rgba(129,140,248,0.22);
  border-radius: 99px;
  padding: 6px 16px;
  margin-bottom: 24px;
}
.hero-eyebrow-dot {
  width: 5px; height: 5px;
  border-radius: 50%;
  background: #818CF8;
  animation: pulse-dot 2s ease-in-out infinite;
}
.hero-h1 {
  font-family: 'Space Grotesk', sans-serif;
  font-size: clamp(38px, 6vw, 66px);
  font-weight: 800;
  letter-spacing: -0.04em;
  line-height: 1.08;
  color: #F0EEE8;
  margin-bottom: 18px;
}
.hero-h1 .grad {
  background: linear-gradient(135deg, #818CF8 0%, #34D399 60%, #A78BFA 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  background-size: 200%;
  animation: grad-shift 6s ease infinite;
}
@keyframes grad-shift {
  0%   { background-position: 0% 50%; }
  50%  { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
.hero-sub {
  font-size: 17px;
  color: #6B7280;
  max-width: 500px;
  margin: 0 auto 40px;
  line-height: 1.65;
}

/* ── STAT STRIP ── */
.stat-strip {
  display: flex;
  justify-content: center;
  gap: 0;
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 16px;
  overflow: hidden;
  margin: 0 auto 40px;
  max-width: 600px;
}
.stat-cell {
  flex: 1;
  padding: 18px 12px;
  text-align: center;
  border-right: 1px solid rgba(255,255,255,0.07);
  transition: background 0.2s;
}
.stat-cell:last-child { border-right: none; }
.stat-cell:hover { background: rgba(255,255,255,0.04); }
.stat-val {
  font-family: 'JetBrains Mono', monospace;
  font-size: 24px;
  font-weight: 700;
  letter-spacing: -0.03em;
  background: linear-gradient(135deg, #818CF8, #34D399);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 4px;
}
.stat-lbl {
  font-size: 10px;
  color: #4B5563;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  font-family: 'JetBrains Mono', monospace;
}

/* ── GLASS CARD ── */
.g-card {
  background: rgba(255,255,255,0.025);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 20px;
  padding: 22px 24px;
  margin-bottom: 16px;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}
.g-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
}
.g-card:hover {
  background: rgba(255,255,255,0.04);
  border-color: rgba(255,255,255,0.12);
}
.g-card-title {
  font-family: 'JetBrains Mono', monospace;
  font-size: 9px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: #4B5563;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 7px;
}
.g-card-title::before {
  content: '';
  width: 4px; height: 4px;
  border-radius: 50%;
  background: #818CF8;
  box-shadow: 0 0 6px #818CF8;
  display: inline-block;
  flex-shrink: 0;
}

/* ── VERDICT HERO ── */
.verdict-hero {
  border-radius: 22px;
  padding: 32px 36px;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 36px;
  position: relative;
  overflow: hidden;
}
.verdict-hero::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse 65% 90% at 90% 50%, var(--vc-glow-soft) 0%, transparent 65%);
  pointer-events: none;
}
.verdict-hero::after {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--vc-color) 50%, transparent);
  opacity: 0.35;
  pointer-events: none;
}
.verdict-glow-orb {
  position: absolute;
  width: 280px; height: 280px;
  border-radius: 50%;
  right: -60px; top: 50%;
  transform: translateY(-50%);
  background: radial-gradient(circle, var(--vc-glow-soft) 0%, transparent 70%);
  opacity: 0.2;
  pointer-events: none;
}
.verdict-word {
  font-family: 'Space Grotesk', sans-serif;
  font-weight: 800;
  font-size: 58px;
  letter-spacing: -0.04em;
  color: var(--vc-color);
  line-height: 1;
  text-shadow: 0 0 60px var(--vc-glow), 0 0 120px var(--vc-glow-soft);
  animation: verdict-in 0.6s cubic-bezier(0.175,0.885,0.32,1.275) both;
}
@keyframes verdict-in {
  from { opacity: 0; transform: scale(0.6) translateY(12px); }
  to   { opacity: 1; transform: scale(1) translateY(0); }
}
.verdict-icon {
  font-size: 22px;
  animation: verdict-in 0.7s cubic-bezier(0.175,0.885,0.32,1.275) both 0.1s;
}
.verdict-company {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  color: #4B5563;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  margin-bottom: 10px;
}
.verdict-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 14px;
}
.verdict-pill {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  font-weight: 600;
  padding: 6px 12px;
  border-radius: 10px;
}

/* ── DIAL ── */
.dial-num { font-family: 'JetBrains Mono', monospace; font-weight: 700; font-size: 20px; fill: #F0EEE8; }
.dial-lbl { font-family: 'JetBrains Mono', monospace; font-size: 8px; fill: #4B5563; letter-spacing: 0.06em; }

/* ── PILLAR BARS ── */
.pillar-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 9px 0;
  border-bottom: 1px solid rgba(255,255,255,0.04);
}
.pillar-row:last-child { border-bottom: none; }
.pillar-name { font-size: 12.5px; color: #9CA3AF; font-weight: 500; width: 145px; flex-shrink: 0; }
.pillar-track { flex: 1; height: 4px; background: rgba(255,255,255,0.06); border-radius: 99px; overflow: hidden; }
.pillar-fill  { height: 100%; border-radius: 99px; }
.pillar-score { font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #4B5563; width: 28px; text-align: right; }

/* ── DRIVER BARS ── */
.driver {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 7px 0;
}
.driver-label { font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #4B5563; width: 155px; flex-shrink: 0; text-align: right; }
.driver-wrap  { flex: 1; height: 20px; position: relative; background: rgba(255,255,255,0.04); border-radius: 5px; }
.driver-center{ position: absolute; left: 50%; top: 0; width: 1px; height: 100%; background: rgba(255,255,255,0.08); }
.driver-bar   { position: absolute; top: 2px; height: calc(100% - 4px); border-radius: 4px; }

/* ── FLAGS ── */
.flag-row {
  display: flex;
  gap: 10px;
  padding: 9px 0;
  border-bottom: 1px solid rgba(255,255,255,0.04);
  font-size: 13px;
  color: #9CA3AF;
  line-height: 1.55;
  align-items: flex-start;
}
.flag-row:last-child { border-bottom: none; }
.flag-dot { width: 5px; height: 5px; border-radius: 50%; background: #FB7185; box-shadow: 0 0 6px rgba(251,113,133,0.6); margin-top: 7px; flex-shrink: 0; }

/* ── COMPARABLE ── */
.comp-card {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 14px;
  padding: 16px 18px;
}
.comp-name   { font-family: 'Space Grotesk', sans-serif; font-weight: 600; font-size: 15px; color: #F0EEE8; margin-bottom: 3px; }
.comp-meta   { font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #4B5563; margin-bottom: 14px; }
.comp-alpha  { font-family: 'JetBrains Mono', monospace; font-weight: 700; font-size: 24px; letter-spacing: -0.02em; }
.comp-alpha-lbl { font-size: 10px; color: #4B5563; font-family: 'JetBrains Mono', monospace; margin-bottom: 3px; }

/* ── ALERT BANNERS ── */
.alert-banner {
  border-radius: 14px;
  padding: 13px 17px;
  margin-bottom: 16px;
  font-size: 13.5px;
  line-height: 1.6;
  border: 1px solid;
  display: flex;
  gap: 10px;
  align-items: flex-start;
}
.alert-banner.crit { background: rgba(251,113,133,0.07); border-color: rgba(251,113,133,0.22); color: #FCA5A5; }
.alert-banner.warn { background: rgba(251,191,36,0.07);  border-color: rgba(251,191,36,0.22);  color: #FDE68A; }
.alert-banner b { color: #F0EEE8; }

/* ── DATA SIGNAL ── */
.data-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  background: rgba(255,255,255,0.025);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 12px;
  padding: 9px 16px;
  margin-bottom: 14px;
}
.data-bar-label { font-family: 'JetBrains Mono', monospace; font-size: 10px; letter-spacing: 0.1em; text-transform: uppercase; white-space: nowrap; }
.data-bar-track { flex: 1; height: 3px; background: rgba(255,255,255,0.07); border-radius: 99px; overflow: hidden; }
.data-bar-fill  { height: 100%; border-radius: 99px; background: linear-gradient(90deg, #818CF8, #34D399); box-shadow: 0 0 8px rgba(52,211,153,0.4); }
.data-bar-count { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #4B5563; white-space: nowrap; }

/* ── HOW IT WORKS ── */
.hiw-card {
  background: rgba(255,255,255,0.025);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 18px;
  padding: 26px 22px;
  text-align: center;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
  height: 100%;
}
.hiw-card:hover {
  background: rgba(255,255,255,0.045);
  border-color: rgba(255,255,255,0.12);
  transform: translateY(-3px);
}
.hiw-card-top {
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(129,140,248,0.4), transparent);
}
.hiw-icon  { font-size: 30px; margin-bottom: 14px; display: block; }
.hiw-title { font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 14px; color: #F0EEE8; margin-bottom: 9px; }
.hiw-desc  { font-size: 12.5px; color: #6B7280; line-height: 1.65; }

/* ── SIDEBAR ── */
.sb-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 9px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: #4B5563;
  display: block;
  padding: 14px 0 7px;
}
.sb-chip {
  display: inline-flex;
  background: rgba(129,140,248,0.08);
  border: 1px solid rgba(129,140,248,0.18);
  border-radius: 8px;
  padding: 4px 10px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  color: #818CF8;
  margin: 2px 2px;
}

/* ── SOURCE LINK ── */
.src-link { font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #4B5563; display: block; margin-bottom: 12px; }
.src-link a { color: #818CF8; text-decoration: none; }
.src-link a:hover { color: #34D399; }

/* ── DISCLAIMER ── */
.disclaimer {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  color: #2D3748;
  line-height: 1.8;
  border-top: 1px solid rgba(255,255,255,0.05);
  padding-top: 16px;
  margin-top: 10px;
  text-align: center;
}
</style>
"""


def confidence_dial_svg(pct: float, color: str, size: int = 120) -> str:
    r = size / 2 - 12
    cx = cy = size / 2
    circ = 2 * 3.14159265 * r
    offset = circ * (1 - pct / 100)
    uid = color.replace("#", "")
    return f"""<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <filter id="gf{uid}">
      <feGaussianBlur stdDeviation="3.5" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <linearGradient id="lg{uid}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{color}" stop-opacity="0.5"/>
      <stop offset="100%" stop-color="{color}"/>
    </linearGradient>
  </defs>
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="rgba(255,255,255,0.06)" stroke-width="9"/>
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="url(#lg{uid})" stroke-width="9"
          stroke-linecap="round" stroke-dasharray="{circ:.2f}" stroke-dashoffset="{offset:.2f}"
          transform="rotate(-90 {cx} {cy})" filter="url(#gf{uid})"/>
  <text x="{cx}" y="{cy+2}" text-anchor="middle" class="dial-num">{pct:.0f}</text>
  <text x="{cx}" y="{cy+17}" text-anchor="middle" class="dial-lbl">CONFIDENCE</text>
</svg>"""


def verdict_hero_html(verdict: str, confidence: float, invest_p: float, company: str) -> str:
    color = VERDICT_COLOR[verdict]
    glow  = VERDICT_GLOW[verdict]
    dim   = VERDICT_DIM[verdict]
    icon  = VERDICT_ICON[verdict]
    dial  = confidence_dial_svg(confidence, color)
    glow_soft = glow.replace("0.4)", "0.2)")
    proba_pills = f"""
    <div class="verdict-pills">
      <span class="verdict-pill" style="background:{GREEN}12;border:1px solid {GREEN}25;color:{GREEN}">
        INVEST &nbsp;{invest_p:.0%}
      </span>
      <span class="verdict-pill" style="background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);color:#9CA3AF">
        Conf. &nbsp;{confidence:.0f}%
      </span>
    </div>"""
    return f"""
<div class="verdict-hero" style="background:{dim};--vc-color:{color};--vc-glow:{glow};--vc-glow-soft:{glow_soft};border:1px solid {color}22;">
  <div class="verdict-glow-orb"></div>
  <div style="flex-shrink:0">{dial}</div>
  <div style="flex:1">
    <div class="verdict-company">{company}</div>
    <div style="display:flex;align-items:center;gap:14px">
      <div class="verdict-word">{verdict}</div>
      <div class="verdict-icon">{icon}</div>
    </div>
    {proba_pills}
  </div>
</div>"""


def banner_html(level: str, title: str, body: str) -> str:
    icon = "⚠" if level == "warn" else "✕"
    cls  = "warn" if level == "warn" else "crit"
    return f"""<div class="alert-banner {cls}">
  <span style="font-size:14px;margin-top:1px">{icon}</span>
  <span><b>{title}</b><br/>{body}</span>
</div>"""


def pillar_bar_html(name: str, score: float, color: str) -> str:
    pct = score / 10 * 100
    return f"""<div class="pillar-row">
  <div class="pillar-name">{name}</div>
  <div class="pillar-track">
    <div class="pillar-fill" style="width:{pct}%;background:{color};box-shadow:0 0 6px {color}55"></div>
  </div>
  <div class="pillar-score">{score:.1f}</div>
</div>"""


def driver_bar_html(feature: str, shap_val: float, max_abs: float) -> str:
    color = GREEN if shap_val > 0 else RED
    width = abs(shap_val) / max_abs * 100 if max_abs else 0
    side  = "left:50%;" if shap_val > 0 else "right:50%;"
    return f"""<div class="driver">
  <div class="driver-label">{feature}</div>
  <div class="driver-wrap">
    <div class="driver-center"></div>
    <div class="driver-bar" style="{side}width:{width/2:.1f}%;background:{color};box-shadow:0 0 5px {color}55"></div>
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
    return f"""<div class="data-bar">
  <span class="data-bar-label" style="color:{qcolor}">{quality}</span>
  <div class="data-bar-track"><div class="data-bar-fill" style="width:{pct:.0f}%"></div></div>
  <span class="data-bar-count">{n_fetched}/{n_total} signals</span>
</div>"""
