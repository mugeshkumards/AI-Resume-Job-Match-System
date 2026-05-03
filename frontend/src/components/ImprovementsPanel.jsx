export default function ImprovementsPanel({ data }) {
  const { bullet_improvements = [], keyword_suggestions = [], ats_rewrites = [], general_tips = [], summary_improvement = '', formatting_tips = [] } = data || {};

  return (
    <div className="slide-up">
      {summary_improvement && (
        <div className="card" style={{ marginBottom: 24 }}>
          <div className="card-header">
            <div className="card-icon" style={{ background: 'rgba(99,102,241,0.15)', color: 'var(--accent-primary)' }}>📝</div>
            <div><h3>Suggested Professional Summary</h3></div>
          </div>
          <p style={{ fontSize: 14, color: 'var(--text-secondary)', lineHeight: 1.7, padding: 12, background: 'rgba(16,185,129,0.05)', borderLeft: '3px solid var(--success)', borderRadius: 4 }}>{summary_improvement}</p>
        </div>
      )}

      {bullet_improvements.length > 0 && (
        <div className="card" style={{ marginBottom: 24 }}>
          <div className="card-header">
            <div className="card-icon" style={{ background: 'rgba(245,158,11,0.15)', color: 'var(--warning)' }}>✍️</div>
            <div><h3>Bullet Point Improvements ({bullet_improvements.length})</h3></div>
          </div>
          {bullet_improvements.map((item, i) => (
            <div key={i} className="improvement-card">
              <div className="original">❌ {item.original}</div>
              <div className="improved">✅ {item.improved}</div>
              {item.reason && <div className="reason">💡 {item.reason}</div>}
            </div>
          ))}
        </div>
      )}

      <div className="grid-2">
        {keyword_suggestions.length > 0 && (
          <div className="card">
            <div className="card-header">
              <div className="card-icon" style={{ background: 'rgba(59,130,246,0.15)', color: 'var(--info)' }}>🔑</div>
              <div><h3>Keywords to Add</h3></div>
            </div>
            <div className="tags-container">
              {keyword_suggestions.map((k, i) => <span key={i} className="tag tag-info">{k}</span>)}
            </div>
          </div>
        )}

        {general_tips.length > 0 && (
          <div className="card">
            <div className="card-header">
              <div className="card-icon" style={{ background: 'rgba(16,185,129,0.15)', color: 'var(--success)' }}>💡</div>
              <div><h3>General Tips</h3></div>
            </div>
            {general_tips.map((tip, i) => (
              <div key={i} style={{ padding: '8px 0', fontSize: 13, color: 'var(--text-secondary)', borderBottom: i < general_tips.length - 1 ? '1px solid var(--border-color)' : 'none' }}>
                • {tip}
              </div>
            ))}
          </div>
        )}
      </div>

      {formatting_tips.length > 0 && (
        <div className="card" style={{ marginTop: 24 }}>
          <div className="card-header">
            <div className="card-icon" style={{ background: 'rgba(139,92,246,0.15)', color: 'var(--accent-secondary)' }}>📐</div>
            <div><h3>Formatting Tips</h3></div>
          </div>
          {formatting_tips.map((tip, i) => (
            <div key={i} style={{ padding: '8px 0', fontSize: 13, color: 'var(--text-secondary)' }}>• {tip}</div>
          ))}
        </div>
      )}
    </div>
  );
}
