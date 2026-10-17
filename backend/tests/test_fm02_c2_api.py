from __future__ import annotations

from typing import Any

import pytest

from app.main import app


class StubC2Service:
    def __init__(self) -> None:
        self.calls: list[tuple[str, tuple[Any, ...]]] = []

    def create_customer_qualification(
        self, item_id: str, payload: dict[str, Any], correlation_id: str | None
    ) -> dict[str, Any]:
        self.calls.append(("customer", (item_id, payload, correlation_id)))
        return {"ok": True, "status": 201, "customer_qualification": {"item_id": item_id}}

    def create_conversion_rule(
        self, item_id: str, payload: dict[str, Any], correlation_id: str | None
    ) -> dict[str, Any]:
        self.calls.append(("create_conversion", (item_id, payload, correlation_id)))
        return {"ok": True, "status": 201, "conversion_rule": {"item_id": item_id}}

    def resolve_conversion(
        self,
        item_id: str,
        from_item_uom_id: str,
        to_item_uom_id: str,
        effective_at: str | None,
    ) -> dict[str, Any]:
        self.calls.append(
            ("resolve_conversion", (item_id, from_item_uom_id, to_item_uom_id, effective_at))
        )
        return {
            "ok": False,
            "status": 404,
            "errors": [
                {
                    "field": "conversion",
                    "message": "no active Item-specific conversion rule exists",
                }
            ],
        }


@pytest.fixture()
def c2_client():
    service = StubC2Service()
    app.config["FM02_C2_SERVICE"] = service
    with app.test_client() as client:
        yield client, service
    app.config.pop("FM02_C2_SERVICE", None)


def test_main_app_registers_customer_qualification_route(c2_client) -> None:
    client, service = c2_client

    response = client.post(
        "/api/v1/fm02/items/ITEM-1/customer-qualifications",
        json={"customer_ref": "CUSTOMER-A"},
        headers={"X-Correlation-ID": "corr-1"},
    )

    assert response.status_code == 201
    assert response.json["customer_qualification"]["item_id"] == "ITEM-1"
    assert service.calls == [("customer", ("ITEM-1", {"customer_ref": "CUSTOMER-A"}, "corr-1"))]


def test_main_app_registers_conversion_create_route(c2_client) -> None:
    client, service = c2_client

    response = client.post(
        "/api/v1/fm02/items/ITEM-1/uom-conversions",
        json={"conversion_type": "CATCH_WEIGHT"},
    )

    assert response.status_code == 201
    assert service.calls == [
        ("create_conversion", ("ITEM-1", {"conversion_type": "CATCH_WEIGHT"}, None))
    ]


def test_main_app_registers_item_specific_conversion_resolver(c2_client) -> None:
    client, service = c2_client

    response = client.get(
        "/api/v1/fm02/items/ITEM-1/uom-conversions/UOM-1/UOM-2?effective_at=2026-10-13T00:00:00"
    )

    assert response.status_code == 404
    assert "Item-specific" in response.json["errors"][0]["message"]
    assert service.calls == [
        (
            "resolve_conversion",
            ("ITEM-1", "UOM-1", "UOM-2", "2026-10-13T00:00:00"),
        )
    ]
