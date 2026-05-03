# 🧠 ResumeAI — Intelligent Job Match System

An **AI-powered agentic system** for resume parsing, skill analysis, ATS scoring, job matching, and career guidance. Built with a multi-agent backend (Python + FastAPI + Google Gemini) and a premium React dashboard.

## ✨ Features

| Agent | Function |
|-------|----------|
| **Resume Parser** | Extracts structured data (name, skills, experience, education, projects) from raw text or PDF |
| **Skill Intelligence** | Normalizes, categorizes, detects outdated skills, and suggests trending skills |
| **Job Matcher** | Scores resume against job descriptions (skills, keywords, experience, education) |
| **Resume Improver** | Rewrites bullet points, suggests keywords, and provides ATS-friendly improvements |
| **ATS Score Engine** | Scores resume across 6 categories (keywords, format, readability, content, style, sections) |
| **Job Recommender** | Suggests matching roles, career paths, and skill roadmaps |
| **Memory Agent** | Persists user profiles, resume history, and improvement tracking in SQLite |

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    React Dashboard (Vite)                │
│  Upload → Workflow Viz → Dashboard (6 analysis panels)  │
└─────────────────┬───────────────────────────────────────┘
                  │ REST API
┌─────────────────▼───────────────────────────────────────┐
│              FastAPI Backend (Python)                    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│  │  Resume   │ │  Skill   │ │   Job    │ │  Resume  │  │
│  │  Parser   │ │  Intel   │ │ Matcher  │ │ Improver │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘  │
│  ┌──────────┐ ┌──────────┐ ┌──────────────────────┐   │
│  │   ATS    │ │   Job    │ │   Memory Agent       │   │
│  │  Scorer  │ │ Recomm.  │ │   (SQLite)           │   │
│  └──────────┘ └──────────┘ └──────────────────────┘   │
│                      │                                  │
│              Google Gemini API                          │
└─────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Google Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))

### 1. Clone & Setup

```bash
git clone https://github.com/your-username/ai-resume-job-match.git
cd ai-resume-job-match
```

### 2. Backend Setup

```bash
# Create and configure .env
cp .env.example backend/.env
# Edit backend/.env and add your GEMINI_API_KEY

# Install dependencies
pip install -r backend/requirements.txt

# Start backend
python -m backend.main
```

Backend runs at `http://localhost:8001` — Swagger docs at `/docs`.

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`.

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | System info & agent list |
| `GET` | `/health` | Health check |
| `POST` | `/api/resume/parse` | Parse resume text → structured JSON |
| `POST` | `/api/resume/upload-pdf` | Upload PDF → extract text |
| `POST` | `/api/resume/skills` | Analyze & categorize skills |
| `POST` | `/api/resume/ats-score` | ATS compatibility scoring |
| `POST` | `/api/resume/improve` | Resume improvement suggestions |
| `POST` | `/api/resume/full-analysis` | **Run all 6 agents** in pipeline |
| `POST` | `/api/jobs/match` | Match resume vs job description |
| `POST` | `/api/jobs/recommend` | Job & career recommendations |
| `GET` | `/api/profile/{email}` | User profile & history |
| `GET` | `/api/profile/history/{id}` | Match history for a resume |

## 🌐 Deployment

### Option 1: Render (Recommended)

1. Push code to GitHub
2. Go to [Render Dashboard](https://dashboard.render.com)
3. Click **"New Blueprint"** → connect your repo
4. The `render.yaml` auto-configures everything
5. Set `GEMINI_API_KEY` in environment variables

### Option 2: Docker

```bash
# Build
docker build -t resume-ai .

# Run
docker run -p 8001:8001 \
  -e GEMINI_API_KEY=your_key \
  -e ENVIRONMENT=production \
  resume-ai
```

### Option 3: Manual Deployment

```bash
# Build frontend
cd frontend && npm run build && cd ..

# Start production server
cd backend
ENVIRONMENT=production PORT=8001 \
  gunicorn main:app \
  --workers 2 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8001 \
  --timeout 180
```

## 🔧 Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GEMINI_API_KEY` | — | **Required.** Google Gemini API key |
| `GEMINI_MODEL` | `gemini-2.5-flash` | Gemini model to use |
| `PORT` | `8001` | Server port |
| `ENVIRONMENT` | `development` | `development` or `production` |
| `DATABASE_PATH` | `resume_match.db` | SQLite database path |
| `FRONTEND_URL` | `http://localhost:5173` | Frontend origin for CORS |

## 🛠️ Tech Stack

- **Backend:** Python, FastAPI, Pydantic, aiosqlite
- **Frontend:** React 19, Vite 8, Vanilla CSS
- **AI:** Google Gemini 2.5 Flash (via REST API)
- **Database:** SQLite (async)
- **Deployment:** Render / Docker / Any cloud platform

## 📄 License

MIT
