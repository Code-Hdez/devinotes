from typing import Iterator

from rich.pretty import d
from sqlmodel import SQLModel, Session, create_engine

from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=True,
    connect_args=(
        {"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
    ),
)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)  # dev


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session
