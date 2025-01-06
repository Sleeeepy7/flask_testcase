from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Float, Enum
from . import Base
import enum


class TransactionStatus(enum.Enum):
    PENDING = "pending"  # Ожидание
    CONFIRMED = "confirmed"  # Подтверждена
    CANCELLED = "cancelled"  # Отменена
    EXPIRED = "expired"  # Истекла


class Transaction(Base):
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    commission: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[TransactionStatus] = mapped_column(Enum(TransactionStatus), default=TransactionStatus.PENDING)  # статус

    def __repr__(self):
        return f"<Transaction(id={self.id}, amount={self.amount}, commission={self.commission}, status={self.status})>"
