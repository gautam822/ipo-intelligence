import { motion } from "framer-motion"

export default function Panel({ title, children, className = "", action, delay = 0 }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay, duration: 0.4, ease: "easeOut" }}
      className={`bg-surface border border-border rounded-2xl p-5 shadow-card ${className}`}
    >
      {title && (
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-xs font-semibold text-muted uppercase tracking-widest">{title}</h3>
          {action}
        </div>
      )}
      {children}
    </motion.div>
  )
}
