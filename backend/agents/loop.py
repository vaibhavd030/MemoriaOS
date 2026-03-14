"""Loop agent for clarifying ambiguous or missing information.

Manages a stateful conversation loop to ensure all necessary data for extraction
is present before proceeding.
"""

from google.adk.agents import LlmAgent, LoopAgent

from backend.config.prompts import load_prompt

GEMINI_MODEL = "gemini-2.5-flash"

# Agent to ask clarifying questions
clarifier = LlmAgent(
    name="Clarifier",
    model=GEMINI_MODEL,
    instruction=load_prompt("clarifier"),
    output_key="clarification_question",
    description="Asks targeted questions to fill gaps in user intent.",
)

# Agent to validate if we have enough info to proceed
validator = LlmAgent(
    name="Validator",
    model=GEMINI_MODEL,
    instruction=load_prompt("validator"),
    output_key="loop_status",
    description="Determines if the clarification loop should exit or continue.",
)

# The Loop Agent
loop_agent = LoopAgent(
    name="LoopAgent",
    sub_agents=[clarifier, validator],
    max_iterations=3,
    description="Manages clarification loops with the user until intent is clear.",
)
