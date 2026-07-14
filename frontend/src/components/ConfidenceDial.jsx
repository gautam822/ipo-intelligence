import { useEffect, useState } from "react"

const COLORS = {
  INVEST:  "#40D993",
  NEUTRAL: "#E5B84B",
  AVOID:   "#F2657E",
}

// Instrument gauge: a 270° arc with etched tick marks — reads like a
// physical meter, not a neon ring.
export default function ConfidenceDial({ pct = 0, verdict = "NEUTRAL", size = 128 }) {
  // SSR renders the resting value; the browser animates up from 0 on mount.
  const [displayed, setDisplayed] = useState(() => (typeof window === "undefined" ? pct : 0))
  const stroke = COLORS[verdict] ?? COLORS.NEUTRAL

  const cx = size / 2
  const cy = size / 2
  const r  = size / 2 - 10

  // 270° sweep, opening at the bottom (135° → 405°)
  const START = 135
  const SWEEP = 270
  const polar = (deg, radius) => {
    const rad = (deg * Math.PI) / 180
    return [cx + radius * Math.cos(rad), cy + radius * Math.sin(rad)]
  }
  const arcPath = (fromDeg, toDeg, radius) => {
    const [x1, y1] = polar(fromDeg, radius)
    const [x2, y2] = polar(toDeg, radius)
    const large = toDeg - fromDeg > 180 ? 1 : 0
    return `M ${x1} ${y1} A ${radius} ${radius} 0 ${large} 1 ${x2} ${y2}`
  }

  // Tick marks: 21 ticks, majors every 5th (0/25/50/75/100)
  const ticks = Array.from({ length: 21 }, (_, i) => {
    const deg = START + (SWEEP * i) / 20
    const major = i % 5 === 0
    const [x1, y1] = polar(deg, r - (major ? 0 : 1))
    const [x2, y2] = polar(deg, r - (major ? 6 : 3.5))
    return { x1, y1, x2, y2, major }
  })

  const progressEnd = START + (SWEEP * displayed) / 100
  const trackLen = (Math.PI * r * SWEEP) / 180
  const progLen  = (trackLen * displayed) / 100

  useEffect(() => {
    let frame
    const start = performance.now()
    const duration = 1100
    function tick(now) {
      const t = Math.min((now - start) / duration, 1)
      const ease = 1 - Math.pow(1 - t, 3)
      setDisplayed(ease * pct)
      if (t < 1) frame = requestAnimationFrame(tick)
    }
    frame = requestAnimationFrame(tick)
    return () => cancelAnimationFrame(frame)
  }, [pct])

  return (
    <div className="relative flex-shrink-0" style={{ width: size, height: size }} role="img" aria-label={`Confidence ${Math.round(pct)} percent`}>
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
        {/* Etched ticks */}
        {ticks.map((t, i) => (
          <line
            key={i}
            x1={t.x1} y1={t.y1} x2={t.x2} y2={t.y2}
            stroke={t.major ? "rgba(255,255,255,0.28)" : "rgba(255,255,255,0.12)"}
            strokeWidth={t.major ? 1.5 : 1}
          />
        ))}
        {/* Track */}
        <path d={arcPath(START, START + SWEEP, r - 9)} fill="none" stroke="rgba(255,255,255,0.07)" strokeWidth="3" strokeLinecap="round" />
        {/* Progress */}
        {displayed > 0.5 && (
          <path
            d={arcPath(START, progressEnd, r - 9)}
            fill="none"
            stroke={stroke}
            strokeWidth="3"
            strokeLinecap="round"
          />
        )}
        {/* Needle tip */}
        {displayed > 0.5 && (() => {
          const [nx, ny] = polar(progressEnd, r - 9)
          return <circle cx={nx} cy={ny} r="2.6" fill={stroke} />
        })()}
      </svg>

      {/* Center readout */}
      <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
        <span className="font-mono font-semibold tabular leading-none text-ink" style={{ fontSize: size * 0.24 }}>
          {Math.round(displayed)}
        </span>
        <span className="font-mono text-muted uppercase" style={{ fontSize: size * 0.068, letterSpacing: "0.14em", marginTop: size * 0.045 }}>
          conf&thinsp;%
        </span>
      </div>
    </div>
  )
}
