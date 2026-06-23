import { motion } from "framer-motion"

export default function Panel({ title, children, className = "", delay = 0 }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay, duration: 0.5, ease: [0.4, 0, 0.2, 1] }}
      className={`relative rounded-2xl bg-[rgba(255,255,255,0.03)] border border-[rgba(255,255,255,0.08)] p-5 overflow-hidden transition-all duration-300 hover:bg-[rgba(255,255,255,0.05)] hover:border-[rgba(255,255,255,0.12)] ${className}`}
    >
      {/* Top shimmer line */}
      <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-[rgba(255,255,255,0.1)] to-transparent" />

      {title && (
        <p className="text-[10px] font-semibold tracking-[0.12em] uppercase text-muted mb-4 flex items-center gap-2">
          <span className="w-1 h-1 rounded-full bg-accent inline-block" />
          {title}
        </p>
      )}
      {children}
    </motion.div>
  )
}
