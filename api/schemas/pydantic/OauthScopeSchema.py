from pydantic import BaseModel

from api.schemas.pydantic.core import IDModelMixin, DateTimeModelMixin


class OauthScopeBase(BaseModel):
    """
    OauthScopeBase is the base class for OauthScope
    """
    name: str
    description: str | None = None


class OauthScopeUpdate(BaseModel):
    """
    OauthScopeUpdate is the update class for PUT request
    """
    description: str | None = None


class OauthScopeCreate(OauthScopeBase):
    """
    OauthScopeCreate is the create class for POST request
    """
    pass


class OauthScopeInDB(IDModelMixin, DateTimeModelMixin, OauthScopeBase):
    """
    OauthScopeInDB is the class for database model
    """
    pass


class OauthScopePublic(IDModelMixin, DateTimeModelMixin, OauthScopeBase):
    pass