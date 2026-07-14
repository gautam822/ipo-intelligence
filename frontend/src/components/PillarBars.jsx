import { motion } from "framer-motion"

function colorFor(score) {
  if (score >= 6.5) return "#40D993"
  if (score >= 4)   return "#E5B84B"
  return "#F2657E"
}

// Report-style rows: label … dotted leader … score, hairline meter below.
export default function PillarBars({ pillars = {} }) {
  const entries = Object.entries(pillars)
  return (
    <div className="flex flex-col gap-4">
      {entries.map(([name, score], i) => {
        const c = colorFor(score)
        const pct = Math.max(0, Math.min(100, (score / 10) * 100))
        return (
          <div key={name}>
            <div className="flex items-baseline mb-2">
              <span className="text-[13px] text-ink2">{name}</span>
              <span className="leader" aria-hidden="true" />
              <span className="font-mono text-xs font-semibold tabular" style={{ color: c }}>
                {score.toFixed(1)}<span className="text-muted font-normal"> / 10</span>
              </span>
            </div>
            <div className="h-[3px] rounded-full bg-[rgba(255,255,255,0.05)] overflow-hidden">
              <motion.div
                className="h-full rounded-full origin-left"
                style={{ background: c, width: `${pct}%` }}
                initial={{ scaleX: 0 }}
                animate={{ scaleX: 1 }}
                transition={{ delay: 0.1 + i * 0.06, duration: 0.8, ease: [0.22, 1, 0.36, 1] }}
              />
            </div>
          </div>
        )
      })}
    </div>
  )
}
