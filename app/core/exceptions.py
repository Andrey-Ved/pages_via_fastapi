from fastapi import HTTPException, status


class UserExampleException(HTTPException):
    status_code = 400
    detail = ""

    def __init__(self):
        super().__init__(
            status_code=self.status_code,
            detail=self.detail,
        )


class UserIdAbsentException(UserExampleException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "User id is missing"


class UserIsNotPresentException(UserExampleException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "User not present"


class UserAlreadyExistsException(UserExampleException):
    status_code = status.HTTP_409_CONFLICT
    detail = "User already exists"


print('init exception')
