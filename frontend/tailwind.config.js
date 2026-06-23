/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        // Core
        bg:       "#08090F",
        surface:  "rgba(255,255,255,0.04)",
        surface2: "rgba(255,255,255,0.07)",
        border:   "rgba(255,255,255,0.08)",
        "border-strong": "rgba(255,255,255,0.16)",

        // Text
        ink:   "#F0EEE8",
        ink2:  "#9CA3AF",
        muted: "#4B5563",

        // Accent — indigo
        accent:       "#818CF8",
        "accent-dim": "rgba(129,140,248,0.1)",
        "accent-mid": "rgba(129,140,248,0.3)",

        // Verdict colors
        invest:       "#34D399",
        "invest-dim": "rgba(52,211,153,0.1)",
        "invest-mid": "rgba(52,211,153,0.3)",
        avoid:        "#FB7185",
        "avoid-dim":  "rgba(251,113,133,0.1)",
        "avoid-mid":  "rgba(251,113,133,0.3)",
        neutral:      "#FBBF24",
        "neutral-dim":"rgba(251,191,36,0.1)",
        "neutral-mid":"rgba(251,191,36,0.3)",

        // Cinema
        cinema: "#05060C",
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
        display: ["Space Grotesk", "system-ui", "sans-serif"],
      },
      backgroundImage: {
        "gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
        "hero-glow": "radial-gradient(ellipse 80% 50% at 50% -10%, rgba(129,140,248,0.2) 0%, transparent 60%)",
        "invest-glow-bg": "radial-gradient(ellipse 60% 60% at 50% 50%, rgba(52,211,153,0.15) 0%, transparent 70%)",
        "avoid-glow-bg":  "radial-gradient(ellipse 60% 60% at 50% 50%, rgba(251,113,133,0.15) 0%, transparent 70%)",
      },
      keyframes: {
        ticker:    { "0%": { transform: "translateX(0)" }, "100%": { transform: "translateX(-50%)" } },
        scan:      { "0%": { left: "-10%" }, "100%": { left: "110%" } },
        "fade-up": { "0%": { opacity: 0, transform: "translateY(20px)" }, "100%": { opacity: 1, transform: "translateY(0)" } },
        "fade-in": { "0%": { opacity: 0 }, "100%": { opacity: 1 } },
        "scale-in":{ "0%": { opacity: 0, transform: "scale(0.8)" }, "100%": { opacity: 1, transform: "scale(1)" } },
        shimmer:   { "0%": { backgroundPosition: "-200% 0" }, "100%": { backgroundPosition: "200% 0" } },
        glow:      { "0%,100%": { opacity: 0.5 }, "50%": { opacity: 1 } },
        "pulse-ring": {
          "0%":   { transform: "scale(0.95)", opacity: 1 },
          "100%": { transform: "scale(1.6)",  opacity: 0 },
        },
        aurora: {
          "0%":   { transform: "translate(0%, 0%) scale(1)" },
          "33%":  { transform: "translate(5%, -8%) scale(1.05)" },
          "66%":  { transform: "translate(-4%, 5%) scale(0.97)" },
          "100%": { transform: "translate(0%, 0%) scale(1)" },
        },
        "aurora-2": {
          "0%":   { transform: "translate(0%, 0%) scale(1)" },
          "33%":  { transform: "translate(-6%, 6%) scale(1.03)" },
          "66%":  { transform: "translate(5%, -4%) scale(0.96)" },
          "100%": { transform: "translate(0%, 0%) scale(1)" },
        },
        float: {
          "0%,100%": { transform: "translateY(0)" },
          "50%":     { transform: "translateY(-8px)" },
        },
        "verdict-pop": {
          "0%":   { opacity: 0, transform: "scale(0.5) translateY(20px)" },
          "70%":  { transform: "scale(1.06) translateY(-4px)" },
          "100%": { opacity: 1, transform: "scale(1) translateY(0)" },
        },
        "slide-up": {
          "0%":   { transform: "translateY(0)", opacity: 1 },
          "100%": { transform: "translateY(-100%)", opacity: 0 },
        },
        "bar-fill": {
          "0%":   { transform: "scaleX(0)" },
          "100%": { transform: "scaleX(1)" },
        },
        "count-up": { "0%": { opacity: 0 }, "100%": { opacity: 1 } },
        "border-spin": {
          "0%":   { "--border-angle": "0deg" },
          "100%": { "--border-angle": "360deg" },
        },
      },
      animation: {
        ticker:       "ticker 45s linear infinite",
        scan:         "scan 2s ease-in-out infinite",
        "fade-up":    "fade-up 0.6s cubic-bezier(0.4,0,0.2,1) forwards",
        "fade-in":    "fade-in 0.4s ease-out forwards",
        "scale-in":   "scale-in 0.5s cubic-bezier(0.175,0.885,0.32,1.275) forwards",
        shimmer:      "shimmer 2s linear infinite",
        glow:         "glow 3s ease-in-out infinite",
        "pulse-ring": "pulse-ring 1.5s cubic-bezier(0,0,0.2,1) infinite",
        aurora:       "aurora 18s ease-in-out infinite",
        "aurora-2":   "aurora-2 24s ease-in-out infinite",
        float:        "float 6s ease-in-out infinite",
        "verdict-pop":"verdict-pop 0.7s cubic-bezier(0.175,0.885,0.32,1.275) forwards",
        "slide-up":   "slide-up 0.6s cubic-bezier(0.76,0,0.24,1) forwards",
        "bar-fill":   "bar-fill 1s cubic-bezier(0.4,0,0.2,1) forwards",
      },
      boxShadow: {
        card:          "0 1px 3px rgba(0,0,0,0.4), 0 4px 16px rgba(0,0,0,0.3)",
        "card-hover":  "0 4px 24px rgba(0,0,0,0.5), 0 1px 4px rgba(0,0,0,0.3)",
        "glow-accent": "0 0 40px rgba(129,140,248,0.3), 0 0 80px rgba(129,140,248,0.1)",
        "glow-invest": "0 0 60px rgba(52,211,153,0.4),  0 0 120px rgba(52,211,153,0.15)",
        "glow-avoid":  "0 0 60px rgba(251,113,133,0.4), 0 0 120px rgba(251,113,133,0.15)",
        "glow-neutral":"0 0 60px rgba(251,191,36,0.4),  0 0 120px rgba(251,191,36,0.15)",
        "search":      "0 0 0 1px rgba(129,140,248,0.4), 0 0 40px rgba(129,140,248,0.15)",
        "inner-glow":  "inset 0 1px 0 rgba(255,255,255,0.08)",
      },
    },
  },
  plugins: [],
}
