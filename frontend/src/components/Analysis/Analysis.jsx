import "./Analysis.css";
import { useEffect, useState } from "react";
import api from "../../services/api";
import ScoreGauge from "../common/ScoreGauge";
import StatusBadge from "../common/StatusBadge";

function Analysis() {

  const [repositories, setRepositories] = useState([]);
  const [pullRequests, setPullRequests] = useState([]);

  const [selectedRepository, setSelectedRepository] = useState("");
  // Track the owner that belongs to the selected repository
  const [selectedOwner, setSelectedOwner] = useState("");
  const [selectedPullRequest, setSelectedPullRequest] = useState("");
  const [loading, setLoading] = useState(false);
  const [reviewResult, setReviewResult] = useState(null);
  const [commenting, setCommenting] = useState(false);
  const [commentPosted, setCommentPosted] = useState(false);

  async function handlePostComment() {
    if (!selectedRepository || !selectedPullRequest || !reviewResult) return;
    try {
      setCommenting(true);
      const summaryText = `## 🤖 AutoSecAI Multi-Agent PR Review
**Overall Score**: ${reviewResult.summary.overall_score}
**Recommendation**: ${reviewResult.summary.recommendation}

| Severity | Count |
| --- | --- |
| 🚨 Critical | ${reviewResult.summary.critical} |
| ⚠️ High | ${reviewResult.summary.high} |
| 🟡 Medium | ${reviewResult.summary.medium} |
| 🟢 Low | ${reviewResult.summary.low} |

*Generated automatically by AutoSecAI.*`;

      await api.post("/post-comment", {
        owner: selectedOwner,
        repository: selectedRepository,
        pull_request: Number(selectedPullRequest),
        comment: summaryText,
      });
      setCommentPosted(true);
      alert("Successfully posted review comment directly to GitHub PR! 🎉");
    } catch (err) {
      console.error(err);
      alert("Failed to post comment to GitHub. Make sure your token has repo access permissions.");
    } finally {
      setCommenting(false);
    }
  }


  useEffect(() => {
    loadRepositories();

    function handleAuthChange() {
      setSelectedRepository("");
      setSelectedOwner("");
      setSelectedPullRequest("");
      setPullRequests([]);
      loadRepositories();
    }

    window.addEventListener("user-auth-changed", handleAuthChange);
    return () => window.removeEventListener("user-auth-changed", handleAuthChange);
  }, []);

  async function loadRepositories() {
    try {
      const response = await api.get("/repositories");
      setRepositories(response.data || []);
    } catch (error) {
      console.error("Error loading repositories:", error);
      setRepositories([]);
    }
  }


  async function loadPullRequests(owner, repository) {
    try {
      const response = await api.get("/pull-requests", {
        params: {
          owner: owner,
          repo: repository,
        },
      });

      setPullRequests(response.data);
    } catch (error) {
      console.error("Error loading pull requests:", error);
      setPullRequests([]);
    }
  }

  async function analyzePullRequest() {
    console.log("Analyze button clicked");

    if (!selectedRepository || !selectedPullRequest) {
      alert("Please select both Repository and Pull Request");
      return;
    }

    try {
      setLoading(true);

      const response = await api.post("/review", {
        owner: selectedOwner,
        repository: selectedRepository,
        pull_request: Number(selectedPullRequest),
      });

      console.log(response.data);
      setReviewResult(response.data);

    } catch (error) {
      console.error(error);
      alert("Analysis Failed. Please check the backend is running and try again.");
    } finally {
      setLoading(false);
    }
  }

  function handleRepositoryChange(event) {
    const repoName = event.target.value;

    // Find the full repo object to get the owner
    const repoObj = repositories.find((r) => r.name === repoName);

    setSelectedRepository(repoName);
    setSelectedOwner(repoObj ? repoObj.owner : "");
    setSelectedPullRequest("");

    if (repoName !== "" && repoObj) {
      loadPullRequests(repoObj.owner, repoName);
    } else {
      setPullRequests([]);
    }
  }

  return (
    // id="analysis" allows the Hero "Start Analysis" button to scroll here
    <section className="analysis" id="analysis">

      <div className="analysis-card">

        <h2>Analyze GitHub Pull Request</h2>

        <div className="input-group">

          <label>Repository</label>

          <select
            value={selectedRepository}
            onChange={handleRepositoryChange}
          >
            <option value="">Select Repository</option>

            {repositories.map((repo) => (
              <option
                key={repo.name}
                value={repo.name}
              >
                {repo.owner}/{repo.name}
              </option>
            ))}

          </select>

        </div>

        <div className="input-group">

          <label>Pull Request</label>

          <select
            value={selectedPullRequest}
            onChange={(e) => setSelectedPullRequest(e.target.value)}
            disabled={!selectedRepository}
          >

            <option value="">
              {selectedRepository ? "Select Pull Request" : "Select a repository first"}
            </option>

            {pullRequests.map((pr) => (
              <option
                key={pr.number}
                value={pr.number}
              >
                #{pr.number} - {pr.title}
              </option>
            ))}

          </select>

        </div>

        <button
          className="analyze-btn"
          onClick={analyzePullRequest}
          disabled={loading}
        >

          {loading ? "Analyzing... (this may take a few minutes)" : "🚀 Analyze Pull Request"}

        </button>

      </div>

      {reviewResult && (

  <div className="results-card">

    <h2>Review Results</h2>

    <div className="results-summary">

      <div className="results-score-section">
        <ScoreGauge score={reviewResult.summary.overall_score} />
        <p className="results-recommendation">
          {reviewResult.summary.recommendation}
        </p>
      </div>

      <div className="results-severity-section">
        <StatusBadge severity="critical" count={reviewResult.summary.critical} />
        <StatusBadge severity="high" count={reviewResult.summary.high} />
        <StatusBadge severity="medium" count={reviewResult.summary.medium} />
        <StatusBadge severity="low" count={reviewResult.summary.low} />
      </div>

    </div>

    <div style={{ marginTop: "20px", marginBottom: "20px", textAlign: "center", display: "flex", gap: "12px", justifyContent: "center" }}>
      <button 
        className="analyze-btn" 
        onClick={() => {
          const url = `${api.defaults.baseURL}/download-report?repo=${selectedRepository}&pull_request=${selectedPullRequest}`;
          window.open(url, "_blank");
        }}
      >
        📥 Download Full Report
      </button>

      <button
        className="analyze-btn"
        style={{ backgroundColor: commentPosted ? "#10b981" : "#8b5cf6" }}
        onClick={handlePostComment}
        disabled={commenting || commentPosted}
      >
        {commentPosted ? "✓ Posted to GitHub PR" : commenting ? "Posting..." : "💬 Post Review to GitHub PR"}
      </button>
    </div>


    <hr />

    {reviewResult.results.map((result) => (

      <div
        key={result.agent}
        className="agent-result"
      >

        <h3>{result.agent}</h3>

        <pre>{result.analysis}</pre>

      </div>

    ))}

  </div>

)}
    </section>
  );
}

export default Analysis;