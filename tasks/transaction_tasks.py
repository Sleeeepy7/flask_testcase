from datetime import datetime, timedelta

from celery_app import celery
from core.database import SessionLocal


from services.transaction_service import expire_pending_transactions


@celery.task(name="tasks.transaction_tasks.expire_pending_transactions_task")
def expire_pending_transactions_task():
    """
    Раз в n минут Celery вызывает задачу expire_pending_transactions_task:
    """
    now = datetime.utcnow()
    cutoff = now - timedelta(minutes=15)

    with SessionLocal() as db:
        expire_pending_transactions(db, cutoff)
