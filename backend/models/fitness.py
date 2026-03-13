"""New Pydantic schemas for MemoriaOS UI Navigator track: Fitness."""

from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, Field


class WorkoutExercise(BaseModel):
    """A single exercise within a workout split."""

    name: str = Field(description="Exercise name, e.g. 'Bench Press'")
    sets: int | None = Field(default=None, ge=1)
    reps: int | None = Field(default=None, ge=1)
    weight_kg: float | None = Field(default=None, ge=0)
    duration_seconds: int | None = Field(default=None, ge=0)
    notes: str | None = None


class WorkoutSplit(BaseModel):
    """Workout plan extracted from a screenshot."""

    title: str
    focus_areas: list[str] = Field(
        default_factory=list,
        description="e.g. ['chest', 'shoulders', 'triceps']",
    )
    exercises: list[WorkoutExercise] = Field(default_factory=list)
    estimated_duration_minutes: int | None = Field(default=None, ge=0)
    difficulty: Annotated[int, Field(ge=1, le=5)] | None = None
    source_url: str | None = None
