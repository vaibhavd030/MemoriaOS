"""Main entry point for MemoriaOS Backend API."""

import structlog
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.agents.supervisor import root_agent
from backend.config.logging import configure_logging

# Initialize logging
configure_logging()
log = structlog.get_logger(__name__)

app = FastAPI(title="MemoriaOS API", version="0.1.0")

class ChatRequest(BaseModel):
    message: str
    user_id: str = "default_user"

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/chat")
async def chat(request: ChatRequest):
    """Route user message through the Supervisor system."""
    try:
        log.info("chat_request_received", message=request.message, user_id=request.user_id)
        
        # In a real ADK session, we would manage state/history. 
        # For this demo, we'll run a single step.
        response = await root_agent.run(request.message)
        
        return {
            "response": response.text,
            "agent": response.agent_name,
            "status": "success"
        }
    except Exception as e:
        log.error("chat_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
