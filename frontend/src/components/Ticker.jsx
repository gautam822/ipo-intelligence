const COLORS = {
  INVEST:  "#40D993",
  NEUTRAL: "#E5B84B",
  AVOID:   "#F2657E",
}

// Exchange tape: the app's memory scrolling by. Pauses on hover.
export default function Ticker({ items = [] }) {
  const seen = new Set()
  const unique = items.filter((it) => {
    const key = (it.company || "").toLowerCase()
    if (seen.has(key)) return false
    seen.add(key)
    return true
  })
  if (!unique.length) return null
  const doubled = [...unique, ...unique]

  return (
    <div className="tape-track w-full overflow-hidden border-b border-border bg-[rgba(255,255,255,0.015)]" aria-hidden="true">
      <div className="flex animate-tape whitespace-nowrap will-change-transform py-2" style={{ width: "max-content" }}>
        {doubled.map((item, i) => {
          const c = COLORS[item.verdict] ?? COLORS.NEUTRAL
          return (
            <span key={i} className="inline-flex items-center font-mono text-[11px]">
              <span className="inline-flex items-center gap-2 px-5">
                <span className="w-1 h-1 rounded-full flex-shrink-0" style={{ background: c }} />
                <span className="text-ink2 uppercase tracking-wider">{item.company}</span>
                <span className="font-semibold tracking-wider" style={{ color: c }}>
                  {item.verdict}
                </span>
                <span className="tabular text-muted">{item.confidence?.toFixed(0)}</span>
              </span>
              <span className="h-3 w-px bg-[rgba(255,255,255,0.08)]" />
            </span>
          )
        })}
      </div>
    </div>
  )
}
