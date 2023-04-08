from sqlalchemy import Column, String, Integer, DateTime, func
from sqlalchemy.orm import relationship

from api.models.BaseModel import EntityMeta
from api.models.UserScopeAssociation import user_scope_association


class OauthScope(EntityMeta):
    """
    OauthScope is the base class for OauthScope model
    """

    __tablename__ = "scopes"

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    name = Column(String(40), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    users = relationship(
        "User",
        secondary=user_scope_association,
        back_populates="scopes",
    )
    updated_at: Column = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    created_at: Column = Column(DateTime, nullable=False, server_default=func.now())
    deleted_at: Column = Column(DateTime, nullable=True)

    def normalize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "updated_at": self.updated_at,
            "created_at": self.created_at,
            "deleted_at": self.deleted_at,
        }