from typing import Literal
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.api.dependencies import get_current_user
from app.db.database import get_db
from app.models import User
from app.schemas import (
    CustomerCreate,
    CustomerUpdate,
    CustomerResponse,
    CustomerListResponse,
)
from app.services.customer_service import (
    create_customer,
    get_customer_by_id,
    update_customer,
    delete_customer,
    get_customers,
)
from app.utils.response import global_response_format


router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_customer_endpoint(
    customer_data: CustomerCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        customer = create_customer(
            db=db,
            customer_data=customer_data,
        )

        customer_response = CustomerResponse.model_validate(customer)

        return global_response_format(
            status_value=True,
            data=customer_response.model_dump(mode="json"),
            status_code=status.HTTP_201_CREATED,
            status_message="Customer created successfully",
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    except RuntimeError:
        return global_response_format(
            status_value=False,
            data={},
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            status_message="Customer creation failed",
        )


@router.get("/")
def list_customers_endpoint(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    search: str | None = Query(default=None, max_length=100),
    status_filter: Literal["Active", "Inactive"] | None = Query(
        default=None,
        alias="status",
    ),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        result = get_customers(
            db=db,
            page=page,
            limit=limit,
            search=search,
            status=status_filter,
        )

        customers_response = CustomerListResponse.model_validate(result)

        return global_response_format(
            status_value=True,
            data=customers_response.model_dump(mode="json"),
            status_code=status.HTTP_200_OK,
            status_message="Customers retrieved successfully",
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    except RuntimeError:
        return global_response_format(
            status_value=False,
            data={},
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            status_message="Failed to retrieve customers",
        )


@router.get("/{customer_id}")
def get_customer_endpoint(
    customer_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        customer = get_customer_by_id(
            db=db,
            customer_id=customer_id,
        )

        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found",
            )

        customer_response = CustomerResponse.model_validate(customer)

        return global_response_format(
            status_value=True,
            data=customer_response.model_dump(mode="json"),
            status_code=status.HTTP_200_OK,
            status_message="Customer retrieved successfully",
        )

    except RuntimeError:
        return global_response_format(
            status_value=False,
            data={},
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            status_message="Failed to retrieve customer",
        )


@router.patch("/{customer_id}")
def update_customer_endpoint(
    customer_id: int,
    customer_data: CustomerUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        customer = update_customer(
            db=db,
            customer_id=customer_id,
            customer_data=customer_data,
        )

        customer_response = CustomerResponse.model_validate(customer)

        return global_response_format(
            status_value=True,
            data=customer_response.model_dump(mode="json"),
            status_code=status.HTTP_200_OK,
            status_message="Customer updated successfully",
        )

    except ValueError as exc:
        error_message = str(exc)

        error_status = (
            status.HTTP_409_CONFLICT
            if error_message == "Customer email already exists"
            else status.HTTP_404_NOT_FOUND
            if error_message == "Customer not found"
            else status.HTTP_400_BAD_REQUEST
        )

        raise HTTPException(
            status_code=error_status,
            detail=error_message,
        ) from exc

    except RuntimeError:
        return global_response_format(
            status_value=False,
            data={},
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            status_message="Customer update failed",
        )


@router.delete("/{customer_id}")
def delete_customer_endpoint(
    customer_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        delete_customer(
            db=db,
            customer_id=customer_id,
        )

        return global_response_format(
            status_value=True,
            data={},
            status_code=status.HTTP_200_OK,
            status_message="Customer deactivated successfully",
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    except RuntimeError:
        return global_response_format(
            status_value=False,
            data={},
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            status_message="Customer deactivation failed",
        )
