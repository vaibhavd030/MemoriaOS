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


class PhotoAnalysis(BaseModel):
    """Structured analysis of a Google Photo via Gemini Vision.

    Attributes:
        timestamp (str): When the photo was taken.
        location (str | None): Inferred location.
        activity (str | None): Activity detected in photo.
        objects (list[str]): List of objects identified.
        mood (str | None): Emotional tone of the photo.
        inferred_context (str | None): Narrative context.
    """

    timestamp: str = Field(default="Unknown", description="When the photo was taken")
    location: str | None = Field(default=None, description="Inferred location from visual cues")
    activity: str | None = Field(default=None, description="Activity depicted")
    objects: list[str] = Field(default_factory=list, description="Objects identified")
    mood: str | None = Field(default=None, description="Emotional tone")
    inferred_context: str | None = Field(default=None, description="Narrative context")


class ExtractedData(BaseModel):
    """Container for all data extracted from a single user message or image.

    Attributes:
        sleep (SleepEntry | None): Extracted sleep data.
        exercise (list[ExerciseEntry]): Extracted exercises.
        meditation (list[MeditationEntry]): Meditation sessions.
        cleaning (list[CleaningEntry]): Cleaning sessions.
        sitting (list[SittingEntry]): Sitting sessions.
        group_meditation (list[GroupMeditationEntry]): Group sessions.
        habits (list[HabitEntry]): Habit events.
        tasks (list[TaskItem]): New tasks identified.
        reading_links (list[ReadingLink]): Links to read later.
        recipe (RecipeCard | None): Full recipe extraction.
        expense (ExpenseRecord | None): Financial expense record.
        workout (WorkoutSplit | None): Full workout plan.
        photos (list[PhotoAnalysis]): Enriched photo data.
        journal_note (str | None): Accompanying narrative/text.
    """

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
    photos: list[PhotoAnalysis] = Field(default_factory=list)

    # General
    journal_note: str | None = None
