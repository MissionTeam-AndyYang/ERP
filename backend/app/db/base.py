from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Import model modules so Alembic can discover metadata for autogeneration.
from app.models import ewdb  # noqa: E402,F401
