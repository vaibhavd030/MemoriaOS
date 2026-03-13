"""Supervisor Agent — routes user intent to specialised sub-agents.

This is the root agent of the MemoriaOS multi-agent system.
"""

from google.adk.agents import LlmAgent
from backend.agents.memory_weaver import memory_weaver_agent
from backend.agents.ui_snipper import ui_snipper_agent
from backend.agents.reel_generator import reel_generator_agent
from backend.agents.loop import loop_agent
from backend.agents.query_agent import query_agent

GEMINI_MODEL = "gemini-2.5-flash"

supervisor_agent = LlmAgent(
    name="SupervisorAgent",
    model=GEMINI_MODEL,
    instruction="""You are the MemoriaOS Supervisor. Your job is to inspect the
user's input and route to the correct specialist agent.

ROUTING RULES:
- If the input contains an image/screenshot, delegate to UISnipperAgent.
- If the user is asking a question about their past data, delegate to QueryAgent.
- If the user wants a weekly summary or a "Reel", delegate to ReelGeneratorAgent.
- If this is a follow-up clarification, delegate to LoopAgent.
- For EVERYTHING else, delegate to MemoryWeaverAgent.

Do NOT try to answer the user directly.""",
    description="Routes user inputs to the appropriate specialist agent.",
    sub_agents=[ui_snipper_agent, memory_weaver_agent, reel_generator_agent, loop_agent, query_agent],
)

root_agent = supervisor_agent
