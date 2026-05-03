export default function ScoreGauge({ score, label, color, max = 100, isCount = false }) {
  const pct = isCount ? Math.min((score / max) * 100, 100) : Math.min(score, 100);
  const circumference = 2 * Math.PI * 54;
  const offset = circumference - (pct / 100) * circumference;

  return (
    <div className="score-gauge">
      <div className="gauge-ring">
        <svg width="140" height="140" viewBox="0 0 120 120">
          <circle cx="60" cy="60" r="54" fill="none" stroke="var(--bg-secondary)" strokeWidth="8" />
          <circle
            cx="60" cy="60" r="54" fill="none" stroke={color} strokeWidth="8"
            strokeDasharray={circumference} strokeDashoffset={offset}
            strokeLinecap="round"
            style={{ transition: 'stroke-dashoffset 1.5s ease', transform: 'rotate(-90deg)', transformOrigin: '50% 50%' }}
          />
        </svg>
        <div style={{ position: 'absolute', textAlign: 'center' }}>
          <div className="gauge-value" style={{ color }}>{Math.round(score)}</div>
          {!isCount && <div style={{ fontSize: 12, color: 'var(--text-muted)' }}>/ {max}</div>}
        </div>
      </div>
      <div className="gauge-label">{label}</div>
    </div>
  );
}
