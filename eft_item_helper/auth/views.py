from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError

from auth.schemas import RegisterCredentials
from dependencies import SessionDep
from user.services import create_user_and_add_quest_items


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
