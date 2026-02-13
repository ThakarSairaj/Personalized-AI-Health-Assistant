'''
backend\services\report_storage_service/py
This file is use to store structured data extracted from the pdf report
'''

from sqlalchemy.orm import Session
from models.models import UploadedReport, ExtractedLabResult
from datetime import datetime
import re


def save_report_to_db(
    db: Session,
    user_id: int,
    extracted_json: dict,
):

    try:
        # ----------------------------
        # 1️⃣ Parse Report Date
        # ----------------------------
        report_date_str = (
            extracted_json.get("patient_info", {})
            .get("report_date")
        )

        report_date = _parse_date(report_date_str)

        # ----------------------------
        # 2️⃣ Create Uploaded Report
        # ----------------------------
        new_report = UploadedReport(
            user_id=user_id,
            report_type="lab",
            report_date=report_date,
        )

        db.add(new_report)
        db.flush()  # Get uploaded_report_id

        # ----------------------------
        # 3️⃣ Insert Lab Results
        # ----------------------------
        lab_results = extracted_json.get("lab_results", [])

        if not isinstance(lab_results, list):
            raise ValueError("Invalid lab_results format")

        for test in lab_results:

            test_name = test.get("test_name")

            # Skip invalid or empty rows
            if not test_name:
                continue

            value = _safe_float(test.get("value"))

            status = test.get("status")
            if status:
                status = status.capitalize()

            lab_entry = ExtractedLabResult(
                uploaded_report_id=new_report.uploaded_report_id,
                user_id=user_id,
                test_name=test_name.strip(),
                test_value=value,
                unit=test.get("unit"),
                reference_range=test.get("reference_range"),
                status=status,
                test_date=report_date
            )

            db.add(lab_entry)

        db.commit()
        return new_report.uploaded_report_id

    except Exception as e:
        db.rollback()
        print("DB ERROR:", e)
        raise e


# -------------------------------------------------
# 🔹 Safe Float Conversion (Handles OCR Errors)
# -------------------------------------------------

def _safe_float(value):
    if value is None:
        return None

    value_str = str(value).strip()

    # Fix common OCR mistake: 4-79 → 4.79
    if re.match(r"^\d+-\d+$", value_str):
        value_str = value_str.replace("-", ".")

    # Remove commas (14,500 → 14500)
    value_str = value_str.replace(",", "")

    try:
        return float(value_str)
    except:
        return None


# -------------------------------------------------
# 🔹 Flexible Date Parsing
# -------------------------------------------------

def _parse_date(date_str):
    if not date_str:
        return None

    formats = [
        "%d-%b-%Y",      # 28-Feb-2023
        "%d/%m/%Y",      # 28/02/2023
        "%d-%m-%Y",      # 28-02-2023
        "%Y-%m-%d",      # 2023-02-28
        "%b %d, %Y",     # Feb 28, 2023
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_str.strip(), fmt).date()
        except:
            continue

    return None
