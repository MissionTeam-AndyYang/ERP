from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SQL_PATH = ROOT / "docs" / "database" / "EWDB_20260517_3.sql"
MODEL_PATH = ROOT / "backend" / "app" / "models" / "ewdb.py"
MODELS_INIT_PATH = ROOT / "backend" / "app" / "models" / "__init__.py"
MIGRATION_PATH = ROOT / "backend" / "alembic" / "versions" / "20260517_0001_ewdb_baseline.py"


TYPE_MAP = {
    "INT": ("Integer", "int"),
    "BIGINT UNSIGNED": ("BigInteger", "int"),
    "FLOAT": ("Float", "float"),
    "DOUBLE": ("Double", "float"),
    "DATE": ("Date", "date"),
    "LONGTEXT": ("Text", "str"),
}

RESERVED_ATTRS = {
    "metadata",
    "registry",
}


def pascal_case(name: str) -> str:
    return "".join(part[:1].upper() + part[1:] for part in re.split(r"[_\W]+", name) if part)


def attr_name(name: str) -> str:
    return f"{name}_" if name in RESERVED_ATTRS else name


def parse_column_type(sql_type: str) -> tuple[str, str]:
    base = re.sub(r"\s+NOT NULL.*$", "", sql_type)
    base = re.sub(r"\s+NULL.*$", "", base).strip()

    varchar = re.match(r"VARCHAR\((\d+)\)", base)
    if varchar:
        return f"String({varchar.group(1)})", "str"

    return TYPE_MAP.get(base, ("String(255)", "str"))


def strip_database_directives(sql: str) -> str:
    lines = []
    for line in sql.splitlines():
        stripped = line.strip()
        if stripped.startswith("CREATE DATABASE"):
            continue
        if stripped.startswith("USE "):
            continue
        lines.append(line)
    return "\n".join(lines).strip() + "\n"


def parse_tables(sql: str) -> dict[str, dict[str, object]]:
    tables: dict[str, dict[str, object]] = {}
    pattern = re.compile(
        r"CREATE TABLE IF NOT EXISTS `([^`]+)` \((.*?)\) ENGINE=InnoDB",
        re.DOTALL,
    )

    for match in pattern.finditer(sql):
        table_name = match.group(1)
        body = match.group(2)
        columns: dict[str, dict[str, object]] = {}
        primary_keys: set[str] = set()
        unique_keys: list[list[str]] = []

        for raw_line in body.splitlines():
            line = raw_line.strip().rstrip(",")
            col_match = re.match(r"`([^`]+)`\s+(.+)$", line)
            if col_match:
                col_name = col_match.group(1)
                columns[col_name] = {"definition": col_match.group(2)}
                continue

            pk_match = re.match(r"PRIMARY KEY\s+\((.+)\)", line)
            if pk_match:
                primary_keys.update(re.findall(r"`([^`]+)`", pk_match.group(1)))
                continue

            uk_match = re.match(r"UNIQUE KEY\s+`[^`]+`\s+\((.+)\)", line)
            if uk_match:
                unique_keys.append(re.findall(r"`([^`]+)`", uk_match.group(1)))

        tables[table_name] = {
            "columns": columns,
            "primary_keys": primary_keys,
            "unique_keys": unique_keys,
        }

    return tables


def parse_foreign_keys(sql: str) -> dict[tuple[str, str], dict[str, str]]:
    fks: dict[tuple[str, str], dict[str, str]] = {}
    pattern = re.compile(
        r"ALTER TABLE `([^`]+)` ADD CONSTRAINT `([^`]+)` "
        r"FOREIGN KEY \(`([^`]+)`\) REFERENCES `([^`]+)` \(`([^`]+)`\);"
    )
    for match in pattern.finditer(sql):
        table, constraint, column, ref_table, ref_column = match.groups()
        fks[(table, column)] = {
            "constraint": constraint,
            "ref_table": ref_table,
            "ref_column": ref_column,
        }
    return fks


def render_models(tables: dict[str, dict[str, object]], fks: dict[tuple[str, str], dict[str, str]]) -> str:
    imports = (
        "from __future__ import annotations\n\n"
        "from datetime import date\n\n"
        "from sqlalchemy import BigInteger, Date, Double, Float, ForeignKey, Integer, String, Text\n"
        "from sqlalchemy.orm import Mapped, mapped_column\n\n"
        "from app.db.base import Base\n\n\n"
    )
    classes: list[str] = []

    for table_name, table in tables.items():
        class_name = pascal_case(table_name)
        lines = [f"class {class_name}(Base):", f'    __tablename__ = "{table_name}"', ""]
        columns = table["columns"]
        primary_keys = table["primary_keys"]

        for col_name, col in columns.items():
            definition = str(col["definition"])
            sa_type, py_type = parse_column_type(definition)
            nullable = " NOT NULL" not in definition and col_name not in primary_keys
            is_pk = col_name in primary_keys
            autoincrement = "AUTO_INCREMENT" in definition
            fk = fks.get((table_name, col_name))
            mapped_args = [sa_type]
            mapped_kwargs: list[str] = []

            if fk:
                mapped_args.append(
                    f'ForeignKey("{fk["ref_table"]}.{fk["ref_column"]}", name="{fk["constraint"]}")'
                )
            if is_pk:
                mapped_kwargs.append("primary_key=True")
            if autoincrement:
                mapped_kwargs.append("autoincrement=True")
            if nullable and not is_pk:
                mapped_kwargs.append("nullable=True")
            elif not is_pk:
                mapped_kwargs.append("nullable=False")

            annotation = py_type if not nullable or is_pk else f"{py_type} | None"
            args = ", ".join(mapped_args + mapped_kwargs)
            lines.append(f"    {attr_name(col_name)}: Mapped[{annotation}] = mapped_column({args})")

        classes.append("\n".join(lines))

    return imports + "\n\n".join(classes) + "\n"


def render_migration(sql: str, table_names: list[str]) -> str:
    drop_lines = "\n".join(
        f'    op.execute("DROP TABLE IF EXISTS `{table_name}`")'
        for table_name in reversed(table_names)
    )
    return f'''"""EWDB 20260517 baseline schema.

Revision ID: 20260517_0001
Revises:
Create Date: 2026-05-17
"""

from __future__ import annotations

from alembic import op


revision = "20260517_0001"
down_revision = None
branch_labels = None
depends_on = None


BASELINE_SQL = {sql!r}


def upgrade() -> None:
    op.execute(BASELINE_SQL)


def downgrade() -> None:
    op.execute("SET FOREIGN_KEY_CHECKS = 0")
{drop_lines}
    op.execute("SET FOREIGN_KEY_CHECKS = 1")
'''


def main() -> None:
    raw_sql = SQL_PATH.read_text(encoding="utf-8")
    baseline_sql = strip_database_directives(raw_sql)
    tables = parse_tables(baseline_sql)
    fks = parse_foreign_keys(baseline_sql)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    MODEL_PATH.write_text(render_models(tables, fks), encoding="utf-8")
    MODELS_INIT_PATH.write_text("from app.models import ewdb\n\n__all__ = [\"ewdb\"]\n", encoding="utf-8")
    MIGRATION_PATH.write_text(render_migration(baseline_sql, list(tables.keys())), encoding="utf-8")

    print(f"models={MODEL_PATH.relative_to(ROOT)}")
    print(f"migration={MIGRATION_PATH.relative_to(ROOT)}")
    print(f"tables={len(tables)}")
    print(f"foreign_keys={len(fks)}")


if __name__ == "__main__":
    main()
