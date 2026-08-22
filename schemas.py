from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional
from enum import Enum

class ApplicationStatus(str, Enum):
    applied = "Applied"
    oa = "OA"
    interview = "Interview"
    offer = "Offer"
    rejected = "Rejected"
    ghosted = "Ghosted"

class ApplicationCreate(BaseModel):
    company: str
    role: str
    date_applied: date
    source: str
    current_status: ApplicationStatus = ApplicationStatus.applied
    job_url: Optional[str] = None
    notes: Optional[str] = None

class ApplicationResponse(BaseModel):
    id: int
    user_id: int
    company: str
    role: str
    date_applied: date
    source: str
    current_status: str
    created_at: datetime
    job_url: Optional[str] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True

class ApplicationUpdate(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    date_applied: Optional[date] = None
    source: Optional[str] = None
    current_status: Optional[ApplicationStatus] = None
    job_url: Optional[str] = None
    notes: Optional[str] = None

class UserCreate(BaseModel):
    email: str
    password: str = Field(..., min_length=8, max_length=72)

class UserResponse(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    email: str
    password: str
