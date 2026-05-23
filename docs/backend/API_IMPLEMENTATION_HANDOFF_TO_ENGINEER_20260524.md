# ERP V1 API Implementation Handoff To Engineer

Date: 2026-05-24
Audience: backend engineer

## Purpose

The frontend V1 screens are now stable enough to start API implementation and integration planning. The new API development specs define the response datasets needed to replace frontend mock data.

## Source Documents

Start here:

- `docs/frontend/api/ERP_API_DEVELOPMENT_SPECS_INDEX_20260524.md`
- `docs/backend/API_IMPLEMENTATION_TRACKER_20260524.md`
- `docs/frontend/ERP_FRONTEND_API_FIELD_MAPPING_20260524.md`

Core module specs:

- `docs/frontend/api/ERP_WAREHOUSE_API_DEVELOPMENT_SPEC_20260524.md`
- `docs/frontend/api/ERP_ORDERS_API_DEVELOPMENT_SPEC_20260524.md`
- `docs/frontend/api/ERP_PRODUCTION_API_DEVELOPMENT_SPEC_20260524.md`
- `docs/frontend/api/ERP_QUALITY_API_DEVELOPMENT_SPEC_20260524.md`
- `docs/frontend/api/ERP_PLANNING_APS_API_DEVELOPMENT_SPEC_20260524.md`
- `docs/frontend/api/ERP_PURCHASING_API_DEVELOPMENT_SPEC_20260524.md`

## Requested Engineer Response

Please review the specs and respond module by module with:

```txt
Module:
Proposed endpoint accepted? yes/no/modify
Existing endpoint candidates:
Required new endpoint(s):
Missing DB/table/field:
Status mapping notes:
Implementation blocker:
Estimated implementation order:
```

## Recommended First Implementation

Start with Warehouse read-only API.

Preferred endpoint:

```txt
GET /api/v1/warehouse/dashboard
```

If adding `/warehouse` is not preferred yet, an equivalent endpoint or temporary aggregation route is acceptable, but the response must include the required datasets from:

```txt
docs/frontend/api/ERP_WAREHOUSE_API_DEVELOPMENT_SPEC_20260524.md
```

## Verification Expectation

After implementing an endpoint, run the API contract verification script:

```powershell
python scripts/verify_v1_api_contracts.py --base-url http://127.0.0.1:5000 --module warehouse --output docs/backend/runtime-verification/WAREHOUSE_API_CONTRACT_YYYYMMDD.md
```

The output should be committed or shared for review only after confirming it does not contain secrets.

## Current Backend Candidates

Observed backend prefix:

```txt
/api/v1
```

Useful existing groups:

- `inventory`
- `sale`
- `purchase`
- `workorder`
- `work`
- `productline`
- `plstatistics`
- `batchnumber`
- `batchtrace`
- `shipwarehouse`
- `quotation`
- `contract`
- `bom`
- `material`
- `goods`

## First Warehouse Confirmation Items

Please confirm:

1. Where warehouse location and pallet capacity are stored.
2. Whether inventory distinguishes on-hand, reserved, quality-hold and available quantity.
3. Safety stock source table/field.
4. Cost method for inventory value.
5. Where material inspection release/hold status is stored.
6. Whether batch expiry and shelf-life data can be returned from existing endpoints.
