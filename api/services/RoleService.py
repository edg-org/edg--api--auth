from datetime import datetime
from typing import List

from fastapi import Depends

from api.models.PermissionModel import Permission
from api.models.RoleModel import Role
from api.repositories.PermissionRepository import PermissionRepository

from api.repositories.RoleRepository import RoleRepository
from api.schemas.pydantic.RoleSchema import RoleCreate, RoleUpdate
from api.services.TokenService import TokenService
from api.utils.CustomHTTPException import InexistentRoleException


class RoleService:
    roleRepository: RoleRepository
    tokenService: TokenService

    def __init__(
            self,
            roleRepository: RoleRepository = Depends(),
            permissionRepository: PermissionRepository = Depends(),
            tokenService: TokenService = Depends()
    ) -> None:
        self.tokenService = tokenService
        self.roleRepository = roleRepository
        self.permissionRepository = permissionRepository

    def check_role_exists(self, id: int) -> Role:
        role = self.roleRepository.get(Role(id=id))
        if role is None:
            raise InexistentRoleException
        return role

    def create_role(self, role_body: RoleCreate, token: str) -> Role:
        self.tokenService.check_token_exists(token)
        return self.roleRepository.create(Role(**role_body.dict()))

    def get_role(self, id: int, token: str) -> Role | None:
        self.tokenService.check_token_exists(token)
        return self.roleRepository.get(Role(id=id))

    def get_roles(self, limit: int, start: int, token: str, deleted: bool = False) -> (int, List[Role]):
        self.tokenService.check_token_exists(token)
        return self.roleRepository.list(limit, start, deleted)

    def update_role(self, id: int, role_body: RoleUpdate, token: str) -> Role:
        self.tokenService.check_token_exists(token)
        self.check_role_exists(id)
        return self.roleRepository.update(id, Role(**role_body.dict()))

    def delete_role(self, id: int, token: str) -> Role:
        self.tokenService.check_token_exists(token)
        self.check_role_exists(id)
        return self.roleRepository.update(id, Role(deleted_at=datetime.now()), delete=True)

    def get_role_permissions(self, id: int, token: str) -> List[Permission]:
        self.tokenService.check_token_exists(token)
        role = self.check_role_exists(id)
        return role.permissions

    def update_role_permissions(self, id: int, permissions_ids: List[int], token: str) -> List[Permission]:
        self.tokenService.check_token_exists(token)
        role = self.check_role_exists(id)
        permissions = list(map(
            lambda permission_id: self.permissionRepository.get(Permission(id=permission_id)),
            permissions_ids
        ))
        role.permissions = [permission for permission in permissions if permission is not None]
        return self.roleRepository.update(id, role).permissions