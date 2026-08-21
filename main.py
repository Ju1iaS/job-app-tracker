from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional

from database import SessionLocal
import models
import schemas

import auth

from auth import get_db, get_current_user

import pandas as pd

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Job app tracker API is running"}

@app.post("/applications", response_model=schemas.ApplicationResponse)
def create_application(
    application: schemas.ApplicationCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    new_application = models.Application(
        user_id = current_user.id,
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
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    query = db.query(models.Application).filter(models.Application.user_id == current_user.id)
    if role:
        query = query.filter(models.Application.role == role)
    if sort == "asc":
        query = query.order_by(models.Application.date_applied.asc())
    else:
        query = query.order_by(models.Application.date_applied.desc())
    if status:
        query = query.filter(models.Application.current_status == status)
    return query.all()

@app.get("/applications/{application_id}", response_model=schemas.ApplicationResponse)
def get_application(
    application_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    application = db.query(models.Application).filter(
        models.Application.id == application_id,
        models.Application.user_id == current_user.id
    ).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application

@app.patch("/applications/{application_id}", response_model=schemas.ApplicationResponse)
def update_application(
    application_id: int, 
    update: schemas.ApplicationUpdate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    application = db.query(models.Application).filter(
        models.Application.id == application_id,
        models.Application.user_id == current_user.id
    ).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    update_data = update.model_dump(exclude_unset=True)
    status_changed = "current_status" in update_data and update_data["current_status"] != application.current_status

    for field, value in update_data.items():
        setattr(application, field, value)

    db.commit()
    db.refresh(application)

    if status_changed:
        status_entry = models.StatusHistory(
            application_id=application.id,
            status=application.current_status,
        )
        db.add(status_entry)
        db.commit()

    return application

@app.delete("/applications/{application_id}")
def delete_application(
    application_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    application = db.query(models.Application).filter(
        models.Application.id == application_id,
        models.Application.user_id == current_user.id
    ).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    db.query(models.StatusHistory).filter(models.StatusHistory.application_id == application_id).delete()
    db.delete(application)
    db.commit()

    return {"detail": "Application deleted"}

@app.post("/signup", response_model=schemas.UserResponse)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = models.User(
        email=user.email,
        hashed_password=auth.hash_password(user.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login")
def login(credentials: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == credentials.email).first()
    if not user or not auth.verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}



STAGE_ORDER = ["Applied", "OA", "Interview", "Offer"]

@app.get("/summary/funnel")
def funnel_summary(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    results = (
        db.query(models.StatusHistory.application_id, models.StatusHistory.status)
        .join(models.Application, models.Application.id == models.StatusHistory.application_id)
        .filter(models.Application.user_id == current_user.id)
        .all()
    )

    if not results:
        return {"total_applications": 0, "funnel": []}

    df = pd.DataFrame(results, columns=["application_id", "status"])
    df["stage_rank"] = df["status"].apply(lambda s: STAGE_ORDER.index(s) if s in STAGE_ORDER else -1)

    furthest_per_app = df.loc[df.groupby("application_id")["stage_rank"].idxmax()]

    total = furthest_per_app["application_id"].nunique()
    funnel = []
    for stage in STAGE_ORDER:
        reached = (furthest_per_app["stage_rank"] >= STAGE_ORDER.index(stage)).sum()
        rate = round((reached / total) * 100, 1) if total > 0 else 0
        funnel.append({"stage": stage, "count": int(reached), "conversion_rate": rate})

    return {"total_applications": total, "funnel": funnel}