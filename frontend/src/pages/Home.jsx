import { useState, useEffect, useRef, useCallback } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { Download, ExternalLink, AlertTriangle, Zap, Shield, Brain, ChevronDown } from "lucide-react"
import CommandSearch from "../components/CommandSearch"
import Ticker from "../components/Ticker"
import CinematicReveal from "../components/CinematicReveal"
import VerdictHero from "../components/VerdictHero"
import DataBanner from "../components/DataBanner"
import Panel from "../components/Panel"
import PillarBars from "../components/PillarBars"
import DriverBars from "../components/DriverBars"
import api from "../lib/api"

// Render **bold** and ⚠️ emoji markdown from the LLM explanation
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

const HOW_IT_WORKS = [
  { icon: Zap,    title: "Scrape & Fetch",      desc: "We pull DRHP from SEBI, NSE subscription data, GMP, and 35 financial signals in real-time." },
  { icon: Brain,  title: "ML + RL Verdict",     desc: "Calibrated XGBoost on 700 IPOs, overlaid with a REINFORCE agent that self-corrects from 180-day outcomes." },
  { icon: Shield, title: "SHAP Explainability", desc: "Every verdict shows exactly which features drove the call — no black box. See the signals behind the score." },
]

export default function Home() {
  const [result, setResult]           = useState(null)
  const [loading, setLoading]         = useState(false)
  const [company, setCompany]         = useState("")
  const [error, setError]             = useState(null)
  const [history, setHistory]         = useState([])
  const [showCinema, setShowCinema]   = useState(false)
  const [pendingResult, setPending]   = useState(null)
  const resultRef = useRef(null)

  useEffect(() => {
    api.history().then((h) => setHistory(h.reverse())).catch(() => {})
  }, [])

  async function handleSearch(name) {
    setLoading(true); setError(null); setResult(null); setPending(null)
    setCompany(name); setShowCinema(true)
    try {
      const res = await api.analyseAuto(name)
      setPending(res)
      api.history().then((h) => setHistory(h.reverse())).catch(() => {})
    } catch (e) {
      setError(e.message)
      setShowCinema(false)
      setLoading(false)
    }
  }

  function handleDismiss() {
    setResult(pendingResult)
    setShowCinema(false)
    setLoading(false)
    setTimeout(() => resultRef.current?.scrollIntoView({ behavior: "smooth", block: "start" }), 120)
  }

  const tickerItems = history.slice(0, 14).map((h) => ({
    company: h.company, verdict: h.verdict, confidence: h.confidence,
  }))

  return (
    <>
      <CinematicReveal isVisible={showCinema} company={company} result={pendingResult} onDismiss={handleDismiss} />

      <div className="flex flex-col min-h-screen">
        {tickerItems.length > 0 && <div className="pt-16"><Ticker items={tickerItems} /></div>}

        {/* Hero */}
        <section className="flex-1 flex flex-col">
          <div className={`max-w-5xl mx-auto w-full px-4 sm:px-6 flex flex-col items-center text-center ${tickerItems.length ? "py-14 sm:py-20" : "pt-28 pb-14 sm:pt-36 sm:pb-20"}`}>

            <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}
              className="inline-flex items-center gap-2 bg-accent-dim border border-accent-mid text-accent text-xs font-semibold px-3 py-1.5 rounded-full mb-6">
              <span className="w-1.5 h-1.5 rounded-full bg-accent animate-pulse" />
              XGBoost + Reinforcement Learning · 700 Indian IPOs
            </motion.div>

            <motion.h1 initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.15, duration: 0.55 }}
              className="font-black text-4xl sm:text-5xl md:text-6xl text-ink leading-[1.1] tracking-tight mb-4">
              Should you invest<br />
              <span className="gradient-text">in this IPO?</span>
            </motion.h1>

            <motion.p initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.25 }}
              className="text-ink2 text-lg max-w-lg mb-10 leading-relaxed">
              Type any company name. We scrape the filings, run the model, and deliver an analyst-grade verdict in seconds.
            </motion.p>

            <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.35 }} className="w-full">
              <CommandSearch onSearch={handleSearch} loading={loading} />
            </motion.div>

            {!result && !loading && (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 1.4 }}
                className="mt-14 flex flex-col items-center gap-2 text-muted">
                <span className="text-xs font-medium">How it works</span>
                <ChevronDown size={16} className="animate-bounce" />
              </motion.div>
            )}
          </div>

          {/* Error */}
          <AnimatePresence>
            {error && (
              <motion.div initial={{ opacity: 0, y: -8 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}
                className="max-w-2xl mx-auto w-full px-4 sm:px-6 pb-6">
                <div className="flex items-start gap-3 bg-avoid-dim border border-red-200 rounded-xl px-4 py-3.5 text-avoid text-sm">
                  <AlertTriangle size={16} className="mt-0.5 flex-shrink-0" />
                  <span>{error}</span>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Results */}
          <AnimatePresence>
            {result && (
              <div ref={resultRef} className="max-w-5xl mx-auto w-full px-4 sm:px-6 pb-16 flex flex-col gap-5">
                {result.source_url && (
                  <a href={result.source_url} target="_blank" rel="noreferrer"
                    className="self-start flex items-center gap-1.5 font-mono text-[11px] text-muted hover:text-accent transition-colors">
                    <ExternalLink size={11} /> Source: {result.source_url}
                  </a>
                )}

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

                <div className="grid md:grid-cols-2 gap-5">
                  <Panel title="Pillar scorecard" delay={0.15}>
                    <PillarBars pillars={result.pillar_scores} />
                  </Panel>
                  <Panel title="Top model drivers (SHAP)" delay={0.2}>
                    <DriverBars drivers={result.top_drivers} />
                  </Panel>
                  {result.red_flags?.length > 0 && (
                    <Panel title="Red flags" delay={0.25}>
                      <div className="flex flex-col divide-y divide-border">
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
                      <div className="bg-surface2 border border-border rounded-xl p-4">
                        <p className="font-semibold text-ink">{result.nearest_comparable.company}</p>
                        <p className="text-muted text-xs mt-0.5 font-mono">{result.nearest_comparable.sector} · {result.nearest_comparable.year}</p>
                        <div className="mt-3 flex items-baseline gap-2">
                          <span className="text-xs text-muted">180-day alpha vs Nifty:</span>
                          <span className="tabular font-bold text-sm" style={{ color: result.nearest_comparable.alpha_180d >= 0 ? "#059669" : "#DC2626" }}>
                            {result.nearest_comparable.alpha_180d > 0 ? "+" : ""}{result.nearest_comparable.alpha_180d}%
                          </span>
                        </div>
                      </div>
                    </Panel>
                  )}
                </div>

                <button
                  onClick={async () => {
                    const res = await fetch("/api/analyse/pdf", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ company: result.company, features: {} }) })
                    const blob = await res.blob()
                    const url = URL.createObjectURL(blob)
                    const a = document.createElement("a"); a.href = url; a.download = `${result.company}_report.pdf`; a.click()
                  }}
                  className="flex items-center justify-center gap-2 bg-surface border border-border hover:border-accent/40 hover:shadow-card text-ink2 hover:text-accent font-medium text-sm py-3.5 rounded-2xl transition-all"
                >
                  <Download size={15} /> Download full PDF report
                </button>

                <p className="font-mono text-[10px] text-muted text-center leading-relaxed pt-3 border-t border-border">
                  {result.disclaimer || "Not investment advice. Model output only — do your own research."}
                </p>
              </div>
            )}
          </AnimatePresence>
        </section>

        {/* How it works — only when no result showing */}
        {!result && (
          <section className="bg-surface border-t border-border py-16">
            <div className="max-w-5xl mx-auto px-4 sm:px-6">
              <h2 className="text-xl font-bold text-ink text-center mb-10">How it works</h2>
              <div className="grid sm:grid-cols-3 gap-6">
                {HOW_IT_WORKS.map((item, i) => (
                  <motion.div key={i} initial={{ opacity: 0, y: 16 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: i * 0.1, duration: 0.4 }}
                    className="flex flex-col gap-3 p-6 bg-bg rounded-2xl border border-border hover:shadow-card transition-shadow">
                    <div className="w-10 h-10 rounded-xl bg-accent-dim flex items-center justify-center">
                      <item.icon size={18} className="text-accent" />
                    </div>
                    <p className="font-semibold text-ink text-sm">{item.title}</p>
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
