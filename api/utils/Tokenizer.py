
"""
Create a class that create and verify jwt token
"""
from datetime import datetime, timedelta
from jose import JWTError, jwt

from api.configs.Environment import env
from api.repositories.TokenRepository import TokenRepository


class Tokenizer:
    """
    Tokenizer is the class that create and verify jwt token
    """

    tokenRepository: TokenRepository

    def __init__(self, secret_key: str, algorithm: str, access_token_expire_days: int):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_days = access_token_expire_days

    def create_access_token(self, data: dict) -> str:
        """
        Create an access token
        :param data: the data to encode
        :return: the access token
        """
        to_encode = data.copy()
        expire = datetime.now() + timedelta(days=self.access_token_expire_days)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def verify_token(self, token: str) -> dict | None:
        """
        Verify the token
        :param token: the token to verify
        :return: the decoded token
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload if "exp" in payload and datetime.fromtimestamp(payload["exp"]) >= datetime.now() else None
        except JWTError:
            return None


bearer_tokenizer = Tokenizer(env.JWT_SECRET_BEARER, env.JWT_ALGORITHM, env.JWT_EXPIRATION_DAYS_BEARER)
refresh_tokenizer = Tokenizer(env.JWT_SECRET_REFRESH, env.JWT_ALGORITHM, env.JWT_EXPIRATION_DAYS_REFRESH)
forgot_password_tokenizer = Tokenizer(env.JWT_SECRET_FORGOT_PASSWORD, env.JWT_ALGORITHM,
                                      env.JWT_EXPIRATION_DAYS_BEARER)