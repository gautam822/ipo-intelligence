const BASE = "/api"

async function req(path, opts = {}) {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...opts,
  })
  if (!res.ok) {
    const body = await res.text().catch(() => "")
    throw new Error(`${res.status} ${res.statusText}: ${body}`)
  }
  return res.json()
}

export const api = {
  analyse: (company, features) =>
    req("/analyse", { method: "POST", body: JSON.stringify({ company, features }) }),

  analyseAuto: (company) =>
    req("/analyse/auto", { method: "POST", body: JSON.stringify({ company }) }),

  metrics: () => req("/metrics"),

  history: () => req("/history"),

  feedback: (features, decision, alpha_180d) =>
    req("/feedback", { method: "POST", body: JSON.stringify({ features, decision, alpha_180d }) }),

  pdfUrl: (company) => `${BASE}/analyse/pdf`,
}

export default api
