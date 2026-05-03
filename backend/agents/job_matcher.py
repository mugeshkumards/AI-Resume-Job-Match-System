"""Agent 3: Job Matcher — scores resume against job descriptions."""

from backend.agents.base_agent import BaseAgent

SYSTEM_PROMPT = """You are a Job Matching Agent. You compare resumes against job descriptions and provide detailed match scoring.

Scoring criteria:
1. KEYWORD MATCH (0-100): How well resume keywords match job requirements
2. SKILL MATCH (0-100): Technical and soft skills alignment
3. EXPERIENCE MATCH (0-100): Years and relevance of experience
4. EDUCATION MATCH (0-100): Education requirements alignment
5. OVERALL SCORE (0-100): Weighted average (Skills 40%, Experience 25%, Keywords 20%, Education 15%)

Return valid JSON:
{
    "overall_score": 85,
    "keyword_match": 80,
    "skill_match": 90,
    "experience_match": 85,
    "education_match": 80,
    "matched_skills": ["Python", "Machine Learning", "SQL"],
    "missing_skills": ["Kubernetes", "Go"],
    "match_summary": "Strong match in core technical skills...",
    "strengths": ["Strong Python background", "ML experience"],
    "gaps": ["No cloud infrastructure experience", "Missing containerization skills"],
    "fit_assessment": "Good fit for the role with minor skill gaps"
}"""


class JobMatcherAgent(BaseAgent):
    def __init__(self):
        super().__init__("Job Matcher", SYSTEM_PROMPT)

    async def match(self, resume_text: str, job_description: str,
                    job_title: str = "") -> dict:
        """Match resume against a job description."""
        prompt = f"""Compare this resume against the job description and provide detailed scoring.

RESUME:
---
{resume_text}
---

JOB TITLE: {job_title or 'Not specified'}

JOB DESCRIPTION:
---
{job_description}
---

Score each category 0-100 and identify matched/missing skills."""

        result = await self.call_llm_json(prompt)
        return self._validate_result(result)

    @staticmethod
    def _validate_result(data: dict) -> dict:
        defaults = {
            "overall_score": 0, "keyword_match": 0, "skill_match": 0,
            "experience_match": 0, "education_match": 0,
            "matched_skills": [], "missing_skills": [],
            "match_summary": "", "strengths": [], "gaps": [],
            "fit_assessment": ""
        }
        for key, default in defaults.items():
            if key not in data:
                data[key] = default
        # Ensure scores are numbers
        for score_key in ["overall_score", "keyword_match", "skill_match",
                          "experience_match", "education_match"]:
            try:
                data[score_key] = float(data[score_key])
            except (ValueError, TypeError):
                data[score_key] = 0
        return data
