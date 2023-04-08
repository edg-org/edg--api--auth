from typing import List

from fastapi import Depends, HTTPException, status
from pydantic.annotated_types import Type
from sqlalchemy.orm import Session, lazyload

from api.configs.Database import get_db_connection
from api.models.UserModel import User


class UserRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)) -> None:
        self.db = db

    def list(self, limit: int | None, start: int | None, deleted: bool = False) -> List[User] | list[Type[User]]:
        """
        List all users
        :param deleted: whether to include deleted users
        :param limit: the number of users to return
        :param start: the offset to start from
        :return: a list of users
        """
        query = self.db.query(User).options(lazyload(User.scopes))
        if not deleted:
            query = query.filter_by(deleted_at=None)
        return query.offset(start).limit(limit).all()

    def get(self, user: User, deleted: bool = False) -> User | None:
        """
        Get a user by id
        :param deleted: whether to include delete user
        :param user: the user to get
        :return: the user
        """
        try:
            query = self.db.query(User).options(lazyload(User.scopes))
            if not deleted:
                query = query.filter_by(deleted_at=None)
            return query.filter_by(id=user.id).first()
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"An error occurred while updating scope")

    def get_by_email(self, user: User, deleted: bool = False) -> User | None:
        """
        Get a user by email
        :param deleted: whether to include delete user
        :param user: the user to get
        :return: the user
        """
        try:
            query = self.db.query(User).options(lazyload(User.scopes))
            if not deleted:
                query = query.filter_by(deleted_at=None)
            return query.filter_by(email=user.email).first()
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"An error occurred while updating user")

    def create(self, user: User) -> User:
        """
        Create a new user
        :param user: the user to create
        :return: the created user
        """
        try:
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"An error occurred while updating user")

    def update(self, id: int, user: User, delete: bool = False) -> User:
        """
        Update a user
        :param delete: if the user is going to be deleted
        :param id: the id of the user to update
        :param user: the user to update
        :return: the updated user
        """
        try:
            user.id = id
            self.db.merge(user)
            self.db.commit()
            return self.get(user, deleted=delete)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"An error occurred while updating user")