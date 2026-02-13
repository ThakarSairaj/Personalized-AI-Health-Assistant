from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from database_con.database import session
from core.dependencies import get_current_user
from models.models import User
from services.report_analysis_service import analyze_report_question
from schemas.health import HealthQuestion



router = APIRouter()


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/ask-health-question")
def ask_health_question(
    payload: HealthQuestion,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    question = payload.question

    if not question:
        raise HTTPException(status_code=400, detail="Question required")

    result = analyze_report_question(
        db,
        current_user.user_id,
        question
    )

    return {"answer": result}
