from typing import List, Type

from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session

from api.configs.Database import get_db_connection
from api.models.PermissionModel import Permission


class PermissionRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)) -> None:
        self.db = db

    def list(self, limit: int | None, start: int | None, deleted: bool = False) -> (int, List[Permission]):
        """
        List all Permissions
        :param deleted: return all permissions including deleted ones
        :param limit: the number of permissions to return
        :param start: the offset to start from
        :return: a list of permissions
        """
        query = self.db.query(Permission)
        if not deleted:
            query = query.filter_by(deleted_at=None)
        return query.count(), query.offset(start).limit(limit).all()

    def get(self, permission: Permission, deleted: bool = False) -> Permission | None:
        """
        Get a Permission by Permission
        :param deleted: return the Permission even if it is deleted
        :param permission: the Permission to get
        :return: the Permission
        """
        query = self.db.query(Permission)
        if not deleted:
            query = query.filter_by(deleted_at=None)
        return query.filter_by(id=permission.id).first()

    def create(self, permissions: List[Permission]) -> List[Permission]:
        """
        Create a new permission
        :param permissions: the permissions to create
        :return: the created permission
        """
        self.db.add_all(permissions)
        self.db.commit()
        return permissions

    def update(self, id: int, permission: Permission, delete: bool = False) -> Permission:
        """
        Update a permission
        :param delete: delete the permission instead of updating it
        :param id: the id of the permission to update
        :param permission: the permission to update
        :return: the updated permission
        """
        permission.id = id
        self.db.merge(permission)
        self.db.commit()
        return self.get(permission, deleted=delete)