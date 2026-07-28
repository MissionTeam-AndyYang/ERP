# Purchasing API Group

> Implementation source: `restserver/package/restserver/api/v2/purchasing.py`
> Proposal source: `docs/spec/api-proposal/purchasing_purchase_order_first_proposal.md`
> Flow source: `docs/spec/api-proposal/purchasing_purchase_order_first_flow_algorithm.md`

## Common Request Rules

All list endpoints require `startDate` and `endDate` in `YYYY-MM-DD` format and accept the `x-timezone` IANA timezone header. The date range is inclusive in the requested local timezone and is converted to UTC timestamps for database filtering. `start` defaults to `0`; `count` defaults to `50` and is capped at `100`. Enum codes are returned as codes for frontend localization.

## Implemented Endpoints

| URL | Method | Description |
|---|---|---|
| `/api/v2/purchasing/purchase-orders/dashboard` | GET | Purchase order dashboard, receipt quantity, risk code and purchase request linkage. |
| `/api/v2/purchasing/purchase-orders/delivery-risk` | GET | Non-normal purchase order delivery risks. |
| `/api/v2/purchasing/goods-receipts/dashboard` | GET | Goods receipt rows and receipt/warehouse handoff codes. |
| `/api/v2/purchasing/suppliers/dashboard` | GET | Supplier-level purchase order aggregation. |
| `/api/v2/purchasing/purchase-orders/{purchase_order_no}/detail` | GET | One purchase order with formal request and receipt relations. |

## Response Contract

Each list response contains `serverTimestamp`, `timezone`, `range`, `summary`, `items`, `total`, `start`, and `count`. `range` contains `startDate`, `endDate`, `startTimestamp`, and `endTimestamp`.

Purchase-order item fields are `purchaseOrderNo`, `purchaseDateTimestamp`, `itemNo`, `itemName`, `unit`, `supplierNo`, `supplierName`, `orderedCount`, `receivedCount`, `openCount`, `unitPrice`, `purchaseAmount`, `expectedArrivalTimestamp`, `purchaseRequestNo`, `purchaseRequestLinkStatusCode`, `sourceOrderNo`, `linkedWorkOrderNo`, `warehouseStatusCode`, `riskLevel`, and `riskCode`.

Delivery-risk rows additionally contain `shortageCount`, `shortageValue`, `impactSourceType`, `impactSourceNo`, and `followUpCode`.

Goods-receipt rows contain `no`, `purchaseOrderNo`, `dateTimestamp`, `category`, `itemNo`, `itemName`, `expectedCount`, `checkedCount`, `receivedCount`, `receivingStatusCode`, `warehouseStatusCode`, and `nextOwnerDepartment`.

Supplier rows contain `supplierNo`, `supplierName`, `purchaseOrderCount`, `openPurchaseOrderCount`, `latePurchaseOrderCount`, `purchaseAmount`, `pendingReceiptCount`, and `riskLevel`.

Detail response contains `purchaseOrder`, `purchaseRequest`, `supplier`, `receipts`, `source`, `inventory`, `workflow`, and `relatedDocuments`. Missing formal relations are represented by `null`, empty strings, empty arrays, or `unknown`; no relation is inferred from item names or dates.

## Calculation Rules

- `receivedCount` sums `goods_receipt_note.checkedCount`; category `0` adds and category `1` subtracts.
- `openCount` is `max(orderedCount - receivedCount, 0)`.
- Quantity uses two decimal places, unit price four decimal places, and amount is rounded to an integer.
- `riskLevel` and `riskCode`, warehouse status, receipt status, and owner department are codes; the frontend supplies localized labels.
- V1 does not expose Quality status or perform purchase-order mutations.
