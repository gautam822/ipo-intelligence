"""
LLM-based DRHP analyser — 3 structured prompt chains.
Works with ANY of: ANTHROPIC_API_KEY (paid), GEMINI_API_KEY (free),
GROQ_API_KEY (free). See llm/client.py.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from llm.client import ask_json


def analyse_risk_factors(risk_text):
    return ask_json(
        "You are an IPO analyst. Read these DRHP risk factors. Ignore boilerplate. "
        'Return JSON: {"top_risks":[{"risk":str,"severity":1-5}], "risk_factor_severity": 1-10}',
        risk_text[:100000])

def analyse_objects(objects_text):
    return ask_json(
        "Analyse use of IPO proceeds. Return JSON: "
        '{"growth_capex_pct":0-1,"debt_repayment_pct":0-1,"gcp_pct":0-1,"gcp_red_flag":bool}',
        objects_text[:60000])

def analyse_governance(promoter_text, rpt_text):
    return ask_json(
        "Assess promoter background, related-party transactions, board independence. "
        'Return JSON: {"governance_score":1-10,"rpt_intensity":0-1,"red_flags":[str]}',
        promoter_text[:60000] + "\n\nRELATED PARTY:\n" + rpt_text[:40000])

def analyse_drhp(sections: dict) -> dict:
    out = {}
    out.update(analyse_objects(sections.get("objects_of_issue", "")))
    out.update(analyse_governance(sections.get("promoters", ""), sections.get("rpt", "")))
    risks = analyse_risk_factors(sections.get("risk_factors", ""))
    out["risk_factor_severity"] = risks.get("risk_factor_severity", 5)
    out["top_risks"] = risks.get("top_risks", [])
    return out
