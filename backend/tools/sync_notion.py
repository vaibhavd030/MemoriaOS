"""ADK Tool for syncing extracted data to Notion."""

from typing import Any

from backend.integrations.notion_store import sync_extraction_to_notion


async def sync_to_notion(data: Any) -> bool:
    """Sync generic data to Notion.

    Args:
        data (Any): The structured data object or dictionary to sync.

    Returns:
        bool: True if sync succeeded, False otherwise.
    """
    return await sync_extraction_to_notion(data)
