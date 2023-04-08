from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from api.configs.Environment import env
from api.models.TokenModel import Token
from api.repositories.TokenRepository import TokenRepository
from api.utils.Hasher import Hasher
from api.utils.Tokenizer import Tokenizer


class JWTBearer(HTTPBearer):

    bearer_tokenizer: Tokenizer

    def __init__(self, auto_error: bool = True, tokenRepository: TokenRepository = Depends()):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.bearer_tokenizer = Tokenizer(env.JWT_SECRET_BEARER, env.JWT_ALGORITHM, env.JWT_EXPIRATION_DAYS_BEARER)
        self.tokenRepository = tokenRepository

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                    detail="Invalid authentication scheme.")

            if  not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                    detail="Invalid token or expired token.aaaa")
            return credentials.credentials
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Invalid authorization code.")

    def verify_jwt(self, jwt_token: str) -> bool:
        try:
            if self.tokenRepository.get_by_bearer(Token(bearer_token=Hasher.hash_sha256(jwt_token))) is None:
                return False
            
            payload = self.bearer_tokenizer.verify_token(jwt_token)
            return payload is not None
        except Exception:
            return False