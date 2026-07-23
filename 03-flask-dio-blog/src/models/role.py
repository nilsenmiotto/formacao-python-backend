from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import db

if TYPE_CHECKING:
    from .user import User


class Role(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    user: Mapped[list["User"]] = relationship(back_populates="role")

    def __repr__(self):
        return f"Role(id={self.id!r}, name={self.name!r})"
