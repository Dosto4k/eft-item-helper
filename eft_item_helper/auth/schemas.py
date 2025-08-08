import re
from datetime import datetime

from fastapi.security import HTTPBasicCredentials as BasicCredentials
from pydantic import BaseModel as BaseSchema, field_validator, ValidationInfo


class RegisterCredentials(BasicCredentials):
    repeat_password: str

    @field_validator("username", mode="after")
    @classmethod
    def check_username_len(cls, username: str) -> str:
        """
        Проверяет длину username
        """
        if len(username) < 3:
            raise ValueError("Username must contain at least 3 characters.")
        return username

    @field_validator("repeat_password", mode="after")
    @classmethod
    def check_passwotd_match(cls, repeat_password: str, info: ValidationInfo) -> str:
        """
        Проверяет пароли на совпадение
        """
        password = info.data.get("password")
        if not password:
            return repeat_password
        if password != repeat_password:
            raise ValueError("Password dont match")
        return repeat_password

    @field_validator("password", mode="after")
    @classmethod
    def check_password_strength(cls, password: str) -> str:
        """
        Проверяется сложность пароля
        """
        if len(password) < 12:
            raise ValueError(
                "Password is too simple it must contain at least 12 characters."
            )
        if re.search(r"\d", password) is None:
            raise ValueError("Password is too simple it must contain at least 1 digit.")
        if re.search(r"[A-Z]", password) is None:
            raise ValueError(
                "Password is too simple it must contain at least 1 uppercase letter."
            )
        if re.search(r"[a-z]", password) is None:
            raise ValueError(
                "Password is too simple it must contain at least 1 lowercase letter."
            )
        if re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~" + r'"]', password) is None:
            raise ValueError(
                "Password is too simple it must contain at least 1 special character."
            )
        return password


class LoginCredentials(BasicCredentials):
    pass


class SessionAuthSchema(BaseSchema):
    session_id: str
    expiry: datetime
    user_id: int
