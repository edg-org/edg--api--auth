from datetime import datetime
from typing import List

from fastapi import Depends, HTTPException, status
from api.models.OauthScopeModel import OauthScope

from api.repositories.OauthScopeRepository import OauthScopeRepository
from api.schemas.pydantic.OauthScopeSchema import OauthScopeCreate, OauthScopeUpdate
from api.services.TokenService import TokenService


class OauthScopeService:
    oauthScopeRepository: OauthScopeRepository
    tokenService: TokenService

    def __init__(
            self,
            oauthScopeRepository: OauthScopeRepository = Depends(),
            tokenService: TokenService = Depends()
    ) -> None:
        self.tokenService = tokenService
        self.oauthScopeRepository = oauthScopeRepository

    def create_scope(self, oauth_scope_body: OauthScopeCreate, token: str) -> OauthScope:
        if not self.tokenService.check_token(token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Inexistent token")
        return self.oauthScopeRepository.create(OauthScope(**oauth_scope_body.dict()))

    def get_scope(self, id: int, token: str) -> OauthScope | None:
        if not self.tokenService.check_token(token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Inexistent token")
        return self.oauthScopeRepository.get(OauthScope(id=id))

    def get_scopes(self, limit: int, start: int, token: str, deleted: bool = False) -> List[OauthScope]:
        if not self.tokenService.check_token(token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Inexistent token")
        return self.oauthScopeRepository.list(limit, start, deleted)

    def update_scope(self, id: int, oauth_scope_body: OauthScopeUpdate, token: str) -> OauthScope:
        if not self.tokenService.check_token(token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Inexistent token")

        scope = self.oauthScopeRepository.get(OauthScope(id=id))
        if scope is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="scope does not exist")
        return self.oauthScopeRepository.update(id, OauthScope(**oauth_scope_body.dict()))

    def delete_scope(self, id: int, token: str) -> OauthScope:
        if not self.tokenService.check_token(token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Inexistent token")

        scope = self.oauthScopeRepository.get(OauthScope(id=id))
        if scope is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="scope does not exist")
        return self.oauthScopeRepository.update(id, OauthScope(deleted_at=datetime.now()), delete=True)