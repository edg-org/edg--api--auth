from typing import List

from pydantic import BaseModel

from api.schemas.pydantic.core import IDModelMixin, DateTimeModelMixin


class PermissionBase(BaseModel):
    name: str
    description: str | None = None


class PermissionUpdate(BaseModel):
    description: str | None = None


class PermissionsCreate(PermissionBase):
    pass


class PermissionInDB(IDModelMixin, DateTimeModelMixin, PermissionBase):
    pass


class PermissionPublic(IDModelMixin, DateTimeModelMixin, PermissionBase):
    pass


class PermissionsPublic(BaseModel):
    count: int
    total: int
    page_size: int
    start_index: int
    results: List[PermissionPublic] = []