import { useState, useEffect } from "react"
import { NavLink, useLocation } from "react-router-dom"
import { Menu, X } from "lucide-react"
import { motion, AnimatePresence } from "framer-motion"
import BrandMark from "./BrandMark"

const links = [
  { to: "/",             label: "Analyze",      end: true },
  { to: "/open",         label: "Open IPOs" },
  { to: "/listings",     label: "Listings" },
  { to: "/nfo",          label: "NFOs" },
  { to: "/track-record", label: "Track record" },
  { to: "/about",        label: "Method" },
]

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false)
  const [open, setOpen]         = useState(false)
  const location = useLocation()

  useEffect(() => {
    const fn = () => setScrolled(window.scrollY > 12)
    window.addEventListener("scroll", fn, { passive: true })
    return () => window.removeEventListener("scroll", fn)
  }, [])

  useEffect(() => setOpen(false), [location])

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled ? "bg-[rgba(10,11,13,0.86)] backdrop-blur-xl border-b border-border" : "bg-transparent border-b border-transparent"
      }`}
    >
      <div className="max-w-6xl mx-auto px-5 sm:px-8 h-[60px] flex items-center justify-between gap-4">
        <NavLink to="/" className="group" aria-label="IPO Intelligence — home">
          <BrandMark />
        </NavLink>

        {/* Desktop nav */}
        <nav className="hidden md:flex items-center gap-6" aria-label="Primary">
          {links.map((l) => (
            <NavLink
              key={l.to}
              to={l.to}
              end={l.end}
              className={({ isActive }) =>
                `relative py-2 text-[13px] font-medium transition-colors duration-200 ${
                  isActive ? "text-ink" : "text-ink2 hover:text-ink"
                }`
              }
            >
              {({ isActive }) => (
                <>
                  {l.label}
                  {isActive && (
                    <motion.span
                      layoutId="nav-underline"
                      className="absolute left-0 right-0 -bottom-px h-px bg-gold"
                      transition={{ type: "spring", stiffness: 420, damping: 34 }}
                    />
                  )}
                </>
              )}
            </NavLink>
          ))}
        </nav>

        <div className="flex items-center gap-2">

          {/* Mobile hamburger */}
          <button
            onClick={() => setOpen((v) => !v)}
            className="md:hidden p-2 rounded-lg text-ink2 hover:text-ink hover:bg-surface transition-colors"
            aria-label={open ? "Close menu" : "Open menu"}
            aria-expanded={open}
          >
            {open ? <X size={19} /> : <Menu size={19} />}
          </button>
        </div>
      </div>

      {/* Mobile menu */}
      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.2 }}
            className="md:hidden overflow-hidden bg-[rgba(10,11,13,0.96)] backdrop-blur-xl border-b border-border px-4 pb-4"
          >
            {links.map((l, i) => (
              <motion.div
                key={l.to}
                initial={{ opacity: 0, x: -8 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.04 }}
              >
                <NavLink
                  to={l.to}
                  end={l.end}
                  className={({ isActive }) =>
                    `block px-4 py-3 rounded-lg text-sm font-medium mt-1 transition-colors ${
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
