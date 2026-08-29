import "./Footer.css";

function Footer() {
  return (
    <footer className="footer">
      <div className="footer-content">

        <div className="footer-brand">
          <div className="footer-logo">
            <div className="footer-logo-icon">A</div>
            <span className="footer-logo-text">AutoSecAI</span>
          </div>
          <p className="footer-tagline">
            AI-Powered Pull Request Reviews — Security, Quality, Performance,
            Testing & Documentation.
          </p>
        </div>

        <div className="footer-links">
          <h4>Project</h4>
          <ul>
            <li><a href="#analysis">Analysis</a></li>
            <li><a href="#dashboard">Dashboard</a></li>
            <li>
              <a
                href="https://github.com"
                target="_blank"
                rel="noopener noreferrer"
              >
                GitHub
              </a>
            </li>
          </ul>
        </div>

        <div className="footer-links">
          <h4>Tech Stack</h4>
          <ul>
            <li>React + Vite</li>
            <li>FastAPI + Python</li>
            <li>Groq / LLaMA</li>
          </ul>
        </div>

      </div>

      <div className="footer-bottom">
        <p>© {new Date().getFullYear()} AutoSecAI — Built for intelligent code review.</p>
      </div>
    </footer>
  );
}

export default Footer;
