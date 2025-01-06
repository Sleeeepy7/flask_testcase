from flask import Blueprint, render_template, request, redirect, url_for
from core.database import SessionLocal
from services.transaction_service import get_dashboard_statistics
from crud.user_crud import get_all_users, create_user, delete_user
from crud.transaction_crud import update_transaction_status
from services.transaction_service import get_all_transactions

admin_bp = Blueprint("admin", __name__, template_folder="../templates/admin")


@admin_bp.route("/")
def dashboard():
    """
    Вкладка "Дашборд".
    """
    with SessionLocal() as db:
        stats = get_dashboard_statistics(db)
    return render_template(
        "dashboard.html",
        user_count=stats["user_count"],
        transaction_count=stats["transaction_count"],
        total_transactions_today=stats["total_transactions_today"],
        recent_transactions=stats["recent_transactions"],
    )


@admin_bp.route("/users", methods=["GET", "POST"])
def users():
    """
    Вкладка "Пользователи".
    """
    with SessionLocal() as db:
        if request.method == "POST":
            username = request.form.get("username")
            create_user(db, username, password_hash="default_hash")
            return redirect(url_for("admin.users"))

        users = get_all_users(db)
    return render_template("users.html", users=users)


@admin_bp.route("/users/delete/<int:user_id>", methods=["POST"])
def delete_user_view(user_id):
    """
    Удаление пользователя.
    """
    with SessionLocal() as db:
        delete_user(db, user_id)
    return redirect(url_for("admin.users"))


@admin_bp.route("/transactions", methods=["GET", "POST"])
def transactions():
    """
    Вкладка "Транзакции".
    """
    with SessionLocal() as db:
        transactions = get_all_transactions(db)
    return render_template("transactions.html", transactions=transactions)


@admin_bp.route("/transactions/update/<int:transaction_id>", methods=["POST"])
def update_transaction(transaction_id):
    """
    Обновление статуса транзакции.
    """
    new_status = request.form.get("status")
    with SessionLocal() as db:
        update_transaction_status(db, transaction_id, new_status)
    return redirect(url_for("admin.transactions"))
