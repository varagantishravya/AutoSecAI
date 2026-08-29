import "./StatusBadge.css";

/**
 * Colour-coded badge for severity levels.
 *
 * Props:
 *   severity — one of "critical", "high", "medium", "low"
 *   count    — numeric count to display (optional, shows next to label)
 */
function StatusBadge({ severity, count }) {
  const label = severity.charAt(0).toUpperCase() + severity.slice(1);

  return (
    <span className={`status-badge status-badge--${severity}`}>
      {label}
      {count !== undefined && <span className="status-badge__count">{count}</span>}
    </span>
  );
}

export default StatusBadge;
