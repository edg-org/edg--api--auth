from sqlalchemy import Column, String, Boolean, DateTime, func, Integer
from sqlalchemy.orm import relationship

from api.models.BaseModel import EntityMeta
from api.models.UserScopeAssociation import user_scope_association


class User(EntityMeta):
    """
    User is the base class for User model
    """

    __tablename__ = "users"

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    email = Column(String(40), nullable=False, unique=True)
    email_verified = Column(Boolean, nullable=False, default=False)
    password = Column(String(256), nullable=False)
    salt = Column(String(100), nullable=False)
    scopes = relationship(
        "OauthScope",
        secondary=user_scope_association,
        back_populates="users",
    )
    updated_at: Column = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    created_at: Column = Column(DateTime, nullable=False, server_default=func.now())
    deleted_at: Column = Column(DateTime, nullable=True)

    def normalize(self):
        return {
            "id": self.id,
            "email": self.email,
            "email_verified": self.email_verified,
            "password": self.password,
            "salt": self.salt,
            "updated_at": self.updated_at,
            "created_at": self.created_at,
            "deleted_at": self.deleted_at,
        }