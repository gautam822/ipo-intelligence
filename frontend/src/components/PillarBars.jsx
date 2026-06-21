import { motion } from "framer-motion"

function colorFor(score) {
  if (score >= 6.5) return { bar: "#059669", bg: "#ECFDF5", text: "#059669" }
  if (score >= 4)   return { bar: "#D97706", bg: "#FFFBEB", text: "#B45309" }
  return                   { bar: "#DC2626", bg: "#FEF2F2", text: "#DC2626" }
}

export default function PillarBars({ pillars = {} }) {
  return (
    <div className="flex flex-col divide-y divide-border">
      {Object.entries(pillars).map(([name, score], i) => {
        const cfg = colorFor(score)
        return (
          <motion.div
            key={name}
            initial={{ opacity: 0, x: -8 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: i * 0.07, duration: 0.35 }}
            className="flex items-center gap-3 py-3"
          >
            <span className="text-[13px] text-ink2 font-medium w-[160px] flex-shrink-0">{name}</span>
            <div className="flex-1 h-2 bg-surface2 rounded-full overflow-hidden border border-border">
              <motion.div
                className="h-full rounded-full"
                initial={{ width: 0 }}
                animate={{ width: `${score * 10}%` }}
                transition={{ delay: i * 0.07 + 0.15, duration: 0.7, ease: "easeOut" }}
                style={{ background: cfg.bar }}
              />
            </div>
            <span
              className="tabular text-xs font-bold w-8 text-right flex-shrink-0"
              style={{ color: cfg.text }}
            >
              {score.toFixed(1)}
            </span>
          </motion.div>
        )
      })}
    </div>
  )
}
