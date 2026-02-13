'''
backend\services\report_analysis_service.py
Description: Service layer for analyzing patient lab history. 
Aggregates database records and utilizes LLM reasoning to answer 
user inquiries regarding health trends and report status.
'''
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from models.models import ExtractedLabResult
from services.report_llm_service import generate_report_explanation

import re


def analyze_report_question(
    db: Session,
    user_id: int,
    question: str
):
    if not question:
        return "Please provide a valid question."

    # Fetch ALL lab data for that user
    results = db.query(ExtractedLabResult)\
        .filter(ExtractedLabResult.user_id == user_id)\
        .order_by(ExtractedLabResult.test_date.asc())\
        .all()

    if not results:
        return "No lab records found."

    # Build full structured history
    summary_text = "Complete Lab History:\n\n"

    for r in results:
        summary_text += (
            f"{r.test_date} | "
            f"{r.test_name}: {r.test_value} "
            f"(Reference: {r.reference_range}) "
            f"Status: {r.status}\n"
        )

    # Let LLM reason freely
    llm_prompt = f"""
User question:
{question}

Here is the patient's complete lab history:

{summary_text}

Analyze intelligently and answer clearly in simple medical language.

If typo exists in test name, infer correct one.
If overall question, summarize entire health profile.
If specific test, focus on that.
Explain trends, abnormalities, and possible implications.
"""

    response = generate_report_explanation(llm_prompt)

    return response
