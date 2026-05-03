export default function RecommendationsPanel({ data }) {
  const { recommended_jobs = [], career_paths = [], skill_roadmap = [], industry_insights = '' } = data || {};
  const getColor = (v) => v >= 80 ? 'var(--success)' : v >= 60 ? 'var(--info)' : 'var(--warning)';
  const getPriorityStyle = (p) => {
    const pr = (p || '').toLowerCase();
    if (pr === 'high') return { background: 'rgba(239,68,68,0.15)', color: 'var(--danger)' };
    if (pr === 'medium') return { background: 'rgba(245,158,11,0.15)', color: 'var(--warning)' };
    return { background: 'rgba(59,130,246,0.15)', color: 'var(--info)' };
  };

  return (
    <div className="slide-up">
      {industry_insights && (
        <div className="card" style={{ marginBottom: 24 }}>
          <div className="card-header">
            <div className="card-icon" style={{ background: 'rgba(99,102,241,0.15)', color: 'var(--accent-primary)' }}>📈</div>
            <div><h3>Industry Insights</h3></div>
          </div>
          <p style={{ fontSize: 14, color: 'var(--text-secondary)', lineHeight: 1.7 }}>{industry_insights}</p>
        </div>
      )}

      {recommended_jobs.length > 0 && (
        <div className="card" style={{ marginBottom: 24 }}>
          <div className="card-header">
            <div className="card-icon" style={{ background: 'rgba(16,185,129,0.15)', color: 'var(--success)' }}>💼</div>
            <div><h3>Recommended Jobs</h3></div>
          </div>
          <div className="grid-2">
            {recommended_jobs.map((job, i) => (
              <div key={i} className="job-card">
                <h4>{job.title}</h4>
                <div className="job-meta">{job.company_type} {job.salary_range ? `• ${job.salary_range}` : ''}</div>
                <p style={{ fontSize: 13, color: 'var(--text-secondary)', marginBottom: 10 }}>{job.match_reason}</p>
                <span className="fit-score" style={{ background: `${getColor(job.fit_score)}22`, color: getColor(job.fit_score) }}>
                  {job.fit_score}% fit
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {career_paths.length > 0 && (
        <div className="card" style={{ marginBottom: 24 }}>
          <div className="card-header">
            <div className="card-icon" style={{ background: 'rgba(139,92,246,0.15)', color: 'var(--accent-secondary)' }}>🛤️</div>
            <div><h3>Career Paths</h3></div>
          </div>
          {career_paths.map((cp, i) => (
            <div key={i} style={{ marginBottom: 16 }}>
              <div className="career-path">
                {(cp.path || '').split('→').map((step, j, arr) => (
                  <span key={j}>
                    <span className="career-step">{step.trim()}</span>
                    {j < arr.length - 1 && <span className="career-arrow"> → </span>}
                  </span>
                ))}
              </div>
              <p style={{ fontSize: 13, color: 'var(--text-secondary)', padding: '0 16px' }}>{cp.description} • ⏱️ {cp.timeline}</p>
            </div>
          ))}
        </div>
      )}

      {skill_roadmap.length > 0 && (
        <div className="card">
          <div className="card-header">
            <div className="card-icon" style={{ background: 'rgba(59,130,246,0.15)', color: 'var(--info)' }}>🗺️</div>
            <div><h3>Skill Roadmap</h3></div>
          </div>
          {skill_roadmap.map((item, i) => (
            <div key={i} className="roadmap-item">
              <span className="roadmap-priority" style={getPriorityStyle(item.priority)}>{item.priority}</span>
              <div>
                <h4>{item.skill}</h4>
                <p>{item.reason} • ⏱️ {item.timeline}</p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
