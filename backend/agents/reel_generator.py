"""Agent for generating weekly Memory Reels.

Summarizes the week's memories and coordinates video compilation.
"""

from google.adk.agents import LlmAgent

from backend.tools.compile_video import compile_reel_video
from backend.tools.query_bigquery import query_past_entries

GEMINI_MODEL = "gemini-2.5-flash"

reel_generator_agent = LlmAgent(
    name="ReelGeneratorAgent",
    model=GEMINI_MODEL,
    instruction="""You are the MemoriaOS Reel Director. Your job is to create a
compelling weekly summary (a "Reel") for the user.

STEPS:
1. QUERY past entries from the last 7 days using query_past_entries.
2. SYNTHESIZE a high-level narrative of the week's achievements, moods, and events.
3. SELECT the best photos (if available) to include in the visual reel.
4. COORDINATE with the compile_video tool to create the final MP4 asset.

The narrative should be uplifting and reflective of growth.""",
    description="Generates weekly video reels and summaries.",
    tools=[query_past_entries, compile_reel_video],
)
