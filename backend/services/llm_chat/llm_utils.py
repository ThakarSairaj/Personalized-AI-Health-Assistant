'''
Docstring for llm_utils
call the llm via openrouter, pass the information of the user and receives the output in the structured format
'''

import re
import json
import requests
# from .module2_1 import KbManager
import os
from .rag_service import retrieve_similar




# =====================================================
# 🔐 OPENROUTER CONFIGURATION
# =====================================================

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

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
    conversation_context: str,
    user_id: str,
    recurrence_flag: bool
    
):


   # Retrieve only at early stage of conversation
    if conversation_context.count("User:") <= 1:

    # Safely extract the latest USER message
        lines = conversation_context.strip().split("\n")
        latest_user_line = ""

        for line in reversed(lines):
            if line.startswith("User:"):
                latest_user_line = line.replace("User: ", "")
                break

        retrieved_memories = retrieve_similar(
            user_id=user_id,
            query=latest_user_line,
            top_k=3
        )

    else:
        retrieved_memories = []
        
    recurrence_detected = recurrence_flag or (len(retrieved_memories) > 0)
    if retrieved_memories:
        kb_context = "Previous relevant medical records:\n"
        for i, doc in enumerate(retrieved_memories, 1):
            kb_context += f"{i}. {doc}\n"
    else:
        kb_context = "No relevant past medical history."




    system_prompt = """
You are a calm and professional medical doctor conducting a triage conversation.

Conversation style:
- Be natural and conversational.
- Sound like a real doctor, not a checklist.
- Briefly acknowledge patient answers when appropriate.
- Ask one question at a time.
- Keep questions concise but natural.
- Avoid robotic tone.

Clinical behavior:
- Ask relevant follow-up questions logically.
- Do not repeat already answered information.
- Build questions based on previous responses.
- Avoid unnecessary questions.

Memory handling:
- If "Recurrence Detected" is YES,
  you MUST acknowledge that the patient had a similar episode before.
- Mention it in one short natural sentence BEFORE giving the final explanation.
- Do NOT ignore this instruction.
- If "Recurrence Detected" is NO, do not mention past history.

Final response style:
- Use simple, reassuring language.
- Be concise but helpful.
- Do not use medical jargon.
- Provide clear next steps.
- Include when to seek urgent care.
- Mention appropriate doctor type.

You MUST respond ONLY with valid JSON.
No markdown.
No extra text.
Return exactly one JSON object.
"""


    user_prompt = f"""
Conversation so far:
{conversation_context}

Relevant patient background:
{kb_context}

Recurrence Detected: {"YES" if recurrence_detected else "NO"}

INSTRUCTIONS:

1. If user changed topic away from medical issue:
{{ "type": "reset", "content": "It seems you changed topic. Let's focus on your medical concern." }}

2. If more information is needed:
{{ "type": "question", "content": "Short clarifying medical question here." }}

3. If sufficient information:

If Recurrence Detected is YES,
begin the content with ONE short natural sentence acknowledging
that the patient had a similar episode before.

Then continue EXACTLY in this structure:

{{
  "type": "final",
  "content": "
<Optional recurrence sentence if Recurrence Detected is YES>

Possible Cause:
<short and simple condition name>

Why This Might Be It:
<1-2 short simple sentences>

What You Can Do Now:
- <simple safe home remedy>
- <another safe remedy>
- <lifestyle advice>

See a Doctor If:
- <clear warning sign 1>
- <clear warning sign 2>

Doctor Type:
<specialist name in simple terms>"
}}

Rules for final:
- Keep total response under 150 words.
- Use simple and reassuring language.
- Avoid complex medical terms.
- Do not restate symptoms as diagnosis.
- Keep it natural and conversational.
- Be concise.
"""


    raw = _call_llm_api(system_prompt, user_prompt)
    cleaned = remove_emoji(raw.strip())

    print("RAW LLM RESPONSE:\n", raw)

    try:
        start = cleaned.find("{")
        end = cleaned.rfind("}") + 1
        json_text = cleaned[start:end]
        return {
        "response": json.loads(json_text),
        "recurrence_detected": recurrence_detected
        }
    except Exception:
        return {
        "response": {
            "type": "final",
            "content": "I'm sorry, I couldn't process that properly. Please try again."
        },
        "recurrence_detected": recurrence_detected
    }

def extract_condition(text: str) -> str:
    match = re.search(r"Possible Cause:\s*(.+)", text)
    return match.group(1).strip() if match else "Unknown"
