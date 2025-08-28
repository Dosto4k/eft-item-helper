from auth.schemas import LoginCredentials, RegisterCredentials
from forms.forms import BaseForm
from forms.fields import TextField, PasswordField
from auth import validators


class LoginForm(BaseForm[LoginCredentials]):
    username = TextField(label="Имя пользователя:", placeholder="SomeUser2212")
    password = PasswordField(label="Пароль:", placeholder="SecretPassword*2")

    pydantic_schema = LoginCredentials


class RegisterForm(BaseForm[RegisterCredentials]):
    username = TextField(label="Имя пользователя:", placeholder="SomeUser2212")
    password = PasswordField(label="Пароль:", placeholder="SecretPassword*2")
    repeat_password = PasswordField(
        label="Повтор пароля:", placeholder="SecretPassword*2"
    )

    pydantic_schema = RegisterCredentials
    fields_validators = {
        "username": [
            validators.check_username_len,
        ],
        "password": [
            validators.check_password_len,
            validators.check_password_contain_digit,
            validators.check_password_contain_uppercase,
            validators.check_password_contain_lowercase,
        ],
        "password__repeat_password": [
            validators.check_password_match,
        ],
    }
