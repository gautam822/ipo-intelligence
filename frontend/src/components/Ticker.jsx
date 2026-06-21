const COLORS = { INVEST: "#059669", NEUTRAL: "#D97706", AVOID: "#DC2626" }
const BG     = { INVEST: "#ECFDF5", NEUTRAL: "#FFFBEB", AVOID: "#FEF2F2" }

export default function Ticker({ items = [] }) {
  if (!items.length) return null
  const loop = [...items, ...items]

  return (
    <div className="relative w-full overflow-hidden bg-surface border-b border-border py-2">
      <div className="absolute left-0 top-0 bottom-0 w-20 bg-gradient-to-r from-surface to-transparent z-10 pointer-events-none" />
      <div className="absolute right-0 top-0 bottom-0 w-20 bg-gradient-to-l from-surface to-transparent z-10 pointer-events-none" />
      <div className="flex w-max animate-ticker gap-8 whitespace-nowrap">
        {loop.map((it, i) => (
          <span key={i} className="flex items-center gap-2 text-sm">
            <span
              className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full font-semibold text-xs"
              style={{
                background: BG[it.verdict],
                color: COLORS[it.verdict],
              }}
            >
              <span className="w-1.5 h-1.5 rounded-full inline-block" style={{ background: COLORS[it.verdict] }} />
              {it.verdict}
            </span>
            <span className="text-ink2 font-medium">{it.company}</span>
            <span className="text-muted tabular text-xs">{it.confidence?.toFixed(0)}%</span>
          </span>
        ))}
      </div>
    </div>
  )
}
