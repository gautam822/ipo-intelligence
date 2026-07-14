import { motion } from "framer-motion"
import { AlertTriangle, AlertCircle } from "lucide-react"

// Signal coverage as an instrument strip: one cell per signal,
// lit cells = fetched. Honest about how much the model actually saw.
export default function DataBanner({ nFetched, nTotal = 35 }) {
  if (nFetched >= 15) return null
  const isCrit = nFetched < 8
  const c = isCrit ? "#F2657E" : "#E5B84B"

  return (
    <motion.div
      initial={{ opacity: 0, y: -6 }}
      animate={{ opacity: 1, y: 0 }}
      className="rounded-xl px-5 py-4 border bg-surface"
      style={{ borderColor: `${c}40` }}
    >
      <div className="flex items-center gap-2.5 mb-3">
        {isCrit
          ? <AlertCircle size={13} style={{ color: c }} className="flex-shrink-0" />
          : <AlertTriangle size={13} style={{ color: c }} className="flex-shrink-0" />}
        <p className="font-mono text-[10px] tracking-caps uppercase" style={{ color: c }}>
          Signal coverage — {nFetched}/{nTotal}
        </p>
      </div>

      <div className="flex gap-[3px] mb-2.5" role="img" aria-label={`${nFetched} of ${nTotal} signals found`}>
        {Array.from({ length: nTotal }, (_, i) => (
          <motion.span
            key={i}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.15 + i * 0.012 }}
            className="h-3 flex-1 rounded-[1px]"
            style={{ background: i < nFetched ? c : "rgba(255,255,255,0.06)" }}
          />
        ))}
      </div>

      <p className="text-xs text-ink2">
        {isCrit
          ? "Too few signals for a reliable read — this verdict leans on historical averages. Check back closer to listing."
          : "Partial data. Treat this verdict as a first read, not a final call."}
      </p>
    </motion.div>
  )
}
