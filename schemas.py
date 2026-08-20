from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class ApplicationCreate(BaseModel):
    company: str
    role: str
    date_applied: date
    source: str
    current_status: str = "Applied"
    job_url: Optional[str] = None
    notes: Optional[str] = None

class ApplicationResponse(BaseModel):
    id: int
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
    current_status: Optional[str] = None
    job_url: Optional[str] = None
    notes: Optional[str] = None

class UserCreate(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    email: str
    password: str
