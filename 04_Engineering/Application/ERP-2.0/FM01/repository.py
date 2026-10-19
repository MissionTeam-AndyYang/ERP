"""Repository boundary for the isolated FM-01 GET-only slice."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Iterable, Mapping, Protocol


RESOURCE_TABLES = {
    "legal-entities": "legal_entity",
    "companies": "company",
    "sites": "site",
    "plants": "plant",
    "warehouses": "warehouse",
    "locations": "location",
}


class ReferenceRepository(Protocol):
    def list_rows(self, table: str) -> Iterable[Mapping[str, Any]]: ...


@dataclass(frozen=True)
class InMemoryReferenceRepository:
    """Disposable synthetic fixture repository; it has no persistence."""

    rows: Mapping[str, tuple[Mapping[str, Any], ...]]

    def list_rows(self, table: str) -> Iterable[Mapping[str, Any]]:
        return self.rows.get(table, ())


class MariaDbReferenceRepository:
    """Read-only repository backed by an injected DB-API connection factory.

    The SQL identifiers are selected from a closed allowlist and every query is
    a parameter-free SELECT. The caller is responsible for supplying a
    SELECT-only database principal; this class never commits or mutates.
    """

    _columns = {
        "legal_entity": ("legal_entity_id", "legal_entity_ref", "display_name"),
        "company": ("company_id", "company_ref", "display_name", "legal_entity_id"),
        "site": ("site_id", "site_ref", "display_name", "company_id"),
        "plant": ("plant_id", "plant_ref", "display_name", "site_id"),
        "warehouse": ("warehouse_id", "warehouse_ref", "display_name", "site_id", "plant_id"),
        "location": ("location_id", "location_ref", "display_name", "warehouse_id", "parent_location_id", "location_type"),
    }
    _primary_keys = {
        "legal_entity": "legal_entity_id",
        "company": "company_id",
        "site": "site_id",
        "plant": "plant_id",
        "warehouse": "warehouse_id",
        "location": "location_id",
    }

    def __init__(self, connection_factory: Callable[[], Any]):
        self._connection_factory = connection_factory

    def list_rows(self, table: str) -> Iterable[Mapping[str, Any]]:
        if table not in self._columns:
            raise ValueError(f"table is outside the FM-01 allowlist: {table}")
        columns = self._columns[table]
        identifiers = ", ".join(f"`{column}`" for column in columns)
        order_column = self._primary_keys[table]
        query = f"SELECT {identifiers} FROM `{table}` ORDER BY `{order_column}`"
        connection = self._connection_factory()
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            if rows and isinstance(rows[0], Mapping):
                return tuple(dict(row) for row in rows)
            return tuple(dict(zip(columns, row)) for row in rows)
        finally:
            cursor.close()
            connection.close()


def synthetic_repository() -> InMemoryReferenceRepository:
    """Return a minimal six-table fixture using approved physical names."""

    return InMemoryReferenceRepository(
        rows={
            "legal_entity": (
                {"legal_entity_id": 1, "legal_entity_ref": "LE-001", "display_name": "Synthetic Legal Entity"},
            ),
            "company": (
                {"company_id": 10, "company_ref": "CO-001", "display_name": "Synthetic Company", "legal_entity_id": 1},
            ),
            "site": (
                {"site_id": 20, "site_ref": "SITE-001", "display_name": "Synthetic Site", "company_id": 10},
            ),
            "plant": (
                {"plant_id": 30, "plant_ref": "PLANT-001", "display_name": "Synthetic Plant", "site_id": 20},
            ),
            "warehouse": (
                {"warehouse_id": 40, "warehouse_ref": "WH-001", "display_name": "Synthetic Warehouse", "site_id": 20, "plant_id": 30},
            ),
            "location": (
                {"location_id": 50, "location_ref": "LOC-001", "display_name": "Synthetic Location", "warehouse_id": 40, "parent_location_id": None},
            ),
        }
    )
