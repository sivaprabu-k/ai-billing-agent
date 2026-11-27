from typing import Literal
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.api.dependencies import require_role
from app.db.database import get_db
from app.models import User
from app.schemas import (
    InvoiceCreate,
    InvoiceResponse,
    InvoiceUpdate,
    InvoiceItemUpdate,
)
from app.services.invoice_service import (
    create_invoice,
    get_invoices,
    get_invoice_by_id,
    update_invoice,
    update_invoice_item,
    delete_invoice,
)
from app.utils.response import global_response_format


router = APIRouter(
    prefix="/invoices",
    tags=["Invoices"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_invoice_endpoint(
    invoice_data: InvoiceCreate,
    current_user: User = Depends(
        require_role("Admin", "Billing Staff")
    ),
    db: Session = Depends(get_db),
):
    try:
        invoice = create_invoice(
            db=db,
            invoice_data=invoice_data,
        )

        invoice_response = InvoiceResponse.model_validate(invoice)

        return global_response_format(
            status_value=True,
            data=invoice_response.model_dump(mode="json"),
            status_code=status.HTTP_201_CREATED,
            status_message="Invoice created successfully",
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
            status_message="Invoice creation failed",
        )


@router.get("/")
def get_invoices_endpoint(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    search: str | None = Query(default=None),
    invoice_status: Literal[
        "Draft",
        "Issued",
        "Paid",
        "Partially Paid",
        "Overdue",
        "Cancelled",
    ] | None = Query(
        default=None,
        alias="status",
    ),
    current_user: User = Depends(
        require_role("Admin", "Billing Staff", "Support Staff")
    ),
    db: Session = Depends(get_db),
):
    try:
        result = get_invoices(
            db=db,
            page=page,
            limit=limit,
            search=search,
            status=invoice_status,
        )

        invoice_responses = [
            InvoiceResponse.model_validate(invoice).model_dump(mode="json")
            for invoice in result["items"]
        ]

        return global_response_format(
            status_value=True,
            data={
                "items": invoice_responses,
                "pagination": result["pagination"],
            },
            status_code=status.HTTP_200_OK,
            status_message="Invoices retrieved successfully",
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
            status_message="Failed to retrieve invoices",
        )


@router.get("/{invoice_id}")
def get_invoice_by_id_endpoint(
    invoice_id: int,
    current_user: User = Depends(
        require_role("Admin", "Billing Staff", "Support Staff")
    ),
    db: Session = Depends(get_db),
):
    try:
        invoice = get_invoice_by_id(
            db=db,
            invoice_id=invoice_id,
        )

        invoice_response = InvoiceResponse.model_validate(invoice)

        return global_response_format(
            status_value=True,
            data=invoice_response.model_dump(mode="json"),
            status_code=status.HTTP_200_OK,
            status_message="Invoice retrieved successfully",
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
            status_message="Failed to retrieve invoice",
        )


@router.patch("/{invoice_id}")
def update_invoice_endpoint(
    invoice_id: int,
    invoice_data: InvoiceUpdate,
    current_user: User = Depends(
        require_role("Admin", "Billing Staff")
    ),
    db: Session = Depends(get_db),
):
    try:
        invoice = update_invoice(
            db=db,
            invoice_id=invoice_id,
            invoice_data=invoice_data,
        )

        invoice_response = InvoiceResponse.model_validate(invoice)

        return global_response_format(
            status_value=True,
            data=invoice_response.model_dump(mode="json"),
            status_code=status.HTTP_200_OK,
            status_message="Invoice updated successfully",
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
            status_message="Invoice update failed",
        )


@router.patch("/{invoice_id}/items/{item_id}")
def update_invoice_item_endpoint(
    invoice_id: int,
    item_id: int,
    item_data: InvoiceItemUpdate,
    current_user: User = Depends(
        require_role("Admin", "Billing Staff")
    ),
    db: Session = Depends(get_db),
):
    try:
        invoice = update_invoice_item(
            db=db,
            invoice_id=invoice_id,
            item_id=item_id,
            item_data=item_data,
        )

        invoice_response = InvoiceResponse.model_validate(invoice)

        return global_response_format(
            status_value=True,
            data=invoice_response.model_dump(mode="json"),
            status_code=status.HTTP_200_OK,
            status_message="Invoice item updated successfully",
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
            status_message="Invoice item update failed",
        )


@router.delete("/{invoice_id}")
def delete_invoice_endpoint(
    invoice_id: int,
    current_user: User = Depends(
        require_role("Admin")
    ),
    db: Session = Depends(get_db),
):
    try:
        delete_invoice(
            db=db,
            invoice_id=invoice_id,
        )

        return global_response_format(
            status_value=True,
            data={
                "invoice_id": invoice_id,
            },
            status_code=status.HTTP_200_OK,
            status_message="Invoice deleted successfully",
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
            status_message="Invoice deletion failed",
        )
