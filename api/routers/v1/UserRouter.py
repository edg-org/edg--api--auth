from typing import List

from fastapi import APIRouter, Depends, status, HTTPException

from api.schemas.pydantic.OauthScopeSchema import OauthScopePublic
from api.schemas.pydantic.UserSchema import (
    UserPublic, UserCreate, UserUpdatePassword, UserScopes, UserUpdateVerifiedEmail
)
from api.services.UserService import UserService
from api.utils.JWTBearer import JWTBearer

UserRouter = APIRouter(
    prefix="/v1/users", tags=["user"]
)


@UserRouter.get("/",
                response_model=List[UserPublic],
                summary="Get all existing users",
                description="Get all users that are not deleted",
                dependencies=[Depends(JWTBearer())])
def index(
        pageSize: int | None = 100,
        startIndex: int | None = 0,
        userService: UserService = Depends(),
        token: str = Depends(JWTBearer())
):
    users = userService.get_users(pageSize, startIndex, token)
    return [user.normalize() for user in users]


@UserRouter.post("/",
                 response_model=UserPublic,
                 status_code=status.HTTP_201_CREATED,
                 summary="Create a new user",
                 description="Create a new user with a email and password")
def create(user_body: UserCreate, userService: UserService = Depends()):
    try:
        return userService.create_user(user_body).normalize()
    except AttributeError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found")


@UserRouter.get("/all",
                response_model=List[UserPublic],
                summary="Get all users",
                description="Get all users including deleted ones",
                dependencies=[Depends(JWTBearer())])
def index(
        pageSize: int | None = 100,
        startIndex: int | None = 0,
        userService: UserService = Depends(),
        token: str = Depends(JWTBearer())
):
    users = userService.get_users(pageSize, startIndex, token, deleted=True)
    return [user.normalize() for user in users]


@UserRouter.put("/password",
                response_model=UserPublic,
                summary="Update a user's password",
                description="Update a user's password")
async def update_password(
        user_body: UserUpdatePassword,
        userService: UserService = Depends()):
    try:
        return userService.update_password(user_body).normalize()
    except AttributeError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found")


@UserRouter.get("/{id}",
                response_model=UserPublic,
                summary="Get a user",
                description="Get a user by id",
                dependencies=[Depends(JWTBearer())])
async def show(id: int,
               userService: UserService = Depends(),
               token: str = Depends(JWTBearer())):
    try:
        return userService.get_user(id, token).normalize()
    except AttributeError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found")


@UserRouter.delete("/{id}",
                   response_model=UserPublic,
                   summary="Delete a user",
                   description="Delete a user by id",
                   dependencies=[Depends(JWTBearer())])
async def delete(id: int,
                 userService: UserService = Depends(),
                 token: str = Depends(JWTBearer())):
    try:
        return userService.delete_user(id, token).normalize()
    except AttributeError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found")


@UserRouter.get("/{id}/scopes",
                response_model=List[OauthScopePublic],
                summary="Get a user's scopes",
                description="Get a user's scopes by id (scopes are used for authorization)",
                dependencies=[Depends(JWTBearer())])
async def get_user_scopes(id: int,
                          userService: UserService = Depends(),
                          token: str = Depends(JWTBearer())):
    try:
        scopes = userService.get_user_scopes(id, token)
        return [scope.normalize() for scope in scopes]
    except AttributeError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found")


@UserRouter.put("/{id}/scopes",
                response_model=List[OauthScopePublic],
                summary="Update a user's scopes",
                description="Update a user's scopes by id (scopes are used for authorization)",
                dependencies=[Depends(JWTBearer())])
async def update_scopes(id: int,
                        user_body: UserScopes,
                        userService: UserService = Depends(),
                        token: str = Depends(JWTBearer())):
    try:
        scopes = userService.update_scopes(id, user_body, token)
        return [scope.normalize() for scope in scopes]
    except AttributeError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found")


@UserRouter.put("/{id}/email_verified",
                response_model=UserPublic,
                summary="Valide a user's email",
                description="Valide a user's email by id and set it to verified",
                dependencies=[Depends(JWTBearer())])
async def update_email_verified(id: int,
                                user_body: UserUpdateVerifiedEmail,
                                userService: UserService = Depends(),
                                token: str = Depends(JWTBearer())):
    try:
        user_body.email_verified = True
        return userService.update_verified_email(id, user_body, token).normalize()
    except AttributeError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found")