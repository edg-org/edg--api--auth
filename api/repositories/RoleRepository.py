from typing import List, Type

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session, lazyload

from api.configs.Database import (
    get_db_connection,
)
from api.models.RoleModel import Role


class RoleRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)) -> None:
        self.db = db

    def list(self, limit: int | None, start: int | None, deleted: bool = False) -> (int, List[Role]):
        """
        List all Roles
        :param deleted: return all Roles including deleted ones
        :param limit: the number of Roles to return
        :param start: the offset to start from
        :return: a list of Roles
        """
        query = self.db.query(Role)
        if not deleted:
            query = query.filter_by(deleted_at=None)
        return query.count(), query.offset(start).limit(limit).all()

    def get(self, role: Role, deleted: bool = False) -> Role | None:
        """
        Get a Role by Role
        :param deleted: return the Role even if it is deleted
        :param role: the Role to get
        :return: the Role
        """
        query = self.db.query(Role).options(lazyload(Role.permissions))
        if not deleted:
            query = query.filter_by(deleted_at=None)
        return query.filter_by(id=role.id).first()

    def create(self, role: Role) -> Role:
        """
        Create a new Role
        :param role: the Role to create
        :return: the created Role
        """
        self.db.add(role)
        self.db.commit()
        self.db.refresh(role)
        return role

    def update(self, id: int, role: Role, delete: bool = False) -> Role:
        """
        Update a Role
        :param delete: delete the Role
        :param id: the id of the Role to update
        :param role: the Role to update
        :return: the updated Role
        """
        role.id = id
        self.db.merge(role)
        self.db.commit()
        return self.get(role, deleted=delete)