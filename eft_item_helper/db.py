from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session


engine = create_engine("sqlite:///database.db", echo=True)


class BaseModel(DeclarativeBase):
    pass


def create_all_table() -> None:
    BaseModel.metadata.create_all(engine)


def get_session() -> Generator[Session]:
    with Session(engine) as session:
        yield session
