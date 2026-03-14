"""Notion API integration for MemoriaOS."""

from __future__ import annotations

from collections.abc import Callable, Coroutine
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any

import httpx
import structlog
from notion_client import AsyncClient
from tenacity import retry, stop_after_attempt, wait_exponential

from backend.config.settings import settings
from backend.models.finance import ExpenseRecord
from backend.models.fitness import WorkoutSplit
from backend.models.recipes import RecipeCard
from backend.models.tasks import TaskItem

log = structlog.get_logger(__name__)

_notion_client: AsyncClient | None = None


def _get_now_formatted() -> str:
    """Gets current timestamp formatted for Notion titles.

    Returns:
        str: Formatted string like '13 March 2026 11:45pm'.
    """
    now = datetime.now()
    time_str = now.strftime("%I:%M%p").lstrip("0").lower()
    return f"{now.day} {now.strftime('%B %Y')} {time_str}"


def _format_date_only(d: date) -> str:
    """Formats a date object for Notion display.

    Args:
        d (date): The date to format.

    Returns:
        str: Formatted date string.
    """
    return f"{d.day} {d.strftime('%B %Y')}"


def _bullet_block(text: str) -> dict[str, Any]:
    """Creates a Notion bulleted list item block.

    Args:
        text (str): The text content for the bullet.

    Returns:
        dict[str, Any]: Notion block dictionary.
    """
    return {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": text}}]},
    }


def _get_notion() -> AsyncClient:
    """Lazily instantiates the Notion client.

    Returns:
        AsyncClient: The authenticated Notion client.

    Raises:
        RuntimeError: If NOTION_API_KEY is missing.
    """
    global _notion_client
    if _notion_client is None:
        if not settings.notion_api_key:
            raise RuntimeError("NOTION_API_KEY not set")
        _notion_client = AsyncClient(auth=settings.notion_api_key.get_secret_value())
    return _notion_client


@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=8), reraise=True)
async def _append_blocks(
    notion: AsyncClient, block_id: str, children: list[dict[str, Any]]
) -> None:
    """Appends blocks to a Notion parent with retries.

    Args:
        notion (AsyncClient): Authenticated client.
        block_id (str): ID of the parent block/page.
        children (list[dict[str, Any]]): List of blocks to append.
    """
    await notion.blocks.children.append(block_id=block_id, children=children)


@dataclass(slots=True)
class SyncConfig:
    """Configuration for routing data types to Notion.

    Attributes:
        page_id_attr (str): Setting name for the target page ID.
        block_builder (Callable): Function to transform data into blocks.
    """

    page_id_attr: str
    block_builder: Callable[[Any], Coroutine[Any, Any, list[dict[str, Any]]]]


# ── Builders ─────────────────────────────────────────────────────────


async def _build_tasks(tasks: list[TaskItem]) -> list[dict[str, Any]]:
    """Builds Notion blocks for task items."""
    return []


async def _build_recipes(recipe: RecipeCard) -> list[dict[str, Any]]:
    """Builds Notion blocks for a recipe card."""
    blocks = [
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {"rich_text": [{"text": {"content": recipe.title}}]},
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [{"text": {"content": recipe.description or ""}}]},
        },
    ]
    blocks.append(_bullet_block("Ingredients:"))
    for ing in recipe.ingredients:
        blocks.append(_bullet_block(f"- {ing.quantity or ''} {ing.name}"))
    return blocks


async def _build_expenses(expense: ExpenseRecord) -> list[dict[str, Any]]:
    """Builds Notion blocks for an expense record."""
    text = (
        f"💰 {expense.date}: {expense.vendor} - {expense.currency} "
        f"{expense.amount} ({expense.category})"
    )
    return [_bullet_block(text)]


async def _build_workouts(workout: WorkoutSplit) -> list[dict[str, Any]]:
    """Builds Notion blocks for a workout split."""
    blocks = [
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {"rich_text": [{"text": {"content": f"🏋️ {workout.title}"}}]},
        }
    ]
    for ex in workout.exercises:
        blocks.append(_bullet_block(f"{ex.name}: {ex.sets}x{ex.reps} @ {ex.weight_kg}kg"))
    return blocks


# ── Sync Config ──────────────────────────────────────────────────────

_SYNC_CONFIGS: dict[str, SyncConfig] = {
    "recipe": SyncConfig(page_id_attr="notion_wellness_page_id", block_builder=_build_recipes),
    "expense": SyncConfig(page_id_attr="notion_wellness_page_id", block_builder=_build_expenses),
    "workout": SyncConfig(page_id_attr="notion_wellness_page_id", block_builder=_build_workouts),
}


async def sync_extraction_to_notion(data: Any) -> bool:
    """ADK Tool for syncing an extraction to Notion.

    Args:
        data (Any): The Pydantic model or list of models to sync.

    Returns:
        bool: True if sync succeeded, False otherwise.
    """
    notion = _get_notion()

    try:
        config: SyncConfig | None = None
        data_item: Any = None

        is_list = isinstance(data, (list, tuple)) and len(data) > 0
        data_item = data[0] if is_list else data

        if isinstance(data_item, RecipeCard):
            config = _SYNC_CONFIGS["recipe"]
        elif isinstance(data_item, ExpenseRecord):
            config = _SYNC_CONFIGS["expense"]
        elif isinstance(data_item, WorkoutSplit):
            config = _SYNC_CONFIGS["workout"]

        if not config:
            log.warning("no_sync_config_found", type=type(data_item))
            return False

        target_page_id: str | None = getattr(settings, config.page_id_attr, None)
        if not target_page_id:
            log.error("target_page_id_not_set", attr=config.page_id_attr)
            return False

        blocks = await config.block_builder(data_item)
        await _append_blocks(notion, target_page_id, blocks)
        log.info("sync_to_notion_success", type=type(data_item))
        return True

    except httpx.HTTPStatusError as e:
        log.error("notion_api_status_error", error=str(e), code=e.response.status_code)
        return False
    except httpx.RequestError as e:
        log.error("notion_request_failed", error=str(e))
        return False
    except Exception as e:
        log.error("sync_to_notion_unexpected_error", error=str(e))
        return False
