# Backend Coding Convention

Backend stack:

```text
Flask API + SQLAlchemy + Alembic + Pydantic
```

## Directory Rules

```text
backend/app/
  api/v1/endpoints/   Flask Blueprint route handlers
  api/v1/router.py    API blueprint registration
  api/v1/utils.py     API helpers, request parsing, JSON response, DB session access
  core/               Settings and shared exceptions
  db/                 SQLAlchemy engine/session/base
  models/             SQLAlchemy ORM models
  schemas/            Pydantic request/response schemas
  services/           Business logic and database operations
```

## Layer Responsibilities

Endpoint files should:

- Define Flask routes.
- Parse query/body input.
- Call service functions.
- Convert service results into response schemas.
- Return JSON responses.

Endpoint files should not:

- Contain business rules.
- Write complex SQL queries.
- Commit transactions directly.

Service files should:

- Own database reads and writes.
- Validate upstream references such as `product_order_no`, `purchase_request_no`, `batchNumber`.
- Raise `ApiError` for expected API failures.
- Commit transactions for create/update/delete operations.

Service files should not:

- Import Flask request/response objects.
- Import endpoint modules.
- Return raw Flask responses.

Schema files should:

- Use Pydantic models for API input and output.
- Use `ConfigDict(from_attributes=True)` for ORM read models.
- Keep field names aligned with the current EWDB schema, including camelCase fields already present in the database.

## Error Handling

Use:

```python
from app.core.exceptions import ApiError
```

Examples:

```python
raise ApiError(404, "Product order 'SO-001' was not found.")
raise ApiError(400, "Purchase request 'PR-001' was not found.")
raise ApiError(409, "Batch number 'BATCH-001' already exists.")
```

Expected status codes:

| Case | Status |
| --- | --- |
| Validation error | `422` |
| Missing upstream reference | `400` |
| Record not found | `404` |
| Duplicate business key | `409` |

## CRUD Pattern

For business tables with a `no` column:

```text
GET    /api/v1/<resource>
POST   /api/v1/<resource>
GET    /api/v1/<resource>/<no>
PATCH  /api/v1/<resource>/<no>
DELETE /api/v1/<resource>/<no>
```

For tables without `no`, use the primary key:

```text
GET    /api/v1/inventory-records/<record_id>
PATCH  /api/v1/inventory-records/<record_id>
DELETE /api/v1/inventory-records/<record_id>
```

List endpoints should support:

```text
skip: int >= 0
limit: int between 1 and 200
```

## Workflow Rules

When adding CRUD for a table that belongs to a workflow, add or update tests proving that the workflow moves forward.

Example:

- Creating `purchase_request` removes `purchase_request` from `missing_steps`.
- Creating `batch_number` removes `batch_number` from `missing_steps`.
- Creating the final `inventory_record` makes `order-to-warehouse.complete = true`.

## Test Rules

Add tests for:

- Create success.
- Read/list success.
- Update success.
- Delete success.
- Duplicate business key.
- Missing upstream reference.
- Workflow progress, if applicable.

Use the shared SQLite fixture in:

```text
backend/tests/conftest.py
```

For Flask tests, inject the test DB session with:

```python
app.config["TEST_DB_SESSION"] = db_session
```

Always clear it in `finally`:

```python
app.config.pop("TEST_DB_SESSION", None)
```

## Naming

Use these file naming patterns:

```text
schemas/product_orders.py
services/product_orders.py
api/v1/endpoints/product_orders.py
tests/test_product_orders.py
```

Use plural resource names for API endpoints:

```text
product-orders
purchase-requests
purchase-orders
goods-receipt-notes
batch-numbers
inventory-records
```

## Forbidden Patterns

Do not add:

- FastAPI imports or dependencies.
- Direct request parsing inside service files.
- Database writes from endpoint files.
- New framework-level abstractions without a clear need.
- Unvalidated workflow links.
