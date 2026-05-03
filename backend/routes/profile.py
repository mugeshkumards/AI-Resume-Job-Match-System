"""User profile / Memory API routes."""

from fastapi import APIRouter, HTTPException
from backend.database import (
    get_user_profile, get_user_resumes, get_match_history, save_user
)

router = APIRouter(prefix="/api/profile", tags=["Profile"])


@router.get("/{email}")
async def get_profile(email: str):
    """Get user profile and improvement history."""
    try:
        # Get or create user
        user_id = await save_user(email)
        profile = await get_user_profile(user_id)
        resumes = await get_user_resumes(user_id)

        return {
            "status": "success",
            "data": {
                "user_id": user_id,
                "email": email,
                "profile": profile,
                "resumes": resumes,
                "total_analyses": len(resumes)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"Profile fetch failed: {str(e)}")


@router.get("/history/{resume_id}")
async def get_history(resume_id: int):
    """Get job match history for a resume."""
    try:
        history = await get_match_history(resume_id)
        return {"status": "success", "data": history}
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"History fetch failed: {str(e)}")
