from flask import request, flash, redirect, jsonify
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView

# Импорты из вашего проекта
from core.database import SessionLocal
from services.transaction_service import get_dashboard_statistics, get_transactions_desc
from models.user import User
from models.transaction import Transaction, TransactionStatus

from forms.user_forms import UserForm
from forms.transaction_forms import TransactionForm


class MyAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        with SessionLocal() as db:
            stats = get_dashboard_statistics(db)

        return self.render(
            "admin/dashboard.html",
            user_count=stats["user_count"],
            transaction_count=stats["transaction_count"],
            total_transactions_today=stats["total_transactions_today"],
            recent_transactions=stats["recent_transactions"],
        )


class UserModelView(ModelView):
    """
    Управление пользователями:
      - Создание
      - Просмотр
      - Редактирование
      - Удаление
    """

    column_list = ("id", "username", "wallet_address", "balance", "commission_rate", "webhook_url")

    form = UserForm

    column_labels = {
        "id": "ID",
        "username": "Имя пользователя",
        "wallet_address": "USDT TRC20 Address",
        "balance": "Баланс",
        "commission_rate": "Комиссия",
        "webhook_url": "Webhook URL",
        "password_hash": "Хеш пароля",
    }


class TransactionModelView(ModelView):
    column_list = ("id", "user_id", "amount", "commission", "status", "created_at")

    column_default_sort = ("id", True)
    can_view_details = False

    list_template = "admin/transaction_list.html"

    form = TransactionForm

    column_filters = ("user_id", "status")

    column_labels = {
        "id": "ID",
        "user_id": "ID пользователя",
        "user": "Пользователь",
        "amount": "Сумма",
        "commission": "Комиссия",
        "status": "Статус",
        "created_at": "Создано",
    }

    @expose("/json_list")
    def json_list(self):
        transactions = get_transactions_desc(self.session)

        items = []
        for tx in transactions:
            items.append(
                {
                    "id": tx.id,
                    "user_id": tx.user_id,
                    "amount": tx.amount,
                    "commission": tx.commission,
                    "status": str(tx.status),
                    "created_at": str(tx.created_at),
                }
            )

        return jsonify(items)

    @expose("/details/<int:pk>", methods=["GET", "POST"])
    def details_view(self, pk):
        """
        Детальная страница: показ info + форма для смены status, если статус 'отправка'.
        """
        tx = self.session.query(Transaction).get(pk)
        if not tx:
            flash("Транзакция не найдена.", "error")
            return redirect(self.get_url(".index_view"))

        form = TransactionForm(obj=tx)

        if request.method == "POST":
            if form.validate_on_submit():
                if tx.status == TransactionStatus.PENDING:
                    form.populate_obj(tx)
                    self.session.commit()
                    flash("Изменения сохранены.", "success")
                else:
                    flash("Статус нельзя менять, т.к. не Ожидание.", "warning")

                return redirect(self.get_url(".details_view", pk=pk))
            else:
                flash("Проверьте введённые данные.", "error")

        return self.render("admin/transaction_details.html", details=tx, form=form)


admin = Admin(
    name="Админка",
    index_view=MyAdminIndexView(),
    template_mode="bootstrap4",
)

admin.add_view(UserModelView(User, SessionLocal(), name="Пользователи"))
admin.add_view(TransactionModelView(Transaction, SessionLocal(), name="Транзакции"))
