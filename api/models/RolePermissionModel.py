from sqlalchemy import Table, Column, Integer, ForeignKey

from api.models.BaseModel import EntityMeta

role_permission_association = Table(
    "role_permission_association",
    EntityMeta.metadata,
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("permissions.id"), primary_key=True),
)