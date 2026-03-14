"""Agent for querying past memories and data using SQL."""

from google.adk.agents import LlmAgent

from backend.tools.query_bigquery import query_past_entries

GEMINI_MODEL = "gemini-2.5-flash"

query_agent = LlmAgent(
    name="QueryAgent",
    model=GEMINI_MODEL,
    instruction="""You are the MemoriaOS Archivist. Your job is to answer questions
about the user's past data.

1. USE the query_past_entries tool to search BigQuery for relevant records.
2. SYNTHESIZE the raw data into a human-friendly answer.
3. BE PRECISE with dates and metrics (e.g. "You slept 7.2 hours on Tuesday").
4. If no data is found, be honest and suggest how they might log it in the future.""",
    description="Analyzes historical trends and answers data-driven queries.",
    tools=[query_past_entries],
)
