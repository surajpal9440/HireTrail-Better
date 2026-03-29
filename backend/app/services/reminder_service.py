"""
Daily email reminder service.

Runs via APScheduler every day at 9am.
Finds jobs where:
  - status is still 'applied'
  - applied_date is REMINDER_DAYS or more days ago

Groups them by user and sends one consolidated email per user.
"""
import logging
from datetime import date, timedelta
from flask import current_app
from flask_mail import Message

from app import mail, db
from app.models.job import Job, JobStatus
from app.models.user import User

logger = logging.getLogger(__name__)


def send_reminder_emails(app):
    """
    Scheduled job entry point. Must be called with the Flask app context.
    """
    with app.app_context():
        reminder_days = app.config.get("REMINDER_DAYS", 7)
        cutoff_date = date.today() - timedelta(days=reminder_days)

        stale_jobs = (
            db.session.query(Job)
            .filter(Job.status == JobStatus.APPLIED, Job.applied_date <= cutoff_date)
            .all()
        )

        if not stale_jobs:
            logger.info("Reminder job: no stale applications found today.")
            return

        # Group by user
        by_user: dict[int, list[Job]] = {}
        for job in stale_jobs:
            by_user.setdefault(job.user_id, []).append(job)

        sent = 0
        for user_id, jobs in by_user.items():
            user = User.query.get(user_id)
            if not user:
                continue
            try:
                _send_reminder_email(user, jobs, reminder_days)
                sent += 1
            except Exception as e:
                logger.error(f"Failed to send reminder to {user.email}: {e}")

        logger.info(f"Reminder job: sent {sent} email(s) for {len(stale_jobs)} stale application(s).")


def _send_reminder_email(user: User, jobs: list[Job], reminder_days: int):
    """Send a single consolidated reminder email to a user."""
    subject = f"HireTrail: {len(jobs)} application(s) need a follow-up 📬"

    # Build plain-text and HTML body
    job_lines_text = "\n".join(
        f"  • {j.position} at {j.company} (applied {j.applied_date})" for j in jobs
    )
    job_lines_html = "".join(
        f"<li><strong>{j.position}</strong> at {j.company} &mdash; applied {j.applied_date}</li>"
        for j in jobs
    )

    text_body = f"""Hi {user.name},

You have {len(jobs)} job application(s) that you applied to {reminder_days}+ days ago with no status update:

{job_lines_text}

Consider sending a follow-up email or updating the status in HireTrail.

Good luck! 🎯
— The HireTrail Team
"""

    html_body = f"""
<div style="font-family: Inter, sans-serif; max-width: 560px; margin: 0 auto; padding: 24px; color: #1a1d27;">
  <h2 style="color: #6c63ff;">📬 Follow-up reminder</h2>
  <p>Hi <strong>{user.name}</strong>,</p>
  <p>You have <strong>{len(jobs)}</strong> application(s) that have been sitting at <em>Applied</em>
     for {reminder_days}+ days with no update:</p>
  <ul style="line-height: 1.9;">
    {job_lines_html}
  </ul>
  <p>Consider sending a follow-up email or update the status in <strong>HireTrail</strong>.</p>
  <p style="color: #8b90a8; font-size: 13px;">Good luck! 🎯<br/>— The HireTrail Team</p>
</div>
"""

    msg = Message(
        subject=subject,
        recipients=[user.email],
        body=text_body,
        html=html_body,
    )
    mail.send(msg)
    logger.info(f"Reminder email sent to {user.email} ({len(jobs)} jobs)")
