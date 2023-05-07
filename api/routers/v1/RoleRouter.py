from typing import List

from fastapi import APIRouter, Depends, status

from api.schemas.pydantic.RoleSchema import RolePublic, RoleCreate, RoleUpdate, RolesPublic
from api.schemas.pydantic.PermissionSchema import PermissionPublic
from api.services.RoleService import RoleService
from api.utils.CustomHTTPException import NotFountException
from api.utils.JWTBearer import JWTBearer
from api.utils.utility import APIRouter_responses

RoleRouter = APIRouter(
    prefix="/v1/roles",
    tags=["Role"],
    dependencies=[Depends(JWTBearer())],
    responses=APIRouter_responses
)


@RoleRouter.get("/",
                response_model=RolesPublic,
                summary="Get all existing roles",
                description="Get all roles that are not deleted")
def index(
        pageSize: int | None = 100,
        startIndex: int | None = 0,
        role_service: RoleService = Depends(),
        token: str = Depends(JWTBearer())
):
    count, roles = role_service.get_roles(pageSize, startIndex, token)
    return {
        "results": [role.normalize() for role in roles],
        "total": len(roles),
        "count": count,
        "page_size": pageSize,
        "start_index": startIndex
    }


@RoleRouter.post("/",
                 response_model=RolePublic,
                 status_code=status.HTTP_201_CREATED,
                 summary="Create a new role",
                 description="Create a new role with a name and description")
def create(role_body: RoleCreate,
           role_service: RoleService = Depends(),
           token: str = Depends(JWTBearer())):
    try:
        return role_service.create_role(role_body, token).normalize()
    except AttributeError:
        raise NotFountException


@RoleRouter.get("/all",
                response_model=RolesPublic,
                summary="Get all roles",
                description="Get all roles including deleted ones")
def index(
        pageSize: int | None = 100,
        startIndex: int | None = 0,
        role_service: RoleService = Depends(),
        token: str = Depends(JWTBearer())
):
    count, roles = role_service.get_roles(pageSize, startIndex, token, deleted=True)
    return {
        "results": [role.normalize() for role in roles],
        "total": len(roles),
        "count": count,
        "page_size": pageSize,
        "start_index": startIndex
    }


@RoleRouter.get("/{id}",
                response_model=RolePublic | None,
                summary="Get a role",
                description="Get a role by id")
def show(id: int,
         role_service: RoleService = Depends(),
         token: str = Depends(JWTBearer())):
    try:
        return role_service.get_role(id, token).normalize()
    except AttributeError:
        raise NotFountException


@RoleRouter.put("/{id}",
                response_model=RolePublic,
                summary="Update a role",
                description="Update a role's description by id")
def update(id: int,
           role_body: RoleUpdate,
           role_service: RoleService = Depends(),
           token: str = Depends(JWTBearer())):
    try:
        return role_service.update_role(id, role_body, token).normalize()
    except AttributeError:
        raise NotFountException


@RoleRouter.delete("/{id}",
                   response_model=RolePublic,
                   summary="Delete a role",
                   description="Delete a role by id")
def delete(id: int,
           role_service: RoleService = Depends(),
           token: str = Depends(JWTBearer())):
    try:
        return role_service.delete_role(id, token).normalize()
    except AttributeError:
        raise NotFountException


@RoleRouter.get("/{id}/permissions",
                response_model=List[PermissionPublic],
                summary="Get all permissions of a role",
                description="Get all permissions of a role by id")
def get_role_permissions(id: int,
                         role_service: RoleService = Depends(),
                         token: str = Depends(JWTBearer())):
    try:
        permissions = role_service.get_role_permissions(id, token)
        return [permission.normalize() for permission in permissions if permission.deleted_at is None]
    except AttributeError:
        raise NotFountException


@RoleRouter.put("/{id}/permissions",
                response_model=List[PermissionPublic],
                summary="Update permissions to a role",
                description="Update permissions to a role by id")
def add_role_permissions(id: int,
                         permissions: List[int],
                         role_service: RoleService = Depends(),
                         token: str = Depends(JWTBearer())):
        try:
            permissions = role_service.update_role_permissions(id, permissions, token)
            return [permission.normalize() for permission in permissions]
        except AttributeError:
            raise NotFountException