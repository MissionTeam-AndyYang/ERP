# ERP API Development Specs Index

Date: 2026-05-24
Scope: Frontend-driven API development specifications for ERP V1.

These documents define the API datasets and response structures needed to replace frontend mock data with real backend data. They are development specs, not proof that every endpoint already exists.

## Baseline

- Frontend V1 screens: approved management-first workspaces.
- Database baseline: `docs/database/EWDB_20260526.sql`.
- Workflow baseline: `docs/database/EWDB_20260522_WORKFLOW.md`.
- Current backend source: `restserver/package/restserver/api`.
- Current backend prefix observed in code: `/api/v1`.

## Common API Design Principle

Each module should use two API layers:

1. Aggregation API for the first screen or manager workspace.
2. Detail APIs for tables, filters, drill-downs and later controlled actions.

Aggregation APIs should return compact, already-calculated datasets for the page. Detail APIs should support pagination, filters and drill-down data.

## Spec Documents

| Module | Spec |
| --- | --- |
| Warehouse | `ERP_WAREHOUSE_API_DEVELOPMENT_SPEC_20260524.md` |
| Orders | `ERP_ORDERS_API_DEVELOPMENT_SPEC_20260524.md` |
| Planning / APS | `ERP_PLANNING_APS_API_DEVELOPMENT_SPEC_20260524.md` |
| Purchasing | `ERP_PURCHASING_API_DEVELOPMENT_SPEC_20260524.md` |
| Quality | `ERP_QUALITY_API_DEVELOPMENT_SPEC_20260524.md` |
| Production | `ERP_PRODUCTION_API_DEVELOPMENT_SPEC_20260524.md` |
| Traceability | `ERP_TRACEABILITY_API_DEVELOPMENT_SPEC_20260524.md` |
| Logistics | `ERP_LOGISTICS_API_DEVELOPMENT_SPEC_20260524.md` |
| Finance | `ERP_FINANCE_API_DEVELOPMENT_SPEC_20260524.md` |
| R&D / Costing | `ERP_RD_COSTING_API_DEVELOPMENT_SPEC_20260524.md` |
| Workforce | `ERP_WORKFORCE_API_DEVELOPMENT_SPEC_20260524.md` |
| Manager Dashboard | `ERP_MANAGER_DASHBOARD_API_DEVELOPMENT_SPEC_20260524.md` |
| Settings / Master Data | `ERP_SETTINGS_MASTER_DATA_API_DEVELOPMENT_SPEC_20260524.md` |

## Common Response Envelope

Recommended response envelope:

```json
{
  "success": true,
  "data": {},
  "meta": {
    "generatedAt": "2026-05-24T08:00:00Z",
    "source": "restserver",
    "warnings": []
  }
}
```

For list endpoints:

```json
{
  "success": true,
  "data": [],
  "pagination": {
    "page": 1,
    "pageSize": 50,
    "total": 0
  },
  "meta": {
    "generatedAt": "2026-05-24T08:00:00Z"
  }
}
```

## Common Status Values

| Value | Meaning |
| --- | --- |
| `normal` | No action needed |
| `attention` | Needs monitoring |
| `warning` | Needs owner follow-up |
| `blocking` | Blocks commitment, production, shipment or billing |
| `pending` | Waiting for upstream decision/document |
| `released` | Approved for next workflow step |
| `hold` | Temporarily blocked |

## Engineer Confirmation Required

All specs include fields that may require backend confirmation:

- Existing endpoint response shape.
- Exact table/field mapping.
- Status code/value mapping.
- Permission and audit strategy for future write actions.
- Whether aggregation should be implemented in backend or initially in frontend service layer.
