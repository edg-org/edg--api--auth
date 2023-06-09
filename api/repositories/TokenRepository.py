from fastapi import Depends, HTTPException, status, logger
from sqlalchemy.orm import Session

from api.configs.Database import (
    get_db_connection,
)
from api.models.TokenModel import Token


class TokenRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)) -> None:
        self.db = db

    def create(self, token: Token) -> Token:
        """
        Create a new token
        :param token: the token to create
        :return: the created token
        """
        self.db.add(token)
        self.db.commit()
        self.db.refresh(token)
        return token

    def update(self, token: Token, delete: bool = False) -> Token:
        """
        Update a token
        :param delete: if the token should be deleted
        :param token: the token to update
        :return: the updated token
        """
        self.db.add(token)
        self.db.commit()
        return self.get_by_bearer(token, deleted=delete)

    def get_by_bearer(self, token: Token, deleted: bool = False) -> Token | None:
        """
        Get a token by bearer
        :param deleted: get the token even if the token is deleted
        :param token: the token to get
        :return: the token
        """
        query = self.db.query(Token)
        if not deleted:
            query = query.filter_by(deleted_at=None)
        return query.filter_by(bearer_token=token.bearer_token).first()