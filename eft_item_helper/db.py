from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session

from eft_item_helper.settings import db_config


engine = create_engine(**db_config.model_dump())


class BaseModel(DeclarativeBase):
    pass


def create_all_table() -> None:
    BaseModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
