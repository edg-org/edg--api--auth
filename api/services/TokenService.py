from datetime import datetime
from fastapi import Depends
from pydantic import EmailStr

from api.models.TokenModel import Token
from api.models.UserModel import User
from api.repositories.TokenRepository import TokenRepository
from api.repositories.UserRepository import UserRepository
from api.schemas.pydantic.TokenSchema import TokenNew, TokenRefresh, TokenPayload
from api.utils.CustomHTTPException import InexistentTokenException, EmailOrPasswordInvalidException, \
    InvalidRefreshTokenException, InvalidBearerTokenException, InexistentUserException
from api.utils.Hasher import Hasher
from api.utils.Tokenizer import forgot_password_tokenizer, refresh_tokenizer, bearer_tokenizer


class TokenService:
    tokenRepository: TokenRepository
    userRepository: UserRepository

    def __init__(
            self, tokenRepository: TokenRepository = Depends(),
            userRepository: UserRepository = Depends()
    ) -> None:
        self.tokenRepository = tokenRepository
        self.userRepository = userRepository

    def check_token_exists(self, token: str) -> Token:
        token = self.tokenRepository.get_by_bearer(Token(bearer_token=Hasher.hash_sha256(token)))
        if token is None:
            raise InexistentTokenException
        return token

    def _check_user_exists_by_email(self, email: EmailStr) -> User:
        user = self.userRepository.get_by_email(User(email=email))
        if user is None:
            raise InexistentUserException
        return user

    def _check_user_exists_by_id(self, id: int) -> User:
        user = self.userRepository.get(User(id=id))
        if user is None:
            raise InexistentUserException
        return user

    def new_token(self, user_body: TokenNew) -> Token | None:
        user = self._check_user_exists_by_email(user_body.email)
        if not Hasher.verify_password(user_body.password, user.password, user.salt):
            raise EmailOrPasswordInvalidException

        payload = {"email": user.email}
        bearer_token = bearer_tokenizer.create_access_token(payload)
        refresh_token = refresh_tokenizer.create_access_token(payload)
        new_token = self.tokenRepository.create(
            Token(bearer_token=Hasher.hash_sha256(bearer_token),
                  refresh_token=Hasher.hash_sha256(refresh_token),
                  user_id=user.id))
        new_token.bearer_token = bearer_token
        new_token.refresh_token = refresh_token
        return new_token

    def new_forgot_password_token(self, email: EmailStr) -> Token | None:
        user = self._check_user_exists_by_email(email)

        payload = {"email": user.email}
        bearer_token = forgot_password_tokenizer.create_access_token(payload)
        new_token = self.tokenRepository.create(
            Token(bearer_token=Hasher.hash_sha256(bearer_token),
                  refresh_token=Hasher.hash_sha256(bearer_token),
                  user_id=user.id))
        new_token.bearer_token = bearer_token
        new_token.refresh_token = bearer_token
        return new_token

    def renew_token(self, _bearer_token: str, token_body: TokenRefresh) -> Token:
        token = self.check_token_exists(_bearer_token)
        if (token.refresh_token != Hasher.hash_sha256(token_body.refresh_token) or
                refresh_tokenizer.verify_token(token_body.refresh_token) is None):
            raise InvalidRefreshTokenException

        user = self._check_user_exists_by_id(token.user_id)
        bearer_token = bearer_tokenizer.create_access_token({"email": user.email})
        new_token = self.tokenRepository.create(
            Token(bearer_token=Hasher.hash_sha256(bearer_token),
                  refresh_token=Hasher.hash_sha256(token_body.refresh_token),
                  user_id=user.id))
        new_token.bearer_token = bearer_token
        new_token.refresh_token = token_body.refresh_token
        # self.revoke_token(_bearer_token)
        return new_token

    def introspect_token(self, bearer_token: str) -> TokenPayload:
        token = self.check_token_exists(bearer_token)
        user = self._check_user_exists_by_id(token.user_id)
        payload = bearer_tokenizer.verify_token(bearer_token)
        payload["roles"] = [role.name for role in user.roles]
        return TokenPayload(**payload)

    def revoke_token(self, bearer_token: str) -> Token:
        token = self.check_token_exists(bearer_token)
        token.deleted_at = datetime.utcnow()
        return self.tokenRepository.update(token, delete=True)