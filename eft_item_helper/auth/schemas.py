from datetime import datetime

from fastapi.security import HTTPBasicCredentials as BasicCredentials
from pydantic import BaseModel as BaseSchema


class RegisterCredentials(BasicCredentials):
    repeat_password: str


class LoginCredentials(BasicCredentials):
    pass


class SessionAuthSchema(BaseSchema):
    session_id: str
    expiry: datetime
    user_id: int
