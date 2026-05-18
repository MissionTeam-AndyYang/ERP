from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.main import app


def seed_batch_number_chain(client: TestClient) -> None:
    assert client.post("/api/v1/product-orders", json={"no": "SO-INV-001"}).status_code == 201
    assert (
        client.post(
            "/api/v1/purchase-requests",
            json={
                "no": "PR-INV-001",
                "product_order_no": "SO-INV-001",
                "items": [{"item_no": "MAT-INV-001", "count": 24}],
            },
        ).status_code
        == 201
    )
    assert (
        client.post(
            "/api/v1/purchase-orders",
            json={"no": "PO-INV-001", "purchase_request_no": "PR-INV-001"},
        ).status_code
        == 201
    )
    assert (
        client.post(
            "/api/v1/goods-receipt-notes",
            json={"no": "GRN-INV-001", "purchase_order_no": "PO-INV-001"},
        ).status_code
        == 201
    )
    assert (
        client.post(
            "/api/v1/batch-numbers",
            json={
                "no": "BATCH-INV-001",
                "ref_no": "GRN-INV-001",
                "item_no": "MAT-INV-001",
                "item_name": "Inventory Material",
                "checkedCount": 24,
            },
        ).status_code
        == 201
    )


def test_inventory_record_crud_completes_warehouse_workflow(db_session: Session) -> None:
    def override_get_db() -> Session:
        return db_session

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    try:
        seed_batch_number_chain(client)

        create_response = client.post(
            "/api/v1/inventory-records",
            json={
                "ref_no": "GRN-INV-001",
                "warehouse_no": "WH-001",
                "warehouse_displayName": "Main Warehouse",
                "date": 20260518,
                "batchNumber": "BATCH-INV-001",
                "item_no": "MAT-INV-001",
                "item_name": "Inventory Material",
                "count": 24,
                "amount": 4800,
            },
        )
        assert create_response.status_code == 201
        created = create_response.json()
        assert created["id"] is not None
        assert created["batchNumber"] == "BATCH-INV-001"

        record_id = created["id"]
        read_response = client.get(f"/api/v1/inventory-records/{record_id}")
        assert read_response.status_code == 200
        assert read_response.json()["warehouse_no"] == "WH-001"

        list_response = client.get("/api/v1/inventory-records")
        assert list_response.status_code == 200
        assert list_response.json()["total"] == 1

        update_response = client.patch(
            f"/api/v1/inventory-records/{record_id}",
            json={"count": 23, "comment": "One unit reserved"},
        )
        assert update_response.status_code == 200
        assert update_response.json()["count"] == 23

        workflow_response = client.get("/api/v1/workflows/order-to-warehouse/SO-INV-001")
        assert workflow_response.status_code == 200
        workflow = workflow_response.json()
        assert workflow["complete"] is True
        assert workflow["missing_steps"] == []
        assert len(workflow["inventory_records"]) == 1
        assert workflow["inventory_records"][0]["fields"]["batchNumber"] == "BATCH-INV-001"

        delete_response = client.delete(f"/api/v1/inventory-records/{record_id}")
        assert delete_response.status_code == 204

        missing_response = client.get(f"/api/v1/inventory-records/{record_id}")
        assert missing_response.status_code == 404
    finally:
        app.dependency_overrides.clear()


def test_inventory_record_validates_batch_number(db_session: Session) -> None:
    def override_get_db() -> Session:
        return db_session

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    try:
        response = client.post(
            "/api/v1/inventory-records",
            json={"batchNumber": "BATCH-MISSING", "count": 1},
        )

        assert response.status_code == 400
        assert "was not found" in response.json()["detail"]
    finally:
        app.dependency_overrides.clear()
