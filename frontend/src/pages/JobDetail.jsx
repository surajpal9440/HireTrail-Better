import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { jobsApi } from "../api/jobs";
import StatusBadge from "../components/StatusBadge";
import JobForm from "../components/JobForm";
import { formatDate } from "../utils/formatters";

export default function JobDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [job, setJob] = useState(null);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [error, setError] = useState(null);
  const [confirmDelete, setConfirmDelete] = useState(false);

  useEffect(() => {
    jobsApi
      .getById(id)
      .then((res) => setJob(res.data))
      .catch(() => setError("Job not found or failed to load."))
      .finally(() => setLoading(false));
  }, [id]);

  async function handleUpdate(payload) {
    setSaving(true);
    try {
      const res = await jobsApi.update(id, payload);
      setJob(res.data);
      setEditing(false);
    } finally {
      setSaving(false);
    }
  }

  async function handleDelete() {
    setDeleting(true);
    try {
      await jobsApi.remove(id);
      navigate("/", { replace: true });
    } finally {
      setDeleting(false);
    }
  }

  if (loading) return <div className="loader"><div className="spinner" /> Loading…</div>;
  if (error || !job) return <div className="alert alert-error">{error || "Job not found"}</div>;

  if (editing) {
    return (
      <div>
        <button className="back-link" onClick={() => setEditing(false)}>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <polyline points="15 18 9 12 15 6"/>
          </svg>
          Cancel Edit
        </button>
        <div className="page-header">
          <div><h2>Edit Application</h2></div>
        </div>
        <div className="form-card">
          <JobForm
            initialData={{
              ...job,
              applied_date: job.applied_date || "",
              location: job.location || "",
              salary_range: job.salary_range || "",
              job_url: job.job_url || "",
              notes: job.notes || "",
            }}
            onSubmit={handleUpdate}
            onCancel={() => setEditing(false)}
            loading={saving}
          />
        </div>
      </div>
    );
  }

  return (
    <div>
      <button className="back-link" onClick={() => navigate(-1)}>
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <polyline points="15 18 9 12 15 6"/>
        </svg>
        Back
      </button>

      <div className="detail-card" id={`job-detail-${job.id}`}>
        <div className="detail-header">
          <div>
            <h2>{job.position}</h2>
            <div className="company-name">{job.company}</div>
          </div>
          <StatusBadge status={job.status} />
        </div>

        <div className="detail-body">
          <div className="detail-fields">
            <div className="detail-field">
              <div className="field-label">Applied Date</div>
              <div className="field-value">{formatDate(job.applied_date)}</div>
            </div>
            <div className="detail-field">
              <div className="field-label">Location</div>
              <div className="field-value">{job.location || "—"}</div>
            </div>
            <div className="detail-field">
              <div className="field-label">Salary Range</div>
              <div className="field-value">{job.salary_range || "—"}</div>
            </div>
            <div className="detail-field">
              <div className="field-label">Job Posting</div>
              <div className="field-value">
                {job.job_url ? (
                  <a href={job.job_url} target="_blank" rel="noopener noreferrer">
                    View Posting ↗
                  </a>
                ) : "—"}
              </div>
            </div>
          </div>

          {job.notes && (
            <div>
              <div className="field-label" style={{ marginBottom: 8, fontSize: 11.5, textTransform: "uppercase", letterSpacing: "0.5px", color: "var(--text-muted)", fontWeight: 600 }}>
                Notes
              </div>
              <div className="notes-block">{job.notes}</div>
            </div>
          )}
        </div>

        <div className="detail-actions">
          {confirmDelete ? (
            <>
              <span style={{ color: "var(--text-secondary)", fontSize: 13, alignSelf: "center" }}>
                Are you sure?
              </span>
              <button className="btn btn-secondary btn-sm" onClick={() => setConfirmDelete(false)}>
                Cancel
              </button>
              <button
                id="btn-confirm-delete"
                className="btn btn-danger btn-sm"
                onClick={handleDelete}
                disabled={deleting}
              >
                {deleting ? "Deleting…" : "Yes, Delete"}
              </button>
            </>
          ) : (
            <>
              <button
                id="btn-delete-job"
                className="btn btn-danger btn-sm"
                onClick={() => setConfirmDelete(true)}
              >
                Delete
              </button>
              <button
                id="btn-edit-job"
                className="btn btn-primary btn-sm"
                onClick={() => setEditing(true)}
              >
                Edit
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
