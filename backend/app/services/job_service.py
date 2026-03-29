import logging
from datetime import date
from app import db
from app.models.job import Job, JobStatus
from app.services import sse_service

logger = logging.getLogger(__name__)


def get_all_jobs(user_id, status_filter=None):
    query = Job.query.filter_by(user_id=user_id)
    if status_filter and status_filter in JobStatus.ALL:
        query = query.filter_by(status=status_filter)
    jobs = query.order_by(Job.applied_date.desc()).all()
    return [j.to_dict() for j in jobs]


def get_job_by_id(job_id, user_id):
    """Returns job only if it belongs to the requesting user."""
    return Job.query.filter_by(id=job_id, user_id=user_id).first()


def create_job(data, user_id):
    job = Job(
        user_id=user_id,
        company=data["company"].strip(),
        position=data["position"].strip(),
        location=data.get("location"),
        status=data.get("status", JobStatus.APPLIED),
        applied_date=data["applied_date"],
        salary_range=data.get("salary_range"),
        job_url=data.get("job_url"),
        notes=data.get("notes"),
    )
    db.session.add(job)
    db.session.commit()
    logger.info(f"Job created: {job.company} — {job.position} (user={user_id}, id={job.id})")
    sse_service.publish(str(user_id), "job_created", job.to_dict())
    return job


def update_job(job, data, user_id):
    updatable_fields = [
        "company", "position", "location", "status",
        "applied_date", "salary_range", "job_url", "notes",
    ]
    for field in updatable_fields:
        if field in data:
            value = data[field]
            if isinstance(value, str) and field in ("company", "position"):
                value = value.strip()
            setattr(job, field, value)

    db.session.commit()
    logger.info(f"Job updated: id={job.id} (user={user_id})")
    sse_service.publish(str(user_id), "job_updated", job.to_dict())
    return job


def delete_job(job, user_id):
    job_data = job.to_dict()
    db.session.delete(job)
    db.session.commit()
    logger.info(f"Job deleted: id={job.id} (user={user_id})")
    sse_service.publish(str(user_id), "job_deleted", {"id": job_data["id"]})


def get_stats(user_id):
    total = Job.query.filter_by(user_id=user_id).count()
    counts = {status: 0 for status in JobStatus.ALL}
    for status in JobStatus.ALL:
        counts[status] = Job.query.filter_by(user_id=user_id, status=status).count()

    response_rate = 0
    if total > 0:
        responded = total - counts[JobStatus.APPLIED]
        response_rate = round((responded / total) * 100, 1)

    return {
        "total": total,
        "by_status": counts,
        "response_rate": response_rate,
    }
