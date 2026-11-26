from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models import Role


def get_all_roles(db: Session) -> list[Role]:
    try:
        return (
            db.query(Role)
            .order_by(Role.id.asc())
            .all()
        )
    except SQLAlchemyError as exc:
        raise RuntimeError("Failed to retrieve roles") from exc


def get_role_by_id(db: Session, role_id: int) -> Role | None:
    try:
        return (
            db.query(Role)
            .filter(Role.id == role_id)
            .first()
        )
    except SQLAlchemyError as exc:
        raise RuntimeError("Failed to retrieve role") from exc
