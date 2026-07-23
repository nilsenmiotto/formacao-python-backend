from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import db

if TYPE_CHECKING:
    from .role import Role


class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(120), nullable=False)
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("role.id"), nullable=True)
    role: Mapped["Role"] = relationship(back_populates="user")
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    def __repr__(self):
        return f"User(id={self.id!r}, username={self.username!r}, active={self.active})"
