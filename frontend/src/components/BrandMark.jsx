// The seal: bond-gold ring + rising spark. Wordmark speaks in the app's two
// voices — mono "IPO" (the machine), serif italic "Intelligence" (the press).
export function Seal({ size = 26 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 32 32" aria-hidden="true" className="flex-shrink-0">
      <rect width="32" height="32" rx="7" fill="rgba(201,169,97,0.08)" />
      <rect x="0.5" y="0.5" width="31" height="31" rx="6.5" fill="none" stroke="rgba(201,169,97,0.35)" />
      <circle cx="16" cy="16" r="10" fill="none" stroke="#C9A961" strokeWidth="1.3" />
      <path
        d="M10.8 19.4l3.7-3.7 2.4 2.4 4.6-5.8"
        fill="none"
        stroke="#C9A961"
        strokeWidth="1.9"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  )
}

export default function BrandMark({ size = 26 }) {
  return (
    <span className="flex items-center gap-2.5">
      <Seal size={size} />
      <span className="leading-none whitespace-nowrap">
        <span className="font-mono font-semibold text-[13px] tracking-[0.08em] text-ink">IPO</span>
        <span className="font-display italic text-[17px] text-ink ml-1.5" style={{ fontWeight: 500 }}>
          Intelligence
        </span>
      </span>
    </span>
  )
}
