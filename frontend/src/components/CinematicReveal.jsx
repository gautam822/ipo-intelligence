import { useState, useEffect } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { TrendingUp, TrendingDown, Minus, CheckCircle } from "lucide-react"

const STEPS = [
  "Fetching DRHP filings from SEBI...",
  "Extracting 35 financial signals...",
  "Running calibrated XGBoost model...",
  "Applying reinforcement learning overlay...",
  "Computing SHAP explainability...",
  "Generating verdict...",
]

const VERDICT_CONFIG = {
  INVEST:  { color: "#059669", glow: "rgba(5,150,105,0.5)",  Icon: TrendingUp,   bg: "from-emerald-950" },
  NEUTRAL: { color: "#D97706", glow: "rgba(217,119,6,0.5)",  Icon: Minus,        bg: "from-amber-950"   },
  AVOID:   { color: "#DC2626", glow: "rgba(220,38,38,0.5)",  Icon: TrendingDown, bg: "from-red-950"     },
}

export default function CinematicReveal({ isVisible, company, result, onDismiss }) {
  const [phase, setPhase] = useState("scanning") // scanning | revealing | done
  const [stepIdx, setStepIdx] = useState(0)
  const [confidence, setConfidence] = useState(0)

  // Cycle through steps while scanning
  useEffect(() => {
    if (!isVisible || phase !== "scanning") return
    const t = setInterval(() => {
      setStepIdx((i) => (i + 1) % STEPS.length)
    }, 900)
    return () => clearInterval(t)
  }, [isVisible, phase])

  // When result arrives, transition to reveal
  useEffect(() => {
    if (result && phase === "scanning") {
      setStepIdx(STEPS.length - 1)
      const t = setTimeout(() => {
        setPhase("revealing")
        // Animate confidence number
        let n = 0
        const target = result.confidence_pct || 0
        const step = target / 40
        const counter = setInterval(() => {
          n = Math.min(n + step, target)
          setConfidence(Math.round(n))
          if (n >= target) clearInterval(counter)
        }, 30)
      }, 600)
      return () => clearTimeout(t)
    }
  }, [result, phase])

  // Auto-dismiss after reveal
  useEffect(() => {
    if (phase === "revealing") {
      const t = setTimeout(() => {
        setPhase("done")
        setTimeout(() => {
          onDismiss?.()
          setPhase("scanning")
          setStepIdx(0)
          setConfidence(0)
        }, 700)
      }, 2800)
      return () => clearTimeout(t)
    }
  }, [phase, onDismiss])

  const cfg = result ? VERDICT_CONFIG[result.verdict] : null

  return (
    <AnimatePresence>
      {isVisible && (
        <motion.div
          key="cinema"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0, y: "-100%" }}
          transition={
            phase === "done"
              ? { duration: 0.7, ease: [0.76, 0, 0.24, 1] }
              : { duration: 0.3 }
          }
          className="fixed inset-0 z-50 flex flex-col items-center justify-center overflow-hidden"
          style={{ background: "#080D1A" }}
        >
          {/* Ambient glow */}
          {cfg && (
            <motion.div
              initial={{ opacity: 0, scale: 0.5 }}
              animate={{ opacity: 0.18, scale: 1.5 }}
              transition={{ duration: 1 }}
              className="absolute inset-0 pointer-events-none"
              style={{
                background: `radial-gradient(circle at 50% 50%, ${cfg.glow}, transparent 60%)`,
              }}
            />
          )}

          {/* Scan line — only during loading */}
          {phase === "scanning" && (
            <div className="absolute inset-0 overflow-hidden pointer-events-none">
              <div className="scan-line" />
            </div>
          )}

          {/* Grid overlay */}
          <div
            className="absolute inset-0 pointer-events-none opacity-[0.04]"
            style={{
              backgroundImage: "linear-gradient(#fff 1px, transparent 1px), linear-gradient(90deg, #fff 1px, transparent 1px)",
              backgroundSize: "60px 60px",
            }}
          />

          {/* Content */}
          <div className="relative z-10 flex flex-col items-center text-center px-6 max-w-lg w-full">
            {/* Company name */}
            <motion.p
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="text-white/40 font-mono text-xs tracking-[0.3em] uppercase mb-8"
            >
              {company}
            </motion.p>

            {/* Scanning phase */}
            {phase === "scanning" && (
              <div className="flex flex-col items-center gap-6">
                {/* Pulse rings */}
                <div className="relative w-20 h-20 flex items-center justify-center">
                  {[0, 1, 2].map((i) => (
                    <motion.div
                      key={i}
                      className="absolute rounded-full border border-accent/30"
                      initial={{ width: 32, height: 32, opacity: 0.8 }}
                      animate={{ width: 80, height: 80, opacity: 0 }}
                      transition={{ duration: 1.8, delay: i * 0.6, repeat: Infinity, ease: "easeOut" }}
                    />
                  ))}
                  <div className="w-8 h-8 rounded-full bg-accent/20 border border-accent/50 flex items-center justify-center">
                    <div className="w-2 h-2 rounded-full bg-accent animate-pulse" />
                  </div>
                </div>

                {/* Step text */}
                <AnimatePresence mode="wait">
                  <motion.p
                    key={stepIdx}
                    initial={{ opacity: 0, y: 6 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -6 }}
                    transition={{ duration: 0.25 }}
                    className="text-white/60 font-mono text-sm"
                  >
                    {STEPS[stepIdx]}
                  </motion.p>
                </AnimatePresence>

                {/* Progress dots */}
                <div className="flex gap-1.5 mt-2">
                  {STEPS.map((_, i) => (
                    <motion.div
                      key={i}
                      className="h-1 rounded-full"
                      animate={{
                        width: i === stepIdx ? 20 : 6,
                        background: i <= stepIdx ? "#2563EB" : "rgba(255,255,255,0.15)",
                      }}
                      transition={{ duration: 0.3 }}
                    />
                  ))}
                </div>
              </div>
            )}

            {/* Revealing phase */}
            {phase === "revealing" && cfg && result && (
              <div className="flex flex-col items-center gap-5">
                <motion.div
                  initial={{ scale: 0.3, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  transition={{ type: "spring", stiffness: 180, damping: 14, delay: 0.1 }}
                >
                  <cfg.Icon
                    size={48}
                    strokeWidth={2}
                    style={{ color: cfg.color, filter: `drop-shadow(0 0 20px ${cfg.glow})` }}
                  />
                </motion.div>

                <motion.h1
                  initial={{ scale: 0.5, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  transition={{ type: "spring", stiffness: 220, damping: 16, delay: 0.2 }}
                  className="font-black text-7xl sm:text-8xl tracking-tight"
                  style={{
                    color: cfg.color,
                    textShadow: `0 0 60px ${cfg.glow}`,
                  }}
                >
                  {result.verdict}
                </motion.h1>

                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.5 }}
                  className="flex items-baseline gap-2"
                >
                  <span className="text-white/90 font-bold text-3xl tabular">{confidence}</span>
                  <span className="text-white/40 font-mono text-sm">% confidence</span>
                </motion.div>

                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.8 }}
                  className="flex items-center gap-2 text-white/30 font-mono text-xs"
                >
                  <CheckCircle size={12} />
                  <span>Analysis complete — loading report</span>
                </motion.div>
              </div>
            )}
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}
