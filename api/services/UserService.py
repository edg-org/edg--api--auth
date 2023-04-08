from datetime import datetime
from typing import List

from fastapi import Depends, HTTPException, status
from pydantic import EmailStr

from api.models.UserModel import User
from api.models.OauthScopeModel import OauthScope
from api.repositories.UserRepository import UserRepository
from api.repositories.OauthScopeRepository import OauthScopeRepository
from api.schemas.pydantic.UserSchema import (
    UserCreate, UserUpdatePassword, UserScopes, UserUpdateVerifiedEmail
)
from api.utils.Hasher import Hasher


class UserService:
    userRepository: UserRepository
    scopeRepository: OauthScopeRepository

    def __init__(
            self, userRepository: UserRepository = Depends(),
            scopeRepository: OauthScopeRepository = Depends()
    ) -> None:
        self.userRepository = userRepository
        self.scopeRepository = scopeRepository

    def create_user(self, user_body: UserCreate) -> User:
        user_body.password, user_body.salt = Hasher.hash_password(user_body.password)
        return self.userRepository.create(User(**user_body.dict()))

    def get_user(self, id: int) -> User | None:
        return self.userRepository.get(User(id=id))

    def get_user_by_email(self, email: EmailStr) -> User | None:
        return self.userRepository.get_by_email(User(email=email))

    def get_users(self, limit: int, start: int, deleted: bool = False) -> List[User]:
        return self.userRepository.list(limit, start, deleted)

    def update_password(self, id: int, user_body: UserUpdatePassword) -> User:
        user = self.userRepository.get(User(id=id))
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="user does not exist")

        user_body.password, user_body.salt = Hasher.hash_password(user_body.password)
        return self.userRepository.update(id, User(**user_body.dict()))

    def get_user_scopes(self, id: int) -> List[OauthScope]:
        user = self.userRepository.get(User(id=id))
        return user.scopes

    def update_scopes(self, id: int, user_body: UserScopes) -> List[OauthScope]:
        scopes = map(
            lambda scope_id: self.scopeRepository.get(OauthScope(id=scope_id)),
            user_body.scopes)
        user = self.userRepository.get(User(id=id))
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="user does not exist")

        user.scopes = list(scopes)
        self.userRepository.update(id, user)
        return user.scopes

    def update_verified_email(self, id: int, user_body: UserUpdateVerifiedEmail) -> User:
        user = self.userRepository.get(User(id=id))
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="user does not exist")

        return self.userRepository.update(id, User(**user_body.dict()))

    def delete_user(self, id: int) -> User:
        user = self.userRepository.get(User(id=id))
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="user does not exist")

        return self.userRepository.update(id, User(deleted_at=datetime.now()), delete=True)