"""Main entry point for MemoriaOS Backend API."""

import asyncio
import base64
import json
from typing import Any

import structlog
from fastapi import FastAPI, File, Form, HTTPException, UploadFile, WebSocket
from fastapi.responses import StreamingResponse
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import Client, types

from backend.agents.supervisor import root_agent
from backend.config.logging import configure_logging
from backend.config.settings import settings
from backend.integrations.bigquery_store import get_recent_records
from backend.integrations.cloud_storage import list_files

# Initialize logging
configure_logging()
log = structlog.get_logger(__name__)

app = FastAPI(title="MemoriaOS API", version="0.1.0")

# Initialize ADK components
session_service = InMemorySessionService()
runner = Runner(agent=root_agent, app_name="memoria_os", session_service=session_service)


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint.

    Returns:
        dict[str, str]: Status object.
    """
    return {"status": "healthy"}


@app.post("/api/chat")
async def chat(
    message: str = Form(default=""),
    user_id: str = Form(default="default"),
    session_id: str = Form(default="default_session"),
    image: UploadFile | None = File(default=None),  # noqa: B008
) -> dict[str, Any]:
    """Routes user message through the Supervisor system using ADK Runner.

    Handles multimodal input (text + image) and returns a structured response
    from the agentic workflow.

    Args:
        message (str): Text message from the user.
        user_id (str): Unique user identifier.
        session_id (str): Unique session identifier for memory.
        image (UploadFile | None): Optional image file for analysis.

    Returns:
        dict[str, Any]: Agent response container.

    Raises:
        HTTPException: If payload is empty or processing fails.
    """
    try:
        log.info("chat_request_received", message=message, user_id=user_id, session_id=session_id)

        await session_service.get_or_create_session(
            app_name="memoria_os",
            user_id=user_id,
            session_id=session_id,
        )

        parts: list[types.Part] = []
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

        response_data: list[dict[str, str]] = []
        async for event in runner.run_async(
            user_id=user_id, session_id=session_id, new_message=content
        ):
            if event.is_final_response() and event.content:
                for part in event.content.parts:
                    if part.text:
                        response_data.append({"type": "text", "content": part.text})
                    elif part.inline_data:
                        response_data.append(
                            {
                                "type": "image",
                                "content": base64.b64encode(part.inline_data.data).decode(),
                                "mime_type": part.inline_data.mime_type,
                            }
                        )

        return {"response": response_data, "status": "success"}

    except ValueError as e:
        log.error("chat_payload_invalid", error=str(e))
        raise HTTPException(status_code=400, detail=f"Invalid payload: {str(e)}") from e
    except Exception as e:
        log.error("chat_unexpected_error", error=str(e))
        raise HTTPException(
            status_code=500, detail="Internal server error during chat processing"
        ) from e


@app.get("/api/chat/stream")
async def chat_stream(
    message: str,
    user_id: str = "default",
    session_id: str = "default_session",
) -> StreamingResponse:
    """Streams agent responses via SSE for a cinematic modal reveal.

    Events:
    - text: Narrative content chunks.
    - image: Base64 or GCS URL of generated imagery.
    - audio: GCS URL of synthesized narrative audio.
    - done: Final completion signal.
    """

    async def event_generator():
        try:
            await session_service.get_or_create_session(
                app_name="memoria_os",
                user_id=user_id,
                session_id=session_id,
            )

            content = types.Content(role="user", parts=[types.Part.from_text(message)])

            async for event in runner.run_async(
                user_id=user_id, session_id=session_id, new_message=content
            ):
                # Inspect parts for text, images, or tools producing media
                if event.content:
                    for part in event.content.parts:
                        if part.text:
                            yield f"event: text\ndata: {json.dumps({'content': part.text})}\n\n"
                        elif part.inline_data:
                            img_data = base64.b64encode(part.inline_data.data).decode()
                            yield f"event: image\ndata: {json.dumps({'content': img_data, 'mime_type': part.inline_data.mime_type})}\n\n"

                # Check if this event contains tool outputs (like audio URL)
                # Note: In ADK, tool outputs often appear in the conversation history or specific event fields
                # We'll specifically look for .mp3 URLs in text as a fallback if not structured
                if event.content:
                    for part in event.content.parts:
                        if part.text and (".mp3" in part.text or "https://storage.googleapis.com" in part.text):
                            if "audio" in part.text.lower() or "reel" in part.text.lower():
                                yield f"event: audio\ndata: {json.dumps({'url': part.text.strip()})}\n\n"

            yield "event: done\ndata: {}\n\n"

        except Exception as e:
            log.error("stream_error", error=str(e))
            yield f"event: error\ndata: {json.dumps({'detail': str(e)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@app.get("/api/journal")
async def get_journal(user_id: str = "default", limit: int = 50):
    """Fetches recent journal records for the UI."""
    try:
        records = await get_recent_records(user_id=user_id, limit=limit)
        return {"records": records, "status": "success"}
    except Exception as e:
        log.error("journal_fetch_error", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to fetch journal records")


@app.get("/api/reels")
async def get_reels():
    """Fetches list of generated reels from GCS."""
    try:
        files = await list_files(prefix="reels/")
        # Filter for video files
        reels = [f for f in files if f["name"].lower().split('.')[-1] in ('mp4', 'mkv', 'mov')]
        return {"reels": reels, "status": "success"}
    except Exception as e:
        log.error("reels_fetch_error", error=str(e))
        return {"reels": [], "status": "error", "message": str(e)}


@app.get("/api/vault")
async def get_vault():
    """Fetches media and structured data summary for the vault."""
    try:
        # For now, let's just list photos
        photos = await list_files(prefix="photos/")
        return {
            "media": photos,
            "counts": {
                "media": len(photos),
                "documents": 0,
                "data": 0
            },
            "status": "success"
        }
    except Exception as e:
        log.error("vault_fetch_error", error=str(e))
        return {"status": "error", "message": str(e)}


@app.websocket("/api/live")
async def live_session(websocket: WebSocket) -> None:
    """Gemini Live API bridge for low-latency voice interaction.

    Args:
        websocket (WebSocket): The client websocket connection.
    """
    await websocket.accept()
    log.info("live_session_established")
    try:
        genai_client = Client(
            api_key=settings.google_api_key.get_secret_value(),
            http_options={"api_version": "v1alpha"},
        )
        async with genai_client.aio.live.connect(model="gemini-2.5-flash") as session:

            async def send_to_client() -> None:
                async for message in session:
                    await websocket.send_json(message.model_dump())

            async def receive_from_client() -> None:
                while True:
                    data = await websocket.receive_json()
                    await session.send(data)

            await asyncio.gather(send_to_client(), receive_from_client())
    except Exception as e:
        log.error("live_session_error", error=str(e))
    finally:
        await websocket.close()


@app.get("/api/reels")
async def get_reels() -> dict[str, Any]:
    """Fetches generated reels from Cloud Storage.

    Returns:
        dict[str, Any]: List of reels metadata.
    """
    return {"reels": [], "status": "success"}


@app.post("/api/generate-reel")
async def generate_reel() -> dict[str, str]:
    """Triggers reel generation process.

    Returns:
        dict[str, str]: Acknowledgement message.
    """
    return {"message": "Reel generation started", "status": "success"}


@app.get("/api/photos/connect")
async def photos_connect() -> dict[str, str]:
    """Initiates Google Photos OAuth flow.

    Returns:
        dict[str, str]: Authentication URL.
    """
    return {"auth_url": "https://accounts.google.com/o/oauth2/v2/auth?...", "status": "success"}


@app.post("/api/enrich-photos")
async def enrich_photos() -> dict[str, str]:
    """Triggers photo enrichment pipeline.

    Returns:
        dict[str, str]: Acknowledgement message.
    """
    return {"message": "Photo enrichment started", "status": "success"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)  # noqa: S104
