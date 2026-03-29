import { useEffect, useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { jobsApi } from "../api/jobs";
import StatsCard from "../components/StatsCard";
import JobCard from "../components/JobCard";
import { useRealtime } from "../hooks/useRealtime";
import { useAuth } from "../context/AuthContext";

const STATUS_FILTERS = ["all", "applied", "interviewing", "offer", "rejected", "withdrawn"];

export default function Dashboard() {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [jobs, setJobs] = useState([]);
  const [stats, setStats] = useState(null);
  const [filter, setFilter] = useState("all");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadData = useCallback(async () => {
    try {
      const [jobsRes, statsRes] = await Promise.all([
        jobsApi.getAll(filter === "all" ? null : filter),
        jobsApi.getStats(),
      ]);
      setJobs(jobsRes.data);
      setStats(statsRes.data);
      setError(null);
    } catch (err) {
      setError("Failed to load jobs. Is the backend running?");
    } finally {
      setLoading(false);
    }
  }, [filter]);

  useRealtime(loadData);

  useEffect(() => {
    loadData();
  }, [filter]);



  return (
    <div>
      <div className="page-header">
        <div>
          <h2>Dashboard</h2>
          <p>Track and manage all your job applications</p>
        </div>
        <button id="btn-add-job" className="btn btn-primary" onClick={() => navigate("/add")}>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
            <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
          Add Application
        </button>
      </div>

      {stats && (
        <div className="stats-grid">
          <StatsCard label="Total" value={stats.total} sub="all applications" />
          <StatsCard
            label="Applied"
            value={stats.by_status.applied}
            color="var(--status-applied)"
            sub="awaiting response"
          />
          <StatsCard
            label="Interviewing"
            value={stats.by_status.interviewing}
            color="var(--status-interviewing)"
            sub="in progress"
          />
          <StatsCard
            label="Offers"
            value={stats.by_status.offer}
            color="var(--status-offer)"
            sub="received"
          />
          <StatsCard
            label="Response Rate"
            value={`${stats.response_rate}%`}
            sub="of applications"
          />
        </div>
      )}

      <div className="filter-bar">
        {STATUS_FILTERS.map((s) => (
          <button
            key={s}
            id={`filter-${s}`}
            className={`filter-chip ${filter === s ? "active" : ""}`}
            onClick={() => setFilter(s)}
          >
            {s === "all" ? "All" : s.charAt(0).toUpperCase() + s.slice(1)}
            {stats && s !== "all" && (
              <span style={{ marginLeft: 4, opacity: 0.7 }}>
                {stats.by_status[s]}
              </span>
            )}
          </button>
        ))}
      </div>

      {error && <div className="alert alert-error">{error}</div>}

      {loading ? (
        <div className="loader">
          <div className="spinner" /> Loading…
        </div>
      ) : jobs.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">📋</div>
          <h3>No applications yet</h3>
          <p>
            {filter === "all"
              ? "Click «Add Application» to log your first one."
              : `No applications with status "${filter}".`}
          </p>
        </div>
      ) : (
        <div className="jobs-list">
          {jobs.map((job) => (
            <JobCard key={job.id} job={job} />
          ))}
        </div>
      )}
    </div>
  );
}
