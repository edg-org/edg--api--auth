from sqlalchemy import Column, Table, ForeignKey, Integer

from api.models.BaseModel import EntityMeta

user_role_association = Table(
    "user_role_association",
    EntityMeta.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
)