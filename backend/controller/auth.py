from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated

from database_con.database import session
from models.models import User
from schemas.users import LoginUser
from core.jwt import create_token, to_decode
from core.security import verify_password

router=APIRouter()

def get_db():
    db=session()
    try:
        yield db
    finally:
        db.close()

db_dependancy=Annotated[Session, Depends(get_db)]

@router.post("/login/", status_code=status.HTTP_200_OK)
def login(user: LoginUser, db: db_dependancy):
    db_user=db.query(User).filter(User.email == user.email).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Credentials"

        )
    
    if not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Credentials"

        )
    
    access_token=create_token(
        data={"user_id": db_user.user_id}
    )
    
    return{
        "access_token": access_token,
        "token_type":"bearer"
    }