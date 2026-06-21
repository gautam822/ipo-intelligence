import { motion } from "framer-motion"
import { TrendingUp, TrendingDown, Minus } from "lucide-react"
import ConfidenceDial from "./ConfidenceDial"

const CONFIGS = {
  INVEST:  { Icon: TrendingUp,   color: "#059669", bg: "#ECFDF5", border: "#6EE7B7", badge: "badge-invest"  },
  NEUTRAL: { Icon: Minus,        color: "#D97706", bg: "#FFFBEB", border: "#FCD34D", badge: "badge-neutral" },
  AVOID:   { Icon: TrendingDown, color: "#DC2626", bg: "#FEF2F2", border: "#FCA5A5", badge: "badge-avoid"   },
}

export default function VerdictHero({ result }) {
  const cfg = CONFIGS[result.verdict] || CONFIGS.NEUTRAL
  const proba = result.xgb_probabilities || {}

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, ease: "easeOut" }}
      className="relative overflow-hidden bg-surface border border-border rounded-2xl p-6 sm:p-8 flex items-center gap-8 flex-wrap shadow-card"
    >
      {/* Ambient background */}
      <div
        className="absolute inset-0 pointer-events-none"
        style={{
          background: `radial-gradient(ellipse at 90% 20%, ${cfg.bg}, transparent 60%)`,
        }}
      />

      <ConfidenceDial confidence={result.confidence_pct} verdict={result.verdict} size={140} />

      <div className="flex-1 min-w-[200px] relative z-10">
        {/* Company */}
        <p className="text-xs font-mono tracking-widest text-muted uppercase mb-2">
          {result.company}
        </p>

        {/* Verdict */}
        <div className="flex items-center gap-3 mb-4">
          <div
            className="w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0"
            style={{ background: cfg.bg, border: `1.5px solid ${cfg.border}` }}
          >
            <cfg.Icon size={20} style={{ color: cfg.color }} strokeWidth={2.5} />
          </div>
          <h2
            className="font-black text-4xl sm:text-5xl tracking-tight"
            style={{ color: cfg.color }}
          >
            {result.verdict}
          </h2>
        </div>

        {/* Probability breakdown */}
        <div className="flex gap-6">
          {[
            ["AVOID",   proba.avoid,   "#DC2626"],
            ["NEUTRAL", proba.neutral, "#D97706"],
            ["INVEST",  proba.invest,  "#059669"],
          ].map(([label, val, c]) => (
            <div key={label}>
              <p className="tabular font-bold text-base" style={{ color: c }}>
                {((val || 0) * 100).toFixed(0)}%
              </p>
              <p className="font-mono text-[9px] tracking-widest uppercase text-muted">{label}</p>
            </div>
          ))}
        </div>
      </div>
    </motion.div>
  )
}
