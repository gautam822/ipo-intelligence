import { useState, useRef } from "react"
import { Search, Loader2, ArrowRight } from "lucide-react"
import { motion } from "framer-motion"

export default function CommandSearch({ onSearch, loading }) {
  const [value, setValue] = useState("")
  const [focused, setFocused] = useState(false)
  const inputRef = useRef(null)

  function submit(e) {
    e.preventDefault()
    if (value.trim() && !loading) onSearch(value.trim())
  }

  const suggestions = ["Tata Capital", "Swiggy", "PhysicsWallah", "NTPC Green", "Hyundai India"]

  return (
    <div className="w-full max-w-2xl mx-auto">
      <form onSubmit={submit} className="relative">
        <motion.div
          animate={{
            boxShadow: focused
              ? "0 2px 8px rgba(0,0,0,0.07)"
              : "0 1px 3px rgba(0,0,0,0.05)",
          }}
          transition={{ duration: 0.2 }}
          className={`flex items-center gap-3 bg-surface border rounded-2xl px-5 py-4 transition-colors duration-200 ${
            focused ? "border-ink2/30" : "border-border"
          }`}
        >
          {loading ? (
            <Loader2 size={20} className="text-accent animate-spin flex-shrink-0" />
          ) : (
            <Search size={20} className={`flex-shrink-0 transition-colors ${focused ? "text-accent" : "text-muted"}`} />
          )}
          <input
            ref={inputRef}
            value={value}
            onChange={(e) => setValue(e.target.value)}
            onFocus={() => setFocused(true)}
            onBlur={() => setFocused(false)}
            placeholder="Type a company name — e.g. Tata Capital, Swiggy, NSE..."
            className="flex-1 bg-transparent outline-none text-ink placeholder:text-muted text-[15px] font-medium"
            autoComplete="off"
          />
          <motion.button
            type="submit"
            disabled={loading || !value.trim()}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className="flex items-center gap-2 bg-accent text-white font-semibold text-sm px-5 py-2.5 rounded-xl disabled:opacity-40 disabled:cursor-not-allowed transition-opacity flex-shrink-0"
          >
            {loading ? "Analyzing..." : "Analyze"}
            {!loading && <ArrowRight size={15} />}
          </motion.button>
        </motion.div>
      </form>

      {!loading && (
        <div className="flex items-center gap-2 mt-3 px-1 flex-wrap">
          <span className="text-xs text-muted font-medium">Try:</span>
          {suggestions.map((s) => (
            <button
              key={s}
              onClick={() => { setValue(s); inputRef.current?.focus() }}
              className="text-xs text-ink2 bg-surface border border-border hover:border-accent/40 hover:text-accent px-2.5 py-1 rounded-lg transition-colors"
            >
              {s}
            </button>
          ))}
        </div>
      )}
    </div>
  )
}
