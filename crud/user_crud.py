from typing import Union

from sqlalchemy.orm import Session

from models.user import User


def get_user_by_username(db: Session, username: str) -> Union[User, None]:
    """
    Получить пользователя по имени пользователя.
    """
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, username: str, password_hash: str) -> User:
    """
    Создать нового пользователя с указанным именем пользователя и хэшем пароля.
    """
    user = User(username=username, password_hash=password_hash)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_all_users(db: Session):
    """
    Получить всех пользователей.
    """
    return db.query(User)


def delete_user(db: Session, user_id: int) -> None:
    """
    Удалить пользователя по ID.
    """
    user = db.get(User, user_id)
    if user:
        db.delete(user)
        db.commit()
