"""Google Photos Library API integration for MemoriaOS."""

import httpx
import structlog
from typing import Any, Optional
from backend.config.settings import settings

log = structlog.get_logger(__name__)

class GooglePhotosClient:
    """Simple client for Google Photos Library API."""
    
    BASE_URL = "https://photoslibrary.googleapis.com/v1"

    def __init__(self, access_token: str):
        self.access_token = access_token
        self.client = httpx.AsyncClient(
            headers={"Authorization": f"Bearer {access_token}"},
            base_url=self.BASE_URL,
            timeout=10.0
        )

    async def list_media_items(self, page_size: int = 10) -> list[dict[str, Any]]:
        """List recent media items."""
        response = await self.client.get("/mediaItems", params={"pageSize": page_size})
        response.raise_for_status()
        return response.json().get("mediaItems", [])

    async def search_media_items(self, filters: dict[str, Any]) -> list[dict[str, Any]]:
        """Search media items (e.g. by date range or content categories)."""
        response = await self.client.post("/mediaItems:search", json={"filters": filters})
        response.raise_for_status()
        return response.json().get("mediaItems", [])

    async def close(self):
        await self.client.aclose()
