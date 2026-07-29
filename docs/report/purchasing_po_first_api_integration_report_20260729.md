# Purchasing PO-first API Integration Test Report

Date: 2026-07-29
Scope: `PurchasingWorkspaceScreen` (`/purchasing`)
Proposal basis: `docs/spec/api-proposal/purchasing_purchase_order_first_proposal.md`

## Implementation Summary

- Updated `/purchasing` from PR/demand-first layout to PO-first layout.
- Integrated the confirmed V1 read-only APIs:
  - `GET /api/v2/purchasing/purchase-orders/dashboard`
  - `GET /api/v2/purchasing/purchase-orders/delivery-risk`
  - `GET /api/v2/purchasing/goods-receipts/dashboard`
  - `GET /api/v2/purchasing/suppliers/dashboard`
  - `GET /api/v2/purchasing/purchase-orders/{purchase_order_no}/detail`
- Added date range and keyword query controls.
- Added API / Mock source toggle.
- API mode now preserves real backend results:
  - Empty arrays render as empty states.
  - API errors render an error banner.
  - Mock data is shown only when the user explicitly selects Mock mode.
- Added frontend enum-to-label mapping with multi-language support for unit, risk, PR link status, warehouse status, receipt category, receiving status, impact source, follow-up code, workflow task type, task status, and owner department.
- Updated `docs/spec/api-proposal/planned_screen_list_naming.md` to mark Purchasing V1 screen/view/panel implementation status.

## Verification

| Check | Result |
| --- | --- |
| `npm.cmd run lint` | Pass |
| `npm.cmd run build` | Pass |
| Browser smoke: `/purchasing` API mode | Pass |
| Browser smoke: API error does not show mock fallback | Pass |
| Browser smoke: Mock mode displays PO-first mock data | Pass |
| Browser smoke: receiving view shows goods receipt data | Pass |

## Browser Smoke Notes

- Local URL: `http://localhost:3000/purchasing`
- API mode displayed `Purchasing API 發生錯誤，畫面未改用 mock 資料。` when the local backend endpoint returned `404`.
- Page did not show the old `已使用 mock fallback` text.
- Switching to Mock mode displayed PO-first sample purchase orders, suppliers, and receipt records.

## Remaining Runtime Review Items

- Re-run browser smoke with the engineer's backend server available and confirm all five API payloads align with the frontend mappers.
- Confirm real supplier and purchase order date ranges with production-like historical data.
- Confirm detail API workflow and receipt arrays against at least one PO with multiple goods receipt notes.
