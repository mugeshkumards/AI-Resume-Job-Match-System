import { useState } from 'react';
import './index.css';
import Sidebar from './components/Sidebar';
import ResumeUpload from './components/ResumeUpload';
import Dashboard from './components/Dashboard';

export default function App() {
  const [activeTab, setActiveTab] = useState('upload');
  const [analysisData, setAnalysisData] = useState(null);
  const [resumeText, setResumeText] = useState('');
  const [loading, setLoading] = useState(false);

  const handleAnalysisComplete = (data) => {
    setAnalysisData(data);
    setActiveTab('dashboard');
  };

  return (
    <div className="app-layout">
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} hasData={!!analysisData} />
      <main className="main-content">
        {activeTab === 'upload' && (
          <ResumeUpload
            resumeText={resumeText}
            setResumeText={setResumeText}
            onAnalysisComplete={handleAnalysisComplete}
            loading={loading}
            setLoading={setLoading}
          />
        )}
        {activeTab === 'dashboard' && analysisData && (
          <Dashboard data={analysisData} resumeText={resumeText} />
        )}
        {activeTab === 'dashboard' && !analysisData && (
          <div className="empty-state">
            <div className="empty-icon">📄</div>
            <h3>No Analysis Yet</h3>
            <p>Upload your resume to get started with AI-powered analysis, scoring, and recommendations.</p>
            <button className="btn btn-primary" style={{ marginTop: 20 }} onClick={() => setActiveTab('upload')}>
              Upload Resume
            </button>
          </div>
        )}
      </main>
    </div>
  );
}
