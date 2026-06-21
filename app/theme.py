"""
Design system for IPO Intelligence — a terminal-inspired dark theme.

Token system:
  INK        #0B0E14   page background
  PANEL      #11151D   card/panel background
  PANEL_2    #161B26   nested panel / hover
  LINE       #232938   hairline borders
  PAPER      #E8E6DF   primary text (warm white, not pure white)
  MUTE       #8A8F9C   secondary text
  GREEN      #3D8B6E   INVEST
  RED        #C24E4E   AVOID
  AMBER      #D4A24C   NEUTRAL / warnings
  STEEL      #5B7A9D   data accents, charts

Typography:
  Display : "Space Grotesk"  — headings, verdict word
  Body    : "Inter"          — prose
  Mono    : "IBM Plex Mono"  — every number: confidence %, tickers, metrics
            (the signature move — numbers always read like a terminal printout)
"""

INK, PANEL, PANEL_2, LINE = "#0B0E14", "#11151D", "#161B26", "#232938"
PAPER, MUTE = "#E8E6DF", "#8A8F9C"
GREEN, RED, AMBER, STEEL = "#3D8B6E", "#C24E4E", "#D4A24C", "#5B7A9D"

VERDICT_COLOR = {"INVEST": GREEN, "AVOID": RED, "NEUTRAL": AMBER}

CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

:root {{
  --ink:{INK}; --panel:{PANEL}; --panel2:{PANEL_2}; --line:{LINE};
  --paper:{PAPER}; --mute:{MUTE};
  --green:{GREEN}; --red:{RED}; --amber:{AMBER}; --steel:{STEEL};
}}

html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}
.stApp {{ background: var(--ink); }}

/* ---------- kill default streamlit chrome ---------- */
#MainMenu, header[data-testid="stHeader"], footer {{ visibility: hidden; height:0; }}
.block-container {{ padding-top: 1.5rem; max-width: 1180px; }}
[data-testid="stSidebar"] {{
  background: var(--panel); border-right: 1px solid var(--line);
}}
[data-testid="stSidebar"] * {{ color: var(--paper) !important; }}

/* ---------- typography ---------- */
h1, h2, h3 {{ font-family:'Space Grotesk', sans-serif !important; color: var(--paper) !important;
  letter-spacing: -0.01em; }}
p, label, .stMarkdown {{ color: var(--paper); }}
.mono {{ font-family:'IBM Plex Mono', monospace; }}

/* ---------- top bar / wordmark ---------- */
.brand {{
  display:flex; align-items:baseline; gap:10px; padding: 4px 0 18px 0;
  border-bottom: 1px solid var(--line); margin-bottom: 28px;
}}
.brand .mark {{ font-family:'Space Grotesk'; font-weight:700; font-size:20px; color:var(--paper); }}
.brand .tick {{ font-family:'IBM Plex Mono'; font-size:11px; color:var(--green);
  background: rgba(61,139,110,0.12); border:1px solid rgba(61,139,110,0.35);
  border-radius:4px; padding:2px 7px; letter-spacing:0.04em; }}
.brand .sub {{ font-family:'IBM Plex Mono'; font-size:11px; color:var(--mute); margin-left:auto; }}

/* ---------- generic panel ---------- */
.panel {{
  background: var(--panel); border:1px solid var(--line); border-radius:10px;
  padding: 20px 22px; margin-bottom: 16px;
}}
.panel-title {{
  font-family:'IBM Plex Mono'; font-size:11px; letter-spacing:0.08em; text-transform:uppercase;
  color: var(--mute); margin-bottom:12px; display:flex; align-items:center; gap:8px;
}}
.panel-title::before {{ content:''; width:6px; height:6px; border-radius:50%; background:var(--steel); }}

/* ---------- verdict hero ---------- */
.verdict-hero {{
  display:flex; align-items:center; gap:28px; background: var(--panel);
  border:1px solid var(--line); border-radius:14px; padding:26px 28px; margin-bottom:18px;
  position:relative; overflow:hidden;
}}
.verdict-hero::before {{
  content:''; position:absolute; inset:0; opacity:0.06; pointer-events:none;
  background: radial-gradient(circle at 85% 50%, var(--vc) 0%, transparent 60%);
}}
.verdict-word {{
  font-family:'Space Grotesk'; font-weight:700; font-size:40px; letter-spacing:-0.02em;
  color: var(--vc); line-height:1;
}}
.verdict-meta {{ font-family:'IBM Plex Mono'; font-size:12px; color:var(--mute); margin-top:6px; }}
.dial-wrap {{ flex-shrink:0; }}
.dial-num {{ font-family:'IBM Plex Mono'; font-weight:600; font-size:22px; fill:var(--paper); }}
.dial-lbl {{ font-family:'IBM Plex Mono'; font-size:9px; fill:var(--mute); letter-spacing:0.06em; }}

/* ---------- data warning banner ---------- */
.banner {{
  border-radius:10px; padding:14px 18px; margin-bottom:18px; font-size:13.5px; line-height:1.6;
  border:1px solid; display:flex; gap:12px; align-items:flex-start;
}}
.banner.crit {{ background: rgba(194,78,78,0.08); border-color: rgba(194,78,78,0.35); color:#F0C9C9; }}
.banner.warn {{ background: rgba(212,162,76,0.08); border-color: rgba(212,162,76,0.35); color:#F0DCB8; }}
.banner .icon {{ font-size:15px; margin-top:1px; }}
.banner b {{ color: var(--paper); }}

/* ---------- pillar bars ---------- */
.pillar-row {{ display:flex; align-items:center; gap:14px; padding:9px 0; border-bottom:1px solid var(--line); }}
.pillar-row:last-child {{ border-bottom:none; }}
.pillar-name {{ font-size:13px; color:var(--paper); width:150px; flex-shrink:0; }}
.pillar-track {{ flex:1; height:6px; background:var(--panel2); border-radius:4px; overflow:hidden; }}
.pillar-fill {{ height:100%; border-radius:4px; }}
.pillar-score {{ font-family:'IBM Plex Mono'; font-size:12px; color:var(--mute); width:36px; text-align:right; }}

/* ---------- red flag chips ---------- */
.flag {{
  display:flex; gap:10px; padding:10px 0; border-bottom:1px solid var(--line); font-size:13.5px;
}}
.flag:last-child {{ border-bottom:none; }}
.flag .dot {{ width:6px; height:6px; border-radius:50%; background:var(--red); margin-top:6px; flex-shrink:0; }}

/* ---------- driver bars (shap) ---------- */
.driver {{ display:flex; align-items:center; gap:10px; padding:6px 0; }}
.driver-label {{ font-family:'IBM Plex Mono'; font-size:11px; color:var(--mute); width:150px;
  flex-shrink:0; text-align:right; }}
.driver-bar-wrap {{ flex:1; height:18px; position:relative; background:var(--panel2); border-radius:3px; }}
.driver-bar {{ position:absolute; top:0; height:100%; border-radius:3px; }}

/* ---------- comparable card ---------- */
.comp-card {{
  background: var(--panel2); border:1px solid var(--line); border-radius:8px;
  padding:14px 16px; font-size:13px; color:var(--paper);
}}
.comp-card .alpha {{ font-family:'IBM Plex Mono'; font-weight:600; }}

/* ---------- buttons ---------- */
.stButton button {{
  background: var(--green) !important; color: #06140F !important; border:none !important;
  font-family:'Space Grotesk' !important; font-weight:600 !important; border-radius:8px !important;
  letter-spacing:0.01em;
}}
.stButton button:hover {{ filter: brightness(1.1); }}

/* ---------- text input ---------- */
.stTextInput input {{
  background: var(--panel2) !important; border:1px solid var(--line) !important;
  color: var(--paper) !important; font-family:'IBM Plex Mono' !important; border-radius:8px !important;
}}

/* ---------- radio (mode toggle) ---------- */
[role="radiogroup"] label {{ color: var(--paper) !important; }}

/* ---------- footer disclaimer ---------- */
.disclaimer {{ font-family:'IBM Plex Mono'; font-size:11px; color:var(--mute); line-height:1.7;
  border-top:1px solid var(--line); padding-top:14px; margin-top:8px; }}
</style>
"""


def confidence_dial_svg(pct: float, color: str, size: int = 116) -> str:
    """Radial confidence gauge — the page's signature element."""
    r = size / 2 - 10
    cx = cy = size / 2
    circumference = 2 * 3.14159265 * r
    offset = circumference * (1 - pct / 100)
    return f"""
    <svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">
      <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{LINE}" stroke-width="8"/>
      <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="8"
              stroke-linecap="round" stroke-dasharray="{circumference}"
              stroke-dashoffset="{offset}" transform="rotate(-90 {cx} {cy})"/>
      <text x="{cx}" y="{cy-2}" text-anchor="middle" class="dial-num">{pct:.0f}</text>
      <text x="{cx}" y="{cy+16}" text-anchor="middle" class="dial-lbl">CONFIDENCE</text>
    </svg>"""


def verdict_hero_html(verdict: str, confidence: float, invest_p: float, company: str) -> str:
    color = VERDICT_COLOR[verdict]
    dial = confidence_dial_svg(confidence, color)
    return f"""
    <div class="verdict-hero" style="--vc:{color}">
      <div class="dial-wrap">{dial}</div>
      <div>
        <div class="verdict-word">{verdict}</div>
        <div class="verdict-meta">{company.upper()} &nbsp;·&nbsp; INVEST PROBABILITY {invest_p:.0%}</div>
      </div>
    </div>"""


def banner_html(level: str, title: str, body: str) -> str:
    icon = "⚠" if level == "warn" else "✕"
    cls = "warn" if level == "warn" else "crit"
    return f"""<div class="banner {cls}"><span class="icon">{icon}</span>
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
    side = "left:50%;" if shap_val > 0 else f"right:50%;"
    return f"""<div class="driver">
      <div class="driver-label">{feature}</div>
      <div class="driver-bar-wrap">
        <div class="driver-bar" style="{side}width:{width/2}%;background:{color}"></div>
      </div></div>"""


def flag_html(text: str) -> str:
    return f'<div class="flag"><div class="dot"></div><div>{text}</div></div>'
