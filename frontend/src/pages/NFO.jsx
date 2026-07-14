import { useMemo, useState } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { Search, AlertTriangle, ChevronDown, Layers, ShieldQuestion } from "lucide-react"
import { NFOS, NFO_UPDATED } from "../lib/nfoData"
import AnimatedNumber from "../components/AnimatedNumber"

// verdict presentation
const V = {
  redundant: {
    label: "Existing equivalent",
    color: "#F2657E",
    badge: "badge-avoid",
    tip: "An established fund already gives this exact exposure — usually cheaper and with a track record.",
  },
  neutral: {
    label: "Timing neutral",
    color: "#E5B84B",
    badge: "badge-neutral",
    tip: "NFO timing is roughly neutral here — compare terms against existing funds.",
  },
  novel: {
    label: "Genuinely new",
    color: "#40D993",
    badge: "badge-invest",
    tip: "Strategy isn't otherwise on the shelf. Not automatically good — you're betting on an unproven fund, so judge the thesis and manager.",
  },
}

const FILTERS = [
  { key: "all",       label: "All" },
  { key: "redundant", label: "Has equivalent" },
  { key: "novel",     label: "Genuinely new" },
  { key: "neutral",   label: "Timing neutral" },
]

const RISK_COLOR = {
  "Very High": "#F2657E",
  "High":      "#E5B84B",
  "Moderate":  "#40D993",
}

function fmtDate(iso) {
  try {
    return new Date(iso).toLocaleDateString("en-IN", { day: "2-digit", month: "short" })
  } catch { return iso }
}

function fmtMin(n) {
  if (n >= 100000) return `₹${(n / 100000).toFixed(n % 100000 ? 1 : 0)}L`
  if (n >= 1000) return `₹${(n / 1000).toFixed(n % 1000 ? 1 : 0)}k`
  return `₹${n}`
}

function daysLeft(iso) {
  const ms = new Date(iso) - new Date()
  return Math.ceil(ms / 86400000)
}

function NFOCard({ nfo, i, expanded, onToggle }) {
  const v = V[nfo.verdict]
  const dl = daysLeft(nfo.close)
  const closing = dl >= 0 && dl <= 3

  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: Math.min(i * 0.03, 0.3), duration: 0.3 }}
      whileHover={{ y: -2 }}
      className="bg-surface border border-border rounded-xl overflow-hidden hover:border-border-strong transition-colors"
    >
      <button onClick={onToggle} className="w-full text-left px-5 py-4">
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2.5 flex-wrap mb-1.5">
              <span className={`inline-flex items-center px-2 py-0.5 rounded-md font-mono text-[9.5px] font-semibold tracking-wider ${v.badge}`}>
                {v.label}
              </span>
              {closing && (
                <motion.span
                  className="font-mono text-[9.5px] font-semibold tracking-wider text-avoid"
                  animate={{ opacity: [1, 0.4, 1] }}
                  transition={{ duration: 1.6, repeat: Infinity, ease: "easeInOut" }}
                >
                  {dl === 0 ? "CLOSES TODAY" : `${dl}D LEFT`}
                </motion.span>
              )}
            </div>
            <h3 className="font-medium text-[15px] text-ink leading-snug pr-2">{nfo.name}</h3>
            <p className="font-mono text-[10px] text-muted mt-1.5 tracking-wide uppercase">
              {nfo.amc} · {nfo.category}
            </p>
          </div>
          <ChevronDown
            size={16}
            className={`text-muted flex-shrink-0 mt-1 transition-transform ${expanded ? "rotate-180" : ""}`}
          />
        </div>

        {/* meta strip */}
        <div className="flex items-center gap-x-5 gap-y-1.5 flex-wrap mt-3.5 pt-3.5 border-t border-[rgba(255,255,255,0.05)]">
          <Meta label="Window" value={`${fmtDate(nfo.open)} – ${fmtDate(nfo.close)}`} />
          <Meta label="Min" value={fmtMin(nfo.minInvest)} />
          <Meta label="Style" value={nfo.structure} />
          <div className="flex flex-col">
            <span className="font-mono text-[8.5px] tracking-caps uppercase text-muted mb-0.5">Risk</span>
            <span className="font-mono text-[11px] tabular" style={{ color: RISK_COLOR[nfo.risk] || "#A3A099" }}>
              {nfo.risk}
            </span>
          </div>
        </div>
      </button>

      <AnimatePresence initial={false}>
        {expanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.25, ease: [0.22, 1, 0.36, 1] }}
            className="overflow-hidden"
          >
            <div className="px-5 pb-5 pt-1 flex flex-col gap-4">
              <div>
                <p className="eyebrow mb-1.5">What it is</p>
                <p className="text-[13px] text-ink2 leading-relaxed">{nfo.thesis}</p>
              </div>
              <div className="rounded-lg p-3.5 border" style={{ borderColor: `${v.color}25`, background: `${v.color}0d` }}>
                <p className="font-mono text-[9.5px] tracking-caps uppercase mb-1.5" style={{ color: v.color }}>
                  Is the NFO worth it?
                </p>
                <p className="text-[13px] text-ink2 leading-relaxed">{nfo.equivalent}</p>
              </div>
              {nfo.exitLoad && nfo.exitLoad !== "Check SID" && (
                <p className="font-mono text-[10px] text-muted">Exit load · {nfo.exitLoad}</p>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  )
}

function Meta({ label, value }) {
  return (
    <div className="flex flex-col">
      <span className="font-mono text-[8.5px] tracking-caps uppercase text-muted mb-0.5">{label}</span>
      <span className="font-mono text-[11px] tabular text-ink2">{value}</span>
    </div>
  )
}

export default function NFO() {
  const [filter, setFilter] = useState("all")
  const [search, setSearch] = useState("")
  const [openId, setOpenId] = useState(null)

  const counts = useMemo(() => ({
    total: NFOS.length,
    redundant: NFOS.filter((n) => n.verdict === "redundant").length,
    novel: NFOS.filter((n) => n.verdict === "novel").length,
  }), [])

  const list = NFOS
    .filter((n) => filter === "all" || n.verdict === filter)
    .filter((n) => !search || `${n.name} ${n.amc} ${n.category}`.toLowerCase().includes(search.toLowerCase()))
    .sort((a, b) => new Date(a.close) - new Date(b.close))

  return (
    <div className="pt-[60px]">
      {/* Header */}
      <div className="border-b border-border">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 py-12">
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
            <p className="eyebrow mb-4 flex items-center gap-2">
              <span className="gold-tick" /> New fund offers
            </p>
            <h1 className="font-display text-4xl sm:text-[44px] text-ink mb-2.5">
              Which NFOs are <em className="italic" style={{ fontWeight: 500 }}>actually worth it?</em>
            </h1>
            <p className="text-ink2 text-sm leading-relaxed max-w-xl">
              Unlike an IPO, an NFO has no listing gain and no scarcity — a ₹10 NAV isn&rsquo;t
              &ldquo;cheap.&rdquo; The only real question is whether an established fund already
              gives you the same exposure, cheaper. We flag exactly that.
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="grid grid-cols-3 gap-y-4 mt-9 max-w-md"
          >
            <Stat value={counts.total} label="Open now" color="#E9E7E2" />
            <Stat value={counts.redundant} label="Has equivalent" color="#F2657E" />
            <Stat value={counts.novel} label="Genuinely new" color="#40D993" />
          </motion.div>
        </div>
      </div>

      <div className="max-w-5xl mx-auto px-4 sm:px-6 py-8">
        {/* How to read this */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.15 }}
          className="rounded-xl border border-border bg-surface p-4 mb-7 flex gap-3"
        >
          <ShieldQuestion size={15} className="text-gold flex-shrink-0 mt-0.5" />
          <p className="text-[12.5px] text-ink2 leading-relaxed">
            <span className="text-ink font-medium">How to read this:</span> a{" "}
            <span style={{ color: "#F2657E" }}>&ldquo;has equivalent&rdquo;</span> flag means an existing
            fund tracks the same thing with a real record — usually the smarter buy.{" "}
            <span style={{ color: "#40D993" }}>&ldquo;Genuinely new&rdquo;</span> means the strategy is
            hard to get elsewhere, so it&rsquo;s worth a look — but new means unproven, not good.
          </p>
        </motion.div>

        {/* Controls */}
        <div className="flex flex-col sm:flex-row gap-3 mb-7">
          <div className="relative flex-1">
            <Search size={14} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-muted" />
            <input
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Filter by fund or AMC…"
              className="w-full pl-9 pr-4 py-2.5 bg-surface border border-border rounded-lg text-sm text-ink placeholder:text-muted focus:outline-none focus:border-gold-mid transition-colors"
            />
          </div>
          <div className="flex items-center gap-1 bg-surface border border-border rounded-lg p-1 overflow-x-auto">
            {FILTERS.map((f) => (
              <button
                key={f.key}
                onClick={() => setFilter(f.key)}
                className={`px-3.5 py-1.5 rounded-md font-mono text-[11px] font-medium tracking-wide transition-all whitespace-nowrap ${
                  filter === f.key ? "bg-surface2 border border-border-strong text-ink" : "border border-transparent text-muted hover:text-ink2"
                }`}
              >
                {f.label}
              </button>
            ))}
          </div>
        </div>

        {/* List */}
        {list.length === 0 ? (
          <div className="text-center py-20">
            <Layers size={24} className="mx-auto mb-3 text-muted opacity-50" />
            <p className="text-sm text-ink2">No NFOs match that filter.</p>
          </div>
        ) : (
          <div className="flex flex-col gap-2.5">
            {list.map((nfo, i) => (
              <NFOCard
                key={nfo.id}
                nfo={nfo}
                i={i}
                expanded={openId === nfo.id}
                onToggle={() => setOpenId(openId === nfo.id ? null : nfo.id)}
              />
            ))}
          </div>
        )}

        {/* Disclaimer */}
        <div className="mt-8 rounded-xl border border-neutral-mid bg-neutral-dim p-4 flex gap-3" style={{ borderLeftWidth: 2 }}>
          <AlertTriangle size={14} className="text-neutral flex-shrink-0 mt-0.5" />
          <p className="text-[12px] text-ink2 leading-relaxed">
            Educational analysis, not investment advice. NFO categorisation reflects publicly available
            information and may change — always confirm against the Scheme Information Document. An NFO
            being &ldquo;genuinely new&rdquo; is not a recommendation to buy. Data updated {fmtDate(NFO_UPDATED)}.
          </p>
        </div>
      </div>
    </div>
  )
}

function Stat({ value, label, color }) {
  return (
    <div>
      <AnimatedNumber value={value} className="font-mono font-medium text-xl tabular block" style={{ color }} />
      <span className="font-mono text-[9.5px] tracking-caps uppercase text-muted">{label}</span>
    </div>
  )
}
