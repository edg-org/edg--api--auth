from typing import List

from fastapi import APIRouter, Depends, status

from api.schemas.pydantic.RoleSchema import RolePublic
from api.schemas.pydantic.UserSchema import (
    UserPublic, UserCreate, UserUpdatePassword, UserUpdateVerifiedEmail, UsersPublic
)
from api.services.UserService import UserService
from api.utils.CustomHTTPException import InexistentUserException
from api.utils.JWTBearer import JWTBearer
from api.utils.utility import APIRouter_responses

UserRouter = APIRouter(
    prefix="/v1/users",
    tags=["User"],
    dependencies=[Depends(JWTBearer())],
    responses=APIRouter_responses
)

PublicUserRouter = APIRouter(
    prefix="/v1/users",
    tags=["User"],
    responses=APIRouter_responses)


@UserRouter.get("/",
                response_model=UsersPublic,
                summary="Get all existing users",
                description="Get all users that are not deleted")
def index(
        pageSize: int | None = 100,
        startIndex: int | None = 0,
        userService: UserService = Depends(),
        token: str = Depends(JWTBearer())
):
    count, users = userService.get_users(pageSize, startIndex, token)
    return {
        "results": [user.normalize() for user in users],
        "total": len(users),
        "count": count,
        "page_size": pageSize,
        "start_index": startIndex
    }


@PublicUserRouter.post("/",
                       response_model=UserPublic,
                       status_code=status.HTTP_201_CREATED,
                       summary="Create a new user",
                       description="Create a new user with a email and password")
def create(user_body: UserCreate, userService: UserService = Depends()):
    try:
        return userService.create_user(user_body).normalize()
    except AttributeError:
        raise InexistentUserException


@UserRouter.get("/all",
                response_model=UsersPublic,
                summary="Get all users",
                description="Get all users including deleted ones")
def index(
        pageSize: int | None = 100,
        startIndex: int | None = 0,
        userService: UserService = Depends(),
        token: str = Depends(JWTBearer())
):
    count, users = userService.get_users(pageSize, startIndex, token, deleted=True)
    return {
        "results": [user.normalize() for user in users],
        "total": len(users),
        "count": count,
        "page_size": pageSize,
        "start_index": startIndex
    }


@PublicUserRouter.put("/password",
                      response_model=UserPublic,
                      summary="Update a user's password",
                      description="Update a user's password")
async def update_password(
        user_body: UserUpdatePassword,
        userService: UserService = Depends()):
    try:
        return userService.update_password(user_body).normalize()
    except AttributeError:
        raise InexistentUserException


@UserRouter.get("/{id}",
                response_model=UserPublic,
                summary="Get a user",
                description="Get a user by id")
async def show(id: int,
               userService: UserService = Depends(),
               token: str = Depends(JWTBearer())):
    try:
        return userService.get_user(id, token).normalize()
    except AttributeError:
        raise InexistentUserException


@UserRouter.delete("/{id}",
                   response_model=UserPublic,
                   summary="Delete a user",
                   description="Delete a user by id",)
async def delete(id: int,
                 userService: UserService = Depends(),
                 token: str = Depends(JWTBearer())):
    try:
        return userService.delete_user(id, token).normalize()
    except AttributeError:
        raise InexistentUserException


@UserRouter.get("/{id}/roles",
                response_model=List[RolePublic],
                summary="Get a user's roles",
                description="Get a user's roles by id (roles are used for authorization)")
async def get_user_roles(id: int,
                         userService: UserService = Depends(),
                         token: str = Depends(JWTBearer())):
    try:
        roles = userService.get_user_roles(id, token)
        return [role.normalize() for role in roles]
    except AttributeError:
        raise InexistentUserException


@UserRouter.put("/{id}/roles",
                response_model=List[RolePublic],
                summary="Update a user's roles",
                description="Update a user's roles by id (roles are used for authorization)")
async def update_roles(id: int,
                       roles_ids: List[int],
                       userService: UserService = Depends(),
                       token: str = Depends(JWTBearer())):
    try:
        roles = userService.update_roles(id, roles_ids, token)
        return [role.normalize() for role in roles]
    except AttributeError:
        raise InexistentUserException


@UserRouter.put("/{id}/emailverified",
                response_model=UserPublic,
                summary="Valide a user's email",
                description="Valide a user's email by id and set it to verified")
async def update_email_verified(id: int,
                                user_body: UserUpdateVerifiedEmail,
                                userService: UserService = Depends(),
                                token: str = Depends(JWTBearer())):
    try:
        user_body.email_verified = True
        return userService.update_verified_email(id, user_body, token).normalize()
    except AttributeError:
        raise InexistentUserException