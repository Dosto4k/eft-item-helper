from pathlib import Path

from fastapi.templating import Jinja2Templates


BASE_DIR = Path(__file__).resolve().parent

TEMPLATE_DIRS = [
    BASE_DIR / "templates",
]

TEMPLATES = Jinja2Templates(TEMPLATE_DIRS)
