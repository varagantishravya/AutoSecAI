import { useState, useEffect } from "react";
import api from "../../services/api";
import "./Navbar.css";

function Navbar() {
  const [user, setUser] = useState(null);
  const [showPatModal, setShowPatModal] = useState(false);
  const [patInput, setPatInput] = useState("");
  const [patError, setPatError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchUserProfile();
  }, []);

  async function fetchUserProfile() {
    const token = localStorage.getItem("github_token");
    if (!token) {
      setUser(null);
      return;
    }

    try {
      const response = await api.get("/auth/me");
      setUser(response.data);
    } catch (err) {
      console.error("Failed to fetch user profile:", err);
      // Token might be invalid or expired
      localStorage.removeItem("github_token");
      setUser(null);
    }
  }

  async function handlePatSubmit(e) {
    e.preventDefault();
    if (!patInput.trim()) return;

    try {
      setLoading(true);
      setPatError("");
      const response = await api.post("/auth/pat", { token: patInput.trim() });
      localStorage.setItem("github_token", response.data.token);
      setUser(response.data);
      setShowPatModal(false);
      setPatInput("");
      // Notify other components (Analysis, Dashboard) to refresh
      window.dispatchEvent(new Event("user-auth-changed"));
    } catch (err) {
      setPatError(err.response?.data?.detail || "Invalid Token. Please check and try again.");
    } finally {
      setLoading(false);
    }
  }

  function handleLogout() {
    localStorage.removeItem("github_token");
    setUser(null);
    window.dispatchEvent(new Event("user-auth-changed"));
  }

  return (
    <nav className="navbar">
      <div className="logo">
        <div className="logo-icon">A</div>
        <div className="logo-text">
          <h2>AutoSecAI</h2>
          <span>AI Pull Request Review</span>
        </div>
      </div>

      <ul className="nav-links">
        <li><a href="#dashboard" style={{ color: "inherit", textDecoration: "none" }}>Dashboard</a></li>
        <li><a href="#analysis" style={{ color: "inherit", textDecoration: "none" }}>Analysis</a></li>
      </ul>

      <div className="auth-section">
        {user ? (
          <div className="user-profile">
            {user.avatar_url && (
              <img src={user.avatar_url} alt={user.username} className="user-avatar" />
            )}
            <span className="user-name">@{user.username}</span>
            <button className="logout-btn" onClick={handleLogout}>
              Sign Out
            </button>
          </div>
        ) : (
            <button
              className="login-btn"
              onClick={() => {
                setShowPatModal(true);
              }}
            >
              Sign In with GitHub / Token
            </button>

        )}
      </div>

      {/* PAT Modal */}
      {showPatModal && (
        <div className="pat-modal-overlay">
          <div className="pat-modal">
            <h3>Sign In with GitHub Token</h3>
            <p>
              Enter your GitHub Personal Access Token (`ghp_...`) to load your private and public repositories.
              <br />
              <a
                href="https://github.com/settings/tokens/new?scopes=repo,user&description=AutoSecAI"
                target="_blank"
                rel="noreferrer"
                style={{ color: "#38bdf8", fontSize: "13px", marginTop: "6px", display: "inline-block" }}
              >
                👉 Click here to generate a GitHub Token (10 seconds)
              </a>
            </p>

            <form onSubmit={handlePatSubmit}>
              <input
                type="password"
                placeholder="ghp_xxxxxxxxxxxxxxxxxxxx"
                value={patInput}
                onChange={(e) => setPatInput(e.target.value)}
                className="pat-input"
              />
              {patError && <p className="pat-error">{patError}</p>}
              <div className="modal-actions">
                <button type="submit" className="login-btn" disabled={loading}>
                  {loading ? "Validating..." : "Save & Authenticate"}
                </button>
                <button
                  type="button"
                  className="cancel-btn"
                  onClick={() => setShowPatModal(false)}
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </nav>
  );
}

export default Navbar;