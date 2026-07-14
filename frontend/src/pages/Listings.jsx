import { useEffect, useState } from "react"
import { motion } from "framer-motion"
import { TrendingUp, TrendingDown, Minus, Search, ArrowUpRight, BarChart2 } from "lucide-react"
import { useNavigate, Link } from "react-router-dom"
import api from "../lib/api"

const VERDICT_CFG = {
  INVEST:  { Icon: TrendingUp,   color: "#40D993", badge: "badge-invest" },
  NEUTRAL: { Icon: Minus,        color: "#E5B84B", badge: "badge-neutral" },
  AVOID:   { Icon: TrendingDown, color: "#F2657E", badge: "badge-avoid" },
}

function VerdictBadge({ verdict }) {
  const cfg = VERDICT_CFG[verdict]
  if (!cfg) return null
  return (
    <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md font-mono text-[10px] font-semibold tracking-wider ${cfg.badge}`}>
      <cfg.Icon size={10} strokeWidth={2.5} />
      {verdict}
    </span>
  )
}

function ConfidenceBar({ value = 0 }) {
  const color = value >= 70 ? "#40D993" : value >= 50 ? "#E5B84B" : "#F2657E"
  return (
    <div className="flex items-center gap-2.5">
      <div className="flex-1 h-[3px] bg-[rgba(255,255,255,0.06)] rounded-full overflow-hidden">
        <motion.div
          className="h-full rounded-full"
          initial={{ width: 0 }}
          animate={{ width: `${value}%` }}
          transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
          style={{ background: color }}
        />
      </div>
      <span className="font-mono tabular text-xs text-ink2 w-9 text-right">{value?.toFixed(0)}%</span>
    </div>
  )
}

const FILTERS = ["All", "INVEST", "NEUTRAL", "AVOID"]
const FILTER_COLOR = { INVEST: "#40D993", NEUTRAL: "#E5B84B", AVOID: "#F2657E" }
const SORTS = [
  { label: "Newest first",       key: "date",       dir: -1 },
  { label: "Highest confidence", key: "confidence", dir: -1 },
  { label: "Lowest confidence",  key: "confidence", dir:  1 },
]

export default function Listings({ initialRows = null }) {
  const [rows, setRows]       = useState(initialRows ?? [])
  const [loading, setLoading] = useState(initialRows == null)
  const [filter, setFilter]   = useState("All")
  const [sortIdx, setSortIdx] = useState(0)
  const [search, setSearch]   = useState("")
  const navigate = useNavigate()

  useEffect(() => {
    if (initialRows != null) return
    api.history().then((h) => { setRows(h); setLoading(false) }).catch(() => setLoading(false))
  }, [initialRows])

  const sort = SORTS[sortIdx]

  const filtered = rows
    .filter((r) => filter === "All" || r.verdict === filter)
    .filter((r) => !search || r.company?.toLowerCase().includes(search.toLowerCase()))
    .sort((a, b) => {
      if (sort.key === "date") return sort.dir * (new Date(b.created_at) - new Date(a.created_at))
      return sort.dir * ((b.confidence || 0) - (a.confidence || 0))
    })

  const stats = [
    { label: "Analyzed", value: rows.length, color: "#E9E7E2" },
    { label: "Invest",   value: rows.filter((r) => r.verdict === "INVEST").length,  color: "#40D993" },
    { label: "Neutral",  value: rows.filter((r) => r.verdict === "NEUTRAL").length, color: "#E5B84B" },
    { label: "Avoid",    value: rows.filter((r) => r.verdict === "AVOID").length,   color: "#F2657E" },
  ]

  return (
    <div className="pt-[60px]">
      {/* Header */}
      <div className="border-b border-border">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 py-12">
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
            <p className="eyebrow mb-4 flex items-center gap-2">
              <span className="gold-tick" /> IPO database
            </p>
            <h1 className="font-display text-4xl sm:text-[44px] text-ink mb-2.5">
              Every verdict, <em className="italic" style={{ fontWeight: 500 }}>on record</em>
            </h1>
            <p className="text-ink2 text-sm max-w-md">
              Each analysis is logged the moment it&rsquo;s made — verdict, confidence, and
              the 180-day outcome once it lands.
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="grid grid-cols-2 sm:flex gap-y-4 mt-9 max-w-lg"
          >
            {stats.map((s, i) => (
              <div key={s.label} className={`px-5 first:pl-0 sm:flex-1 ${i > 0 ? "sm:border-l sm:border-[rgba(255,255,255,0.08)]" : ""}`}>
                <span className="font-mono font-medium text-xl tabular block" style={{ color: s.color }}>{s.value}</span>
                <span className="font-mono text-[9.5px] tracking-caps uppercase text-muted">{s.label}</span>
              </div>
            ))}
          </motion.div>
        </div>
      </div>

      <div className="max-w-5xl mx-auto px-4 sm:px-6 py-8">
        {/* Controls */}
        <div className="flex flex-col sm:flex-row gap-3 mb-7">
          <div className="relative flex-1">
            <Search size={14} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-muted" />
            <input
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Filter by company…"
              className="w-full pl-9 pr-4 py-2.5 bg-surface border border-border rounded-lg text-sm text-ink placeholder:text-muted focus:outline-none focus:border-gold-mid transition-colors"
            />
          </div>
          <div className="flex items-center gap-1 bg-surface border border-border rounded-lg p-1 overflow-x-auto">
            {FILTERS.map((f) => (
              <button
                key={f}
                onClick={() => setFilter(f)}
                className={`px-3.5 py-1.5 rounded-md font-mono text-[11px] font-medium tracking-wide transition-all whitespace-nowrap ${
                  filter === f ? "bg-surface2 border border-border-strong" : "border border-transparent text-muted hover:text-ink2"
                }`}
                style={filter === f ? { color: FILTER_COLOR[f] ?? "#E9E7E2" } : undefined}
              >
                {f}
              </button>
            ))}
          </div>
          <select
            value={sortIdx}
            onChange={(e) => setSortIdx(Number(e.target.value))}
            className="px-4 py-2.5 bg-surface border border-border rounded-lg text-sm text-ink2 focus:outline-none focus:border-gold-mid appearance-none cursor-pointer hover:text-ink transition-colors"
            aria-label="Sort predictions"
          >
            {SORTS.map((s, i) => <option key={i} value={i} className="bg-[#101114]">{s.label}</option>)}
          </select>
        </div>

        {/* Rows */}
        {loading ? (
          <div className="flex flex-col gap-3">
            {[...Array(6)].map((_, i) => (
              <div key={i} className="h-[76px] rounded-xl border border-border skeleton" />
            ))}
          </div>
        ) : filtered.length === 0 ? (
          <div className="text-center py-24">
            <BarChart2 size={26} className="mx-auto mb-4 text-muted opacity-50" />
            <p className="text-sm text-ink2 mb-1.5">No verdicts match.</p>
            <p className="text-[13px] text-muted">
              Adjust the filters, or{" "}
              <Link to="/" className="text-gold hover:underline underline-offset-4">analyze a new company</Link>.
            </p>
          </div>
        ) : (
          <div className="flex flex-col gap-2.5">
            {filtered.map((r, i) => (
              <motion.button
                key={r.id ?? `${r.company}-${i}`}
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: Math.min(i * 0.03, 0.3), duration: 0.3 }}
                whileHover={{ y: -2 }}
                whileTap={{ scale: 0.995 }}
                onClick={() => navigate(`/?q=${encodeURIComponent(r.company)}`)}
                title={`Re-run analysis for ${r.company}`}
                className="text-left bg-surface border border-border rounded-xl px-5 py-4 hover:border-border-strong hover:bg-surface2 transition-all cursor-pointer group"
              >
                <div className="flex items-center justify-between gap-4 flex-wrap">
                  <div className="flex-1 min-w-[220px]">
                    <div className="flex items-center gap-2.5 flex-wrap mb-2.5">
                      <h3 className="font-medium text-[15px] text-ink truncate">{r.company}</h3>
                      <VerdictBadge verdict={r.verdict} />
                      {r.outcome_alpha != null && (
                        <span
                          className="font-mono text-[10px] font-semibold tabular px-2 py-0.5 rounded-md border"
                          style={
                            r.outcome_alpha >= 0
                              ? { color: "#40D993", background: "rgba(64,217,147,0.09)", borderColor: "rgba(64,217,147,0.28)" }
                              : { color: "#F2657E", background: "rgba(242,101,126,0.09)", borderColor: "rgba(242,101,126,0.28)" }
                          }
                        >
                          {r.outcome_alpha > 0 ? "+" : ""}{r.outcome_alpha.toFixed(1)}% · 180d
                        </span>
                      )}
                    </div>
                    <div className="max-w-[240px]">
                      <ConfidenceBar value={r.confidence} />
                    </div>
                  </div>
                  <div className="flex items-center gap-3 flex-shrink-0">
                    <span className="font-mono text-[10px] text-muted tabular">
                      {r.created_at ? new Date(r.created_at).toLocaleDateString("en-IN", { day: "2-digit", month: "short", year: "numeric" }) : "—"}
                    </span>
                    <ArrowUpRight size={14} className="text-muted opacity-0 group-hover:opacity-100 group-hover:text-gold transition-all" />
                  </div>
                </div>
              </motion.button>
            ))}
          </div>
        )}

        {filtered.length > 0 && (
          <p className="text-center font-mono text-[10px] text-muted mt-8 tracking-wide">
            Showing {filtered.length} of {rows.length} verdicts
          </p>
        )}
      </div>
    </div>
  )
}
