# ERP Logistics API Development Spec

Date: 2026-05-24
Route: `/logistics`
Purpose: Define read-only APIs for Logistics V1.

## 1. V1 Goal

Logistics V1 shows shipment readiness, dispatch status, cold-chain/document status, POD and blockers from warehouse outbound and quality release.

## 2. Aggregation API

### `GET /api/v1/logistics/dashboard`

```json
{
  "summary": {
    "todayShipmentCount": 0,
    "readyToShipCount": 0,
    "blockedShipmentCount": 0,
    "podPendingCount": 0,
    "documentMissingCount": 0
  },
  "todayShipments": [],
  "dispatchRisks": [],
  "coldChainSignals": [],
  "documentStatus": [],
  "podStatus": []
}
```

## 3. Detail APIs

| Endpoint | Purpose |
| --- | --- |
| `GET /api/v1/logistics/shipments` | Shipment list |
| `GET /api/v1/logistics/shipments/{shipmentNo}` | Shipment detail |
| `GET /api/v1/logistics/dispatch` | Dispatch and vehicle plan |
| `GET /api/v1/logistics/documents` | Shipment documents |
| `GET /api/v1/logistics/pod` | POD status |

## 4. Dataset Structures

### `todayShipments[]`

```json
{
  "shipmentNo": "",
  "orderNo": "",
  "customerName": "",
  "shipDate": "2026-05-24",
  "deliveryWindow": "13:00-16:00",
  "warehouseOutboundStatus": "pending",
  "qualityReleaseStatus": "released",
  "dispatchStatus": "planned",
  "documentStatus": "ready",
  "podStatus": "pending",
  "riskLevel": "normal"
}
```

### `dispatchRisks[]`

```json
{
  "shipmentNo": "",
  "riskType": "quality_hold",
  "message": "",
  "ownerModule": "quality",
  "blocking": true
}
```

## 5. Existing API Candidates

- `/api/v1/sale/shippingorder`
- `/api/v1/shipwarehouse/shiprec`
- `/api/v1/shipwarehouse/shippayment`
- `/api/v1/shipwarehouse/shiparap`
- `/api/v1/inventory`
- `/api/v1/batchtrace`

## 6. Engineer Confirmation Required

1. Where is POD status stored?
2. Does shipping order include dispatch/vehicle data?
3. Where is cold-chain temperature or status recorded?
4. Which quality release status blocks shipment?
5. Which logistics event makes Finance billing-ready?
