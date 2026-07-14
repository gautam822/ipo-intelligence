import { useEffect, useState } from "react"
import { motion } from "framer-motion"
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, ResponsiveContainer, Cell, Tooltip } from "recharts"
import { TrendingUp, TrendingDown, Minus, Activity } from "lucide-react"
import Panel from "../components/Panel"
import AnimatedNumber from "../components/AnimatedNumber"
import api from "../lib/api"

const VC      = { INVEST: "#40D993", AVOID: "#F2657E", NEUTRAL: "#E5B84B" }
const VC_DIM  = { INVEST: "rgba(64,217,147,0.09)", AVOID: "rgba(242,101,126,0.09)", NEUTRAL: "rgba(229,184,75,0.09)" }
const VC_ICON = { INVEST: TrendingUp, AVOID: TrendingDown, NEUTRAL: Minus }

function StatCard({ label, value, color = "#E9E7E2", delay = 0 }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay, duration: 0.4 }}
      className="bg-surface border border-border rounded-xl p-5"
    >
      {value == null
        ? <p className="font-mono font-medium tabular text-[26px] mb-1.5" style={{ color }}>—</p>
        : <AnimatedNumber value={value} className="font-mono font-medium tabular text-[26px] mb-1.5 block" style={{ color }} />}
      <p className="font-mono text-[9.5px] tracking-caps uppercase text-muted leading-relaxed">{label}</p>
    </motion.div>
  )
}

export default function TrackRecord({ initialMetrics = null, initialHistory = null }) {
  const [metrics, setMetrics] = useState(initialMetrics)
  const [history, setHistory] = useState(initialHistory ?? [])

  useEffect(() => {
    if (initialMetrics == null) api.metrics().then(setMetrics).catch(() => {})
    if (initialHistory == null) api.history().then(setHistory).catch(() => {})
  }, [initialMetrics, initialHistory])

  const chartData = history.slice(0, 20).reverse().map((h) => ({
    name: h.company?.length > 12 ? h.company.slice(0, 11) + "…" : h.company,
    confidence: h.confidence,
    verdict: h.verdict,
  }))

  return (
    <div className="pt-[60px]">
      {/* Header */}
      <div className="border-b border-border">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 py-12">
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
            <p className="eyebrow mb-4 flex items-center gap-2">
              <span className="gold-tick" /> Performance
            </p>
            <h1 className="font-display text-4xl sm:text-[44px] text-ink mb-2.5">
              The <em className="italic" style={{ fontWeight: 500 }}>track record</em>
            </h1>
            <p className="text-ink2 text-sm max-w-md">
              Held-out 2023–24 test-set numbers, plus every live prediction the
              system has made since.
            </p>
          </motion.div>
        </div>
      </div>

      <div className="max-w-5xl mx-auto px-4 sm:px-6 py-8 flex flex-col gap-5">
        {metrics && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <StatCard label="Invest-call precision"   value={metrics.model.invest_precision?.toFixed(2)}                    delay={0.05} />
            <StatCard label="Portfolio alpha · 180d"  value={`+${(metrics.model.portfolio_alpha_180d * 100).toFixed(1)}%`}  color="#40D993" delay={0.1} />
            <StatCard label="Hit rate on invest calls" value={`${(metrics.model.hit_rate * 100).toFixed(0)}%`}              color="#40D993" delay={0.15} />
            <StatCard label="RL uplift vs XGBoost"    value={`+${metrics.rl.rl_improvement_pct?.toFixed(1)}%`}              color="#E5B84B" delay={0.2} />
          </div>
        )}

        {metrics?.live && (
          <Panel title="Live prediction distribution" delay={0.25}>
            <div className="flex flex-wrap gap-x-10 gap-y-5 items-center">
              <div>
                <p className="font-mono font-medium tabular text-2xl text-ink">{metrics.live.total_predictions}</p>
                <p className="font-mono text-[9.5px] tracking-caps uppercase text-muted mt-1">Total verdicts</p>
              </div>
              <div className="h-9 w-px bg-[rgba(255,255,255,0.08)] hidden sm:block" />
              {Object.entries(metrics.live.by_verdict || {}).map(([v, c]) => {
                const Icon = VC_ICON[v]
                return (
                  <div key={v} className="flex items-center gap-3">
                    <span className="w-8 h-8 rounded-lg flex items-center justify-center border" style={{ background: VC_DIM[v], borderColor: `${VC[v]}30` }}>
                      {Icon && <Icon size={13} style={{ color: VC[v] }} strokeWidth={2.5} />}
                    </span>
                    <div>
                      <p className="font-mono font-medium tabular text-lg leading-none" style={{ color: VC[v] }}>{c}</p>
                      <p className="font-mono text-[9px] tracking-caps uppercase text-muted mt-1">{v}</p>
                    </div>
                  </div>
                )
              })}
            </div>
          </Panel>
        )}

        {chartData.length > 0 && (
          <Panel title="Recent confidence scores" delay={0.3}>
            <ResponsiveContainer width="100%" height={260}>
              <BarChart data={chartData} margin={{ top: 6, right: 6, left: -16, bottom: 44 }}>
                <CartesianGrid stroke="rgba(255,255,255,0.06)" vertical={false} />
                <XAxis
                  dataKey="name" angle={-35} textAnchor="end" height={60}
                  tick={{ fill: "#66635C", fontSize: 10, fontFamily: "JetBrains Mono" }}
                  axisLine={{ stroke: "rgba(255,255,255,0.10)" }} tickLine={false}
                />
                <YAxis
                  tick={{ fill: "#66635C", fontSize: 10, fontFamily: "JetBrains Mono" }}
                  domain={[0, 100]} axisLine={false} tickLine={false}
                />
                <Tooltip
                  contentStyle={{
                    background: "#101114",
                    border: "1px solid rgba(255,255,255,0.12)",
                    borderRadius: 10,
                    fontFamily: "Inter",
                    fontSize: 12,
                    color: "#E9E7E2",
                    boxShadow: "0 12px 40px rgba(0,0,0,0.55)",
                  }}
                  labelStyle={{ color: "#E9E7E2", fontWeight: 600, marginBottom: 4 }}
                  itemStyle={{ color: "#A3A099" }}
                  cursor={{ fill: "rgba(255,255,255,0.04)" }}
                />
                <Bar dataKey="confidence" radius={[3, 3, 0, 0]} maxBarSize={26}>
                  {chartData.map((d, i) => <Cell key={i} fill={VC[d.verdict] || "#66635C"} fillOpacity={0.85} />)}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </Panel>
        )}

        <Panel title="All predictions" delay={0.35}>
          {history.length === 0 ? (
            <div className="text-center py-12">
              <Activity size={24} className="mx-auto mb-3 text-muted opacity-50" />
              <p className="text-sm text-ink2">No predictions yet — analyze a company to start the record.</p>
            </div>
          ) : (
            <div className="overflow-x-auto -mx-1">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-border">
                    {["Company", "Verdict", "Confidence", "Coverage", "Date"].map((h) => (
                      <th key={h} className="text-left font-mono text-[9.5px] font-medium text-muted pb-3 pr-4 whitespace-nowrap tracking-caps uppercase">
                        {h}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-[rgba(255,255,255,0.05)]">
                  {history.map((h, i) => (
                    <motion.tr
                      key={h.id ?? i}
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ delay: Math.min(i * 0.02, 0.3) }}
                      className="hover:bg-surface transition-colors"
                    >
                      <td className="py-3 pr-4 font-medium text-ink truncate max-w-[180px]">{h.company}</td>
                      <td className="py-3 pr-4">
                        <span className="inline-flex items-center gap-1.5 font-mono text-[11px] font-semibold tracking-wider" style={{ color: VC[h.verdict] }}>
                          <span className="w-1 h-1 rounded-full" style={{ background: VC[h.verdict] }} />
                          {h.verdict}
                        </span>
                      </td>
                      <td className="py-3 pr-4 font-mono tabular text-ink2 text-[13px]">{h.confidence?.toFixed(1)}%</td>
                      <td className="py-3 pr-4 font-mono tabular text-muted text-xs">{h.n_features}/35</td>
                      <td className="py-3 font-mono text-muted text-xs whitespace-nowrap tabular">
                        {h.created_at ? new Date(h.created_at).toLocaleDateString("en-IN", { day: "2-digit", month: "short", year: "numeric" }) : "—"}
                      </td>
                    </motion.tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </Panel>
      </div>
    </div>
  )
}
