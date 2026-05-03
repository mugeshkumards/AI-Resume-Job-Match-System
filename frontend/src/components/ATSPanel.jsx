import ScoreGauge from './ScoreGauge';

export default function ATSPanel({ data }) {
  const { overall_score = 0, keyword_score = 0, format_score = 0, readability_score = 0, content_score = 0, style_score = 0, sections_score = 0, issues = [], strengths = [], overall_assessment = '' } = data || {};

  const categories = [
    { label: 'Keywords', value: keyword_score, icon: '🔑' },
    { label: 'Format', value: format_score, icon: '📐' },
    { label: 'Readability', value: readability_score, icon: '📖' },
    { label: 'Content', value: content_score, icon: '📝' },
    { label: 'Style', value: style_score, icon: '🎨' },
    { label: 'Sections', value: sections_score, icon: '📋' },
  ];

  const getColor = (v) => v >= 70 ? 'var(--success)' : v >= 40 ? 'var(--warning)' : 'var(--danger)';

  return (
    <div className="slide-up">
      <div className="card" style={{ marginBottom: 24, textAlign: 'center' }}>
        <ScoreGauge score={overall_score} label="ATS Compatibility Score" color={getColor(overall_score)} />
        {overall_assessment && <p style={{ marginTop: 16, fontSize: 14, color: 'var(--text-secondary)', maxWidth: 600, margin: '16px auto 0', lineHeight: 1.6 }}>{overall_assessment}</p>}
      </div>

      <div className="grid-3" style={{ marginBottom: 24 }}>
        {categories.map((c) => (
          <div key={c.label} className="card" style={{ textAlign: 'center', padding: 20 }}>
            <div style={{ fontSize: 24, marginBottom: 8 }}>{c.icon}</div>
            <div style={{ fontSize: 28, fontWeight: 800, color: getColor(c.value) }}>{Math.round(c.value)}</div>
            <div style={{ fontSize: 12, color: 'var(--text-muted)', marginTop: 4 }}>{c.label}</div>
            <div className="score-bar-track" style={{ marginTop: 8 }}>
              <div className="score-bar-fill" style={{ width: `${c.value}%`, background: getColor(c.value) }} />
            </div>
          </div>
        ))}
      </div>

      <div className="grid-2">
        <div className="card">
          <div className="card-header">
            <div className="card-icon" style={{ background: 'rgba(239,68,68,0.15)', color: 'var(--danger)' }}>🐛</div>
            <div><h3>Issues Found ({issues.length})</h3></div>
          </div>
          {issues.map((issue, i) => (
            <div key={i} className={`issue-item ${issue.severity || 'medium'}`}>
              <div className="issue-text">
                <h4>{issue.category || 'General'}</h4>
                <p>{issue.issue}</p>
                {issue.fix && <p style={{ color: 'var(--success)', marginTop: 4 }}>💡 Fix: {issue.fix}</p>}
              </div>
            </div>
          ))}
          {!issues.length && <p style={{ color: 'var(--text-muted)', fontSize: 13 }}>No issues found!</p>}
        </div>

        <div className="card">
          <div className="card-header">
            <div className="card-icon" style={{ background: 'rgba(16,185,129,0.15)', color: 'var(--success)' }}>✅</div>
            <div><h3>Strengths ({strengths.length})</h3></div>
          </div>
          {strengths.map((s, i) => (
            <div key={i} className="issue-item low">
              <div className="issue-text"><p>{s}</p></div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
