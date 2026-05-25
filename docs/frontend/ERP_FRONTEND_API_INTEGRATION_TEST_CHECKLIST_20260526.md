# ERP Frontend API Integration Test Checklist

Date: 2026-05-26
Scope: Shared frontend test checklist for each workspace after API integration.

## Required Commands

Run these after each integration chunk:

```txt
npm.cmd run lint
npm.cmd run build
```

## Browser Smoke Checklist

| Check | Required for every workspace | Notes |
| --- | --- | --- |
| Page route loads | Yes | Open the route directly. |
| Source badge is correct | Yes | `API data` on success; `Mock fallback` on failure. |
| Warning message is controlled | Yes | API failure should not throw fatal UI errors. |
| Header search works | Yes | Search should filter rows/cards. |
| Current selection syncs | Yes | Detail panel should follow selected or first filtered row. |
| Tab/view switching works | Yes | Each V1 tab should remain usable. |
| Header CTA works as view navigation | Yes | No mutation unless endpoint exists. |
| Empty search result shows empty state | Yes | No blank panels. |
| Valid API empty array stays empty | Yes | Must not repopulate mock rows. |
| Desktop layout has no overlap | Yes | Check page-level horizontal overflow. |
| Mobile 390px layout has no overlap | Yes | Check page-level horizontal overflow. |

## Per-Workspace Smoke Inputs

| Workspace | Route | Suggested search values | CTA expected result |
| --- | --- | --- | --- |
| Warehouse | `/warehouse` | batch no, item no, warehouse name | Switch to task/risk-oriented view if present. |
| Orders | `/orders` | order no, customer, product | Switch to fulfillment/commitment view. |
| Production | `/production` | work order, line, product | Switch to schedule/MES view. |
| Quality | `/quality` | batch no, QC no, product | Switch to release-block view. |
| Planning | `/planning` | order no, product, material | Switch to work-order suggestion view. |
| Purchasing | `/purchasing` | supplier, material, PO | Switch to receiving view. |
| Logistics | `/logistics` | shipment no, order no, vehicle | Switch to dispatch-risk view. |
| Finance | `/finance` | order no, invoice, customer | Switch to receivables/billing view. |
| Traceability | `/traceability` | batch no, order no, work order | Switch to chain view. |
| Settings | `/settings` | domain, workspace, owner | Switch to integrations view. |
| R&D | `/rd` | project no, product, BOM | Switch to quotation view. |
| Workforce | `/workforce` | line, shift, skill | Switch to overtime/support view. |

## Runtime Verification Result Codes

| Result | Meaning |
| --- | --- |
| `accepted` | Endpoint and UI behavior are ready for V1. |
| `accepted_with_notes` | Usable for V1, but has documented mapping/status/date gaps. |
| `blocked_by_api_shape` | Response shape prevents reliable page rendering. |
| `blocked_by_missing_endpoint` | Endpoint is unavailable or not routable. |
| `blocked_by_status_vocabulary` | Unknown statuses prevent trustworthy user-facing state. |

## Integration Chunk Definition Of Done

An API integration chunk is done when:

1. Service mapper accepts the real backend payload.
2. TypeScript build passes.
3. Runtime verification document is created.
4. Browser smoke passes on desktop and mobile.
5. Any backend questions are captured as follow-up rows.
6. The page still preserves the V1 read-only / view-navigation boundary.
