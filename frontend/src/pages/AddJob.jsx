import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { jobsApi } from "../api/jobs";
import JobForm from "../components/JobForm";

export default function AddJob() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  async function handleSubmit(payload) {
    setLoading(true);
    try {
      const res = await jobsApi.create(payload);
      navigate(`/jobs/${res.data.id}`);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <button className="back-link" onClick={() => navigate(-1)}>
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <polyline points="15 18 9 12 15 6"/>
        </svg>
        Back
      </button>
      <div className="page-header">
        <div>
          <h2>Add Application</h2>
          <p>Log a new job application</p>
        </div>
      </div>
      <div className="form-card">
        <JobForm onSubmit={handleSubmit} onCancel={() => navigate(-1)} loading={loading} />
      </div>
    </div>
  );
}
