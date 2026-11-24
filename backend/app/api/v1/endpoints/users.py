from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas import UserResponse, UserUpdate
from app.services.user_service import (
    update_user,
    delete_user,
)
from app.utils.response import global_response_format
from app.models import User
from app.api.dependencies import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/me")
def get_my_profile(
    current_user: User = Depends(get_current_user),
):
    user_response = UserResponse.model_validate(current_user)

    return global_response_format(
        status_value=True,
        data=user_response.model_dump(mode="json"),
        status_code=status.HTTP_200_OK,
        status_message="User profile retrieved successfully",
    )


@router.patch("/me")
def update_my_profile(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        updated_user = update_user(
            db=db,
            user_id=current_user.id,
            user_data=user_data,
        )

        user_response = UserResponse.model_validate(updated_user)

        return global_response_format(
            status_value=True,
            data=user_response.model_dump(mode="json"),
            status_code=status.HTTP_200_OK,
            status_message="User profile updated successfully",
        )

    except ValueError as exc:
        error_message = str(exc)

        error_status = (
            status.HTTP_409_CONFLICT
            if error_message == "Email is already registered"
            else status.HTTP_404_NOT_FOUND
            if error_message == "User not found"
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
            status_message="User profile update failed",
        )


@router.delete("/me")
def delete_my_account(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        delete_user(db=db, user_id=current_user.id)

        return global_response_format(
            status_value=True,
            data={},
            status_code=status.HTTP_200_OK,
            status_message="User account deactivated successfully",
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
            status_message="User account deactivation failed",
        )
