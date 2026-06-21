import { useEffect, useState } from "react"
import { motion } from "framer-motion"
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, ResponsiveContainer, Cell, Tooltip } from "recharts"
import { TrendingUp, TrendingDown, Minus, Activity } from "lucide-react"
import Panel from "../components/Panel"
import api from "../lib/api"

const VC = { INVEST: "#059669", AVOID: "#DC2626", NEUTRAL: "#D97706" }
const VC_DIM = { INVEST: "#ECFDF5", AVOID: "#FEF2F2", NEUTRAL: "#FFFBEB" }
const VC_ICON = { INVEST: TrendingUp, AVOID: TrendingDown, NEUTRAL: Minus }

function StatCard({ label, value, color, delay = 0 }) {
  return (
    <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay, duration: 0.4 }}
      className="bg-surface border border-border rounded-2xl p-5 shadow-card">
      <p className="tabular font-black text-3xl mb-1" style={{ color }}>{value ?? "—"}</p>
      <p className="text-xs text-muted font-medium">{label}</p>
    </motion.div>
  )
}

export default function TrackRecord() {
  const [metrics, setMetrics] = useState(null)
  const [history, setHistory] = useState([])

  useEffect(() => {
    api.metrics().then(setMetrics).catch(() => {})
    api.history(100).then(setHistory).catch(() => {})
  }, [])

  const chartData = history.slice(0, 20).reverse().map((h) => ({
    name: h.company?.length > 12 ? h.company.slice(0, 11) + "…" : h.company,
    confidence: h.confidence,
    verdict: h.verdict,
  }))

  return (
    <div className="min-h-screen bg-bg pt-16">
      {/* Header */}
      <div className="bg-surface border-b border-border">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 py-10">
          <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}>
            <p className="text-xs font-mono tracking-widest text-muted uppercase mb-2">Performance</p>
            <h1 className="font-black text-3xl sm:text-4xl text-ink mb-1">Track Record</h1>
            <p className="text-ink2 text-sm">Model performance on the held-out test set and live predictions.</p>
          </motion.div>
        </div>
      </div>

      <div className="max-w-5xl mx-auto px-4 sm:px-6 py-8 flex flex-col gap-6">
        {/* Model stats */}
        {metrics && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <StatCard label="Invest-call precision" value={metrics.model.invest_precision?.toFixed(2)} color="#2563EB" delay={0.05} />
            <StatCard label="Portfolio alpha (180d)" value={`+${(metrics.model.portfolio_alpha_180d * 100).toFixed(1)}%`} color="#059669" delay={0.1} />
            <StatCard label="Hit rate on INVEST calls" value={`${(metrics.model.hit_rate * 100).toFixed(0)}%`} color="#059669" delay={0.15} />
            <StatCard label="RL improvement vs XGBoost" value={`+${metrics.rl.rl_improvement_pct?.toFixed(1)}%`} color="#D97706" delay={0.2} />
          </div>
        )}

        {/* Live stats */}
        {metrics?.live && (
          <Panel title="Live prediction distribution" delay={0.25}>
            <div className="flex flex-wrap gap-6">
              <div>
                <p className="tabular font-bold text-2xl text-ink">{metrics.live.total_predictions}</p>
                <p className="text-xs text-muted mt-0.5">total predictions</p>
              </div>
              {Object.entries(metrics.live.by_verdict || {}).map(([v, c]) => {
                const Icon = VC_ICON[v]
                return (
                  <div key={v} className="flex items-center gap-2">
                    <div className="w-8 h-8 rounded-lg flex items-center justify-center" style={{ background: VC_DIM[v] }}>
                      {Icon && <Icon size={14} style={{ color: VC[v] }} strokeWidth={2.5} />}
                    </div>
                    <div>
                      <p className="tabular font-bold text-lg" style={{ color: VC[v] }}>{c}</p>
                      <p className="text-[10px] text-muted font-mono uppercase tracking-wide">{v}</p>
                    </div>
                  </div>
                )
              })}
            </div>
          </Panel>
        )}

        {/* Chart */}
        {chartData.length > 0 && (
          <Panel title="Recent confidence scores" delay={0.3}>
            <ResponsiveContainer width="100%" height={260}>
              <BarChart data={chartData} margin={{ top: 6, right: 6, left: -20, bottom: 44 }}>
                <CartesianGrid stroke="#E2E8F0" vertical={false} />
                <XAxis dataKey="name" angle={-35} textAnchor="end" height={60}
                  tick={{ fill: "#94A3B8", fontSize: 10, fontFamily: "JetBrains Mono" }} />
                <YAxis tick={{ fill: "#94A3B8", fontSize: 10, fontFamily: "JetBrains Mono" }} domain={[0, 100]} />
                <Tooltip
                  contentStyle={{ background: "#fff", border: "1px solid #E2E8F0", borderRadius: 10, fontFamily: "Inter", fontSize: 12, boxShadow: "0 4px 12px rgba(0,0,0,0.08)" }}
                  cursor={{ fill: "rgba(37,99,235,0.05)" }}
                />
                <Bar dataKey="confidence" radius={[6, 6, 0, 0]}>
                  {chartData.map((d, i) => <Cell key={i} fill={VC[d.verdict] || "#94A3B8"} />)}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </Panel>
        )}

        {/* History table */}
        <Panel title="All predictions" delay={0.35}>
          {history.length === 0 ? (
            <div className="text-center py-10 text-muted">
              <Activity size={28} className="mx-auto mb-3 opacity-30" />
              <p className="text-sm">No predictions yet — search a company to get started.</p>
            </div>
          ) : (
            <div className="overflow-x-auto -mx-1">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-border">
                    {["Company", "Verdict", "Confidence", "Coverage", "Date"].map((h) => (
                      <th key={h} className="text-left text-xs font-semibold text-muted pb-3 pr-4 whitespace-nowrap font-mono tracking-widest uppercase">{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-border">
                  {history.map((h, i) => (
                    <motion.tr key={h.id} initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: i * 0.02 }}
                      className="hover:bg-surface2 transition-colors">
                      <td className="py-3 pr-4 font-medium text-ink truncate max-w-[160px]">{h.company}</td>
                      <td className="py-3 pr-4">
                        <span className="inline-flex items-center gap-1 text-xs font-bold" style={{ color: VC[h.verdict] }}>
                          {h.verdict}
                        </span>
                      </td>
                      <td className="py-3 pr-4 tabular text-ink2">{h.confidence?.toFixed(1)}%</td>
                      <td className="py-3 pr-4 tabular text-muted font-mono text-xs">{h.n_features}/35</td>
                      <td className="py-3 text-muted font-mono text-xs whitespace-nowrap">
                        {h.created_at ? new Date(h.created_at).toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" }) : "—"}
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
