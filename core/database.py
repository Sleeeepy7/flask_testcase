from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import settings

engine = create_engine(
    str(settings.db.url),
    echo=settings.db.echo,
    future=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True,
)


def get_db_session():
    """
    Генератор сессий для работы с бд.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
