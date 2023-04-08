from typing import List

from fastapi import APIRouter, Depends, status, HTTPException

from api.schemas.pydantic.OauthScopeSchema import OauthScopePublic, OauthScopeCreate, OauthScopeUpdate
from api.services.OauthScopeService import OauthScopeService
from api.utils.JWTBearer import JWTBearer

OauthScopeRouter = APIRouter(
    prefix="/v1/scopes", tags=["scope"]
)


@OauthScopeRouter.get("/",
                      response_model=List[OauthScopePublic],
                      summary="Get all existing scopes",
                      description="Get all scopes that are not deleted",
                      dependencies=[Depends(JWTBearer())])
def index(
        pageSize: int | None = 100,
        startIndex: int | None = 0,
        oauthScopeService: OauthScopeService = Depends(),
):
    oauth_scopes = oauthScopeService.get_scopes(pageSize, startIndex)
    return [oauth_scope.normalize() for oauth_scope in oauth_scopes]


@OauthScopeRouter.post("/",
                       response_model=OauthScopePublic,
                       status_code=status.HTTP_201_CREATED,
                       summary="Create a new scope",
                       description="Create a new scope with a name and description",
                       dependencies=[Depends(JWTBearer())])
def create(scope_body: OauthScopeCreate, oauthScopeService: OauthScopeService = Depends()):
    try:
        oauth_scope = oauthScopeService.create_scope(scope_body)
        return oauth_scope.normalize()
    except AttributeError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="scope not found")


@OauthScopeRouter.get("/all",
                      response_model=List[OauthScopePublic],
                      summary="Get all scopes",
                      description="Get all scopes including deleted ones",
                      dependencies=[Depends(JWTBearer())])
def index(
        pageSize: int | None = 100,
        startIndex: int | None = 0,
        oauthScopeService: OauthScopeService = Depends(),
):
    oauth_scopes = oauthScopeService.get_scopes(pageSize, startIndex, deleted=True)
    return [oauth_scope.normalize() for oauth_scope in oauth_scopes]


@OauthScopeRouter.get("/{id}",
                      response_model=OauthScopePublic | None,
                      summary="Get a scope",
                      description="Get a scope by id",
                      dependencies=[Depends(JWTBearer())])
def show(id: int, oauthScopeService: OauthScopeService = Depends()):
    try:
        oauth_scope = oauthScopeService.get_scope(id)
        return oauth_scope.normalize()
    except AttributeError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="scope not found")


@OauthScopeRouter.put("/{id}",
                      response_model=OauthScopePublic,
                      summary="Update a scope",
                      description="Update a scope's description by id",
                      dependencies=[Depends(JWTBearer())])
def update(id: int, OauthScope_body: OauthScopeUpdate, oauthScopeService: OauthScopeService = Depends()):
    try:
        oauth_scope = oauthScopeService.update_scope(id, OauthScope_body)
        return oauth_scope.normalize()
    except AttributeError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="scope not found")


@OauthScopeRouter.delete("/{id}",
                         response_model=OauthScopePublic,
                         summary="Delete a scope",
                         description="Delete a scope by id",
                         dependencies=[Depends(JWTBearer())])
def delete(id: int, oauthScopeService: OauthScopeService = Depends()):
    try:
        oauth_scope = oauthScopeService.delete_scope(id)
        return oauth_scope.normalize()
    except AttributeError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="scope not found")