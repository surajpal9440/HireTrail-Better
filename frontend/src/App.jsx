import { BrowserRouter, Routes, Route, NavLink, Outlet } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import Board from "./pages/Board";
import AddJob from "./pages/AddJob";
import JobDetail from "./pages/JobDetail";
import Login from "./pages/Login";
import Register from "./pages/Register";
import ProtectedRoute from "./components/ProtectedRoute";
import { AuthProvider, useAuth } from "./context/AuthContext";

function Sidebar() {
  const { logout, user } = useAuth();

  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <div className="logo-icon">🎯</div>
        <h1>HireTrail</h1>
      </div>
      <nav>
        <NavLink
          to="/"
          end
          id="nav-dashboard"
          className={({ isActive }) => `nav-link ${isActive ? "active" : ""}`}
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/>
            <rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/>
          </svg>
          Dashboard
        </NavLink>
        <NavLink
          to="/board"
          id="nav-board"
          className={({ isActive }) => `nav-link ${isActive ? "active" : ""}`}
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <rect x="3" y="3" width="18" height="18" rx="2"/>
            <line x1="9" y1="3" x2="9" y2="21"/>
            <line x1="15" y1="3" x2="15" y2="21"/>
          </svg>
          Board
        </NavLink>
        <NavLink
          to="/add"
          id="nav-add"
          className={({ isActive }) => `nav-link ${isActive ? "active" : ""}`}
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="9"/>
            <line x1="12" y1="8" x2="12" y2="16"/>
            <line x1="8" y1="12" x2="16" y2="12"/>
          </svg>
          Add Application
        </NavLink>
      </nav>

      <div style={{ marginTop: "auto", padding: "16px", borderTop: "1px solid var(--border)", display: "flex", flexDirection: "column", gap: "12px" }}>
        <div style={{ fontSize: "14px", color: "var(--text-secondary)", wordBreak: "break-all" }}>
          {user?.email}
        </div>
        <button onClick={logout} className="btn btn-secondary" style={{ width: "100%", justifyContent: "center" }}>
          Sign out
        </button>
      </div>
    </aside>
  );
}

function ProtectedLayout() {
  return (
    <div className="layout">
      <Sidebar />
      <main className="main-content">
        <Outlet />
      </main>
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          
          <Route element={<ProtectedRoute><ProtectedLayout /></ProtectedRoute>}>
            <Route path="/" element={<Dashboard />} />
            <Route path="/board" element={<Board />} />
            <Route path="/add" element={<AddJob />} />
            <Route path="/jobs/:id" element={<JobDetail />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
