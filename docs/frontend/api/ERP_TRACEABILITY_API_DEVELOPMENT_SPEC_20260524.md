# ERP Traceability API Development Spec

Date: 2026-05-24
Route: `/traceability`
Purpose: Define read-only APIs for Traceability V1.

## 1. V1 Goal

Traceability V1 allows users to search by batch, item, order or work order, then inspect upstream/downstream trace chains, recall scope and document completeness.

## 2. Aggregation API

### `GET /api/v1/traceability/dashboard`

```json
{
  "summary": {
    "traceableBatchCount": 0,
    "documentMissingCount": 0,
    "recallRiskCount": 0,
    "openTraceInvestigations": 0
  },
  "recentTraceSearches": [],
  "documentGaps": [],
  "recallCandidates": []
}
```

## 3. Detail APIs

| Endpoint | Purpose |
| --- | --- |
| `GET /api/v1/traceability/search` | Search by batch, item, order or work order |
| `GET /api/v1/traceability/batches/{batchNo}` | Batch trace detail |
| `GET /api/v1/traceability/batches/{batchNo}/upstream` | Source material and supplier chain |
| `GET /api/v1/traceability/batches/{batchNo}/downstream` | Produced goods, shipped orders and customers |
| `GET /api/v1/traceability/recall-scope` | Recall scope by batch/item/date |

## 4. Dataset Structures

### `traceChain`

```json
{
  "queryType": "batch",
  "queryValue": "",
  "rootBatchNo": "",
  "upstream": [],
  "production": [],
  "downstream": [],
  "documents": [],
  "recallScope": {
    "affectedOrders": 0,
    "affectedCustomers": 0,
    "affectedQty": 0,
    "unit": ""
  }
}
```

### `upstream[]`

```json
{
  "nodeType": "material_batch",
  "batchNo": "",
  "itemNo": "",
  "itemName": "",
  "supplierName": "",
  "purchaseOrderNo": "",
  "receiptNo": "",
  "qualityStatus": "released"
}
```

### `downstream[]`

```json
{
  "nodeType": "shipping_order",
  "orderNo": "",
  "customerName": "",
  "shipDate": "2026-05-24",
  "quantity": 0,
  "unit": "",
  "podStatus": "completed"
}
```

## 5. Existing API Candidates

- `/api/v1/batchnumber`
- `/api/v1/batchtrace`
- `/api/v1/batchtrace/record`
- `/api/v1/sale/productorder`
- `/api/v1/sale/shippingorder`
- `/api/v1/workorder`
- `/api/v1/inventory`
- `/api/v1/purchase/goodsreceiptnote`

## 6. Engineer Confirmation Required

1. Does `/api/v1/batchtrace/record` include both upstream and downstream relationships?
2. Can batch trace connect purchase receipt, work order, inventory and shipping order?
3. Where are required traceability documents stored?
4. Is recall scope calculated today or must it be derived by API aggregation?
