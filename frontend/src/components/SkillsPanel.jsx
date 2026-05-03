export default function SkillsPanel({ data }) {
  const { normalized_skills = [], skill_categories = {}, missing_skills = [], outdated_skills = [], trending_skills = [], skill_summary = '' } = data || {};

  return (
    <div className="slide-up">
      {skill_summary && (
        <div className="card" style={{ marginBottom: 24 }}>
          <div className="card-header">
            <div className="card-icon" style={{ background: 'rgba(99,102,241,0.15)', color: 'var(--accent-primary)' }}>🧠</div>
            <div><h3>Skill Analysis Summary</h3></div>
          </div>
          <p style={{ fontSize: 14, color: 'var(--text-secondary)', lineHeight: 1.7 }}>{skill_summary}</p>
        </div>
      )}

      <div className="grid-2">
        <div className="card">
          <div className="card-header">
            <div className="card-icon" style={{ background: 'rgba(99,102,241,0.15)', color: 'var(--accent-primary)' }}>📂</div>
            <div><h3>Skill Categories</h3></div>
          </div>
          {Object.entries(skill_categories).map(([cat, skills]) => (
            <div key={cat} style={{ marginBottom: 16 }}>
              <div style={{ fontSize: 13, fontWeight: 600, color: 'var(--text-primary)', marginBottom: 8 }}>{cat}</div>
              <div className="tags-container">
                {(Array.isArray(skills) ? skills : []).map((s, i) => (
                  <span key={i} className="tag tag-purple">{s}</span>
                ))}
              </div>
            </div>
          ))}
        </div>

        <div>
          <div className="card" style={{ marginBottom: 16 }}>
            <div className="card-header">
              <div className="card-icon" style={{ background: 'rgba(239,68,68,0.15)', color: 'var(--danger)' }}>⚠️</div>
              <div><h3>Missing Skills</h3></div>
            </div>
            <div className="tags-container">
              {missing_skills.map((s, i) => <span key={i} className="tag tag-danger">{s}</span>)}
              {!missing_skills.length && <span style={{ fontSize: 13, color: 'var(--text-muted)' }}>No gaps detected!</span>}
            </div>
          </div>

          <div className="card" style={{ marginBottom: 16 }}>
            <div className="card-header">
              <div className="card-icon" style={{ background: 'rgba(245,158,11,0.15)', color: 'var(--warning)' }}>📅</div>
              <div><h3>Outdated Skills</h3></div>
            </div>
            <div className="tags-container">
              {outdated_skills.map((s, i) => <span key={i} className="tag tag-warning">{s}</span>)}
              {!outdated_skills.length && <span style={{ fontSize: 13, color: 'var(--text-muted)' }}>All skills look current!</span>}
            </div>
          </div>

          <div className="card">
            <div className="card-header">
              <div className="card-icon" style={{ background: 'rgba(16,185,129,0.15)', color: 'var(--success)' }}>🔥</div>
              <div><h3>Trending Skills to Learn</h3></div>
            </div>
            <div className="tags-container">
              {trending_skills.map((s, i) => <span key={i} className="tag tag-success">{s}</span>)}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
