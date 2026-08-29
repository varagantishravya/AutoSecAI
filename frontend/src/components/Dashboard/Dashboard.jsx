import "./Dashboard.css";
import useReviewHistory from "../../hooks/useReviewHistory";
import StatusBadge from "../common/StatusBadge";

/**
 * Dashboard — shows past review history and aggregate stats.
 */
function Dashboard() {
  const { reviews, loading, error, refresh } = useReviewHistory();

  // ── Aggregate stats ──────────────────────────────────────────
  const totalReviews = reviews.length;

  const avgScore =
    totalReviews > 0
      ? (
          reviews.reduce((sum, r) => {
            const match = (r.overall_score || "0").match(/([\d.]+)/);
            return sum + (match ? parseFloat(match[1]) : 0);
          }, 0) / totalReviews
        ).toFixed(1)
      : "—";

  const recommendationCounts = {};
  reviews.forEach((r) => {
    const rec = r.recommendation || "Unknown";
    recommendationCounts[rec] = (recommendationCounts[rec] || 0) + 1;
  });
  const topRecommendation =
    Object.entries(recommendationCounts).sort((a, b) => b[1] - a[1])[0]?.[0] ||
    "—";

  return (
    <section className="dashboard" id="dashboard">
      <h2>Review History</h2>

      {/* Stats bar */}
      <div className="dashboard-stats">
        <div className="stat-card">
          <span className="stat-value">{totalReviews}</span>
          <span className="stat-label">Total Reviews</span>
        </div>
        <div className="stat-card">
          <span className="stat-value">{avgScore}</span>
          <span className="stat-label">Avg Score</span>
        </div>
        <div className="stat-card">
          <span className="stat-value">{topRecommendation}</span>
          <span className="stat-label">Most Common</span>
        </div>
      </div>

      {/* Refresh button */}
      <button className="dashboard-refresh" onClick={refresh} disabled={loading}>
        {loading ? "Loading…" : "↻ Refresh"}
      </button>

      {/* Error state */}
      {error && <p className="dashboard-error">{error}</p>}

      {/* Empty state */}
      {!loading && !error && reviews.length === 0 && (
        <p className="dashboard-empty">
          No reviews yet. Run your first analysis above! 🚀
        </p>
      )}

      {/* Reviews table */}
      {reviews.length > 0 && (
        <div className="dashboard-table-wrap">
          <table className="dashboard-table">
            <thead>
              <tr>
                <th>#</th>
                <th>Repository</th>
                <th>PR</th>
                <th>Score</th>
                <th>Critical</th>
                <th>High</th>
                <th>Medium</th>
                <th>Low</th>
                <th>Recommendation</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              {reviews.map((r) => (
                <tr key={r.id}>
                  <td>{r.id}</td>
                  <td className="td-repo">
                    {r.owner}/{r.repo}
                  </td>
                  <td>#{r.pull_request}</td>
                  <td className="td-score">{r.overall_score}</td>
                  <td>
                    {r.critical > 0 ? (
                      <StatusBadge severity="critical" count={r.critical} />
                    ) : (
                      <span className="td-zero">0</span>
                    )}
                  </td>
                  <td>
                    {r.high > 0 ? (
                      <StatusBadge severity="high" count={r.high} />
                    ) : (
                      <span className="td-zero">0</span>
                    )}
                  </td>
                  <td>
                    {r.medium > 0 ? (
                      <StatusBadge severity="medium" count={r.medium} />
                    ) : (
                      <span className="td-zero">0</span>
                    )}
                  </td>
                  <td>
                    {r.low > 0 ? (
                      <StatusBadge severity="low" count={r.low} />
                    ) : (
                      <span className="td-zero">0</span>
                    )}
                  </td>
                  <td>{r.recommendation}</td>
                  <td className="td-date">
                    {new Date(r.created_at).toLocaleDateString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}

export default Dashboard;
