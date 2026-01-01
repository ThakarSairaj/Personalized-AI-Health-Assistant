from sqlalchemy import Boolean, Integer, Float, BIGINT, String, Column, ForeignKey, Date
from database_con.database import base



class User(base):
    __tablename__='users'
    user_id=Column(Integer, primary_key=True, index=True)
    first_name=Column(String(50))
    last_name=Column(String(50))
    dob=Column(Date) #This need to change to the format('date-month-year')
    gender=Column(String(6))
    phone=Column(String(10))
    email=Column(String(50))
    password=Column(String(50))
    country=Column(String(20))
    state=Column(String(20))
    city=Column(String(20))


class UserHealthInfo(base):
    __tablename__='user_health_information'
    user_health_info_id=Column(Integer, ForeignKey('user.user_id'), primary_key=True)
    height=Column(Float)
    weight=Column(Float)
    blood_group=Column(String)