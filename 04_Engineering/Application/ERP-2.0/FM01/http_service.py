"""Loopback-only WSGI service entrypoint for the isolated FM-01 surface."""

from __future__ import annotations

import os

from werkzeug.serving import make_server

from .api import create_app
from .repository import MariaDbReferenceRepository


def _repository_from_environment() -> MariaDbReferenceRepository:
    import pymysql

    return MariaDbReferenceRepository(
        lambda: pymysql.connect(
            host=os.environ["FM01_STAGE4_DB_HOST"],
            port=int(os.environ["FM01_STAGE4_DB_PORT"]),
            user=os.environ["FM01_STAGE4_DB_USER"],
            password=os.environ["FM01_STAGE4_DB_PASSWORD"],
            database=os.environ["FM01_STAGE4_DB_NAME"],
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True,
            ssl_disabled=True,
        )
    )


def create_service():
    """Build the real HTTP application using the SELECT-only repository."""

    return create_app(_repository_from_environment())


def serve_forever() -> None:
    host = os.environ.get("FM01_STAGE4_HTTP_HOST", "127.0.0.1")
    port = int(os.environ.get("FM01_STAGE4_HTTP_PORT", "8087"))
    server = make_server(host, port, create_service())
    server.serve_forever()


if __name__ == "__main__":
    serve_forever()
