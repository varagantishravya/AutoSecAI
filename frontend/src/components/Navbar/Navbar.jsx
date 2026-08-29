import "./Navbar.css";

function Navbar() {
  return (
    <nav className="navbar">

      <div className="logo">

        <div className="logo-icon">
          A
        </div>

        <div className="logo-text">
          <h2>AutoSecAI</h2>
          <span>AI Pull Request Review</span>
        </div>

      </div>

      <ul className="nav-links">
        <li>Dashboard</li>
        <li>Reports</li>
        <li>Documentation</li>
        <li>About</li>
      </ul>

      <button className="login-btn">
        Sign In
      </button>

    </nav>
  );
}

export default Navbar;