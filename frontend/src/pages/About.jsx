import { motion } from "framer-motion"
import Panel from "../components/Panel"
import { Database, Brain, RefreshCw, FileText, AlertCircle } from "lucide-react"

const STEPS = [
  {
    icon: Database, color: "#2563EB",
    title: "Data ingestion",
    body: "Scrapes SEBI DRHPs, NSE subscription data, and grey market premium trackers in real time. Extracts 35 signals spanning financials, valuation, issue structure, governance, and demand.",
  },
  {
    icon: Brain, color: "#059669",
    title: "Calibrated prediction",
    body: "A gradient-boosted model (XGBoost) trained on 700 historical Indian IPOs with time-based train/test splits, isotonic-calibrated so a '78% confidence' call is actually right ~78% of the time historically.",
  },
  {
    icon: RefreshCw, color: "#D97706",
    title: "Reinforcement learning overlay",
    body: "A policy agent, warm-started from the supervised model, adjusts confidence based on realised 180-day outcomes vs Nifty. Wrong, confident calls are penalised twice as hard — the system gets more cautious exactly where it should.",
  },
  {
    icon: FileText, color: "#7C3AED",
    title: "Explainable output",
    body: "Every verdict ships with SHAP-attributed drivers, a plain-language explanation, red flags, and the nearest historical comparable IPO — so the reasoning is inspectable, not a black box.",
  },
]

const PERFORMANCE = [
  { label: "Invest-call precision", value: "0.625" },
  { label: "Portfolio alpha (180d)", value: "+21.1%" },
  { label: "Hit rate on INVEST calls", value: "80%" },
  { label: "RL vs XGBoost reward", value: "+12.8%" },
  { label: "Training dataset", value: "700 IPOs" },
  { label: "Test period", value: "2023–24" },
]

export default function About() {
  return (
    <div className="min-h-screen bg-bg pt-16">
      {/* Header */}
      <div className="bg-surface border-b border-border">
        <div className="max-w-3xl mx-auto px-4 sm:px-6 py-10">
          <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}>
            <p className="text-xs font-mono tracking-widest text-muted uppercase mb-2">Methodology</p>
            <h1 className="font-black text-3xl sm:text-4xl text-ink mb-1">How it works</h1>
            <p className="text-ink2 text-sm leading-relaxed max-w-xl">
              IPO Intelligence chains four systems together to turn a company name into an analyst-grade verdict.
            </p>
          </motion.div>
        </div>
      </div>

      <div className="max-w-3xl mx-auto px-4 sm:px-6 py-8 flex flex-col gap-5">
        {/* Architecture steps */}
        {STEPS.map((s, i) => (
          <motion.div key={s.title} initial={{ opacity: 0, y: 14 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: i * 0.08, duration: 0.4 }}
            className="bg-surface border border-border rounded-2xl p-6 shadow-card hover:shadow-card-hover transition-shadow">
            <div className="flex gap-4">
              <div className="w-11 h-11 rounded-xl flex items-center justify-center flex-shrink-0"
                style={{ background: `${s.color}15`, border: `1.5px solid ${s.color}30` }}>
                <s.icon size={18} style={{ color: s.color }} />
              </div>
              <div>
                <div className="flex items-center gap-2 mb-1.5">
                  <span className="text-xs font-mono text-muted">0{i + 1}</span>
                  <h3 className="font-bold text-ink text-[15px]">{s.title}</h3>
                </div>
                <p className="text-sm text-ink2 leading-relaxed">{s.body}</p>
              </div>
            </div>
          </motion.div>
        ))}

        {/* Performance grid */}
        <motion.div initial={{ opacity: 0, y: 12 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: 0.1 }}
          className="bg-surface border border-border rounded-2xl p-6 shadow-card">
          <h3 className="text-xs font-semibold text-muted uppercase tracking-widest mb-5">Model performance (held-out 2023–24 test set)</h3>
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
            {PERFORMANCE.map((p, i) => (
              <div key={i} className="bg-bg rounded-xl border border-border p-4">
                <p className="tabular font-black text-xl text-ink mb-1">{p.value}</p>
                <p className="text-xs text-muted leading-snug">{p.label}</p>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Limitations */}
        <motion.div initial={{ opacity: 0, y: 12 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: 0.15 }}
          className="bg-verdict-dim border border-amber-200 rounded-2xl p-6">
          <div className="flex items-center gap-2 mb-4">
            <AlertCircle size={16} className="text-amber-600 flex-shrink-0" />
            <h3 className="font-semibold text-amber-800 text-sm">Honest limitations</h3>
          </div>
          <ul className="text-sm text-amber-800/80 space-y-2.5">
            {[
              "Confidence reflects historical calibration, not a guarantee — markets remain unpredictable.",
              "India sees ~60–80 mainboard IPOs per year, so the RL feedback loop learns slowly; multi-horizon rewards (Day 1/30/180) help offset this.",
              "When fewer than 8 of 35 signals are available (common before subscription opens), the system says so explicitly rather than guessing confidently.",
              "This is informational only. Not investment advice and should not be the sole basis for any financial decision.",
            ].map((l, i) => (
              <li key={i} className="flex gap-2.5">
                <span className="w-1 h-1 rounded-full bg-amber-600 mt-2 flex-shrink-0" />
                {l}
              </li>
            ))}
          </ul>
        </motion.div>
      </div>
    </div>
  )
}
