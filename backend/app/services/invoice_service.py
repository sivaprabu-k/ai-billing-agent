from decimal import Decimal, ROUND_HALF_UP
from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy.exc import SQLAlchemyError
from app.models import(
    Invoice,
    InvoiceItem,
    Customer,
)  
from uuid import uuid4
from app.schemas import(
    InvoiceCreate,
    InvoiceUpdate,
    InvoiceItemUpdate
) 
from app.utils.query_helpers import (
    apply_search,
    apply_filters,
    paginate_query,
)


TWO_DECIMAL_PLACES = Decimal("0.01")


def round_money(amount: Decimal) -> Decimal:
    """Round a monetary amount to two decimal places."""
    return amount.quantize(
        TWO_DECIMAL_PLACES,
        rounding=ROUND_HALF_UP,
    )


def calculate_invoice_item(
    quantity: Decimal,
    unit_price: Decimal,
    tax_rate: Decimal,
) -> dict:
    """Calculate an invoice item's subtotal, tax, and total."""

    line_subtotal = round_money(quantity * unit_price)

    tax_amount = round_money(
        line_subtotal * tax_rate / Decimal("100")
    )

    line_total = round_money(line_subtotal + tax_amount)

    return {
        "line_subtotal": line_subtotal,
        "tax_amount": tax_amount,
        "line_total": line_total,
    }


def calculate_invoice_totals(
    items: list[dict],
) -> dict:
    """Calculate invoice-level subtotal, tax, and total."""

    subtotal = sum(
        (item["line_subtotal"] for item in items),
        Decimal("0.00"),
    )

    tax_amount = sum(
        (item["tax_amount"] for item in items),
        Decimal("0.00"),
    )

    total_amount = subtotal + tax_amount

    return {
        "subtotal": round_money(subtotal),
        "tax_amount": round_money(tax_amount),
        "total_amount": round_money(total_amount),
    }


def create_invoice(
    db: Session,
    invoice_data: InvoiceCreate,
) -> Invoice:

    try:
        customer = (
            db.query(Customer)
            .filter(Customer.id == invoice_data.customer_id)
            .first()
        )

        if not customer:
            raise ValueError("Customer not found")

        if customer.status != "Active":
            raise ValueError("Cannot create invoice for an inactive customer")

        invoice_number = (
            f"INV-{invoice_data.invoice_date.year}-"
            f"{uuid4().hex[:8].upper()}"
        )

        new_invoice = Invoice(
            customer_id=invoice_data.customer_id,
            invoice_number=invoice_number,
            invoice_date=invoice_data.invoice_date,
            due_date=invoice_data.due_date,
            notes=invoice_data.notes,
            status="Draft",
        )

        item_calculations = []

        for item_data in invoice_data.items:

            calculations = calculate_invoice_item(
                quantity=item_data.quantity,
                unit_price=item_data.unit_price,
                tax_rate=item_data.tax_rate,
            )

            item_calculations.append(calculations)

            new_item = InvoiceItem(
                description=item_data.description,
                quantity=item_data.quantity,
                unit_price=item_data.unit_price,
                tax_rate=item_data.tax_rate,
                **calculations,
            )

            new_invoice.items.append(new_item)

        totals = calculate_invoice_totals(item_calculations)

        new_invoice.subtotal = totals["subtotal"]
        new_invoice.tax_amount = totals["tax_amount"]
        new_invoice.total_amount = totals["total_amount"]

        db.add(new_invoice)
        db.commit()
        db.refresh(new_invoice)

        return new_invoice

    except ValueError:
        db.rollback()
        raise

    except SQLAlchemyError as exc:
        db.rollback()
        raise RuntimeError("Invoice creation failed") from exc


def get_invoice_by_id(
    db: Session,
    invoice_id: int,
) -> Invoice | None:

    try:
        invoice = (
            db.query(Invoice)
            .options(
                joinedload(Invoice.customer),
                selectinload(Invoice.items),
            )
            .filter(Invoice.id == invoice_id)
            .first()
        )

        return invoice

    except SQLAlchemyError as exc:
        raise RuntimeError("Failed to retrieve invoice") from exc


def get_invoices(
    db: Session,
    page: int = 1,
    limit: int = 10,
    search: str | None = None,
    status: str | None = None,
) -> dict:

    try:
        allowed_statuses = (
            "Draft",
            "Issued",
            "Paid",
            "Partially Paid",
            "Overdue",
            "Cancelled",
        )

        if status and status not in allowed_statuses:
            raise ValueError("Invalid invoice status")

        query = (
            db.query(Invoice)
            .options(
                joinedload(Invoice.customer),
                selectinload(Invoice.items),
            )
        )

        if search and search.strip():
            query = query.join(Invoice.customer)

        query = apply_search(
            query=query,
            search=search,
            search_fields=[
                Invoice.invoice_number,
                Customer.name,
            ],
        )

        query = apply_filters(
            query=query,
            filters={
                Invoice.status: status,
            },
        )

        return paginate_query(
            query=query,
            page=page,
            limit=limit,
            order_by=Invoice.id.desc(),
        )

    except ValueError:
        raise

    except SQLAlchemyError as exc:
        raise RuntimeError(
            "Failed to retrieve invoices"
        ) from exc


def update_invoice(
    db: Session,
    invoice_id: int,
    invoice_data: InvoiceUpdate,
) -> Invoice:

    try:
        invoice = (
            db.query(Invoice)
            .filter(Invoice.id == invoice_id)
            .first()
        )

        if not invoice:
            raise ValueError("Invoice not found")

        if invoice.status != "Draft":
            raise ValueError("Only Draft invoices can be updated")

        update_data = invoice_data.model_dump(
            exclude_unset=True,
        )

        if not update_data:
            raise ValueError("No valid fields provided for update")

        if (
            "due_date" in update_data
            and update_data["due_date"] is not None
            and update_data["due_date"] < invoice.invoice_date
        ):
            raise ValueError(
                "Due date cannot be earlier than invoice date"
            )

        for field, value in update_data.items():
            setattr(invoice, field, value)

        db.commit()
        db.refresh(invoice)

        return invoice

    except ValueError:
        db.rollback()
        raise

    except SQLAlchemyError as exc:
        db.rollback()
        raise RuntimeError("Invoice update failed") from exc


def update_invoice_item(
    db: Session,
    invoice_id: int,
    item_id: int,
    item_data: InvoiceItemUpdate,
) -> Invoice:

    try:
        invoice = (
            db.query(Invoice)
            .filter(Invoice.id == invoice_id)
            .first()
        )

        if not invoice:
            raise ValueError("Invoice not found")

        if invoice.status != "Draft":
            raise ValueError(
                "Only Draft invoices can be updated"
            )

        invoice_item = (
            db.query(InvoiceItem)
            .filter(
                InvoiceItem.id == item_id,
                InvoiceItem.invoice_id == invoice_id,
            )
            .first()
        )

        if not invoice_item:
            raise ValueError("Invoice item not found")

        update_data = item_data.model_dump(
            exclude_unset=True,
        )

        if not update_data:
            raise ValueError(
                "No valid fields provided for update"
            )

        if any(value is None for value in update_data.values()):
            raise ValueError(
                "Invoice item fields cannot be null"
            )

        for field, value in update_data.items():
            setattr(invoice_item, field, value)

        calculations = calculate_invoice_item(
            quantity=invoice_item.quantity,
            unit_price=invoice_item.unit_price,
            tax_rate=invoice_item.tax_rate,
        )

        invoice_item.line_subtotal = calculations["line_subtotal"]
        invoice_item.tax_amount = calculations["tax_amount"]
        invoice_item.line_total = calculations["line_total"]

        item_calculations = [
            {
                "line_subtotal": item.line_subtotal,
                "tax_amount": item.tax_amount,
                "line_total": item.line_total,
            }
            for item in invoice.items
        ]

        totals = calculate_invoice_totals(item_calculations)

        invoice.subtotal = totals["subtotal"]
        invoice.tax_amount = totals["tax_amount"]
        invoice.total_amount = totals["total_amount"]

        db.commit()
        db.refresh(invoice)

        return invoice

    except ValueError:
        db.rollback()
        raise

    except SQLAlchemyError as exc:
        db.rollback()
        raise RuntimeError(
            "Invoice item update failed"
        ) from exc


def delete_invoice(
    db: Session,
    invoice_id: int,
) -> Invoice:

    try:
        invoice = (
            db.query(Invoice)
            .filter(Invoice.id == invoice_id)
            .first()
        )

        if not invoice:
            raise ValueError("Invoice not found")

        if invoice.status != "Draft":
            raise ValueError(
                "Only Draft invoices can be deleted"
            )

        db.delete(invoice)
        db.commit()

        return invoice

    except ValueError:
        db.rollback()
        raise

    except SQLAlchemyError as exc:
        db.rollback()
        raise RuntimeError("Invoice deletion failed") from exc
