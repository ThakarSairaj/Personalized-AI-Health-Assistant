'''
services\medical_report_parser.py
This file takes the unstructured text data from the `pdf_text_extractor` and gives output in the structured format which can be
stored in the database further

'''

import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)


def send_text_to_llm(raw_text: str) -> dict:
    """
    Sends extracted PDF text to Gemini 2.5 Flash via OpenRouter
    and returns structured JSON output.
    """

    system_prompt = """
You are a medical laboratory report parser.

Extract structured lab data and return ONLY valid JSON.
Do not include markdown, explanation, or extra text.
"""

    user_prompt = f"""
Extract:

1. Patient details (name, age, gender, report date).
2. All laboratory tests with numeric values.

For each test return:
- test_name
- value
- unit
- reference_range
- status (Normal / High / Low)

Rules:
- Ignore doctor names.
- Ignore explanations.
- If 'H' before value → High.
- If 'L' before value → Low.
- Otherwise determine from reference range.

Return strictly in this JSON format:

{{
  "patient_info": {{
    "name": "",
    "age": "",
    "gender": "",
    "report_date": ""
  }},
  "lab_results": []
}}

Medical Report Text:
{raw_text}
"""

    response = client.chat.completions.create(
        model="google/gemini-2.5-flash",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0,
        max_tokens=1200,
        response_format={"type": "json_object"},
        extra_headers={
            "HTTP-Referer": "http://localhost",
            "X-Title": "AI Health Assistant"
        }
    )

    content = response.choices[0].message.content.strip()
    print("===== LLM RAW OUTPUT =====")
    print(content)
    print("===========================")
    try:
        return json.loads(content)
    except Exception:
        raise ValueError("LLM did not return valid JSON")
