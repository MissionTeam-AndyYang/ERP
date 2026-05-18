from flask.testing import FlaskClient
from sqlalchemy.orm import Session

from app.main import app


def seed_purchase_order_chain(client: FlaskClient) -> None:
    assert (
        client.post(
            "/api/v1/product-orders",
            json={"no": "SO-GRN-001", "item_name": "Receipt Source"},
        ).status_code
        == 201
    )
    assert (
        client.post(
            "/api/v1/purchase-requests",
            json={
                "no": "PR-GRN-001",
                "product_order_no": "SO-GRN-001",
                "items": [{"item_no": "MAT-GRN-001", "count": 40}],
            },
        ).status_code
        == 201
    )
    assert (
        client.post(
            "/api/v1/purchase-orders",
            json={
                "no": "PO-GRN-001",
                "purchase_request_no": "PR-GRN-001",
                "item_no": "MAT-GRN-001",
                "item_name": "Receipt Material",
                "count": 40,
            },
        ).status_code
        == 201
    )


def test_goods_receipt_note_crud_advances_warehouse_workflow(db_session: Session) -> None:
    def override_get_db() -> Session:
        return db_session

    app.config["TEST_DB_SESSION"] = db_session
    client = app.test_client()
    try:
        seed_purchase_order_chain(client)

        create_response = client.post(
            "/api/v1/goods-receipt-notes",
            json={
                "no": "GRN-CRUD-001",
                "purchase_order_no": "PO-GRN-001",
                "date": 20260518,
                "item_no": "MAT-GRN-001",
                "item_name": "Receipt Material",
                "expectedCount": 40,
                "checkedCount": 38,
                "amount": 7600,
            },
        )
        assert create_response.status_code == 201
        created = create_response.json
        assert created["no"] == "GRN-CRUD-001"
        assert created["purchase_order_no"] == "PO-GRN-001"

        read_response = client.get("/api/v1/goods-receipt-notes/GRN-CRUD-001")
        assert read_response.status_code == 200
        assert read_response.json["checkedCount"] == 38

        list_response = client.get("/api/v1/goods-receipt-notes")
        assert list_response.status_code == 200
        assert list_response.json["total"] == 1

        update_response = client.patch(
            "/api/v1/goods-receipt-notes/GRN-CRUD-001",
            json={"checkedCount": 40, "comment": "Accepted"},
        )
        assert update_response.status_code == 200
        assert update_response.json["checkedCount"] == 40

        workflow_response = client.get("/api/v1/workflows/order-to-warehouse/SO-GRN-001")
        assert workflow_response.status_code == 200
        workflow = workflow_response.json
        assert workflow["complete"] is False
        assert workflow["goods_receipt_note"]["exists"] is True
        assert workflow["goods_receipt_note"]["no"] == "GRN-CRUD-001"
        assert "goods_receipt_note" not in workflow["missing_steps"]
        assert "batch_number" in workflow["missing_steps"]

        delete_response = client.delete("/api/v1/goods-receipt-notes/GRN-CRUD-001")
        assert delete_response.status_code == 204

        missing_response = client.get("/api/v1/goods-receipt-notes/GRN-CRUD-001")
        assert missing_response.status_code == 404
    finally:
        app.config.pop("TEST_DB_SESSION", None)


def test_goods_receipt_note_validates_purchase_order_and_duplicate_no(
    db_session: Session,
) -> None:
    def override_get_db() -> Session:
        return db_session

    app.config["TEST_DB_SESSION"] = db_session
    client = app.test_client()
    try:
        missing_order_response = client.post(
            "/api/v1/goods-receipt-notes",
            json={"no": "GRN-MISSING-PO", "purchase_order_no": "PO-MISSING"},
        )
        assert missing_order_response.status_code == 400

        seed_purchase_order_chain(client)
        payload = {"no": "GRN-DUP-001", "purchase_order_no": "PO-GRN-001"}
        first_response = client.post("/api/v1/goods-receipt-notes", json=payload)
        second_response = client.post("/api/v1/goods-receipt-notes", json=payload)

        assert first_response.status_code == 201
        assert second_response.status_code == 409
        assert "already exists" in second_response.json["detail"]
    finally:
        app.config.pop("TEST_DB_SESSION", None)
