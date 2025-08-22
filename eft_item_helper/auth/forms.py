from auth.schemas import LoginCredentials
from forms.forms import BaseForm
from forms.fields import TextField, PasswordField


class LoginForm(BaseForm[LoginCredentials]):
    username = TextField(label="Имя пользователя:", placeholder="SomeUser2212")
    password = PasswordField(label="Пароль:", placeholder="SecretPassword*2")

    pydantic_schema = LoginCredentials
