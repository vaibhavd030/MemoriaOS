"""UI Snipper Agent — the UI Navigator engine.

Processes screenshots using Gemini Vision to extract structured data
without DOM access or API calls.
"""

from google.adk.agents import LlmAgent

from backend.tools.extract_structured_data import extract_from_screenshot
from backend.tools.sync_notion import sync_extraction_to_notion

GEMINI_MODEL = "gemini-2.5-flash"

ui_snipper_agent = LlmAgent(
    name="UISnipperAgent",
    model=GEMINI_MODEL,
    instruction="""You are a visual UI parsing specialist. When given a screenshot:

1. IDENTIFY what type of content is shown:
   - Recipe/food content → extract as RecipeCard
   - Financial receipt/transaction → extract as ExpenseRecord
   - Workout plan/fitness content → extract as WorkoutSplit
   - General information → extract as GenericExtraction

2. USE the extract_from_screenshot tool with the image and the appropriate
   schema type.

3. IGNORE UI chrome (navigation bars, comments, likes, buttons, ads).
   Focus ONLY on the actual content.

4. After extraction, USE sync_extraction_to_notion to save the structured
   data to the appropriate Notion database.

5. Return a clean confirmation showing what was extracted.""",
    description="Extracts structured data from images and screenshots using Vision.",
    tools=[extract_from_screenshot, sync_extraction_to_notion],
)
