import { useEffect } from "react"
import { Routes, Route, useLocation } from "react-router-dom"
import { motion, AnimatePresence } from "framer-motion"
import Navbar from "./components/Navbar"
import Footer from "./components/Footer"
import Home from "./pages/Home"
import OpenIPOs from "./pages/OpenIPOs"
import Listings from "./pages/Listings"
import NFO from "./pages/NFO"
import TrackRecord from "./pages/TrackRecord"
import About from "./pages/About"
import NotFound from "./pages/NotFound"

function ScrollToTop() {
  const { pathname } = useLocation()
  useEffect(() => { window.scrollTo(0, 0) }, [pathname])
  return null
}

const pageMotion = {
  initial: { opacity: 0, y: 12 },
  animate: { opacity: 1, y: 0 },
  exit:    { opacity: 0, y: -8 },
  transition: { duration: 0.4, ease: [0.22, 1, 0.36, 1] },
}

function AnimatedRoutes() {
  const location = useLocation()
  return (
    <AnimatePresence mode="wait">
      <motion.div key={location.pathname} className="flex-1 flex flex-col" {...pageMotion}>
        <Routes location={location}>
          <Route path="/"             element={<Home />} />
          <Route path="/open"         element={<OpenIPOs />} />
          <Route path="/listings"     element={<Listings />} />
          <Route path="/nfo"          element={<NFO />} />
          <Route path="/track-record" element={<TrackRecord />} />
          <Route path="/about"        element={<About />} />
          <Route path="*"             element={<NotFound />} />
        </Routes>
      </motion.div>
    </AnimatePresence>
  )
}

export default function App() {
  return (
    <div className="min-h-screen bg-bg text-ink font-sans relative flex flex-col">
      {/* Ground layers */}
      <div className="graph-grid" aria-hidden="true" />
      <div className="grain" aria-hidden="true" />

      <ScrollToTop />

      <div className="relative z-10 flex flex-col flex-1">
        <Navbar />
        <main className="flex-1 flex flex-col">
          <AnimatedRoutes />
        </main>
        <Footer />
      </div>
    </div>
  )
}
