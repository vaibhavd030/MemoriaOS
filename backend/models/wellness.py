"""Pydantic v2 data models for all wellness tracking categories."""

from __future__ import annotations

import enum
from datetime import date as dt_date
from datetime import datetime as dt_datetime
from typing import Annotated

from pydantic import BaseModel, Field, field_validator, model_validator


class SleepEntry(BaseModel):
    """A single night of sleep data.

    Attributes:
        date (dt_date): Calendar date of the sleep.
        bedtime_hour (int | None): Hour went to sleep (0-23).
        bedtime_minute (int | None): Minute went to sleep (0-59).
        wake_hour (int | None): Hour woke up (0-23).
        wake_minute (int | None): Minute woke up (0-59).
        duration_hours (float | None): Total sleep duration.
        quality (int | None): Quality rating from 1-10.
        notes (str | None): Additional notes.
    """

    date: dt_date = Field(description="Calendar date of the sleep")
    bedtime_hour: Annotated[int, Field(ge=0, le=23)] | None = Field(
        default=None, description="Hour went to sleep"
    )
    bedtime_minute: Annotated[int, Field(ge=0, le=59)] | None = Field(default=None)
    wake_hour: Annotated[int, Field(ge=0, le=23)] | None = Field(
        default=None, description="Hour woke up"
    )
    wake_minute: Annotated[int, Field(ge=0, le=59)] | None = Field(default=None)
    duration_hours: float | None = Field(
        default=None, description="Total sleep duration if specific times are not given"
    )
    quality: Annotated[int, Field(ge=1, le=10)] | None = Field(
        default=None, description="Quality rating from 1-10"
    )
    notes: str | None = None

    @model_validator(mode="after")
    def compute_duration(self) -> SleepEntry:
        """Computes sleep duration and auto-rates quality.

        Returns:
            SleepEntry: The validated model with computed fields.
        """
        # Calculate duration if exact times are given
        if (
            self.bedtime_hour is not None
            and self.wake_hour is not None
            and self.bedtime_minute is not None
            and self.wake_minute is not None
        ):

            bh = self.bedtime_hour
            bm = self.bedtime_minute
            wh = self.wake_hour
            wm = self.wake_minute

            bed_total_mins = bh * 60 + bm
            wake_total_mins = wh * 60 + wm

            if wake_total_mins <= bed_total_mins:
                wake_total_mins += 24 * 60

            calculated_duration = float(wake_total_mins - bed_total_mins) / 60.0

            # Use calculated duration if none is explicitly provided, or override
            if self.duration_hours is None:
                self.duration_hours = round(calculated_duration, 2)

        # Auto-calculate excellent quality rating
        if (
            self.duration_hours is not None
            and self.bedtime_hour is not None
            and self.bedtime_hour <= 22
            and self.duration_hours >= 7.5
            and self.quality is None
        ):
            self.quality = 10

        return self

    @field_validator("bedtime_hour")
    @classmethod
    def validate_bedtime_is_evening(cls, v: int | None) -> int | None:
        """Warns if bedtime looks like daytime (potential extraction error).

        Args:
            v (int | None): The hour value to validate.

        Returns:
            int | None: The validated hour value.
        """
        if v is not None and 9 <= v <= 17:
            import logging

            logging.getLogger(__name__).warning(f"Unusual bedtime: {v}")
        return v


class ExerciseType(enum.StrEnum):
    """Supported exercise types for tracking."""

    RUN = "run"
    WALK = "walk"
    GYM = "gym"
    WEIGHTS = "weights"
    YOGA = "yoga"
    SWIM = "swim"
    CYCLE = "cycle"
    OTHER = "other"


class MuscleGroup(enum.StrEnum):
    """Primary muscle groups for targeted workout tracking."""

    FULL_BODY = "full_body"
    CHEST = "chest"
    BICEPS = "biceps"
    TRICEPS = "triceps"
    SHOULDERS = "shoulders"
    BACK = "back"
    ABS = "abs"
    LOWER_BODY = "lower_body"
    OTHER = "other"


class ExerciseEntry(BaseModel):
    """A single exercise / training session.

    Attributes:
        date (dt_date): Date of the session.
        exercise_type (ExerciseType | None): Type of exercise.
        body_parts (list[MuscleGroup] | None): Muscle groups trained.
        duration_minutes (int | None): Duration in minutes.
        distance_km (float | None): Distance in km.
        intensity (int | None): Intensity score from 1-10.
        notes (str | None): Additional notes.
    """

    date: dt_date
    exercise_type: ExerciseType | None = None
    body_parts: list[MuscleGroup] | None = Field(
        default=None,
        description=(
            "Muscle groups trained — only for gym/weights sessions. "
            "Options: full_body, chest, biceps, triceps, shoulders, back, abs, lower_body."
        ),
    )
    duration_minutes: Annotated[int, Field(gt=0, le=600)] | None = None
    distance_km: Annotated[float, Field(ge=0)] | None = None
    intensity: Annotated[int, Field(ge=1, le=10)] | None = Field(
        default=None,
        description=(
            "Intensity score from 1-10. If the user uses words like "
            "'intense', 'hard', 'tiring', infer a score of 8 or 9."
        ),
    )
    notes: str | None = Field(default=None, max_length=500)


class PracticeBase(BaseModel):
    """Base for all spiritual practices.

    Attributes:
        date (dt_date): Date of the practice.
        datetime_logged (dt_datetime | None): Exact time if known.
        duration_minutes (int | None): Duration in minutes.
        notes (str | None): Additional notes.
    """

    date: dt_date
    datetime_logged: dt_datetime | None = Field(
        default=None,
        description=(
            "The datetime when the practice was done. "
            "If user specifies a time, combine with date. "
            "If not specified, leave null and system will auto-fill."
        ),
    )
    duration_minutes: Annotated[int, Field(ge=1, le=300)] | None = None
    notes: str | None = Field(default=None, max_length=1000)


class MeditationEntry(PracticeBase):
    """General / unspecified meditation session."""

    pass


class CleaningEntry(PracticeBase):
    """Heartfulness cleaning practice session."""

    pass


class SittingEntry(PracticeBase):
    """Heartfulness sitting / transmission practice."""

    took_from: str | None = Field(
        default=None, description="Name of the trainer/preceptor who gave the sitting"
    )


class GroupMeditationEntry(PracticeBase):
    """Satsang / group meditation session."""

    place: str | None = Field(default=None, description="Location/venue of the group meditation")


class HabitCategory(enum.StrEnum):
    """Categories for tracking daily habits and self-control."""

    SELF_CONTROL = "lost_self_control"
    JUNK_FOOD = "junk_food"
    OUTSIDE_FOOD = "outside_food"
    LATE_EATING = "late_eating"
    SCREEN_TIME = "screen_time"
    OTHER = "other"


class HabitEntry(BaseModel):
    """A habit event to track."""

    date: dt_date
    datetime_logged: dt_datetime | None = None
    category: HabitCategory
    description: str = Field(
        description="What happened, e.g. ate ice cream, ordered Deliveroo, watched Netflix till 2am"
    )
    notes: str | None = None
