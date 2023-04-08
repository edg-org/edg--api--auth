from typing import List, Type, Any

from sqlalchemy import exc
from fastapi import Depends, HTTPException, status
from pydantic.class_validators import Type
from sqlalchemy.orm import Session

from api.configs.Database import (
    get_db_connection,
)
from api.models.OauthScopeModel import OauthScope


class OauthScopeRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)) -> None:
        self.db = db

    def list(self, limit: int | None, start: int | None, deleted: bool = False) -> List[OauthScope] | list[Type[OauthScope]]:
        """
        List all OauthScopes
        :param deleted: return all OauthScopes including deleted ones
        :param limit: the number of OauthScopes to return
        :param start: the offset to start from
        :return: a list of OauthScopes
        """
        query = self.db.query(OauthScope)
        if not deleted:
            query = query.filter_by(deleted_at=None)
        return query.offset(start).limit(limit).all()

    def get(self, oauth_scope: OauthScope, deleted: bool = False) -> OauthScope | None:
        """
        Get a OauthScope by OauthScope
        :param deleted: return the OauthScope even if it is deleted
        :param oauth_scope: the OauthScope to get
        :return: the OauthScope
        """
        try:
            query = self.db.query(OauthScope)
            if not deleted:
                query = query.filter_by(deleted_at=None)
            return query.filter_by(id=oauth_scope.id).first()
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while getting scope")

    def create(self, oauth_scope: OauthScope) -> OauthScope:
        """
        Create a new OauthScope
        :param oauth_scope: the OauthScope to create
        :return: the created OauthScope
        """
        try:
            self.db.add(oauth_scope)
            self.db.commit()
            self.db.refresh(oauth_scope)
            return oauth_scope
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while updating scope")

    def update(self, id: int, oauth_scope: OauthScope, delete: bool = False) -> OauthScope:
        """
        Update a OauthScope
        :param delete: delete the OauthScope
        :param id: the id of the OauthScope to update
        :param oauth_scope: the OauthScope to update
        :return: the updated OauthScope
        """
        try:
            oauth_scope.id = id
            self.db.merge(oauth_scope)
            self.db.commit()
            return self.get(oauth_scope, deleted=delete)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while updating scope")