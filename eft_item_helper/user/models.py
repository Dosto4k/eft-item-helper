from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import BaseModel


class User(BaseModel):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    items = relationship(
        argument="UserItemQuestAssociation",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    session = relationship(
        argument="SessionAuth", back_populates="user", cascade="all, delete-orphan"
    )


class UserItemQuestAssociation(BaseModel):
    __tablename__ = "user_item_quest"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("item.id"), primary_key=True)
    found_in_raid: Mapped[int] = mapped_column(default=0)
    found_not_in_raid: Mapped[int] = mapped_column(default=0)

    user = relationship(argument="User", back_populates="items", uselist=False)
    item = relationship(argument="Item", back_populates="users", uselist=False)
