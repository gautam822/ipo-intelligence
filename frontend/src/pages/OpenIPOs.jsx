import { useState } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { useNavigate } from "react-router-dom"
import { Search, ChevronDown, TrendingUp, TrendingDown, ArrowUpRight, CircleDot, CheckCircle2, Clock } from "lucide-react"
import { OPEN_IPOS, IPO_UPDATED } from "../lib/openIpoData"
import AnimatedNumber from "../components/AnimatedNumber"

const STATUS = {
  open:   { label: "Open now",   color: "#40D993", Icon: CircleDot,     badge: "badge-invest" },
  closed: { label: "Closed",     color: "#E5B84B", Icon: Clock,         badge: "badge-neutral" },
  listed: { label: "Listed",     color: "#66635C", Icon: CheckCircle2,  badge: "" },
}

const ALLOT = {
  awaited: { label: "Allotment awaited", color: "#E5B84B" },
  out:     { label: "Allotment out",     color: "#40D993" },
}

function fmtDate(iso) {
  try { return new Date(iso).toLocaleDateString("en-IN", { day: "2-digit", month: "short" }) }
  catch { return iso }
}
function daysLeft(iso) { return Math.ceil((new Date(iso) - new Date()) / 86400000) }

function SubRow({ label, x }) {
  if (x == null) return (
    <div className="flex items-center justify-between text-[12px]">
      <span className="text-ink2">{label}</span>
      <span className="font-mono text-muted text-[11px]">—</span>
    </div>
  )
  const color = x >= 3 ? "#40D993" : x >= 1 ? "#E5B84B" : "#F2657E"
  return (
    <div className="flex items-center justify-between text-[12px]">
      <span className="text-ink2">{label}</span>
      <span className="font-mono tabular font-semibold" style={{ color }}>{x.toFixed(2)}×</span>
    </div>
  )
}

function IPOCard({ ipo, i, expanded, onToggle }) {
  const navigate = useNavigate()
  const s = STATUS[ipo.status]
  const al = ipo.allotment ? ALLOT[ipo.allotment] : null
  const dl = daysLeft(ipo.close)
  const gmpPos = ipo.gmpPct >= 0
  const closingSoon = ipo.status === "open" && dl >= 0 && dl <= 1

  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: Math.min(i * 0.04, 0.3), duration: 0.3 }}
      whileHover={{ y: -2 }}
      className="bg-surface border border-border rounded-xl overflow-hidden hover:border-border-strong transition-colors"
    >
      <button onClick={onToggle} className="w-full text-left px-5 py-4">
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2.5 flex-wrap mb-1.5">
              <span className={`inline-flex items-center gap-1.5 px-2 py-0.5 rounded-md font-mono text-[9.5px] font-semibold tracking-wider ${s.badge}`}
                    style={s.badge ? undefined : { color: s.color, background: "rgba(255,255,255,0.05)" }}>
                <s.Icon size={9} strokeWidth={2.5} />
                {s.label}
              </span>
              {al && (
                <span className="font-mono text-[9.5px] font-semibold tracking-wider" style={{ color: al.color }}>
                  {al.label.toUpperCase()}
                </span>
              )}
              {closingSoon && (
                <motion.span
                  className="font-mono text-[9.5px] font-semibold tracking-wider text-avoid"
                  animate={{ opacity: [1, 0.4, 1] }}
                  transition={{ duration: 1.6, repeat: Infinity, ease: "easeInOut" }}
                >
                  {dl === 0 ? "CLOSES TODAY" : "LAST DAY"}
                </motion.span>
              )}
            </div>
            <h3 className="font-medium text-[15px] text-ink leading-snug">{ipo.company}</h3>
            <p className="font-mono text-[10px] text-muted mt-1.5 tracking-wide uppercase">
              {ipo.type} · {ipo.priceBand}
            </p>
          </div>
          <div className="flex items-center gap-3 flex-shrink-0">
            <div className="text-right">
              <div className="flex items-center gap-1 justify-end">
                {gmpPos ? <TrendingUp size={12} style={{ color: "#40D993" }} strokeWidth={2.5} />
                        : <TrendingDown size={12} style={{ color: "#F2657E" }} strokeWidth={2.5} />}
                <AnimatedNumber value={`${gmpPos ? "+" : ""}${(ipo.gmpPct * 100).toFixed(1)}%`}
                  className="font-mono tabular text-[13px] font-semibold"
                  style={{ color: gmpPos ? "#40D993" : "#F2657E" }} />
              </div>
              <span className="font-mono text-[8.5px] tracking-caps uppercase text-muted">GMP</span>
            </div>
            <ChevronDown size={16} className={`text-muted transition-transform ${expanded ? "rotate-180" : ""}`} />
          </div>
        </div>

        <div className="flex items-center gap-x-5 gap-y-1.5 flex-wrap mt-3.5 pt-3.5 border-t border-[rgba(255,255,255,0.05)]">
          <Meta label="Window" value={`${fmtDate(ipo.open)} – ${fmtDate(ipo.close)}`} />
          <Meta label="Listing" value={fmtDate(ipo.listing)} />
          <Meta label="Issue size" value={ipo.issueSize} />
          {ipo.lotSize && <Meta label="Lot" value={`${ipo.lotSize} sh`} />}
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
              {ipo.note && <p className="text-[13px] text-ink2 leading-relaxed">{ipo.note}</p>}

              <div className="rounded-lg border border-border bg-[rgba(255,255,255,0.02)] p-4">
                <p className="eyebrow mb-3">Subscription by category</p>
                <div className="flex flex-col gap-2">
                  <SubRow label="QIB" x={ipo.subscription.qib} />
                  <SubRow label="NII / HNI" x={ipo.subscription.nii} />
                  <SubRow label="Retail" x={ipo.subscription.retail} />
                </div>
                {ipo.subscription.qib == null && (
                  <p className="font-mono text-[9.5px] text-muted mt-3">Figures appear once bidding is underway.</p>
                )}
              </div>

              {/* Allotment status block */}
              <div className="rounded-lg p-4 border" style={{
                borderColor: al ? `${al.color}25` : "rgba(255,255,255,0.07)",
                background: al ? `${al.color}0d` : "rgba(255,255,255,0.02)",
              }}>
                <p className="eyebrow mb-1.5" style={al ? { color: al.color } : undefined}>Allotment status</p>
                <p className="text-[13px] text-ink2 leading-relaxed">
                  {ipo.status === "open"
                    ? "Bidding is still open — allotment runs after the issue closes."
                    : ipo.allotment === "awaited"
                    ? "Issue closed. Allotment is being finalised; check your registrar/broker for status."
                    : "Allotment is out — check your application status with the registrar or your broker."}
                </p>
              </div>

              <button
                onClick={(e) => { e.stopPropagation(); navigate(`/?q=${encodeURIComponent(ipo.company)}`) }}
                className="self-start inline-flex items-center gap-2 px-4 py-2 rounded-lg text-[13px] font-semibold bg-gold text-bg sheen hover:brightness-110 transition-all"
              >
                Run AI analysis <ArrowUpRight size={13} strokeWidth={2.5} />
              </button>
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

const FILTERS = [
  { key: "all",    label: "All" },
  { key: "open",   label: "Open now" },
  { key: "closed", label: "Awaiting allotment" },
  { key: "listed", label: "Listed" },
]

export default function OpenIPOs() {
  const [filter, setFilter] = useState("all")
  const [search, setSearch] = useState("")
  const [openId, setOpenId] = useState(null)

  const counts = {
    open:   OPEN_IPOS.filter((x) => x.status === "open").length,
    closed: OPEN_IPOS.filter((x) => x.status === "closed").length,
    listed: OPEN_IPOS.filter((x) => x.status === "listed").length,
  }

  const list = OPEN_IPOS
    .filter((x) => filter === "all" || x.status === filter)
    .filter((x) => !search || x.company.toLowerCase().includes(search.toLowerCase()))
    .sort((a, b) => new Date(a.close) - new Date(b.close))

  return (
    <div className="pt-[60px]">
      <div className="border-b border-border">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 py-12">
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
            <p className="eyebrow mb-4 flex items-center gap-2">
              <span className="gold-tick" /> Live market
            </p>
            <h1 className="font-display text-4xl sm:text-[44px] text-ink mb-2.5">
              IPOs open <em className="italic" style={{ fontWeight: 500 }}>right now</em>
            </h1>
            <p className="text-ink2 text-sm leading-relaxed max-w-xl">
              Current mainboard issues with grey-market premium, category subscription, and
              allotment status — then run any of them through the model in one click.
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}
            className="grid grid-cols-3 gap-y-4 mt-9 max-w-md"
          >
            <Stat value={counts.open} label="Open now" color="#40D993" />
            <Stat value={counts.closed} label="Awaiting allotment" color="#E5B84B" />
            <Stat value={counts.listed} label="Recently listed" color="#E9E7E2" />
          </motion.div>
        </div>
      </div>

      <div className="max-w-5xl mx-auto px-4 sm:px-6 py-8">
        <div className="flex flex-col sm:flex-row gap-3 mb-7">
          <div className="relative flex-1">
            <Search size={14} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-muted" />
            <input
              value={search} onChange={(e) => setSearch(e.target.value)}
              placeholder="Filter by company…"
              className="w-full pl-9 pr-4 py-2.5 bg-surface border border-border rounded-lg text-sm text-ink placeholder:text-muted focus:outline-none focus:border-gold-mid transition-colors"
            />
          </div>
          <div className="flex items-center gap-1 bg-surface border border-border rounded-lg p-1 overflow-x-auto">
            {FILTERS.map((f) => (
              <button key={f.key} onClick={() => setFilter(f.key)}
                className={`px-3.5 py-1.5 rounded-md font-mono text-[11px] font-medium tracking-wide transition-all whitespace-nowrap ${
                  filter === f.key ? "bg-surface2 border border-border-strong text-ink" : "border border-transparent text-muted hover:text-ink2"
                }`}>
                {f.label}
              </button>
            ))}
          </div>
        </div>

        {list.length === 0 ? (
          <div className="text-center py-20">
            <CircleDot size={24} className="mx-auto mb-3 text-muted opacity-50" />
            <p className="text-sm text-ink2">No IPOs match that filter.</p>
          </div>
        ) : (
          <div className="flex flex-col gap-2.5">
            {list.map((ipo, i) => (
              <IPOCard key={ipo.id} ipo={ipo} i={i}
                expanded={openId === ipo.id}
                onToggle={() => setOpenId(openId === ipo.id ? null : ipo.id)} />
            ))}
          </div>
        )}

        <div className="mt-8 rounded-xl border border-neutral-mid bg-neutral-dim p-4 flex gap-3" style={{ borderLeftWidth: 2 }}>
          <TrendingUp size={14} className="text-neutral flex-shrink-0 mt-0.5" />
          <p className="text-[12px] text-ink2 leading-relaxed">
            GMP is an unofficial grey-market figure, not a guarantee of listing gains — never invest on GMP alone.
            Allotment status must be confirmed with the official registrar or your broker. Snapshot data, updated {fmtDate(IPO_UPDATED)}.
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
