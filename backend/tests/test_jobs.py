import json

AUTH_BASE = "/api/auth"
JOBS_BASE = "/api/jobs"

SAMPLE_JOB = {
    "company": "Acme Corp",
    "position": "Backend Engineer",
    "location": "Remote",
    "status": "applied",
    "applied_date": "2024-06-01",
    "salary_range": "80k-100k",
    "job_url": "https://example.com/jobs/1",
    "notes": "Referred by a friend",
}


def post_job(client, headers, data=None):
    return client.post(
        JOBS_BASE,
        data=json.dumps(data or SAMPLE_JOB),
        content_type="application/json",
        headers=headers,
    )


# ── Auth ───────────────────────────────────────────────────────────────────────

def test_register(client):
    res = client.post(
        f"{AUTH_BASE}/register",
        data=json.dumps({"name": "Jane", "email": "jane@test.com", "password": "securepass"}),
        content_type="application/json",
    )
    assert res.status_code == 201
    body = res.get_json()
    assert body["success"] is True
    assert "token" in body["data"]
    assert body["data"]["user"]["email"] == "jane@test.com"


def test_register_duplicate_email(client):
    payload = {"name": "Jane", "email": "jane@test.com", "password": "securepass"}
    client.post(f"{AUTH_BASE}/register", data=json.dumps(payload), content_type="application/json")
    res = client.post(f"{AUTH_BASE}/register", data=json.dumps(payload), content_type="application/json")
    assert res.status_code == 409


def test_register_weak_password(client):
    res = client.post(
        f"{AUTH_BASE}/register",
        data=json.dumps({"name": "Jane", "email": "jane@test.com", "password": "short"}),
        content_type="application/json",
    )
    assert res.status_code == 422


def test_login(client):
    client.post(
        f"{AUTH_BASE}/register",
        data=json.dumps({"name": "Jane", "email": "jane@test.com", "password": "securepass"}),
        content_type="application/json",
    )
    res = client.post(
        f"{AUTH_BASE}/login",
        data=json.dumps({"email": "jane@test.com", "password": "securepass"}),
        content_type="application/json",
    )
    assert res.status_code == 200
    assert "token" in res.get_json()["data"]


def test_login_wrong_password(client):
    client.post(
        f"{AUTH_BASE}/register",
        data=json.dumps({"name": "Jane", "email": "jane@test.com", "password": "securepass"}),
        content_type="application/json",
    )
    res = client.post(
        f"{AUTH_BASE}/login",
        data=json.dumps({"email": "jane@test.com", "password": "wrongpass"}),
        content_type="application/json",
    )
    assert res.status_code == 401


def test_me_requires_auth(client):
    res = client.get(f"{AUTH_BASE}/me")
    assert res.status_code == 401


def test_me_returns_user(client, auth_headers):
    res = client.get(f"{AUTH_BASE}/me", headers=auth_headers)
    assert res.status_code == 200
    assert res.get_json()["data"]["email"] == "test@example.com"


# ── Jobs require auth ──────────────────────────────────────────────────────────

def test_jobs_require_auth(client):
    res = client.get(JOBS_BASE)
    assert res.status_code == 401


# ── Create ─────────────────────────────────────────────────────────────────────

def test_create_job(client, auth_headers):
    res = post_job(client, auth_headers)
    assert res.status_code == 201
    body = res.get_json()
    assert body["success"] is True
    assert body["data"]["company"] == "Acme Corp"


def test_create_job_missing_fields(client, auth_headers):
    res = post_job(client, auth_headers, {"company": "Only Company"})
    assert res.status_code == 422


def test_create_job_invalid_url(client, auth_headers):
    res = post_job(client, auth_headers, {**SAMPLE_JOB, "job_url": "not-a-url"})
    assert res.status_code == 422


# ── Data isolation ─────────────────────────────────────────────────────────────

def test_user_cannot_see_other_users_jobs(client, auth_headers):
    # Create job as user 1
    post_job(client, auth_headers)

    # Register user 2
    client.post(
        f"{AUTH_BASE}/register",
        data=json.dumps({"name": "Bob", "email": "bob@test.com", "password": "securepass"}),
        content_type="application/json",
    )
    res2 = client.post(
        f"{AUTH_BASE}/login",
        data=json.dumps({"email": "bob@test.com", "password": "securepass"}),
        content_type="application/json",
    )
    token2 = res2.get_json()["data"]["token"]
    headers2 = {"Authorization": f"Bearer {token2}"}

    # User 2 should see 0 jobs
    res = client.get(JOBS_BASE, headers=headers2)
    assert len(res.get_json()["data"]) == 0


# ── Read ───────────────────────────────────────────────────────────────────────

def test_list_jobs(client, auth_headers):
    post_job(client, auth_headers)
    res = client.get(JOBS_BASE, headers=auth_headers)
    assert res.status_code == 200
    assert len(res.get_json()["data"]) == 1


def test_filter_by_status(client, auth_headers):
    post_job(client, auth_headers)
    post_job(client, auth_headers, {**SAMPLE_JOB, "status": "rejected"})
    res = client.get(f"{JOBS_BASE}?status=rejected", headers=auth_headers)
    assert len(res.get_json()["data"]) == 1


def test_get_job_not_found(client, auth_headers):
    res = client.get(f"{JOBS_BASE}/999", headers=auth_headers)
    assert res.status_code == 404


# ── Update ─────────────────────────────────────────────────────────────────────

def test_update_status(client, auth_headers):
    post_job(client, auth_headers)
    res = client.put(
        f"{JOBS_BASE}/1",
        data=json.dumps({"status": "interviewing"}),
        content_type="application/json",
        headers=auth_headers,
    )
    assert res.status_code == 200
    assert res.get_json()["data"]["status"] == "interviewing"


# ── Delete ─────────────────────────────────────────────────────────────────────

def test_delete_job(client, auth_headers):
    post_job(client, auth_headers)
    res = client.delete(f"{JOBS_BASE}/1", headers=auth_headers)
    assert res.status_code == 200
    assert client.get(f"{JOBS_BASE}/1", headers=auth_headers).status_code == 404


# ── Stats ──────────────────────────────────────────────────────────────────────

def test_stats(client, auth_headers):
    post_job(client, auth_headers)
    post_job(client, auth_headers, {**SAMPLE_JOB, "status": "interviewing"})
    res = client.get(f"{JOBS_BASE}/stats", headers=auth_headers)
    data = res.get_json()["data"]
    assert data["total"] == 2
    assert data["by_status"]["applied"] == 1
    assert data["by_status"]["interviewing"] == 1
