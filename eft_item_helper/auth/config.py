from pydantic import BaseModel as BaseSchema


class SessionConfig(BaseSchema):
    cookie_key: str = "session"
    days_of_life: int = 14


session_config = SessionConfig()
