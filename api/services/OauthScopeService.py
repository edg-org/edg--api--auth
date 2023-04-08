from datetime import datetime
from typing import List

from fastapi import Depends, HTTPException, status
from api.models.OauthScopeModel import OauthScope

from api.repositories.OauthScopeRepository import OauthScopeRepository
from api.schemas.pydantic.OauthScopeSchema import OauthScopeCreate, OauthScopeUpdate


class OauthScopeService:
    oauthScopeRepository: OauthScopeRepository

    def __init__(
            self, oauthScopeRepository: OauthScopeRepository = Depends()
    ) -> None:
        self.oauthScopeRepository = oauthScopeRepository

    def create_scope(self, oauth_scope_body: OauthScopeCreate) -> OauthScope:
        return self.oauthScopeRepository.create(OauthScope(**oauth_scope_body.dict()))

    def get_scope(self, id: int) -> OauthScope | None:
        return self.oauthScopeRepository.get(OauthScope(id=id))

    def get_scopes(self, limit: int, start: int, deleted: bool = False) -> List[OauthScope]:
        return self.oauthScopeRepository.list(limit, start, deleted)

    def update_scope(self, id: int, oauth_scope_body: OauthScopeUpdate) -> OauthScope:
        scope = self.oauthScopeRepository.get(OauthScope(id=id))
        if scope is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="scope does not exist")
        return self.oauthScopeRepository.update(id, OauthScope(**oauth_scope_body.dict()))

    def delete_scope(self, id: int) -> OauthScope:
        scope = self.oauthScopeRepository.get(OauthScope(id=id))
        if scope is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="scope does not exist")
        return self.oauthScopeRepository.update(id, OauthScope(deleted_at=datetime.now()), delete=True)