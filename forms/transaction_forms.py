from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField
from wtforms.validators import DataRequired


class TransactionForm(FlaskForm):
    # amount = FloatField("Сумма", validators=[DataRequired()])
    # commission = FloatField("Комиссия", validators=[DataRequired()])
    status = SelectField(
        "Статус",
        choices=[
            ("PENDING", "Ожидание"),
            ("CONFIRMED", "Подтверждена"),
            ("CANCELLED", "Отменена"),
            ("EXPIRED", "Истекла"),
        ],
        validators=[DataRequired()],
    )
