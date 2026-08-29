import "./ScoreGauge.css";

/**
 * Animated circular gauge that displays the overall PR score (0-10).
 *
 * Props:
 *   score — string like "7.5/10" or a number 0-10
 */
function ScoreGauge({ score }) {
  // Parse the numeric value
  let numericScore = 0;
  if (typeof score === "string") {
    const match = score.match(/([\d.]+)/);
    numericScore = match ? parseFloat(match[1]) : 0;
  } else if (typeof score === "number") {
    numericScore = score;
  }

  // Clamp to [0, 10]
  numericScore = Math.max(0, Math.min(10, numericScore));

  // SVG circle math
  const radius = 54;
  const circumference = 2 * Math.PI * radius;
  const progress = (numericScore / 10) * circumference;
  const offset = circumference - progress;

  // Colour based on score
  let colour;
  if (numericScore >= 8) colour = "var(--color-score-great, #16a34a)";
  else if (numericScore >= 6) colour = "var(--color-score-good, #65a30d)";
  else if (numericScore >= 4) colour = "var(--color-score-ok, #d97706)";
  else colour = "var(--color-score-bad, #dc2626)";

  return (
    <div className="score-gauge">
      <svg className="score-gauge__svg" viewBox="0 0 120 120">
        {/* Background track */}
        <circle
          className="score-gauge__track"
          cx="60"
          cy="60"
          r={radius}
          fill="none"
          stroke="var(--color-border, #e2e8f0)"
          strokeWidth="10"
        />
        {/* Animated progress arc */}
        <circle
          className="score-gauge__progress"
          cx="60"
          cy="60"
          r={radius}
          fill="none"
          stroke={colour}
          strokeWidth="10"
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          transform="rotate(-90 60 60)"
        />
      </svg>
      <div className="score-gauge__label">
        <span className="score-gauge__value" style={{ color: colour }}>
          {numericScore.toFixed(1)}
        </span>
        <span className="score-gauge__max">/10</span>
      </div>
    </div>
  );
}

export default ScoreGauge;
