# Production Analytics and Purchasing PO-first Preview Report

Date: 2026-07-24

## Scope

- Production analytics refinement:
  - `src/app/production/page.tsx`
- Purchasing static preview:
  - `docs/spec/api-proposal/purchasing_purchase_order_first_static_preview.html`

## Production Analytics Confirmation

The previous `效率損耗品質` tab showed per-work-order cards above and a per-work-order table below. Although the layout was visually different, both areas communicated nearly the same row-level data. This was not ideal for the intended screen hierarchy.

The refined behavior is:

- Upper cards: aggregate and exception-focused management summary.
- Lower table: row-level work-order detail for tracing and comparison.

Current upper cards:

- 平均產時效率
- 平均原料損耗
- 最高單品人工費
- 品質需注意

## Production Date-range Understanding

Based on the current Production API proposal and frontend mapping:

- `週排程與產能` uses `scheduleByLine` and the dashboard `period` query. V1 supports `7d` and `14d`, calculated from the query date forward.
- `MES 工單現況`, `效率損耗品質`, and `生產明細` currently use the dashboard `todayWorkOrders` list, so they are treated as query-date work-order views.
- Historical work-order lookup is not fully covered by the current list UI. The recommended V1 refinement is to extend `生產明細` with a date range / work-order search mode, backed by a historical work-order query API. If the exact work-order number is known, the existing detail endpoint pattern can still be used for drill-down.

## Purchasing PO-first Preview

The current data constraint is that purchase orders are available, while purchase requests and purchase-request-to-purchase-order links are not yet reliable.

The proposed UX direction is feasible:

- Use purchase orders as the main list rows.
- Treat purchase requests as supporting linkage/status data.
- Explicitly show missing PR links as data-governance gaps instead of inventing request data.
- Keep the screen read-only until the backend API proposal and flow algorithm are revised and approved.

Static preview file:

- `docs/spec/api-proposal/purchasing_purchase_order_first_static_preview.html`

## Verification

- `npm.cmd run lint`: Passed
- `npm.cmd run build`: Passed
- Browser smoke on `/production`: Passed
  - No runtime error.
  - No `NaN`.
  - `效率損耗品質` upper cards are aggregate summary cards.
  - Lower analytics table keeps row-level work-order columns.
- Browser could not open the local `file:///` HTML preview due to browser URL security policy. The preview file was created in the repository and can be opened directly from the filesystem by the user or reviewed as source.
