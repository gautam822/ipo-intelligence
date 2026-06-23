import { motion } from "framer-motion"

function colorFor(score) {
  if (score >= 6.5) return { bar: "#34D399", text: "#34D399" }
  if (score >= 4)   return { bar: "#FBBF24", text: "#FBBF24" }
  return               { bar: "#FB7185", text: "#FB7185" }
}

export default function PillarBars({ pillars = {} }) {
  const entries = Object.entries(pillars)
  return (
    <div className="flex flex-col gap-3">
      {entries.map(([name, score], i) => {
        const { bar, text } = colorFor(score)
        const pct = (score / 10) * 100
        return (
          <div key={name}>
            <div className="flex justify-between items-center mb-1.5">
              <span className="text-xs font-medium text-ink2">{name}</span>
              <span className="text-xs font-mono font-semibold" style={{ color: text }}>{score.toFixed(1)}</span>
            </div>
            <div className="h-1.5 rounded-full bg-[rgba(255,255,255,0.06)] overflow-hidden">
              <motion.div
                className="h-full rounded-full origin-left"
                style={{ background: `linear-gradient(90deg, ${bar}80, ${bar})` }}
                initial={{ scaleX: 0 }}
                animate={{ scaleX: 1 }}
                transition={{ delay: i * 0.06, duration: 0.8, ease: [0.4, 0, 0.2, 1] }}
                custom={pct}
              >
                <div style={{ width: `${pct}%`, height: "100%", borderRadius: "inherit" }} />
              </motion.div>
            </div>
          </div>
        )
      })}
    </div>
  )
}
