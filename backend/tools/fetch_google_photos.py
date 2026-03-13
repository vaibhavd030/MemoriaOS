"""ADK Tool for fetching and analyzing recent Google Photos."""

import structlog
from backend.integrations.google_photos import GooglePhotosClient

log = structlog.get_logger(__name__)

async def fetch_and_analyze_recent_photos(access_token: str, limit: int = 5) -> str:
    """Fetch recent photos and get a brief Gemini description of them."""
    gp_client = GooglePhotosClient(access_token)
    try:
        items = await gp_client.list_media_items(page_size=limit)
        if not items:
            return "No recent photos found."
        
        # In a real implementation, we would download the bytes and send to Gemini Vision.
        # For now, we'll return the descriptions or captions if available.
        summaries = []
        for item in items:
            desc = item.get("description", "Untitled Photo")
            summaries.append(f"- {desc}")
        
        return "\n".join(summaries)
    except Exception as e:
        log.error(f"Error fetching photos: {e}")
        return f"Error fetching photos: {e}"
    finally:
        await gp_client.close()
