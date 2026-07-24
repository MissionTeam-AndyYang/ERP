# Purchasing PO-first Static Preview Extension Report

Date: 2026-07-24

## Scope

- Static preview:
  - `docs/spec/api-proposal/purchasing_purchase_order_first_static_preview.html`

## Changes

1. Extended the `採購單` page preview with:
   - `日期`: purchase order date.
   - `單位`: purchase contract transaction unit.
   - `單價`: purchase contract unit price.

2. Renamed the `預計到貨` concept to `到貨規劃`.
   - A purchase order can have multiple goods receipt notes.
   - The table should not imply a single arrival date when partial receipts exist.
   - Recommended display:
     - Primary line: next pending arrival date or most actionable arrival date.
     - Secondary line: receipt summary, such as receipt count, received quantity, and remaining quantity.

3. Added static preview sections for:
   - `交期風險`
   - `到貨驗收`
   - `供應商`

## Design Notes

- `採購單`: uses PO as the main row and shows PR linkage as supporting data.
- `交期風險`: focuses on PO delay, remaining quantity, next arrival, receipt status, and production/order impact.
- `到貨驗收`: uses goods receipt note as the operational row while retaining PO context.
- `供應商`: aggregates open PO count, unreceived amount, delivery status, document gaps, and contract price signals by supplier.

## Verification

- Confirmed the static preview contains the new PO columns.
- Confirmed the static preview contains all four preview sections.
- No frontend runtime code was changed in this task.
