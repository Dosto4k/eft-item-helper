from fastapi import Request, status
from fastapi.responses import JSONResponse

from eft_item_helper.auth.config import session_config
from eft_item_helper.auth.exceptions import InvalidCookieSessionError


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
