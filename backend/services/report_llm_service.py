'''
backend\services\report_llm_service.py
This service acts as the core interface for LLM communication. 
It handles API connections, model configurations (Gemini), and 
converts structured prompts into natural language medical explanations.
'''
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)


def generate_report_explanation(prompt: str) -> str:
    response = client.chat.completions.create(
        model="google/gemini-2.5-flash",
        messages=[
            {
                "role": "system",
                "content": "You are a medical assistant. Explain lab results clearly in simple, patient-friendly language. Do not return JSON."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=800,
        extra_headers={
            "HTTP-Referer": "http://localhost",
            "X-Title": "AI Health Assistant"
        }
    )

    return response.choices[0].message.content.strip()
