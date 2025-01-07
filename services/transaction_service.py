from datetime import datetime


import requests
from sqlalchemy.orm import Session

from crud.user_crud import get_all_users
from crud.transaction_crud import get_all_transactions, get_recent_transactions

from core.config import settings

from models.transaction import Transaction, TransactionStatus
from models.user import User


def get_dashboard_statistics(db: Session):
    """
    Получить статистику для дашборда.
    """
    user_count = get_all_users(db).count()

    transaction_count = get_all_transactions(db).count()

    # сумма транзакций за сегодня
    today = datetime.now().date()
    total_transactions_today = (
        db.query(Transaction).filter(Transaction.created_at >= today).count()
    )  # TODO: добавить фильтр по статусу

    # последние 5 транзакций
    recent_transactions = get_recent_transactions(db, limit=5)

    return {
        "user_count": user_count,
        "transaction_count": transaction_count,
        "total_transactions_today": total_transactions_today,
        "recent_transactions": recent_transactions,
    }


def calculate_commission(amount: float, user_commission_rate: float) -> float:
    rate = user_commission_rate if user_commission_rate > 0 else settings.app.default_commission_rate
    return round(amount * rate, 2)


def create_transaction(db: Session, user_id: int, amount: float) -> Transaction:
    """
    Создать транзакцию с расчетом комиссии.
    """
    user = db.query(User).get(user_id)
    if not user:
        raise ValueError("Пользователь не найден.")

    commission = calculate_commission(amount, user.commission_rate)

    transaction = Transaction(
        user_id=user_id,
        amount=amount,
        commission=commission,
        status=TransactionStatus.PENDING,
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


def cancel_transaction(db: Session, transaction_id: int) -> Transaction:
    """
    Отменить транзакцию
    """
    transaction = db.query(Transaction).get(transaction_id)
    if not transaction:
        raise ValueError("Транзакция не найдена.")
    if transaction.status == TransactionStatus.CANCELLED:
        raise ValueError("Транзакция уже отменена.")
    elif transaction.status != TransactionStatus.PENDING:
        raise ValueError("Транзакцию можно отменить только в статусе 'Ожидание'.")  # опять же нету явности, частных случаев
    transaction.status = TransactionStatus.CANCELLED
    db.commit()
    db.refresh(transaction)
    return transaction


def get_transaction_by_id(db: Session, transaction_id: int) -> Transaction:
    """
    Получить транзакцию по ID.
    """
    transaction = db.query(Transaction).get(transaction_id)
    if not transaction:
        raise ValueError("Транзакция не найдена.")
    return transaction


def get_transactions_desc(db: Session):
    """
    Возвращает все транзакции, отсортированные по desc id.
    """
    return db.query(Transaction).order_by(Transaction.id.desc()).all()


def get_pending_expired_transactions(db: Session, cutoff: datetime):
    """
    Найти транзакции в статусе PENDING, у которых created_at < cutoff.
    """
    return (
        db.query(Transaction)
        .filter(
            Transaction.status == TransactionStatus.PENDING,
            Transaction.created_at < cutoff,
        )
        .all()
    )


def send_webhook_if_needed(db: Session, tx: Transaction):
    """
    Отправить данные на вебхук, если у пользователя есть webhook_url.
    """
    user = db.query(User).get(tx.user_id)
    if user and user.webhook_url:
        try:
            payload = {"transaction_id": tx.id, "status": "expired"}
            response = requests.post(
                user.webhook_url.replace("127.0.0.1", "web"), json=payload, timeout=5
            )  # заглушка внутри докера на replace локалхост на web (dev)
            print(response.status_code)  # debug
        except requests.RequestException as e:
            print("Ошибка при отправке webhook:", e)


def expire_pending_transactions(db: Session, cutoff: datetime):
    pending = get_pending_expired_transactions(db, cutoff)
    if not pending:
        return

    pending_ids = [tx.id for tx in pending]

    db.query(Transaction).filter(Transaction.id.in_(pending_ids)).update(
        {Transaction.status: TransactionStatus.EXPIRED}, synchronize_session=False
    )
    db.commit()

    for tx in pending:
        tx.status = TransactionStatus.EXPIRED
        send_webhook_if_needed(db, tx)
