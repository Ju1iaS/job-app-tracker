from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class ApplicationCreate(BaseModel):
    company: str
    role: str
    date_applied: date
    source: str
    current_status: str = "Applied"

class ApplicationResponse(BaseModel):
    id: int
    company: str
    role: str
    date_applied: date
    source: str
    current_status: str
    created_at: datetime

    class Config:
        from_attributes = True
