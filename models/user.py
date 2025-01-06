from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float, Text

from typing import Optional

from . import Base
from core.config import settings


class User(Base):
    username: Mapped[Optional[str]] = mapped_column(String(50), unique=True, nullable=True)
    password_hash: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    balance: Mapped[float] = mapped_column(default=0.0)
    commission_rate: Mapped[float] = mapped_column(default=settings.app.default_commission_rate)  # комиссия
    webhook_url: Mapped[str] = mapped_column(Text, nullable=True)

    def __repr__(self):
        return f"<User(id={self.id}, balance={self.balance}, commission_rate={self.commission_rate})>"
