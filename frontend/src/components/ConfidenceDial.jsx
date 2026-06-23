import { useEffect, useState } from "react"
import { motion } from "framer-motion"

const COLORS = {
  INVEST:  { stroke: "#34D399", glow: "rgba(52,211,153,0.5)"  },
  NEUTRAL: { stroke: "#FBBF24", glow: "rgba(251,191,36,0.5)"  },
  AVOID:   { stroke: "#FB7185", glow: "rgba(251,113,133,0.5)" },
}

export default function ConfidenceDial({ pct = 0, verdict = "NEUTRAL", size = 120 }) {
  const [displayed, setDisplayed] = useState(0)
  const { stroke, glow } = COLORS[verdict] ?? COLORS.NEUTRAL

  const r   = size / 2 - 12
  const cx  = size / 2
  const cy  = size / 2
  const circ = 2 * Math.PI * r
  const offset = circ * (1 - displayed / 100)

  useEffect(() => {
    let frame
    const start = performance.now()
    const duration = 1200
    function tick(now) {
      const t = Math.min((now - start) / duration, 1)
      const ease = 1 - Math.pow(1 - t, 3)
      setDisplayed(Math.round(ease * pct))
      if (t < 1) frame = requestAnimationFrame(tick)
    }
    frame = requestAnimationFrame(tick)
    return () => cancelAnimationFrame(frame)
  }, [pct])

  return (
    <div className="relative" style={{ width: size, height: size }}>
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
        <defs>
          <filter id={`dial-glow-${verdict}`}>
            <feGaussianBlur stdDeviation="3" result="blur" />
            <feMerge><feMergeNode in="blur" /><feMergeNode in="SourceGraphic" /></feMerge>
          </filter>
        </defs>
        {/* Track */}
        <circle cx={cx} cy={cy} r={r} fill="none" stroke="rgba(255,255,255,0.06)" strokeWidth="8" />
        {/* Progress */}
        <motion.circle
          cx={cx} cy={cy} r={r}
          fill="none"
          stroke={stroke}
          strokeWidth="8"
          strokeLinecap="round"
          strokeDasharray={circ}
          strokeDashoffset={offset}
          transform={`rotate(-90 ${cx} ${cy})`}
          filter={`url(#dial-glow-${verdict})`}
          initial={{ strokeDashoffset: circ }}
          animate={{ strokeDashoffset: offset }}
          transition={{ duration: 1.2, ease: [0.4, 0, 0.2, 1] }}
        />
        {/* Number */}
        <text
          x={cx} y={cy + 2}
          textAnchor="middle"
          dominantBaseline="middle"
          className="num"
          style={{ fontFamily: "'JetBrains Mono',monospace", fontWeight: 700, fontSize: size * 0.18, fill: "#F0EEE8" }}
        >
          {displayed}
        </text>
        <text
          x={cx} y={cy + size * 0.17}
          textAnchor="middle"
          style={{ fontFamily: "'JetBrains Mono',monospace", fontSize: size * 0.09, fill: "#4B5563", letterSpacing: "0.05em" }}
        >
          CONFIDENCE
        </text>
      </svg>
    </div>
  )
}
