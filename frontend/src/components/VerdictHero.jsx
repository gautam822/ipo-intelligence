import { motion } from "framer-motion"
import { TrendingUp, TrendingDown, Minus, ExternalLink, HelpCircle } from "lucide-react"
import ConfidenceDial from "./ConfidenceDial"
import { assess, INCONCLUSIVE_COPY } from "../lib/reliability"

const CONFIGS = {
  INVEST:  { color: "#40D993", dim: "rgba(64,217,147,0.05)",  border: "rgba(64,217,147,0.22)",  Icon: TrendingUp,   label: "Model signals subscribe" },
  AVOID:   { color: "#F2657E", dim: "rgba(242,101,126,0.05)", border: "rgba(242,101,126,0.22)", Icon: TrendingDown, label: "Model signals avoid" },
  NEUTRAL: { color: "#E5B84B", dim: "rgba(229,184,75,0.05)",  border: "rgba(229,184,75,0.22)",  Icon: Minus,        label: "Model signals wait and watch" },
}

// The verdict, stamped like a certificate: corner registration marks,
// a double-ruled seal, and the machine's mono voice.
export default function VerdictHero({ result }) {
  const { verdict, confidence_pct, company, xgb_probabilities, source_url } = result

  // Reliability gate: if the model didn't gather enough signal, don't fake a verdict.
  const view = assess(result)
  if (!view.reliable) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
        className="corner-ticks relative rounded-xl overflow-hidden p-7 sm:p-9 bg-surface"
        style={{ border: "1px solid rgba(201,169,97,0.3)", "--tick": "rgba(201,169,97,0.5)" }}
      >
        <span className="ct" aria-hidden="true" />
        <div className="relative z-10 flex flex-col sm:flex-row items-start gap-6">
          <div className="w-12 h-12 rounded-xl flex items-center justify-center flex-shrink-0 border border-[rgba(201,169,97,0.3)] bg-[rgba(201,169,97,0.06)]">
            <HelpCircle size={22} className="text-gold" />
          </div>
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2.5 mb-3">
              <span className="eyebrow" style={{ color: "#8B8880" }}>{company}</span>
              <span className="h-px flex-1 max-w-[64px] bg-[rgba(255,255,255,0.12)]" />
              <span className="eyebrow">Inconclusive</span>
            </div>
            <h3 className="font-display text-2xl sm:text-[28px] text-ink mb-2.5">
              {INCONCLUSIVE_COPY.title}
            </h3>
            <p className="text-sm text-ink2 leading-relaxed max-w-lg mb-4">{INCONCLUSIVE_COPY.body}</p>
            {view.nFetched != null && (
              <p className="font-mono text-[10px] tracking-caps uppercase text-muted">
                Only {view.nFetched} of {view.nTotal ?? 35} signals available · need {8}+ to judge
              </p>
            )}
          </div>
        </div>
      </motion.div>
    )
  }

  const cfg = CONFIGS[verdict] ?? CONFIGS.NEUTRAL
  const { color, dim, border, Icon, label } = cfg

  const probs = [
    { key: "INVEST",  val: xgb_probabilities?.invest  ?? 0, c: "#40D993" },
    { key: "NEUTRAL", val: xgb_probabilities?.neutral ?? 0, c: "#E5B84B" },
    { key: "AVOID",   val: xgb_probabilities?.avoid   ?? 0, c: "#F2657E" },
  ]
  const probSum = probs.reduce((a, p) => a + p.val, 0) || 1

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
      className="corner-ticks relative rounded-xl overflow-hidden p-7 sm:p-9 bg-surface"
      style={{ border: `1px solid ${border}`, "--tick": `${color}55` }}
    >
      <span className="ct" aria-hidden="true" />
      {/* Verdict-tinted wash, kept faint */}
      <div className="absolute inset-0 pointer-events-none" style={{ background: dim }} />

      <div className="relative z-10 flex flex-col sm:flex-row items-start sm:items-center gap-7 sm:gap-9">
        <ConfidenceDial pct={confidence_pct} verdict={verdict} size={132} />

        <div className="flex-1 min-w-0 w-full">
          <div className="flex items-center gap-2.5 mb-3">
            <span className="eyebrow" style={{ color: "#8B8880" }}>{company}</span>
            <span className="h-px flex-1 max-w-[64px] bg-[rgba(255,255,255,0.12)]" />
            <span className="eyebrow">Model verdict</span>
            {source_url && (
              <a href={source_url} target="_blank" rel="noreferrer" className="text-muted hover:text-gold transition-colors" aria-label="Source filing">
                <ExternalLink size={11} />
              </a>
            )}
          </div>

          {/* The stamp */}
          <motion.div
            initial={{ opacity: 0, scale: 1.12 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.12, duration: 0.45, ease: [0.22, 1, 0.36, 1] }}
            className="inline-flex items-center gap-4 mb-4"
          >
            <span
              className="inline-flex items-center gap-3 rounded-lg px-5 py-3"
              style={{ border: `1px solid ${color}66`, boxShadow: `inset 0 0 0 3px ${dim}, inset 0 0 0 1px transparent, 0 0 0 4px transparent`, outline: `1px solid ${color}22`, outlineOffset: "3px" }}
            >
              <span
                className="font-mono font-bold tabular leading-none"
                style={{ color, fontSize: "clamp(34px, 6vw, 52px)", letterSpacing: "0.09em" }}
              >
                {verdict}
              </span>
              <Icon size={26} style={{ color }} strokeWidth={2.2} className="flex-shrink-0" />
            </span>
          </motion.div>

          <p className="text-sm text-ink2 mb-6">{label}</p>

          {/* Probability distribution — one instrument bar, three readouts */}
          <div className="max-w-md">
            <div className="flex h-1.5 rounded-full overflow-hidden bg-[rgba(255,255,255,0.05)]">
              {probs.map((p) => (
                <motion.div
                  key={p.key}
                  initial={{ flexGrow: 0 }}
                  animate={{ flexGrow: p.val / probSum }}
                  transition={{ delay: 0.35, duration: 0.8, ease: [0.22, 1, 0.36, 1] }}
                  style={{ background: p.c, flexBasis: 0 }}
                />
              ))}
            </div>
            <div className="flex mt-2.5">
              {probs.map((p, i) => (
                <div key={p.key} className={`flex items-baseline gap-1.5 ${i > 0 ? "pl-4 ml-4 border-l border-[rgba(255,255,255,0.09)]" : ""}`}>
                  <span className="font-mono text-[9px] tracking-caps uppercase text-muted">{p.key}</span>
                  <span className="font-mono text-xs font-semibold tabular" style={{ color: p.c }}>
                    {(p.val * 100).toFixed(0)}%
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  )
}
