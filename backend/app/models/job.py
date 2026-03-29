from datetime import datetime, date
from app import db


class JobStatus:
    APPLIED = "applied"
    INTERVIEWING = "interviewing"
    OFFER = "offer"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"

    ALL = [APPLIED, INTERVIEWING, OFFER, REJECTED, WITHDRAWN]


class Job(db.Model):
    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    company = db.Column(db.String(150), nullable=False)
    position = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(150), nullable=True)
    status = db.Column(db.String(20), nullable=False, default=JobStatus.APPLIED)
    applied_date = db.Column(db.Date, nullable=False, default=date.today)
    salary_range = db.Column(db.String(50), nullable=True)
    job_url = db.Column(db.Text, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "company": self.company,
            "position": self.position,
            "location": self.location,
            "status": self.status,
            "applied_date": self.applied_date.isoformat() if self.applied_date else None,
            "salary_range": self.salary_range,
            "job_url": self.job_url,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self):
        return f"<Job {self.company} — {self.position} [{self.status}]>"
