from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


class InvoiceItemCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    description: str = Field(
        min_length=1,
        max_length=255,
    )

    quantity: Decimal = Field(
        gt=0,
        max_digits=10,
        decimal_places=2,
    )

    unit_price: Decimal = Field(
        ge=0,
        max_digits=12,
        decimal_places=2,
    )

    tax_rate: Decimal = Field(
        default=Decimal("0.00"),
        ge=0,
        le=100,
        max_digits=5,
        decimal_places=2,
    )


class InvoiceItemUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    description: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )

    quantity: Decimal | None = Field(
        default=None,
        gt=0,
        max_digits=10,
        decimal_places=2,
    )

    unit_price: Decimal | None = Field(
        default=None,
        ge=0,
        max_digits=12,
        decimal_places=2,
    )

    tax_rate: Decimal | None = Field(
        default=None,
        ge=0,
        le=100,
        max_digits=5,
        decimal_places=2,
    )


class InvoiceItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    invoice_id: int
    description: str
    quantity: Decimal
    unit_price: Decimal
    tax_rate: Decimal
    line_subtotal: Decimal
    tax_amount: Decimal
    line_total: Decimal
