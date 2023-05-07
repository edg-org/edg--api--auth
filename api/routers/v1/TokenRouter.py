from fastapi import APIRouter, Depends, status
from pydantic import EmailStr

from api.schemas.pydantic.TokenSchema import TokenPublic, TokenNew, TokenRefresh, TokenPayload
from api.services.TokenService import TokenService
from api.utils.CustomHTTPException import InexistentUserException, InvalidBearerTokenException
from api.utils.JWTBearer import JWTBearer
from fastapi.security import HTTPBearer

from api.utils.utility import APIRouter_responses

TokenRouter = APIRouter(
    prefix="/v1/token",
    tags=["Token"],
    dependencies=[Depends(JWTBearer())],
    responses=APIRouter_responses
)

PublicTokenRouter = APIRouter(
    prefix="/v1/token",
    tags=["Token"],
    responses=APIRouter_responses)


@PublicTokenRouter.post("/",
                        response_model=TokenPublic,
                        status_code=status.HTTP_201_CREATED,
                        summary="Create a new token",
                        description="Create a new token for a user with email and password")
def new_token(
        user_body: TokenNew,
        token_service: TokenService = Depends(),
):
    try:
        return token_service.new_token(user_body).normalize()
    except AttributeError:
        raise InexistentUserException


@PublicTokenRouter.post("/renew",
                        response_model=TokenPublic,
                        summary="Renew a token",
                        description="Renew a token for a user with refresh token",
                        dependencies=[Depends(HTTPBearer())])
def renew_token(
        token_body: TokenRefresh,
        token_service: TokenService = Depends(),
        bearer_token=Depends(HTTPBearer()),
):
    try:
        return token_service.renew_token(bearer_token.credentials, token_body).normalize()
    except AttributeError:
        raise InvalidBearerTokenException


@TokenRouter.get("/introspect",
                 response_model=TokenPayload,
                 summary="Verify a token",
                 description="Verify a token and return the payload containing user's email and scopes if valid")
def introspect_token(
        bearer_token: str = Depends(JWTBearer()),
        token_service: TokenService = Depends(),
):
    try:
        return token_service.introspect_token(bearer_token)
    except AttributeError:
        raise InvalidBearerTokenException


@TokenRouter.delete("/revoke",
                    response_model=TokenPublic,
                    summary="Revoke a token",
                    description="Revoke a token and return the deleted user")
def revoke_token(
        bearer_token: str = Depends(JWTBearer()),
        token_service: TokenService = Depends(),
):
    try:
        return token_service.revoke_token(bearer_token).normalize()
    except AttributeError:
        raise InvalidBearerTokenException


@PublicTokenRouter.get("/forgotpassword",
                 response_model=dict,
                 summary="Create a new token for forgot password",
                 description="Create a new token for forgot password with email")
def get_forgot_password_token(
        email: EmailStr,
        token_service: TokenService = Depends(),
):
    try:
        return {"token": token_service.new_forgot_password_token(email).bearer_token}
    except AttributeError:
        raise InexistentUserException