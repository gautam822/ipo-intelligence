import { useState, useEffect } from "react"
import { NavLink, useLocation } from "react-router-dom"
import { TrendingUp, Menu, X } from "lucide-react"
import { motion, AnimatePresence } from "framer-motion"

const links = [
  { to: "/",             label: "Analyze",      end: true },
  { to: "/listings",     label: "IPO Listings" },
  { to: "/track-record", label: "Track Record" },
  { to: "/about",        label: "How It Works" },
]

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false)
  const [open, setOpen]         = useState(false)
  const location = useLocation()

  useEffect(() => {
    const fn = () => setScrolled(window.scrollY > 16)
    window.addEventListener("scroll", fn, { passive: true })
    return () => window.removeEventListener("scroll", fn)
  }, [])

  useEffect(() => setOpen(false), [location])

  return (
    <header className={`fixed top-0 left-0 right-0 z-50 transition-all duration-500 ${
      scrolled
        ? "bg-[rgba(8,9,15,0.85)] backdrop-blur-2xl border-b border-border"
        : "bg-transparent"
    }`}>
      <div className="max-w-6xl mx-auto px-5 sm:px-8 h-16 flex items-center justify-between">

        {/* Logo */}
        <NavLink to="/" className="flex items-center gap-2.5 group">
          <div className="relative w-8 h-8 rounded-xl bg-gradient-to-br from-accent to-invest flex items-center justify-center shadow-lg group-hover:scale-105 transition-transform duration-300">
            <TrendingUp size={15} className="text-white" strokeWidth={2.5} />
            <div className="absolute inset-0 rounded-xl bg-gradient-to-br from-accent to-invest opacity-0 group-hover:opacity-100 blur-md transition-opacity duration-300" />
          </div>
          <span className="font-display font-bold text-[15px] tracking-tight">
            <span className="text-ink">IPO</span>
            <span className="gradient-text">Intelligence</span>
          </span>
        </NavLink>

        {/* Desktop nav */}
        <nav className="hidden md:flex items-center gap-1 p-1 rounded-2xl bg-surface border border-border">
          {links.map((l) => (
            <NavLink
              key={l.to}
              to={l.to}
              end={l.end}
              className={({ isActive }) =>
                `relative px-4 py-1.5 rounded-xl text-sm font-medium transition-all duration-200 ${
                  isActive
                    ? "text-ink"
                    : "text-ink2 hover:text-ink"
                }`
              }
            >
              {({ isActive }) => (
                <>
                  {isActive && (
                    <motion.div
                      layoutId="nav-pill"
                      className="absolute inset-0 rounded-xl bg-surface2 border border-border-strong"
                      transition={{ type: "spring", stiffness: 400, damping: 30 }}
                    />
                  )}
                  <span className="relative z-10">{l.label}</span>
                </>
              )}
            </NavLink>
          ))}
        </nav>

        {/* CTA */}
        <a
          href="https://github.com/gautam822/ipo-intelligence"
          target="_blank"
          rel="noreferrer"
          className="hidden md:flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-semibold text-ink2 hover:text-ink border border-border hover:border-border-strong bg-surface hover:bg-surface2 transition-all duration-200"
        >
          <svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor">
            <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/>
          </svg>
          GitHub
        </a>

        {/* Mobile hamburger */}
        <button
          onClick={() => setOpen(v => !v)}
          className="md:hidden p-2 rounded-xl text-ink2 hover:text-ink hover:bg-surface transition-colors"
        >
          {open ? <X size={20} /> : <Menu size={20} />}
        </button>
      </div>

      {/* Mobile menu */}
      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.2 }}
            className="md:hidden overflow-hidden bg-[rgba(8,9,15,0.95)] backdrop-blur-2xl border-b border-border px-4 pb-4"
          >
            {links.map((l, i) => (
              <motion.div
                key={l.to}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.05 }}
              >
                <NavLink
                  to={l.to}
                  end={l.end}
                  className={({ isActive }) =>
                    `block px-4 py-3 rounded-xl text-sm font-medium mt-1 transition-colors ${
                      isActive
                        ? "bg-surface2 text-ink border border-border"
                        : "text-ink2 hover:text-ink hover:bg-surface"
                    }`
                  }
                >
                  {l.label}
                </NavLink>
              </motion.div>
            ))}
          </motion.div>
        )}
      </AnimatePresence>
    </header>
  )
}
