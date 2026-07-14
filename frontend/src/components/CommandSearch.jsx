import { useState, useRef, useEffect } from "react"
import { Loader2, ArrowRight } from "lucide-react"
import { motion, AnimatePresence } from "framer-motion"

const SUGGESTIONS = ["Tata Capital", "Swiggy", "PhysicsWallah", "NTPC Green", "Hyundai India"]
const PLACEHOLDERS = [
  "Search any Indian IPO — e.g. Tata Capital",
  "Try Swiggy, Hyundai India…",
  "Type a company name for a verdict",
  "e.g. NTPC Green, PhysicsWallah",
]

export default function CommandSearch({ onSearch, loading, initialQuery = "" }) {
  const [value, setValue]     = useState(initialQuery)
  const [focused, setFocused] = useState(false)
  const [phIdx, setPhIdx]     = useState(0)
  const [isMac, setIsMac]     = useState(true)
  const inputRef              = useRef(null)

  // Keep in sync when a query arrives from elsewhere (e.g. a Listings row)
  useEffect(() => { if (initialQuery) setValue(initialQuery) }, [initialQuery])

  useEffect(() => {
    setIsMac(/Mac|iPhone|iPad/.test(navigator.platform || ""))
  }, [])

  // ⌘K / Ctrl+K focuses the bar; Esc clears focus
  useEffect(() => {
    function onKey(e) {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault()
        inputRef.current?.focus()
        inputRef.current?.select()
      }
      if (e.key === "Escape") inputRef.current?.blur()
    }
    window.addEventListener("keydown", onKey)
    return () => window.removeEventListener("keydown", onKey)
  }, [])

  useEffect(() => {
    if (focused || value) return
    const id = setInterval(() => setPhIdx((i) => (i + 1) % PLACEHOLDERS.length), 3200)
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
            borderColor: focused ? "rgba(201,169,97,0.45)" : "rgba(255,255,255,0.09)",
            boxShadow: focused
              ? "0 0 0 3px rgba(201,169,97,0.10), 0 10px 34px rgba(0,0,0,0.5)"
              : "0 1px 2px rgba(0,0,0,0.5), 0 8px 28px rgba(0,0,0,0.35)",
          }}
          transition={{ duration: 0.2 }}
          className="flex items-center gap-3 rounded-xl pl-5 pr-2.5 py-2.5 bg-[rgba(255,255,255,0.035)] border backdrop-blur-sm"
        >
          {/* Terminal prompt — the machine is listening */}
          <span className="flex-shrink-0 w-5 flex items-center justify-center" aria-hidden="true">
            {loading
              ? <Loader2 size={16} className="text-gold animate-spin" />
              : <span className={`font-mono text-[15px] font-semibold leading-none transition-colors ${focused ? "text-gold" : "text-muted"}`}>›</span>
            }
          </span>

          <div className="flex-1 relative overflow-hidden py-1.5">
            <input
              ref={inputRef}
              value={value}
              onChange={(e) => setValue(e.target.value)}
              onFocus={() => setFocused(true)}
              onBlur={() => setFocused(false)}
              className="relative z-10 w-full bg-transparent outline-none text-ink text-[15px] font-medium placeholder-transparent"
              autoComplete="off"
              spellCheck="false"
              aria-label="Company name"
            />
            <AnimatePresence mode="wait">
              {!value && (
                <motion.span
                  key={phIdx}
                  initial={{ opacity: 0, y: 5 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -5 }}
                  transition={{ duration: 0.22 }}
                  className="absolute inset-0 flex items-center text-[15px] text-muted pointer-events-none"
                >
                  {PLACEHOLDERS[phIdx]}
                </motion.span>
              )}
            </AnimatePresence>
          </div>

          {!value && !loading && (
            <kbd className="hidden sm:flex items-center gap-1 flex-shrink-0 font-mono text-[10px] text-muted border border-border rounded-md px-1.5 py-1 mr-1">
              {isMac ? "⌘" : "Ctrl"} K
            </kbd>
          )}

          <motion.button
            type="submit"
            disabled={loading || !value.trim()}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className="sheen flex items-center gap-2 bg-gold text-bg font-semibold text-[13px] px-[18px] py-2.5 rounded-lg disabled:opacity-35 disabled:cursor-not-allowed flex-shrink-0 transition-opacity hover:brightness-110"
            style={{ paddingLeft: 18, paddingRight: 18 }}
          >
            {loading ? "Analyzing…" : "Analyze"}
            {!loading && <ArrowRight size={13} strokeWidth={2.5} />}
          </motion.button>
        </motion.div>
      </form>

      <AnimatePresence>
        {!loading && (
          <motion.div
            initial={{ opacity: 0, y: -4 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            className="flex items-center gap-x-2 gap-y-1.5 mt-3.5 px-1 flex-wrap justify-center"
          >
            <span className="font-mono text-[10px] tracking-caps uppercase text-muted mr-1">Try</span>
            {SUGGESTIONS.map((s, i) => (
              <motion.button
                key={s}
                type="button"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.25 + i * 0.05 }}
                onClick={() => { setValue(s); inputRef.current?.focus() }}
                className="text-xs text-ink2 border border-border hover:border-gold-mid hover:text-gold px-3 py-1.5 rounded-md transition-all duration-150 font-medium bg-surface hover:bg-gold-dim"
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
