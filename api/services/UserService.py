from datetime import datetime
from typing import List

from fastapi import Depends
from pydantic import EmailStr

from api.models.UserModel import User
from api.models.RoleModel import Role
from api.repositories.TokenRepository import TokenRepository
from api.repositories.UserRepository import UserRepository
from api.repositories.RoleRepository import RoleRepository
from api.schemas.pydantic.UserSchema import (
    UserCreate, UserUpdatePassword, UserRoles, UserUpdateVerifiedEmail
)
from api.services.TokenService import TokenService
from api.utils.CustomHTTPException import InexistentUserException, InexistentTokenException, AlreadyExistsUserException
from api.utils.Hasher import Hasher
from api.utils.Tokenizer import forgot_password_tokenizer


class UserService:
    userRepository: UserRepository
    roleRepository: RoleRepository
    tokenService: TokenService
    tokenRepository: TokenRepository

    def __init__(
            self, userRepository: UserRepository = Depends(),
            roleRepository: RoleRepository = Depends(),
            tokenService: TokenService = Depends(),

    ) -> None:
        self.userRepository = userRepository
        self.roleRepository = roleRepository
        self.tokenService = tokenService

    def check_user_exists_by_email(self, email: EmailStr) -> User:
        user = self.userRepository.get_by_email(User(email=email))
        if user is None:
            raise InexistentUserException
        return user

    def check_user_exists_by_id(self, id: int) -> User:
        user = self.userRepository.get(User(id=id))
        if user is None:
            raise InexistentUserException
        return user

    def create_user(self, user_body: UserCreate) -> User:
        user = self.check_user_exists_by_email(user_body.email)
        if user is not None:
            raise AlreadyExistsUserException
        user_body.password, salt = Hasher.hash_password(user_body.password)
        return self.userRepository.create(User(email=user_body.email, password=user_body.password, salt=salt))

    def get_user(self, id: int, token: str) -> User | None:
        self.tokenService.check_token_exists(token)
        return self.check_user_exists_by_id(id)

    def get_user_by_email(self, email: EmailStr) -> User | None:
        return self.userRepository.get_by_email(User(email=email))

    def get_users(self, limit: int, start: int, token: str, deleted: bool = False) -> (int, List[User]):
        self.tokenService.check_token_exists(token)
        return self.userRepository.list(limit, start, deleted)

    def update_password(self, user_body: UserUpdatePassword) -> User:
        self.tokenService.check_token_exists(user_body.token)
        payload = forgot_password_tokenizer.verify_token(user_body.token)
        if payload is None:
            raise InexistentTokenException

        user = self.check_user_exists_by_email(payload["email"])
        user_body.password, salt = Hasher.hash_password(user_body.password)
        updated_user = self.userRepository.update(user.id, User(password=user_body.password, salt=salt))
        self.tokenService.revoke_token(user_body.token)
        return updated_user

    def get_user_roles(self, id: int, token: str) -> List[Role]:
        self.tokenService.check_token_exists(token)
        user = self.check_user_exists_by_id(id)
        return user.roles

    def update_roles(self, id: int, roles_ids: List[int], token: str) -> List[Role]:
        self.tokenService.check_token_exists(token)
        user = self.check_user_exists_by_id(id)
        roles = list(map(
            lambda role_id: self.roleRepository.get(Role(id=role_id)),
            roles_ids))
        user.roles = [role for role in roles if role is not None]
        self.userRepository.update(id, user)
        return user.roles

    def update_verified_email(self, id: int, user_body: UserUpdateVerifiedEmail, token: str) -> User:
        self.tokenService.check_token_exists(token)
        self.check_user_exists_by_id(id)
        return self.userRepository.update(id, User(**user_body.dict()))

    def delete_user(self, id: int, token: str) -> User:
        self.tokenService.check_token_exists(token)
        self.check_user_exists_by_id(id)
        return self.userRepository.update(id, User(deleted_at=datetime.now()), delete=True)