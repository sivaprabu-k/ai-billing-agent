from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas import (
    LoginRequest,
    UserCreate, 
    UserResponse,
    RefreshTokenRequest,
    PasswordChangeRequest
)
from app.utils.response import global_response_format
from app.services.auth_service import(
    login_user,
    refresh_access_token,
    logout_user,
    change_user_password
)
from uuid import UUID
from fastapi.security import HTTPAuthorizationCredentials
from app.api.dependencies import bearer_scheme, get_current_user
from app.models import User
from app.utils.security import decode_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/login", status_code=status.HTTP_200_OK)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db),
):
    try:
        user, access_token, refresh_token = login_user(
            db=db,
            login_data=login_data,
        )

        user_response = UserResponse.model_validate(user)

        return global_response_format(
            status_value=True,
            data={
                "user": user_response.model_dump(mode="json"),
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
            },
            status_code=status.HTTP_200_OK,
            status_message="Login successful",
        )

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password, or inactive account",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except RuntimeError:
        return global_response_format(
            status_value=False,
            data={},
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            status_message="Login failed",
        )


@router.post("/refresh", status_code=status.HTTP_200_OK)
def refresh_token(
    token_data: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    try:
        access_token = refresh_access_token(
            db=db,
            refresh_token=token_data.refresh_token,
        )

        return global_response_format(
            status_value=True,
            data={
                "access_token": access_token,
                "token_type": "bearer",
            },
            status_code=status.HTTP_200_OK,
            status_message="Access token refreshed successfully",
        )

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    except RuntimeError:
        return global_response_format(
            status_value=False,
            data={},
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            status_message="Token refresh failed",
        )

@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:

        if credentials is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication credentials missing",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        payload = decode_access_token(credentials.credentials)
        session_id = UUID(payload["sid"])

        logout_user(
            db=db,
            session_id=session_id,
            user_id=current_user.id,
        )

        return global_response_format(
            status_value=True,
            data={},
            status_code=status.HTTP_200_OK,
            status_message="Logout successful",
        )

    except (ValueError, KeyError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    except RuntimeError:
        return global_response_format(
            status_value=False,
            data={},
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            status_message="Logout failed",
        )


@router.post("/change-password", status_code=status.HTTP_200_OK)
def change_password(
    password_data: PasswordChangeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        change_user_password(
            db=db,
            user_id=current_user.id,
            password_data=password_data,
        )

        return global_response_format(
            status_value=True,
            data={},
            status_code=status.HTTP_200_OK,
            status_message="Password changed successfully. Please log in again.",
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
            status_message="Password change failed",
        )