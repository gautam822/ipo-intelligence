"""
AUTO-FETCH LAYER — turns an IPO *name* into the 35-feature vector.

Flow:
  name ──► 1. find IPO on Chittorgarh (details page URL)
       ──► 2. scrape issue structure: price band, OFS/fresh, GMP, subscription
       ──► 3. scrape financials table (revenue, PAT, debt, OCF if shown)
       ──► 4. locate + download DRHP PDF from SEBI link on the page
       ──► 5. (optional, needs ANTHROPIC_API_KEY) LLM reads DRHP for
              governance / risk / objects scores
       ──► 6. compute derived features, fill gaps with historical medians
       ──► 7. return features dict ready for pipeline.analyze.IPOAnalyzer

Run:  python pipeline/auto_fetch.py "Company Name"

NOTE: scraping selectors are correct as of writing but WILL need occasional
maintenance when source sites change layout. Each step degrades gracefully —
anything not found falls back to the historical median and is reported in
`missing` so you know what the model guessed.
"""
import re
import sys
import json
import pathlib
import requests
from difflib import SequenceMatcher
from bs4 import BeautifulSoup

ROOT = pathlib.Path(__file__).resolve().parents[1]
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}


# ------------------------------------------------------------------ helpers
def _get(url, **kw):
    r = requests.get(url, headers=HEADERS, timeout=30, **kw)
    r.raise_for_status()
    return r

def _num(s):
    """'1,234.5 Cr' / '45.2x' / '12%' -> float"""
    if s is None:
        return None
    m = re.search(r"-?[\d,]+\.?\d*", str(s))
    return float(m.group().replace(",", "")) if m else None


# -------------------------------------------------- 1. find IPO detail page
def _fuzzy_score(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def find_ipo_page(name: str) -> str | None:
    """Search Chittorgarh's IPO list for a matching company.
    Uses fuzzy matching so minor typos still resolve correctly."""
    name_lower = name.lower().strip()
    for url in [
        "https://www.chittorgarh.com/ipo/ipo_dashboard.asp",
        "https://www.chittorgarh.com/report/latest-ipo-in-india-list-mainboard/82/",
    ]:
        try:
            soup = BeautifulSoup(_get(url).text, "html.parser")
        except Exception:
            continue

        candidates = []
        for a in soup.find_all("a", href=True):
            if "/ipo/" not in a["href"]:
                continue
            text = a.get_text(strip=True)
            text_lower = text.lower()
            # exact substring match — highest priority
            if name_lower in text_lower:
                href = a["href"]
                return href if href.startswith("http") else "https://www.chittorgarh.com" + href
            # fuzzy score
            score = _fuzzy_score(name_lower, text_lower)
            # also check if all words of the query appear (handles word-order typos)
            words_match = sum(1 for w in name_lower.split() if w in text_lower)
            candidates.append((score, words_match, a["href"], text))

        if candidates:
            candidates.sort(key=lambda x: (x[1], x[0]), reverse=True)
            best_score, best_words, best_href, best_text = candidates[0]
            if best_score >= 0.6 or best_words >= max(1, len(name_lower.split()) - 1):
                print(f"  Fuzzy match: '{best_text}' (score={best_score:.2f})")
                return best_href if best_href.startswith("http") else "https://www.chittorgarh.com" + best_href
    return None


# ----------------------------------------- 2-3. scrape issue data + financials
def scrape_ipo_details(page_url: str) -> dict:
    soup = BeautifulSoup(_get(page_url).text, "html.parser")
    raw = {}

    # key-value tables ("Issue Size", "Fresh Issue", "OFS", "Price Band"...)
    for tr in soup.select("table tr"):
        tds = [td.get_text(" ", strip=True) for td in tr.find_all(["td", "th"])]
        if len(tds) == 2:
            raw[tds[0].lower()] = tds[1]

    out = {}
    fresh = _num(next((v for k, v in raw.items() if "fresh issue" in k), None))
    ofs   = _num(next((v for k, v in raw.items() if "offer for sale" in k or k.strip() == "ofs"), None))
    total = _num(next((v for k, v in raw.items() if "issue size" in k or "total issue" in k), None))
    if ofs is not None and (total or (fresh is not None)):
        denom = total if total else (fresh + ofs)
        if denom:
            out["ofs_pct"] = round(ofs / denom, 3)
    if total:
        out["issue_size_cr"] = total

    # financials table: rows like Revenue / PAT / Total Borrowing across 3 FYs
    fin = {}
    for tbl in soup.find_all("table"):
        head = tbl.get_text(" ", strip=True).lower()
        if "revenue" in head and ("profit" in head or "pat" in head):
            for tr in tbl.find_all("tr"):
                cells = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
                if len(cells) >= 3:
                    fin[cells[0].lower()] = [_num(c) for c in cells[1:]]
            break

    def series(*keys):
        for k, v in fin.items():
            if any(key in k for key in keys):
                vals = [x for x in v if x is not None]
                return vals
        return []

    rev = series("revenue", "income")
    pat = series("profit after tax", "pat", "net profit")
    debt = series("borrowing", "debt")
    networth = series("net worth", "networth", "equity")

    if len(rev) >= 2 and rev[-1]:
        years = len(rev) - 1
        if rev[-1] > 0 and rev[0] > 0:
            out["revenue_cagr_3y"] = round((rev[0] / rev[-1]) ** (1 / years) - 1, 3)
    if rev and pat and rev[0]:
        out["pat_margin"] = round(pat[0] / rev[0], 3)
    if len(pat) >= 2 and rev and rev[0] and len(rev) >= 2 and rev[1]:
        out["pat_margin_trend"] = round(pat[0]/rev[0] - pat[1]/rev[1], 3)
    if debt and networth and networth[0]:
        out["debt_equity"] = round(debt[0] / networth[0], 3)
    if pat and networth and networth[0]:
        out["roe"] = round(pat[0] / networth[0], 3)

    # company "about" paragraph(s) — skip admin boilerplate (lead managers, registrars etc.)
    SKIP_WORDS = ["book running", "lead manager", "registrar", "market maker",
                  "sebi registration", "demat", "escrow", "syndicate member"]
    about = ""
    for p in soup.find_all("p"):
        t = p.get_text(" ", strip=True)
        if len(t) < 150:
            continue
        if any(w in t.lower() for w in SKIP_WORDS):
            continue
        if any(w in t.lower() for w in ["incorporated", "company", "business",
                                         "engaged", "manufacture", "provide",
                                         "operate", "founded", "established"]):
            about += t + "\n\n"
            if len(about) > 1200:
                break

    # DRHP link if present
    drhp = next((a["href"] for a in soup.find_all("a", href=True)
                 if "drhp" in a.get_text(strip=True).lower()
                 or "sebi.gov.in" in a["href"]), None)
    return out, drhp, about.strip()


# ------------------------------------------------------------ 4. GMP + subs
def scrape_gmp(name: str) -> dict:
    out = {}
    try:
        soup = BeautifulSoup(
            _get("https://www.investorgain.com/report/live-ipo-gmp/331/").text,
            "html.parser")
        for tr in soup.select("table tbody tr"):
            tds = [td.get_text(strip=True) for td in tr.find_all("td")]
            if tds and name.lower()[:10] in tds[0].lower():
                gmp = _num(tds[2]) if len(tds) > 2 else None
                price = _num(tds[1]) if len(tds) > 1 else None
                if gmp is not None and price:
                    out["gmp_pct"] = round(gmp / price, 3)
                break
    except Exception:
        pass
    return out

def scrape_subscription(page_url: str) -> dict:
    """Subscription table on the same Chittorgarh page (live during bidding)."""
    out = {}
    try:
        soup = BeautifulSoup(_get(page_url).text, "html.parser")
        for tr in soup.select("table tr"):
            tds = [td.get_text(strip=True) for td in tr.find_all("td")]
            if len(tds) >= 2:
                k = tds[0].lower()
                if "qib" in k:
                    out["qib_subscription"] = _num(tds[-1])
                elif "nii" in k or "hni" in k:
                    out["hni_subscription"] = _num(tds[-1])
                elif "retail" in k:
                    out["retail_subscription"] = _num(tds[-1])
    except Exception:
        pass
    return {k: v for k, v in out.items() if v is not None}


# --------------------------------------------------------- 5. LLM on DRHP
def llm_scores(drhp_url: str) -> dict:
    """Downloads the DRHP, extracts sections, runs the 3 Claude prompt chains.
    Skipped silently if ANTHROPIC_API_KEY isn't set."""
    import tempfile
    sys.path.insert(0, str(ROOT))
    from llm.client import provider
    if not provider() or not drhp_url:
        return {}
    try:
        sys.path.insert(0, str(ROOT))
        from scrapers.scrape_all import extract_drhp_sections
        from llm.drhp_analyzer import analyse_drhp
        pdf = tempfile.mktemp(suffix=".pdf")
        pathlib.Path(pdf).write_bytes(_get(drhp_url).content)
        sections = extract_drhp_sections(pdf)
        res = analyse_drhp(sections)
        return {k: v for k, v in {
            "governance_score": res.get("governance_score"),
            "rpt_intensity": res.get("rpt_intensity"),
            "risk_factor_severity": res.get("risk_factor_severity"),
            "gcp_pct": res.get("gcp_pct"),
        }.items() if v is not None}
    except Exception as e:
        print(f"  LLM step skipped: {e}")
        return {}


# ------------------------------------------------------------------ 6. main
def fetch_features(name: str) -> dict:
    print(f"Searching for '{name}'...")
    page = find_ipo_page(name)
    if not page:
        raise SystemExit(
            f"Could not find '{name}' on the IPO trackers. Check spelling, or the "
            "IPO may not be listed yet. You can still analyse it manually in the app.")
    print(f"  Found: {page}")

    features, drhp_url, about = scrape_ipo_details(page)
    print(f"  Issue + financials: {len(features)} features extracted")
    features.update(scrape_gmp(name))
    features.update(scrape_subscription(page))
    features.update(llm_scores(drhp_url))

    # market regime: trailing 3-month Nifty direction via NSE (best effort)
    try:
        import datetime as dt
        s = requests.Session(); s.headers.update(HEADERS)
        s.get("https://www.nseindia.com", timeout=20)
        r = s.get("https://www.nseindia.com/api/allIndices", timeout=20).json()
        nifty = next(i for i in r["data"] if i["index"] == "NIFTY 50")
        features["bull_regime"] = int(float(nifty.get("perChange365d", 0)) > 0)
    except Exception:
        pass

    return features, page, about


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT))
    name = " ".join(sys.argv[1:]) or input("IPO company name: ")
    features, page, about = fetch_features(name)

    from pipeline.analyze import IPOAnalyzer
    A = IPOAnalyzer()
    missing = [f for f in A.feats if f not in features]
    print(f"\nFetched {len(features)} features; {len(missing)} fell back to historical medians:")
    print("  " + ", ".join(missing[:12]) + ("..." if len(missing) > 12 else ""))

    result = A.analyze(features, name)
    result["fetched_features"] = features
    result["features_defaulted_to_median"] = missing

    from pipeline.explainer import explain
    ex = explain(name, result, features, about)
    print("\n--- ABOUT ---\n" + ex["about"])
    print("\n--- WHY " + result["verdict"] + " (simple language) ---\n" + ex["explanation"])
    print("\n" + json.dumps({k: result[k] for k in
          ["company", "verdict", "confidence_pct", "red_flags"]}, indent=2))

    from reports.report_generator import generate_report
    out = ROOT / "artifacts" / f"{re.sub(r'\\W+','_',name)}_report.pdf"
    generate_report(result, str(out))
    print(f"\nFull PDF report: {out}")
