# 🎯 HireTrail — Advanced Job Application Tracker

**HireTrail** is a centralized platform designed to solve a common problem for job seekers: when you apply to dozens of companies across different platforms, it's easy to forget where you applied, what role it was for, and what stage of the process you are currently in (Applied, Interviewing, Offer). HireTrail helps you effortlessly organize and track the progress of every application in one single dashboard.

## ✨ Key Features

- **🔐 Secure Authentication:** Full user registration and JWT-based authentication system. Your data is private and secure to your account.
- **⚡ Real-Time Updates:** Live event streaming via Server-Sent Events (SSE). See status updates across all your devices instantly without refreshing the page.
- **📊 Interactive Dashboard:** Visual statistics and metrics to track your application success rate, weekly applications, and current pipeline health.
- **📋 Kanban Board View:** Drag-and-drop style organization (visually) grouping your applications by their current stage (Applied, Interviewing, Offer, Rejected).
- **📱 Responsive UI:** A beautiful, responsive frontend built with React and styled elegantly, providing a native-like experience on both desktop and mobile.

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3, Flask, SQLAlchemy ORM, Marshmallow, Flask-JWT-Extended |
| **Frontend** | React 18, Vite, React Router, Context API |
| **Database** | SQLite (Easily swappable to PostgreSQL) |

## 🏗️ Project Structure


```
hiretrail/
├── backend/
│   ├── app/
│   │   ├── __init__.py       # App factory
│   │   ├── config.py         # Dev / test / prod configs
│   │   ├── models/job.py     # SQLAlchemy Job model
│   │   ├── routes/jobs.py    # HTTP endpoints (thin layer)
│   │   ├── services/job_service.py   # Business logic
│   │   ├── schemas/job_schema.py     # Marshmallow validation
│   │   └── utils/response.py         # Consistent API responses
│   ├── tests/
│   │   ├── conftest.py       # Fixtures (in-memory SQLite)
│   │   └── test_jobs.py      # 16 integration tests
│   ├── run.py
│   └── requirements.txt
│
└── frontend/
    └── src/
        ├── api/jobs.js       # All API calls (one file)
        ├── components/       # JobCard, JobForm, StatusBadge, StatsCard
        ├── pages/            # Dashboard, Board, AddJob, JobDetail
        └── utils/formatters.js
```

## Setup

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
python run.py
# → http://localhost:5000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
# → http://localhost:5173
```

### Run Tests

```bash
cd backend
venv\Scripts\activate
pytest tests/ -v
```

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/jobs` | List jobs (optional `?status=` filter) |
| POST | `/api/jobs` | Create job |
| GET | `/api/jobs/:id` | Get job detail |
| PUT | `/api/jobs/:id` | Update job |
| DELETE | `/api/jobs/:id` | Delete job |
| GET | `/api/jobs/stats` | Summary stats |

## Key Technical Decisions

**SQLite as default** — Zero configuration. Realistically, a single-user job tracker doesn't need Postgres. SQLAlchemy's ORM means switching is one env var change.

**Separate Create/Update schemas** — Using two Marshmallow schemas (`JobCreateSchema`, `JobUpdateSchema`) prevents accidental field overwrites and makes it explicit what can change in a PATCH.

**Service layer** — Routes only handle HTTP (parse JSON, call service, return response). All logic lives in `job_service.py`. This makes services unit-testable without spinning up Flask.

**Response format contract** — Every API response is `{ success, data/error, message }`. Frontend can trust this shape always exists.

## ⚠️ Current Limitations

- **SQLite Constraints** — Currently uses SQLite out-of-the-box which is perfect for personal tracking but may face write-locks under heavy concurrent multi-user load. Can be easily swapped to PostgreSQL for production.
- **No File Uploads** — Keeping it simple: Resume and cover letter attachments are currently out of scope to avoid complex cloud storage configurations.
