from pydantic import BaseModel, EmailStr, Field
from app.schemas.role import RoleResponse


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    model_config = {"extra": "forbid"}

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    model_config = {"extra": "forbid"}

class AdminUserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    role_id: int = Field(gt=0)

    model_config = {"extra": "forbid"}

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role_id: int
    role: RoleResponse
    is_active: bool
    model_config = {"from_attributes": True}

class UserUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )
    email: EmailStr | None = None
    model_config = {"extra": "forbid"}

class AdminUserUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )
    email: EmailStr | None = None
    role_id: int | None = Field(default=None, gt=0)
    is_active: bool | None = None

    model_config = {"extra": "forbid"}
