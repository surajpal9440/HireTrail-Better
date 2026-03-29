const BASE_URL = "http://localhost:5000/api/auth";

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
    const err = new Error(data.error || "Request failed");
    err.details = data.details || null;
    err.status = res.status;
    throw err;
  }
  return data;
}

export const authApi = {
  login: (email, password) => request("POST", "/login", { email, password }),
  register: (name, email, password) => request("POST", "/register", { name, email, password }),
  getMe: () => request("GET", "/me"),
};
