from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.main import app


def seed_goods_receipt_chain(client: TestClient) -> None:
    assert client.post("/api/v1/product-orders", json={"no": "SO-BN-001"}).status_code == 201
    assert (
        client.post(
            "/api/v1/purchase-requests",
            json={
                "no": "PR-BN-001",
                "product_order_no": "SO-BN-001",
                "items": [{"item_no": "MAT-BN-001", "count": 30}],
            },
        ).status_code
        == 201
    )
    assert (
        client.post(
            "/api/v1/purchase-orders",
            json={"no": "PO-BN-001", "purchase_request_no": "PR-BN-001"},
        ).status_code
        == 201
    )
    assert (
        client.post(
            "/api/v1/goods-receipt-notes",
            json={
                "no": "GRN-BN-001",
                "purchase_order_no": "PO-BN-001",
                "item_no": "MAT-BN-001",
                "item_name": "Batch Material",
                "checkedCount": 30,
            },
        ).status_code
        == 201
    )


def test_batch_number_crud_advances_warehouse_workflow(db_session: Session) -> None:
    def override_get_db() -> Session:
        return db_session

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    try:
        seed_goods_receipt_chain(client)

        create_response = client.post(
            "/api/v1/batch-numbers",
            json={
                "no": "BATCH-CRUD-001",
                "ref_no": "GRN-BN-001",
                "date": 20260518,
                "item_no": "MAT-BN-001",
                "item_name": "Batch Material",
                "expectedCount": 30,
                "checkedCount": 30,
                "validDate": 20260818,
            },
        )
        assert create_response.status_code == 201
        created = create_response.json()
        assert created["no"] == "BATCH-CRUD-001"
        assert created["ref_no"] == "GRN-BN-001"

        read_response = client.get("/api/v1/batch-numbers/BATCH-CRUD-001")
        assert read_response.status_code == 200
        assert read_response.json()["validDate"] == 20260818

        list_response = client.get("/api/v1/batch-numbers")
        assert list_response.status_code == 200
        assert list_response.json()["total"] == 1

        update_response = client.patch(
            "/api/v1/batch-numbers/BATCH-CRUD-001",
            json={"checkedCount": 29, "comment": "One unit rejected"},
        )
        assert update_response.status_code == 200
        assert update_response.json()["checkedCount"] == 29

        workflow_response = client.get("/api/v1/workflows/order-to-warehouse/SO-BN-001")
        assert workflow_response.status_code == 200
        workflow = workflow_response.json()
        assert workflow["complete"] is False
        assert workflow["batch_number"]["exists"] is True
        assert workflow["batch_number"]["no"] == "BATCH-CRUD-001"
        assert "batch_number" not in workflow["missing_steps"]
        assert "inventory_records" in workflow["missing_steps"]

        delete_response = client.delete("/api/v1/batch-numbers/BATCH-CRUD-001")
        assert delete_response.status_code == 204

        missing_response = client.get("/api/v1/batch-numbers/BATCH-CRUD-001")
        assert missing_response.status_code == 404
    finally:
        app.dependency_overrides.clear()


def test_batch_number_validates_goods_receipt_note_and_duplicate_no(
    db_session: Session,
) -> None:
    def override_get_db() -> Session:
        return db_session

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    try:
        missing_receipt_response = client.post(
            "/api/v1/batch-numbers",
            json={"no": "BATCH-MISSING-GRN", "ref_no": "GRN-MISSING"},
        )
        assert missing_receipt_response.status_code == 400

        seed_goods_receipt_chain(client)
        payload = {"no": "BATCH-DUP-001", "ref_no": "GRN-BN-001"}
        first_response = client.post("/api/v1/batch-numbers", json=payload)
        second_response = client.post("/api/v1/batch-numbers", json=payload)

        assert first_response.status_code == 201
        assert second_response.status_code == 409
        assert "already exists" in second_response.json()["detail"]
    finally:
        app.dependency_overrides.clear()
