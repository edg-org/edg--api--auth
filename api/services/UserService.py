from datetime import datetime
from typing import List

from fastapi import Depends, HTTPException, status
from pydantic import EmailStr

from api.configs.Environment import env
from api.models.UserModel import User
from api.models.OauthScopeModel import OauthScope
from api.repositories.UserRepository import UserRepository
from api.repositories.OauthScopeRepository import OauthScopeRepository
from api.schemas.pydantic.UserSchema import (
    UserCreate, UserUpdatePassword, UserScopes, UserUpdateVerifiedEmail
)
from api.services.TokenService import TokenService
from api.utils.Hasher import Hasher
from api.utils.Tokenizer import Tokenizer


class UserService:
    userRepository: UserRepository
    scopeRepository: OauthScopeRepository
    tokenService: TokenService
    forgot_password_tokenizer: Tokenizer

    def __init__(
            self, userRepository: UserRepository = Depends(),
            scopeRepository: OauthScopeRepository = Depends(),
            tokenService: TokenService = Depends()
    ) -> None:
        self.userRepository = userRepository
        self.scopeRepository = scopeRepository
        self.tokenService = tokenService
        self.forgot_password_tokenizer = Tokenizer(env.JWT_SECRET_FORGOT_PASSWORD, env.JWT_ALGORITHM,
                                                   env.JWT_EXPIRATION_MINUTES_FORGOT_PASSWORD)

    def create_user(self, user_body: UserCreate) -> User:
        user_body.password, salt = Hasher.hash_password(user_body.password)
        return self.userRepository.create(User(email=user_body.email, password=user_body.password, salt=salt))

    def get_user(self, id: int) -> User | None:
        return self.userRepository.get(User(id=id))

    def get_user_by_email(self, email: EmailStr) -> User | None:
        return self.userRepository.get_by_email(User(email=email))

    def get_users(self, limit: int, start: int, deleted: bool = False) -> List[User]:
        return self.userRepository.list(limit, start, deleted)

    def update_password(self, user_body: UserUpdatePassword) -> User:
        payload = self.forgot_password_tokenizer.verify_token(user_body.token)
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"invalid token")

        user = self.userRepository.get_by_email(User(email=payload["email"]))
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="user does not exist")

        user_body.password, salt = Hasher.hash_password(user_body.password)
        updated_user = self.userRepository.update(user.id, User(password=user_body.password, salt=salt))
        self.tokenService.revoke_token(user_body.token)
        return updated_user

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