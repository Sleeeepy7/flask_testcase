# celery_app.py
import os
from celery import Celery

from core.config import settings

broker_url = str(settings.redis.url)
backend_url = str(settings.redis.url)

celery = Celery("flask_testcase", broker=broker_url, backend=backend_url)

celery.conf.beat_schedule = {
    "check-pending-transactions-every-minute": {
        "task": "tasks.transaction_tasks.expire_pending_transactions_task",
        "schedule": 60.0,
    },
    "check-wallet-balances": {
        "task": "tasks.wallet_tasks.check_wallet_balances",
        "schedule": 300.0,  # каждые 5 минут
    },
}
celery.conf.timezone = "UTC"

import tasks.transaction_tasks
import tasks.wallet_tasks
