import { useEffect, useRef, useState } from "react"

// Parses "700", "80%", "+21.1%", "₹5k", "35/35" into an animatable number
// while preserving any prefix/suffix. Counts up once when scrolled into view.
// SSR renders the final value so no-JS / crawlers see the real figure.
function parse(str) {
  const s = String(str)
  const m = s.match(/-?\d[\d,]*\.?\d*/)
  if (!m) return null
  const numStr = m[0].replace(/,/g, "")
  const value = parseFloat(numStr)
  const decimals = (numStr.split(".")[1] || "").length
  return { prefix: s.slice(0, m.index), value, decimals, suffix: s.slice(m.index + m[0].length) }
}

export default function AnimatedNumber({ value, duration = 1100, className, style }) {
  const parsed = parse(value)
  const isServer = typeof window === "undefined"
  const [display, setDisplay] = useState(() =>
    parsed && !isServer ? 0 : parsed ? parsed.value : null
  )
  const ref = useRef(null)
  const ran = useRef(false)

  useEffect(() => {
    if (!parsed || ran.current) return
    const el = ref.current
    if (!el) return

    const start = () => {
      if (ran.current) return
      ran.current = true
      const t0 = performance.now()
      const tick = (now) => {
        const p = Math.min((now - t0) / duration, 1)
        // easeOutExpo for a snappy settle
        const eased = p === 1 ? 1 : 1 - Math.pow(2, -10 * p)
        setDisplay(parsed.value * eased)
        if (p < 1) requestAnimationFrame(tick)
        else setDisplay(parsed.value)
      }
      requestAnimationFrame(tick)
    }

    const io = new IntersectionObserver(
      (entries) => entries.forEach((e) => e.isIntersecting && start()),
      { threshold: 0.4 }
    )
    io.observe(el)
    return () => io.disconnect()
  }, [parsed, duration])

  if (!parsed) return <span className={className} style={style}>{value}</span>

  const shown = display != null ? display.toFixed(parsed.decimals) : parsed.value.toFixed(parsed.decimals)
  return (
    <span ref={ref} className={className} style={style}>
      {parsed.prefix}{shown}{parsed.suffix}
    </span>
  )
}
