from datetime import date
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field, model_validator
from app.schemas.invoice_item import (
    InvoiceItemCreate,
    InvoiceItemResponse,
)


class InvoiceCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    customer_id: int = Field(gt=0)

    invoice_date: date

    due_date: date | None = None

    notes: str | None = None

    items: list[InvoiceItemCreate] = Field(
        min_length=1,
    )

    @model_validator(mode="after")
    def validate_due_date(self):
        if self.due_date and self.due_date < self.invoice_date:
            raise ValueError(
                "Due date cannot be earlier than invoice date"
            )

        return self


class InvoiceUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    due_date: date | None = None

    notes: str | None = None


class InvoiceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_id: int
    invoice_number: str
    invoice_date: date
    due_date: date | None
    subtotal: Decimal
    tax_amount: Decimal
    total_amount: Decimal
    status: str
    notes: str | None
    items: list[InvoiceItemResponse]
