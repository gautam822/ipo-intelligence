import { Link } from "react-router-dom"
import { ArrowLeft } from "lucide-react"

export default function NotFound() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center text-center px-6 pt-16">
      <p className="eyebrow mb-5 flex items-center gap-2">
        <span className="gold-tick" /> Page not listed
      </p>
      <p className="font-mono font-semibold text-[64px] sm:text-[88px] leading-none tracking-tight text-ink mb-4 tabular">
        404
      </p>
      <h1 className="font-display text-2xl sm:text-3xl text-ink2 mb-10">
        This ticker isn&rsquo;t on the <em className="text-ink not-italic font-display italic">exchange</em>.
      </h1>
      <Link
        to="/"
        className="inline-flex items-center gap-2 px-5 py-2.5 rounded-lg text-[13px] font-medium text-ink border border-border-strong bg-surface hover:bg-surface2 transition-colors"
      >
        <ArrowLeft size={14} /> Back to analysis
      </Link>
    </div>
  )
}
