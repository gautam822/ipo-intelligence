import { motion } from "framer-motion"

const humanize = (s) => s.replaceAll("_", " ")

// SHAP drivers on a diverging axis: what pushed the model toward
// AVOID (left) or INVEST (right).
export default function DriverBars({ drivers = [] }) {
  const maxAbs = Math.max(...drivers.map((d) => Math.abs(d.shap)), 0.0001)

  return (
    <div className="flex flex-col gap-2.5">
      {drivers.map((d, i) => {
        const pct = (Math.abs(d.shap) / maxAbs) * 46
        const pos = d.shap > 0
        const color = pos ? "#40D993" : "#F2657E"
        return (
          <div key={d.feature} className="flex items-center gap-3">
            <span
              className="font-mono text-[10px] text-ink2 w-32 sm:w-36 text-right flex-shrink-0 truncate"
              title={humanize(d.feature)}
            >
              {humanize(d.feature)}
            </span>
            <div className="flex-1 h-4 relative flex items-center">
              <div className="absolute inset-y-0 left-1/2 w-px bg-[rgba(255,255,255,0.14)]" />
              <motion.div
                className="absolute top-[5px] bottom-[5px] rounded-[2px]"
                style={{ [pos ? "left" : "right"]: "50%", background: color, opacity: 0.9 }}
                initial={{ width: 0 }}
                animate={{ width: `${pct}%` }}
                transition={{ delay: 0.1 + i * 0.05, duration: 0.65, ease: [0.22, 1, 0.36, 1] }}
              />
            </div>
            <span className="font-mono text-[10px] tabular w-12 flex-shrink-0 text-right" style={{ color }}>
              {d.shap > 0 ? "+" : ""}{d.shap.toFixed(3)}
            </span>
          </div>
        )
      })}
      <div className="flex justify-between font-mono text-[9px] tracking-caps uppercase mt-1.5 pl-[140px] pr-12 max-sm:pl-0 max-sm:pr-0">
        <span className="text-avoid/70">‹ pushes avoid</span>
        <span className="text-invest/70">pushes invest ›</span>
      </div>
    </div>
  )
}
