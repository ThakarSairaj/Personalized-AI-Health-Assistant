'''
backend\schemas\health
add Pydantic schema for HealthQuestion validation when asking about the health related question from the report
'''
from pydantic import BaseModel

class HealthQuestion(BaseModel):
    question: str
