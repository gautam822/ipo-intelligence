"""
IPO Intelligence — $100k Premium Theme
Aurora · Glassmorphism · Cinematic · Animated
"""

GREEN       = "#00D9A3"
GREEN_DIM   = "rgba(0,217,163,0.08)"
GREEN_GLOW  = "rgba(0,217,163,0.5)"
RED         = "#FF4D6A"
RED_DIM     = "rgba(255,77,106,0.08)"
RED_GLOW    = "rgba(255,77,106,0.5)"
AMBER       = "#FFB547"
AMBER_DIM   = "rgba(255,181,71,0.08)"
AMBER_GLOW  = "rgba(255,181,71,0.5)"
STEEL       = "#4F8EF7"
INK         = "#04070F"
MUTE        = "#555F70"

VERDICT_COLOR = {"INVEST": GREEN, "AVOID": RED, "NEUTRAL": AMBER}
VERDICT_GLOW  = {"INVEST": GREEN_GLOW, "AVOID": RED_GLOW, "NEUTRAL": AMBER_GLOW}
VERDICT_DIM   = {"INVEST": GREEN_DIM, "AVOID": RED_DIM, "NEUTRAL": AMBER_DIM}
VERDICT_EMOJI = {"INVEST": "↑", "AVOID": "↓", "NEUTRAL": "→"}

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@300;400;500;600;700&display=swap');

/* ═══════════════════════════════════════════════════
   RESET
═══════════════════════════════════════════════════ */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif; -webkit-font-smoothing: antialiased; }

/* ═══════════════════════════════════════════════════
   KILL STREAMLIT CHROME
═══════════════════════════════════════════════════ */
#MainMenu, header[data-testid="stHeader"], footer { visibility: hidden; height: 0 !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stAppViewContainer"] { padding: 0 !important; }
[data-testid="stVerticalBlock"] { gap: 0 !important; }
div[data-testid="stMarkdownContainer"] > div { display: contents; }

/* ═══════════════════════════════════════════════════
   AURORA BACKGROUND
═══════════════════════════════════════════════════ */
.stApp {
  background: #04070F !important;
  min-height: 100vh;
  overflow-x: hidden;
}

.stApp::before {
  content: '';
  position: fixed;
  inset: 0;
  background:
    radial-gradient(ellipse 120% 60% at 20% -10%, rgba(79,142,247,0.18) 0%, transparent 55%),
    radial-gradient(ellipse 80% 50% at 80% 110%, rgba(0,217,163,0.12) 0%, transparent 50%),
    radial-gradient(ellipse 60% 40% at 50% 50%, rgba(139,92,246,0.06) 0%, transparent 60%);
  pointer-events: none;
  z-index: 0;
  animation: aurora 12s ease-in-out infinite alternate;
}

@keyframes aurora {
  0%   { opacity: 1; transform: scale(1) rotate(0deg); }
  50%  { opacity: 0.8; transform: scale(1.05) rotate(0.5deg); }
  100% { opacity: 1; transform: scale(1) rotate(0deg); }
}

/* Grid dot overlay */
.stApp::after {
  content: '';
  position: fixed;
  inset: 0;
  background-image:
    radial-gradient(rgba(255,255,255,0.025) 1px, transparent 1px);
  background-size: 28px 28px;
  pointer-events: none;
  z-index: 0;
}

/* ═══════════════════════════════════════════════════
   SIDEBAR — DEEP GLASS
═══════════════════════════════════════════════════ */
[data-testid="stSidebar"] {
  background: rgba(4,7,15,0.92) !important;
  border-right: 1px solid rgba(255,255,255,0.06) !important;
  backdrop-filter: blur(40px) saturate(150%) !important;
}
[data-testid="stSidebar"] * { color: #E8E6F0 !important; }

[data-testid="stSidebar"] .stTextInput input {
  background: rgba(255,255,255,0.05) !important;
  border: 1px solid rgba(255,255,255,0.1) !important;
  color: #E8E6F0 !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 14px !important;
  border-radius: 12px !important;
  padding: 12px 16px !important;
  transition: all 0.3s ease !important;
}
[data-testid="stSidebar"] .stTextInput input:focus {
  border-color: rgba(79,142,247,0.6) !important;
  box-shadow: 0 0 0 3px rgba(79,142,247,0.12), 0 0 20px rgba(79,142,247,0.1) !important;
  background: rgba(255,255,255,0.07) !important;
}
[data-testid="stSidebar"] .stTextInput input::placeholder {
  color: rgba(255,255,255,0.25) !important;
}

/* ═══════════════════════════════════════════════════
   BUTTONS
═══════════════════════════════════════════════════ */
.stButton > button {
  background: linear-gradient(135deg, #00D9A3 0%, #00B8D9 100%) !important;
  color: #020F09 !important;
  border: none !important;
  font-family: 'Space Grotesk', sans-serif !important;
  font-weight: 700 !important;
  font-size: 14px !important;
  border-radius: 14px !important;
  padding: 13px 24px !important;
  letter-spacing: 0.03em !important;
  transition: all 0.25s cubic-bezier(0.4,0,0.2,1) !important;
  box-shadow: 0 4px 24px rgba(0,217,163,0.3), 0 1px 3px rgba(0,0,0,0.3) !important;
  position: relative !important;
  overflow: hidden !important;
}
.stButton > button::before {
  content: '' !important;
  position: absolute !important;
  inset: 0 !important;
  background: linear-gradient(135deg, rgba(255,255,255,0.15) 0%, transparent 60%) !important;
  pointer-events: none !important;
}
.stButton > button:hover {
  transform: translateY(-2px) scale(1.01) !important;
  box-shadow: 0 8px 32px rgba(0,217,163,0.45), 0 2px 8px rgba(0,0,0,0.4) !important;
}
.stButton > button:active {
  transform: translateY(0) scale(0.99) !important;
}

.stDownloadButton > button {
  background: rgba(255,255,255,0.05) !important;
  color: #E8E6F0 !important;
  border: 1px solid rgba(255,255,255,0.1) !important;
  font-family: 'Space Grotesk', sans-serif !important;
  font-weight: 600 !important;
  border-radius: 14px !important;
  transition: all 0.25s ease !important;
}
.stDownloadButton > button:hover {
  background: rgba(255,255,255,0.09) !important;
  border-color: rgba(255,255,255,0.2) !important;
  transform: translateY(-1px) !important;
}

/* ═══════════════════════════════════════════════════
   SLIDERS & RADIO
═══════════════════════════════════════════════════ */
[role="radiogroup"] label { color: #E8E6F0 !important; }
[data-baseweb="slider"] [role="slider"] { background: #00D9A3 !important; box-shadow: 0 0 12px rgba(0,217,163,0.5) !important; }
[data-baseweb="slider"] div[class*="Track"] div:first-child { background: rgba(0,217,163,0.7) !important; }

/* ═══════════════════════════════════════════════════
   SPINNER
═══════════════════════════════════════════════════ */
.stSpinner > div { border-top-color: #00D9A3 !important; }

/* ═══════════════════════════════════════════════════
   SCROLLBAR
═══════════════════════════════════════════════════ */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.08); border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.15); }

/* ═══════════════════════════════════════════════════
   WORDMARK BAR
═══════════════════════════════════════════════════ */
.ipo-topbar {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 16px 32px;
  background: rgba(4,7,15,0.85);
  backdrop-filter: blur(30px) saturate(150%);
  border-bottom: 1px solid rgba(255,255,255,0.06);
  position: sticky;
  top: 0;
  z-index: 200;
}
.ipo-topbar-logo {
  font-family: 'Space Grotesk', sans-serif;
  font-weight: 800;
  font-size: 17px;
  color: #E8E6F0;
  letter-spacing: -0.04em;
}
.ipo-topbar-logo span {
  background: linear-gradient(90deg, #4F8EF7, #00D9A3);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.ipo-topbar-badge {
  font-family: 'JetBrains Mono', monospace;
  font-size: 9px;
  letter-spacing: 0.12em;
  color: #00D9A3;
  background: rgba(0,217,163,0.1);
  border: 1px solid rgba(0,217,163,0.25);
  border-radius: 6px;
  padding: 3px 9px;
}
.ipo-topbar-tagline {
  font-family: 'JetBrains Mono', monospace;
  font-size: 9px;
  letter-spacing: 0.06em;
  color: #394150;
  margin-left: auto;
}
.ipo-topbar-dot {
  width: 6px; height: 6px;
  border-radius: 50%;
  background: #00D9A3;
  box-shadow: 0 0 8px #00D9A3;
  animation: pulse-dot 2s ease-in-out infinite;
}
@keyframes pulse-dot {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.6; transform: scale(0.8); }
}

/* ═══════════════════════════════════════════════════
   MAIN CONTENT WRAPPER
═══════════════════════════════════════════════════ */
.main-wrap {
  position: relative;
  z-index: 1;
  padding: 0 36px 64px;
  max-width: 1200px;
  margin: 0 auto;
}

/* ═══════════════════════════════════════════════════
   HERO EMPTY STATE
═══════════════════════════════════════════════════ */
.hero-section {
  text-align: center;
  padding: 72px 24px 56px;
  position: relative;
}
.hero-eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: #00D9A3;
  background: rgba(0,217,163,0.08);
  border: 1px solid rgba(0,217,163,0.2);
  border-radius: 99px;
  padding: 6px 16px;
  margin-bottom: 28px;
}
.hero-eyebrow-dot {
  width: 5px; height: 5px;
  border-radius: 50%;
  background: #00D9A3;
  animation: pulse-dot 2s ease-in-out infinite;
}
.hero-h1 {
  font-family: 'Space Grotesk', sans-serif;
  font-size: clamp(40px, 6vw, 68px);
  font-weight: 800;
  letter-spacing: -0.04em;
  line-height: 1.05;
  color: #E8E6F0;
  margin-bottom: 20px;
}
.hero-h1 .grad {
  background: linear-gradient(135deg, #4F8EF7 0%, #00D9A3 50%, #8B5CF6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  background-size: 200% 200%;
  animation: grad-shift 6s ease infinite;
}
@keyframes grad-shift {
  0%   { background-position: 0% 50%; }
  50%  { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
.hero-sub {
  font-size: 18px;
  color: #4A5568;
  max-width: 520px;
  margin: 0 auto 52px;
  line-height: 1.65;
  font-weight: 400;
}

/* ═══════════════════════════════════════════════════
   METRIC STRIP
═══════════════════════════════════════════════════ */
.metric-strip {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1px;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 20px;
  overflow: hidden;
  margin-bottom: 40px;
}
.metric-cell {
  background: rgba(255,255,255,0.02);
  padding: 24px 20px;
  text-align: center;
  position: relative;
  transition: background 0.3s ease;
}
.metric-cell::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(255,255,255,0.03) 0%, transparent 100%);
  opacity: 0;
  transition: opacity 0.3s;
}
.metric-cell:hover { background: rgba(255,255,255,0.05); }
.metric-cell:hover::before { opacity: 1; }
.metric-val {
  font-family: 'JetBrains Mono', monospace;
  font-size: 30px;
  font-weight: 700;
  color: #E8E6F0;
  line-height: 1;
  margin-bottom: 8px;
  letter-spacing: -0.02em;
}
.metric-lbl {
  font-size: 10px;
  color: #394150;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  font-family: 'JetBrains Mono', monospace;
}

/* ═══════════════════════════════════════════════════
   HOW IT WORKS
═══════════════════════════════════════════════════ */
.hiw-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-top: 48px;
}
.hiw-card {
  background: rgba(255,255,255,0.025);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 20px;
  padding: 28px 24px;
  text-align: center;
  transition: all 0.35s cubic-bezier(0.4,0,0.2,1);
  position: relative;
  overflow: hidden;
}
.hiw-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
}
.hiw-card:hover {
  background: rgba(255,255,255,0.05);
  border-color: rgba(255,255,255,0.12);
  transform: translateY(-4px);
  box-shadow: 0 20px 60px rgba(0,0,0,0.4), 0 0 0 1px rgba(255,255,255,0.06);
}
.hiw-icon {
  font-size: 32px;
  margin-bottom: 16px;
  display: block;
  filter: drop-shadow(0 0 12px rgba(79,142,247,0.4));
}
.hiw-title {
  font-family: 'Space Grotesk', sans-serif;
  font-weight: 700;
  font-size: 15px;
  color: #E8E6F0;
  margin-bottom: 10px;
  letter-spacing: -0.01em;
}
.hiw-desc {
  font-size: 13px;
  color: #4A5568;
  line-height: 1.65;
}

/* ═══════════════════════════════════════════════════
   VERDICT HERO
═══════════════════════════════════════════════════ */
.verdict-hero-wrap {
  border-radius: 24px;
  padding: 36px 40px;
  margin: 24px 0 20px;
  display: flex;
  align-items: center;
  gap: 40px;
  position: relative;
  overflow: hidden;
  transition: all 0.5s ease;
}
.verdict-hero-wrap::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse 70% 90% at 90% 50%, var(--vc-dim) 0%, transparent 70%);
  pointer-events: none;
}
.verdict-hero-wrap::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 24px;
  border: 1px solid var(--vc-border);
  pointer-events: none;
}
.verdict-glow-ring {
  position: absolute;
  width: 300px; height: 300px;
  border-radius: 50%;
  background: radial-gradient(circle, var(--vc-glow) 0%, transparent 70%);
  right: -80px; top: 50%;
  transform: translateY(-50%);
  opacity: 0.15;
  pointer-events: none;
}
.verdict-word {
  font-family: 'Space Grotesk', sans-serif;
  font-weight: 800;
  font-size: 64px;
  letter-spacing: -0.04em;
  color: var(--vc);
  line-height: 1;
  text-shadow: 0 0 60px var(--vc-glow), 0 0 120px var(--vc-glow-soft);
  animation: verdict-in 0.6s cubic-bezier(0.175,0.885,0.32,1.275) both;
}
@keyframes verdict-in {
  from { opacity: 0; transform: scale(0.7) translateY(10px); }
  to   { opacity: 1; transform: scale(1) translateY(0); }
}
.verdict-company {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  color: #394150;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  margin-bottom: 10px;
}
.verdict-stats {
  display: flex;
  gap: 20px;
  margin-top: 14px;
  flex-wrap: wrap;
}
.verdict-stat {
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 10px;
  padding: 8px 14px;
}
.verdict-stat-val {
  font-family: 'JetBrains Mono', monospace;
  font-size: 18px;
  font-weight: 600;
  color: #E8E6F0;
  line-height: 1;
}
.verdict-stat-lbl {
  font-size: 10px;
  color: #394150;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  margin-top: 4px;
  font-family: 'JetBrains Mono', monospace;
}

/* ═══════════════════════════════════════════════════
   GLASS PANELS
═══════════════════════════════════════════════════ */
.g-panel {
  background: rgba(255,255,255,0.025);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 20px;
  padding: 24px 26px;
  margin-bottom: 16px;
  backdrop-filter: blur(20px);
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}
.g-panel::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
}
.g-panel:hover {
  background: rgba(255,255,255,0.04);
  border-color: rgba(255,255,255,0.11);
}
.g-panel-title {
  font-family: 'JetBrains Mono', monospace;
  font-size: 9px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: #394150;
  margin-bottom: 18px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.g-panel-title::before {
  content: '';
  width: 4px; height: 4px;
  border-radius: 50%;
  background: #4F8EF7;
  box-shadow: 0 0 6px #4F8EF7;
  flex-shrink: 0;
}

/* ═══════════════════════════════════════════════════
   PILLAR BARS
═══════════════════════════════════════════════════ */
.pillar-row {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 10px 0;
  border-bottom: 1px solid rgba(255,255,255,0.04);
}
.pillar-row:last-child { border-bottom: none; }
.pillar-name {
  font-size: 12.5px;
  color: #C8C6D0;
  width: 145px;
  flex-shrink: 0;
  font-weight: 500;
  letter-spacing: -0.01em;
}
.pillar-track {
  flex: 1;
  height: 4px;
  background: rgba(255,255,255,0.05);
  border-radius: 99px;
  overflow: hidden;
}
.pillar-fill {
  height: 100%;
  border-radius: 99px;
  transition: width 1.2s cubic-bezier(0.4,0,0.2,1);
  position: relative;
}
.pillar-fill::after {
  content: '';
  position: absolute;
  right: 0; top: -2px;
  width: 8px; height: 8px;
  border-radius: 50%;
  background: inherit;
  filter: blur(2px);
  opacity: 0.8;
}
.pillar-score {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  color: #394150;
  width: 28px;
  text-align: right;
}

/* ═══════════════════════════════════════════════════
   SHAP DRIVER BARS
═══════════════════════════════════════════════════ */
.driver {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 7px 0;
}
.driver-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  color: #394150;
  width: 155px;
  flex-shrink: 0;
  text-align: right;
  letter-spacing: 0.01em;
}
.driver-bar-wrap {
  flex: 1;
  height: 22px;
  position: relative;
  background: rgba(255,255,255,0.03);
  border-radius: 5px;
}
.driver-center {
  position: absolute;
  left: 50%; top: 0;
  width: 1px; height: 100%;
  background: rgba(255,255,255,0.08);
}
.driver-bar {
  position: absolute;
  top: 2px;
  height: calc(100% - 4px);
  border-radius: 4px;
  opacity: 0.9;
}

/* ═══════════════════════════════════════════════════
   RED FLAGS
═══════════════════════════════════════════════════ */
.flag-row {
  display: flex;
  gap: 12px;
  padding: 10px 0;
  border-bottom: 1px solid rgba(255,255,255,0.04);
  font-size: 13px;
  color: #C8C6D0;
  line-height: 1.6;
  align-items: flex-start;
}
.flag-row:last-child { border-bottom: none; }
.flag-dot {
  width: 5px; height: 5px;
  border-radius: 50%;
  background: #FF4D6A;
  box-shadow: 0 0 6px rgba(255,77,106,0.6);
  margin-top: 8px;
  flex-shrink: 0;
}

/* ═══════════════════════════════════════════════════
   COMPARABLE CARD
═══════════════════════════════════════════════════ */
.comp-card {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 14px;
  padding: 18px 20px;
}
.comp-name {
  font-family: 'Space Grotesk', sans-serif;
  font-weight: 600;
  font-size: 15px;
  color: #E8E6F0;
  margin-bottom: 4px;
}
.comp-meta {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  color: #394150;
  letter-spacing: 0.06em;
  margin-bottom: 16px;
}
.comp-alpha {
  font-family: 'JetBrains Mono', monospace;
  font-weight: 700;
  font-size: 24px;
  letter-spacing: -0.02em;
}
.comp-alpha-lbl {
  font-size: 10px;
  color: #394150;
  font-family: 'JetBrains Mono', monospace;
  letter-spacing: 0.06em;
  margin-bottom: 4px;
}

/* ═══════════════════════════════════════════════════
   ALERT BANNERS
═══════════════════════════════════════════════════ */
.alert-banner {
  border-radius: 14px;
  padding: 14px 18px;
  margin-bottom: 16px;
  font-size: 13.5px;
  line-height: 1.6;
  border: 1px solid;
  display: flex;
  gap: 12px;
  align-items: flex-start;
  backdrop-filter: blur(10px);
}
.alert-banner.crit { background: rgba(255,77,106,0.06); border-color: rgba(255,77,106,0.2); color: #FCA5A5; }
.alert-banner.warn { background: rgba(255,181,71,0.06); border-color: rgba(255,181,71,0.2); color: #FDE68A; }
.alert-banner b { color: #E8E6F0; }

/* ═══════════════════════════════════════════════════
   DATA SIGNAL BAR
═══════════════════════════════════════════════════ */
.data-signal-bar {
  display: flex;
  align-items: center;
  gap: 14px;
  background: rgba(255,255,255,0.025);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 12px;
  padding: 10px 16px;
  margin-bottom: 14px;
}
.data-signal-label { font-family: 'JetBrains Mono', monospace; font-size: 10px; letter-spacing: 0.1em; text-transform: uppercase; white-space: nowrap; }
.data-signal-track { flex: 1; height: 3px; background: rgba(255,255,255,0.06); border-radius: 99px; overflow: hidden; }
.data-signal-fill { height: 100%; border-radius: 99px; background: linear-gradient(90deg, #4F8EF7 0%, #00D9A3 100%); box-shadow: 0 0 8px rgba(0,217,163,0.4); }
.data-signal-count { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #394150; white-space: nowrap; }

/* ═══════════════════════════════════════════════════
   SOURCE LINK
═══════════════════════════════════════════════════ */
.src-link {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  color: #394150;
  display: block;
  margin-bottom: 12px;
}
.src-link a { color: #4F8EF7; text-decoration: none; transition: color 0.2s; }
.src-link a:hover { color: #00D9A3; }

/* ═══════════════════════════════════════════════════
   DISCLAIMER
═══════════════════════════════════════════════════ */
.disclaimer {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  color: #28303D;
  line-height: 1.8;
  border-top: 1px solid rgba(255,255,255,0.05);
  padding-top: 16px;
  margin-top: 12px;
  text-align: center;
  letter-spacing: 0.02em;
}

/* ═══════════════════════════════════════════════════
   DIAL SVG CLASSES
═══════════════════════════════════════════════════ */
.dial-num { font-family: 'JetBrains Mono', monospace; font-weight: 700; font-size: 22px; fill: #E8E6F0; }
.dial-pct { font-family: 'JetBrains Mono', monospace; font-size: 11px; fill: #394150; letter-spacing: 0.04em; }

/* ═══════════════════════════════════════════════════
   SIDEBAR SECTION LABELS
═══════════════════════════════════════════════════ */
.sidebar-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 9px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: #394150;
  margin: 20px 0 8px;
  display: flex;
  align-items: center;
  gap: 6px;
}
.sidebar-label::before {
  content: '';
  flex: 1;
  height: 1px;
  background: rgba(255,255,255,0.06);
}

/* ═══════════════════════════════════════════════════
   SUGGESTION CHIPS
═══════════════════════════════════════════════════ */
.suggestion-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 8px;
  padding: 5px 10px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  color: #6B7280;
  margin: 3px 2px;
  cursor: pointer;
  transition: all 0.2s;
}
.suggestion-chip:hover {
  background: rgba(79,142,247,0.1);
  border-color: rgba(79,142,247,0.3);
  color: #4F8EF7;
}

/* ═══════════════════════════════════════════════════
   FADE IN ANIMATION
═══════════════════════════════════════════════════ */
.fade-up {
  animation: fade-up 0.5s cubic-bezier(0.4,0,0.2,1) both;
}
@keyframes fade-up {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}
.fade-up-1 { animation-delay: 0.05s; }
.fade-up-2 { animation-delay: 0.1s; }
.fade-up-3 { animation-delay: 0.15s; }
.fade-up-4 { animation-delay: 0.2s; }
.fade-up-5 { animation-delay: 0.25s; }
</style>
"""

# ── JS for animated counters ──────────────────────────────────────────────
COUNTER_JS = """
<script>
function animateCounter(el, target, duration, prefix, suffix, decimals) {
  let start = 0;
  const step = timestamp => {
    if (!start) start = timestamp;
    const progress = Math.min((timestamp - start) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    const val = eased * target;
    el.textContent = prefix + val.toFixed(decimals) + suffix;
    if (progress < 1) requestAnimationFrame(step);
  };
  requestAnimationFrame(step);
}
document.querySelectorAll('[data-count]').forEach(el => {
  const target = parseFloat(el.dataset.count);
  const prefix = el.dataset.prefix || '';
  const suffix = el.dataset.suffix || '';
  const decimals = parseInt(el.dataset.decimals || '0');
  animateCounter(el, target, 1600, prefix, suffix, decimals);
});
</script>
"""


def confidence_dial_svg(pct: float, color: str, size: int = 124) -> str:
    r = size / 2 - 13
    cx = cy = size / 2
    circ = 2 * 3.14159265 * r
    offset = circ * (1 - pct / 100)
    uid = color.replace("#", "")
    return f"""<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <filter id="gf{uid}"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <linearGradient id="lg{uid}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{color}" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="{color}"/>
    </linearGradient>
  </defs>
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="9"/>
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="url(#lg{uid})" stroke-width="9"
          stroke-linecap="round"
          stroke-dasharray="{circ:.2f}" stroke-dashoffset="{offset:.2f}"
          transform="rotate(-90 {cx} {cy})"
          filter="url(#gf{uid})"/>
  <text x="{cx}" y="{cy + 2}" text-anchor="middle" class="dial-num">{pct:.0f}</text>
  <text x="{cx}" y="{cy + 18}" text-anchor="middle" class="dial-pct">CONFIDENCE</text>
</svg>"""


def verdict_hero_html(verdict: str, confidence: float, invest_p: float, company: str) -> str:
    color = VERDICT_COLOR[verdict]
    glow  = VERDICT_GLOW[verdict]
    dim   = VERDICT_DIM[verdict]
    emoji = VERDICT_EMOJI[verdict]
    dial  = confidence_dial_svg(confidence, color)
    return f"""
<div class="verdict-hero-wrap fade-up"
     style="background:{dim}; --vc:{color}; --vc-dim:{dim}; --vc-glow:{glow};
            --vc-glow-soft:{glow.replace('0.5','0.2')}; --vc-border:rgba(255,255,255,0.08);">
  <div class="verdict-glow-ring"></div>
  <div style="flex-shrink:0">{dial}</div>
  <div>
    <div class="verdict-company">{company}</div>
    <div class="verdict-word">{emoji} {verdict}</div>
    <div class="verdict-stats">
      <div class="verdict-stat">
        <div class="verdict-stat-val" style="color:{color}">{invest_p:.0%}</div>
        <div class="verdict-stat-lbl">Invest prob.</div>
      </div>
      <div class="verdict-stat">
        <div class="verdict-stat-val">{confidence:.0f}%</div>
        <div class="verdict-stat-lbl">Confidence</div>
      </div>
    </div>
  </div>
</div>"""


def banner_html(level: str, title: str, body: str) -> str:
    icon = "⚠" if level == "warn" else "✕"
    return f"""<div class="alert-banner {level if level == 'warn' else 'crit'}">
  <span style="font-size:15px;margin-top:1px">{icon}</span>
  <span><b>{title}</b><br/>{body}</span>
</div>"""


def pillar_bar_html(name: str, score: float, color: str = STEEL) -> str:
    pct = score / 10 * 100
    return f"""<div class="pillar-row">
  <div class="pillar-name">{name}</div>
  <div class="pillar-track"><div class="pillar-fill" style="width:{pct}%;background:{color};box-shadow:0 0 8px {color}55"></div></div>
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
    <div class="driver-bar" style="{side}width:{width/2:.1f}%;background:{color};box-shadow:0 0 6px {color}55"></div>
  </div>
</div>"""


def flag_html(text: str) -> str:
    return f'<div class="flag-row"><div class="flag-dot"></div><div>{text}</div></div>'


def data_bar_html(n_fetched: int, n_total: int = 35) -> str:
    pct = min(100, n_fetched / n_total * 100)
    quality = "FULL DATA" if n_fetched >= 20 else ("PARTIAL DATA" if n_fetched >= 10 else "LOW DATA")
    qcolor = GREEN if n_fetched >= 20 else (AMBER if n_fetched >= 10 else RED)
    return f"""<div class="data-signal-bar">
  <span class="data-signal-label" style="color:{qcolor}">{quality}</span>
  <div class="data-signal-track"><div class="data-signal-fill" style="width:{pct:.0f}%"></div></div>
  <span class="data-signal-count">{n_fetched}/{n_total} signals</span>
</div>"""
