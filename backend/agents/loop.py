"""Agent for handling clarification loops with the user."""

from google.adk.agents import LlmAgent

GEMINI_MODEL = "gemini-2.0-flash"

loop_agent = LlmAgent(
    name="LoopAgent",
    model=GEMINI_MODEL,
    instruction="""You are the MemoriaOS Concierge. Your job is to handle
clarification requests from other agents.

If an agent (like MemoryWeaver or UISnipper) is unsure about a detail, they
delegate to you. You should:
1. REVIEW the context of the confusion.
2. CRAFT a polite, concise question for the user to clarify.
3. Once the user responds, delegate back to the original agent with the new info.

Your goal is to be helpful without being annoying. Keep the loop turns minimal.""",
    description="Handles user clarification loops.",
    sub_agents=[], 
)
