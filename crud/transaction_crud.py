from sqlalchemy.orm import Session
from models.transaction import Transaction


def get_all_transactions(db: Session):
    """
    Получить все транзакции.
    """
    return db.query(Transaction)


def get_recent_transactions(db: Session, limit: int):
    """
    Получить последние транзакции.
    """
    return db.query(Transaction).order_by(Transaction.created_at.desc()).limit(limit)


def update_transaction_status(db: Session, transaction_id: int, new_status: str):
    """
    Обновить статус транзакции.
    """
    transaction = db.query(Transaction).get(transaction_id)
    if transaction:
        transaction.status = new_status
        db.commit()
        db.refresh(transaction)
    return transaction
