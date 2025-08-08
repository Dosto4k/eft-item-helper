from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import BaseModel


class SessionAuth(BaseModel):
    __tablename__ = "session_auth"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), unique=True)
    expiry: Mapped[datetime]

    user = relationship(argument="User", back_populates="session")
