import bcrypt


async def get_pw_hash(password: str) -> str:
    """
    Получает hash пароля
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
