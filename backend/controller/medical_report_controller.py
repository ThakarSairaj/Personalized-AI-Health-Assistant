from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated

from database_con.database import session
from models.models import MedicalReport, User
from schemas.medical_report import CreateMedicalReport

from fastapi.responses import StreamingResponse
from services.pdf_services import generate_medical_report_pdf


router = APIRouter()


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.post(
    "/users/{user_id}/medical-report/",
    status_code=status.HTTP_201_CREATED
)
def create_medical_report(
    user_id: int,
    report: CreateMedicalReport,
    db: db_dependency
):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    new_report = MedicalReport(
        user_id=user_id,
        chief_complaint=report.chief_complaint,
        symptoms=report.symptoms,
        duration=report.duration,
        onset_type=report.onset_type,
        progression=report.progression,
        severity=report.severity
    )

    db.add(new_report)
    db.commit()
    db.refresh(new_report)

    return {
        "message": "Medical report created successfully",
        "report_id": new_report.report_id
    }


@router.get("/medical-report/{report_id}/pdf")
def download_medical_report_pdf(report_id: int, db: db_dependency):
    report = db.query(MedicalReport).filter(
        MedicalReport.report_id == report_id
    ).first()

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    user = db.query(User).filter(User.user_id == report.user_id).first()

    pdf_buffer = generate_medical_report_pdf(user, report)

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=medical_report_{report_id}.pdf"
        },
    )