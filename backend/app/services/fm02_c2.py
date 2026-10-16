"""Main-backend integration boundary for the approved FM02 C2 service.

The C2 rules remain in the isolated service source under
``04_Engineering/Application/ERP-2.0/restserver/package/fm02_c2``.  This
module adapts the main Flask application's SQLAlchemy session to the narrow
DB-API connection contract that service uses.  The adapter deliberately does
not create or close a database connection; request lifecycle ownership stays
with ``app.api.v1.utils`` and the application's teardown hook.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session


def _load_approved_c2_service():
    """Load the approved C2 implementation from this repository.

    The isolated service is intentionally retained as the single source of
    C2 validation and transaction rules.  The main backend is packaged from
    ``backend/`` only, so the repository-local package path is added lazily
    when this integration boundary is imported.
    """

    package_root = (
        Path(__file__).resolve().parents[3]
        / "04_Engineering"
        / "Application"
        / "ERP-2.0"
        / "restserver"
        / "package"
    )
    package_root_text = str(package_root)
    if package_root_text not in sys.path:
        sys.path.insert(0, package_root_text)

    from fm02_c2.service import C2Service  # noqa: PLC0415

    return C2Service


C2Service = _load_approved_c2_service()


class _SessionCursor:
    """Small DB-API cursor facade backed by SQLAlchemy's session connection."""

    def __init__(self, session: Session):
        self._session = session
        self._result: Any | None = None
        self.description: list[tuple[str]] = []

    def __enter__(self) -> _SessionCursor:
        return self

    def __exit__(self, *_: Any) -> bool:
        if self._result is not None:
            self._result.close()
        return False

    def execute(self, sql: str, params: tuple[Any, ...] = ()) -> None:
        self._result = self._session.connection().exec_driver_sql(sql, params)
        self.description = [(key,) for key in self._result.keys()]

    def fetchone(self) -> Any:
        if self._result is None:
            raise RuntimeError("execute must be called before fetchone")
        return self._result.fetchone()

    def fetchall(self) -> list[Any]:
        if self._result is None:
            raise RuntimeError("execute must be called before fetchall")
        return list(self._result.fetchall())


class SessionConnectionBoundary:
    """Expose the C2 connection contract without taking session ownership."""

    def __init__(self, session: Session):
        self.session = session

    def cursor(self) -> _SessionCursor:
        return _SessionCursor(self.session)

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()

    def close(self) -> None:
        """Leave request-scoped session close to the main application's teardown."""


def build_c2_service(session: Session) -> C2Service:
    """Build C2 with the current request's session boundary."""

    return C2Service(lambda: SessionConnectionBoundary(session))
