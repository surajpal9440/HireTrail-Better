# HireTrail — Walkthrough Script (10–15 min)

---

## 1. Introduction (1 min)

"Hi, I'm going to walk you through HireTrail — a job application tracker I built from scratch using Flask, React, and SQLite.

The goal was to build something practical and realistic: not a toy app, not over-engineered, but something that could actually be useful and demonstrates clean full-stack development."

---

## 2. Project Structure (2 min)

"Let me show you the folder structure first."

```
better/
├── backend/      # Flask REST API
├── frontend/     # React + Vite app
├── README.md
└── agents.md     # AI usage policy
```

"The backend and frontend are completely separate — they talk through a REST API on port 5000. The frontend runs on port 5173. This is intentional: the backend could power a mobile app or CLI in the future without any changes."

### Backend structure:
"Inside backend/app:
- `models/` — SQLAlchemy ORM model
- `routes/` — thin HTTP handlers, just parse/validate/respond
- `services/` — where actual business logic lives
- `schemas/` — Marshmallow for input validation
- `utils/` — shared response helpers"

"This is called a service layer pattern. Routes don't contain logic, services don't know about HTTP. Clean separation."

---

## 3. Database Design (1 min)

"The `jobs` table has 11 columns: id, company, position, location, status (ENUM), applied_date, salary_range, job_url, notes, created_at, updated_at."

"I used SQLite via SQLAlchemy. SQLite is zero-config and perfectly fine for a single-user tracker. But if you want PostgreSQL, it's one environment variable change — the ORM handles the rest."

"The `JobStatus` class holds all valid statuses as constants. No magic strings anywhere — this prevents typos and makes changes safe."

---

## 4. Backend API (2 min)

"Let me show you the API."

`GET /api/jobs` — lists all jobs, supports `?status=` filter
`POST /api/jobs` — creates a new job, validates with Marshmallow
`GET /api/jobs/:id` — single job
`PUT /api/jobs/:id` — update (partial updates supported)
`DELETE /api/jobs/:id` — delete
`GET /api/jobs/stats` — summary stats used by the dashboard

"Every response looks the same:
```json
{ "success": true, "data": {...}, "message": "Job created" }
```
If there's an error:
```json
{ "success": false, "error": "Validation failed", "details": {...} }
```
The frontend always knows what shape to expect."

---

## 5. Validation (1 min)

"I used two separate schemas: `JobCreateSchema` and `JobUpdateSchema`.

Why two? On create, `company`, `position`, and `applied_date` are required. On update, every field is optional — you might only want to update the status. Using one schema for both would require messy conditional required logic."

"The `job_url` field validates that it's a real URL. Status validates against the `JobStatus.ALL` list. Company/position can't be blank strings."

---

## 6. Frontend Architecture (2 min)

"The React app is built with Vite and uses React Router for navigation."

"The key architectural decision was keeping the API layer separate — all fetch calls live in `src/api/jobs.js`. If the backend URL changes or we add auth headers, there's exactly one file to update."

"Pages are thin — they call hooks or API functions, then render components. Components are dumb — they just receive props and render. Business formatting is in `utils/formatters.js`."

"The design uses a CSS custom property design system — 30+ variables for colors, spacing, shadows. No Tailwind, no styled-components, just vanilla CSS. This gives full control and no build-time overhead."

---

## 7. Live Demo (2 min)

- Open dashboard — show stats cards, filter chips
- Add a new application — fill the form, submit
- Show job detail page — view/edit/delete flow
- Go to Board — show Kanban columns
- Filter by status on dashboard

---

## 8. Tests (1 min)

"I wrote 16 integration tests in `tests/test_jobs.py`. They cover:
- Full CRUD
- Validation failures (missing fields, bad URL, invalid status)
- Status filtering
- Stats accuracy
- 404 on non-existent jobs"

"Tests use an in-memory SQLite database via the `testing` config, so they're fast (< 1 second) and don't touch the real database."

---

## 9. AI Usage (1 min)

"I used AI assistance — documented in `agents.md`. The rules were:
- AI could suggest patterns and generate boilerplate
- AI could NOT make architectural decisions or define API contracts
- Every generated snippet was read, understood, tested, and refactored

For example, AI generated the Marshmallow schema stub. I then added the two-schema approach (create vs update), the custom validators, and the error message format — none of which AI suggested."

---

## 10. Risks & Limitations (1 min)

"Honest limitations:
1. **No auth** — anyone with the URL can see/edit everything. Adding JWT is planned next.
2. **SQLite concurrency** — safe for single-user, would need PostgreSQL for multi-user.
3. **No real-time** — board doesn't auto-refresh when another tab updates data.
4. **No attachments** — can't upload resumes or cover letters yet."

---

## 11. Future Improvements (1 min)

- User authentication (JWT)
- PostgreSQL in production
- Email reminders for follow-ups
- Interview round tracking (sub-events per job)
- Resume upload per application
- Analytics: time-to-offer, response rate trends

---

## 12. Closing

"To summarize: HireTrail is a clean, practical, production-like project. The backend follows a service layer pattern for testability. The frontend is organized by concern — API, components, pages, utils. The database is pragmatic — SQLite now, Postgres-ready later. And everything is tested."

"Questions?"
