from typing import Annotated, Any

from fastapi import APIRouter, HTTPException, status, Response, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.exc import IntegrityError

from auth.schemas import RegisterCredentials, LoginCredentials
from auth.services import (
    authenticate_user,
    create_session_auth,
    get_current_user,
    delete_session_auth_by_user_if_exists,
)
from auth.config import session_config
from auth.forms import LoginForm
from dependencies import SessionDep
from user.services import create_user_and_add_quest_items
from user.schemas import UserSchema
import settings


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


@router.get("/login/")
async def get_login_user(request: Request) -> HTMLResponse:
    """
    Get endpoint для аутентификации пользователей
    """
    form = LoginForm()
    context = {"title": "Аутентификация", "form": form()}
    return settings.TEMPLATES.TemplateResponse(request, "/auth/login.html", context)


@router.post("/login/")
async def post_login_user(
    request: Request,
    request_form_data: Annotated[LoginCredentials, Form()],
    session: SessionDep,
) -> Response:
    """
    Post endpoint для аутентификации пользователей
    """
    form = LoginForm(form_data=request_form_data.model_dump())
    context: dict[str, Any] = {
        "title": "Аутентификация",
    }
    if form.is_valid():
        form_data = form.get_form_data()
        try:
            user = await authenticate_user(form_data, session)
        except HTTPException as err:
            form.non_field_errors.append(err.detail)
        else:
            session_data = await create_session_auth(user, session)
            response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
            response.set_cookie(
                key=session_config.cookie_key,
                value=session_data.session_id,
                httponly=True,
            )
            return response
    context["form"] = form()
    return settings.TEMPLATES.TemplateResponse(request, "/auth/login.html", context)


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
    response.delete_cookie(key=session_config.cookie_key)
    return {"success": True}
