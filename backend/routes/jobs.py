"""Job-related API routes."""

from fastapi import APIRouter, HTTPException
from backend.models import JobMatchRequest, JobRecommendRequest
from backend.agents.job_matcher import JobMatcherAgent
from backend.agents.job_recommender import JobRecommenderAgent
from backend.agents.resume_parser import ResumeParserAgent

router = APIRouter(prefix="/api/jobs", tags=["Jobs"])

matcher_agent = JobMatcherAgent()
recommender_agent = JobRecommenderAgent()
parser_agent = ResumeParserAgent()


@router.post("/match", response_model=dict)
async def match_job(request: JobMatchRequest):
    """Match resume against a specific job description."""
    try:
        result = await matcher_agent.match(
            request.resume_text,
            request.job_description,
            request.job_title or ""
        )
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"Job matching failed: {str(e)}")


@router.post("/recommend", response_model=dict)
async def recommend_jobs(request: JobRecommendRequest):
    """Get job recommendations based on resume."""
    try:
        # First parse the resume to extract skills
        parsed = await parser_agent.parse(request.resume_text)

        result = await recommender_agent.recommend(
            parsed.get("skills", []),
            parsed.get("experience", []),
            parsed.get("education", []),
            request.career_goals or ""
        )
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"Job recommendation failed: {str(e)}")
