"""Agent 4: Resume Improver — suggests improvements for resume content."""

from backend.agents.base_agent import BaseAgent

SYSTEM_PROMPT = """You are a Resume Improvement Agent. You analyze resumes and provide actionable improvement suggestions.

Focus areas:
1. BULLET POINT IMPROVEMENTS: Rewrite weak bullets with action verbs and quantified impact
2. KEYWORD OPTIMIZATION: Suggest missing industry keywords
3. ATS-FRIENDLY REWRITES: Rewrite sections to pass ATS systems
4. GENERAL TIPS: Overall resume improvement advice

Return valid JSON:
{
    "bullet_improvements": [
        {
            "original": "Worked on machine learning projects",
            "improved": "Developed and deployed 3 ML models using TensorFlow, improving prediction accuracy by 25% across 500K+ data points",
            "reason": "Added quantified impact, specific technology, and action verb"
        }
    ],
    "keyword_suggestions": ["Keywords to add based on industry standards"],
    "ats_rewrites": [
        {
            "section": "Experience - Software Engineer",
            "issue": "Missing quantifiable metrics",
            "rewrite": "Improved section text..."
        }
    ],
    "general_tips": [
        "Use consistent date formatting",
        "Add a professional summary section"
    ],
    "summary_improvement": "Suggested professional summary if missing or weak",
    "formatting_tips": ["Remove tables and graphics for ATS", "Use standard section headers"]
}"""


class ResumeImproverAgent(BaseAgent):
    def __init__(self):
        super().__init__("Resume Improver", SYSTEM_PROMPT)

    async def improve(self, resume_text: str,
                      job_description: str = None) -> dict:
        """Generate improvement suggestions for a resume."""
        prompt_parts = [f"""Analyze this resume and provide detailed improvement suggestions.

RESUME:
---
{resume_text}
---"""]

        if job_description:
            prompt_parts.append(f"""
TARGET JOB DESCRIPTION (tailor improvements to this):
---
{job_description}
---""")

        prompt_parts.append("""
Provide bullet improvements, keyword suggestions, ATS rewrites, and general tips.
Focus on making each bullet impactful with metrics and action verbs.""")

        prompt = "\n".join(prompt_parts)
        result = await self.call_llm_json(prompt, max_tokens=5000)
        return self._validate_result(result)

    @staticmethod
    def _validate_result(data: dict) -> dict:
        defaults = {
            "bullet_improvements": [], "keyword_suggestions": [],
            "ats_rewrites": [], "general_tips": [],
            "summary_improvement": "", "formatting_tips": []
        }
        for key, default in defaults.items():
            if key not in data:
                data[key] = default
        return data
