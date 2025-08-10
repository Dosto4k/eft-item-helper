from typing import Annotated
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Request, Depends

from auth.schemas import LoginCredentials, SessionAuthSchema
from auth.models import SessionAuth
from auth.utils import verify_pw, generate_session_id, get_session_expiry
from auth.config import session_config
from auth.exceptions import InvalidCookieSessionError
from user.schemas import UserSchema
from user.services import get_user_or_none
from user.models import User
from dependencies import SessionDep


async def authenticate_user(
    credentials: LoginCredentials, session: Session
) -> UserSchema:
    """
    Аутентифицирует пользователя
    """
    auth_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Username or Password",
    )
    user = await get_user_or_none(credentials.username, session)
    if not user:
        raise auth_exc
    if not await verify_pw(credentials.password, user.password):
        raise auth_exc
    return user


async def create_session_auth(user: UserSchema, session: Session) -> SessionAuthSchema:
    """
    Создаёт сессию для аутентифицированного пользователя
    """
    session_auth = session.execute(
        select(SessionAuth).where(SessionAuth.user_id == user.id)
    ).scalar_one_or_none()
    if session_auth:
        session_auth.session_id = await generate_session_id()
        session_auth.expiry = await get_session_expiry()
    else:
        session_auth = SessionAuth(
            session_id=await generate_session_id(),
            user_id=user.id,
            expiry=await get_session_expiry(),
        )
    session.add(session_auth)
    session.commit()
    session.refresh(session_auth)
    return SessionAuthSchema.model_validate(session_auth, from_attributes=True)


async def get_cookie_session_auth(
    request: Request, session: SessionDep
) -> SessionAuthSchema:
    """
    Получает информацию о текущей сессии по cookie
    """
    session_id = request.cookies.get(session_config.cookie_key)
    exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
    )
    if not session_id:
        raise exc
    session_obj = session.execute(
        select(SessionAuth).where(SessionAuth.session_id == session_id)
    ).scalar_one_or_none()
    if not session_obj:
        raise InvalidCookieSessionError
    if session_obj.expiry.timestamp() <= datetime.now(timezone.utc).timestamp():
        raise InvalidCookieSessionError
    return SessionAuthSchema.model_validate(session_obj, from_attributes=True)


async def get_current_user(
    session_auth: Annotated[SessionAuthSchema, Depends(get_cookie_session_auth)],
    db_session: SessionDep,
) -> UserSchema:
    """
    Получает текущего пользователя
    """
    return UserSchema.model_validate(
        db_session.get(User, session_auth.user_id),
        from_attributes=True,
    )


async def delete_session_auth_by_user_if_exists(
    user: UserSchema, session: Session
) -> None:
    """
    Удаляет текущую сессию из бд если она существует
    """
    session_auth = session.execute(
        select(SessionAuth).where(SessionAuth.user_id == user.id)
    ).scalar_one_or_none()
    if session_auth:
        session.delete(session_auth)
        session.commit()
