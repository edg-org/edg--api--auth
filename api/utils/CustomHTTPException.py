from typing import Dict, Any

from fastapi import HTTPException, status


class BaseHttpException(HTTPException):
    status_code: int = None
    detail: str = None
    headers: Dict[str, Any] = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail, headers=self.headers)


class InexistentTokenException(BaseHttpException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Inexistent token"


class NotFountException(BaseHttpException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Not found"


class InternalServerErrorException(BaseHttpException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Internal server error"


class EmailOrPasswordInvalidException(BaseHttpException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Invalid email or password"


class InexistentUserException(BaseHttpException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Inexistent user"


class InvalidRefreshTokenException(BaseHttpException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Invalid refresh token"


class InvalidBearerTokenException(BaseHttpException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Invalid bearer token"


class InexistentRoleException(BaseHttpException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Inexistent role"


class InexistentPermissionException(BaseHttpException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Inexistent permission"


class AlreadyExistsUserException(BaseHttpException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "User already exists"