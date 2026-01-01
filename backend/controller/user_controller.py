from fastapi import APIRouter, status, Depends
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session
from database_con.database import session, engine
from models.models import User, UserHealthInfo
from schemas.users import CreateUser, CreateUserHealthInfo
from core.security import hash_password

router=APIRouter()



def get_db():
    db=session()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session, Depends(get_db)]

@router.post("/createUser/", status_code=status.HTTP_201_CREATED)
def create_user(user: CreateUser, db: db_dependency):
    hashed_password=hash_password(user.password)
    db_user=User(
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
        
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    


