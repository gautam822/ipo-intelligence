"""
Production scrapers — run these on your own machine (internet required).
1. SEBI DRHP scraper  : downloads DRHP PDFs from SEBI public filings page
2. NSE IPO data       : subscription figures, listing prices
3. GMP scraper        : grey market premium from public tracker sites
4. DRHP text extractor: pdfplumber-based section extraction

Usage:
    python scrapers/scrape_all.py --from-year 2014
"""
import io
import re
import time
import json
import pathlib
import requests
import pdfplumber
import pandas as pd
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (research; contact: you@example.com)"}
RAW_DIR = pathlib.Path("data/raw_drhp"); RAW_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------- SEBI DRHP
def list_sebi_drhps(from_year=2014):
    """SEBI public-issues page lists DRHP/RHP filings with PDF links."""
    url = "https://www.sebi.gov.in/sebiweb/home/HomeAction.do?doListing=yes&sid=3&ssid=15&smid=10"
    out, page = [], 1
    while True:
        r = requests.get(url, params={"pageno": page}, headers=HEADERS, timeout=30)
        soup = BeautifulSoup(r.text, "html.parser")
        rows = soup.select("table tr")
        if len(rows) <= 1:
            break
        for tr in rows[1:]:
            tds = tr.find_all("td")
            if len(tds) < 2:
                continue
            date, title = tds[0].get_text(strip=True), tds[1].get_text(strip=True)
            link = tds[1].find("a")
            if link and int(date[-4:]) >= from_year:
                out.append({"date": date, "company": title, "url": link["href"]})
        page += 1
        time.sleep(1.0)                      # be polite — do not hammer SEBI
    return pd.DataFrame(out)


def download_drhp(row, dest=RAW_DIR):
    fn = dest / (re.sub(r"\W+", "_", row["company"])[:80] + ".pdf")
    if fn.exists():
        return fn
    r = requests.get(row["url"], headers=HEADERS, timeout=60)
    fn.write_bytes(r.content)
    time.sleep(0.5)
    return fn


# ------------------------------------------------------ DRHP text extraction
SECTION_PATTERNS = {
    "risk_factors":      r"RISK FACTORS(.*?)(?:THE ISSUE|SUMMARY OF)",
    "objects_of_issue":  r"OBJECTS OF THE (?:ISSUE|OFFER)(.*?)(?:BASIS FOR|STATEMENT OF)",
    "promoters":         r"OUR PROMOTERS?(.*?)(?:OUR GROUP|DIVIDEND POLICY)",
    "litigation":        r"OUTSTANDING LITIGATION(.*?)(?:GOVERNMENT|OTHER REGULATORY)",
    "rpt":               r"RELATED PARTY TRANSACTIONS(.*?)(?:FINANCIAL INDEBTEDNESS|CAPITALISATION)",
}

def extract_drhp_sections(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join((p.extract_text() or "") for p in pdf.pages)
    sections = {}
    for name, pat in SECTION_PATTERNS.items():
        m = re.search(pat, text, re.S | re.I)
        sections[name] = m.group(1)[:50000] if m else ""
    return sections


# ----------------------------------------------------------------- NSE data
def nse_session():
    s = requests.Session()
    s.headers.update(HEADERS)
    s.get("https://www.nseindia.com", timeout=30)     # sets cookies
    return s

def nse_ipo_subscription(symbol):
    s = nse_session()
    r = s.get(f"https://www.nseindia.com/api/ipo-active-category?symbol={symbol}", timeout=30)
    return r.json()

def nse_historical_price(symbol, from_date, to_date):
    s = nse_session()
    r = s.get("https://www.nseindia.com/api/historical/cm/equity",
              params={"symbol": symbol, "from": from_date, "to": to_date}, timeout=30)
    return pd.DataFrame(r.json().get("data", []))


# ----------------------------------------------------------------- GMP
def scrape_gmp():
    """Grey market premium from a public tracker (structure changes often —
    inspect the page and adjust selectors)."""
    r = requests.get("https://www.investorgain.com/report/live-ipo-gmp/331/", headers=HEADERS, timeout=30)
    soup = BeautifulSoup(r.text, "html.parser")
    rows = []
    for tr in soup.select("table tbody tr"):
        tds = [td.get_text(strip=True) for td in tr.find_all("td")]
        if len(tds) >= 4:
            rows.append({"company": tds[0], "gmp": tds[2], "est_listing": tds[3]})
    return pd.DataFrame(rows)


if __name__ == "__main__":
    print("Listing SEBI DRHPs...")
    df = list_sebi_drhps()
    df.to_csv("data/drhp_index.csv", index=False)
    print(f"{len(df)} filings indexed. Downloading PDFs...")
    for _, row in df.iterrows():
        try:
            download_drhp(row)
        except Exception as e:
            print("skip", row["company"], e)
