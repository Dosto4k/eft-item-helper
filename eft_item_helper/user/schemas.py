from fastapi.security import HTTPBasicCredentials


class UserSchema(HTTPBasicCredentials):
    id: int
    username: str
    password: str
