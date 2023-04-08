from fastapi import APIRouter, Depends, status, HTTPException

from api.schemas.pydantic.TokenSchema import TokenPublic, TokenNew, TokenRefresh, TokenPayload
from api.services.TokenService import TokenService

TokenRouter = APIRouter(
    prefix="/v1/token", tags=["token"]
)


@TokenRouter.post("/",
                  response_model=TokenPublic,
                  status_code=status.HTTP_201_CREATED,
                  summary="Create a new token",
                  description="Create a new token for a user with email and password"
)
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
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating token")


@TokenRouter.post("/renew",
                  response_model=TokenPublic,
                  summary="Renew a token",
                  description="Renew a token for a user with refresh token")
def renew_token(
        token_body: TokenRefresh,
        tokenService: TokenService = Depends(),
):
    try:
        return tokenService.renew_token(token_body).normalize()
    except AttributeError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="token not found")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating token")


@TokenRouter.post("/introspect",
                  response_model=TokenPayload,
                  summary="Verify a token",
                  description="Verify a token and return the payload containing user's email and scopes if valid")
def introspect_token(
        bearer_token: str,
        tokenService: TokenService = Depends(),
):
    try:
        return tokenService.introspect_token(bearer_token)
    except AttributeError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="token not found")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while checking token")


@TokenRouter.post("/revoke", response_model=TokenPublic,
                  summary="Revoke a token",
                  description="Revoke a token and return the deleted user")
def revoke_token(
        bearer_token: str,
        tokenService: TokenService = Depends(),
):
    try:
        return tokenService.revoke_token(bearer_token).normalize()
    except AttributeError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="token not found")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while checking token")