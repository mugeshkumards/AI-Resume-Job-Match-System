"""Agent 1: Resume Parser — extracts structured data from raw resume text."""

from backend.agents.base_agent import BaseAgent

SYSTEM_PROMPT = """You are an expert resume parser. Your job is to extract structured information from raw resume text.

You MUST return valid JSON with this exact structure:
{
    "name": "Full Name",
    "email": "email@example.com",
    "phone": "+1-xxx-xxx-xxxx",
    "summary": "Professional summary or objective",
    "skills": ["skill1", "skill2", ...],
    "experience": [
        {
            "title": "Job Title",
            "company": "Company Name",
            "duration": "Start - End",
            "location": "City, State",
            "highlights": ["Achievement 1", "Achievement 2"]
        }
    ],
    "education": [
        {
            "degree": "Degree Name",
            "institution": "University Name",
            "year": "Year or Duration",
            "gpa": "GPA if available"
        }
    ],
    "projects": [
        {
            "name": "Project Name",
            "description": "Brief description",
            "technologies": ["tech1", "tech2"]
        }
    ],
    "certifications": ["Cert 1", "Cert 2"]
}

Rules:
- Extract ALL skills mentioned anywhere in the resume
- Include both technical and soft skills
- If a field is not found, use empty string or empty list
- Preserve original skill names exactly as written
- Extract project technologies from descriptions if not explicitly listed"""


class ResumeParserAgent(BaseAgent):
    def __init__(self):
        super().__init__("Resume Parser", SYSTEM_PROMPT)

    async def parse(self, resume_text: str) -> dict:
        """Parse raw resume text into structured JSON."""
        prompt = f"""Parse the following resume and extract all structured information.

RESUME TEXT:
---
{resume_text}
---

Return the structured JSON as specified."""

        result = await self.call_llm_json(prompt)
        return self._validate_result(result)

    @staticmethod
    def _validate_result(data: dict) -> dict:
        """Ensure all expected fields exist."""
        defaults = {
            "name": "", "email": "", "phone": "", "summary": "",
            "skills": [], "experience": [], "education": [],
            "projects": [], "certifications": []
        }
        for key, default in defaults.items():
            if key not in data:
                data[key] = default
        return data
