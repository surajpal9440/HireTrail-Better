import { useState } from "react";
import { ALL_STATUSES, STATUS_LABELS } from "../utils/formatters";

const EMPTY_FORM = {
  company: "",
  position: "",
  location: "",
  status: "applied",
  applied_date: new Date().toISOString().split("T")[0],
  salary_range: "",
  job_url: "",
  notes: "",
};

function validate(data) {
  const errors = {};
  if (!data.company.trim()) errors.company = "Company is required";
  if (!data.position.trim()) errors.position = "Position is required";
  if (!data.applied_date) errors.applied_date = "Applied date is required";
  if (data.job_url && !/^https?:\/\/.+/.test(data.job_url)) {
    errors.job_url = "Must be a valid URL (start with http/https)";
  }
  return errors;
}

export default function JobForm({ initialData = {}, onSubmit, onCancel, loading }) {
  const [form, setForm] = useState({ ...EMPTY_FORM, ...initialData });
  const [errors, setErrors] = useState({});
  const [serverErrors, setServerErrors] = useState(null);

  function handleChange(e) {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
    if (errors[name]) setErrors((prev) => ({ ...prev, [name]: undefined }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setServerErrors(null);
    const validationErrors = validate(form);
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }
    const payload = {
      company: form.company.trim(),
      position: form.position.trim(),
      location: form.location.trim() || null,
      status: form.status,
      applied_date: form.applied_date,
      salary_range: form.salary_range.trim() || null,
      job_url: form.job_url.trim() || null,
      notes: form.notes.trim() || null,
    };
    try {
      await onSubmit(payload);
    } catch (err) {
      setServerErrors(err.message || "Something went wrong");
    }
  }

  return (
    <form onSubmit={handleSubmit} noValidate>
      {serverErrors && <div className="alert alert-error">{serverErrors}</div>}
      <div className="form-grid">
        <div className="form-row">
          <div className="form-group">
            <label htmlFor="field-company">Company <span className="required">*</span></label>
            <input
              id="field-company"
              className="form-control"
              name="company"
              value={form.company}
              onChange={handleChange}
              placeholder="e.g. Google"
            />
            {errors.company && <span className="form-error">{errors.company}</span>}
          </div>
          <div className="form-group">
            <label htmlFor="field-position">Position <span className="required">*</span></label>
            <input
              id="field-position"
              className="form-control"
              name="position"
              value={form.position}
              onChange={handleChange}
              placeholder="e.g. Backend Engineer"
            />
            {errors.position && <span className="form-error">{errors.position}</span>}
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="field-location">Location</label>
            <input
              id="field-location"
              className="form-control"
              name="location"
              value={form.location}
              onChange={handleChange}
              placeholder="e.g. Remote, New York"
            />
          </div>
          <div className="form-group">
            <label htmlFor="field-status">Status</label>
            <select id="field-status" className="form-control" name="status" value={form.status} onChange={handleChange}>
              {ALL_STATUSES.map((s) => (
                <option key={s} value={s}>{STATUS_LABELS[s]}</option>
              ))}
            </select>
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="field-applied-date">Applied Date <span className="required">*</span></label>
            <input
              id="field-applied-date"
              className="form-control"
              type="date"
              name="applied_date"
              value={form.applied_date}
              onChange={handleChange}
            />
            {errors.applied_date && <span className="form-error">{errors.applied_date}</span>}
          </div>
          <div className="form-group">
            <label htmlFor="field-salary">Salary Range</label>
            <input
              id="field-salary"
              className="form-control"
              name="salary_range"
              value={form.salary_range}
              onChange={handleChange}
              placeholder="e.g. 80k–100k"
            />
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="field-url">Job URL</label>
          <input
            id="field-url"
            className="form-control"
            name="job_url"
            type="url"
            value={form.job_url}
            onChange={handleChange}
            placeholder="https://careers.company.com/..."
          />
          {errors.job_url && <span className="form-error">{errors.job_url}</span>}
        </div>

        <div className="form-group">
          <label htmlFor="field-notes">Notes</label>
          <textarea
            id="field-notes"
            className="form-control"
            name="notes"
            value={form.notes}
            onChange={handleChange}
            placeholder="Recruiter contact, interview tips, follow-up dates..."
          />
        </div>

        <div className="form-actions">
          {onCancel && (
            <button type="button" className="btn btn-secondary" onClick={onCancel}>
              Cancel
            </button>
          )}
          <button
            id="btn-submit-job"
            type="submit"
            className="btn btn-primary"
            disabled={loading}
          >
            {loading ? "Saving…" : "Save Application"}
          </button>
        </div>
      </div>
    </form>
  );
}
