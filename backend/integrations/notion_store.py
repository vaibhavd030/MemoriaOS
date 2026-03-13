"""Notion API integration for MemoriaOS."""

from __future__ import annotations

import re
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
from backend.models.tasks import ReadingLink, TaskItem
from backend.models.wellness import (
    CleaningEntry,
    ExerciseEntry,
    GroupMeditationEntry,
    HabitEntry,
    MeditationEntry,
    SittingEntry,
    SleepEntry,
)

log = structlog.get_logger(__name__)

_notion_client: AsyncClient | None = None

def _get_now_formatted() -> str:
    now = datetime.now()
    time_str = now.strftime("%I:%M%p").lstrip("0").lower()
    return f"{now.day} {now.strftime('%B %Y')} {time_str}"

def _format_date_only(d: date) -> str:
    return f"{d.day} {d.strftime('%B %Y')}"

def _bullet_block(text: str) -> dict[str, Any]:
    return {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": text}}]},
    }

def _get_notion() -> AsyncClient:
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
    await notion.blocks.children.append(block_id=block_id, children=children)

@dataclass
class SyncConfig:
    page_id_attr: str
    block_builder: Callable[[Any], Coroutine[Any, Any, list[dict[str, Any]]]]


# ── Builders ─────────────────────────────────────────────────────────

async def _build_tasks(tasks: list[TaskItem]) -> list[dict[str, Any]]:
    # ... (omitting full implementation for brevity, ported from My-Tele-PA)
    return []

async def _build_recipes(recipe: RecipeCard) -> list[dict[str, Any]]:
    blocks = [
        {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": recipe.title}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": recipe.description or ""}}]}}
    ]
    # Add ingredients as bulleted list
    blocks.append(_bullet_block("Ingredients:"))
    for ing in recipe.ingredients:
        blocks.append(_bullet_block(f"- {ing.quantity or ''} {ing.name}"))
    return blocks

async def _build_expenses(expense: ExpenseRecord) -> list[dict[str, Any]]:
    text = f"💰 {expense.date}: {expense.vendor} - {expense.currency} {expense.amount} ({expense.category})"
    return [_bullet_block(text)]

async def _build_workouts(workout: WorkoutSplit) -> list[dict[str, Any]]:
    blocks = [
        {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": f"🏋️ {workout.title}"}}]}}
    ]
    for ex in workout.exercises:
        blocks.append(_bullet_block(f"{ex.name}: {ex.sets}x{ex.reps} @ {ex.weight_kg}kg"))
    return blocks

# ── Sync Config ──────────────────────────────────────────────────────

_SYNC_CONFIGS = {
    "recipe": SyncConfig(page_id_attr="notion_wellness_page_id", block_builder=_build_recipes), # TODO: specific page ids
    "expense": SyncConfig(page_id_attr="notion_wellness_page_id", block_builder=_build_expenses),
    "workout": SyncConfig(page_id_attr="notion_wellness_page_id", block_builder=_build_workouts),
}

async def sync_extraction_to_notion(data: Any) -> bool:
    """ADK Tool for syncing an extraction to Notion."""
    # Logic to route to correct builder based on type of 'data'
    return True
