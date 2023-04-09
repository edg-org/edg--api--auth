from datetime import datetime
from fastapi import Depends, HTTPException, status

from api.models.TokenModel import Token
from api.models.UserModel import User
from api.repositories.TokenRepository import TokenRepository
from api.repositories.UserRepository import UserRepository
from api.schemas.pydantic.TokenSchema import TokenNew, TokenRefresh, TokenPayload
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

    def check_token(self, token: str) -> bool:
        token = self.tokenRepository.get_by_bearer(Token(bearer_token=Hasher.hash_sha256(token)))
        return token is not None

    def new_token(self, user_body: TokenNew) -> Token | None:
        user = self.userRepository.get_by_email(User(email=user_body.email))
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Inexistent user")

        if not Hasher.verify_password(user_body.password, user.password, user.salt):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid email or password")

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

    def new_forgot_password_token(self, email: str) -> Token | None:
        user = self.userRepository.get_by_email(User(email=email))
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Inexistent user")

        payload = {"email": user.email}
        bearer_token = forgot_password_tokenizer.create_access_token(payload)
        new_token = self.tokenRepository.create(
            Token(bearer_token=Hasher.hash_sha256(bearer_token),
                  refresh_token=Hasher.hash_sha256(bearer_token),
                  user_id=user.id))
        new_token.bearer_token = bearer_token
        new_token.refresh_token = bearer_token
        return new_token

    def renew_token(self, bearer_token: str, token_body: TokenRefresh) -> Token:
        token = self.tokenRepository.get_by_bearer(Token(bearer_token=Hasher.hash_sha256(bearer_token)))
        if token is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Inexistent bearer token")

        if (token.refresh_token != Hasher.hash_sha256(token_body.refresh_token) or
                refresh_tokenizer.verify_token(token_body.refresh_token) is None):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid refresh token")

        user = self.userRepository.get(User(id=token.user_id))
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Inexistent user")

        bearer_token = bearer_tokenizer.create_access_token({"email": user.email})
        new_token = self.tokenRepository.create(
            Token(bearer_token=Hasher.hash_sha256(bearer_token),
                  refresh_token=Hasher.hash_sha256(token_body.refresh_token),
                  user_id=user.id))
        new_token.bearer_token = bearer_token
        new_token.refresh_token = token_body.refresh_token
        return new_token

    def introspect_token(self, bearer_token: str) -> TokenPayload:
        token = self.tokenRepository.get_by_bearer(
            Token(bearer_token=Hasher.hash_sha256(bearer_token)))
        if token is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Inexistent bearer token")

        payload = bearer_tokenizer.verify_token(bearer_token)
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid bearer token")

        user = self.userRepository.get(User(id=token.user_id))
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Inexistent user")

        payload["scopes"] = [scope.name for scope in user.scopes]
        return TokenPayload(**payload)

    def revoke_token(self, bearer_token: str) -> Token:
        token = self.tokenRepository.get_by_bearer(
            Token(bearer_token=Hasher.hash_sha256(bearer_token)))
        if token is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Inexistent bearer token")

        token.deleted_at = datetime.now()
        return self.tokenRepository.update(token, delete=True)