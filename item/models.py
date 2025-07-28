from sqlalchemy.orm import Mapped, mapped_column

from db import BaseModel


class Item(BaseModel):
    __tablename__ = 'item'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
