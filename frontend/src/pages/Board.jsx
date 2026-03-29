import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { jobsApi } from "../api/jobs";
import { ALL_STATUSES, STATUS_LABELS, formatDate } from "../utils/formatters";

const STATUS_COLORS = {
  applied: "var(--status-applied)",
  interviewing: "var(--status-interviewing)",
  offer: "var(--status-offer)",
  rejected: "var(--status-rejected)",
  withdrawn: "var(--status-withdrawn)",
};

export default function Board() {
  const navigate = useNavigate();
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    jobsApi
      .getAll()
      .then((res) => setJobs(res.data))
      .catch(() => setError("Failed to load board"))
      .finally(() => setLoading(false));
  }, []);

  const byStatus = ALL_STATUSES.reduce((acc, s) => {
    acc[s] = jobs.filter((j) => j.status === s);
    return acc;
  }, {});

  if (loading) return <div className="loader"><div className="spinner" /> Loading…</div>;
  if (error) return <div className="alert alert-error">{error}</div>;

  return (
    <div>
      <div className="page-header">
        <div>
          <h2>Kanban Board</h2>
          <p>Visual overview of your pipeline</p>
        </div>
        <button id="btn-board-add" className="btn btn-primary" onClick={() => navigate("/add")}>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
            <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
          Add Application
        </button>
      </div>

      <div className="board-container" id="kanban-board">
        {ALL_STATUSES.map((status) => (
          <div key={status} className="board-col" id={`col-${status}`}>
            <div className="board-col-header">
              <span
                className="col-title"
                style={{ color: STATUS_COLORS[status] }}
              >
                {STATUS_LABELS[status]}
              </span>
              <span className="col-count">{byStatus[status].length}</span>
            </div>
            <div className="board-col-body">
              {byStatus[status].length === 0 ? (
                <div style={{ padding: "16px 0", textAlign: "center", color: "var(--text-muted)", fontSize: 12 }}>
                  No applications
                </div>
              ) : (
                byStatus[status].map((job) => (
                  <div
                    key={job.id}
                    className="board-job-card"
                    id={`board-card-${job.id}`}
                    onClick={() => navigate(`/jobs/${job.id}`)}
                    role="button"
                    tabIndex={0}
                    onKeyDown={(e) => e.key === "Enter" && navigate(`/jobs/${job.id}`)}
                  >
                    <div className="b-position">{job.position}</div>
                    <div className="b-company">{job.company}</div>
                    <div className="b-date">{formatDate(job.applied_date)}</div>
                  </div>
                ))
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
