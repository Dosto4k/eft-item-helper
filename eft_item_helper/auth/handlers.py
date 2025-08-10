from fastapi import Request, status
from fastapi.responses import JSONResponse

from auth.exceptions import InvalidCookieSessionError
from auth.config import session_config


async def invalid_cookie_session_handler(
    request: Request,  # noqa
    exc: InvalidCookieSessionError,  # noqa
) -> JSONResponse:
    response = JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": "Not authenticated"},
    )
    response.delete_cookie(session_config.cookie_key)
    return response
