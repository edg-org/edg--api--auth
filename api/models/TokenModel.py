from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship, mapped_column

from api.models.BaseModel import EntityMeta


class Token(EntityMeta):
    """
    TokenBase is the base class for Token model
    """

    __tablename__ = "tokens"

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    bearer_token = Column(String(256), nullable=False, unique=True)
    refresh_token = Column(String(256), nullable=False)
    user_id = mapped_column(ForeignKey("users.id"))
    user = relationship("User")
    updated_at: Column = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    created_at: Column = Column(DateTime, nullable=False, server_default=func.now())
    deleted_at: Column = Column(DateTime, nullable=True)

    def normalize(self):
        return {
            "id": self.id,
            "bearer_token": self.bearer_token,
            "refresh_token": self.refresh_token,
            "updated_at": self.updated_at,
            "created_at": self.created_at,
            "deleted_at": self.deleted_at,
        }