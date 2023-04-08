
"""
Create a class that create and verify jwt token
"""
from datetime import datetime, timedelta

from fastapi import HTTPException, status
from jose import JWTError, jwt


class Tokenizer:
    """
    Tokenizer is the class that create and verify jwt token
    """

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
        expire = datetime.utcnow() + timedelta(days=self.access_token_expire_days)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def verify_token(self, token: str) -> dict:
        """
        Verify the token
        :param token: the token to verify
        :return: the decoded token
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )