from datetime import datetime, timezone
from uuid import UUID

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models import User, UserSession
from app.utils.security import decode_access_token


bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:

    unauthorized_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if credentials is None:
        raise unauthorized_error

    try:
        payload = decode_access_token(credentials.credentials)

        user_id = int(payload["sub"])
        session_id = UUID(payload["sid"])

    except (
        jwt.InvalidTokenError,
        ValueError,
        KeyError,
        TypeError,
    ):
        raise unauthorized_error

    user_session = (
        db.query(UserSession)
        .filter(
            UserSession.id == session_id,
            UserSession.user_id == user_id,
        )
        .first()
    )

    if not user_session:
        raise unauthorized_error

    if user_session.revoked_at is not None:
        raise unauthorized_error

    if user_session.expires_at <= datetime.now(timezone.utc):
        raise unauthorized_error

    user = db.query(User).filter(User.id == user_id).first()

    if not user or not user.is_active:
        raise unauthorized_error

    return user