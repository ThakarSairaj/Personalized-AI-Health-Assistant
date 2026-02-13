from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from database_con.database import session
from typing import Annotated

from backend.services.pdf_text_extractor import extract_text_hybrid
from services.medical_report_parser import send_text_to_llm
from services.report_storage_service import save_report_to_db

from core.dependencies import get_current_user
from models.models import User

router = APIRouter()


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/upload-report")
async def upload_report(
    db: db_dependency,
    current_user: User = Depends(get_current_user),
    file: UploadFile = File(...),
):


    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    file_bytes = await file.read()

    raw_text = extract_text_hybrid(file_bytes)

    if not raw_text:
        raise HTTPException(status_code=400, detail="Could not extract text from PDF")

    limited_text = raw_text[:8000]

    try:
        # ✅ Now returns dict directly
        extracted_json = send_text_to_llm(limited_text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    try:
        report_id = save_report_to_db(
            db=db,
            user_id=current_user.user_id,
            extracted_json=extracted_json,
        )

        return {
            "message": "Report stored successfully",
            "report_id": report_id
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )
