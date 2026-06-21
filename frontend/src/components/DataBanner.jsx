import { AlertTriangle, AlertCircle } from "lucide-react"
import { motion } from "framer-motion"

export default function DataBanner({ nFetched, nTotal = 35 }) {
  if (nFetched >= 15) return null
  const critical = nFetched < 8

  return (
    <motion.div
      initial={{ opacity: 0, y: -8 }}
      animate={{ opacity: 1, y: 0 }}
      className={`flex items-start gap-3 rounded-xl border px-4 py-3.5 text-sm ${
        critical
          ? "bg-avoid-dim border-red-200 text-avoid"
          : "bg-verdict-dim border-amber-200 text-amber-700"
      }`}
    >
      {critical
        ? <AlertCircle size={16} className="mt-0.5 flex-shrink-0" />
        : <AlertTriangle size={16} className="mt-0.5 flex-shrink-0" />
      }
      <div>
        <span className="font-semibold">
          {critical ? "Insufficient data" : "Partial data"} — {nFetched}/{nTotal} signals found
        </span>
        <p className="text-current/70 text-xs mt-0.5 leading-relaxed">
          {critical
            ? "Verdict is unreliable — mostly defaults, not real company data. Check back once subscription opens."
            : "Treat as an early signal only — not a final call."}
        </p>
      </div>
    </motion.div>
  )
}
