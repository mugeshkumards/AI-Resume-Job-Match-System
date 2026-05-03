import ScoreGauge from './ScoreGauge';

export default function JobMatchPanel({ data }) {
  const { overall_score = 0, keyword_match = 0, skill_match = 0, experience_match = 0, education_match = 0, matched_skills = [], missing_skills = [], match_summary = '', strengths = [], gaps = [], fit_assessment = '' } = data || {};

  const bars = [
    { label: 'Keyword Match', value: keyword_match, color: 'var(--info)' },
    { label: 'Skill Match', value: skill_match, color: 'var(--accent-primary)' },
    { label: 'Experience Match', value: experience_match, color: 'var(--success)' },
    { label: 'Education Match', value: education_match, color: 'var(--accent-secondary)' },
  ];

  return (
    <div className="slide-up">
      <div className="grid-2" style={{ marginBottom: 24 }}>
        <div className="card" style={{ textAlign: 'center' }}>
          <ScoreGauge score={overall_score} label="Overall Match" color={overall_score >= 70 ? 'var(--success)' : overall_score >= 40 ? 'var(--warning)' : 'var(--danger)'} />
          {fit_assessment && <p style={{ marginTop: 16, fontSize: 13, color: 'var(--text-secondary)', lineHeight: 1.6 }}>{fit_assessment}</p>}
        </div>

        <div className="card">
          <h3 style={{ marginBottom: 20, fontSize: 15 }}>Score Breakdown</h3>
          <div className="score-bar-group">
            {bars.map((b) => (
              <div key={b.label} className="score-bar">
                <div className="score-bar-header">
                  <span>{b.label}</span>
                  <span style={{ color: b.color }}>{Math.round(b.value)}/100</span>
                </div>
                <div className="score-bar-track">
                  <div className="score-bar-fill" style={{ width: `${b.value}%`, background: b.color }} />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="grid-2">
        <div className="card">
          <div className="card-header">
            <div className="card-icon" style={{ background: 'rgba(16,185,129,0.15)', color: 'var(--success)' }}>✅</div>
            <div><h3>Matched Skills</h3></div>
          </div>
          <div className="tags-container">
            {matched_skills.map((s, i) => <span key={i} className="tag tag-success">{s}</span>)}
          </div>
        </div>

        <div className="card">
          <div className="card-header">
            <div className="card-icon" style={{ background: 'rgba(239,68,68,0.15)', color: 'var(--danger)' }}>❌</div>
            <div><h3>Missing Skills</h3></div>
          </div>
          <div className="tags-container">
            {missing_skills.map((s, i) => <span key={i} className="tag tag-danger">{s}</span>)}
          </div>
        </div>
      </div>

      {(strengths.length > 0 || gaps.length > 0) && (
        <div className="grid-2" style={{ marginTop: 24 }}>
          <div className="card">
            <h3 style={{ marginBottom: 12, fontSize: 15 }}>💪 Strengths</h3>
            {strengths.map((s, i) => (
              <div key={i} className="issue-item low">
                <div className="issue-text"><p>{s}</p></div>
              </div>
            ))}
          </div>
          <div className="card">
            <h3 style={{ marginBottom: 12, fontSize: 15 }}>🔧 Gaps to Address</h3>
            {gaps.map((g, i) => (
              <div key={i} className="issue-item medium">
                <div className="issue-text"><p>{g}</p></div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
