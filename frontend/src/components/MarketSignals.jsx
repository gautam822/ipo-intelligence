import { motion } from "framer-motion"
import { TrendingUp, TrendingDown, Users } from "lucide-react"
import AnimatedNumber from "./AnimatedNumber"

// Reads result.market_signals = { gmp_pct?, qib_subscription?, hni_subscription?, retail_subscription? }
// gmp_pct is a fraction (0.12 = +12%); subscription values are "times" (e.g. 2.4 = 2.4x).

const CATS = [
  { key: "qib_subscription",    label: "QIB",    hint: "Qualified institutional" },
  { key: "hni_subscription",    label: "NII/HNI", hint: "Non-institutional" },
  { key: "retail_subscription", label: "Retail", hint: "Retail individual" },
]

function subColor(x) {
  if (x >= 3) return "#40D993"
  if (x >= 1) return "#E5B84B"
  return "#F2657E"
}

export default function MarketSignals({ result }) {
  const ms = result?.market_signals || {}
  const gmp = ms.gmp_pct
  const subs = CATS.filter((c) => ms[c.key] != null)
  const hasGmp = gmp != null
  if (!hasGmp && subs.length === 0) return null

  // scale bars against the max subscription (min 5x for headroom)
  const maxSub = Math.max(5, ...subs.map((c) => ms[c.key] || 0))
  const gmpPos = (gmp ?? 0) >= 0

  return (
    <div className="flex flex-col gap-5">
      {hasGmp && (
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            {gmpPos ? (
              <TrendingUp size={15} style={{ color: "#40D993" }} strokeWidth={2.5} />
            ) : (
              <TrendingDown size={15} style={{ color: "#F2657E" }} strokeWidth={2.5} />
            )}
            <div>
              <p className="text-[13px] text-ink font-medium leading-none">Grey market premium</p>
              <p className="font-mono text-[9.5px] tracking-caps uppercase text-muted mt-1">Unofficial · indicative</p>
            </div>
          </div>
          <AnimatedNumber
            value={`${gmpPos ? "+" : ""}${(gmp * 100).toFixed(1)}%`}
            className="font-mono font-semibold text-xl tabular"
            style={{ color: gmpPos ? "#40D993" : "#F2657E" }}
          />
        </div>
      )}

      {hasGmp && subs.length > 0 && <div className="rule" />}

      {subs.length > 0 && (
        <div>
          <div className="flex items-center gap-2 mb-3.5">
            <Users size={13} className="text-ink2" />
            <p className="text-[13px] text-ink font-medium">Subscription by investor category</p>
          </div>
          <div className="flex flex-col gap-3">
            {subs.map((c, i) => {
              const x = ms[c.key]
              const color = subColor(x)
              const pct = Math.min((x / maxSub) * 100, 100)
              return (
                <div key={c.key}>
                  <div className="flex items-baseline justify-between mb-1.5">
                    <span className="text-[12px] text-ink2">
                      {c.label}
                      <span className="text-muted font-mono text-[9.5px] ml-2 tracking-wide">{c.hint}</span>
                    </span>
                    <span className="font-mono tabular text-[13px] font-semibold" style={{ color }}>
                      {x.toFixed(2)}×
                    </span>
                  </div>
                  <div className="h-[3px] rounded-full bg-[rgba(255,255,255,0.06)] overflow-hidden">
                    <motion.div
                      className="h-full rounded-full"
                      initial={{ width: 0 }}
                      whileInView={{ width: `${pct}%` }}
                      viewport={{ once: true }}
                      transition={{ duration: 0.7, delay: i * 0.08, ease: [0.22, 1, 0.36, 1] }}
                      style={{ background: color }}
                    />
                  </div>
                </div>
              )
            })}
          </div>
          <p className="font-mono text-[9.5px] text-muted mt-3.5 leading-relaxed">
            &ldquo;×&rdquo; = times subscribed. Above 1× means fully subscribed; higher signals stronger demand.
            Live figures move until the issue closes.
          </p>
        </div>
      )}
    </div>
  )
}
