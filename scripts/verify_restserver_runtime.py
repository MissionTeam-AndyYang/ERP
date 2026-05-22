"""Runtime verification for legacy restserver and EWDB.

This script is intended for engineers who have MariaDB/MySQL available locally.
It avoids printing database passwords and returns a JSON summary that can be
shared back for review.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


REQUIRED_TABLES = {
    "company",
    "payment",
    "material",
    "inproduct",
    "product",
    "trans_items",
    "quotation",
    "contract",
    "product_order",
    "purchase_request",
    "purchase_order",
    "goods_receipt_note",
    "batch_number",
    "inventory_record",
    "warehouse_record",
    "warehouse_payment",
    "aps_quantity",
    "work_order",
    "process_order",
    "process_labor",
    "production_data",
    "production_data_input",
    "production_data_output",
    "production_data_reuse",
    "production_data_machine",
    "production_data_labor",
    "shipping_order",
    "shipping_record",
    "shipping_payment",
}


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            os.environ[key] = value


def check_restserver() -> dict:
    from package.dbwrapper.table import Base
    import package.restserver.restserver as restserver

    app = restserver.g_obj_flask
    routes = sorted(str(rule) for rule in app.url_map.iter_rules())
    client = app.test_client()
    heartbeat = client.get("/heartbeat")

    return {
        "ok": heartbeat.status_code == 200,
        "orm_table_count": len(Base.metadata.tables),
        "orm_has_required_tables": sorted(
            table for table in REQUIRED_TABLES if table in Base.metadata.tables
        ),
        "orm_missing_required_tables": sorted(
            table for table in REQUIRED_TABLES if table not in Base.metadata.tables
        ),
        "blueprint_count": len(app.blueprints),
        "blueprints": sorted(app.blueprints.keys()),
        "route_count": len(routes),
        "heartbeat_status": heartbeat.status_code,
        "heartbeat_body_prefix": heartbeat.get_data(as_text=True)[:200],
    }


def check_database() -> dict:
    from sqlalchemy import create_engine, text
    from package.dbwrapper.maria import CMaria

    url = CMaria().gen_connection_str()
    safe_target = url.split("@")[-1]
    engine = create_engine(url, pool_pre_ping=True)

    with engine.connect() as conn:
        database_name = conn.execute(text("SELECT DATABASE()")).scalar()
        tables = [
            row[0]
            for row in conn.execute(
                text(
                    "SELECT table_name "
                    "FROM information_schema.tables "
                    "WHERE table_schema = DATABASE() "
                    "ORDER BY table_name"
                )
            )
        ]
        fk_count = conn.execute(
            text(
                "SELECT COUNT(*) "
                "FROM information_schema.referential_constraints "
                "WHERE constraint_schema = DATABASE()"
            )
        ).scalar()
        unique_count = conn.execute(
            text(
                "SELECT COUNT(*) "
                "FROM information_schema.table_constraints "
                "WHERE table_schema = DATABASE() "
                "AND constraint_type = 'UNIQUE'"
            )
        ).scalar()

    return {
        "ok": True,
        "target": safe_target,
        "database": database_name,
        "table_count": len(tables),
        "fk_count": int(fk_count),
        "unique_count": int(unique_count),
        "has_required_tables": sorted(table for table in REQUIRED_TABLES if table in tables),
        "missing_required_tables": sorted(table for table in REQUIRED_TABLES if table not in tables),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify restserver runtime and EWDB connection.")
    parser.add_argument(
        "--env-file",
        default="restserver/package/config/.env.example",
        help="Path to DB env file. Defaults to restserver/package/config/.env.example.",
    )
    parser.add_argument(
        "--require-db",
        action="store_true",
        help="Return non-zero if the database connection check fails.",
    )
    args = parser.parse_args()

    repo_root = Path.cwd()
    sys.path.insert(0, str(repo_root / "restserver"))
    load_env_file(repo_root / args.env_file)

    result = {
        "restserver": None,
        "database": None,
        "environment": {
            "python": sys.version.split()[0],
            "db_host": os.getenv("DB_HOST", ""),
            "db_port": os.getenv("DB_PORT", ""),
            "db_name": os.getenv("DB_NAME", ""),
            "db_user_set": bool(os.getenv("DB_USER")),
            "db_password_set": bool(os.getenv("DB_PASSWORD")),
        },
    }

    exit_code = 0

    try:
        result["restserver"] = check_restserver()
    except Exception as exc:  # pragma: no cover - diagnostic script
        result["restserver"] = {"ok": False, "error": repr(exc)}
        exit_code = 1

    try:
        result["database"] = check_database()
    except Exception as exc:  # pragma: no cover - diagnostic script
        result["database"] = {"ok": False, "error": repr(exc)}
        if args.require_db:
            exit_code = 1

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
