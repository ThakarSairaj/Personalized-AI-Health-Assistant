from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CreateMedicalReport(BaseModel):
    chief_complaint: str=Field(..., max_length=255)
    symptoms:str
    duration: Optional[str]=None
    onset_type: Optional[str]=None
    progression: Optional[str]=None
    severity: Optional[str]=None