"""Google Photos Library API integration for MemoriaOS."""

from typing import Any

import httpx
import structlog

log = structlog.get_logger(__name__)


class GooglePhotosClient:
    """Client for interacting with the Google Photos Library API.

    Handles media item listing, searching, and raw content downloading.
    Uses an asynchronous HTTP client for performance.
    """

    BASE_URL = "https://photoslibrary.googleapis.com/v1"

    def __init__(self, access_token: str) -> None:
        """Initializes the Google Photos client with an access token.

        Args:
            access_token: A valid Google OAuth2 access token.
        """
        self.access_token = access_token
        self.client = httpx.AsyncClient(
            headers={"Authorization": f"Bearer {access_token}"},
            base_url=self.BASE_URL,
            timeout=10.0,
        )

    async def list_media_items(self, page_size: int = 10) -> list[dict[str, Any]]:
        """Lists recent media items from the user's library.

        Args:
            page_size (int): Maximum number of items to return in this call. Defaults to 10.

        Returns:
            list[dict[str, Any]]: A list of dictionary objects representing media items.

        Raises:
            httpx.HTTPStatusError: If the API request fails.
        """
        response = await self.client.get("/mediaItems", params={"pageSize": page_size})
        response.raise_for_status()
        return response.json().get("mediaItems", [])

    async def search_media_items(self, filters: dict[str, Any]) -> list[dict[str, Any]]:
        """Searches media items using specific filters.

        Args:
            filters (dict[str, Any]): Dictionary containing search criteria (dates, categories).

        Returns:
            list[dict[str, Any]]: A list of dictionary objects representing matching media items.

        Raises:
            httpx.HTTPStatusError: If the API request fails.
        """
        response = await self.client.post("/mediaItems:search", json={"filters": filters})
        response.raise_for_status()
        return response.json().get("mediaItems", [])

    async def download_media(self, base_url: str) -> bytes:
        """Downloads the raw binary content of a media item.

        Args:
            base_url (str): The baseUrl provided by the Google Photos API.

        Returns:
            bytes: The raw bytes of the image/video content.

        Raises:
            httpx.HTTPStatusError: If the download fails.
        """
        # baseUrl=d allows downloading the actual data
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}=d")
            response.raise_for_status()
            return response.content

    async def close(self) -> None:
        """Closes the underlying HTTP client."""
        await self.client.aclose()
