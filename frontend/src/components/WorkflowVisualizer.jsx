export default function WorkflowVisualizer({ status, hasJobDesc }) {
  const steps = [
    { id: 'parse', icon: '📄', label: 'Resume Parser', desc: 'Extracting skills, experience, education' },
    { id: 'skills', icon: '🧠', label: 'Skill Intelligence', desc: 'Normalizing & categorizing skills' },
    ...(hasJobDesc ? [{ id: 'job_match', icon: '🎯', label: 'Job Matcher', desc: 'Scoring resume vs job description' }] : []),
    { id: 'improve', icon: '✍️', label: 'Resume Improver', desc: 'Generating improvement suggestions' },
    { id: 'ats', icon: '📊', label: 'ATS Score Engine', desc: 'Evaluating ATS compatibility' },
    { id: 'recommend', icon: '🔎', label: 'Job Recommender', desc: 'Finding matching roles & career paths' },
  ];

  const getStepState = (id) => {
    if (status[id] === 'complete') return 'complete';
    if (status[id] === 'running') return 'active';
    return 'pending';
  };

  return (
    <div className="card" style={{ position: 'sticky', top: 32 }}>
      <div className="card-header">
        <div className="card-icon" style={{ background: 'rgba(139,92,246,0.15)', color: 'var(--accent-secondary)' }}>⚙️</div>
        <div>
          <h3>Agent Workflow</h3>
          <p>AI pipeline visualization</p>
        </div>
      </div>

      <div className="workflow">
        {steps.map((step, i) => (
          <div key={step.id}>
            <div className={`workflow-step ${getStepState(step.id)}`}>
              <div
                className="step-icon"
                style={{
                  background: getStepState(step.id) === 'complete' ? 'rgba(16,185,129,0.15)' :
                    getStepState(step.id) === 'active' ? 'rgba(99,102,241,0.15)' : 'var(--bg-secondary)',
                }}
              >
                {getStepState(step.id) === 'complete' ? '✅' :
                  getStepState(step.id) === 'active' ? <span className="spinner" style={{ width: 18, height: 18 }} /> :
                    step.icon}
              </div>
              <div className="step-info">
                <h4>{step.label}</h4>
                <p>{step.desc}</p>
              </div>
              {getStepState(step.id) === 'complete' && (
                <span style={{ marginLeft: 'auto', fontSize: 11, color: 'var(--success)', fontWeight: 600 }}>DONE</span>
              )}
              {getStepState(step.id) === 'active' && (
                <span className="pulse" style={{ marginLeft: 'auto', fontSize: 11, color: 'var(--accent-primary)', fontWeight: 600 }}>RUNNING</span>
              )}
              {getStepState(step.id) === 'pending' && (
                <span style={{ marginLeft: 'auto', fontSize: 11, color: 'var(--text-muted)', fontWeight: 500 }}>PENDING</span>
              )}
            </div>
            {i < steps.length - 1 && (
              <div className={`workflow-connector ${getStepState(steps[i + 1]?.id) !== 'pending' ? 'active' : ''} ${getStepState(step.id)}`} />
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
