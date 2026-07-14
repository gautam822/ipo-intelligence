import { useState, useEffect, useRef, useCallback } from "react"
import { useSearchParams } from "react-router-dom"
import { motion, AnimatePresence } from "framer-motion"
import { Download, AlertTriangle } from "lucide-react"
import CommandSearch from "../components/CommandSearch"
import Ticker from "../components/Ticker"
import CinematicReveal from "../components/CinematicReveal"
import VerdictHero from "../components/VerdictHero"
import DataBanner from "../components/DataBanner"
import MarketSignals from "../components/MarketSignals"
import { assess } from "../lib/reliability"
import AnimatedNumber from "../components/AnimatedNumber"
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
  { val: "700",    label: "IPOs in training set" },
  { val: "80%",    label: "Hit rate on invest calls" },
  { val: "+21.1%", label: "Alpha vs Nifty, 180d" },
  { val: "35",     label: "Signals per filing" },
]

const HOW = [
  {
    n: "01",
    title: "Read the filing",
    desc: "DRHP from SEBI, NSE subscription data, grey-market premium — 35 signals extracted from the sources analysts actually read.",
  },
  {
    n: "02",
    title: "Weigh it against history",
    desc: "A calibrated XGBoost model scores the issue against 700 Indian IPOs since 2014, with an RL overlay that learns from every 180-day outcome.",
  },
  {
    n: "03",
    title: "Defend the verdict",
    desc: "Every call ships with SHAP-attributed drivers, red flags, and the nearest historical comparable. The reasoning is inspectable, never a black box.",
  },
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
  const [searchParams, setSearchParams] = useSearchParams()
  const autoRan = useRef(false)

  useEffect(() => {
    api.history().then((h) => setHistory([...h].reverse())).catch(() => {})
  }, [])

  const handleSearch = useCallback(async (name) => {
    setLoading(true); setError(null); setResult(null); setPending(null)
    setCompany(name); setShowCinema(true)
    setSearchParams({ q: name }, { replace: true })
    try {
      const res = await api.analyseAuto(name)
      setPending(res)
      api.history().then((h) => setHistory([...h].reverse())).catch(() => {})
    } catch (e) {
      setError(e.message)
      setShowCinema(false)
      setLoading(false)
    }
  }, [setSearchParams])

  // Deep link: /?q=Company (also how Listings rows re-run an analysis)
  useEffect(() => {
    const q = searchParams.get("q")
    if (q && !autoRan.current) {
      autoRan.current = true
      handleSearch(q)
    }
  }, [searchParams, handleSearch])

  function handleDismiss() {
    setResult(pending)
    setShowCinema(false)
    setLoading(false)
    setTimeout(() => resultRef.current?.scrollIntoView({ behavior: "smooth", block: "start" }), 120)
  }

  const tickerItems = history.slice(0, 14).map((h) => ({
    company: h.company, verdict: h.verdict, confidence: h.confidence,
  }))

  return (
    <>
      <CinematicReveal isVisible={showCinema} company={company} result={pending} onDismiss={handleDismiss} />

      <div className="flex flex-col flex-1">
        {tickerItems.length > 0 && <div className="pt-[60px]"><Ticker items={tickerItems} /></div>}

        {/* ── Hero ── */}
        <section className={`relative flex flex-col items-center justify-center text-center px-4 sm:px-6 ${tickerItems.length ? "pt-16 pb-14" : "pt-36 pb-16"}`}>
          <div className="hero-halo" aria-hidden="true" />

          <motion.p
            initial={{ opacity: 0, y: -8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.05 }}
            className="eyebrow relative flex items-center gap-2.5 mb-7"
          >
            <span className="gold-tick" />
            Equity research, automated
            <span className="gold-tick" />
          </motion.p>

          <motion.h1
            initial={{ opacity: 0, y: 14 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1, duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
            className="relative font-display font-normal text-[44px] sm:text-6xl md:text-[68px] tracking-[-0.015em] leading-[1.04] mb-6 max-w-3xl text-ink"
          >
            Should you invest
            <br />
            in <em className="italic" style={{ fontWeight: 500 }}>this</em> IPO?
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="relative text-ink2 text-[15px] sm:text-base max-w-lg mb-11 leading-relaxed"
          >
            Type a company. The model reads the DRHP, checks demand and pricing
            against 700 past listings, and returns a verdict it can defend.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="relative w-full max-w-2xl"
          >
            <CommandSearch onSearch={handleSearch} loading={loading} initialQuery={searchParams.get("q") || ""} />
          </motion.div>

          {!result && !loading && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.55 }}
              className="relative mt-16 w-full max-w-3xl"
            >
              <div className="rule mb-6" />
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-y-6">
                {STATS.map((s, i) => (
                  <div key={s.label} className={`px-4 ${i > 0 ? "sm:border-l sm:border-[rgba(255,255,255,0.08)]" : ""}`}>
                    <AnimatedNumber value={s.val} className="font-mono font-medium text-[22px] tabular text-ink block" />
                    <div className="font-mono text-[9.5px] tracking-caps uppercase text-muted mt-1.5">{s.label}</div>
                  </div>
                ))}
              </div>
              <div className="rule mt-6" />
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
              className="max-w-2xl mx-auto w-full px-4 sm:px-6 pb-8"
            >
              <div className="flex items-start gap-3 bg-avoid-dim border border-avoid-mid rounded-xl px-4 py-3.5 text-sm">
                <AlertTriangle size={15} className="mt-0.5 flex-shrink-0 text-avoid" />
                <div>
                  <p className="font-semibold text-avoid mb-0.5">Analysis failed</p>
                  <p className="text-ink2 text-[13px] break-words">{error}</p>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* ── The report ── */}
        <AnimatePresence>
          {result && (
            <div ref={resultRef} className="max-w-5xl mx-auto w-full px-4 sm:px-6 pb-28 flex flex-col gap-4 scroll-mt-20">
              <DataBanner nFetched={result.n_fetched} nTotal={result.n_total} />
              <VerdictHero result={result} />

              {result.market_signals && Object.keys(result.market_signals).length > 0 && (
                <Panel title="Market signals" delay={0.04}>
                  <MarketSignals result={result} />
                </Panel>
              )}

              {result.about && (
                <Panel title="About the company" delay={0.05}>
                  <p className="text-sm leading-relaxed text-ink2">{result.about}</p>
                </Panel>
              )}

              {/* Detailed model panels only when the verdict is reliable — no fake precision on thin data. */}
              {assess(result).reliable && (
                <>
              {result.explanation && (
                <Panel title={`Why ${result.verdict?.toLowerCase()} — in plain language`} delay={0.1}>
                  <SimpleMarkdown text={result.explanation} />
                </Panel>
              )}

              <div className="grid md:grid-cols-2 gap-4">
                <Panel title="Pillar scorecard" delay={0.15}>
                  <PillarBars pillars={result.pillar_scores} />
                </Panel>
                <Panel title="Top model drivers · SHAP" delay={0.2}>
                  <DriverBars drivers={result.top_drivers} />
                </Panel>

                {result.red_flags?.length > 0 && (
                  <Panel title="Red flags" delay={0.25}>
                    <div className="flex flex-col divide-y divide-[rgba(255,255,255,0.05)]">
                      {result.red_flags.map((f, i) => (
                        <div key={i} className="flex gap-3 py-2.5 text-sm">
                          <span className="font-mono text-[10px] text-avoid mt-[3px] flex-shrink-0 tabular">{String(i + 1).padStart(2, "0")}</span>
                          <span className="text-ink2 leading-relaxed">{f}</span>
                        </div>
                      ))}
                    </div>
                  </Panel>
                )}

                {result.nearest_comparable && (
                  <Panel title="Nearest historical comparable" delay={0.3}>
                    <div className="rounded-lg p-4 border border-border bg-[rgba(255,255,255,0.02)]">
                      <p className="font-semibold text-ink text-[15px]">{result.nearest_comparable.company}</p>
                      <p className="font-mono text-[10px] tracking-wide text-muted mt-1 uppercase">
                        {result.nearest_comparable.sector} · {result.nearest_comparable.year}
                      </p>
                      <div className="rule my-3.5" />
                      <div className="flex items-baseline justify-between">
                        <span className="text-xs text-muted">180-day alpha vs Nifty</span>
                        <span
                          className="font-mono font-semibold text-lg tabular"
                          style={{ color: result.nearest_comparable.alpha_180d >= 0 ? "#40D993" : "#F2657E" }}
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
                whileTap={{ scale: 0.995 }}
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
                  URL.revokeObjectURL(url)
                }}
                className="flex items-center justify-center gap-2 border border-border hover:border-border-strong bg-surface hover:bg-surface2 text-ink2 hover:text-ink font-medium text-sm py-3.5 rounded-xl transition-all"
              >
                <Download size={14} /> Download the PDF report
              </motion.button>
                </>
              )}

              <div className="pt-4">
                <div className="rule mb-4" />
                <p className="font-mono text-[10px] text-muted text-center leading-relaxed">
                  {result.disclaimer || "Model output only — not investment advice. Do your own research."}
                </p>
              </div>
            </div>
          )}
        </AnimatePresence>

        {/* ── How the verdict is made ── */}
        {!result && (
          <section className="border-t border-border py-20 sm:py-24 relative mt-auto">
            <div className="max-w-5xl mx-auto px-4 sm:px-6">
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                className="text-center mb-14"
              >
                <p className="eyebrow mb-4 flex items-center justify-center gap-2">
                  <span className="gold-tick" /> Method
                </p>
                <h2 className="font-display text-3xl sm:text-4xl text-ink">
                  How the verdict is <em className="italic" style={{ fontWeight: 500 }}>made</em>
                </h2>
              </motion.div>

              <div className="grid sm:grid-cols-3 gap-x-10 gap-y-10">
                {HOW.map((item, i) => (
                  <motion.div
                    key={item.n}
                    initial={{ opacity: 0, y: 16 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: i * 0.1, duration: 0.5 }}
                  >
                    <div className="flex items-center gap-3 mb-4">
                      <span className="font-mono text-xs font-medium text-gold tabular">{item.n}</span>
                      <span className="h-px flex-1 bg-[rgba(255,255,255,0.09)]" />
                    </div>
                    <p className="font-semibold text-ink text-[15px] mb-2.5">{item.title}</p>
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
