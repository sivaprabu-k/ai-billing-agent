from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

    model_config = {"extra": "forbid"}


class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(min_length=1)

    model_config = {"extra": "forbid"}


class PasswordChangeRequest(BaseModel):
    current_password: str = Field(min_length=8, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)

    model_config = {"extra": "forbid"}