"""Application configuration — reads from .env"""

import os
from dotenv import load_dotenv

load_dotenv()

# ── LLM Config ──────────────────────────────────────────────
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
GEMINI_BASE_URL = os.getenv(
    "GEMINI_BASE_URL",
    "https://generativelanguage.googleapis.com/v1beta"
)

# ── Server Config ───────────────────────────────────────────
PORT = int(os.getenv("PORT", "8001"))
DATABASE_PATH = os.getenv("DATABASE_PATH", "resume_match.db")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
