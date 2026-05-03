export default function Sidebar({ activeTab, setActiveTab, hasData }) {
  const items = [
    { id: 'upload', icon: '📤', label: 'Upload Resume' },
    { id: 'dashboard', icon: '📊', label: 'Analysis Dashboard' },
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <div className="logo-icon">🧠</div>
        <h1>ResumeAI<span>Intelligent Job Match</span></h1>
      </div>

      {items.map((item) => (
        <button
          key={item.id}
          className={`nav-item ${activeTab === item.id ? 'active' : ''}`}
          onClick={() => setActiveTab(item.id)}
        >
          <span className="nav-icon">{item.icon}</span>
          {item.label}
        </button>
      ))}

      <div style={{ marginTop: 'auto', padding: '16px 14px', borderTop: '1px solid var(--border-color)' }}>
        <div style={{ fontSize: 12, color: 'var(--text-muted)', marginBottom: 8 }}>Powered by</div>
        <div style={{ fontSize: 13, fontWeight: 600, color: 'var(--text-secondary)' }}>
          🤖 Google Gemini AI
        </div>
        <div style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 4 }}>
          {hasData ? '✅ Analysis ready' : '⏳ Awaiting resume'}
        </div>
      </div>
    </aside>
  );
}
