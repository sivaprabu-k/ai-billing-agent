from datetime import datetime, timezone
from uuid import UUID
import jwt
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models import User, UserSession
from app.schemas import (
    LoginRequest,
    PasswordChangeRequest,
)
from app.utils.security import (
    verify_password,
    hash_password,
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    hash_refresh_token,
)
from datetime import timedelta
from uuid import uuid4

from app.config import settings


def login_user(
    db: Session,
    login_data: LoginRequest,
) -> tuple[User, str, str]:
    try:
        user = (
            db.query(User)
            .filter(User.email == str(login_data.email))
            .first()
        )

        if not user or not verify_password(
            login_data.password,
            user.hashed_password,
        ):
            raise ValueError("Invalid email or password")

        if not user.is_active:
            raise ValueError("User account is inactive")

        session_id = str(uuid4())

        access_token = create_access_token(
            subject=str(user.id),
            session_id=session_id,
        )

        refresh_token = create_refresh_token(
            subject=str(user.id),
            session_id=session_id,
        )

        refresh_token_expires_at = datetime.now(
            timezone.utc
        ) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

        user_session = UserSession(
            id=UUID(session_id),
            user_id=user.id,
            refresh_token_hash=hash_refresh_token(refresh_token),
            expires_at=refresh_token_expires_at,
        )

        db.add(user_session)
        db.commit()

        return user, access_token, refresh_token

    except ValueError:
        raise
    except SQLAlchemyError as exc:
        db.rollback()
        raise RuntimeError("User login failed") from exc


def refresh_access_token(
    db: Session,
    refresh_token: str,
) -> str:
    try:
        payload = decode_refresh_token(refresh_token)

        user_id = int(payload["sub"])
        session_id = UUID(payload["sid"])

        user_session = (
            db.query(UserSession)
            .filter(
                UserSession.id == session_id,
                UserSession.user_id == user_id,
            )
            .with_for_update()
            .first()
        )

        if not user_session:
            raise ValueError("Invalid refresh session")

        if user_session.revoked_at is not None:
            raise ValueError("Refresh session has been revoked")

        if user_session.expires_at <= datetime.now(timezone.utc):
            raise ValueError("Refresh session has expired")

        if user_session.refresh_token_hash != hash_refresh_token(
            refresh_token
        ):
            raise ValueError("Invalid refresh token")

        user = db.query(User).filter(User.id == user_id).first()

        if not user or not user.is_active:
            raise ValueError("User account is unavailable")

        return create_access_token(
            subject=str(user.id),
            session_id=str(user_session.id),
        )

    except (ValueError, jwt.InvalidTokenError, KeyError, TypeError) as exc:
        raise ValueError("Invalid or expired refresh token") from exc
    except SQLAlchemyError as exc:
        db.rollback()
        raise RuntimeError("Access token refresh failed") from exc


def logout_user(
    db: Session,
    session_id: UUID,
    user_id: int,
) -> None:
    try:
        user_session = (
            db.query(UserSession)
            .filter(
                UserSession.id == session_id,
                UserSession.user_id == user_id,
            )
            .first()
        )

        if not user_session:
            raise ValueError("Session not found")

        if user_session.revoked_at is None:
            user_session.revoked_at = datetime.now(timezone.utc)
            db.commit()

    except ValueError:
        raise
    except SQLAlchemyError as exc:
        db.rollback()
        raise RuntimeError("User logout failed") from exc


def change_user_password(
    db: Session,
    user_id: int,
    password_data: PasswordChangeRequest,
) -> None:
    try:
        user = (
            db.query(User)
            .filter(User.id == user_id)
            .with_for_update()
            .first()
        )

        if not user:
            raise ValueError("User not found")

        if not verify_password(
            password_data.current_password,
            user.hashed_password,
        ):
            raise ValueError("Current password is incorrect")   

        if password_data.current_password == password_data.new_password:
            raise ValueError("New password must be different")

        user.hashed_password = hash_password(
            password_data.new_password
        )

        active_sessions = (
            db.query(UserSession)
            .filter(
                UserSession.user_id == user_id,
                UserSession.revoked_at.is_(None),
            )
            .all()
        )

        revoked_at = datetime.now(timezone.utc)

        for session in active_sessions:
            session.revoked_at = revoked_at

        db.commit()

        db.commit()

    except ValueError:
        raise
    except SQLAlchemyError as exc:
        db.rollback()
        raise RuntimeError("Password change failed") from exc