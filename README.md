# HireTrail — Job Application Tracker

A full-stack web app to track job applications through their entire lifecycle — from first click to offer letter.

## Tech Stack

| Layer | Tech |
|---|---|
| Backend | Python 3, Flask, SQLAlchemy, Marshmallow |
| Frontend | React 18, Vite, React Router |
| Database | SQLite (swap to PostgreSQL with one env var) |

## Project Structure

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

## Tradeoffs & Limitations

- **No authentication** — Single-user app. Adding JWT auth requires a `users` table + `user_id` FK on `jobs`.
- **SQLite** — Not suitable for concurrent multi-user writes. Swap to PostgreSQL for production.
- **No real-time** — Page refreshes to see updates. WebSocket or polling can be added.
- **No file uploads** — Resume/cover letter attachments are out of scope.
