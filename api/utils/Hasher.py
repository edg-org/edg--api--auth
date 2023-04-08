import hashlib
from passlib.context import CryptContext
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    @staticmethod
    def hash_password(password: str) -> [str, str]:
        salt = os.urandom(32).hex()
        return pwd_context.hash(password + salt), salt

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str, salt: str) -> bool:
        return pwd_context.verify(plain_password + salt, hashed_password)

    @staticmethod
    def hash_sha256(secret: str) -> str:
        return hashlib.sha256(secret.encode()).hexdigest()