"""Base agent with Google Gemini API integration."""

import asyncio
import httpx
import json
import logging
import re
from backend.config import GEMINI_API_KEY, GEMINI_MODEL, GEMINI_BASE_URL

logger = logging.getLogger(__name__)

# Maximum number of retries for rate-limited requests
MAX_RETRIES = 6
# Base delay in seconds — Gemini free tier is ~15 RPM, so we need
# delays that actually wait out the rate-limit window (60s).
# Backoff sequence: 10s, 20s, 40s, 60s, 60s, 60s
BASE_DELAY = 10.0
MAX_DELAY = 60.0


class BaseAgent:
    """Base class for all AI agents — handles Gemini API calls."""

    def __init__(self, name: str, system_prompt: str):
        self.name = name
        self.system_prompt = system_prompt

    async def call_llm(self, user_prompt: str, temperature: float = 0.3,
                       max_tokens: int = 4000) -> str:
        """Call Google Gemini API with retry logic for rate limits."""
        url = (
            f"{GEMINI_BASE_URL}/models/{GEMINI_MODEL}"
            f":generateContent?key={GEMINI_API_KEY}"
        )

        payload = {
            "system_instruction": {
                "parts": [{"text": self.system_prompt}]
            },
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": user_prompt}]
                }
            ],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens
            }
        }

        attempt = 1
        while attempt <= MAX_RETRIES:
            try:
                async with httpx.AsyncClient(timeout=120.0) as client:
                    response = await client.post(
                        url,
                        headers={"Content-Type": "application/json"},
                        json=payload
                    )

                    # Handle rate limiting (429) and service unavailable (503)
                    if response.status_code in (429, 503):
                        delay = min(BASE_DELAY * (2 ** (attempt - 1)), MAX_DELAY)
                        logger.warning(
                            f"[{self.name}] Server returned {response.status_code}. "
                            f"Retrying in {delay}s (attempt {attempt}/{MAX_RETRIES})"
                        )
                        await asyncio.sleep(delay)
                        attempt += 1
                        continue

                    response.raise_for_status()
                    data = response.json()

                content = data["candidates"][0]["content"]["parts"][0]["text"]
                return content

            except httpx.HTTPStatusError as e:
                if e.response.status_code in (429, 503):
                    delay = min(BASE_DELAY * (2 ** (attempt - 1)), MAX_DELAY)
                    logger.warning(
                        f"[{self.name}] Server returned {e.response.status_code}. "
                        f"Retrying in {delay}s (attempt {attempt}/{MAX_RETRIES})"
                    )
                    await asyncio.sleep(delay)
                    attempt += 1
                    continue
                raise
            except Exception:
                raise

        raise Exception(f"[{self.name}] Failed after {MAX_RETRIES} retries")

    async def call_llm_json(self, user_prompt: str, temperature: float = 0.2,
                            max_tokens: int = 4000) -> dict:
        """Call LLM and parse response as JSON."""
        raw = await self.call_llm(user_prompt, temperature, max_tokens)
        return self._extract_json(raw)

    @staticmethod
    def _extract_json(text: str) -> dict:
        """Extract JSON from LLM response, handling markdown code blocks."""
        # Try to find JSON in code blocks first
        patterns = [
            r"```json\s*([\s\S]*?)\s*```",
            r"```\s*([\s\S]*?)\s*```",
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                try:
                    return json.loads(match.group(1))
                except json.JSONDecodeError:
                    continue

        # Try parsing the whole text as JSON
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        # Try finding any JSON object in the text
        brace_match = re.search(r"\{[\s\S]*\}", text)
        if brace_match:
            try:
                return json.loads(brace_match.group(0))
            except json.JSONDecodeError:
                pass

        return {"raw_response": text, "parse_error": True}
