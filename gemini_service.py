"""
gemini_service.py
──────────────────
All AI / backend logic lives here. The frontend (app.py, ui_components.py)
never talks to the Gemini API directly — it only calls functions from
this module. This keeps "backend" and "frontend" cleanly separated.
"""

import json
import re
import google.generativeai as genai

from config import GEMINI_API_KEY, MODEL_NAME

_model = None
_configured_key = None


def configure(api_key: str) -> None:
    """Configure the Gemini client with a given API key."""
    global _model, _configured_key
    if api_key and api_key != _configured_key:
        genai.configure(api_key=api_key)
        _model = genai.GenerativeModel(MODEL_NAME)
        _configured_key = api_key


def is_configured() -> bool:
    return _model is not None


def _ensure_ready(api_key: str) -> bool:
    """Make sure the model is configured, using .env key or provided key."""
    key_to_use = api_key or GEMINI_API_KEY
    if not key_to_use:
        return False
    configure(key_to_use)
    return True


def _generate(prompt: str, api_key: str = "") -> str:
    """Low-level call to Gemini. Returns text or an error message."""
    if not _ensure_ready(api_key):
        return "⚠️ No API key found. Add GEMINI_API_KEY to your .env file, or enter it in the sidebar."
    try:
        response = _model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Error calling Gemini API: {str(e)}"


# ── Public service functions (one per feature) ─────────────────────────────

def explain_concept(topic: str, level: str, include_example: bool, include_analogy: bool, api_key: str = "") -> str:
    """Concept Explainer service."""
    extras = []
    if include_example:
        extras.append("a real-world example")
    if include_analogy:
        extras.append("a simple analogy")
    extra_str = f"Also include {' and '.join(extras)}." if extras else ""

    prompt = f"""You are an expert educator. Explain the concept of "{topic}" at a {level} level.
Structure your response as:
1. **What is it?** – A clear 2-3 sentence definition.
2. **How it works** – Key points in bullet form (4-6 bullets).
3. **Why it matters** – A brief paragraph on real-world importance.
{extra_str}
Keep the language appropriate for the {level} level. Be concise yet thorough."""

    return _generate(prompt, api_key)


def summarize_notes(notes: str, style: str, extras_selected: list, api_key: str = "") -> str:
    """Notes Summarizer service."""
    style_map = {
        "Concise (bullet points)": "a concise bullet-point summary with 6-10 key points",
        "Detailed (paragraphs)": "a detailed paragraph summary covering all major topics",
        "Key terms + definitions": "a list of key terms with their definitions",
    }
    extras_str = f"\n\nAlso extract: {', '.join(extras_selected)}." if extras_selected else ""

    prompt = f"""You are a study assistant. Summarize the following notes as {style_map[style]}.

Structure your response:
1. **📌 Topic Overview** – What subject/topic are these notes about? (1-2 sentences)
2. **🔑 Summary** – The main summary in the chosen style.
3. **⭐ Most Important Point** – The single most critical takeaway.
{extras_str}

Notes to summarize:
---
{notes}
---"""

    return _generate(prompt, api_key)


def generate_quiz(source_text: str, is_topic: bool, num_questions: int, difficulty: str, api_key: str = ""):
    """
    Quiz Generator service.
    Returns a tuple: (questions_list_or_None, raw_text_if_parse_failed_or_None)
    """
    source_desc = f"the topic: {source_text}" if is_topic else f"these notes:\n{source_text}"

    prompt = f"""Generate {num_questions} multiple choice questions (MCQs) about {source_desc}.
Difficulty: {difficulty}

Return ONLY a valid JSON array. No extra text, no markdown fences.
Format:
[
  {{
    "question": "Question text here?",
    "options": ["A) Option1", "B) Option2", "C) Option3", "D) Option4"],
    "answer": "A) Option1",
    "explanation": "Brief explanation of why this is correct."
  }}
]"""

    raw = _generate(prompt, api_key)

    try:
        clean = re.sub(r"```(?:json)?|```", "", raw).strip()
        questions = json.loads(clean)
        return questions, None
    except Exception:
        return None, raw
