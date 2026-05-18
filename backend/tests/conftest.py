from collections.abc import Generator

import pytest
from sqlalchemy import create_engine, event, func, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base


def assign_sqlite_bigint_ids(session: Session) -> None:
    for obj in session.new:
        if not hasattr(obj, "id") or getattr(obj, "id") is not None:
            continue

        model = type(obj)
        max_id = session.scalar(select(func.max(model.id))) or 0
        setattr(obj, "id", max_id + 1)


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    testing_session = sessionmaker(bind=engine)
    event.listen(
        testing_session, "before_flush", lambda session, *_: assign_sqlite_bigint_ids(session)
    )
    db = testing_session()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(engine)
