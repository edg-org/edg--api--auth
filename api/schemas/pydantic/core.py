from pydantic import BaseModel, validator
from pydantic.schema import datetime


class DateTimeModelMixin(BaseModel):
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None

    @validator("created_at", "updated_at", pre=True)
    def default_datetime(cls, value: datetime) -> datetime:
        return value or datetime.now()


class IDModelMixin(BaseModel):
    id: int


class NotFoundExceptionSchema(BaseModel):
    detail: str = "Not found"
    exception: str = "NotFountException"
    status_code: int = 404
    headers: dict | None = None


class InternalServerErrorExceptionSchema(BaseModel):
    detail: str = "Internal server error"
    exception: str = "InternalServerErrorException"
    status_code: int = 500
    headers: dict | None = None


class InexistentTokenExceptionSchema(BaseModel):
    detail: str = "Inexistent token"
    exception: str = "InexistentTokenException"
    status_code: int = 401
    headers: dict | None = None


class ExpiredTokenExceptionSchema(BaseModel):
    detail: str = "Expired or Invalid token"
    exception: str = "InexistentTokenException"
    status_code: int = 401
    headers: dict | None = None