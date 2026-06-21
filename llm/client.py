"""
Provider-agnostic LLM client. Auto-detects whichever API key is set:

  ANTHROPIC_API_KEY  -> Claude  (paid, best quality)
  GEMINI_API_KEY     -> Google Gemini Flash (FREE: 1,500 req/day, aistudio.google.com)
  GROQ_API_KEY       -> Groq Llama 70B      (FREE: 1,000 req/day, console.groq.com)

All three are called via plain HTTPS (requests) — no extra SDKs needed.
ask_json(system, user) -> dict parsed from the model's JSON reply.
"""
import os
import json
import requests


def _strip(raw: str) -> dict:
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        raw = raw[4:] if raw.startswith("json") else raw
    # tolerate leading/trailing prose around the JSON object
    start, end = raw.find("{"), raw.rfind("}")
    return json.loads(raw[start:end + 1])


def _anthropic(system, user):
    r = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={"x-api-key": os.environ["ANTHROPIC_API_KEY"],
                 "anthropic-version": "2023-06-01",
                 "content-type": "application/json"},
        json={"model": "claude-sonnet-4-20250514", "max_tokens": 1200,
              "system": system,
              "messages": [{"role": "user", "content": user}]},
        timeout=120)
    r.raise_for_status()
    return "".join(b.get("text", "") for b in r.json()["content"])


def _gemini(system, user):
    r = requests.post(
        "https://generativelanguage.googleapis.com/v1beta/models/"
        "gemini-2.5-flash:generateContent",
        params={"key": os.environ["GEMINI_API_KEY"]},
        json={"system_instruction": {"parts": [{"text": system}]},
              "contents": [{"parts": [{"text": user}]}],
              "generationConfig": {"maxOutputTokens": 1200}},
        timeout=120)
    r.raise_for_status()
    return r.json()["candidates"][0]["content"]["parts"][0]["text"]


def _groq(system, user):
    r = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {os.environ['GROQ_API_KEY']}"},
        json={"model": "llama-3.3-70b-versatile", "max_tokens": 1200,
              "messages": [{"role": "system", "content": system},
                           {"role": "user", "content": user}]},
        timeout=120)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]


def provider() -> str | None:
    if os.environ.get("ANTHROPIC_API_KEY"):
        return "anthropic"
    if os.environ.get("GEMINI_API_KEY"):
        return "gemini"
    if os.environ.get("GROQ_API_KEY"):
        return "groq"
    return None


def ask_json(system: str, user: str) -> dict:
    """Route to whichever provider has a key. Raises RuntimeError if none."""
    p = provider()
    if p is None:
        raise RuntimeError(
            "No LLM key found. Set one of: GEMINI_API_KEY (free, aistudio.google.com), "
            "GROQ_API_KEY (free, console.groq.com), or ANTHROPIC_API_KEY.")
    system = system + " Respond ONLY with valid JSON, no markdown fences, no extra text."
    fn = {"anthropic": _anthropic, "gemini": _gemini, "groq": _groq}[p]
    return _strip(fn(system, user))
