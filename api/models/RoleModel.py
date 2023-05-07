from sqlalchemy import Column, String, Integer, DateTime, func
from sqlalchemy.orm import relationship

from api.models.BaseModel import EntityMeta
from api.models.RolePermissionModel import role_permission_association
from api.models.UserRoleAssociation import user_role_association


class Role(EntityMeta):
    """
    Role is the base class for Role model
    """

    __tablename__ = "roles"

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    name = Column(String(40), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    users = relationship(
        "User",
        secondary=user_role_association,
        back_populates="roles",
    )
    permissions = relationship(
        "Permission",
        secondary=role_permission_association,
        back_populates="roles",
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