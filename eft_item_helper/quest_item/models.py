from sqlalchemy import (
    Text,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from eft_item_helper.db import BaseModel


class QuestItemDetail(BaseModel):
    __tablename__ = "quest_item_detail"

    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("item.id"), unique=True)
    total_count: Mapped[int]
    count_of_found_in_raid: Mapped[int]

    item = relationship(
        argument="Item",
        back_populates="detail",
        single_parent=True,
        uselist=False,
        cascade="all, delete-orphan",
    )


class Quest(BaseModel):
    __tablename__ = "quest"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    guide_url: Mapped[str] = mapped_column("guide_url", Text, unique=True)

    items = relationship(
        argument="QuestItemAssociation",
        back_populates="quest",
        cascade="all, delete-orphan",
    )


class QuestItemAssociation(BaseModel):
    __tablename__ = "quest_item"

    item_id: Mapped[int] = mapped_column(ForeignKey("item.id"), primary_key=True)
    quest_id: Mapped[int] = mapped_column(ForeignKey("quest.id"), primary_key=True)
    total_count: Mapped[int]
    found_in_raid: Mapped[bool]

    quest = relationship(argument="Quest", back_populates="items", uselist=False)
    item = relationship(argument="Item", back_populates="quests", uselist=False)
