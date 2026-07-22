# Production API Error and Tab Table Refinement Report

Date: 2026-07-22

## Scope

- Screen: Production Workspace (`/production`)
- Frontend files:
  - `src/app/production/page.tsx`
  - `src/hooks/use-production-dashboard.ts`
  - `src/services/production-api.ts`

## Design Confirmation

The first version Production workspace separates the following concerns:

- MES status: today's work-order execution and shop-floor readiness.
- Efficiency / loss / quality: production efficiency, material loss, labor cost, and quality signals.
- Production detail: work order, batch, BOM/source order, workflow, materials, and related documents.

Therefore, it is acceptable for these views to use the same backend work-order source data, but it is not acceptable for the three tabs to render the exact same table columns. The frontend now renders separate table views for each tab.

## Changes

1. API error behavior
   - API mode no longer falls back to mock data when `GET /api/v2/production/dashboard` fails.
   - API errors return an empty dashboard state and an explicit error message.
   - Mock data is shown only when the user explicitly selects mock mode.
   - Detail API errors preserve the selected list row context but do not mark the result as mock.

2. Tab-specific tables
   - `MES 工單現況`: focuses on schedule window, MES status, progress, shop-floor resources, and attention items.
   - `效率損耗品質`: focuses on efficiency, standard/actual hours, material loss, unit labor cost, quality, and delivery impact.
   - `生產明細`: focuses on work order batch, BOM/source order, planned window, workflow progress, material detail count, and related document count.

## Verification

- `npm.cmd run lint`: Passed
- `npm.cmd run build`: Passed
- Browser smoke test on `http://127.0.0.1:3000/production`: Passed
  - API error state does not show `Mock fallback`.
  - API error state does not show `Mock data`.
  - API error state shows the explicit message that mock data is not displayed.
  - No runtime error.
  - No `NaN`.
  - MES, analytics, and detail tabs render different table headers.
