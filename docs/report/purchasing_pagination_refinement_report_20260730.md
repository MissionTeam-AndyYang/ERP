# Purchasing Pagination Refinement Report

Date: 2026-07-30
Scope: `PurchasingWorkspaceScreen` (`/purchasing`)

## Issue

The Purchasing Center API query already supported `start`, `count`, and `total`, but the frontend always sent `count=50` without a visible pagination control. Users could only review the first 50 records and had no way to navigate to later records.

## Implementation

- Added pagination controls to the Purchasing Center main content area.
- Added independent page state for each Purchasing view:
  - `PurchasingPurchaseOrderView`
  - `PurchasingDeliveryRiskView`
  - `PurchasingReceivingView`
  - `PurchasingSupplierView`
- Added page size options: 25, 50, 100.
- Connected the active view pagination state to API query parameters:
  - `start = activePage * pageSize`
  - `count = pageSize`
- Reset pagination to page 1 when date range, keyword search, page size, or data source changes.
- Updated selected PO fallback lookup so a selected delivery-risk item can still drive the right-side detail panel even when it is not present in the current purchase-order page.

## Verification

| Check | Result |
| --- | --- |
| `npm.cmd run lint` | Pass |
| `npm.cmd run build` | Pass |
| Browser smoke: API mode shows pagination controls | Pass |
| Browser smoke: API error does not show mock fallback | Pass |
| Browser smoke: Mock mode shows pagination controls and PO-first data | Pass |
| Browser smoke: page size can switch to 25 | Pass |

## Runtime Notes

- Local URL used for smoke test: `http://localhost:3000/purchasing`
- API mode displayed the expected backend error banner when local backend endpoints were unavailable.
- Mock mode displayed PO-first sample rows and allowed page size selection.
