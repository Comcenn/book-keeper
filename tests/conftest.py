from collections.abc import Generator
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session
from pytest import fixture

from book_keeper.models import Base


DB_URL = "sqlite+pysqlite:///:memory:"


@fixture
def engine() -> Engine:
    engine = create_engine(DB_URL, echo=True)
    Base.metadata.create_all(engine)
    return engine


@fixture
def db_session(engine: Engine) -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
