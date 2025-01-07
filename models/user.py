from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Float, Text, event

from typing import Optional

from . import Base
from core.config import settings


class User(Base):
    wallet_address: Mapped[str] = mapped_column(String(50), nullable=True, unique=True)  # USDT TRC20

    username: Mapped[Optional[str]] = mapped_column(String(50), unique=True, nullable=True)
    password_hash: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    balance: Mapped[float] = mapped_column(default=0.0)
    commission_rate: Mapped[float] = mapped_column(default=settings.app.default_commission_rate)  # комиссия
    webhook_url: Mapped[str] = mapped_column(Text, nullable=True)

    transactions = relationship("Transaction", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, balance={self.balance}, commission_rate={self.commission_rate})>"


@event.listens_for(User, "before_insert")
def set_default_webhook_url(mapper, connection, target):
    """Если пользователь не задал webhook_url, поставим дефолтный."""
    if not target.webhook_url:
        target.webhook_url = "http://127.0.0.1:5000/test-webhook"
