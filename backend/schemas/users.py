# schemas/users.py
from pydantic import BaseModel, field_validator
from datetime import date, datetime

class CreateUser(BaseModel):
    first_name: str
    last_name: str
    dob: date
    gender: str
    phone: str
    email: str
    password: str
    country: str
    state: str
    city: str

    # This is for the date format in dd-mm-yyyy
    @field_validator('dob', mode='before')
    @classmethod
    def parse_dob(cls, value):
        if isinstance(value, str):
            return datetime.strptime(value, "%d-%m-%Y").date()
        return value
    
    @field_validator('gender')
    @classmethod
    def gender_sel(cls, value):
        allowed=['male', 'female']
        if value.lower() not in allowed:
            raise ValueError("Invalid gender")
        return value

class CreateUserHealthInfo(BaseModel):
    height: float
    weight: float
    blood_group: str