from collections import defaultdict
from typing import Generic, Type, Any

from eft_item_helper.forms.exceptions import (
    InvalidFieldNameError,
    FieldValueNotSpecifiedError,
)
from eft_item_helper.forms.fields import BaseField
from eft_item_helper.forms.types import (
    PydanticSchema,
    FieldsValidators,
    FieldsData,
    ErrorMessage,
)


class BaseForm(Generic[PydanticSchema]):
    pydantic_schema: Type[PydanticSchema]
    fields_validators: FieldsValidators | None = None

    def __init__(
        self,
        form_data: dict[str, Any] | None = None,
    ) -> None:
        self.non_field_errors: list[str] = []
        self.fields_errors: dict[str, list[ErrorMessage]] = defaultdict(list)
        self.fields: dict[str, BaseField] = self.get_fields()
        self.set_default_attr()
        self.form_data = None
        if form_data:
            self.form_data = form_data
            self.load_form_data(form_data)
            self.validate_fields()

    def __call__(self) -> dict[str, FieldsData | list[str]]:
        """
        Возвращает данные html формы
        """
        fields: FieldsData = []
        for field_name, field in self.fields.items():
            fields.append(
                {
                    "label": field.get_html_label(),
                    "input": field.get_html_input(),
                    "errors": self.fields_errors[field_name],
                }
            )
        form: dict[str, FieldsData | list[str]] = {
            "fields": fields,
            "non_fields_errors": self.non_field_errors,
        }
        return form

    def is_valid(self) -> bool:
        """
        Проверяет валидность формы
        """
        if self.form_data:
            return not bool(self.fields_errors)
        raise FieldValueNotSpecifiedError(
            f"The form data is not specified. "
            "Try passing the form from the request as "
            f"an argument when creating the '{self.__class__.__name__}'."
        )

    def validate_fields(self) -> None:
        """
        Валидирует поля формы указанными в 'fields_validators'
        валидаторами и записывает ошибки в self.fields_errors
        """
        if not self.fields_validators:
            return
        for fields_names, validators in self.fields_validators.items():
            fields = self.get_fields_and_values(fields_names.split("__"))
            for validator in validators:
                if err := validator(**fields):
                    self.set_fields_error(fields_names.split("__"), err)

    def load_form_data(self, form_data: dict[str, Any]) -> None:
        """
        Устанавливает атрибутам полей 'value' значения из переданных 'form_data'
        """
        for field_name, field_value in form_data.items():
            if field := self.fields.get(field_name):
                field.set_field_attr("value", field_value)

    def set_default_attr(self) -> None:
        """
        Устанавливает атрибутам полей 'id' и 'name' значение
        равное имение атрибута формы в котором хранится поле
        """
        for attr_name, field_cls in self.fields.items():
            field_cls.set_field_attr("id", attr_name)
            field_cls.set_field_attr("name", attr_name)
            field_cls.set_field_attr("autocomplete", "on")

    def get_form_data(self) -> PydanticSchema:
        """
        Возвращает значения атрибутов полей 'value' полей формы
        """
        if not self.form_data:
            raise FieldValueNotSpecifiedError(
                f"The form data is not specified. "
                "Try passing the form from the request as "
                f"an argument when creating the '{self.__class__.__name__}'."
            )
        data = {}
        for field_name, field_cls in self.fields.items():
            data[field_name] = field_cls.get_field_attr_or_none("value")
        return self.pydantic_schema(**data)

    def get_fields(self) -> dict[str, BaseField]:
        """
        Возвращает все поля формы
        """
        fields = {}
        for attr_name, attr_value in self.__class__.__dict__.items():
            if isinstance(attr_value, BaseField):
                fields[attr_name] = attr_value
        return fields

    def set_fields_error(self, fields_names: list[str], err: ErrorMessage) -> None:
        for field_name in fields_names:
            self.fields_errors[field_name].append(err)

    def get_fields_and_values(self, fields_names: list[str]) -> dict[str, str]:
        fields = {}
        for field_name in fields_names:
            field = self.get_field(field_name)
            field_value = self.get_field_value(field)
            fields[field_name] = field_value
        return fields

    def get_field(self, field_name: str) -> BaseField:
        field = self.fields.get(field_name)
        if not field:
            raise InvalidFieldNameError(
                f"Invalid field name '{field_name}'. "
                "The keys in the fields_validators dict should be the names "
                f"of the fields specified in '{self.__class__.__name__}'."
            )
        return field

    def get_field_value(self, field: BaseField) -> str:
        field_value = field.get_field_attr_or_none("value")
        if field_value is None:
            raise FieldValueNotSpecifiedError(
                f"The '{field.get_field_attr_or_none('name')}' value is not specified. "
                "Try passing the form from the request as "
                f"an argument when creating the '{self.__class__.__name__}'."
            )
        return field_value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.fields})"
