# ERP Frontend V1 API Field Mapping

Date: 2026-05-24
Purpose: Map approved frontend V1 workspaces to current or proposed backend API data sources.

Backend notes:

- Observed backend framework: Flask.
- Observed API prefix: `/api/v1`.
- Backend source location: `restserver/package/restserver/api`.
- This document is a planning map. It does not claim every frontend field is already available from the current API response.

## 1. Existing Backend API Groups Observed

| API group | Observed endpoints | Likely business area |
| --- | --- | --- |
| Auth/User | `/api/v1/user/login`, device login/logout | Login and user session |
| Sale | `/api/v1/sale/productorder`, `/api/v1/sale/shippingorder`, `/api/v1/sale/statistics`, `/api/v1/sale/payment`, `/api/v1/sale/contract`, `/api/v1/sale/arap` | Orders, shipment, contracts, AR/AP |
| Purchase | `/api/v1/purchase/purchaseorder`, `/api/v1/purchase/goodsreceiptnote`, `/api/v1/purchase/statistics`, `/api/v1/purchase/payment`, `/api/v1/purchase/contract`, `/api/v1/purchase/arap` | Purchase orders, receipts, supplier contracts, AP |
| Inventory | `/api/v1/inventory`, `/api/v1/inventory/price`, `/api/v1/inventory/statistics`, `/api/v1/inventory/items`, `/api/v1/inventory/record`, `/api/v1/inventory/months` | Stock, value, inventory movements |
| Material | `/api/v1/material`, `/api/v1/material/itemprice` | Materials and price |
| Goods/Product | `/api/v1/goods`, `/api/v1/product`, `/api/v1/transitems`, `/api/v1/transitems/item` | Items, products and transformed items |
| BOM | `/api/v1/bom`, `/api/v1/bom/tree`, `/api/v1/bom/process`, `/api/v1/bom/aps` | BOM, formula, process and APS expansion |
| APS | `/api/v1/aps/quantity` | Planning quantity calculation |
| Work order | `/api/v1/workorder`, `/api/v1/workorder/productdata`, `/api/v1/workorder/expecteddata`, `/api/v1/workorder/statistics` | Work orders, expected/actual production data |
| Work | `/api/v1/work/assignment`, `/api/v1/work/process`, `/api/v1/work/productdata`, `/api/v1/work/progress` | Work execution and progress |
| Product line | `/api/v1/productline`, `/api/v1/productline/process`, `/api/v1/productline/station`, `/api/v1/productline/equipment`, `/api/v1/productline/factory` | Lines, processes, stations, equipment, factory |
| Production statistics | `/api/v1/plstatistics/mancapacity`, `/api/v1/plstatistics/itemcapacity`, `/api/v1/plstatistics/itemloss`, `/api/v1/plstatistics/itemcost` | Capacity, loss, item cost and labor statistics |
| Batch | `/api/v1/batchnumber`, `/api/v1/batchtrace`, `/api/v1/batchtrace/record` | Batch numbers and traceability |
| Ship/Warehouse service | `/api/v1/shipwarehouse`, `/api/v1/shipwarehouse/contract`, `/api/v1/shipwarehouse/shiprec`, `/api/v1/shipwarehouse/shippayment`, `/api/v1/shipwarehouse/shiparap`, `/api/v1/shipwarehouse/warehouserec`, `/api/v1/shipwarehouse/warehousepayment`, `/api/v1/shipwarehouse/warehousearap` | Logistics, storage contracts, shipping/warehouse records and payments |
| Quotation/Contract | `/api/v1/quotation`, `/api/v1/contract` | Quotation and contract records |
| Master data | `/api/v1/company`, `/api/v1/enterprise`, `/api/v1/bankaccount`, `/api/v1/device` | Company, enterprise, bank, device |

## 2. Workspace Mapping

### Manager Dashboard `/`

Current frontend data groups:

- Fulfillment risk summary
- Today decision queue
- Cross-department blockers
- Today work queue
- Pre-order pipeline
- Production/quality/warehouse/finance signals

Existing candidate APIs:

- Sale: `/api/v1/sale/productorder`, `/api/v1/sale/shippingorder`, `/api/v1/sale/statistics`, `/api/v1/sale/contract`, `/api/v1/sale/arap`
- Purchase: `/api/v1/purchase/purchaseorder`, `/api/v1/purchase/goodsreceiptnote`, `/api/v1/purchase/statistics`, `/api/v1/purchase/contract`
- Inventory: `/api/v1/inventory`, `/api/v1/inventory/statistics`, `/api/v1/inventory/items`
- Work order: `/api/v1/workorder`, `/api/v1/workorder/statistics`
- Quality candidate: no explicit quality endpoint observed; may need quality fields in batch/work/inventory records or a new endpoint.
- Finance candidate: sale/purchase ARAP and payment endpoints.

Proposed aggregation APIs:

- `/api/v1/dashboard/manager/summary`
- `/api/v1/dashboard/manager/decisions`
- `/api/v1/dashboard/manager/blockers`
- `/api/v1/dashboard/manager/workqueue`
- `/api/v1/dashboard/manager/preorder`

Key fields needed:

| Field | Meaning | Source candidate |
| --- | --- | --- |
| fulfillmentRiskCount | Number of orders with delivery/material/quality risk | sale + workorder + inventory + quality |
| deliveryCommitmentRate | Orders deliverable on promised date | sale + planning/APS + logistics |
| estimatedMargin | Estimated margin from quotation/order cost basis | quotation + sale + bom + purchase price |
| cashSignal | AR amount or billing-ready amount | sale/arap + sale/payment |
| decisionQueue | Items requiring manager action | aggregated workflow/status rules |
| blockers | Cross-module blocking records | aggregated module status |

### Warehouse `/warehouse`

Frontend V1 needs:

- Inventory value by category
- Pallet/location usage and available capacity
- Inventory turnover and expiry alerts
- Safety stock alerts
- Pending inbound/outbound tasks
- Release status impact from Quality

Existing candidate APIs:

- `/api/v1/inventory`
- `/api/v1/inventory/price`
- `/api/v1/inventory/statistics`
- `/api/v1/inventory/items`
- `/api/v1/inventory/months`
- `/api/v1/purchase/goodsreceiptnote`
- `/api/v1/sale/shippingorder`
- `/api/v1/shipwarehouse/warehouserec`

Field needs:

| Frontend field | Source candidate | Gap/risk |
| --- | --- | --- |
| item/category | inventory/items, material, goods/product | Need category mapping: raw material, packaging, film, WIP, finished goods |
| qty/onHand/available/reserved | inventory | Need quality hold and reserved quantity rules |
| unitCost/value | inventory/price, material/itemprice | Cost method must be confirmed |
| palletUsed/palletCapacity | shipwarehouse/warehouserec or new warehouse-location data | Capacity model may require new data |
| expiryDate/shelfLife | inventory/items or batchnumber | Must exclude material/film from 1/3 shelf-life rule where applicable |
| inboundPending | purchase/goodsreceiptnote | Need status mapping |
| outboundPending | sale/shippingorder or shipwarehouse/shiprec | Need status mapping |

Recommended first backend task:

Ask the engineer to return a Warehouse V1 read endpoint or confirm whether existing inventory endpoints already include category, value, expiry, batch and location/capacity fields.

### Orders `/orders`

Frontend V1 needs:

- Customer quotation / customer contract status
- Formal order status
- ATP/CTP commitment check
- Delivery risk ranking
- Margin signal
- Links to Planning, Purchasing, Quality, Logistics and Finance

Existing candidate APIs:

- `/api/v1/sale/productorder`
- `/api/v1/sale/contract`
- `/api/v1/sale/statistics`
- `/api/v1/quotation`
- `/api/v1/contract`
- `/api/v1/aps/quantity`
- `/api/v1/inventory/statistics`
- `/api/v1/workorder`

Field needs:

| Frontend field | Source candidate | Gap/risk |
| --- | --- | --- |
| orderNo/customer/promisedDate | sale/productorder | Confirm response fields |
| quoteStatus/customerContractStatus | quotation, sale/contract, contract | Need distinguish supplier vs customer contract |
| materialAvailability | inventory + bom/aps | Aggregated calculation likely needed |
| capacityAvailability | aps + productline + workorder | Aggregated calculation likely needed |
| committedDate | sale/productorder or calculated | Need status rule |
| estimatedMargin | quotation + bom + purchase prices | May need costing endpoint |

### Planning / APS `/planning`

Frontend V1 needs:

- Formal order demand
- BOM explosion
- Material shortage
- Capacity and staff readiness
- Work-order suggestions
- Purchase request suggestions

Existing candidate APIs:

- `/api/v1/aps/quantity`
- `/api/v1/bom/aps`
- `/api/v1/bom/tree`
- `/api/v1/workorder`
- `/api/v1/productline`
- `/api/v1/productline/process`
- `/api/v1/plstatistics/mancapacity`
- `/api/v1/plstatistics/itemcapacity`
- `/api/v1/inventory`
- `/api/v1/purchase/purchaseorder`

Gap:

Existing APS route appears narrow. V1 may need either a planning aggregation endpoint or frontend aggregation from BOM, inventory, workorder and productline APIs.

### Purchasing `/purchasing`

Frontend V1 needs:

- Supplier sourcing and sample material status
- Supplier quotation/contract status
- Mass-production purchase order status
- Arrival risk
- Price variance and contract coverage

Existing candidate APIs:

- `/api/v1/purchase/purchaseorder`
- `/api/v1/purchase/goodsreceiptnote`
- `/api/v1/purchase/statistics`
- `/api/v1/purchase/contract`
- `/api/v1/purchase/arap`
- `/api/v1/material/itemprice`
- `/api/v1/quotation`
- `/api/v1/contract`

Gap:

Need confirm whether quotation/contract endpoints can distinguish supplier quotation, customer quotation, supplier contract and customer contract.

### Quality `/quality`

Frontend V1 needs:

- Material/item inspection queue
- Release/hold/quarantine status
- Process/finished/pre-shipment inspection signal
- Document completeness
- Quality blockers for warehouse, production and logistics

Existing candidate APIs:

- `/api/v1/batchnumber`
- `/api/v1/batchtrace`
- `/api/v1/batchtrace/record`
- `/api/v1/work/productdata`
- `/api/v1/workorder/productdata`
- `/api/v1/inventory`

Gap:

No explicit `/api/v1/quality` endpoint was observed. If quality status is embedded in batch/work/inventory tables, the engineer should document the status fields. If not, a dedicated quality endpoint is recommended.

Proposed endpoint:

- `/api/v1/quality/inspection`
- `/api/v1/quality/release`
- `/api/v1/quality/blockers`

### Production `/production`

Frontend V1 needs:

- Date/line work-order schedule
- MES status
- Material/staff readiness
- Efficiency, loss and unit labor cost
- QC status

Existing candidate APIs:

- `/api/v1/workorder`
- `/api/v1/workorder/productdata`
- `/api/v1/workorder/expecteddata`
- `/api/v1/workorder/statistics`
- `/api/v1/work/assignment`
- `/api/v1/work/process`
- `/api/v1/work/productdata`
- `/api/v1/work/progress`
- `/api/v1/productline`
- `/api/v1/plstatistics/mancapacity`
- `/api/v1/plstatistics/itemcapacity`
- `/api/v1/plstatistics/itemloss`
- `/api/v1/plstatistics/itemcost`

### Traceability `/traceability`

Frontend V1 needs:

- Batch/item/order/work-order lookup
- Forward and backward trace chain
- Recall scope
- Document completeness

Existing candidate APIs:

- `/api/v1/batchnumber`
- `/api/v1/batchtrace`
- `/api/v1/batchtrace/record`
- `/api/v1/sale/productorder`
- `/api/v1/workorder`
- `/api/v1/inventory`

### Logistics `/logistics`

Frontend V1 needs:

- Shipment readiness
- Dispatch status
- Cold chain/document/POD status
- Quality release and warehouse outbound status

Existing candidate APIs:

- `/api/v1/sale/shippingorder`
- `/api/v1/shipwarehouse/shiprec`
- `/api/v1/shipwarehouse/shippayment`
- `/api/v1/shipwarehouse/shiparap`
- `/api/v1/inventory`
- `/api/v1/batchtrace`

Gap:

POD and cold-chain data availability must be confirmed.

### Finance `/finance`

Frontend V1 needs:

- Estimated and actual margin
- Cost variance
- Billing readiness
- AR/AP signal
- Order-level financial trace

Existing candidate APIs:

- `/api/v1/sale/arap`
- `/api/v1/sale/payment`
- `/api/v1/purchase/arap`
- `/api/v1/purchase/payment`
- `/api/v1/shipwarehouse/shiparap`
- `/api/v1/shipwarehouse/warehousearap`
- `/api/v1/plstatistics/itemcost`
- `/api/v1/inventory/price`

Gap:

Estimated margin likely requires joining quotation, BOM, purchase price and sale order data.

### R&D / Costing `/rd`

Frontend V1 needs:

- Development request
- Formula/material selection
- Sample making and sample delivery status
- BOM version
- Costing basis
- Nutrition label status
- Transfer to formal item/BOM

Existing candidate APIs:

- `/api/v1/bom`
- `/api/v1/bom/tree`
- `/api/v1/bom/process`
- `/api/v1/material`
- `/api/v1/material/itemprice`
- `/api/v1/product`
- `/api/v1/goods`
- `/api/v1/quotation`
- `/api/v1/contract`

Gap:

No explicit R&D/development request endpoint observed. R&D V1 may need a new domain endpoint or a status convention using existing BOM/product/quotation records.

Proposed endpoint:

- `/api/v1/rd/projects`
- `/api/v1/rd/samples`
- `/api/v1/rd/costing`
- `/api/v1/rd/nutrition`

### Workforce `/workforce`

Frontend V1 needs:

- Shift coverage
- Skill/certification readiness
- Overtime/support plan
- Labor risk by production schedule

Existing candidate APIs:

- `/api/v1/work/assignment`
- `/api/v1/plstatistics/mancapacity`
- `/api/v1/productline/station`

Gap:

Dedicated employee/skill/certification endpoint was not observed in the route list.

### Settings / Master Data `/settings`

Frontend V1 needs:

- Users and permissions
- Company/enterprise data
- Product/item/material/BOM governance
- Integration settings
- Localization settings

Existing candidate APIs:

- `/api/v1/user/login`
- `/api/v1/company`
- `/api/v1/enterprise`
- `/api/v1/product`
- `/api/v1/goods`
- `/api/v1/material`
- `/api/v1/bom`
- `/api/v1/bankaccount`
- `/api/v1/device`

Gap:

Permission role endpoints are not obvious from the observed route list. Need engineer confirmation.

## 3. First Integration Recommendation

Start with Warehouse read-only integration.

Reason:

- It connects inventory value, stock quantity, warehouse space, inbound/outbound and quality hold.
- It is highly visible to managers.
- It provides a foundation for Orders, Planning, Production and Logistics risk checks.

Minimum Warehouse V1 response shape:

```json
{
  "summary": {
    "totalInventoryValue": 0,
    "availablePallets": 0,
    "occupiedPallets": 0,
    "pendingInbound": 0,
    "pendingOutbound": 0,
    "riskCount": 0
  },
  "categories": [
    {
      "category": "raw_material",
      "label": "原料",
      "quantity": 0,
      "value": 0,
      "pallets": 0,
      "turnoverDays": 0,
      "riskLevel": "normal"
    }
  ],
  "alerts": [
    {
      "type": "expiry",
      "itemNo": "",
      "itemName": "",
      "batchNo": "",
      "message": "",
      "riskLevel": "warning"
    }
  ],
  "tasks": [
    {
      "taskType": "inbound",
      "documentNo": "",
      "status": "pending",
      "owner": "",
      "dueTime": ""
    }
  ]
}
```

## 4. Questions for Engineer

1. Which existing endpoint best represents current inventory by batch, item category, location and value?
2. Does inventory currently distinguish available, reserved and quality-hold quantity?
3. Is warehouse pallet/location capacity stored in the current schema or does it require a new table/API?
4. Where is quality inspection release/hold status stored today?
5. Can supplier quotation and customer quotation be distinguished in existing quotation/contract endpoints?
6. Which endpoint returns formal order promised date and delivery status?
7. Does workorder data include scheduled date, line, process, planned quantity and actual quantity?
8. Is there any existing user role/permission endpoint beyond login?

## 5. Frontend Implementation Guidance

For the first API integration:

- Keep the approved UI layout unchanged.
- Replace mock imports with service-layer calls, not direct fetch calls scattered in components.
- Add a small frontend API client layer such as `src/services/api-client.ts`.
- Keep mock fallback only for local design preview if backend is unavailable.
- Normalize backend data into the existing frontend type shape.
- Mark missing backend fields as `TODO(api)` in the service layer rather than changing the page UI prematurely.

## 6. Decision

The frontend V1 pages are ready for API mapping. The next practical engineering step is Warehouse read-only integration, followed by Orders, Production and Quality.
