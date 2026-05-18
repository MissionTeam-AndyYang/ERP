from sqlalchemy.orm import Session

from app.main import app


def test_purchase_request_crud_advances_warehouse_workflow(db_session: Session) -> None:
    def override_get_db() -> Session:
        return db_session

    app.config["TEST_DB_SESSION"] = db_session
    client = app.test_client()
    try:
        product_order_response = client.post(
            "/api/v1/product-orders",
            json={"no": "SO-PR-001", "item_name": "Workflow Source Order"},
        )
        assert product_order_response.status_code == 201

        create_response = client.post(
            "/api/v1/purchase-requests",
            json={
                "no": "PR-CRUD-001",
                "product_order_no": "SO-PR-001",
                "date": 20260518,
                "comment": "Material request",
                "items": [
                    {
                        "item_no": "MAT-PR-001",
                        "count": 100,
                        "expectedDate": 20260519,
                    }
                ],
            },
        )
        assert create_response.status_code == 201
        created = create_response.json
        assert created["no"] == "PR-CRUD-001"
        assert created["product_order_no"] == "SO-PR-001"
        assert created["items"][0]["item_no"] == "MAT-PR-001"

        add_item_response = client.post(
            "/api/v1/purchase-requests/PR-CRUD-001/items",
            json={"item_no": "MAT-PR-002", "count": 50},
        )
        assert add_item_response.status_code == 201
        assert len(add_item_response.json["items"]) == 2

        read_response = client.get("/api/v1/purchase-requests/PR-CRUD-001")
        assert read_response.status_code == 200
        purchase_request = read_response.json
        assert purchase_request["items"][1]["item_no"] == "MAT-PR-002"

        list_response = client.get("/api/v1/purchase-requests")
        assert list_response.status_code == 200
        assert list_response.json["total"] == 1

        update_response = client.patch(
            "/api/v1/purchase-requests/PR-CRUD-001",
            json={"comment": "Updated material request"},
        )
        assert update_response.status_code == 200
        assert update_response.json["comment"] == "Updated material request"

        workflow_response = client.get("/api/v1/workflows/order-to-warehouse/SO-PR-001")
        assert workflow_response.status_code == 200
        workflow = workflow_response.json
        assert workflow["complete"] is False
        assert workflow["purchase_request"]["exists"] is True
        assert len(workflow["purchase_request_items"]) == 2
        assert "purchase_request" not in workflow["missing_steps"]
        assert "purchase_request_items" not in workflow["missing_steps"]
        assert "purchase_order" in workflow["missing_steps"]

        first_item_id = purchase_request["items"][0]["id"]
        delete_item_response = client.delete(
            f"/api/v1/purchase-requests/PR-CRUD-001/items/{first_item_id}"
        )
        assert delete_item_response.status_code == 204
        assert len(client.get("/api/v1/purchase-requests/PR-CRUD-001").json["items"]) == 1

        delete_response = client.delete("/api/v1/purchase-requests/PR-CRUD-001")
        assert delete_response.status_code == 204

        missing_response = client.get("/api/v1/purchase-requests/PR-CRUD-001")
        assert missing_response.status_code == 404
    finally:
        app.config.pop("TEST_DB_SESSION", None)


def test_purchase_request_validates_product_order_and_duplicate_no(
    db_session: Session,
) -> None:
    def override_get_db() -> Session:
        return db_session

    app.config["TEST_DB_SESSION"] = db_session
    client = app.test_client()
    try:
        missing_order_response = client.post(
            "/api/v1/purchase-requests",
            json={"no": "PR-MISSING-ORDER", "product_order_no": "SO-MISSING"},
        )
        assert missing_order_response.status_code == 400

        client.post("/api/v1/product-orders", json={"no": "SO-PR-DUP"})
        payload = {"no": "PR-DUP-001", "product_order_no": "SO-PR-DUP"}
        first_response = client.post("/api/v1/purchase-requests", json=payload)
        second_response = client.post("/api/v1/purchase-requests", json=payload)

        assert first_response.status_code == 201
        assert second_response.status_code == 409
        assert "already exists" in second_response.json["detail"]
    finally:
        app.config.pop("TEST_DB_SESSION", None)
