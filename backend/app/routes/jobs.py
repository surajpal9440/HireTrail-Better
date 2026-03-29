import logging
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

from app.schemas.job_schema import JobCreateSchema, JobUpdateSchema
from app.services import job_service
from app.utils import response as resp

logger = logging.getLogger(__name__)

jobs_bp = Blueprint("jobs", __name__, url_prefix="/api/jobs")

create_schema = JobCreateSchema()
update_schema = JobUpdateSchema()


@jobs_bp.route("", methods=["GET"])
@jwt_required()
def list_jobs():
    user_id = int(get_jwt_identity())
    status_filter = request.args.get("status")
    jobs = job_service.get_all_jobs(user_id=user_id, status_filter=status_filter)
    return resp.success(data=jobs, message=f"{len(jobs)} job(s) found")


@jobs_bp.route("/stats", methods=["GET"])
@jwt_required()
def job_stats():
    user_id = int(get_jwt_identity())
    stats = job_service.get_stats(user_id=user_id)
    return resp.success(data=stats, message="Stats retrieved")


@jobs_bp.route("/<int:job_id>", methods=["GET"])
@jwt_required()
def get_job(job_id):
    user_id = int(get_jwt_identity())
    job = job_service.get_job_by_id(job_id, user_id=user_id)
    if not job:
        return resp.error("Job not found", status_code=404)
    return resp.success(data=job.to_dict())


@jobs_bp.route("", methods=["POST"])
@jwt_required()
def create_job():
    user_id = int(get_jwt_identity())
    json_data = request.get_json()
    if not json_data:
        return resp.error("Request body must be JSON", status_code=400)
    try:
        data = create_schema.load(json_data)
    except ValidationError as e:
        return resp.error("Validation failed", details=e.messages, status_code=422)

    job = job_service.create_job(data, user_id=user_id)
    return resp.success(data=job.to_dict(), message="Job application added", status_code=201)


@jobs_bp.route("/<int:job_id>", methods=["PUT"])
@jwt_required()
def update_job(job_id):
    user_id = int(get_jwt_identity())
    job = job_service.get_job_by_id(job_id, user_id=user_id)
    if not job:
        return resp.error("Job not found", status_code=404)

    json_data = request.get_json()
    if not json_data:
        return resp.error("Request body must be JSON", status_code=400)

    try:
        data = update_schema.load(json_data)
    except ValidationError as e:
        return resp.error("Validation failed", details=e.messages, status_code=422)

    updated = job_service.update_job(job, data, user_id=user_id)
    return resp.success(data=updated.to_dict(), message="Job updated")


@jobs_bp.route("/<int:job_id>", methods=["DELETE"])
@jwt_required()
def delete_job(job_id):
    user_id = int(get_jwt_identity())
    job = job_service.get_job_by_id(job_id, user_id=user_id)
    if not job:
        return resp.error("Job not found", status_code=404)

    job_service.delete_job(job, user_id=user_id)
    return resp.success(message="Job deleted")
