from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Response, Depends
from sqlalchemy.exc import IntegrityError

from auth.schemas import RegisterCredentials, LoginCredentials
from auth.services import (
    authenticate_user,
    create_session_auth,
    get_current_user,
    delete_session_auth_by_user_if_exists,
)
from dependencies import SessionDep
from user.services import create_user_and_add_quest_items
from user.schemas import UserSchema


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register/")
async def post_register_user(
    user_data: RegisterCredentials, session: SessionDep
) -> dict:
    """
    Endpoint для регистрации пользователя
    """
    try:
        await create_user_and_add_quest_items(user_data, session)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
        ) from e
    return {"success": True}


@router.post("/login/")
async def login_user(
    credentials: LoginCredentials,
    session: SessionDep,
    response: Response,
) -> dict:
    """
    Endpoint для аутентификации пользователя
    """
    user = await authenticate_user(credentials, session)
    session_data = await create_session_auth(user, session)
    response.set_cookie(
        key="session-auth", value=session_data.session_id, httponly=True
    )
    return {"success": True}


@router.post("/logout/")
async def logout_user(
    user: Annotated[UserSchema, Depends(get_current_user)],
    session: SessionDep,
    response: Response,
) -> dict:
    """
    Endpoint для выхода пользователя
    """
    await delete_session_auth_by_user_if_exists(user, session)
    response.delete_cookie("session-auth")
    return {"success": True}
