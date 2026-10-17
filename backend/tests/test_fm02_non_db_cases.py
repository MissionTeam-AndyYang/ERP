from dataclasses import dataclass, field
from typing import Any


@dataclass
class ItemOnlyMock:
    items: dict[str, dict[str, Any]] = field(default_factory=dict)
    requests: dict[str, tuple[str, str]] = field(default_factory=dict)

    @staticmethod
    def _validate(payload: dict[str, Any]) -> dict[str, Any] | None:
        required = ("idempotency_key", "display_name", "primary_category", "ownership_context", "base_uom_code")
        missing = [field for field in required if not str(payload.get(field, "")).strip()]
        if missing:
            return {"status": 400, "errors": [{"field": field, "code": "REQUIRED"} for field in missing]}
        if payload["primary_category"] not in {"RAW", "MATERIAL", "FILM", "WIP", "FG"}:
            return {"status": 400, "errors": [{"field": "primary_category", "code": "INVALID_CATEGORY"}]}
        if payload["base_uom_code"] not in {"EA", "KG", "M"}:
            return {"status": 400, "errors": [{"field": "base_uom_code", "code": "INVALID_UOM"}]}
        if any(field in payload for field in ("item_id", "item_code", "lifecycle_status")):
            return {"status": 400, "errors": [{"field": "server_field", "code": "CLIENT_FORBIDDEN"}]}
        if any(field in payload for field in ("product_id", "sku", "gtin")):
            return {"status": 400, "errors": [{"field": "scope", "code": "PRODUCT_SCOPE_FORBIDDEN"}]}
        return None

    def create(self, payload: dict[str, Any]) -> dict[str, Any]:
        validation = self._validate(payload)
        if validation:
            return validation
        key = payload["idempotency_key"]
        fingerprint = repr(sorted(payload.items()))
        existing = self.requests.get(key)
        if existing is not None:
            item_id, original_fingerprint = existing
            if original_fingerprint != fingerprint:
                return {"status": 409, "errors": [{"field": "idempotency_key", "code": "CONFLICT"}]}
            return {"status": 200, "idempotent_replay": True, "item": self.items[item_id]}
        item_id = f"ITEM-{len(self.items) + 1:04d}"
        item = {"item_id": item_id, "item_code": "AB12CD34EF56", "lifecycle_status": "DRAFT", "row_version": 0, **payload}
        self.items[item_id] = item
        self.requests[key] = (item_id, fingerprint)
        return {"status": 201, "idempotent_replay": False, "item": item}

    def get(self, item_id: str) -> dict[str, Any]:
        item = self.items.get(item_id)
        return {"status": 200, "item": item} if item else {"status": 404, "errors": [{"code": "NOT_FOUND"}]}

    def edit(self, item_id: str, expected_row_version: int, **changes: Any) -> dict[str, Any]:
        item = self.items.get(item_id)
        if item is None:
            return {"status": 404, "errors": [{"code": "NOT_FOUND"}]}
        if expected_row_version != item["row_version"]:
            return {"status": 409, "errors": [{"field": "row_version", "code": "STALE_WRITE"}]}
        if any(field in changes for field in ("product_id", "sku", "gtin")):
            return {"status": 400, "errors": [{"field": "scope", "code": "PRODUCT_SCOPE_FORBIDDEN"}]}
        item.update(changes)
        item["row_version"] += 1
        return {"status": 200, "item": item}


def _payload(**overrides: Any) -> dict[str, Any]:
    value = {
        "idempotency_key": "TC20-001",
        "display_name": "Synthetic Item",
        "primary_category": "MATERIAL",
        "ownership_context": "TC",
        "base_uom_code": "EA",
    }
    value.update(overrides)
    return value


def test_tc19_non_db_api_mock_known_read_and_unknown_error():
    adapter = ItemOnlyMock()
    created = adapter.create(_payload())
    assert created["status"] == 201
    assert adapter.get(created["item"]["item_id"])["status"] == 200
    assert adapter.get("ITEM-UNKNOWN")["status"] == 404


def test_tc19_create_validation_required_uom_category_and_server_fields():
    adapter = ItemOnlyMock()
    assert adapter.create(_payload(display_name=""))["status"] == 400
    assert adapter.create(_payload(primary_category="UNAPPROVED"))["status"] == 400
    assert adapter.create(_payload(base_uom_code="BAD"))["status"] == 400
    assert adapter.create(_payload(item_code="CLIENT-CODE"))["status"] == 400


def test_tc20_deterministic_idempotent_replay_and_conflict():
    adapter = ItemOnlyMock()
    first = adapter.create(_payload())
    replay = adapter.create(_payload())
    conflict = adapter.create(_payload(display_name="Different"))
    assert first["status"] == 201
    assert replay["status"] == 200 and replay["idempotent_replay"] is True
    assert conflict["status"] == 409
    assert len(adapter.items) == 1
    item_id = first["item"]["item_id"]
    assert adapter.edit(item_id, expected_row_version=99, display_name="Stale")["status"] == 409
    assert adapter.edit(item_id, expected_row_version=0, display_name="Edited")["status"] == 200


def test_tc23_item_only_integration_mock_excludes_product_scope():
    adapter = ItemOnlyMock()
    result = adapter.create(_payload())
    item = result["item"]
    assert set(item) >= {"item_id", "item_code", "lifecycle_status"}
    assert "product_id" not in item
    assert "sku" not in item
    assert adapter.create(_payload(product_id="PRODUCT-1"))["status"] == 400
    assert adapter.create(_payload(sku="SKU-1"))["status"] == 400
    assert adapter.create(_payload(gtin="GTIN-1"))["status"] == 400
    assert len(adapter.items) == 1
