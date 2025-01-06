import click
import bcrypt
from core.database import SessionLocal
from crud.user_crud import create_user, get_user_by_username


@click.command("create-admin")
@click.option("--username", prompt=True, help="Логин")
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True, help="Пароль")
def create_admin(username, password):
    """
    Создаёт администратора.
    """
    with SessionLocal() as db:
        existing = get_user_by_username(db, username)
        if existing:
            click.echo("Суперпользователь с таким именем уже существует.")
            return

        # Хэшируем пароль
        hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        create_user(db, username, hashed_pw.decode("utf-8"))
        click.echo("Суперпользователь успешно создан.")
