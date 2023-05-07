from typing import List

from pydantic import BaseModel

from api.schemas.pydantic.core import IDModelMixin, DateTimeModelMixin


class RoleBase(BaseModel):
    """
    RoleBase is the base class for Role
    """
    name: str
    description: str | None = None


class RoleUpdate(BaseModel):
    """
    RoleUpdate is the update class for PUT request
    """
    description: str | None = None


class RoleCreate(RoleBase):
    """
    RoleCreate is the create class for POST request
    """
    pass


class RoleInDB(IDModelMixin, DateTimeModelMixin, RoleBase):
    """
    RoleInDB is the class for database model
    """
    pass


class RolePublic(IDModelMixin, DateTimeModelMixin, RoleBase):
    pass


class RolesPublic(BaseModel):
    """
    RolesPublic is the class for public response
    """
    count: int
    total: int
    page_size: int
    start_index: int
    results: List[RolePublic] = []