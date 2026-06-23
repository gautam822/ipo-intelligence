import { motion } from "framer-motion"
import { AlertTriangle, AlertCircle } from "lucide-react"

export default function DataBanner({ nFetched, nTotal = 35 }) {
  if (nFetched >= 15) return null
  const pct = Math.min(100, (nFetched / nTotal) * 100)
  const isCrit = nFetched < 8

  return (
    <motion.div
      initial={{ opacity: 0, y: -8 }}
      animate={{ opacity: 1, y: 0 }}
      className={`flex items-start gap-3 rounded-xl px-4 py-3 text-sm mb-4 border ${
        isCrit
          ? "bg-avoid-dim border-avoid-mid text-avoid"
          : "bg-neutral-dim border-neutral-mid text-neutral"
      }`}
    >
      {isCrit ? <AlertCircle size={15} className="mt-0.5 flex-shrink-0" /> : <AlertTriangle size={15} className="mt-0.5 flex-shrink-0" />}
      <div className="flex-1 min-w-0">
        <p className="font-semibold text-xs mb-1">
          {isCrit ? `Only ${nFetched}/${nTotal} signals found` : `Partial data — ${nFetched}/${nTotal} signals`}
        </p>
        <div className="h-1 rounded-full bg-[rgba(255,255,255,0.1)] overflow-hidden">
          <motion.div
            className="h-full rounded-full"
            style={{ background: isCrit ? "#FB7185" : "#FBBF24" }}
            initial={{ width: 0 }}
            animate={{ width: `${pct}%` }}
            transition={{ duration: 0.8, ease: [0.4,0,0.2,1] }}
          />
        </div>
        <p className="text-xs mt-1 opacity-70">
          {isCrit ? "Verdict is mostly historical averages. Check back closer to listing." : "Indicative verdict — treat as a first read."}
        </p>
      </div>
    </motion.div>
  )
}
