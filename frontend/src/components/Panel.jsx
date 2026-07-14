import { motion } from "framer-motion"

// A section of the report: hairline frame, gold-ticked mono eyebrow.
export default function Panel({ title, children, className = "", delay = 0 }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 14 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay, duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
      className={`relative rounded-xl bg-surface border border-border p-5 sm:p-6 overflow-hidden transition-colors duration-300 hover:border-border-strong ${className}`}
    >
      {title && (
        <p className="eyebrow mb-5 flex items-center gap-2">
          <span className="gold-tick" />
          {title}
        </p>
      )}
      {children}
    </motion.div>
  )
}
