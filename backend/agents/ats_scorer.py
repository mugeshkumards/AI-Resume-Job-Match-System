"""Agent 5: ATS Score Engine — scores resume for ATS compatibility."""

from backend.agents.base_agent import BaseAgent

SYSTEM_PROMPT = """You are an ATS (Applicant Tracking System) Scoring Engine. You evaluate resumes for ATS compatibility.

Score these categories (0-100 each):
1. KEYWORD SCORE: Industry-standard keywords and terminology
2. FORMAT SCORE: ATS-parseable formatting (no tables, images, columns)
3. READABILITY SCORE: Clear, concise language
4. CONTENT SCORE: Quantified achievements, action verbs, relevant content
5. STYLE SCORE: Professional tone, consistent formatting
6. SECTIONS SCORE: Proper section headers (Summary, Experience, Education, Skills)
7. OVERALL SCORE: Weighted average

Return valid JSON:
{
    "overall_score": 75,
    "keyword_score": 80,
    "format_score": 70,
    "readability_score": 85,
    "content_score": 65,
    "style_score": 70,
    "sections_score": 80,
    "issues": [
        {
            "category": "CONTENT",
            "issue": "Missing quantifiable metrics in 3 bullet points",
            "severity": "high",
            "fix": "Add specific numbers, percentages, or dollar amounts"
        }
    ],
    "strengths": [
        "Strong use of action verbs",
        "Well-organized sections"
    ],
    "overall_assessment": "Your resume scores moderately well..."
}

Be strict but fair. Most resumes should score between 40-80."""


class ATSScorerAgent(BaseAgent):
    def __init__(self):
        super().__init__("ATS Score Engine", SYSTEM_PROMPT)

    async def score(self, resume_text: str,
                    job_description: str = None) -> dict:
        """Score a resume for ATS compatibility."""
        prompt_parts = [f"""Score this resume for ATS compatibility across all categories.

RESUME:
---
{resume_text}
---"""]

        if job_description:
            prompt_parts.append(f"""
TARGET JOB (score keywords against this):
---
{job_description}
---""")

        prompt_parts.append("""
Be thorough and realistic. Identify specific issues with severity levels and fixes.
Score each category 0-100.""")

        prompt = "\n".join(prompt_parts)
        result = await self.call_llm_json(prompt)
        return self._validate_result(result)

    @staticmethod
    def _validate_result(data: dict) -> dict:
        defaults = {
            "overall_score": 0, "keyword_score": 0, "format_score": 0,
            "readability_score": 0, "content_score": 0,
            "style_score": 0, "sections_score": 0,
            "issues": [], "strengths": [], "overall_assessment": ""
        }
        for key, default in defaults.items():
            if key not in data:
                data[key] = default
        for score_key in ["overall_score", "keyword_score", "format_score",
                          "readability_score", "content_score",
                          "style_score", "sections_score"]:
            try:
                data[score_key] = float(data[score_key])
            except (ValueError, TypeError):
                data[score_key] = 0
        return data
