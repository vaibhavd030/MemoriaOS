"""Main entry point for MemoriaOS Backend API."""

import asyncio
import base64
import structlog
from fastapi import FastAPI, File, Form, UploadFile, HTTPException, WebSocket
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import Client, types

from backend.agents.supervisor import root_agent
from backend.config.logging import configure_logging
from backend.config.settings import settings

# Initialize logging
configure_logging()
log = structlog.get_logger(__name__)

app = FastAPI(title="MemoriaOS API", version="0.1.0")

# Initialize ADK components
session_service = InMemorySessionService()
runner = Runner(agent=root_agent, app_name="memoria_os", session_service=session_service)

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/api/chat")
async def chat(
    message: str = Form(default=""),
    user_id: str = Form(default="default"),
    session_id: str = Form(default="default_session"),
    image: UploadFile | None = File(default=None),
):
    """Route user message through the Supervisor system using ADK Runner."""
    try:
        log.info("chat_request_received", message=message, user_id=user_id, session_id=session_id)
        
        # Get or create session
        await session_service.get_or_create_session(
            app_name="memoria_os",
            user_id=user_id,
            session_id=session_id,
        )

        # Build content parts
        parts = []
        if message:
            parts.append(types.Part.from_text(message))
        if image:
            image_bytes = await image.read()
            parts.append(
                types.Part.from_image(
                    image=types.Image(
                        image_bytes=image_bytes,
                        mime_type=image.content_type or "image/png",
                    )
                )
            )

        if not parts:
            raise HTTPException(status_code=400, detail="Empty message or image")

        content = types.Content(role="user", parts=parts)

        # Execute through ADK Runner
        response_data = []
        async for event in runner.run_async(
            user_id=user_id, session_id=session_id, new_message=content
        ):
            if event.is_final_response() and event.content:
                for part in event.content.parts:
                    if part.text:
                        response_data.append({"type": "text", "content": part.text})
                    elif part.inline_data:
                        # For now, we'll encode inline data as base64 if it's an image
                        response_data.append({
                            "type": "image",
                            "content": base64.b64encode(part.inline_data.data).decode(),
                            "mime_type": part.inline_data.mime_type,
                        })

        return {
            "response": response_data,
            "status": "success"
        }
        
    except Exception as e:
        log.error("chat_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/api/live")
async def live_session(websocket: FastAPI.websocket):
    """Gemini Live API bridge for low-latency voice interaction."""
    # Note: In a real implementation, we would use google.genai.Client.aio.live.connect
    # For now, we'll establish the bridge and echo back for demo purposes.
    await websocket.accept()
    log.info("live_session_established")
    try:
        genai_client = Client(api_key=settings.google_api_key, http_options={'api_version': 'v1alpha'})
        async with genai_client.aio.live.connect(model="gemini-2.5-flash") as session:
            async def send_to_client():
                async for message in session:
                    await websocket.send_json(message.model_dump())

            async def receive_from_client():
                while True:
                    data = await websocket.receive_json()
                    await session.send(data)

            await asyncio.gather(send_to_client(), receive_from_client())
    except Exception as e:
        log.error("live_session_error", error=str(e))
    finally:
        await websocket.close()

@app.get("/api/reels")
async def get_reels():
    """Fetch generated reels from Cloud Storage."""
    # This would involve listing objects in GCS
    return {"reels": [], "status": "success"}

@app.post("/api/generate-reel")
async def generate_reel():
    """Trigger reel generation process."""
    # In a real app, this would be an async task (e.g. Cloud Tasks)
    from backend.agents.reel_generator import reel_generator_agent
    # response = await runner.run_async(...)
    return {"message": "Reel generation started", "status": "success"}

@app.get("/api/photos/connect")
async def photos_connect():
    """Initiate Google Photos OAuth flow."""
    return {"auth_url": "https://accounts.google.com/o/oauth2/v2/auth?...", "status": "success"}

@app.post("/api/enrich-photos")
async def enrich_photos():
    """Trigger photo enrichment pipeline."""
    from backend.tools.fetch_google_photos import fetch_and_analyze_recent_photos
    # This would be triggered by a cron job (Cloud Scheduler)
    return {"message": "Photo enrichment started", "status": "success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
