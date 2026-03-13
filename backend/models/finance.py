"""New Pydantic schemas for MemoriaOS UI Navigator track: Finance."""

from __future__ import annotations

import enum
from datetime import date as dt_date
from decimal import Decimal

from pydantic import BaseModel, Field


class ExpenseCategory(enum.StrEnum):
    """Categories for expense classification."""

    TRANSPORT = "transport"
    FOOD = "food"
    GROCERIES = "groceries"
    ENTERTAINMENT = "entertainment"
    SHOPPING = "shopping"
    BILLS = "bills"
    HEALTH = "health"
    SUBSCRIPTION = "subscription"
    OTHER = "other"


class ExpenseRecord(BaseModel):
    """Financial transaction extracted from a receipt or bank screenshot."""

    vendor: str
    amount: Decimal = Field(description="Transaction amount, e.g. 14.50")
    currency: str = Field(default="GBP", description="ISO 4217 currency code")
    date: dt_date
    category: ExpenseCategory = Field(default=ExpenseCategory.OTHER)
    payment_method: str | None = Field(
        default=None, description="e.g. 'Visa ending 4242', 'Apple Pay'"
    )
    reference: str | None = None
    notes: str | None = None
