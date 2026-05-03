import { useState } from 'react';
import ScoreGauge from './ScoreGauge';
import SkillsPanel from './SkillsPanel';
import JobMatchPanel from './JobMatchPanel';
import ATSPanel from './ATSPanel';
import ImprovementsPanel from './ImprovementsPanel';
import RecommendationsPanel from './RecommendationsPanel';

export default function Dashboard({ data }) {
  const [activeSection, setActiveSection] = useState('overview');
  const { parsed_resume, skill_intelligence, job_match, improvements, ats_score, recommendations } = data;

  const sections = [
    { id: 'overview', icon: '📊', label: 'Overview' },
    { id: 'skills', icon: '🧠', label: 'Skills' },
    { id: 'ats', icon: '📋', label: 'ATS Score' },
    { id: 'improve', icon: '✍️', label: 'Improvements' },
    ...(job_match ? [{ id: 'match', icon: '🎯', label: 'Job Match' }] : []),
    { id: 'recommend', icon: '🔎', label: 'Career' },
  ];

  const atsOverall = ats_score?.overall_score || 0;
  const matchOverall = job_match?.overall_score || 0;

  return (
    <div className="fade-in">
      <div className="page-header">
        <h2>📊 Analysis Dashboard</h2>
        <p>Complete AI-powered resume analysis for <strong>{parsed_resume?.name || 'your resume'}</strong></p>
      </div>

      <div className="tabs" style={{ maxWidth: 700 }}>
        {sections.map((s) => (
          <button key={s.id} className={`tab ${activeSection === s.id ? 'active' : ''}`} onClick={() => setActiveSection(s.id)}>
            {s.icon} {s.label}
          </button>
        ))}
      </div>

      {activeSection === 'overview' && (
        <div className="slide-up">
          <div className="grid-3" style={{ marginBottom: 32 }}>
            <div className="card" style={{ textAlign: 'center' }}>
              <ScoreGauge score={atsOverall} label="ATS Score" color={atsOverall >= 70 ? 'var(--success)' : atsOverall >= 40 ? 'var(--warning)' : 'var(--danger)'} />
            </div>
            {job_match && (
              <div className="card" style={{ textAlign: 'center' }}>
                <ScoreGauge score={matchOverall} label="Job Match" color={matchOverall >= 70 ? 'var(--success)' : matchOverall >= 40 ? 'var(--warning)' : 'var(--danger)'} />
              </div>
            )}
            <div className="card" style={{ textAlign: 'center' }}>
              <ScoreGauge score={parsed_resume?.skills?.length || 0} label="Skills Found" max={50} color="var(--accent-primary)" isCount />
            </div>
          </div>

          <div className="grid-2">
            <div className="card">
              <div className="card-header">
                <div className="card-icon" style={{ background: 'rgba(16,185,129,0.15)', color: 'var(--success)' }}>👤</div>
                <div><h3>Profile Summary</h3></div>
              </div>
              <div style={{ fontSize: 14, lineHeight: 1.7, color: 'var(--text-secondary)' }}>
                {parsed_resume?.summary || 'No summary extracted.'}
              </div>
              <div style={{ marginTop: 16 }}>
                <div style={{ fontSize: 12, color: 'var(--text-muted)', marginBottom: 6 }}>📧 {parsed_resume?.email || 'N/A'}</div>
                <div style={{ fontSize: 12, color: 'var(--text-muted)' }}>📱 {parsed_resume?.phone || 'N/A'}</div>
              </div>
            </div>

            <div className="card">
              <div className="card-header">
                <div className="card-icon" style={{ background: 'rgba(99,102,241,0.15)', color: 'var(--accent-primary)' }}>🎯</div>
                <div><h3>Top Skills</h3></div>
              </div>
              <div className="tags-container">
                {(parsed_resume?.skills || []).slice(0, 15).map((s, i) => (
                  <span key={i} className="tag tag-purple">{s}</span>
                ))}
                {(parsed_resume?.skills?.length || 0) > 15 && (
                  <span className="tag tag-info">+{parsed_resume.skills.length - 15} more</span>
                )}
              </div>
            </div>
          </div>

          <div className="grid-2" style={{ marginTop: 24 }}>
            <div className="card">
              <div className="card-header">
                <div className="card-icon" style={{ background: 'rgba(245,158,11,0.15)', color: 'var(--warning)' }}>💼</div>
                <div><h3>Experience</h3></div>
              </div>
              {(parsed_resume?.experience || []).map((exp, i) => (
                <div key={i} style={{ padding: '12px 0', borderBottom: i < parsed_resume.experience.length - 1 ? '1px solid var(--border-color)' : 'none' }}>
                  <div style={{ fontWeight: 600, fontSize: 14 }}>{exp.title}</div>
                  <div style={{ fontSize: 13, color: 'var(--accent-primary)' }}>{exp.company}</div>
                  <div style={{ fontSize: 12, color: 'var(--text-muted)' }}>{exp.duration} {exp.location ? `• ${exp.location}` : ''}</div>
                </div>
              ))}
              {(!parsed_resume?.experience?.length) && <p style={{ color: 'var(--text-muted)', fontSize: 13 }}>No experience data extracted.</p>}
            </div>

            <div className="card">
              <div className="card-header">
                <div className="card-icon" style={{ background: 'rgba(59,130,246,0.15)', color: 'var(--info)' }}>🎓</div>
                <div><h3>Education</h3></div>
              </div>
              {(parsed_resume?.education || []).map((edu, i) => (
                <div key={i} style={{ padding: '12px 0', borderBottom: i < parsed_resume.education.length - 1 ? '1px solid var(--border-color)' : 'none' }}>
                  <div style={{ fontWeight: 600, fontSize: 14 }}>{edu.degree}</div>
                  <div style={{ fontSize: 13, color: 'var(--accent-primary)' }}>{edu.institution}</div>
                  <div style={{ fontSize: 12, color: 'var(--text-muted)' }}>{edu.year} {edu.gpa ? `• GPA: ${edu.gpa}` : ''}</div>
                </div>
              ))}
              {(!parsed_resume?.education?.length) && <p style={{ color: 'var(--text-muted)', fontSize: 13 }}>No education data extracted.</p>}
            </div>
          </div>
        </div>
      )}

      {activeSection === 'skills' && <SkillsPanel data={skill_intelligence} />}
      {activeSection === 'ats' && <ATSPanel data={ats_score} />}
      {activeSection === 'improve' && <ImprovementsPanel data={improvements} />}
      {activeSection === 'match' && job_match && <JobMatchPanel data={job_match} />}
      {activeSection === 'recommend' && <RecommendationsPanel data={recommendations} />}
    </div>
  );
}
