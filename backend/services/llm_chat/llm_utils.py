'''
Docstring for llm_utils
call the llm via openrouter, pass the information of the user and receives the output in the structured format
'''

import re
import json
import requests
from .module2_1 import KbManager


# =====================================================
# 🔐 OPENROUTER CONFIGURATION
# =====================================================

OPENROUTER_API_KEY = "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"

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

MODEL_NAME = "google/gemini-2.5-flash"  
# You can also try:
# "deepseek/deepseek-chat"
# "mistralai/mistral-7b-instruct"

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost",
    "X-Title": "Medical Assistant"
}

# =====================================================
# EMOJI REMOVER
# =====================================================

_EMOJI_PATTERN = re.compile(
    "[" 
    "\U0001F1E0-\U0001F1FF"
    "\U0001F300-\U0001F5FF"
    "\U0001F600-\U0001F64F"
    "\U0001F680-\U0001F6FF"
    "\U0001F700-\U0001F77F"
    "\U0001F780-\U0001F7FF"
    "\U0001F800-\U0001F8FF"
    "\U0001F900-\U0001F9FF"
    "\U0001FA00-\U0001FA6F"
    "\U0001FA70-\U0001FAFF"
    "\U00002702-\U000027B0"
    "\U000024C2-\U0001F251"
    "]+",
    flags=re.UNICODE,
)

def remove_emoji(text: str) -> str:
    return _EMOJI_PATTERN.sub("", text or "")

# =====================================================
# OPENROUTER CALLER
# =====================================================

def _call_llm_api(system_prompt: str, user_prompt: str) -> str:
    try:
        payload = {
    "model": MODEL_NAME,
    "messages": [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    "temperature": 0.3,
    "max_tokens": 500
}


        response = requests.post(OPENROUTER_URL, headers=HEADERS, json=payload)

        if response.status_code != 200:
            print("OpenRouter Error:", response.text)
            return "Error in API call."

        result = response.json()
        return result["choices"][0]["message"]["content"].strip()

    except Exception as e:
        print("OpenRouter Exception:", e)
        return "Error in API call."

# =====================================================
# UNIFIED CONVERSATIONAL ENGINE
# =====================================================

def generate_medical_response(
    initial_query: str,
    conversation_context: str,
    user_id: str,
    kb_manager: KbManager
):

    kb_results = kb_manager.semantic_search(user_id, initial_query, top_k=3)
    kb_context = "\n".join(
        f"- {item['document']}" for item in kb_results
    ) if kb_results else ""

    system_prompt = """
You are a medical triage assistant.
You MUST respond ONLY with valid JSON.
No explanations.
No markdown.
No extra text.
Return exactly one JSON object.
"""

    user_prompt = f"""
Conversation so far:
{conversation_context}

Relevant patient background:
{kb_context}

Initial query:
{initial_query}

INSTRUCTIONS:

1. If user changed topic away from medical issue:
{{ "type": "reset", "content": "It seems you changed topic. Let's focus on your medical concern." }}

2. If more information is needed:
{{ "type": "question", "content": "Your clarifying question here?" }}

3. If sufficient information:
{{ "type": "final", "content": "Two paragraphs medical advice here." }}

If giving final:
- EXACTLY 2 paragraphs
- Each paragraph 3–4 sentences
- No bullet points
"""

    raw = _call_llm_api(system_prompt, user_prompt)
    cleaned = remove_emoji(raw.strip())

    print("RAW LLM RESPONSE:\n", raw)

    try:
        start = cleaned.find("{")
        end = cleaned.rfind("}") + 1
        json_text = cleaned[start:end]
        return json.loads(json_text)
    except Exception:
        return {
            "type": "final",
            "content": "I'm sorry, I couldn't process that properly. Please try again."
        }
