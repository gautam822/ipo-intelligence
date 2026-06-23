import { motion } from "framer-motion"
import { TrendingUp, TrendingDown, Minus, ExternalLink } from "lucide-react"
import ConfidenceDial from "./ConfidenceDial"

const CONFIGS = {
  INVEST:  { color: "#34D399", dim: "rgba(52,211,153,0.08)",  glow: "rgba(52,211,153,0.4)",  border: "rgba(52,211,153,0.2)",  Icon: TrendingUp,   label: "Strong buy signal" },
  AVOID:   { color: "#FB7185", dim: "rgba(251,113,133,0.08)", glow: "rgba(251,113,133,0.4)", border: "rgba(251,113,133,0.2)", Icon: TrendingDown, label: "Avoid this IPO" },
  NEUTRAL: { color: "#FBBF24", dim: "rgba(251,191,36,0.08)",  glow: "rgba(251,191,36,0.4)",  border: "rgba(251,191,36,0.2)",  Icon: Minus,        label: "Wait and watch" },
}

export default function VerdictHero({ result }) {
  const { verdict, confidence_pct, company, xgb_probabilities, source_url } = result
  const cfg = CONFIGS[verdict] ?? CONFIGS.NEUTRAL
  const { color, dim, glow, border, Icon, label } = cfg

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.97 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5, ease: [0.4, 0, 0.2, 1] }}
      className="relative rounded-2xl overflow-hidden p-8"
      style={{ background: dim, border: `1px solid ${border}` }}
    >
      {/* Glow blob */}
      <div
        className="absolute right-0 top-0 w-64 h-64 rounded-full pointer-events-none"
        style={{ background: `radial-gradient(circle, ${glow} 0%, transparent 70%)`, opacity: 0.3, transform: "translate(30%, -30%)" }}
      />
      {/* Top shimmer */}
      <div className="absolute top-0 left-0 right-0 h-px" style={{ background: `linear-gradient(90deg, transparent, ${color}40, transparent)` }} />

      <div className="relative z-10 flex flex-col sm:flex-row items-start sm:items-center gap-6">
        {/* Dial */}
        <div className="flex-shrink-0">
          <ConfidenceDial pct={confidence_pct} verdict={verdict} size={120} />
        </div>

        {/* Main */}
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-2">
            <span className="text-[10px] font-mono font-semibold tracking-[0.12em] uppercase text-muted">{company}</span>
            {source_url && (
              <a href={source_url} target="_blank" rel="noreferrer" className="text-muted hover:text-accent transition-colors">
                <ExternalLink size={10} />
              </a>
            )}
          </div>

          <motion.div
            initial={{ opacity: 0, y: 12, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            transition={{ delay: 0.15, duration: 0.5, type: "spring", stiffness: 200 }}
            className="flex items-center gap-3 mb-4"
          >
            <span
              className="font-display font-black text-5xl sm:text-6xl tracking-tight leading-none"
              style={{ color, textShadow: `0 0 40px ${glow}, 0 0 80px ${glow}40` }}
            >
              {verdict}
            </span>
            <div
              className="w-10 h-10 rounded-2xl flex items-center justify-center flex-shrink-0"
              style={{ background: `${color}18`, border: `1px solid ${color}30` }}
            >
              <Icon size={20} style={{ color }} />
            </div>
          </motion.div>

          <p className="text-sm text-ink2 mb-4 font-medium">{label}</p>

          {/* Probability pills */}
          <div className="flex flex-wrap gap-2">
            {[
              { label: "INVEST",  val: xgb_probabilities?.invest,  color: "#34D399" },
              { label: "NEUTRAL", val: xgb_probabilities?.neutral, color: "#FBBF24" },
              { label: "AVOID",   val: xgb_probabilities?.avoid,   color: "#FB7185" },
            ].map(({ label: l, val, color: c }) => (
              <div
                key={l}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-mono font-semibold"
                style={{ background: `${c}12`, border: `1px solid ${c}25`, color: c }}
              >
                <span className="opacity-70">{l}</span>
                <span>{((val ?? 0) * 100).toFixed(0)}%</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </motion.div>
  )
}
