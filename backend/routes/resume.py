"""Resume-related API routes."""

import asyncio
from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.models import (
    ResumeUploadRequest, ParsedResume, SkillIntelligence,
    ATSScore, ResumeImprovement, FullAnalysisRequest, FullAnalysisResponse,
    JobRecommendation
)
from backend.agents.resume_parser import ResumeParserAgent
from backend.agents.skill_intel import SkillIntelligenceAgent
from backend.agents.ats_scorer import ATSScorerAgent
from backend.agents.resume_improver import ResumeImproverAgent
from backend.agents.job_recommender import JobRecommenderAgent
from backend.database import save_user, save_resume, update_user_profile
import PyPDF2
import io

# Delay between agent calls (seconds) to respect Gemini free-tier rate limits (~15 RPM)
_AGENT_DELAY = 4.0

router = APIRouter(prefix="/api/resume", tags=["Resume"])

# Initialize agents
parser_agent = ResumeParserAgent()
skill_agent = SkillIntelligenceAgent()
ats_agent = ATSScorerAgent()
improver_agent = ResumeImproverAgent()
recommender_agent = JobRecommenderAgent()


@router.post("/parse", response_model=dict)
async def parse_resume(request: ResumeUploadRequest):
    """Parse resume text and extract structured data."""
    try:
        parsed = await parser_agent.parse(request.resume_text)
        return {"status": "success", "data": parsed}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Parsing failed: {str(e)}")


@router.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload PDF resume and extract text."""
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")

    try:
        content = await file.read()
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"

        if len(text.strip()) < 50:
            raise HTTPException(status_code=400,
                                detail="Could not extract enough text from PDF")

        return {"status": "success", "text": text.strip()}
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"PDF processing failed: {str(e)}")


@router.post("/skills", response_model=dict)
async def analyze_skills(request: ResumeUploadRequest):
    """Parse resume and analyze skills."""
    try:
        parsed = await parser_agent.parse(request.resume_text)
        skills_intel = await skill_agent.analyze(
            parsed.get("skills", []),
            parsed.get("experience", []),
            parsed.get("education", [])
        )
        return {"status": "success", "data": skills_intel}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Skill analysis failed: {str(e)}")


@router.post("/ats-score", response_model=dict)
async def get_ats_score(request: ResumeUploadRequest):
    """Score resume for ATS compatibility."""
    try:
        score = await ats_agent.score(request.resume_text)
        return {"status": "success", "data": score}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ATS scoring failed: {str(e)}")


@router.post("/improve", response_model=dict)
async def improve_resume(request: ResumeUploadRequest):
    """Get improvement suggestions for resume."""
    try:
        improvements = await improver_agent.improve(request.resume_text)
        return {"status": "success", "data": improvements}
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"Improvement generation failed: {str(e)}")


@router.post("/full-analysis", response_model=dict)
async def full_analysis(request: FullAnalysisRequest):
    """Run the FULL agent pipeline on a resume.

    Each agent runs independently — if one fails (e.g., rate-limited),
    the pipeline continues and returns partial results instead of crashing.
    """
    workflow_status = {}
    parsed = {}
    skills_intel = {}
    job_match = None
    improvements = {}
    ats_score = {}
    recommendations = {}

    # ── Step 1: Parse Resume (required — without this, nothing else works)
    workflow_status["parse"] = "running"
    try:
        parsed = await parser_agent.parse(request.resume_text)
        workflow_status["parse"] = "complete"
    except Exception as e:
        workflow_status["parse"] = f"failed: {str(e)}"
        # If parse fails, return early — other agents depend on it
        return {
            "status": "partial",
            "data": {
                "parsed_resume": parsed,
                "skill_intelligence": skills_intel,
                "job_match": job_match,
                "improvements": improvements,
                "ats_score": ats_score,
                "recommendations": recommendations,
                "workflow_status": workflow_status
            },
            "error": f"Resume parsing failed: {str(e)}"
        }

    await asyncio.sleep(_AGENT_DELAY)

    # ── Step 2: Skill Intelligence
    workflow_status["skills"] = "running"
    try:
        skills_intel = await skill_agent.analyze(
            parsed.get("skills", []),
            parsed.get("experience", []),
            parsed.get("education", [])
        )
        workflow_status["skills"] = "complete"
    except Exception as e:
        workflow_status["skills"] = f"failed: {str(e)}"
        skills_intel = {
            "normalized_skills": [], "skill_categories": {},
            "missing_skills": [], "outdated_skills": [],
            "trending_skills": [], "skill_summary": "Analysis unavailable due to rate limiting."
        }

    await asyncio.sleep(_AGENT_DELAY)

    # ── Step 3: Job Match (only if job description provided)
    if request.job_description:
        workflow_status["job_match"] = "running"
        try:
            from backend.agents.job_matcher import JobMatcherAgent
            matcher = JobMatcherAgent()
            job_match = await matcher.match(
                request.resume_text,
                request.job_description,
                request.job_title or ""
            )
            workflow_status["job_match"] = "complete"
        except Exception as e:
            workflow_status["job_match"] = f"failed: {str(e)}"
            job_match = {
                "overall_score": 0, "keyword_match": 0, "skill_match": 0,
                "experience_match": 0, "education_match": 0,
                "matched_skills": [], "missing_skills": [],
                "match_summary": "Job matching unavailable due to rate limiting."
            }

        await asyncio.sleep(_AGENT_DELAY)

    # ── Step 4: Resume Improvements
    workflow_status["improve"] = "running"
    try:
        improvements = await improver_agent.improve(
            request.resume_text, request.job_description
        )
        workflow_status["improve"] = "complete"
    except Exception as e:
        workflow_status["improve"] = f"failed: {str(e)}"
        improvements = {
            "bullet_improvements": [], "keyword_suggestions": [],
            "ats_rewrites": [], "general_tips": [],
            "summary_improvement": "Improvement suggestions unavailable due to rate limiting.",
            "formatting_tips": []
        }

    await asyncio.sleep(_AGENT_DELAY)

    # ── Step 5: ATS Score
    workflow_status["ats"] = "running"
    try:
        ats_score = await ats_agent.score(
            request.resume_text, request.job_description
        )
        workflow_status["ats"] = "complete"
    except Exception as e:
        workflow_status["ats"] = f"failed: {str(e)}"
        ats_score = {
            "overall_score": 0, "keyword_score": 0, "format_score": 0,
            "readability_score": 0, "content_score": 0,
            "style_score": 0, "sections_score": 0,
            "issues": [], "strengths": [],
            "overall_assessment": "ATS scoring unavailable due to rate limiting."
        }

    await asyncio.sleep(_AGENT_DELAY)

    # ── Step 6: Job Recommendations
    workflow_status["recommend"] = "running"
    try:
        recommendations = await recommender_agent.recommend(
            parsed.get("skills", []),
            parsed.get("experience", []),
            parsed.get("education", []),
            request.career_goals or ""
        )
        workflow_status["recommend"] = "complete"
    except Exception as e:
        workflow_status["recommend"] = f"failed: {str(e)}"
        recommendations = {
            "recommended_jobs": [], "career_paths": [],
            "skill_roadmap": [], "industry_insights": "Recommendations unavailable due to rate limiting."
        }

    # ── Step 7: Memory — save to DB if email provided
    if request.email:
        try:
            user_id = await save_user(request.email,
                                      parsed.get("name", ""))
            await save_resume(
                user_id, request.resume_text, parsed,
                parsed.get("skills", []),
                ats_score.get("overall_score", 0) if isinstance(ats_score, dict) else 0
            )
            await update_user_profile(
                user_id,
                parsed.get("skills", []),
                request.career_goals or "",
                {"ats_score": ats_score.get("overall_score", 0) if isinstance(ats_score, dict) else 0,
                 "skills_count": len(parsed.get("skills", []))}
            )
            workflow_status["memory"] = "saved"
        except Exception:
            workflow_status["memory"] = "failed"

    # Count how many agents succeeded
    completed = sum(1 for v in workflow_status.values() if v == "complete")
    total = sum(1 for k in workflow_status if k != "memory")
    status = "success" if completed == total else "partial"

    return {
        "status": status,
        "data": {
            "parsed_resume": parsed,
            "skill_intelligence": skills_intel,
            "job_match": job_match,
            "improvements": improvements,
            "ats_score": ats_score,
            "recommendations": recommendations,
            "workflow_status": workflow_status
        }
    }

