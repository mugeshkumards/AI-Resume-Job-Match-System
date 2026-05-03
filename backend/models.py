"""Pydantic models for request/response validation."""

from pydantic import BaseModel, Field
from typing import Optional


# ── Request Models ──────────────────────────────────────────────

class ResumeUploadRequest(BaseModel):
    resume_text: str = Field(..., min_length=50,
                             description="Raw resume text content")
    email: Optional[str] = Field(None, description="User email for memory")


class JobMatchRequest(BaseModel):
    resume_text: str = Field(..., min_length=50)
    job_description: str = Field(..., min_length=50)
    job_title: Optional[str] = Field("", description="Job title for context")


class ResumeImproveRequest(BaseModel):
    resume_text: str = Field(..., min_length=50)
    job_description: Optional[str] = Field(None,
                                           description="Target job description for tailoring")


class JobRecommendRequest(BaseModel):
    resume_text: str = Field(..., min_length=50)
    career_goals: Optional[str] = Field("",
                                        description="Career aspirations")


class FullAnalysisRequest(BaseModel):
    resume_text: str = Field(..., min_length=50)
    job_description: Optional[str] = Field(None)
    job_title: Optional[str] = Field("")
    email: Optional[str] = Field(None)
    career_goals: Optional[str] = Field("")


# ── Response Models ─────────────────────────────────────────────

class ParsedResume(BaseModel):
    name: str = ""
    email: str = ""
    phone: str = ""
    summary: str = ""
    skills: list[str] = []
    experience: list[dict] = []
    education: list[dict] = []
    projects: list[dict] = []
    certifications: list[str] = []


class SkillIntelligence(BaseModel):
    normalized_skills: list[dict] = []  # {skill, category, level}
    skill_categories: dict = {}  # category -> [skills]
    missing_skills: list[str] = []
    outdated_skills: list[str] = []
    trending_skills: list[str] = []


class JobMatchResult(BaseModel):
    overall_score: float = 0
    keyword_match: float = 0
    skill_match: float = 0
    experience_match: float = 0
    education_match: float = 0
    matched_skills: list[str] = []
    missing_skills: list[str] = []
    match_summary: str = ""


class ResumeImprovement(BaseModel):
    bullet_improvements: list[dict] = []  # {original, improved, reason}
    keyword_suggestions: list[str] = []
    ats_rewrites: list[dict] = []  # {section, rewrite}
    general_tips: list[str] = []


class ATSScore(BaseModel):
    overall_score: float = 0
    keyword_score: float = 0
    format_score: float = 0
    readability_score: float = 0
    content_score: float = 0
    style_score: float = 0
    sections_score: float = 0
    issues: list[dict] = []  # {category, issue, severity, fix}
    strengths: list[str] = []


class JobRecommendation(BaseModel):
    recommended_jobs: list[dict] = []  # {title, match_reason, fit_score}
    career_paths: list[dict] = []  # {path, description, timeline}
    skill_roadmap: list[dict] = []  # {skill, priority, resource}


class FullAnalysisResponse(BaseModel):
    parsed_resume: ParsedResume = ParsedResume()
    skill_intelligence: SkillIntelligence = SkillIntelligence()
    job_match: Optional[JobMatchResult] = None
    improvements: ResumeImprovement = ResumeImprovement()
    ats_score: ATSScore = ATSScore()
    recommendations: JobRecommendation = JobRecommendation()
    workflow_status: dict = {}
