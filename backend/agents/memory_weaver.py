"""Sequential agent for weaving memories with ordered steps."""

from google.adk.agents import LlmAgent
from google.adk.agents.sequential_agent import SequentialAgent

from backend.tools.query_bigquery import query_past_entries
from backend.tools.generate_audio import generate_audio_summary
from backend.tools.sync_notion import sync_extraction_to_notion
from backend.config.prompts import load_prompt

GEMINI_MODEL = "gemini-2.5-flash"
IMAGE_MODEL = "gemini-2.5-flash-image-preview"

# Step 1: Retrieve existing context
context_retriever = LlmAgent(
    name="ContextRetriever",
    model=GEMINI_MODEL,
    instruction="""Retrieve relevant past context based on the user's current input.
    Use the query_past_entries tool to look up similar memories or metrics.""",
    tools=[query_past_entries],
    output_key="past_context"
)

# Step 2: Generate the reflective narrative (Interleaved text/image)
narrative_generator = LlmAgent(
    name="NarrativeGenerator",
    model=IMAGE_MODEL,
    instruction=load_prompt("memory_weaver"),
    output_key="narrative_output"
)

# Step 3: Generate ambient audio summary
audio_generator = LlmAgent(
    name="AudioGenerator",
    model=GEMINI_MODEL,
    instruction="""Summarize the day's highlights into a short, ambient audio description.
    Use the generate_audio_summary tool to synthesize this into an audio file.""",
    tools=[generate_audio_summary],
    output_key="audio_url"
)

# Step 4: Persist the memory and extraction
persister = LlmAgent(
    name="Persister",
    model=GEMINI_MODEL,
    instruction="""Commit the final narrative, extraction data, and audio link to the 
    user's vault. Use the sync_extraction_to_notion tool.""",
    tools=[sync_extraction_to_notion],
    output_key="persistence_confirmation"
)

# The Sequential Memory Weaver Agent
memory_weaver_agent = SequentialAgent(
    name="MemoryWeaverAgent",
    sub_agents=[context_retriever, narrative_generator, audio_generator, persister],
    description="Weaves memories sequentially: Retrieval -> Narrative -> Audio -> Persistence."
)
