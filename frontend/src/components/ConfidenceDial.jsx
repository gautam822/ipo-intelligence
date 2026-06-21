import { useEffect, useState } from "react"
import { motion } from "framer-motion"

const COLORS = {
  INVEST:  { stroke: "#059669", track: "#D1FAE5", text: "#059669" },
  NEUTRAL: { stroke: "#D97706", track: "#FEF3C7", text: "#D97706" },
  AVOID:   { stroke: "#DC2626", track: "#FEE2E2", text: "#DC2626" },
}

export default function ConfidenceDial({ confidence, verdict, size = 140 }) {
  const [animated, setAnimated] = useState(0)
  const cfg = COLORS[verdict] || COLORS.NEUTRAL
  const r = size / 2 - 12
  const cx = size / 2
  const cy = size / 2
  const circ = 2 * Math.PI * r

  useEffect(() => {
    setAnimated(0)
    const t = setTimeout(() => setAnimated(confidence), 100)
    return () => clearTimeout(t)
  }, [confidence, verdict])

  const offset = circ * (1 - animated / 100)

  return (
    <div className="relative flex-shrink-0" style={{ width: size, height: size }}>
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
        {/* Track */}
        <circle cx={cx} cy={cy} r={r} fill="none" stroke="#E2E8F0" strokeWidth="10" />
        {/* Progress */}
        <circle
          cx={cx} cy={cy} r={r}
          fill="none"
          stroke={cfg.stroke}
          strokeWidth="10"
          strokeLinecap="round"
          strokeDasharray={circ}
          strokeDashoffset={offset}
          transform={`rotate(-90 ${cx} ${cy})`}
          style={{ transition: "stroke-dashoffset 1.2s cubic-bezier(0.16, 1, 0.3, 1)" }}
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <motion.span
          key={confidence}
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ delay: 0.3, type: "spring", stiffness: 200 }}
          className="tabular font-bold text-2xl"
          style={{ color: cfg.text }}
        >
          {Math.round(animated)}
          <span className="text-sm font-medium text-muted ml-0.5">%</span>
        </motion.span>
        <span className="font-mono text-[9px] tracking-widest text-muted uppercase mt-0.5">
          confidence
        </span>
      </div>
    </div>
  )
}
