from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas import(
    UserResponse,
    UserUpdate,
    AdminUserCreate,
    AdminUserUpdate,
)
from app.services.user_service import (
    admin_update_user,
    create_user,
    get_all_users,
    get_user_by_id,
    update_user,
    delete_user,
    admin_deactivate_user
)
from app.utils.response import global_response_format
from app.models import User
from app.api.dependencies import get_current_user, require_role


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
def create_internal_user(
    user_data: AdminUserCreate,
    current_user: User = Depends(require_role("Admin")),
    db: Session = Depends(get_db),
):
    try:
        new_user = create_user(
            db=db,
            user_data=user_data,
        )

        user_response = UserResponse.model_validate(new_user)

        return global_response_format(
            status_value=True,
            data=user_response.model_dump(mode="json"),
            status_code=status.HTTP_201_CREATED,
            status_message="User created successfully",
        )

    except ValueError as exc:
        error_message = str(exc)

        error_status = (
            status.HTTP_409_CONFLICT
            if error_message == "Email is already registered"
            else status.HTTP_404_NOT_FOUND
            if error_message == "Invalid role ID"
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
            status_message="User creation failed",
        )


@router.get("")
def get_users(
    current_user: User = Depends(require_role("Admin")),
    db: Session = Depends(get_db),
):
    try:
        users = get_all_users(db=db)

        user_responses = [
            UserResponse.model_validate(user).model_dump(mode="json")
            for user in users
        ]

        return global_response_format(
            status_value=True,
            data=user_responses,
            status_code=status.HTTP_200_OK,
            status_message="Users retrieved successfully",
        )

    except RuntimeError:
        return global_response_format(
            status_value=False,
            data={},
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            status_message="Failed to retrieve users",
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


@router.get("/{user_id}")
def get_user(
    user_id: int,
    current_user: User = Depends(require_role("Admin")),
    db: Session = Depends(get_db),
):
    try:
        user = get_user_by_id(
            db=db,
            user_id=user_id,
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        user_response = UserResponse.model_validate(user)

        return global_response_format(
            status_value=True,
            data=user_response.model_dump(mode="json"),
            status_code=status.HTTP_200_OK,
            status_message="User retrieved successfully",
        )

    except RuntimeError:
        return global_response_format(
            status_value=False,
            data={},
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            status_message="Failed to retrieve user",
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


@router.patch("/{user_id}")
def update_internal_user(
    user_id: int,
    user_data: AdminUserUpdate,
    current_user: User = Depends(require_role("Admin")),
    db: Session = Depends(get_db),
):
    try:
        updated_user = admin_update_user(
            db=db,
            user_id=user_id,
            user_data=user_data,
        )

        user_response = UserResponse.model_validate(updated_user)

        return global_response_format(
            status_value=True,
            data=user_response.model_dump(mode="json"),
            status_code=status.HTTP_200_OK,
            status_message="User updated successfully",
        )

    except ValueError as exc:
        error_message = str(exc)

        error_status = (
            status.HTTP_404_NOT_FOUND
            if error_message == "User not found"
            else status.HTTP_409_CONFLICT
            if error_message == "Email is already registered"
            else status.HTTP_404_NOT_FOUND
            if error_message == "Invalid role ID"
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
            status_message="Admin user update failed",
        )


@router.delete("/{user_id}")
def deactivate_internal_user(
    user_id: int,
    current_user: User = Depends(require_role("Admin")),
    db: Session = Depends(get_db),
):
    try:
        deactivated_user = admin_deactivate_user(
            db=db,
            user_id=user_id,
            current_admin_id=current_user.id,
        )

        user_response = UserResponse.model_validate(deactivated_user)

        return global_response_format(
            status_value=True,
            data=user_response.model_dump(mode="json"),
            status_code=status.HTTP_200_OK,
            status_message="User deactivated successfully",
        )

    except ValueError as exc:
        error_message = str(exc)

        error_status = (
            status.HTTP_404_NOT_FOUND
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
            status_message="User deactivation failed",
        )


@router.delete("/me")
def delete_my_account(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        delete_user(
            db=db,
            user_id=current_user.id,
        )

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
