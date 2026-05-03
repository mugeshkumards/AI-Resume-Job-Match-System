import { useState, useRef } from 'react';
import { fullAnalysis, uploadPdf } from '../api';
import WorkflowVisualizer from './WorkflowVisualizer';

export default function ResumeUpload({ resumeText, setResumeText, onAnalysisComplete, loading, setLoading }) {
  const [mode, setMode] = useState('text');
  const [jobDesc, setJobDesc] = useState('');
  const [jobTitle, setJobTitle] = useState('');
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const [workflowStatus, setWorkflowStatus] = useState({});
  const fileRef = useRef();

  const handlePdf = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    try {
      const result = await uploadPdf(file);
      setResumeText(result.text);
      setMode('text');
    } catch (err) {
      setError('Failed to extract text from PDF. Try pasting text instead.');
    }
  };

  const handleAnalyze = async () => {
    if (resumeText.trim().length < 50) {
      setError('Please enter at least 50 characters of resume text.');
      return;
    }
    setError('');
    setLoading(true);
    setWorkflowStatus({ parse: 'running' });

    try {
      const steps = ['parse', 'skills', 'improve', 'ats', 'recommend'];
      let i = 0;
      const interval = setInterval(() => {
        i++;
        if (i < steps.length) {
          setWorkflowStatus((prev) => {
            const next = { ...prev };
            next[steps[i - 1]] = 'complete';
            next[steps[i]] = 'running';
            return next;
          });
        }
      }, 3000);

      const result = await fullAnalysis({
        resume_text: resumeText,
        job_description: jobDesc || null,
        job_title: jobTitle || '',
        email: email || null,
        career_goals: '',
      });

      clearInterval(interval);
      setWorkflowStatus(
        Object.fromEntries(steps.map((s) => [s, 'complete']))
      );

      setTimeout(() => {
        onAnalysisComplete(result.data);
      }, 800);
    } catch (err) {
      setError(err.message || 'Analysis failed. Check your API key and try again.');
      setWorkflowStatus({});
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fade-in">
      <div className="page-header">
        <h2>🚀 Upload & Analyze Resume</h2>
        <p>Paste your resume text or upload a PDF to run the full AI agent pipeline</p>
      </div>

      <div className="grid-2">
        <div>
          <div className="card">
            <div className="card-header">
              <div className="card-icon" style={{ background: 'rgba(99,102,241,0.15)', color: 'var(--accent-primary)' }}>📄</div>
              <div>
                <h3>Resume Input</h3>
                <p>Paste text or upload PDF</p>
              </div>
            </div>

            <div className="tabs">
              <button className={`tab ${mode === 'text' ? 'active' : ''}`} onClick={() => setMode('text')}>
                ✏️ Paste Text
              </button>
              <button className={`tab ${mode === 'pdf' ? 'active' : ''}`} onClick={() => setMode('pdf')}>
                📎 Upload PDF
              </button>
            </div>

            {mode === 'pdf' && (
              <div className="upload-zone" onClick={() => fileRef.current?.click()}>
                <div className="upload-icon">📁</div>
                <p>Click to upload PDF resume</p>
                <input ref={fileRef} type="file" accept=".pdf" hidden onChange={handlePdf} />
              </div>
            )}

            {mode === 'text' && (
              <div className="form-group">
                <textarea
                  placeholder="Paste your full resume text here..."
                  value={resumeText}
                  onChange={(e) => setResumeText(e.target.value)}
                />
              </div>
            )}

            <div className="form-group">
              <label>📧 Email (optional — enables memory)</label>
              <input type="email" placeholder="your@email.com" value={email} onChange={(e) => setEmail(e.target.value)} />
            </div>
          </div>

          <div className="card" style={{ marginTop: 24 }}>
            <div className="card-header">
              <div className="card-icon" style={{ background: 'rgba(59,130,246,0.15)', color: 'var(--info)' }}>💼</div>
              <div>
                <h3>Target Job (Optional)</h3>
                <p>Add a job description for tailored matching</p>
              </div>
            </div>
            <div className="form-group">
              <label>Job Title</label>
              <input type="text" placeholder="e.g. Senior ML Engineer" value={jobTitle} onChange={(e) => setJobTitle(e.target.value)} />
            </div>
            <div className="form-group">
              <label>Job Description</label>
              <textarea
                placeholder="Paste the job description here for matching..."
                value={jobDesc}
                onChange={(e) => setJobDesc(e.target.value)}
                style={{ minHeight: 120 }}
              />
            </div>
          </div>

          {error && (
            <div style={{ marginTop: 16, padding: '12px 16px', background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.3)', borderRadius: 'var(--radius-sm)', color: 'var(--danger)', fontSize: 13 }}>
              ⚠️ {error}
            </div>
          )}

          <button className="btn btn-primary btn-lg" style={{ marginTop: 24, width: '100%', justifyContent: 'center' }} onClick={handleAnalyze} disabled={loading}>
            {loading ? <><span className="spinner" /> Analyzing with AI Agents...</> : '🧠 Run Full Analysis'}
          </button>
        </div>

        <div>
          <WorkflowVisualizer status={workflowStatus} hasJobDesc={!!jobDesc.trim()} />
        </div>
      </div>
    </div>
  );
}
