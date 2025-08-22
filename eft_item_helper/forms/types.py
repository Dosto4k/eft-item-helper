from typing import TypeAlias, TypeVar
from collections.abc import Callable

from pydantic import BaseModel as BaseSchema


PydanticSchema = TypeVar("PydanticSchema", bound=BaseSchema)

FieldsData: TypeAlias = list[dict[str, str | list[str]]]
ErrorMessage: TypeAlias = str
Validator: TypeAlias = Callable[..., ErrorMessage | None]
FieldsValidators: TypeAlias = dict[str, list[Validator]]
