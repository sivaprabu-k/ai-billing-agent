from uuid import uuid4
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.models import Customer
from app.schemas import CustomerCreate, CustomerUpdate
from app.utils.query_helpers import (
    apply_search,
    apply_filters,
    paginate_query,
)


def create_customer(
    db: Session,
    customer_data: CustomerCreate,
) -> Customer:

    try:
        email = str(customer_data.email).lower()

        existing_customer = (
            db.query(Customer)
            .filter(func.lower(Customer.email) == email)
            .first()
        )

        if existing_customer:
            raise ValueError("Customer email already exists")

        new_customer = Customer(
            customer_code=f"T{uuid4().hex[:19]}",
            name=customer_data.name,
            email=email,
            plan=customer_data.plan,
        )

        db.add(new_customer)
        db.flush()

        new_customer.customer_code = (
            f"CUS-{new_customer.id + 1000:04d}"
        )

        db.commit()
        db.refresh(new_customer)

        return new_customer

    except ValueError:
        raise

    except SQLAlchemyError as exc:
        db.rollback()
        raise RuntimeError("Customer creation failed") from exc


def get_customer_by_id(
    db: Session,
    customer_id: int,
) -> Customer | None:

    try:
        return (
            db.query(Customer)
            .filter(Customer.id == customer_id)
            .first()
        )

    except SQLAlchemyError as exc:
        raise RuntimeError("Failed to retrieve customer") from exc


def update_customer(
    db: Session,
    customer_id: int,
    customer_data: CustomerUpdate,
) -> Customer:

    try:
        customer = (
            db.query(Customer)
            .filter(Customer.id == customer_id)
            .first()
        )

        if not customer:
            raise ValueError("Customer not found")

        update_data = customer_data.model_dump(
            exclude_unset=True,
            exclude_none=True,
        )

        if not update_data:
            raise ValueError("No valid fields provided for update")

        if "email" in update_data:
            email = str(update_data["email"]).lower()

            existing_customer = (
                db.query(Customer)
                .filter(
                    func.lower(Customer.email) == email,
                    Customer.id != customer_id,
                )
                .first()
            )

            if existing_customer:
                raise ValueError("Customer email already exists")

            update_data["email"] = email

        for field, value in update_data.items():
            setattr(customer, field, value)

        db.commit()
        db.refresh(customer)

        return customer

    except ValueError:
        raise

    except SQLAlchemyError as exc:
        db.rollback()
        raise RuntimeError("Customer update failed") from exc


def delete_customer(
    db: Session,
    customer_id: int,
) -> Customer:

    try:
        customer = (
            db.query(Customer)
            .filter(Customer.id == customer_id)
            .first()
        )

        if not customer:
            raise ValueError("Customer not found")

        customer.status = "Inactive"

        db.commit()
        db.refresh(customer)

        return customer

    except ValueError:
        raise

    except SQLAlchemyError as exc:
        db.rollback()
        raise RuntimeError("Customer deletion failed") from exc



def get_customers(
    db: Session,
    page: int = 1,
    limit: int = 10,
    search: str | None = None,
    status: str | None = None,
) -> dict:

    try:
        if status and status not in ("Active", "Inactive"):
            raise ValueError("Invalid customer status")

        query = db.query(Customer)

        query = apply_search(
            query=query,
            search=search,
            search_fields=[
                Customer.name,
                Customer.email,
                Customer.customer_code,
            ],
        )

        query = apply_filters(
            query=query,
            filters={
                Customer.status: status,
            },
        )

        return paginate_query(
            query=query,
            page=page,
            limit=limit,
            order_by=Customer.id.desc(),
        )

    except ValueError:
        raise

    except SQLAlchemyError as exc:
        db.rollback()
        raise RuntimeError("Failed to retrieve customers") from exc

