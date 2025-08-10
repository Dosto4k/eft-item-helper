from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import BaseModel


class Item(BaseModel):
    __tablename__ = "item"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    detail = relationship(
        argument="QuestItemDetail",
        back_populates="item",
        uselist=False,
        cascade="all, delete-orphan",
    )
    quests = relationship(
        argument="QuestItemAssociation",
        back_populates="item",
        cascade="all, delete-orphan",
    )
    users = relationship(
        argument="UserItemQuestAssociation",
        back_populates="item",
        cascade="all, delete-orphan",
    )
