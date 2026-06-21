import { useState, useEffect } from "react"
import { NavLink, useLocation } from "react-router-dom"
import { TrendingUp, Menu, X } from "lucide-react"
import { motion, AnimatePresence } from "framer-motion"

const links = [
  { to: "/", label: "Analyze", end: true },
  { to: "/listings", label: "IPO Listings" },
  { to: "/track-record", label: "Track Record" },
  { to: "/about", label: "How It Works" },
]

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false)
  const [open, setOpen] = useState(false)
  const location = useLocation()

  useEffect(() => {
    const fn = () => setScrolled(window.scrollY > 12)
    window.addEventListener("scroll", fn, { passive: true })
    return () => window.removeEventListener("scroll", fn)
  }, [])

  useEffect(() => setOpen(false), [location])

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-40 transition-all duration-300 ${
        scrolled
          ? "bg-surface/90 backdrop-blur-md shadow-card border-b border-border"
          : "bg-transparent"
      }`}
    >
      <div className="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
        <NavLink to="/" className="flex items-center gap-2.5 group">
          <div className="w-8 h-8 rounded-lg bg-accent flex items-center justify-center shadow-sm group-hover:scale-105 transition-transform duration-200">
            <TrendingUp size={16} className="text-white" strokeWidth={2.5} />
          </div>
          <span className="font-bold text-[15px] text-ink tracking-tight">
            IPO<span className="text-accent">Intelligence</span>
          </span>
        </NavLink>

        <nav className="hidden md:flex items-center gap-1">
          {links.map((l) => (
            <NavLink
              key={l.to}
              to={l.to}
              end={l.end}
              className={({ isActive }) =>
                `px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                  isActive
                    ? "bg-accent-dim text-accent"
                    : "text-ink2 hover:text-ink hover:bg-surface"
                }`
              }
            >
              {l.label}
            </NavLink>
          ))}
        </nav>

        <button
          onClick={() => setOpen((v) => !v)}
          className="md:hidden p-2 rounded-lg text-ink2 hover:bg-surface transition-colors"
          aria-label="Toggle menu"
        >
          {open ? <X size={20} /> : <Menu size={20} />}
        </button>
      </div>

      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, y: -6 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -6 }}
            transition={{ duration: 0.15 }}
            className="md:hidden bg-surface border-b border-border px-4 pb-4 shadow-card"
          >
            {links.map((l) => (
              <NavLink
                key={l.to}
                to={l.to}
                end={l.end}
                className={({ isActive }) =>
                  `block px-4 py-3 rounded-lg text-sm font-medium mt-1 transition-colors ${
                    isActive ? "bg-accent-dim text-accent" : "text-ink2 hover:text-ink hover:bg-bg"
                  }`
                }
              >
                {l.label}
              </NavLink>
            ))}
          </motion.div>
        )}
      </AnimatePresence>
    </header>
  )
}
