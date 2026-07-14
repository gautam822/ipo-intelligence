// Central reliability gate. The model only produces a *trustworthy* verdict when
// it actually gathered enough signal. Below the floor, or when confidence is
// degenerate, we reach an honest "inconclusive" conclusion instead of faking
// a confident INVEST/NEUTRAL/AVOID.

export const MIN_SIGNALS = 8   // of ~35; below this, coverage is too thin to trust

export function assess(result) {
  if (!result) {
    return { reliable: false, reason: "no-result", verdict: null, confidencePct: 0 }
  }

  const conf = Number(result.confidence_pct)
  const validConf = Number.isFinite(conf) && conf > 0

  // n_fetched is present on name-based (auto) analyses. When absent (manual
  // feature entry) we don't gate on coverage.
  const nFetched = result.n_fetched
  const coverageKnown = typeof nFetched === "number"
  const thinData = coverageKnown && nFetched < MIN_SIGNALS

  const reliable = validConf && !thinData

  let reason = "ok"
  if (!validConf) reason = "bad-confidence"
  else if (thinData) reason = "thin-data"

  return {
    reliable,
    reason,
    verdict: reliable ? result.verdict : "INCONCLUSIVE",
    confidencePct: validConf ? conf : null,
    nFetched: coverageKnown ? nFetched : null,
    nTotal: result.n_total ?? null,
  }
}

export const INCONCLUSIVE_COPY = {
  title: "Not enough data to call it",
  body:
    "We couldn't gather enough reliable signals on this name to reach a confident verdict — " +
    "so we won't guess. This usually means the company name was misspelt, it isn't a current " +
    "mainboard IPO, or its filing data isn't public yet. Check the spelling, or try a company " +
    "that's currently open.",
}
