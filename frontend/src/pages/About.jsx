import { motion } from "framer-motion"
import { Link } from "react-router-dom"
import { Database, Brain, RefreshCw, FileText, AlertTriangle, ArrowRight } from "lucide-react"

const STEPS = [
  {
    n: "01", icon: Database,
    title: "Data ingestion",
    body: "Scrapes SEBI DRHPs, NSE subscription data, and grey-market premium trackers in real time. Extracts 35 signals spanning financials, valuation, issue structure, governance, and demand.",
  },
  {
    n: "02", icon: Brain,
    title: "Calibrated prediction",
    body: "A gradient-boosted model (XGBoost) trained on 700 Indian IPOs with strictly time-based splits, isotonic-calibrated so a \u201C78% confidence\u201D call has actually been right about 78% of the time.",
  },
  {
    n: "03", icon: RefreshCw,
    title: "Reinforcement learning overlay",
    body: "A policy agent, warm-started from the supervised model, adjusts confidence using realised 180-day outcomes vs Nifty. Confident wrong calls are penalised twice as hard — the system grows cautious exactly where it should.",
  },
  {
    n: "04", icon: FileText,
    title: "Explainable output",
    body: "Every verdict ships with SHAP-attributed drivers, a plain-language explanation, red flags, and the nearest historical comparable — the reasoning is inspectable, never a black box.",
  },
]

const PERFORMANCE = [
  { label: "Invest-call precision",     value: "0.625" },
  { label: "Portfolio alpha · 180d",    value: "+21.1%" },
  { label: "Hit rate on invest calls",  value: "80%" },
  { label: "RL uplift vs XGBoost",      value: "+12.8%" },
  { label: "Training dataset",          value: "700 IPOs" },
  { label: "Held-out test period",      value: "2023–24" },
]

const LIMITS = [
  "Confidence reflects historical calibration, not a guarantee — markets remain unpredictable.",
  "India lists roughly 60–80 mainboard IPOs a year, so the RL feedback loop learns slowly; multi-horizon rewards (day 1 / 30 / 180) help offset this.",
  "When fewer than 8 of 35 signals are available — common before subscription opens — the system says so explicitly rather than guessing confidently.",
  "This is informational only: not investment advice, and never the sole basis for a financial decision.",
]

export default function About() {
  return (
    <div className="pt-[60px]">
      {/* Header */}
      <div className="border-b border-border">
        <div className="max-w-3xl mx-auto px-4 sm:px-6 py-12">
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
            <p className="eyebrow mb-4 flex items-center gap-2">
              <span className="gold-tick" /> Methodology
            </p>
            <h1 className="font-display text-4xl sm:text-[44px] text-ink mb-2.5">
              How the verdict is <em className="italic" style={{ fontWeight: 500 }}>made</em>
            </h1>
            <p className="text-ink2 text-sm leading-relaxed max-w-xl">
              Four systems in sequence turn a company name into an analyst-grade
              call. Each one is inspectable.
            </p>
          </motion.div>
        </div>
      </div>

      <div className="max-w-3xl mx-auto px-4 sm:px-6 py-10 flex flex-col gap-10">
        {/* Pipeline */}
        <div className="relative">
          {/* Spine */}
          <div className="absolute left-[15px] top-6 bottom-6 w-px bg-[rgba(255,255,255,0.08)] hidden sm:block" aria-hidden="true" />
          <div className="flex flex-col gap-8">
            {STEPS.map((s, i) => (
              <motion.div
                key={s.n}
                initial={{ opacity: 0, y: 12 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.06, duration: 0.4 }}
                className="relative flex gap-5 sm:gap-7"
              >
                <div className="relative z-10 w-8 h-8 rounded-lg flex-shrink-0 flex items-center justify-center bg-bg border border-border-strong">
                  <span className="font-mono text-[10px] font-semibold text-gold tabular">{s.n}</span>
                </div>
                <div className="flex-1 pb-1">
                  <div className="flex items-center gap-2.5 mb-2">
                    <s.icon size={14} className="text-ink2 flex-shrink-0" />
                    <h3 className="font-semibold text-ink text-[15px]">{s.title}</h3>
                  </div>
                  <p className="text-sm text-ink2 leading-relaxed">{s.body}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>

        {/* Performance */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="rounded-xl border border-border bg-surface p-6"
        >
          <p className="eyebrow mb-6 flex items-center gap-2">
            <span className="gold-tick" /> Model performance · held-out 2023–24 test set
          </p>
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
            {PERFORMANCE.map((p) => (
              <div key={p.label} className="rounded-lg border border-border bg-[rgba(255,255,255,0.02)] py-4 px-4">
                <p className="font-mono font-medium tabular text-xl text-ink mb-1">{p.value}</p>
                <p className="font-mono text-[9px] tracking-caps uppercase text-muted leading-relaxed">{p.label}</p>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Honest limitations */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="rounded-xl border border-neutral-mid bg-neutral-dim p-6"
          style={{ borderLeftWidth: 2 }}
        >
          <div className="flex items-center gap-2.5 mb-5">
            <AlertTriangle size={14} className="text-neutral flex-shrink-0" />
            <h3 className="font-mono text-[10px] font-medium tracking-caps uppercase text-neutral">Honest limitations</h3>
          </div>
          <ul className="space-y-3.5">
            {LIMITS.map((l, i) => (
              <li key={i} className="flex gap-3 text-sm text-ink2 leading-relaxed">
                <span className="font-mono text-[10px] text-neutral/80 mt-[3px] flex-shrink-0 tabular">{String(i + 1).padStart(2, "0")}</span>
                {l}
              </li>
            ))}
          </ul>
        </motion.div>

        {/* Close the loop */}
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          className="text-center pb-4"
        >
          <Link
            to="/"
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-lg text-[13px] font-semibold bg-gold text-bg hover:brightness-110 transition-all"
          >
            Analyze an IPO <ArrowRight size={13} strokeWidth={2.5} />
          </Link>
        </motion.div>
      </div>
    </div>
  )
}
