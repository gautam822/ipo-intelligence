/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}", "./preview/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        // Ground
        bg:       "#0A0B0D",
        surface:  "rgba(255,255,255,0.025)",
        surface2: "rgba(255,255,255,0.055)",
        border:   "rgba(255,255,255,0.07)",
        "border-strong": "rgba(255,255,255,0.15)",

        // Text — warm bone / graphite
        ink:   "#E9E7E2",
        ink2:  "#A3A099",
        muted: "#66635C",

        // Brand — bond-certificate gold (hairline doses only)
        gold:       "#C9A961",
        "gold-dim": "rgba(201,169,97,0.10)",
        "gold-mid": "rgba(201,169,97,0.35)",
        // Back-compat alias
        accent:       "#C9A961",
        "accent-dim": "rgba(201,169,97,0.10)",
        "accent-mid": "rgba(201,169,97,0.35)",

        // Verdicts — the only saturated color in the app
        invest:        "#40D993",
        "invest-dim":  "rgba(64,217,147,0.09)",
        "invest-mid":  "rgba(64,217,147,0.30)",
        neutral:       "#E5B84B",
        "neutral-dim": "rgba(229,184,75,0.09)",
        "neutral-mid": "rgba(229,184,75,0.30)",
        avoid:         "#F2657E",
        "avoid-dim":   "rgba(242,101,126,0.09)",
        "avoid-mid":   "rgba(242,101,126,0.30)",
      },
      fontFamily: {
        display: ["Newsreader", "Georgia", "Cambria", "serif"],
        sans: ["Inter", "system-ui", "-apple-system", "sans-serif"],
        mono: ["JetBrains Mono", "ui-monospace", "SFMono-Regular", "monospace"],
      },
      letterSpacing: {
        caps: "0.14em",
      },
      keyframes: {
        tape:       { "0%": { transform: "translateX(0)" }, "100%": { transform: "translateX(-50%)" } },
        "fade-up":  { "0%": { opacity: 0, transform: "translateY(14px)" }, "100%": { opacity: 1, transform: "translateY(0)" } },
        "fade-in":  { "0%": { opacity: 0 }, "100%": { opacity: 1 } },
        shimmer:    { "0%": { backgroundPosition: "-200% 0" }, "100%": { backgroundPosition: "200% 0" } },
        stamp:      { "0%": { opacity: 0, transform: "scale(1.16)" }, "60%": { opacity: 1, transform: "scale(0.985)" }, "100%": { opacity: 1, transform: "scale(1)" } },
        caret:      { "0%,45%": { opacity: 1 }, "50%,100%": { opacity: 0 } },
        "bar-fill": { "0%": { transform: "scaleX(0)" }, "100%": { transform: "scaleX(1)" } },
      },
      animation: {
        tape:       "tape 48s linear infinite",
        "fade-up":  "fade-up 0.55s cubic-bezier(0.22,1,0.36,1) forwards",
        "fade-in":  "fade-in 0.4s ease-out forwards",
        shimmer:    "shimmer 1.8s linear infinite",
        stamp:      "stamp 0.5s cubic-bezier(0.22,1,0.36,1) forwards",
        caret:      "caret 1s step-end infinite",
        "bar-fill": "bar-fill 0.9s cubic-bezier(0.22,1,0.36,1) forwards",
      },
      boxShadow: {
        card:  "0 1px 2px rgba(0,0,0,0.5), 0 8px 28px rgba(0,0,0,0.35)",
        press: "inset 0 1px 0 rgba(255,255,255,0.05)",
        pop:   "0 12px 40px rgba(0,0,0,0.55)",
      },
    },
  },
  plugins: [],
}
