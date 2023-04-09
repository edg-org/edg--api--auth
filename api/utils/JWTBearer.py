from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from api.repositories.TokenRepository import TokenRepository
from api.utils.Tokenizer import bearer_tokenizer


class JWTBearer(HTTPBearer):
    token_repository: TokenRepository

    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                    detail="Invalid authentication scheme.")

            if bearer_tokenizer.verify_token(credentials.credentials) is None:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                    detail="Invalid token or expired token")
            return credentials.credentials
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Invalid authorization code.")