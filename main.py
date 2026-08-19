from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional

from database import SessionLocal
import models
import schemas

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Job app tracker API is running"}

@app.post("/applications", response_model=schemas.ApplicationResponse)
def create_application(application: schemas.ApplicationCreate, db: Session = Depends(get_db)):
    new_application = models.Application(
        company=application.company,
        role=application.role,
        date_applied=application.date_applied,
        source=application.source,
        current_status=application.current_status,
    )
    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    status_entry = models.StatusHistory(
        application_id=new_application.id,
        status=new_application.current_status,
    )
    db.add(status_entry)
    db.commit()

    return new_application

@app.get("/applications", response_model=List[schemas.ApplicationResponse])
def list_applications(
    role: Optional[str] = None,
    status: Optional[str] = None,
    sort : str = "desc",
    db: Session = Depends(get_db)):

    query = db.query(models.Application)
    if role:
        query = query.filter(models.Application.role == role)
    if sort == "asc":
        query = query.order_by(models.Application.date_applied.asc())
    else:
        query = query.order_by(models.Application.date_applied.desc())
    if status:
        query = query.filter(models.Application.current_status == status)
    return query.all()
