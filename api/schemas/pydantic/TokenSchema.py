from pydantic.schema import datetime
from pydantic import BaseModel, EmailStr, constr

from api.schemas.pydantic.core import IDModelMixin, DateTimeModelMixin


class TokenBase(BaseModel):
    """
    Only store token and token_type
    """
    bearer_token: str
    refresh_token: str


class TokenNew(BaseModel):
    """
    Used for getting a token
    """
    email: EmailStr
    password: constr(min_length=8, max_length=100)


class TokenUpdate(BaseModel):
    """
    Used for deleting a token
    """
    deleted_at: datetime | None = None


class TokenPayload(BaseModel):
    """
    Used for decoding a token
    """
    email: EmailStr
    exp: datetime
    roles: list[str]


class TokenRefresh(BaseModel):
    """
    Email, and password are required for registering a new user
    """
    refresh_token: str


class TokenInDB(IDModelMixin, DateTimeModelMixin, TokenBase):
    """
    Add in id, created_at, updated_at, and user's id
    """
    user_id: int


class TokenPublic(IDModelMixin, DateTimeModelMixin, TokenBase):
    pass