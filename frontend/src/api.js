// In production, the frontend is served by the backend, so use relative URLs.
// In development, point to the local backend dev server.
const API_BASE = import.meta.env.PROD
  ? '/api'
  : 'http://localhost:8001/api';

export async function fullAnalysis(data) {
  const res = await fetch(`${API_BASE}/resume/full-analysis`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error((await res.json()).detail || 'Analysis failed');
  return res.json();
}

export async function parseResume(resumeText) {
  const res = await fetch(`${API_BASE}/resume/parse`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ resume_text: resumeText }),
  });
  if (!res.ok) throw new Error('Parse failed');
  return res.json();
}

export async function matchJob(resumeText, jobDescription, jobTitle = '') {
  const res = await fetch(`${API_BASE}/jobs/match`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ resume_text: resumeText, job_description: jobDescription, job_title: jobTitle }),
  });
  if (!res.ok) throw new Error('Match failed');
  return res.json();
}

export async function uploadPdf(file) {
  const form = new FormData();
  form.append('file', file);
  const res = await fetch(`${API_BASE}/resume/upload-pdf`, { method: 'POST', body: form });
  if (!res.ok) throw new Error('PDF upload failed');
  return res.json();
}
