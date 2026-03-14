"""New Pydantic schemas for MemoriaOS UI Navigator track: Recipes."""

from __future__ import annotations

from pydantic import BaseModel, Field


class Ingredient(BaseModel):
    """A single ingredient with quantity and unit.

    Attributes:
        name (str): Ingredient name.
        quantity (str | None): Amount/quantity.
        notes (str | None): Preparation notes.
    """

    name: str = Field(description="Ingredient name, e.g. 'chicken breast'")
    quantity: str | None = Field(
        default=None, description="Amount, e.g. '200g', '2 cups', '1 tbsp'"
    )
    notes: str | None = Field(
        default=None, description="Preparation notes, e.g. 'diced', 'room temperature'"
    )


class RecipeCard(BaseModel):
    """Recipe extracted from a screenshot or video frame.

    Attributes:
        title (str): Name of the recipe.
        description (str | None): Short description or origin.
        prep_time_minutes (int | None): Time to prepare.
        cook_time_minutes (int | None): Time to cook.
        servings (int | None): Number of servings.
        ingredients (list[Ingredient]): List of components.
        steps (list[str]): Step-by-step instructions.
        tags (list[str]): Metadata tags.
        source_url (str | None): Original source link.
    """

    title: str
    description: str | None = None
    prep_time_minutes: int | None = Field(default=None, ge=0)
    cook_time_minutes: int | None = Field(default=None, ge=0)
    servings: int | None = Field(default=None, ge=1)
    ingredients: list[Ingredient] = Field(default_factory=list)
    steps: list[str] = Field(default_factory=list)
    tags: list[str] = Field(
        default_factory=list,
        description="e.g. 'high-protein', 'vegetarian', 'quick', 'pasta'",
    )
    source_url: str | None = None
