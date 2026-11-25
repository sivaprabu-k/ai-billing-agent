from decimal import Decimal
from typing import Literal
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class CustomerCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    plan: str = Field(min_length=2, max_length=50)

    model_config = {"extra": "forbid"}


class CustomerUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )
    email: EmailStr | None = None
    plan: str | None = Field(
        default=None,
        min_length=2,
        max_length=50,
    )
    status: Literal["Active", "Inactive"] | None = None

    model_config = {"extra": "forbid"}


class CustomerResponse(BaseModel):
    id: int
    customer_code: str
    name: str
    email: EmailStr
    plan: str
    total_spent: Decimal
    status: Literal["Active", "Inactive"]
    created_at: datetime

    model_config = {"from_attributes": True}


class CustomerPagination(BaseModel):
    page: int
    limit: int
    total_items: int
    total_pages: int
    has_next: bool
    has_previous: bool


class CustomerListResponse(BaseModel):
    items: list[CustomerResponse]
    pagination: CustomerPagination
