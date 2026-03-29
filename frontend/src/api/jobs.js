const BASE_URL = "http://localhost:5000/api/jobs";

async function request(method, path = "", body = null) {
  const options = {
    method,
    headers: { "Content-Type": "application/json" },
  };

  const token = localStorage.getItem("hiretrail_token");
  if (token) {
    options.headers["Authorization"] = `Bearer ${token}`;
  }

  if (body !== null) {
    options.body = JSON.stringify(body);
  }

  const res = await fetch(`${BASE_URL}${path}`, options);
  const data = await res.json();

  if (!res.ok || !data.success) {
    if (res.status === 401) {
      localStorage.removeItem("hiretrail_token");
      window.location.href = "/login";
    }
    const err = new Error(data.error || "Request failed");
    err.details = data.details || null;
    err.status = res.status;
    throw err;
  }
  return data;
}

export const jobsApi = {
  getAll: (status) => request("GET", status ? `?status=${status}` : ""),
  getById: (id) => request("GET", `/${id}`),
  getStats: () => request("GET", "/stats"),
  create: (payload) => request("POST", "", payload),
  update: (id, payload) => request("PUT", `/${id}`, payload),
  remove: (id) => request("DELETE", `/${id}`),
};
