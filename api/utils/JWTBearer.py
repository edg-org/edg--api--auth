from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from api.configs.Environment import env
from api.utils.Tokenizer import Tokenizer


class JWTBearer(HTTPBearer):

    bearer_tokenizer: Tokenizer
    refresh_tokenizer: Tokenizer

    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.bearer_tokenizer = Tokenizer(env.JWT_SECRET_BEARER, env.JWT_ALGORITHM, env.JWT_EXPIRATION_DAYS_BEARER)
        # self.refresh_tokenizer = Tokenizer(env.JWT_SECRET_REFRESH, env.JWT_ALGORITHM, env.JWT_EXPIRATION_DAYS_REFRESH)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                    detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                    detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Invalid authorization code.")

    def verify_jwt(self, jwt_token: str) -> bool:
        try:
            payload = self.bearer_tokenizer.verify_token(jwt_token)
            return payload is not None
        except Exception:
            return False