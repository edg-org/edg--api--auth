from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import EmailStr

from api.schemas.pydantic.TokenSchema import TokenPublic, TokenNew, TokenRefresh, TokenPayload
from api.services.TokenService import TokenService
from api.utils.JWTBearer import JWTBearer
from fastapi.security import HTTPBearer

TokenRouter = APIRouter(
    prefix="/v1/token", tags=["token"]
)


@TokenRouter.post("/",
                  response_model=TokenPublic,
                  status_code=status.HTTP_201_CREATED,
                  summary="Create a new token",
                  description="Create a new token for a user with email and password")
def new_token(
        user_body: TokenNew,
        tokenService: TokenService = Depends(),
):
    try:
        return tokenService.new_token(user_body).normalize()
    except AttributeError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found")


@TokenRouter.post("/renew",
                  response_model=TokenPublic,
                  summary="Renew a token",
                  description="Renew a token for a user with refresh token",
                  dependencies=[Depends(HTTPBearer())])
def renew_token(
        token_body: TokenRefresh,
        tokenService: TokenService = Depends(),
        bearer_token=Depends(HTTPBearer()),
):
    try:
        return tokenService.renew_token(bearer_token.credentials, token_body).normalize()
    except AttributeError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"token not found for bearer token {bearer_token.credentials}")


@TokenRouter.post("/introspect",
                  response_model=TokenPayload,
                  summary="Verify a token",
                  description="Verify a token and return the payload containing user's email and scopes if valid",
                  dependencies=[Depends(JWTBearer())])
def introspect_token(
        bearer_token: str = Depends(JWTBearer()),
        tokenService: TokenService = Depends(),
):
    try:
        return tokenService.introspect_token(bearer_token)
    except AttributeError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="token not found")


@TokenRouter.post("/revoke",
                  response_model=TokenPublic,
                  summary="Revoke a token",
                  description="Revoke a token and return the deleted user",
                  dependencies=[Depends(JWTBearer())])
def revoke_token(
        bearer_token: str = Depends(JWTBearer()),
        tokenService: TokenService = Depends(),
):
    try:
        return tokenService.revoke_token(bearer_token).normalize()
    except AttributeError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="token not found")


@TokenRouter.get("/forgot_password",
                 response_model=dict,
                 summary="Create a new token for forgot password",
                 description="Create a new token for forgot password with email")
def get_forgot_password_token(
        email: EmailStr,
        tokenService: TokenService = Depends(),
):
    try:
        return {"token": tokenService.new_forgot_password_token(email).bearer_token}
    except AttributeError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found")