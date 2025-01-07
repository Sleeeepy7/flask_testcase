from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Float, Enum, DateTime, ForeignKey, Integer
from sqlalchemy.sql import func

from . import Base
import enum


class TransactionStatus(enum.Enum):
    PENDING = "pending"  # Ожидание
    CONFIRMED = "confirmed"  # Подтверждена
    CANCELLED = "cancelled"  # Отменена
    EXPIRED = "expired"  # Истекла

    def __str__(self):
        translations = {"pending": "Ожидание", "confirmed": "Подтверждена", "cancelled": "Отменена", "expired": "Истекла"}
        return translations[self.value]

    def __repr__(self):
        return str(self)


class Transaction(Base):
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    commission: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[TransactionStatus] = mapped_column(Enum(TransactionStatus), default=TransactionStatus.PENDING)  # статус
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="transactions")

    def __repr__(self):
        return f"<Transaction(id={self.id}, amount={self.amount}, commission={self.commission}, status={self.status})>"
