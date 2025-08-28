import re


def check_username_len(username: str) -> str | None:
    """
    Проверяет длину username
    """
    if len(username) < 3:
        return "Имя пользователя должно содержать минимум 3 символа"
    return None


def check_password_match(password: str, repeat_password: str) -> str | None:
    """
    Проверяет пароли на совпадение
    """
    if password != repeat_password:
        return "Пароли не совпадают"
    return None


def check_password_len(password: str) -> str | None:
    """
    Проверяет длину password
    """
    if len(password) < 12:
        return "Пароль должен содержать минимум 12 символов"
    return None


def check_password_contain_digit(password: str) -> str | None:
    """
    Проверяет содержит ли password цифры
    """
    if re.search(r"\d", password) is None:
        return "Пароль должен содержать минимум 1 цифру"
    return None


def check_password_contain_uppercase(password: str) -> str | None:
    """
    Проверяет содержит ли password буквы в верхнем регистре
    """
    if re.search(r"[A-Z]", password) is None:
        return "Пароль должен содержать минимум 1 букву в верхнем регистре"
    return None


def check_password_contain_lowercase(password: str) -> str | None:
    """
    Проверяет содержит ли password буквы в нижнем регистре
    """
    if re.search(r"[a-z]", password) is None:
        return "Пароль должен содержать минимум 1 букву в нижнем регистре"
    return None
