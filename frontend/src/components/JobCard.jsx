import { useNavigate } from "react-router-dom";
import StatusBadge from "./StatusBadge";
import { formatDate, daysSince } from "../utils/formatters";

export default function JobCard({ job }) {
  const navigate = useNavigate();
  const days = daysSince(job.applied_date);

  return (
    <div
      className="job-card"
      onClick={() => navigate(`/jobs/${job.id}`)}
      id={`job-card-${job.id}`}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => e.key === "Enter" && navigate(`/jobs/${job.id}`)}
    >
      <div className="job-info">
        <h3>{job.position}</h3>
        <div className="company">{job.company}</div>
        <div className="job-meta">
          {job.location && (
            <span className="meta-item">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0 1 18 0z"/>
                <circle cx="12" cy="10" r="3"/>
              </svg>
              {job.location}
            </span>
          )}
          <span className="meta-item">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <rect x="3" y="4" width="18" height="18" rx="2"/>
              <line x1="16" y1="2" x2="16" y2="6"/>
              <line x1="8" y1="2" x2="8" y2="6"/>
              <line x1="3" y1="10" x2="21" y2="10"/>
            </svg>
            Applied {formatDate(job.applied_date)}
            {days !== null && (
              <span style={{ color: "var(--text-muted)", marginLeft: 4 }}>
                ({days}d ago)
              </span>
            )}
          </span>
          {job.salary_range && (
            <span className="meta-item">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="12" y1="1" x2="12" y2="23"/>
                <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
              </svg>
              {job.salary_range}
            </span>
          )}
        </div>
      </div>
      <div className="job-actions">
        <StatusBadge status={job.status} />
      </div>
    </div>
  );
}
