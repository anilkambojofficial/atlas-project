"""Identity wire DTOs — ES-002 camelCase aliases; validation at the boundary."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class _WireModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    def wire(self) -> dict:
        return self.model_dump(by_alias=True, mode="json")


class RegisterRequest(_WireModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=512)
    display_name: str = Field(alias="displayName", min_length=1, max_length=200)
    organization_name: str | None = Field(
        alias="organizationName", default=None, max_length=200
    )
    organization_slug: str | None = Field(
        alias="organizationSlug", default=None, max_length=100
    )


class LoginRequest(_WireModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=512)


class PasswordResetRequest(_WireModel):
    email: EmailStr


class PasswordResetConfirm(_WireModel):
    token: str = Field(min_length=16, max_length=200)
    new_password: str = Field(alias="newPassword", min_length=1, max_length=512)


class EmailVerifyRequest(_WireModel):
    token: str = Field(min_length=16, max_length=200)


class ProfileUpdateRequest(_WireModel):
    display_name: str = Field(alias="displayName", min_length=1, max_length=200)


class MembershipView(_WireModel):
    organization_id: str = Field(alias="organizationId")
    role_id: str = Field(alias="roleId")
    status: str


class UserView(_WireModel):
    id: str
    email: str
    display_name: str = Field(alias="displayName")
    status: str
    email_verified: bool = Field(alias="emailVerified")
    created_at: datetime = Field(alias="createdAt")
    last_login_at: datetime | None = Field(alias="lastLoginAt", default=None)
    memberships: list[MembershipView] = Field(default_factory=list)


class TokenView(_WireModel):
    access_token: str = Field(alias="accessToken")
    token_type: str = Field(alias="tokenType", default="Bearer")
    expires_in: int = Field(alias="expiresIn")
    organization_id: str | None = Field(alias="organizationId", default=None)
    roles: list[str] = Field(default_factory=list)
    permissions: list[str] = Field(default_factory=list)
    user: UserView
