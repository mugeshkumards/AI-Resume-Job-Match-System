"""Agent 6: Job Recommender — suggests jobs, career paths, and skill roadmaps."""

from backend.agents.base_agent import BaseAgent

SYSTEM_PROMPT = """You are a Job Recommendation Agent. Based on a candidate's skills, experience, and goals, you suggest:

1. TOP MATCHING JOBS: Real job titles they'd be a great fit for
2. CAREER PATHS: Progression paths they could pursue
3. SKILL ROADMAP: Skills to learn, in priority order, with timelines

Return valid JSON:
{
    "recommended_jobs": [
        {
            "title": "Senior ML Engineer",
            "company_type": "Tech / Startup",
            "match_reason": "Strong Python + ML skills align perfectly",
            "fit_score": 90,
            "salary_range": "$130K - $180K",
            "growth_potential": "High"
        }
    ],
    "career_paths": [
        {
            "path": "ML Engineer → Senior ML Engineer → ML Architect → VP of AI",
            "description": "Technical leadership track in ML/AI",
            "timeline": "5-8 years",
            "required_skills": ["System Design", "Leadership", "Cloud Architecture"]
        }
    ],
    "skill_roadmap": [
        {
            "skill": "Kubernetes",
            "priority": "high",
            "timeline": "1-2 months",
            "reason": "Essential for deploying ML models at scale",
            "resources": ["Kubernetes Documentation", "KodeKloud courses"]
        }
    ],
    "industry_insights": "Brief analysis of the job market for their profile"
}

Provide at least 5 job recommendations, 2-3 career paths, and 5-8 skills in the roadmap."""


class JobRecommenderAgent(BaseAgent):
    def __init__(self):
        super().__init__("Job Recommender", SYSTEM_PROMPT)

    async def recommend(self, skills: list, experience: list = None,
                        education: list = None,
                        career_goals: str = "") -> dict:
        """Generate job recommendations and career guidance."""
        prompt_parts = [f"CANDIDATE SKILLS: {', '.join(skills)}"]

        if experience:
            exp_text = "\n".join([
                f"- {e.get('title', '')} at {e.get('company', '')} ({e.get('duration', '')})"
                for e in experience
            ])
            prompt_parts.append(f"\nEXPERIENCE:\n{exp_text}")

        if education:
            edu_text = "\n".join([
                f"- {e.get('degree', '')} from {e.get('institution', '')}"
                for e in education
            ])
            prompt_parts.append(f"\nEDUCATION:\n{edu_text}")

        if career_goals:
            prompt_parts.append(f"\nCAREER GOALS: {career_goals}")

        prompt = f"""Based on this candidate profile, provide job recommendations, career paths, and a skill roadmap.

{chr(10).join(prompt_parts)}

Suggest realistic, market-relevant jobs and a practical skill development plan."""

        result = await self.call_llm_json(prompt, max_tokens=5000)
        return self._validate_result(result)

    @staticmethod
    def _validate_result(data: dict) -> dict:
        defaults = {
            "recommended_jobs": [], "career_paths": [],
            "skill_roadmap": [], "industry_insights": ""
        }
        for key, default in defaults.items():
            if key not in data:
                data[key] = default
        return data
