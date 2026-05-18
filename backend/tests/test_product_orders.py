from sqlalchemy.orm import Session

from app.main import app


def test_product_order_crud_lifecycle(db_session: Session) -> None:
    def override_get_db() -> Session:
        return db_session

    app.config["TEST_DB_SESSION"] = db_session
    client = app.test_client()
    try:
        create_response = client.post(
            "/api/v1/product-orders",
            json={
                "no": "SO-CRUD-001",
                "date": 20260518,
                "item_no": "FG-CRUD-001",
                "item_name": "Frozen Dumpling",
                "count": 1200,
                "expectedDate": 20260520,
                "comment": "Initial order",
            },
        )
        assert create_response.status_code == 201
        created = create_response.json
        assert created["id"] is not None
        assert created["no"] == "SO-CRUD-001"
        assert created["item_name"] == "Frozen Dumpling"

        read_response = client.get("/api/v1/product-orders/SO-CRUD-001")
        assert read_response.status_code == 200
        assert read_response.json["count"] == 1200

        list_response = client.get("/api/v1/product-orders")
        assert list_response.status_code == 200
        listed = list_response.json
        assert listed["total"] == 1
        assert listed["items"][0]["no"] == "SO-CRUD-001"

        update_response = client.patch(
            "/api/v1/product-orders/SO-CRUD-001",
            json={"item_name": "Frozen Bun", "count": 900},
        )
        assert update_response.status_code == 200
        updated = update_response.json
        assert updated["item_name"] == "Frozen Bun"
        assert updated["count"] == 900

        workflow_response = client.get("/api/v1/workflows/order-to-warehouse/SO-CRUD-001")
        assert workflow_response.status_code == 200
        workflow = workflow_response.json
        assert workflow["product_order"]["exists"] is True
        assert workflow["complete"] is False
        assert "purchase_request" in workflow["missing_steps"]

        delete_response = client.delete("/api/v1/product-orders/SO-CRUD-001")
        assert delete_response.status_code == 204

        missing_response = client.get("/api/v1/product-orders/SO-CRUD-001")
        assert missing_response.status_code == 404
    finally:
        app.config.pop("TEST_DB_SESSION", None)


def test_product_order_rejects_duplicate_no(db_session: Session) -> None:
    def override_get_db() -> Session:
        return db_session

    app.config["TEST_DB_SESSION"] = db_session
    client = app.test_client()
    try:
        payload = {"no": "SO-DUP-001", "item_name": "Duplicate Check"}
        first_response = client.post("/api/v1/product-orders", json=payload)
        second_response = client.post("/api/v1/product-orders", json=payload)

        assert first_response.status_code == 201
        assert second_response.status_code == 409
        assert "already exists" in second_response.json["detail"]
    finally:
        app.config.pop("TEST_DB_SESSION", None)
