from fastapi import HTTPException
from starlette import status


class BadCredentialsError(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = ("Не валидный токен",)
    headers = {"Authneticate": "Bearer"}

    def __init__(self):
        super().__init__(self.status_code, self.detail, self.headers)


class WrongUserNameOrPasswordError(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = ("Неверный логин или пароль",)
    headers = {"Authneticate": "Bearer"}

    def __init__(self):
        super().__init__(self.status_code, self.detail, self.headers)


class InactiveUserError(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = ("Пользователь деактивирован",)
    headers = {"Authneticate": "Bearer"}

    def __init__(self):
        super().__init__(self.status_code, self.detail, self.headers)


class UserAlreadyExistsError(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = ("Выберите дргое имя пользователя",)
    headers = {"Authneticate": "Bearer"}

    def __init__(self):
        super().__init__(self.status_code, self.detail, self.headers)


class NotEnoughRightsError(HTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = ("Не достаточно прав",)
    headers = {"Authneticate": "Bearer"}

    def __init__(self):
        super().__init__(self.status_code, self.detail, self.headers)


class UserNotLatinNameError(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = ("Имя пользователя должно состоять из символов латинского алфавита и/или цифр",)
    headers = {"Authneticate": "Bearer"}

    def __init__(self):
        super().__init__(self.status_code, self.detail, self.headers)