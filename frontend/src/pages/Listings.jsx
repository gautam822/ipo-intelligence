import { useEffect, useState } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { TrendingUp, TrendingDown, Minus, Search, SlidersHorizontal, Calendar, BarChart2 } from "lucide-react"
import { useNavigate } from "react-router-dom"
import api from "../lib/api"

const VERDICT_CFG = {
  INVEST:  { Icon: TrendingUp,   color: "#059669", bg: "#ECFDF5", border: "#6EE7B7", badge: "badge-invest"  },
  NEUTRAL: { Icon: Minus,        color: "#D97706", bg: "#FFFBEB", border: "#FCD34D", badge: "badge-neutral" },
  AVOID:   { Icon: TrendingDown, color: "#DC2626", bg: "#FEF2F2", border: "#FCA5A5", badge: "badge-avoid"   },
}

function VerdictBadge({ verdict }) {
  const cfg = VERDICT_CFG[verdict]
  if (!cfg) return null
  return (
    <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold ${cfg.badge}`}>
      <cfg.Icon size={11} strokeWidth={2.5} />
      {verdict}
    </span>
  )
}

function ConfidenceBar({ value }) {
  const color = value >= 70 ? "#059669" : value >= 50 ? "#D97706" : "#DC2626"
  return (
    <div className="flex items-center gap-2">
      <div className="flex-1 h-1.5 bg-border rounded-full overflow-hidden">
        <motion.div
          className="h-full rounded-full"
          initial={{ width: 0 }}
          animate={{ width: `${value}%` }}
          transition={{ duration: 0.6, ease: "easeOut" }}
          style={{ background: color }}
        />
      </div>
      <span className="tabular text-xs font-semibold text-ink2 w-10 text-right">{value?.toFixed(0)}%</span>
    </div>
  )
}

const FILTERS = ["All", "INVEST", "NEUTRAL", "AVOID"]
const SORTS = [
  { label: "Newest first",    key: "date",       dir: -1 },
  { label: "Highest confidence", key: "confidence", dir: -1 },
  { label: "Lowest confidence",  key: "confidence", dir:  1 },
]

export default function Listings() {
  const [rows, setRows]       = useState([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter]   = useState("All")
  const [sortIdx, setSortIdx] = useState(0)
  const [search, setSearch]   = useState("")
  const navigate = useNavigate()

  useEffect(() => {
    api.history(200).then((h) => { setRows(h); setLoading(false) }).catch(() => setLoading(false))
  }, [])

  const sort = SORTS[sortIdx]

  const filtered = rows
    .filter((r) => filter === "All" || r.verdict === filter)
    .filter((r) => !search || r.company?.toLowerCase().includes(search.toLowerCase()))
    .sort((a, b) => {
      if (sort.key === "date") return sort.dir * (new Date(b.created_at) - new Date(a.created_at))
      return sort.dir * ((b.confidence || 0) - (a.confidence || 0))
    })

  const stats = {
    total:   rows.length,
    invest:  rows.filter((r) => r.verdict === "INVEST").length,
    neutral: rows.filter((r) => r.verdict === "NEUTRAL").length,
    avoid:   rows.filter((r) => r.verdict === "AVOID").length,
  }

  return (
    <div className="min-h-screen bg-bg pt-16">
      {/* Header */}
      <div className="bg-surface border-b border-border">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 py-10">
          <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}>
            <p className="text-xs font-mono tracking-widest text-muted uppercase mb-2">IPO Database</p>
            <h1 className="font-black text-3xl sm:text-4xl text-ink mb-1">All Predictions</h1>
            <p className="text-ink2 text-sm">Every IPO analyzed by our model, with verdicts and confidence scores.</p>
          </motion.div>

          {/* Stat pills */}
          <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}
            className="flex flex-wrap gap-3 mt-6">
            {[
              { label: "Total analyzed", value: stats.total, color: "text-ink" },
              { label: "INVEST",  value: stats.invest,  color: "text-invest"  },
              { label: "NEUTRAL", value: stats.neutral, color: "text-verdict" },
              { label: "AVOID",   value: stats.avoid,   color: "text-avoid"   },
            ].map((s) => (
              <div key={s.label} className="bg-bg border border-border rounded-xl px-4 py-2.5 flex items-center gap-2.5">
                <span className={`tabular font-bold text-xl ${s.color}`}>{s.value}</span>
                <span className="text-xs text-muted font-medium">{s.label}</span>
              </div>
            ))}
          </motion.div>
        </div>
      </div>

      <div className="max-w-5xl mx-auto px-4 sm:px-6 py-6">
        {/* Filters */}
        <div className="flex flex-col sm:flex-row gap-3 mb-6">
          {/* Search */}
          <div className="relative flex-1">
            <Search size={15} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-muted" />
            <input
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search company..."
              className="w-full pl-9 pr-4 py-2.5 bg-surface border border-border rounded-xl text-sm text-ink placeholder:text-muted focus:outline-none focus:border-accent/50 transition-colors"
            />
          </div>
          {/* Verdict filter */}
          <div className="flex items-center gap-1 bg-surface border border-border rounded-xl p-1">
            {FILTERS.map((f) => (
              <button key={f} onClick={() => setFilter(f)}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${filter === f ? "bg-accent text-white shadow-sm" : "text-ink2 hover:bg-bg"}`}>
                {f}
              </button>
            ))}
          </div>
          {/* Sort */}
          <div className="relative">
            <SlidersHorizontal size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-muted pointer-events-none" />
            <select
              value={sortIdx}
              onChange={(e) => setSortIdx(Number(e.target.value))}
              className="pl-8 pr-8 py-2.5 bg-surface border border-border rounded-xl text-sm text-ink focus:outline-none focus:border-accent/50 appearance-none cursor-pointer"
            >
              {SORTS.map((s, i) => <option key={i} value={i}>{s.label}</option>)}
            </select>
          </div>
        </div>

        {/* Table */}
        {loading ? (
          <div className="flex flex-col gap-3">
            {[...Array(6)].map((_, i) => (
              <div key={i} className="h-20 bg-surface rounded-2xl border border-border skeleton" />
            ))}
          </div>
        ) : filtered.length === 0 ? (
          <div className="text-center py-20 text-muted">
            <BarChart2 size={32} className="mx-auto mb-3 opacity-40" />
            <p className="text-sm">No predictions yet. Analyze an IPO to get started.</p>
          </div>
        ) : (
          <div className="flex flex-col gap-3">
            {filtered.map((r, i) => {
              const cfg = VERDICT_CFG[r.verdict]
              return (
                <motion.div
                  key={r.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: i * 0.03, duration: 0.3 }}
                  onClick={() => navigate("/")}
                  className="bg-surface border border-border rounded-2xl p-5 hover:shadow-card hover:border-accent/20 transition-all cursor-pointer group"
                >
                  <div className="flex items-start justify-between gap-4 flex-wrap">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2.5 flex-wrap mb-2">
                        <h3 className="font-semibold text-ink group-hover:text-accent transition-colors truncate">
                          {r.company}
                        </h3>
                        <VerdictBadge verdict={r.verdict} />
                        {r.outcome_alpha != null && (
                          <span className={`text-xs font-semibold tabular px-2 py-0.5 rounded-full ${r.outcome_alpha >= 0 ? "bg-invest-dim text-invest" : "bg-avoid-dim text-avoid"}`}>
                            {r.outcome_alpha > 0 ? "+" : ""}{r.outcome_alpha.toFixed(1)}% outcome
                          </span>
                        )}
                      </div>
                      <div className="max-w-xs">
                        <ConfidenceBar value={r.confidence} />
                      </div>
                    </div>
                    <div className="flex items-center gap-1.5 text-xs text-muted flex-shrink-0">
                      <Calendar size={12} />
                      {r.created_at ? new Date(r.created_at).toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" }) : "—"}
                    </div>
                  </div>
                </motion.div>
              )
            })}
          </div>
        )}

        {filtered.length > 0 && (
          <p className="text-center text-xs text-muted mt-6">
            Showing {filtered.length} of {rows.length} predictions
          </p>
        )}
      </div>
    </div>
  )
}
