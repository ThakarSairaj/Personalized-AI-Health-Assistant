# controller/health_basic_details_controller.py

from fastapi import APIRouter, status, Depends, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session
from database_con.database import session
from models.models import User, UserHealthInfo

from schemas.users import CreateUserHealthInfo

router=APIRouter()


def get_db():
    db=session()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session, Depends(get_db)]


@router.post("/addUser/{user_id}/healthDetails/")
def userHealthDetails(
    user_id: int,
    health_info: CreateUserHealthInfo,
    db: db_dependency
    ):

    user=db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User does not exist"
        )

    db_health=UserHealthInfo(
        user_health_info_id=user_id,
        height=health_info.height,
        weight=health_info.weight,
        blood_group=health_info.blood_group,
    )

    db.add(db_health)
    db.commit()
    db.refresh(db_health)