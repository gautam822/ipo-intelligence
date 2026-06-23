import { useState, useEffect } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { CheckCircle, Zap } from "lucide-react"

const STEPS = [
  "Fetching DRHP filings from SEBI…",
  "Extracting 35 financial signals…",
  "Running calibrated XGBoost model…",
  "Applying RL confidence overlay…",
  "Computing SHAP explainability…",
  "Generating verdict…",
]

const VERDICT_COLOR = {
  INVEST:  { color: "#34D399", glow: "rgba(52,211,153,0.5)",  bg: "rgba(52,211,153,0.08)" },
  AVOID:   { color: "#FB7185", glow: "rgba(251,113,133,0.5)", bg: "rgba(251,113,133,0.08)" },
  NEUTRAL: { color: "#FBBF24", glow: "rgba(251,191,36,0.5)",  bg: "rgba(251,191,36,0.08)" },
}

export default function CinematicReveal({ isVisible, company, result, onDismiss }) {
  const [step, setStep]     = useState(0)
  const [phase, setPhase]   = useState("scanning") // scanning | revealing | done
  const [confVal, setConf]  = useState(0)

  useEffect(() => {
    if (!isVisible) { setStep(0); setPhase("scanning"); setConf(0); return }

    let s = 0
    const id = setInterval(() => {
      s++
      setStep(s)
      if (s >= STEPS.length - 1) clearInterval(id)
    }, 600)
    return () => clearInterval(id)
  }, [isVisible])

  useEffect(() => {
    if (result && step >= STEPS.length - 1) {
      setPhase("revealing")
      const target = result.confidence_pct ?? 0
      let v = 0
      const id = setInterval(() => {
        v = Math.min(v + 2, target)
        setConf(v)
        if (v >= target) {
          clearInterval(id)
          setTimeout(() => setPhase("done"), 800)
        }
      }, 18)
    }
  }, [result, step])

  useEffect(() => {
    if (phase === "done") setTimeout(onDismiss, 500)
  }, [phase])

  const cfg = result ? (VERDICT_COLOR[result.verdict] ?? VERDICT_COLOR.NEUTRAL) : null

  return (
    <AnimatePresence>
      {isVisible && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.3 }}
          className="fixed inset-0 z-[100] flex items-center justify-center"
          style={{ background: "rgba(5,6,12,0.97)", backdropFilter: "blur(20px)" }}
        >
          {/* Scan line */}
          {phase === "scanning" && (
            <div className="absolute inset-0 overflow-hidden pointer-events-none">
              <div className="scan-line" style={{ top: 0 }} />
            </div>
          )}

          {/* Glow when revealing */}
          {cfg && phase !== "scanning" && (
            <motion.div
              initial={{ opacity: 0, scale: 0.5 }}
              animate={{ opacity: 1, scale: 1 }}
              className="absolute inset-0 pointer-events-none"
              style={{ background: `radial-gradient(ellipse 60% 60% at 50% 50%, ${cfg.glow}20 0%, transparent 70%)` }}
            />
          )}

          <div className="w-full max-w-md px-6 text-center">
            {/* Company */}
            <motion.p
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              className="text-xs font-mono tracking-[0.14em] uppercase text-muted mb-8"
            >
              Analyzing · {company}
            </motion.p>

            {/* Steps */}
            <AnimatePresence mode="popLayout">
              {phase === "scanning" && (
                <motion.div
                  key="steps"
                  exit={{ opacity: 0, y: -20 }}
                  className="flex flex-col gap-2 mb-8"
                >
                  {STEPS.map((s, i) => (
                    <motion.div
                      key={s}
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: i <= step ? 1 : 0.2, x: 0 }}
                      transition={{ delay: i * 0.05 }}
                      className="flex items-center gap-3 text-sm"
                    >
                      <div className={`w-4 h-4 rounded-full flex items-center justify-center flex-shrink-0 transition-all duration-300 ${
                        i < step ? "bg-invest-dim border border-invest" : i === step ? "border border-accent animate-pulse" : "border border-[rgba(255,255,255,0.08)]"
                      }`}>
                        {i < step && <CheckCircle size={10} className="text-invest" />}
                      </div>
                      <span className={i <= step ? "text-ink2" : "text-muted"}>{s}</span>
                    </motion.div>
                  ))}
                </motion.div>
              )}
            </AnimatePresence>

            {/* Verdict explosion */}
            <AnimatePresence>
              {phase !== "scanning" && cfg && result && (
                <motion.div
                  key="verdict"
                  initial={{ opacity: 0, scale: 0.5 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ type: "spring", stiffness: 200, damping: 18 }}
                  className="flex flex-col items-center gap-4"
                >
                  <div className="flex items-center gap-3 mb-2">
                    <Zap size={20} style={{ color: cfg.color }} className="animate-glow" />
                    <span className="text-xs font-mono tracking-widest text-muted uppercase">Verdict</span>
                    <Zap size={20} style={{ color: cfg.color }} className="animate-glow" />
                  </div>

                  <motion.span
                    className="font-display font-black text-7xl tracking-tight"
                    style={{
                      color: cfg.color,
                      textShadow: `0 0 60px ${cfg.glow}, 0 0 120px ${cfg.glow}80`,
                    }}
                    animate={{ textShadow: [
                      `0 0 60px ${cfg.glow}, 0 0 120px ${cfg.glow}80`,
                      `0 0 100px ${cfg.glow}, 0 0 200px ${cfg.glow}80`,
                      `0 0 60px ${cfg.glow}, 0 0 120px ${cfg.glow}80`,
                    ]}}
                    transition={{ duration: 2, repeat: Infinity }}
                  >
                    {result.verdict}
                  </motion.span>

                  <div className="flex items-center gap-2 mt-2">
                    <span className="text-muted text-sm font-mono">Confidence</span>
                    <span className="font-mono font-bold text-2xl" style={{ color: cfg.color }}>
                      {confVal.toFixed(0)}%
                    </span>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>

            {/* Loading dots */}
            {phase === "scanning" && (
              <div className="flex justify-center gap-1.5 mt-2">
                {[0, 1, 2].map(i => (
                  <motion.div
                    key={i}
                    className="w-1 h-1 rounded-full bg-accent"
                    animate={{ opacity: [0.3, 1, 0.3] }}
                    transition={{ duration: 1, repeat: Infinity, delay: i * 0.2 }}
                  />
                ))}
              </div>
            )}
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}
