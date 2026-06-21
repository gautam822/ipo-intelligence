"""
Plain-language explainer.

Turns the analysis dict into:
  1. about      : short brief on the company (scraped, optionally LLM-polished)
  2. explanation: 'why invest / why avoid' written for a non-finance reader

Works in two modes:
  - LLM mode (ANTHROPIC_API_KEY set): Claude writes a natural, simple summary
  - Offline mode (no key): template engine translates features into plain English

Both modes are honest about data coverage — if most features were defaulted
to medians, the explanation says so clearly.
"""
import os

# feature -> (plain-English good phrasing, bad phrasing, threshold direction)
PLAIN = {
    "ofs_pct": ("most of the money raised goes INTO the company to grow it",
                "a big part of this IPO is existing owners selling their own shares and taking the money home — the company itself gets little of it"),
    "ocf_pat_ratio": ("the company's profits are backed by real cash coming in",
                      "the company shows profits on paper, but much less actual cash is coming in — a classic warning sign"),
    "debt_equity": ("the company has very little debt",
                    "the company carries heavy loans, which makes it risky if business slows down"),
    "roce": ("the company earns strong returns on the money it uses",
             "the company earns weak returns on the money it uses — it's not putting capital to good use"),
    "revenue_cagr_3y": ("sales have been growing at a healthy pace",
                        "sales growth has been slow or shrinking"),
    "pat_margin": ("the company keeps a good share of every rupee of sales as profit",
                   "profit margins are thin — small problems can wipe out earnings"),
    "pe_vs_peer_median": ("the IPO is priced reasonably compared to similar listed companies",
                          "the IPO is priced expensive compared to similar listed companies — you'd be paying a premium"),
    "qib_subscription": ("big institutional investors (mutual funds, banks) are buying heavily — smart money likes it",
                         "big institutional investors are showing little interest — smart money is staying away"),
    "gmp_pct": ("the unofficial grey market is paying a premium, showing strong demand",
                "the grey market shows weak or no premium — demand looks lukewarm"),
    "promoter_pledge_flag": ("promoters have not pledged their shares",
                             "promoters have pledged their shares as loan collateral — if the stock falls, lenders can force-sell, crashing it further"),
    "governance_score": ("the company's management and governance look clean",
                         "there are governance concerns around how the company is run"),
    "gcp_pct": ("the company clearly explains where IPO money will go",
                "a large chunk of the IPO money is for vague 'general purposes' — we don't know where it will actually go"),
    "auditor_qualified": ("auditors signed off the accounts without objections",
                          "auditors raised objections about the accounts — a serious red flag"),
}
GOOD_IF_HIGH = {"ocf_pat_ratio", "roce", "revenue_cagr_3y", "pat_margin",
                "qib_subscription", "gmp_pct", "governance_score"}


def _offline_about(company, fetched):
    size = fetched.get("issue_size_cr")
    bits = [f"**{company}** is coming out with an IPO"]
    if size:
        bits.append(f"to raise about ₹{size:,.0f} crore")
    ofs = fetched.get("ofs_pct")
    if ofs is not None:
        bits.append(f"of which roughly {ofs:.0%} is existing shareholders selling their stake"
                    if ofs > 0.3 else "mostly as fresh money going into the company")
    return " ".join(bits) + "."


def _offline_explanation(analysis, fetched):
    verdict = analysis["verdict"]
    drivers = analysis["top_drivers"]
    n_fetched = len(fetched)
    n_total = 35

    lines = []
    # honesty first
    if n_fetched < 12:
        lines.append(
            f"⚠️ **Important:** we could only find {n_fetched} out of {n_total} data points "
            f"for this company (the rest were filled with typical-IPO averages). So treat this "
            f"verdict as a rough first look, not a final answer. More data usually becomes "
            f"available closer to the IPO date.")

    # --- insufficient data guard ---
    if n_fetched < 8:
        lines.append(
            "**Honestly, we don't have enough data to give a real verdict yet.** "
            "With only " + str(n_fetched) + " data points found, the system is mostly "
            "guessing using typical-IPO averages. The AVOID/INVEST label above should "
            "be ignored until more data is available.\n\n"
            "**What to do:** wait until the IPO subscription opens (usually 2–3 days "
            "before listing) — by then QIB/HNI subscription numbers, GMP, and financials "
            "from the DRHP will be available. Search again then for a meaningful result.")
        return "\n\n".join(lines)

    opener = {
        "INVEST": "**In simple words — this IPO looks worth considering.** Here's why:",
        "AVOID":  "**In simple words — this IPO looks risky, better to skip it.** Here's why:",
        "NEUTRAL":"**In simple words — this IPO is a mixed bag, neither clearly good nor bad.** Here's why:",
    }[verdict]
    lines.append(opener)

    # translate top drivers into plain sentences — ONLY for features we actually
    # fetched; and only where the plain-English direction MATCHES the verdict.
    used = 0
    for d in drivers:
        feat = d["feature"]
        if feat not in PLAIN or feat not in fetched or used >= 4:
            continue
        val = fetched[feat]
        # determine if this feature value is "good" or "bad" for investment
        if feat in GOOD_IF_HIGH:
            is_good = val > 0
        else:
            is_good = val < 0.5 if feat in {"ofs_pct","gcp_pct","rpt_intensity"} else val < 1
        # only include the sentence if it actually supports the verdict direction
        if verdict == "INVEST" and not is_good:
            continue
        if verdict == "AVOID" and is_good:
            continue
        sentence = PLAIN[feat][0] if is_good else PLAIN[feat][1]
        lines.append(f"- {sentence.capitalize()}.")
        used += 1

    if used == 0:
        lines.append(
            "- The main signals we found are mixed or inconclusive. "
            "The verdict is based on the overall pattern vs historical IPOs, "
            "but we recommend waiting for subscription data before acting.")

    # red flags in plain words
    flags = [f for f in analysis["red_flags"] if not f.startswith("No major")]
    if flags:
        lines.append("**Watch out for:**")
        for f in flags[:4]:
            lines.append(f"- {f}")

    conf = analysis["confidence_pct"]
    lines.append(
        f"The system is **{conf}% confident** in this call — meaning that historically, "
        f"when it saw a similar pattern, it was right about {conf:.0f} times out of 100. "
        f"It can still be wrong. This is information, not investment advice.")
    return "\n\n".join(lines)


def _llm_explain(company, analysis, fetched, about_text=""):
    import json
    from llm.client import ask_json
    return ask_json(
        ("You explain IPO analyses to people with zero finance knowledge. "
         "Use very simple language, short sentences, everyday analogies. No jargon "
         "without explaining it. Be honest about uncertainty. Never promise returns. "
         'Return JSON: {"about": "2-3 sentence company brief", '
         '"explanation": "simple markdown explanation of the verdict, 120-200 words"}'),
        f"Company: {company}\nScraped about-text: {about_text[:2000]}\n"
        f"Analysis: {json.dumps({k: analysis[k] for k in ['verdict','confidence_pct','top_drivers','red_flags','pillar_scores']})}\n"
        f"Features actually fetched ({len(fetched)}/35): {json.dumps(fetched)}\n"
        "If fewer than 12 features were fetched, clearly warn that data is limited.")


def explain(company, analysis, fetched, about_text=""):
    """Returns {'about': str, 'explanation': str}. LLM if any key set, else offline."""
    from llm.client import provider
    if provider():
        try:
            return _llm_explain(company, analysis, fetched, about_text)
        except Exception:
            pass
    return {"about": about_text.strip() or _offline_about(company, fetched),
            "explanation": _offline_explanation(analysis, fetched)}
