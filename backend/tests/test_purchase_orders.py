from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.main import app


def seed_order_and_purchase_request(client: TestClient) -> None:
    product_order_response = client.post(
        "/api/v1/product-orders",
        json={"no": "SO-PO-001", "item_name": "Purchase Order Source"},
    )
    assert product_order_response.status_code == 201

    purchase_request_response = client.post(
        "/api/v1/purchase-requests",
        json={
            "no": "PR-PO-001",
            "product_order_no": "SO-PO-001",
            "items": [{"item_no": "MAT-PO-001", "count": 80}],
        },
    )
    assert purchase_request_response.status_code == 201


def test_purchase_order_crud_advances_warehouse_workflow(db_session: Session) -> None:
    def override_get_db() -> Session:
        return db_session

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    try:
        seed_order_and_purchase_request(client)

        create_response = client.post(
            "/api/v1/purchase-orders",
            json={
                "no": "PO-CRUD-001",
                "purchase_request_no": "PR-PO-001",
                "date": 20260518,
                "item_no": "MAT-PO-001",
                "item_name": "Flour",
                "count": 80,
                "amount": 16000,
            },
        )
        assert create_response.status_code == 201
        created = create_response.json()
        assert created["no"] == "PO-CRUD-001"
        assert created["purchase_request_no"] == "PR-PO-001"

        read_response = client.get("/api/v1/purchase-orders/PO-CRUD-001")
        assert read_response.status_code == 200
        assert read_response.json()["item_name"] == "Flour"

        list_response = client.get("/api/v1/purchase-orders")
        assert list_response.status_code == 200
        assert list_response.json()["total"] == 1

        update_response = client.patch(
            "/api/v1/purchase-orders/PO-CRUD-001",
            json={"item_name": "Premium Flour", "count": 75},
        )
        assert update_response.status_code == 200
        assert update_response.json()["item_name"] == "Premium Flour"
        assert update_response.json()["count"] == 75

        workflow_response = client.get("/api/v1/workflows/order-to-warehouse/SO-PO-001")
        assert workflow_response.status_code == 200
        workflow = workflow_response.json()
        assert workflow["complete"] is False
        assert workflow["purchase_order"]["exists"] is True
        assert workflow["purchase_order"]["no"] == "PO-CRUD-001"
        assert "purchase_order" not in workflow["missing_steps"]
        assert "goods_receipt_note" in workflow["missing_steps"]

        delete_response = client.delete("/api/v1/purchase-orders/PO-CRUD-001")
        assert delete_response.status_code == 204

        missing_response = client.get("/api/v1/purchase-orders/PO-CRUD-001")
        assert missing_response.status_code == 404
    finally:
        app.dependency_overrides.clear()


def test_purchase_order_validates_purchase_request_and_duplicate_no(
    db_session: Session,
) -> None:
    def override_get_db() -> Session:
        return db_session

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    try:
        missing_request_response = client.post(
            "/api/v1/purchase-orders",
            json={"no": "PO-MISSING-PR", "purchase_request_no": "PR-MISSING"},
        )
        assert missing_request_response.status_code == 400

        seed_order_and_purchase_request(client)
        payload = {"no": "PO-DUP-001", "purchase_request_no": "PR-PO-001"}
        first_response = client.post("/api/v1/purchase-orders", json=payload)
        second_response = client.post("/api/v1/purchase-orders", json=payload)

        assert first_response.status_code == 201
        assert second_response.status_code == 409
        assert "already exists" in second_response.json()["detail"]
    finally:
        app.dependency_overrides.clear()
