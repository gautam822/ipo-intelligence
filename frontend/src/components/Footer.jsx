import { Link } from "react-router-dom"
import BrandMark from "./BrandMark"

const NAV = [
  { to: "/",             label: "Analyze" },
  { to: "/listings",     label: "Listings" },
  { to: "/track-record", label: "Track record" },
  { to: "/about",        label: "Method" },
]

export default function Footer() {
  return (
    <footer className="relative z-10 mt-auto border-t border-border">
      <div className="max-w-6xl mx-auto px-5 sm:px-8 py-12">
        <div className="flex flex-col md:flex-row gap-10 md:gap-16 justify-between">
          <div className="max-w-xs">
            <BrandMark />
            <p className="text-[13px] text-ink2 leading-relaxed mt-4">
              A self-correcting verdict engine for Indian mainboard IPOs.
              Calibrated ML, reinforcement learning, and full SHAP
              explainability — trained on 700 listings since 2014.
            </p>
          </div>

          <div className="flex gap-14 flex-wrap">
            <div>
              <p className="eyebrow mb-4">Product</p>
              <ul className="space-y-2.5">
                {NAV.map((l) => (
                  <li key={l.to}>
                    <Link to={l.to} className="text-[13px] text-ink2 hover:text-ink transition-colors">
                      {l.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
            <div>
              <p className="eyebrow mb-4">Project</p>
              <ul className="space-y-2.5">
                <li>
                  <Link to="/about" className="text-[13px] text-ink2 hover:text-ink transition-colors">
                    Model performance
                  </Link>
                </li>
                <li>
                  <Link to="/about" className="text-[13px] text-ink2 hover:text-ink transition-colors">
                    Limitations
                  </Link>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <div className="rule mt-12 mb-5" />
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
          <p className="font-mono text-[10px] tracking-wide text-muted">
            © {new Date().getFullYear()} IPO Intelligence
          </p>
          <p className="font-mono text-[10px] tracking-wide text-muted text-left sm:text-right">
            Educational research tool. Not SEBI-registered investment advice — do your own research.
          </p>
        </div>
      </div>
    </footer>
  )
}
