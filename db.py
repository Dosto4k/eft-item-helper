from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase


engine = create_engine('sqlite:///database.db', echo=True)


class BaseModel(DeclarativeBase):
    pass


def create_all_table() -> None:
    BaseModel.metadata.create_all(engine)
