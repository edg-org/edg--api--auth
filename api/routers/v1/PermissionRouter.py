from typing import List

from fastapi import APIRouter, Depends, status

from api.schemas.pydantic.PermissionSchema import PermissionsPublic, PermissionPublic, PermissionsCreate, \
    PermissionUpdate
from api.services.PermissionService import PermissionService
from api.utils.CustomHTTPException import NotFountException
from api.utils.JWTBearer import JWTBearer
from api.utils.utility import APIRouter_responses

PermissionRouter = APIRouter(
    prefix="/v1/permissions",
    tags=["Permission"],
    dependencies=[Depends(JWTBearer())],
    responses=APIRouter_responses
)


@PermissionRouter.get("/",
                      summary="Get all existing permissions",
                      description="Get all permissions that are not deleted",
                      response_model=PermissionsPublic)
def index(
        pageSize: int | None = 100,
        startIndex: int | None = 0,
        permissionService: PermissionService = Depends(),
        token: str = Depends(JWTBearer())
):
    count, permissions = permissionService.get_permissions(pageSize, startIndex, token)
    return {
        "results": [permission.normalize() for permission in permissions],
        "total": len(permissions),
        "count": count,
        "page_size": pageSize,
        "start_index": startIndex
    }


@PermissionRouter.post("/",
                       summary="Create a new permission",
                       description="Create a new permission with a name and description",
                       response_model=List[PermissionPublic],
                       status_code=status.HTTP_201_CREATED)
def create(permission_body: List[PermissionsCreate],
           permissionService: PermissionService = Depends(),
           token: str = Depends(JWTBearer())):
    try:
        permissions = permissionService.create_permission(permission_body, token)
        return [permission.normalize() for permission in permissions]
    except AttributeError:
        raise NotFountException


@PermissionRouter.get("/all",
                      summary="Get all permissions",
                      description="Get all permissions including deleted ones",
                      response_model=PermissionsPublic)
def index(
        pageSize: int | None = 100,
        startIndex: int | None = 0,
        permissionService: PermissionService = Depends(),
        token: str = Depends(JWTBearer())
):
    permissions = permissionService.get_permissions(pageSize, startIndex, token, deleted=True)
    return {
        "results": [permission.normalize() for permission in permissions],
        "total": len(permissions),
        "count": 0,
        "page_size": pageSize,
        "start_index": startIndex
    }


@PermissionRouter.get("/{id}",
                      summary="Get a permission by id",
                      description="Get a permission by id",
                      response_model=PermissionPublic)
def show(id: int,
         permissionService: PermissionService = Depends(),
         token: str = Depends(JWTBearer())):
    try:
        permission = permissionService.get_permission(id, token)
        return permission.normalize()
    except AttributeError:
        raise NotFountException


@PermissionRouter.put("/{id}",
                      summary="Update a permission by id",
                      description="Update a permission by id",
                      response_model=PermissionPublic)
def update(id: int,
           permission_body: PermissionUpdate,
           permissionService: PermissionService = Depends(),
           token: str = Depends(JWTBearer())):
    try:
        permission = permissionService.update_permission(id, permission_body, token)
        return permission.normalize()
    except AttributeError:
        raise NotFountException


@PermissionRouter.delete("/{id}",
                         summary="Delete a permission by id",
                         description="Delete a permission by id",
                         response_model=PermissionPublic)
def delete(id: int,
           permissionService: PermissionService = Depends(),
           token: str = Depends(JWTBearer())):
    try:
        permission = permissionService.delete_permission(id, token)
        return permission.normalize()
    except AttributeError:
        raise NotFountException