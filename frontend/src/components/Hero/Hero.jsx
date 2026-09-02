import "./Hero.css";

function Hero() {
  function scrollToAnalysis() {
    const analysisSection = document.getElementById("analysis");
    if (analysisSection) {
      analysisSection.scrollIntoView({ behavior: "smooth" });
    }
  }

  return (
    <section className="hero">
      <div className="hero-backdrop-glow"></div>

      <div className="hero-left">
        <span className="badge">
          ⚡ Multi-Agent LLM PR Intelligence
        </span>

        <h1>
          Automated Code Review <span className="gradient-text">&amp; Security Shield</span>
        </h1>

        <p>
          AutoSecAI inspects your GitHub Pull Requests concurrently with six specialized AI agents for 
          Security vulnerabilities, Code Quality, Performance bottlenecks, Testing gaps, and Documentation coverage.
        </p>

        <div className="hero-actions">
          <button className="hero-btn primary" onClick={scrollToAnalysis}>
            🚀 Start PR Analysis
          </button>
          <a href="#dashboard" className="hero-btn secondary">
            📊 View History
          </a>
        </div>

        <div className="hero-metrics">
          <div className="metric-item">
            <span className="metric-val">6</span>
            <span className="metric-lbl">Specialist Agents</span>
          </div>
          <div className="metric-divider"></div>
          <div className="metric-item">
            <span className="metric-val">OWASP</span>
            <span className="metric-lbl">Vector RAG Store</span>
          </div>
          <div className="metric-divider"></div>
          <div className="metric-item">
            <span className="metric-val">100%</span>
            <span className="metric-lbl">User Isolated</span>
          </div>
        </div>
      </div>

      <div className="hero-right">
        <div className="card glass-card">
          <div className="card-header">
            <h3>Active AI Agent Cluster</h3>
            <span className="live-dot"></span>
          </div>

          <ul className="agent-list">
            <li>
              <span className="agent-icon sec">🛡️</span>
              <div className="agent-info">
                <strong>Security Agent</strong>
                <span>OWASP &amp; Secret Detection</span>
              </div>
              <span className="agent-status-tag">Active</span>
            </li>
            <li>
              <span className="agent-icon qual">💻</span>
              <div className="agent-info">
                <strong>Code Quality Agent</strong>
                <span>PEP 8 &amp; Anti-Pattern Audit</span>
              </div>
              <span className="agent-status-tag">Active</span>
            </li>
            <li>
              <span className="agent-icon perf">⚡</span>
              <div className="agent-info">
                <strong>Performance Agent</strong>
                <span>Complexity &amp; I/O Bottlenecks</span>
              </div>
              <span className="agent-status-tag">Active</span>
            </li>
            <li>
              <span className="agent-icon test">🧪</span>
              <div className="agent-info">
                <strong>Testing Agent</strong>
                <span>Automated Unit Test Generator</span>
              </div>
              <span className="agent-status-tag">Active</span>
            </li>
            <li>
              <span className="agent-icon doc">📝</span>
              <div className="agent-info">
                <strong>Documentation Agent</strong>
                <span>Coverage &amp; Type Hints</span>
              </div>
              <span className="agent-status-tag">Active</span>
            </li>
            <li>
              <span className="agent-icon sum">📊</span>
              <div className="agent-info">
                <strong>Summary Agent</strong>
                <span>Synthesis &amp; Score Calculation</span>
              </div>
              <span className="agent-status-tag">Active</span>
            </li>
          </ul>
        </div>
      </div>
    </section>
  );
}

export default Hero;