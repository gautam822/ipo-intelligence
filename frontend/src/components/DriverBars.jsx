import { motion } from "framer-motion"

export default function DriverBars({ drivers = [] }) {
  const maxAbs = Math.max(...drivers.map(d => Math.abs(d.shap)), 0.0001)

  return (
    <div className="flex flex-col gap-2">
      {drivers.map((d, i) => {
        const pct  = (Math.abs(d.shap) / maxAbs) * 45
        const pos  = d.shap > 0
        const color= pos ? "#34D399" : "#FB7185"
        return (
          <div key={d.feature} className="flex items-center gap-3">
            <span className="text-[10px] font-mono text-muted w-36 text-right flex-shrink-0 truncate" title={d.feature}>
              {d.feature}
            </span>
            <div className="flex-1 h-5 relative flex items-center">
              {/* center line */}
              <div className="absolute left-1/2 top-0 bottom-0 w-px bg-[rgba(255,255,255,0.08)]" />
              {/* bar */}
              <motion.div
                className="absolute top-1 bottom-1 rounded-sm"
                style={{
                  [pos ? "left" : "right"]: "50%",
                  background: `linear-gradient(${pos ? "90deg" : "-90deg"}, ${color}30, ${color})`,
                  boxShadow: `0 0 8px ${color}40`,
                }}
                initial={{ width: 0 }}
                animate={{ width: `${pct}%` }}
                transition={{ delay: i * 0.04, duration: 0.7, ease: [0.4, 0, 0.2, 1] }}
              />
            </div>
            <span className="text-[10px] font-mono w-12 flex-shrink-0" style={{ color }}>
              {d.shap > 0 ? "+" : ""}{d.shap.toFixed(3)}
            </span>
          </div>
        )
      })}
      <div className="flex justify-between text-[9px] font-mono text-muted mt-1 px-[calc(36px+12px)]">
        <span>← AVOID</span>
        <span>INVEST →</span>
      </div>
    </div>
  )
}
