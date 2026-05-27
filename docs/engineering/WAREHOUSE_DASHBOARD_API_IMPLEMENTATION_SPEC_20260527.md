# Warehouse Dashboard API Implementation Spec

Date: 2026-05-27
Endpoint: `GET /api/v1/warehouse/dashboard`
Priority: 1
Baseline: `EWDB_20260526.sql`

## Purpose

Implement the first V1 read-only aggregation API for the Warehouse page. This endpoint replaces frontend mock data for management-level warehouse visibility.

The page must help managers understand:

- Current inventory value by category.
- Warehouse/storage capacity and available pallet positions.
- Inventory risk: turnover over one month, shelf-life risk and safety stock shortage.
- Today's pending inbound/outbound warehouse tasks.

## Required Response Shape

The endpoint must return these top-level datasets:

```txt
kpis
categorySummaries
capacities
records
risks
tasks
```

The verifier checks only top-level datasets, but the frontend expects each dataset to be compatible with `src/types/warehouse.ts`.

## Frontend Contract

Reference files:

- `src/services/warehouse-api.ts`
- `src/hooks/use-warehouse-dashboard.ts`
- `src/types/warehouse.ts`
- `src/mock/warehouse.ts`
- `docs/frontend/api/ERP_WAREHOUSE_API_DEVELOPMENT_SPEC_20260524.md`

## Candidate Source Tables / Routes

| Dataset | Candidate tables / route sources | Notes |
| --- | --- | --- |
| `kpis` | `inventory_record`, `inventory_item_month_statistic`, `inventory_month_statistic`, `warehouse_record` | Inventory value, pallet usage, risk count, pending task count. |
| `categorySummaries` | `inventory_item_month_statistic`, `inventory_record`, `item_price`, item master tables | Category-level value and pallet count. |
| `capacities` | `ship_wh_alias`, `ship_wh`, `warehouse_record`, `inventory_record` | Requires confirmation where total capacity/pallet limit is stored. |
| `records` | `inventory_record`, `batch_number`, `company`, item master tables | Current stock rows by item/batch/warehouse. |
| `risks` | `inventory_record`, `batch_number`, `inventory_item_month_statistic`, safety-stock source TBD | Turnover, shelf-life and low-stock signals. |
| `tasks` | `warehouse_record`, `inventory_order`, `goods_receipt_note`, `shipping_order` | Today's unprocessed inbound/outbound tasks. |

Existing route candidates:

```txt
/api/v1/inventory
/api/v1/inventory/items
/api/v1/inventory/months
/api/v1/inventory/price
/api/v1/inventory/statistics
/api/v1/shipwarehouse
/api/v1/shipwarehouse/warehouserec
/api/v1/batchnumber
/api/v1/batchtrace
```

## Open Field Decisions

Engineer should confirm before or during implementation:

| ID | Decision | Current assumption |
| --- | --- | --- |
| W1 | Source of on-hand/reserved/available quantity | Use inventory records/statistics if available; otherwise derive available as on-hand minus reserved. |
| W2 | Warehouse capacity source | TBD; likely `ship_wh_alias` or warehouse master data. |
| W3 | Pallet count calculation | Use stored pallet count if available; otherwise derive from quantity/unit rule only if confirmed. |
| W4 | Safety stock source | TBD. If no source exists, return no low-stock risk and document limitation. |
| W5 | Inventory value method | Use latest item price or inventory amount field if already stored. |
| W6 | Quality hold/release source | TBD; may require Quality API/model later. |
| W7 | Expiry/shelf-life source | Use `batch_number` date/valid fields if confirmed. |

## Recommended Backend Design

Add a Warehouse dashboard API using one of these approaches:

Option A, preferred:

- New `warehouse_uri.py` / `warehouse.py` module for dashboard aggregation.
- Register new blueprint in `restserver/package/restserver/app.py`.
- Route: `/api/v1/warehouse/dashboard`.

Option B, acceptable short-term:

- Add dashboard route to an existing warehouse-related blueprint if engineer prefers not to create a new module yet.
- Endpoint path must still be `/api/v1/warehouse/dashboard`.

## Response Example

Field names can be refined to match `src/types/warehouse.ts`, but the top-level shape should remain:

```json
{
  "kpis": [],
  "categorySummaries": [],
  "capacities": [],
  "records": [],
  "risks": [],
  "tasks": []
}
```

If using `CAPIBase`, the payload may be wrapped:

```json
{
  "code": 0,
  "message": "success",
  "payload": {
    "kpis": [],
    "categorySummaries": [],
    "capacities": [],
    "records": [],
    "risks": [],
    "tasks": []
  }
}
```

The frontend `apiGet` and contract verifier support this restserver `payload` wrapper.

## Verification

After implementation, run:

```powershell
python scripts/verify_v1_api_contracts.py --base-url http://127.0.0.1:5000 --module warehouse --output docs/backend/runtime-verification/WAREHOUSE_API_CONTRACT_YYYYMMDD.md
```

Expected result:

```txt
PASS warehouse http://127.0.0.1:5000/api/v1/warehouse/dashboard
```

## Acceptance Criteria

Backend can be marked `backend_implemented` when:

- `GET /api/v1/warehouse/dashboard` returns HTTP 2xx.
- Response is valid JSON.
- Required top-level datasets are present.
- Contract verifier passes.
- Runtime output is committed or shared under `docs/backend/runtime-verification/`.
- Known missing optional business fields are documented.

Frontend can be marked `frontend_integrated` when:

- Warehouse page uses real API data without schema errors.
- Mock fallback is no longer used when backend is available.
- Warehouse functional checklist passes.
- `npm.cmd run lint` and `npm.cmd run build` pass.
