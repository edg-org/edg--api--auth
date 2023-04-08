from sqlalchemy import Column, Table, ForeignKey, Integer

from api.models.BaseModel import EntityMeta

user_scope_association = Table(
    "user_scope_association",
    EntityMeta.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("scope_id", Integer, ForeignKey("scopes.id"), primary_key=True),
)