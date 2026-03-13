"""ADK Tool for extracting structured data from screenshots using Gemini Vision."""

import base64
import json
from typing import Literal

from google import genai
from google.genai import types

from backend.models.finance import ExpenseRecord
from backend.models.fitness import WorkoutSplit
from backend.models.recipes import RecipeCard


SCHEMA_MAP: dict[str, type] = {
    "recipe": RecipeCard,
    "expense": ExpenseRecord,
    "workout": WorkoutSplit,
}


async def extract_from_screenshot(
    image_base64: str,
    schema_type: Literal["recipe", "expense", "workout", "generic"],
) -> dict:
    """Extract structured data from a screenshot using Gemini Vision."""
    client = genai.Client()
    image_bytes = base64.b64decode(image_base64)

    parts = [
        types.Part.from_image(
            image=types.Image(image_bytes=image_bytes, mime_type="image/png")
        ),
        types.Part.from_text(
            f"Extract all {schema_type} data from this screenshot. "
            "Ignore UI elements like buttons, comments, navigation bars. "
            "Focus only on the actual content. Return valid JSON."
        ),
    ]

    schema_cls = SCHEMA_MAP.get(schema_type)

    generation_config = {}
    if schema_cls:
        generation_config = {
            "response_schema": schema_cls,
            "response_mime_type": "application/json",
        }

    response = await client.aio.models.generate_content(
        model="gemini-2.5-flash",
        contents=[types.Content(role="user", parts=parts)],
        config=types.GenerateContentConfig(**generation_config),
    )

    result_text = response.text
    parsed = json.loads(result_text)

    # Validate with Pydantic if schema available
    if schema_cls:
        validated = schema_cls.model_validate(parsed)
        return validated.model_dump(mode="json")

    return parsed
