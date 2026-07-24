# Production Detail History Query Frontend Report

Date: 2026-07-24

## Scope

- Screen: Production Workspace (`/production`)
- Tab: `生產明細`
- Frontend files:
  - `src/app/production/page.tsx`
  - `src/hooks/use-production-dashboard.ts`

## Feasibility Confirmation

It is feasible to implement a first frontend version now, using the existing Production dashboard query contract:

- `date`
- `period=7d|14d`
- `work_order_no`

Current API limitation:

- The dashboard range is a forward range from the query date.
- It does not yet support arbitrary historical `start_date` / `end_date` semantics beyond the supported 7-day or 14-day forward period.

Therefore, this frontend implementation provides a usable first step:

- Start date and end date inputs.
- Work-order number input.
- Query and clear actions.
- Date range is mapped to the currently supported dashboard `date + period` model.
- Ranges longer than 14 days are explicitly described as currently capped by the API contract.

## Changes

1. Added `ProductionDetailSearchPanel` to the `生產明細` tab.
2. Added date range and work-order number query state in `ProductionPage`.
3. Updated `useProductionDashboard` so callers can pass `ProductionDashboardQuery`.
4. Query is only applied to the dashboard call when the `生產明細` tab is active.
5. Clearing the query returns the page to the default dashboard query.

## Recommended Backend Follow-up

For a complete historical work-order search experience, add or extend an API with explicit historical query parameters, for example:

- `GET /api/v2/production/work-orders?start_date={timestamp}&end_date={timestamp}&work_order_no={no}&keyword={keyword}`

This would avoid overloading the dashboard endpoint, whose current responsibility is a forward-looking production dashboard.

## Verification

- `npm.cmd run lint`: Passed
- `npm.cmd run build`: Passed
- Browser smoke on `/production`: Passed
  - `生產明細` shows the history query panel.
  - Two date inputs are rendered.
  - Work-order number input is rendered.
  - Query action does not cause runtime error.
  - No `NaN`.
  - No mock fallback text is shown in API mode.
