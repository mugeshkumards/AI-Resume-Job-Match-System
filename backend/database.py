"""SQLite database for user profiles, resumes, and job history (Memory Agent)."""

import aiosqlite
import json
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "resume_match.db")


async def get_db():
    """Get database connection."""
    db = await aiosqlite.connect(DB_PATH)
    db.row_factory = aiosqlite.Row
    return db


async def init_db():
    """Initialize database tables."""
    db = await get_db()
    try:
        await db.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE,
                name TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS resumes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                raw_text TEXT,
                parsed_data TEXT,
                skills TEXT,
                ats_score REAL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS job_matches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                resume_id INTEGER,
                job_title TEXT,
                job_description TEXT,
                match_score REAL,
                matched_skills TEXT,
                missing_skills TEXT,
                improvements TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (resume_id) REFERENCES resumes(id)
            );

            CREATE TABLE IF NOT EXISTS user_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                skills_snapshot TEXT,
                career_goals TEXT,
                improvement_history TEXT,
                last_updated TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
        """)
        await db.commit()
    finally:
        await db.close()


async def save_user(email: str, name: str = "") -> int:
    """Create or get user by email."""
    db = await get_db()
    try:
        cursor = await db.execute(
            "SELECT id FROM users WHERE email = ?", (email,)
        )
        row = await cursor.fetchone()
        if row:
            return row[0]
        cursor = await db.execute(
            "INSERT INTO users (email, name) VALUES (?, ?)", (email, name)
        )
        await db.commit()
        return cursor.lastrowid
    finally:
        await db.close()


async def save_resume(user_id: int, raw_text: str, parsed_data: dict,
                      skills: list, ats_score: float) -> int:
    """Save a parsed resume."""
    db = await get_db()
    try:
        cursor = await db.execute(
            """INSERT INTO resumes (user_id, raw_text, parsed_data, skills, ats_score)
               VALUES (?, ?, ?, ?, ?)""",
            (user_id, raw_text, json.dumps(parsed_data),
             json.dumps(skills), ats_score)
        )
        await db.commit()
        return cursor.lastrowid
    finally:
        await db.close()


async def save_job_match(resume_id: int, job_title: str, job_description: str,
                         match_score: float, matched_skills: list,
                         missing_skills: list, improvements: list) -> int:
    """Save a job match result."""
    db = await get_db()
    try:
        cursor = await db.execute(
            """INSERT INTO job_matches
               (resume_id, job_title, job_description, match_score,
                matched_skills, missing_skills, improvements)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (resume_id, job_title, job_description, match_score,
             json.dumps(matched_skills), json.dumps(missing_skills),
             json.dumps(improvements))
        )
        await db.commit()
        return cursor.lastrowid
    finally:
        await db.close()


async def update_user_profile(user_id: int, skills: list,
                              career_goals: str = "",
                              improvement_entry: dict = None):
    """Update or create user profile (Memory Agent)."""
    db = await get_db()
    try:
        cursor = await db.execute(
            "SELECT id, improvement_history FROM user_profiles WHERE user_id = ?",
            (user_id,)
        )
        row = await cursor.fetchone()

        history = []
        if row and row[1]:
            history = json.loads(row[1])
        if improvement_entry:
            improvement_entry["timestamp"] = datetime.now().isoformat()
            history.append(improvement_entry)

        if row:
            await db.execute(
                """UPDATE user_profiles
                   SET skills_snapshot = ?, career_goals = ?,
                       improvement_history = ?, last_updated = ?
                   WHERE user_id = ?""",
                (json.dumps(skills), career_goals,
                 json.dumps(history), datetime.now().isoformat(), user_id)
            )
        else:
            await db.execute(
                """INSERT INTO user_profiles
                   (user_id, skills_snapshot, career_goals, improvement_history)
                   VALUES (?, ?, ?, ?)""",
                (user_id, json.dumps(skills), career_goals, json.dumps(history))
            )
        await db.commit()
    finally:
        await db.close()


async def get_user_profile(user_id: int) -> dict | None:
    """Get user profile with improvement history."""
    db = await get_db()
    try:
        cursor = await db.execute(
            "SELECT * FROM user_profiles WHERE user_id = ?", (user_id,)
        )
        row = await cursor.fetchone()
        if not row:
            return None
        return {
            "user_id": row[1],
            "skills_snapshot": json.loads(row[2]) if row[2] else [],
            "career_goals": row[3] or "",
            "improvement_history": json.loads(row[4]) if row[4] else [],
            "last_updated": row[5]
        }
    finally:
        await db.close()


async def get_user_resumes(user_id: int) -> list:
    """Get all resumes for a user."""
    db = await get_db()
    try:
        cursor = await db.execute(
            "SELECT * FROM resumes WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,)
        )
        rows = await cursor.fetchall()
        return [
            {
                "id": r[0],
                "parsed_data": json.loads(r[3]) if r[3] else {},
                "skills": json.loads(r[4]) if r[4] else [],
                "ats_score": r[5],
                "created_at": r[6]
            }
            for r in rows
        ]
    finally:
        await db.close()


async def get_match_history(resume_id: int) -> list:
    """Get job match history for a resume."""
    db = await get_db()
    try:
        cursor = await db.execute(
            "SELECT * FROM job_matches WHERE resume_id = ? ORDER BY created_at DESC",
            (resume_id,)
        )
        rows = await cursor.fetchall()
        return [
            {
                "id": r[0],
                "job_title": r[2],
                "match_score": r[4],
                "matched_skills": json.loads(r[5]) if r[5] else [],
                "missing_skills": json.loads(r[6]) if r[6] else [],
                "improvements": json.loads(r[7]) if r[7] else [],
                "created_at": r[8]
            }
            for r in rows
        ]
    finally:
        await db.close()
