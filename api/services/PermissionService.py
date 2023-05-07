from datetime import datetime
from typing import List

from fastapi import Depends

from api.models.PermissionModel import Permission
from api.repositories.PermissionRepository import PermissionRepository
from api.schemas.pydantic.PermissionSchema import PermissionsCreate, PermissionUpdate
from api.services.TokenService import TokenService
from api.utils.CustomHTTPException import NotFountException, InexistentPermissionException


class PermissionService:
    """
    Permission service class
    """
    permissionRepository: PermissionRepository
    tokenService: TokenService

    def __init__(
            self,
            permissionRepository: PermissionRepository = Depends(),
            tokenService: TokenService = Depends()
    ) -> None:
        self.tokenService = tokenService
        self.permissionRepository = permissionRepository

    def check_permission_exists(self, id: int) -> Permission:
        permission = self.permissionRepository.get(Permission(id=id))
        if permission is None:
            raise InexistentPermissionException
        return permission

    def create_permission(self, permissions: List[PermissionsCreate], token: str) -> List[Permission]:
        self.tokenService.check_token_exists(token)
        return self.permissionRepository.create(
            [Permission(**permission.dict()) for permission in permissions]
        )

    def get_permission(self, id: int, token: str) -> Permission | None:
        self.tokenService.check_token_exists(token)
        return self.permissionRepository.get(Permission(id=id))

    def get_permissions(self, limit: int, start: int, token: str, deleted: bool = False) -> (int, List[Permission]):
        self.tokenService.check_token_exists(token)
        return self.permissionRepository.list(limit, start, deleted)

    def update_permission(self, id: int, permission_body: PermissionUpdate, token: str) -> Permission:
        self.tokenService.check_token_exists(token)
        self.check_permission_exists(id)
        return self.permissionRepository.update(id, Permission(**permission_body.dict()))

    def delete_permission(self, id: int, token: str) -> Permission:
        self.tokenService.check_token_exists(token)
        self.check_permission_exists(id)
        return self.permissionRepository.update(id, Permission(deleted_at=datetime.now()), delete=True)