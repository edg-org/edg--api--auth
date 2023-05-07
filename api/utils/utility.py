from fastapi import status

from api.schemas.pydantic.core import InexistentTokenExceptionSchema, ExpiredTokenExceptionSchema, \
    NotFoundExceptionSchema, InternalServerErrorExceptionSchema

APIRouter_responses = {
    status.HTTP_401_UNAUTHORIZED: {"description": "The token is not existent",
                                   "model": InexistentTokenExceptionSchema},
    status.HTTP_403_FORBIDDEN: {"description": "Invalid token or Expired token",
                                "model": ExpiredTokenExceptionSchema},
    status.HTTP_404_NOT_FOUND: {"description": "Item not found",
                                "model": NotFoundExceptionSchema},
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error",
                                            "model": InternalServerErrorExceptionSchema}
}