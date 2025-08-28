from pathlib import Path

from fastapi.templating import Jinja2Templates
from pydantic import BaseModel as BaseSchema


BASE_DIR = Path(__file__).resolve().parent


APP_MODULE = "eft_item_helper.main:app"


class TemplateConfig(BaseSchema):
    dir: Path = BASE_DIR / "templates"


class StaticConfig(BaseSchema):
    name: str = "static"
    path: str = "/static"
    dir: Path = BASE_DIR / "static"


class DataBaseConfig(BaseSchema):
    url: str = "sqlite:///eft_item_helper/database.db"
    echo: bool = True


templates = Jinja2Templates(TemplateConfig().dir)
static_config = StaticConfig()
db_config = DataBaseConfig()
