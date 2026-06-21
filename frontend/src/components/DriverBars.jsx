import { motion } from "framer-motion"

export default function DriverBars({ drivers = [] }) {
  const maxAbs = Math.max(...drivers.map((d) => Math.abs(d.shap)), 0.0001)

  return (
    <div className="flex flex-col gap-3">
      {drivers.map((d, i) => {
        const pct = (Math.abs(d.shap) / maxAbs) * 45
        const positive = d.shap > 0
        const color = positive ? "#059669" : "#DC2626"
        const dimColor = positive ? "#ECFDF5" : "#FEF2F2"

        return (
          <motion.div
            key={d.feature}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: i * 0.06, duration: 0.35 }}
            className="flex items-center gap-3"
          >
            <span className="font-mono text-[11px] text-muted w-[130px] flex-shrink-0 text-right truncate">
              {d.feature.replace(/_/g, " ")}
            </span>
            <div className="relative flex-1 h-5 bg-surface2 rounded-lg overflow-hidden border border-border">
              <div className="absolute left-1/2 top-0 bottom-0 w-px bg-border z-10" />
              <motion.div
                className="absolute top-1 bottom-1 rounded-md"
                initial={{ width: 0 }}
                animate={{ width: `${pct}%` }}
                transition={{ delay: i * 0.06 + 0.2, duration: 0.6, ease: "easeOut" }}
                style={{
                  left: positive ? "50%" : `${50 - pct}%`,
                  background: color,
                  opacity: 0.8,
                }}
              />
            </div>
            <span
              className="tabular text-[11px] font-medium w-12 flex-shrink-0"
              style={{ color }}
            >
              {d.shap > 0 ? "+" : ""}{d.shap.toFixed(2)}
            </span>
          </motion.div>
        )
      })}
    </div>
  )
}
