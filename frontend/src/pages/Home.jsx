import { useState, useEffect, useRef } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { Download, AlertTriangle, Zap, Shield, Brain, ChevronDown } from "lucide-react"
import CommandSearch from "../components/CommandSearch"
import Ticker from "../components/Ticker"
import CinematicReveal from "../components/CinematicReveal"
import VerdictHero from "../components/VerdictHero"
import DataBanner from "../components/DataBanner"
import Panel from "../components/Panel"
import PillarBars from "../components/PillarBars"
import DriverBars from "../components/DriverBars"
import api from "../lib/api"

function SimpleMarkdown({ text }) {
  if (!text) return null
  const parts = text.split(/(\*\*[^*]+\*\*)/g)
  return (
    <p className="text-sm leading-relaxed text-ink2 whitespace-pre-line">
      {parts.map((p, i) =>
        p.startsWith("**") && p.endsWith("**")
          ? <strong key={i} className="font-semibold text-ink">{p.slice(2, -2)}</strong>
          : p
      )}
    </p>
  )
}

const STATS = [
  { val: "700+", label: "IPOs trained" },
  { val: "80%",  label: "Hit rate" },
  { val: "+21%", label: "Alpha 180d" },
  { val: "35",   label: "Signals" },
]

const HOW = [
  { icon: Zap,    color: "#818CF8", title: "Scrape & Fetch",      desc: "DRHP from SEBI, NSE subscription data, GMP and 35 financial signals — in real-time." },
  { icon: Brain,  color: "#34D399", title: "ML + RL Verdict",     desc: "Calibrated XGBoost on 700 IPOs, overlaid with a REINFORCE agent that learns from 180-day outcomes." },
  { icon: Shield, color: "#FBBF24", title: "SHAP Explainability", desc: "Every verdict shows which features drove the call. No black box — full transparency." },
]

export default function Home() {
  const [result, setResult]         = useState(null)
  const [loading, setLoading]       = useState(false)
  const [company, setCompany]       = useState("")
  const [error, setError]           = useState(null)
  const [history, setHistory]       = useState([])
  const [showCinema, setShowCinema] = useState(false)
  const [pending, setPending]       = useState(null)
  const resultRef = useRef(null)

  useEffect(() => {
    api.history().then(h => setHistory(h.reverse())).catch(() => {})
  }, [])

  async function handleSearch(name) {
    setLoading(true); setError(null); setResult(null); setPending(null)
    setCompany(name); setShowCinema(true)
    try {
      const res = await api.analyseAuto(name)
      setPending(res)
      api.history().then(h => setHistory(h.reverse())).catch(() => {})
    } catch (e) {
      setError(e.message)
      setShowCinema(false)
      setLoading(false)
    }
  }

  function handleDismiss() {
    setResult(pending)
    setShowCinema(false)
    setLoading(false)
    setTimeout(() => resultRef.current?.scrollIntoView({ behavior: "smooth", block: "start" }), 120)
  }

  const tickerItems = history.slice(0, 14).map(h => ({
    company: h.company, verdict: h.verdict, confidence: h.confidence,
  }))

  return (
    <>
      <CinematicReveal isVisible={showCinema} company={company} result={pending} onDismiss={handleDismiss} />

      <div className="flex flex-col min-h-screen">
        {tickerItems.length > 0 && <div className="pt-16"><Ticker items={tickerItems} /></div>}

        {/* ── Hero ── */}
        <section className={`flex-1 flex flex-col items-center justify-center text-center px-4 sm:px-6 ${tickerItems.length ? "pt-12 pb-10" : "pt-32 pb-12"}`}>

          <motion.div
            initial={{ opacity: 0, y: -12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.05 }}
            className="inline-flex items-center gap-2 mb-6 px-4 py-2 rounded-full text-xs font-semibold font-mono tracking-wide border"
            style={{ background: "rgba(129,140,248,0.08)", borderColor: "rgba(129,140,248,0.25)", color: "#818CF8" }}
          >
            <span className="w-1.5 h-1.5 rounded-full bg-accent animate-pulse" />
            XGBoost + Reinforcement Learning · 700 Indian IPOs
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1, duration: 0.6 }}
            className="font-display font-black text-4xl sm:text-5xl md:text-6xl lg:text-7xl tracking-tight leading-[1.05] mb-5 max-w-3xl"
          >
            Should you invest
            <br />
            <span className="gradient-text">in this IPO?</span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="text-ink2 text-lg max-w-md mb-10 leading-relaxed"
          >
            Type any company name. We scrape the filings, run the model, and deliver an analyst-grade verdict in seconds.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="w-full max-w-2xl mb-12"
          >
            <CommandSearch onSearch={handleSearch} loading={loading} />
          </motion.div>

          {!result && !loading && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.6 }}
              className="flex items-center gap-10 flex-wrap justify-center"
            >
              {STATS.map((s, i) => (
                <motion.div
                  key={s.label}
                  initial={{ opacity: 0, y: 8 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.6 + i * 0.08 }}
                  className="text-center"
                >
                  <div className="font-display font-black text-2xl gradient-text">{s.val}</div>
                  <div className="text-xs text-muted font-medium mt-0.5 tracking-wide">{s.label}</div>
                </motion.div>
              ))}
            </motion.div>
          )}

          {!result && !loading && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 1.5 }}
              className="mt-14 flex flex-col items-center gap-2 text-muted"
            >
              <span className="text-[10px] font-mono tracking-[0.16em] uppercase">How it works</span>
              <ChevronDown size={16} className="animate-bounce" />
            </motion.div>
          )}
        </section>

        {/* ── Error ── */}
        <AnimatePresence>
          {error && (
            <motion.div
              initial={{ opacity: 0, y: -8 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              className="max-w-2xl mx-auto w-full px-4 sm:px-6 pb-6"
            >
              <div className="flex items-start gap-3 bg-avoid-dim border border-avoid-mid rounded-xl px-4 py-3.5 text-avoid text-sm">
                <AlertTriangle size={16} className="mt-0.5 flex-shrink-0" />
                <span>{error}</span>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* ── Results ── */}
        <AnimatePresence>
          {result && (
            <div ref={resultRef} className="max-w-5xl mx-auto w-full px-4 sm:px-6 pb-24 flex flex-col gap-4">
              <DataBanner nFetched={result.n_fetched} nTotal={result.n_total} />
              <VerdictHero result={result} />

              {result.about && (
                <Panel title="About the company" delay={0.05}>
                  <p className="text-sm leading-relaxed text-ink2">{result.about}</p>
                </Panel>
              )}

              {result.explanation && (
                <Panel title={`Why ${result.verdict?.toLowerCase()}? — plain language`} delay={0.1}>
                  <SimpleMarkdown text={result.explanation} />
                </Panel>
              )}

              <div className="grid md:grid-cols-2 gap-4">
                <Panel title="Pillar scorecard" delay={0.15}>
                  <PillarBars pillars={result.pillar_scores} />
                </Panel>
                <Panel title="Top model drivers (SHAP)" delay={0.2}>
                  <DriverBars drivers={result.top_drivers} />
                </Panel>

                {result.red_flags?.length > 0 && (
                  <Panel title="Red flags" delay={0.25}>
                    <div className="flex flex-col divide-y divide-[rgba(255,255,255,0.05)]">
                      {result.red_flags.map((f, i) => (
                        <div key={i} className="flex gap-3 py-2.5 text-sm">
                          <span className="w-1.5 h-1.5 rounded-full bg-avoid mt-1.5 flex-shrink-0" />
                          <span className="text-ink2 leading-relaxed">{f}</span>
                        </div>
                      ))}
                    </div>
                  </Panel>
                )}

                {result.nearest_comparable && (
                  <Panel title="Nearest historical comparable" delay={0.3}>
                    <div className="rounded-xl p-4" style={{ background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.07)" }}>
                      <p className="font-semibold text-ink">{result.nearest_comparable.company}</p>
                      <p className="text-muted text-xs mt-0.5 font-mono">{result.nearest_comparable.sector} · {result.nearest_comparable.year}</p>
                      <div className="mt-3 flex items-baseline gap-2">
                        <span className="text-xs text-muted">180-day alpha vs Nifty:</span>
                        <span
                          className="font-bold text-lg font-mono"
                          style={{ color: result.nearest_comparable.alpha_180d >= 0 ? "#34D399" : "#FB7185" }}
                        >
                          {result.nearest_comparable.alpha_180d > 0 ? "+" : ""}{result.nearest_comparable.alpha_180d}%
                        </span>
                      </div>
                    </div>
                  </Panel>
                )}
              </div>

              <motion.button
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.4 }}
                whileHover={{ y: -1 }}
                whileTap={{ scale: 0.99 }}
                onClick={async () => {
                  const res = await fetch("/api/analyse/pdf", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ company: result.company, features: {} }),
                  })
                  const blob = await res.blob()
                  const url = URL.createObjectURL(blob)
                  const a = document.createElement("a")
                  a.href = url; a.download = `${result.company}_report.pdf`; a.click()
                }}
                className="flex items-center justify-center gap-2 border border-[rgba(255,255,255,0.08)] hover:border-[rgba(255,255,255,0.18)] bg-[rgba(255,255,255,0.03)] hover:bg-[rgba(255,255,255,0.06)] text-ink2 hover:text-ink font-medium text-sm py-3.5 rounded-2xl transition-all"
              >
                <Download size={15} /> Download full PDF report
              </motion.button>

              <p className="font-mono text-[10px] text-muted text-center leading-relaxed pt-3 border-t border-[rgba(255,255,255,0.06)]">
                {result.disclaimer || "Not investment advice. Model output only — do your own research."}
              </p>
            </div>
          )}
        </AnimatePresence>

        {/* ── How it works ── */}
        {!result && (
          <section className="border-t border-[rgba(255,255,255,0.06)] py-20 relative">
            <div className="max-w-5xl mx-auto px-4 sm:px-6">
              <motion.h2
                initial={{ opacity: 0, y: 12 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                className="font-display font-bold text-2xl text-center mb-12"
              >
                How it <span className="gradient-text">works</span>
              </motion.h2>
              <div className="grid sm:grid-cols-3 gap-5">
                {HOW.map((item, i) => (
                  <motion.div
                    key={i}
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: i * 0.12, duration: 0.5 }}
                    className="relative rounded-2xl p-6 overflow-hidden group"
                    style={{ background: "rgba(255,255,255,0.02)", border: "1px solid rgba(255,255,255,0.07)" }}
                    whileHover={{ y: -3, transition: { duration: 0.2 } }}
                  >
                    <div className="absolute top-0 left-0 right-0 h-px" style={{ background: `linear-gradient(90deg, transparent, ${item.color}50, transparent)` }} />
                    <div className="w-10 h-10 rounded-xl flex items-center justify-center mb-4" style={{ background: `${item.color}15`, border: `1px solid ${item.color}25` }}>
                      <item.icon size={18} style={{ color: item.color }} />
                    </div>
                    <p className="font-semibold text-ink text-sm mb-2">{item.title}</p>
                    <p className="text-ink2 text-sm leading-relaxed">{item.desc}</p>
                  </motion.div>
                ))}
              </div>
            </div>
          </section>
        )}
      </div>
    </>
  )
}
