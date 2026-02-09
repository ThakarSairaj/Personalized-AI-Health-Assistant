from fastapi import APIRouter, status, Depends, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database_con.database import session
from models.models import User
from schemas.users import CreateUser
from core.security import hash_password

router = APIRouter()

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/createUser/", status_code=status.HTTP_201_CREATED)
def create_user(user: CreateUser, db: db_dependency):
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )
    
    # Hash password
    hashed_password = hash_password(user.password)
    
    # Create new user
    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        dob=user.dob,
        gender=user.gender,
        phone=user.phone,
        email=user.email,
        password=hashed_password,
        country=user.country,
        state=user.state,
        city=user.city
    )
    
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )
    
    # Return user_id for frontend
    return {"user_id": db_user.user_id}
