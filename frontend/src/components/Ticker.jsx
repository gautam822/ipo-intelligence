const COLORS = {
  INVEST:  { text: "#34D399", bg: "rgba(52,211,153,0.1)",  dot: "#34D399" },
  NEUTRAL: { text: "#FBBF24", bg: "rgba(251,191,36,0.1)",  dot: "#FBBF24" },
  AVOID:   { text: "#FB7185", bg: "rgba(251,113,133,0.1)", dot: "#FB7185" },
}

export default function Ticker({ items = [] }) {
  if (!items.length) return null
  const doubled = [...items, ...items]

  return (
    <div className="w-full overflow-hidden border-b border-[rgba(255,255,255,0.06)] bg-[rgba(255,255,255,0.02)] py-2 backdrop-blur-sm">
      <div className="flex animate-ticker whitespace-nowrap will-change-transform" style={{ width: "max-content" }}>
        {doubled.map((item, i) => {
          const cfg = COLORS[item.verdict] ?? COLORS.NEUTRAL
          return (
            <span
              key={i}
              className="inline-flex items-center gap-2 px-6 text-xs font-mono font-medium"
            >
              <span className="w-1.5 h-1.5 rounded-full flex-shrink-0" style={{ background: cfg.dot }} />
              <span className="text-ink2 uppercase tracking-wide">{item.company}</span>
              <span
                className="px-2 py-0.5 rounded-md font-bold text-[10px] tracking-wider"
                style={{ color: cfg.text, background: cfg.bg }}
              >
                {item.verdict}
              </span>
              <span className="font-mono" style={{ color: cfg.text }}>
                {item.confidence?.toFixed(0)}%
              </span>
              <span className="text-[rgba(255,255,255,0.1)] ml-2">·</span>
            </span>
          )
        })}
      </div>
    </div>
  )
}
