import { useState, useRef, useEffect } from "react"
import { Search, Loader2, ArrowRight } from "lucide-react"
import { motion, AnimatePresence } from "framer-motion"

const SUGGESTIONS = ["Tata Capital", "Swiggy", "PhysicsWallah", "NTPC Green", "Hyundai India"]
const PLACEHOLDERS = [
  "Search any IPO — e.g. Tata Capital…",
  "Try Swiggy, Hyundai India…",
  "Type a company name to get a verdict…",
  "e.g. NTPC Green, PhysicsWallah…",
]

export default function CommandSearch({ onSearch, loading }) {
  const [value, setValue]     = useState("")
  const [focused, setFocused] = useState(false)
  const [phIdx, setPhIdx]     = useState(0)
  const inputRef              = useRef(null)

  useEffect(() => {
    if (focused || value) return
    const id = setInterval(() => setPhIdx(i => (i + 1) % PLACEHOLDERS.length), 3000)
    return () => clearInterval(id)
  }, [focused, value])

  function submit(e) {
    e.preventDefault()
    if (value.trim() && !loading) onSearch(value.trim())
  }

  return (
    <div className="w-full max-w-2xl mx-auto">
      <form onSubmit={submit}>
        <motion.div
          animate={{
            boxShadow: focused
              ? "0 0 0 1px rgba(129,140,248,0.5), 0 0 60px rgba(129,140,248,0.12), 0 8px 32px rgba(0,0,0,0.4)"
              : "0 1px 3px rgba(0,0,0,0.4), 0 4px 16px rgba(0,0,0,0.3)",
          }}
          transition={{ duration: 0.25 }}
          className={`flex items-center gap-3 rounded-2xl px-5 py-4 transition-colors duration-200 ${
            focused
              ? "bg-[rgba(255,255,255,0.06)] border border-[rgba(129,140,248,0.35)]"
              : "bg-[rgba(255,255,255,0.04)] border border-[rgba(255,255,255,0.08)]"
          }`}
        >
          <div className="flex-shrink-0">
            {loading
              ? <Loader2 size={20} className="text-accent animate-spin" />
              : <Search size={20} className={`transition-colors ${focused ? "text-accent" : "text-muted"}`} />
            }
          </div>

          <div className="flex-1 relative overflow-hidden">
            <input
              ref={inputRef}
              value={value}
              onChange={e => setValue(e.target.value)}
              onFocus={() => setFocused(true)}
              onBlur={() => setFocused(false)}
              className="relative z-10 w-full bg-transparent outline-none text-ink text-[15px] font-medium"
              autoComplete="off"
            />
            <AnimatePresence mode="wait">
              {!value && (
                <motion.span
                  key={phIdx}
                  initial={{ opacity: 0, y: 6 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -6 }}
                  transition={{ duration: 0.25 }}
                  className="absolute inset-0 flex items-center text-[15px] font-medium text-muted pointer-events-none"
                >
                  {PLACEHOLDERS[phIdx]}
                </motion.span>
              )}
            </AnimatePresence>
          </div>

          <motion.button
            type="submit"
            disabled={loading || !value.trim()}
            whileHover={{ scale: 1.03 }}
            whileTap={{ scale: 0.97 }}
            className="flex items-center gap-2 bg-accent text-bg font-bold text-sm px-5 py-2.5 rounded-xl disabled:opacity-40 disabled:cursor-not-allowed flex-shrink-0"
            style={{ boxShadow: value.trim() ? "0 4px 24px rgba(129,140,248,0.5)" : "none" }}
          >
            {loading ? "Analyzing…" : "Analyze"}
            {!loading && <ArrowRight size={14} />}
          </motion.button>
        </motion.div>
      </form>

      <AnimatePresence>
        {!loading && (
          <motion.div
            initial={{ opacity: 0, y: -4 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            className="flex items-center gap-2 mt-3 px-1 flex-wrap"
          >
            <span className="text-xs text-muted font-medium">Try:</span>
            {SUGGESTIONS.map((s, i) => (
              <motion.button
                key={s}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: i * 0.05 }}
                onClick={() => { setValue(s); inputRef.current?.focus() }}
                className="text-xs text-ink2 bg-surface border border-border hover:border-accent/40 hover:text-accent hover:bg-accent-dim px-3 py-1.5 rounded-lg transition-all duration-150 font-medium"
              >
                {s}
              </motion.button>
            ))}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}
