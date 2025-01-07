from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, TextAreaField
from wtforms.validators import DataRequired, Optional


class UserForm(FlaskForm):
    username = StringField("Имя пользователя", validators=[DataRequired()])
    password_hash = StringField("Хеш пароля", validators=[Optional()])
    balance = FloatField("Баланс", validators=[Optional()])
    commission_rate = FloatField("Комиссия", validators=[Optional()])
    wallet_address = StringField("USDT Wallet Address", validators=[Optional()], description="usdt trc20 address!")
    webhook_url = TextAreaField(
        "Webhook URL", validators=[Optional()], description="Не заполнять, устанавливается по дефолту"
    )  # оставил поле для редактирования на случай кастомного решения
