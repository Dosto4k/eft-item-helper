class BaseField:
    field_type: str

    def __init__(self, label: str, **field_attrs: str) -> None:
        self.label = label
        self.field_attrs = field_attrs
        self.set_field_attr("type", self.field_type)

    def get_field_attr_or_none(self, attr_name: str) -> str | None:
        """
        Возвращает атрибут поля с указанным именем или None
        """
        return self.field_attrs.get(attr_name)

    def set_field_attr(self, attr_name: str, attr_value: str) -> None:
        """
        Устанавливает атрибуту поля 'attr_name' значение 'attr_value'
        """
        self.field_attrs[attr_name] = attr_value

    def get_html_attrs(self) -> str:
        """
        Возвращает атрибуты поля для html
        """
        html_attrs = []
        for attr_name, attr_value in self.field_attrs.items():
            html_attrs.append(f'{attr_name}="{attr_value}"')
        return " ".join(html_attrs)

    def get_html_label(self) -> str:
        """
        Возвращает html label поля
        """
        return f'<label for="{self.get_field_attr_or_none("id")}">{self.label}</label>'

    def get_html_input(self) -> str:
        """
        Возвращает html input поля
        """
        return f"<input {self.get_html_attrs()}>"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.field_attrs})"


class TextField(BaseField):
    field_type = "text"


class PasswordField(BaseField):
    field_type = "password"
