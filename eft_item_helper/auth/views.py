from typing import Annotated, Any

from fastapi import APIRouter, HTTPException, status, Response, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.exc import IntegrityError

from eft_item_helper.auth.config import session_config
from eft_item_helper.auth.forms import LoginForm, RegisterForm
from eft_item_helper.auth.schemas import RegisterCredentials, LoginCredentials
from eft_item_helper.auth.services import (
    authenticate_user,
    create_session_auth,
    get_current_user,
    delete_session_auth_by_user_if_exists,
)
from eft_item_helper.dependencies import SessionDep
from eft_item_helper.settings import templates
from eft_item_helper.user.schemas import UserSchema
from eft_item_helper.user.services import create_user_and_add_quest_items


router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/register/")
async def get_register_user(request: Request) -> HTMLResponse:
    """
    Get Endpoint для регистрации пользователя
    """
    form = RegisterForm()
    context = {"title": "Регистрация", "form": form()}
    return templates.TemplateResponse(request, "/auth/register.html", context)


@router.post("/register/")
async def post_register_user(
    request: Request,
    request_form_data: Annotated[RegisterCredentials, Form()],
    session: SessionDep,
) -> Response:
    """
    Post Endpoint для регистрации пользователя
    """
    form = RegisterForm(form_data=request_form_data.model_dump())
    context: dict[str, Any] = {
        "title": "Регистрация",
    }
    if form.is_valid():
        form_data = form.get_form_data()
        try:
            await create_user_and_add_quest_items(form_data, session)
        except IntegrityError:
            form.non_field_errors.append("Имя пользователя уже существует")
        else:
            return RedirectResponse(
                url="/auth/login/", status_code=status.HTTP_302_FOUND
            )
    context["form"] = form()
    return templates.TemplateResponse(request, "/auth/register.html", context)


@router.get("/login/")
async def get_login_user(request: Request) -> HTMLResponse:
    """
    Get endpoint для аутентификации пользователей
    """
    form = LoginForm()
    context = {"title": "Аутентификация", "form": form()}
    return templates.TemplateResponse(request, "/auth/login.html", context)


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
    return templates.TemplateResponse(request, "/auth/login.html", context)


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
