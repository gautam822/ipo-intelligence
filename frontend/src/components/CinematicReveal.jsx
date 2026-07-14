import { useState, useEffect } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { assess } from "../lib/reliability"

const STEPS = [
  "Fetching DRHP filings from SEBI",
  "Extracting 35 financial signals",
  "Running calibrated XGBoost model",
  "Applying RL confidence overlay",
  "Computing SHAP attribution",
  "Sealing verdict",
]

const VERDICT_COLOR = {
  INVEST:  "#40D993",
  AVOID:   "#F2657E",
  NEUTRAL: "#E5B84B",
}

// The reveal: a terminal types its work, then the verdict is stamped.
export default function CinematicReveal({ isVisible, company, result, onDismiss }) {
  const [step, setStep]   = useState(0)
  const [phase, setPhase] = useState("scanning") // scanning | revealing | done
  const [confVal, setConf] = useState(0)

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
    if (result && step >= STEPS.length - 1 && phase === "scanning") {
      setPhase("revealing")
      const { reliable, confidencePct } = assess(result)
      // Only count up a real confidence; unreliable results show no fake %.
      const target = reliable && confidencePct != null ? confidencePct : 0
      let v = 0
      const id = setInterval(() => {
        v = Math.min(v + 2, target)
        setConf(v)
        if (v >= target) {
          clearInterval(id)
          setTimeout(() => setPhase("done"), 900)
        }
      }, 16)
      return () => clearInterval(id)
    }
  }, [result, step, phase])

  useEffect(() => {
    if (phase === "done") {
      const t = setTimeout(onDismiss, 400)
      return () => clearTimeout(t)
    }
  }, [phase, onDismiss])

  const verdictView = assess(result)
  const color = result
    ? verdictView.reliable
      ? (VERDICT_COLOR[result.verdict] ?? VERDICT_COLOR.NEUTRAL)
      : "#C9A961" // gold: inconclusive
    : "#C9A961"

  return (
    <AnimatePresence>
      {isVisible && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.25 }}
          className="fixed inset-0 z-[100] flex items-center justify-center px-5"
          style={{ background: "rgba(8,9,11,0.94)", backdropFilter: "blur(14px)" }}
          role="status"
          aria-live="polite"
        >
          <div className="w-full max-w-md">
            {/* Terminal frame */}
            <motion.div
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.35, ease: [0.22, 1, 0.36, 1] }}
              className="rounded-xl border border-border bg-[#0C0D10] shadow-pop overflow-hidden"
            >
              {/* Header */}
              <div className="flex items-center gap-2.5 px-5 py-3.5 border-b border-border">
                <span className="w-1.5 h-1.5 rounded-full flex-shrink-0" style={{ background: phase === "scanning" ? "#C9A961" : color }}>
                  <span className="sr-only">running</span>
                </span>
                <span className="font-mono text-[10px] tracking-caps uppercase text-muted truncate">
                  analysis · {company}
                </span>
                <span className="ml-auto font-mono text-[10px] text-muted tabular">
                  {phase === "scanning" ? `${step + 1}/${STEPS.length}` : "done"}
                </span>
              </div>

              <div className="px-5 py-5 min-h-[248px] flex flex-col justify-center">
                <AnimatePresence mode="wait">
                  {phase === "scanning" ? (
                    <motion.div key="log" exit={{ opacity: 0, y: -10 }} transition={{ duration: 0.2 }} className="flex flex-col gap-2.5">
                      {STEPS.map((s, i) => (
                        <motion.div
                          key={s}
                          initial={{ opacity: 0 }}
                          animate={{ opacity: i <= step ? 1 : 0.18 }}
                          transition={{ duration: 0.25 }}
                          className="flex items-baseline gap-3 font-mono text-xs"
                        >
                          <span className="text-muted tabular flex-shrink-0">[{(i * 0.6).toFixed(1)}s]</span>
                          <span className={i <= step ? "text-ink2" : "text-muted"}>{s}</span>
                          <span className="ml-auto flex-shrink-0">
                            {i < step
                              ? <span className="text-gold font-semibold">ok</span>
                              : i === step
                                ? <span className="inline-block w-[7px] h-[13px] bg-gold/80 animate-caret align-middle" aria-hidden="true" />
                                : null}
                          </span>
                        </motion.div>
                      ))}
                    </motion.div>
                  ) : (
                    <motion.div key="stamp" initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex flex-col items-center text-center py-2">
                      <p className="eyebrow mb-6">Verdict</p>
                      <motion.span
                        initial={{ opacity: 0, scale: 1.25 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
                        className="inline-block rounded-lg px-7 py-4 mb-6"
                        style={{ border: `1px solid ${color}70`, outline: `1px solid ${color}25`, outlineOffset: "4px" }}
                      >
                        <span
                          className="font-mono font-bold tabular leading-none"
                          style={{
                            color,
                            fontSize: verdictView.reliable ? "clamp(38px, 9vw, 56px)" : "clamp(20px, 4.5vw, 30px)",
                            letterSpacing: "0.1em",
                          }}
                        >
                          {verdictView.verdict}
                        </span>
                      </motion.span>
                      {verdictView.reliable ? (
                        <p className="font-mono text-xs text-muted">
                          confidence{" "}
                          <span className="text-base font-semibold tabular" style={{ color }}>
                            {confVal.toFixed(0)}%
                          </span>
                        </p>
                      ) : (
                        <p className="font-mono text-[11px] text-muted max-w-[280px] leading-relaxed">
                          Not enough reliable data to reach a verdict
                        </p>
                      )}
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            </motion.div>

            <p className="text-center font-mono text-[10px] text-muted mt-5 tracking-wide">
              Calibrated on 700 Indian IPOs · 2014–24
            </p>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}
