from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models import User
from app.schemas import UserCreate, UserUpdate
from app.utils.security import hash_password


def create_user(
    db: Session,
    user_data: UserCreate,
) -> User:

    try:
        existing_user = (
            db.query(User)
            .filter(User.email == str(user_data.email))
            .first()
        )

        if existing_user:
            raise ValueError("Email is already registered")

        new_user = User(
            name=user_data.name,
            email=str(user_data.email),
            hashed_password=hash_password(user_data.password),
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

    except ValueError:
        raise

    except SQLAlchemyError as exc:
        db.rollback()
        raise RuntimeError("User registration failed") from exc


def update_user(
    db: Session,
    user_id: int,
    user_data: UserUpdate,
) -> User:

    try:
        user = (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

        if not user:
            raise ValueError("User not found")

        update_data = user_data.model_dump(
            exclude_unset=True,
            exclude_none=True,
        )

        if not update_data:
            raise ValueError("No valid fields provided for update")

        if "email" in update_data:
            update_data["email"] = str(update_data["email"])

            existing_user = (
                db.query(User)
                .filter(
                    User.email == update_data["email"],
                    User.id != user_id,
                )
                .first()
            )

            if existing_user:
                raise ValueError("Email is already registered")

        for field, value in update_data.items():
            setattr(user, field, value)

        db.commit()
        db.refresh(user)

        return user

    except ValueError:
        raise

    except SQLAlchemyError as exc:
        db.rollback()
        raise RuntimeError("User update failed") from exc


def get_user_by_id(
    db: Session,
    user_id: int,
) -> User | None:

    try:
        return (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    except SQLAlchemyError as exc:
        raise RuntimeError("Failed to retrieve user") from exc


def get_user_by_email(
    db: Session,
    email: str,
) -> User | None:

    try:
        return (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

    except SQLAlchemyError as exc:
        raise RuntimeError("Failed to retrieve user") from exc


def delete_user(
    db: Session,
    user_id: int,
) -> User:

    try:
        user = (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

        if not user:
            raise ValueError("User not found")

        user.is_active = False

        db.commit()
        db.refresh(user)

        return user

    except ValueError:
        raise

    except SQLAlchemyError as exc:
        db.rollback()
        raise RuntimeError("User deletion failed") from exc
