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

      <div className="hero-left">

        <span className="badge">
          🚀 AI Powered Security Review
        </span>

        <h1>
          Intelligent Pull Request Reviews
        </h1>

        <p>
          AutoSecAI analyzes GitHub Pull Requests using multiple AI agents
          for Security, Code Quality, Performance, Testing and Documentation.
        </p>

        <button className="hero-btn" onClick={scrollToAnalysis}>
          Start Analysis →
        </button>

      </div>

      <div className="hero-right">

        <div className="card">

          <h3>AI Agents</h3>

          <ul>
            <li>🛡 Security</li>
            <li>💻 Code Quality</li>
            <li>⚡ Performance</li>
            <li>🧪 Testing</li>
            <li>📝 Documentation</li>
          </ul>

        </div>

      </div>

    </section>
  );
}

export default Hero;