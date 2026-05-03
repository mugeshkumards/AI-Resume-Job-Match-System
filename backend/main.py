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

# ── Detect frontend build ───────────────────────────────────
FRONTEND_DIST = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "frontend", "dist"
)
HAS_FRONTEND = os.path.isdir(FRONTEND_DIST)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup."""
    await init_db()
    print("[OK] Database initialized")
    print(f"[OK] Frontend build: {'FOUND' if HAS_FRONTEND else 'NOT FOUND'}")
    print(f"[OK] Frontend path: {FRONTEND_DIST}")
    print(f"[START] AI Resume Job Match System is running! (env={ENVIRONMENT})")
    yield
    print("[STOP] Shutting down...")


app = FastAPI(
    title="AI Resume Job Match System",
    description="Agentic AI system for resume parsing, job matching, and career guidance",
    version="1.0.0",
    lifespan=lifespan
)

# CORS for frontend
allowed_origins = ["http://localhost:5173", "http://localhost:3000", "*"]
if FRONTEND_URL and FRONTEND_URL not in allowed_origins:
    allowed_origins.append(FRONTEND_URL)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(resume.router)
app.include_router(jobs.router)
app.include_router(profile.router)


@app.get("/api/info")
async def api_info():
    """API information endpoint."""
    return {
        "name": "AI Resume Job Match System",
        "version": "1.0.0",
        "agents": [
            "Resume Parser", "Skill Intelligence", "Job Matcher",
            "Resume Improver", "ATS Scorer", "Job Recommender", "Memory"
        ],
        "status": "running",
        "frontend": HAS_FRONTEND
    }


@app.get("/health")
async def health():
    return {"status": "healthy", "environment": ENVIRONMENT}


# ── Serve frontend in production ────────────────────────────
if HAS_FRONTEND:
    # Mount static assets directory
    assets_dir = os.path.join(FRONTEND_DIST, "assets")
    if os.path.isdir(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/")
    async def serve_root():
        """Serve the frontend index.html at root."""
        return FileResponse(os.path.join(FRONTEND_DIST, "index.html"))

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        """Serve static files or fall back to index.html for SPA routing."""
        # Don't interfere with /api or /health routes
        if full_path.startswith("api/") or full_path == "health":
            return {"detail": "Not found"}

        # Try to serve the exact file from dist
        file_path = os.path.join(FRONTEND_DIST, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)

        # Fall back to index.html for SPA client-side routing
        return FileResponse(os.path.join(FRONTEND_DIST, "index.html"))
else:
    # No frontend build — show API info at root
    @app.get("/")
    async def root():
        """Show API info when no frontend build is present."""
        return {
            "name": "AI Resume Job Match System",
            "version": "1.0.0",
            "agents": [
                "Resume Parser", "Skill Intelligence", "Job Matcher",
                "Resume Improver", "ATS Scorer", "Job Recommender", "Memory"
            ],
            "status": "running",
            "docs": "/docs"
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=PORT,
        reload=ENVIRONMENT == "development"
    )
