"""Overall container for all extracted data in MemoriaOS."""

from __future__ import annotations

from pydantic import BaseModel, Field

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


class ExtractedData(BaseModel):
    """Container for all data extracted from a single user message or image."""

    # Wellness (Legacy)
    sleep: SleepEntry | None = None
    exercise: list[ExerciseEntry] = Field(default_factory=list)
    meditation: list[MeditationEntry] = Field(default_factory=list)
    cleaning: list[CleaningEntry] = Field(default_factory=list)
    sitting: list[SittingEntry] = Field(default_factory=list)
    group_meditation: list[GroupMeditationEntry] = Field(default_factory=list)
    habits: list[HabitEntry] = Field(default_factory=list)

    # Tasks & Links (Legacy)
    tasks: list[TaskItem] = Field(default_factory=list)
    reading_links: list[ReadingLink] = Field(default_factory=list)

    # New MemoriaOS Domains
    recipe: RecipeCard | None = None
    expense: ExpenseRecord | None = None
    workout: WorkoutSplit | None = None

    # General
    journal_note: str | None = None
