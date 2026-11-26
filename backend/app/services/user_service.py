from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from app.models import User, Role
from app.schemas import AdminUserCreate, UserUpdate, AdminUserUpdate
from app.utils.security import hash_password


def create_user(
    db: Session,
    user_data: AdminUserCreate,
) -> User:

    try:
        email = str(user_data.email).lower()

        existing_user = (
            db.query(User)
            .filter(func.lower(User.email) == email)
            .first()
        )

        if existing_user:
            raise ValueError("Email is already registered")

        role = (
            db.query(Role)
            .filter(Role.id == user_data.role_id)
            .first()
        )

        if not role:
            raise ValueError("Invalid role ID")

        new_user = User(
            name=user_data.name,
            email=email,
            hashed_password=hash_password(user_data.password),
            role_id=role.id,
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

    except ValueError:
        raise

    except SQLAlchemyError as exc:
        db.rollback()
        raise RuntimeError("User creation failed") from exc


def get_all_users(
    db: Session,
) -> list[User]:

    try:
        return (
            db.query(User)
            .order_by(User.id.asc())
            .all()
        )

    except SQLAlchemyError as exc:
        raise RuntimeError("Failed to retrieve users") from exc


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


def admin_update_user(
    db: Session,
    user_id: int,
    user_data: AdminUserUpdate,
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
            email = str(update_data["email"]).lower()

            existing_user = (
                db.query(User)
                .filter(
                    func.lower(User.email) == email,
                    User.id != user_id,
                )
                .first()
            )

            if existing_user:
                raise ValueError("Email is already registered")

            update_data["email"] = email

        if "role_id" in update_data:
            role = (
                db.query(Role)
                .filter(Role.id == update_data["role_id"])
                .first()
            )

            if not role:
                raise ValueError("Invalid role ID")

        current_role = (
            db.query(Role)
            .filter(Role.id == user.role_id)
            .first()
        )

        is_demoting_admin = (
            current_role
            and current_role.name == "Admin"
            and "role_id" in update_data
            and role.name != "Admin"
        )

        is_deactivating_admin = (
            current_role
            and current_role.name == "Admin"
            and user.is_active
            and update_data.get("is_active") is False
        )

        if user.is_active and (is_demoting_admin or is_deactivating_admin):
            active_admin_count = (
                db.query(func.count(User.id))
                .join(Role, User.role_id == Role.id)
                .filter(
                    Role.name == "Admin",
                    User.is_active.is_(True),
                )
                .scalar()
            )

            if active_admin_count <= 1:
                raise ValueError(
                    "Cannot deactivate or demote the last active Admin"
                )

        for field, value in update_data.items():
            setattr(user, field, value)

        db.commit()
        db.refresh(user)

        return user

    except ValueError:
        raise

    except SQLAlchemyError as exc:
        db.rollback()
        raise RuntimeError("Admin user update failed") from exc


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

        if not user.is_active:
            raise ValueError("User is already deactivated")

        role = (
            db.query(Role)
            .filter(Role.id == user.role_id)
            .first()
        )

        if role and role.name == "Admin":
            active_admin_count = (
                db.query(func.count(User.id))
                .join(Role, User.role_id == Role.id)
                .filter(
                    Role.name == "Admin",
                    User.is_active.is_(True),
                )
                .scalar()
            )

            if active_admin_count <= 1:
                raise ValueError(
                    "Cannot deactivate the last active Admin"
                )

        user.is_active = False

        db.commit()
        db.refresh(user)

        return user

    except ValueError:
        raise

    except SQLAlchemyError as exc:
        db.rollback()
        raise RuntimeError("User deletion failed") from exc


def admin_deactivate_user(
    db: Session,
    user_id: int,
    current_admin_id: int,
) -> User:

    try:
        user = (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

        if not user:
            raise ValueError("User not found")

        if user_id == current_admin_id:
            raise ValueError("Admin cannot deactivate their own account")

        if not user.is_active:
            raise ValueError("User is already deactivated")

        role = (
            db.query(Role)
            .filter(Role.id == user.role_id)
            .first()
        )

        if role and role.name == "Admin":
            active_admin_count = (
                db.query(func.count(User.id))
                .join(Role, User.role_id == Role.id)
                .filter(
                    Role.name == "Admin",
                    User.is_active.is_(True),
                )
                .scalar()
            )

            if active_admin_count <= 1:
                raise ValueError(
                    "Cannot deactivate the last active Admin"
                )

        user.is_active = False

        db.commit()
        db.refresh(user)

        return user

    except ValueError:
        raise

    except SQLAlchemyError as exc:
        db.rollback()
        raise RuntimeError("Admin user deactivation failed") from exc

