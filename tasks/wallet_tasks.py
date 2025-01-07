from celery_app import celery
from core.database import SessionLocal
from models.user import User
from services.wallet_service import get_usdt_balance


@celery.task(name="tasks.wallet_tasks.check_wallet_balances")
def check_wallet_balances():
    """
    Проверяет баланс всех кошельков пользователей, разделяя на подзадачи.
    """
    with SessionLocal() as db:
        users = db.query(User).filter(User.wallet_address.isnot(None)).all()
        for user in users:
            check_user_balance.delay(user.id)


@celery.task(name="tasks.wallet_tasks.check_user_balance")
def check_user_balance(user_id):
    """
    Проверяет баланс одного пользователя.
    """
    with SessionLocal() as db:
        user = db.query(User).get(user_id)
        if not user or not user.wallet_address:
            return

        balance = get_usdt_balance(user.wallet_address)
        print(f"User ID: {user.id}, Wallet: {user.wallet_address}, Balance: {balance}")
