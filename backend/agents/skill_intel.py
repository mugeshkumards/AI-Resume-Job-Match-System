"""Agent 2: Skill Intelligence — normalizes, categorizes, and analyzes skills."""

from backend.agents.base_agent import BaseAgent

SYSTEM_PROMPT = """You are a Skill Intelligence Agent. You analyze extracted skills from resumes and provide deep intelligence.

Your tasks:
1. NORMALIZE skills (e.g., "React.js" → also tagged as "Frontend Development")
2. CATEGORIZE skills into groups (Frontend, Backend, Data Science, DevOps, Soft Skills, etc.)
3. DETECT outdated skills (e.g., jQuery, AngularJS 1.x, Perl for web)
4. IDENTIFY missing skills based on detected categories (what skills would complement existing ones)
5. SUGGEST trending skills the candidate should learn

Return valid JSON:
{
    "normalized_skills": [
        {"skill": "Original Skill", "category": "Category", "level": "beginner|intermediate|advanced", "aliases": ["Alias1"]}
    ],
    "skill_categories": {
        "Frontend": ["React", "HTML", "CSS"],
        "Backend": ["Python", "FastAPI"],
        "Data Science": ["TensorFlow", "PyTorch"]
    },
    "missing_skills": ["Skill that would complement their profile"],
    "outdated_skills": ["Old skills they should update"],
    "trending_skills": ["Hot skills in their domain they should learn"],
    "skill_summary": "Brief analysis of their skill profile"
}"""


class SkillIntelligenceAgent(BaseAgent):
    def __init__(self):
        super().__init__("Skill Intelligence", SYSTEM_PROMPT)

    async def analyze(self, skills: list, experience: list = None,
                      education: list = None) -> dict:
        """Analyze and normalize extracted skills."""
        context_parts = [f"EXTRACTED SKILLS: {', '.join(skills)}"]

        if experience:
            exp_text = "\n".join([
                f"- {e.get('title', '')} at {e.get('company', '')} ({e.get('duration', '')})"
                for e in experience
            ])
            context_parts.append(f"\nEXPERIENCE CONTEXT:\n{exp_text}")

        if education:
            edu_text = "\n".join([
                f"- {e.get('degree', '')} from {e.get('institution', '')}"
                for e in education
            ])
            context_parts.append(f"\nEDUCATION CONTEXT:\n{edu_text}")

        prompt = f"""Analyze these skills from a resume and provide full skill intelligence.

{chr(10).join(context_parts)}

Provide normalized skills, categories, missing skills, outdated skills, and trending suggestions."""

        result = await self.call_llm_json(prompt, temperature=0.3)
        return self._validate_result(result)

    @staticmethod
    def _validate_result(data: dict) -> dict:
        defaults = {
            "normalized_skills": [], "skill_categories": {},
            "missing_skills": [], "outdated_skills": [],
            "trending_skills": [], "skill_summary": ""
        }
        for key, default in defaults.items():
            if key not in data:
                data[key] = default
        return data
