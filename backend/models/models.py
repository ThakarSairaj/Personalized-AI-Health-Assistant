# models/models.py

from sqlalchemy import Boolean, Integer, Float, BIGINT, String, Column, ForeignKey, Date, DateTime, Text
from database_con.database import base
from datetime import datetime


class User(base):
    __tablename__='users'
    user_id=Column(Integer, primary_key=True, index=True)
    first_name=Column(String(50))
    last_name=Column(String(50))
    dob=Column(Date) #This need to change to the format('date-month-year')
    gender=Column(String(6))
    phone=Column(String(10))
    email=Column(String(50), unique=True, index=True)
    password=Column(String(255))
    country=Column(String(20))
    state=Column(String(20))
    city=Column(String(20))


class UserHealthInfo(base):
    __tablename__='user_health_information'
    user_health_info_id=Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    height=Column(Float)
    weight=Column(Float)
    blood_group=Column(String)

# This table is to generate the medical report in pdf for doctors to understand
class MedicalReport(base):
    __tablename__='medical_reports'

    report_id=Column(Integer, primary_key=True, index=True)
    user_id=Column(Integer, ForeignKey("users.user_id"), nullable=False, index=True)
    chief_complaint=Column(String(255), nullable=False) #Single Sentence Description
    symptoms=Column(Text, nullable=False)
    duration=Column(String(50))
    onset_type=Column(String(20)) #Like Suddent/Gradual
    progression=Column(String(20)) #Improving/Worsening/Same
    severity=Column(String(20)) # Mild/Moderate/Severe
    reported_at=Column(DateTime, default=datetime.utcnow)
    

class UploadedReport(base):
    __tablename__ = 'uploaded_reports'

    uploaded_report_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)

    report_type = Column(String(50))  # lab
    report_date = Column(Date)
    uploaded_at = Column(DateTime, default=datetime.utcnow)



class ExtractedLabResult(base):
    __tablename__ = 'extracted_lab_results'

    lab_result_id = Column(Integer, primary_key=True)

    uploaded_report_id = Column(Integer, ForeignKey('uploaded_reports.uploaded_report_id'))
    user_id = Column(Integer, ForeignKey('users.user_id'))

    test_name = Column(String(150))
    test_value = Column(Float)
    unit = Column(String(50))
    reference_range = Column(String(100))
    status = Column(String(20))
    test_date = Column(Date)



    