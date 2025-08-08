import uuid
from datetime import datetime, timedelta, timezone

import bcrypt


async def get_pw_hash(password: str) -> str:
    """
    Получает hash пароля
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


async def verify_pw(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет совпадение паролей
    """
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


async def generate_session_id() -> str:
    """
    Генерирует session_id
    """
    return uuid.uuid4().hex


async def get_session_expiry() -> datetime:
    """
    Получает время окончания жизни сессии
    """
    return datetime.now(timezone.utc) + timedelta(days=14)
