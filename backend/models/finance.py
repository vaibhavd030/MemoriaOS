"""New Pydantic schemas for MemoriaOS UI Navigator track: Finance."""

from __future__ import annotations

import enum
from datetime import date as dt_date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


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
    """Financial transaction extracted from a receipt or bank screenshot.

    Attributes:
        vendor (str): Name of the vendor/merchant.
        amount (Decimal): Transaction amount.
        currency (str): ISO 4217 currency code.
        date (dt_date): Date of transaction.
        category (ExpenseCategory): Classification of the expense.
        payment_method (str | None): How the item was paid for.
        reference (str | None): Transaction reference or ID.
        notes (str | None): Additional comments.
    """

    model_config = ConfigDict(slots=True)

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
