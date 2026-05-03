"""FastAPI application entry point."""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from backend.database import init_db
from backend.config import PORT, FRONTEND_URL, ENVIRONMENT
from backend.routes import resume, jobs, profile


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup."""
    await init_db()
    print("[OK] Database initialized")
    print("[START] AI Resume Job Match System is running!")
    yield
    print("[STOP] Shutting down...")


app = FastAPI(
    title="AI Resume Job Match System",
    description="Agentic AI system for resume parsing, job matching, and career guidance",
    version="1.0.0",
    lifespan=lifespan
)

# CORS for frontend
allowed_origins = ["http://localhost:5173", "http://localhost:3000"]
if FRONTEND_URL and FRONTEND_URL not in allowed_origins:
    allowed_origins.append(FRONTEND_URL)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(resume.router)
app.include_router(jobs.router)
app.include_router(profile.router)


@app.get("/")
async def root():
    return {
        "name": "AI Resume Job Match System",
        "version": "1.0.0",
        "agents": [
            "Resume Parser", "Skill Intelligence", "Job Matcher",
            "Resume Improver", "ATS Scorer", "Job Recommender", "Memory"
        ],
        "status": "running"
    }


@app.get("/health")
async def health():
    return {"status": "healthy", "environment": ENVIRONMENT}


# ── Serve frontend in production ────────────────────────────
frontend_dist = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "frontend", "dist"
)
if os.path.isdir(frontend_dist):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        """Serve the SPA for any unmatched route."""
        file_path = os.path.join(frontend_dist, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(frontend_dist, "index.html"))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=PORT,
        reload=ENVIRONMENT == "development"
    )
