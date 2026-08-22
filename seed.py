from datetime import date, timedelta
import random

from database import SessionLocal
import models
import auth

db = SessionLocal()

# Create demo user
demo_email = "demo@example.com"
existing = db.query(models.User).filter(models.User.email == demo_email).first()
if existing:
    print("Demo user already exists, skipping user creation.")
    demo_user = existing
else:
    demo_user = models.User(
        email=demo_email,
        hashed_password=auth.hash_password("demopassword123"),
    )
    db.add(demo_user)
    db.commit()
    db.refresh(demo_user)
    print(f"Created demo user: {demo_email}")

# Sample application data: (company, role, source, status_progression)
sample_data = [
    ("Nova Systems", "SWE Intern", "referral", ["Applied", "OA", "Interview", "Offer"]),
    ("Bright Labs", "SWE Intern", "LinkedIn", ["Applied", "OA"]),
    ("TechCorp", "Data Engineer", "career fair", ["Applied", "OA", "Interview"]),
    ("Quantum Co", "SWE Intern", "referral", ["Applied"]),
    ("Vertex AI", "ML Engineer", "LinkedIn", ["Applied", "Rejected"]),
    ("Fern Analytics", "Data Engineer", "cold apply", ["Applied"]),
    ("Cedar Robotics", "SWE Intern", "referral", ["Applied", "OA", "Rejected"]),
    ("Marlin Systems", "Backend Engineer", "LinkedIn", ["Applied", "OA", "Interview", "Offer"]),
    ("Orbit Data", "Data Engineer", "career fair", ["Applied", "OA"]),
    ("Halcyon Tech", "ML Engineer", "cold apply", ["Applied"]),
    ("Redwood Cloud", "SWE Intern", "referral", ["Applied", "Ghosted"]),
    ("Solstice AI", "Backend Engineer", "LinkedIn", ["Applied", "OA", "Interview"]),
]

base_date = date(2026, 6, 1)

for i, (company, role, source, statuses) in enumerate(sample_data):
    date_applied = base_date + timedelta(days=i * 3)

    application = models.Application(
        user_id=demo_user.id,
        company=company,
        role=role,
        date_applied=date_applied,
        source=source,
        current_status=statuses[-1],
    )
    db.add(application)
    db.commit()
    db.refresh(application)

    for status in statuses:
        status_entry = models.StatusHistory(
            application_id=application.id,
            status=status,
        )
        db.add(status_entry)
    db.commit()

    print(f"Created application: {company} - {role} ({statuses[-1]})")

db.close()
print("Seeding complete.")
