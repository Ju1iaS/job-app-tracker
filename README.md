# Job Application Tracker API

A backend API for tracking job applications and analyzing your own job search funnel. Built with FastAPI, SQLAlchemy, PostgreSQL, and Pandas.

**Live demo:** https://job-app-tracker-production-a517.up.railway.app/docs
**Demo credentials:** `demo@example.com` / `demopassword123`

> [!NOTE]
> These are shared demo credentials with seeded, fake data.

## What it does

This is a REST API (no frontend yet) that lets a user:
- Track job applications with company, role, source, and status.
- Automatically log a timestamped history of every status change.
- Get analytics on their own job search: funnel conversion rates, average response times, and which sources/roles convert best.

I built this to track my own job search, gain meaningful information, and to practice designing a small backend end-to-end that covers schema design, authentication, and data analysis.

## Tech stack

- **FastAPI** - REST API framework
- **SQLAlchemy** - ORM
- **PostgreSQL** (production) / **SQLite** (local dev) - `database.py` reads a `DATABASE_URL` environment variable if present and falls back to local SQLite otherwise, so local dev has zero setup cost while production gets a persistent database
- **Pandas** - analytics endpoints
- **JWT (python-jose) + bcrypt (passlib)** - authentication
- **slowapi** - rate limiting
- **Railway** - deployment

## Features

- Full CRUD on applications, scoped per-user via JWT auth.
- Automatic status-history logging: every status change is recorded with a timestamp, not just overwritten.
- Three analytics endpoints:
  - `/summary/funnel` — cumulative conversion rate through each stage (Applied to OA to Interview to Offer)
  - `/summary/response-time` — average days to first response, overall and by source
  - `/summary/by-group` — conversion rate broken down by source or role
- Rate limiting on auth endpoints (5 requests/minute) to prevent brute-force attempts.
- Enforced password strength and email/status validation via Pydantic.
- Passwords hashed with bcrypt.

## Schema

Three tables: `users`, `applications`, and `status_history`.

`status_history` is a separate table from `applications` since an application has many status changes over time.

    users (id, email, hashed_password)
      -> applications (id, user_id, company, role, source, current_status, date_applied, job_url, notes)
            -> status_history (id, application_id, status, changed_at)

## Example usage

> [!IMPORTANT]
> This is an API-only project with no frontend. Use the interactive docs above to browse the available endpoints, or try `/signup` and `/login` directly (they don't require a token). For anything else, curl with a token from `/login` (examples below) for anything requiring authentication. The docs page's built-in "Authorize" button isn't wired up to this login flow yet.

Log in and get a token:

    curl -X POST https://job-app-tracker-production-a517.up.railway.app/login \
      -H "Content-Type: application/json" \
      -d '{"email": "demo@example.com", "password": "demopassword123"}'

Use the token to view your applications:

    curl -X GET https://job-app-tracker-production-a517.up.railway.app/applications \
      -H "Authorization: Bearer <token from above>"

Get the funnel breakdown:

    curl -X GET https://job-app-tracker-production-a517.up.railway.app/summary/funnel \
      -H "Authorization: Bearer <token from above>"

## Running locally

    git clone https://github.com/Ju1iaS/job-app-tracker.git
    cd job-app-tracker
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

Create a `.env` file in the project root:

    SECRET_KEY=<generate one with: python -c "import secrets; print(secrets.token_hex(32))">

Create the database tables and (optionally) seed demo data:

    python -c "from database import engine, Base; import models; Base.metadata.create_all(bind=engine)"
    python seed.py

Run the server:

    uvicorn main:app --reload

Visit `http://127.0.0.1:8000/docs` for the interactive API docs.