from typing import Optional

from google import genai
from google.genai import types

from .config import GEMINI_API_KEY


_client: Optional[genai.Client] = None


def get_client():
    global _client

    if not GEMINI_API_KEY:
        return None

    if _client is None:
        _client = genai.Client(
            api_key=GEMINI_API_KEY
        )

    return _client


def generate_text(
    prompt: str,
    model: str,
    system_instruction: str,
    temperature: float = 0.5,
    max_output_tokens: int = 2800,
):
    client = get_client()

    if client is None:
        raise RuntimeError(
            "Gemini API key is not configured."
        )

    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                max_output_tokens=max_output_tokens,
            ),
        )

        if not response.text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return response.text.strip()

    except Exception as exc:
        print("GEMINI ERROR:", repr(exc))
        raise