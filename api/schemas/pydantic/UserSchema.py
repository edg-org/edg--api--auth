from pydantic.schema import datetime
from pydantic import BaseModel, EmailStr, constr

from api.schemas.pydantic.core import IDModelMixin, DateTimeModelMixin


class UserBase(BaseModel):
    """
    Leaving off password and salt from base model
    """
    email: EmailStr | None = None
    email_verified: bool = False


class UserCreate(BaseModel):
    """
    Email, and password are required for registering a new user
    """
    email: EmailStr
    password: constr(min_length=8, max_length=100)


class UserUpdateVerifiedEmail(BaseModel):
    """
    Users are allowed to update their email and/or username
    """
    email_verified = True


class UserUpdatePassword(BaseModel):
    """
    Users can change their password
    """
    password: constr(min_length=8, max_length=100)


class UserScopes(BaseModel):
    """
    Users can change their password
    """
    scopes: list[int]


class UserInDB(IDModelMixin, DateTimeModelMixin, UserBase):
    """
    Add in id, created_at, updated_at, and user's password and salt
    """
    password: constr(min_length=7, max_length=100)
    salt: str


class UserPublic(IDModelMixin, DateTimeModelMixin, UserBase):
    pass