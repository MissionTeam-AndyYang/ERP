# ERP Logistics Workspace Spec

日期：2026-05-23

## Status

Logistics first-version workspace updated from the early module page into the management workspace pattern.

- Page: `src/app/logistics/page.tsx`
- Mock data: `src/mock/logistics.ts`
- Types: `src/types/logistics.ts`

## First-Version Goal

Help management answer:

1. Which shipments must go out today?
2. Which shipments are blocked by warehouse, quality, dispatch, cold-chain, or documents?
3. Which vehicles, drivers, routes, and temperature requirements are assigned?
4. Which shipments risk missing customer arrival time?
5. Are shipping documents, quality release records, temperature logs, and proof of delivery complete?

## First-Version Tabs

| Tab | Purpose |
| --- | --- |
| 今日出貨 | Today's shipments, customer requested arrival time, warehouse release, quality release, and current stage |
| 派車風險 | Shipments blocked by warehouse, quality, inventory, vehicle, route, or documents |
| 冷鏈溫層 | Vehicle, temperature requirement, current temperature, and cold-chain status |
| 文件/簽收 | Shipping documents, quality release, temperature records, and proof of delivery |

## Data Shape

Shipment records are shaped around:

- `id`, `salesOrder`
- `customer`, `channel`, `destination`, `route`
- `product`, `batchNo`
- `quantity`, `unit`
- `requestedArrivalTime`, `plannedDepartureTime`
- `stage`, `deliveryRisk`, `riskReason`
- `warehouseStatus`
- `qualityReleaseStatus`
- `vehicleNo`, `driver`
- `temperatureRequirement`, `currentTemperature`, `temperatureStatus`
- `documentsReady`
- `proofOfDeliveryStatus`
- `documents`
- `workflow`

## Workflow Basis

```txt
product_order
-> planning / production / quality release
-> warehouse picking and outbound review
-> shipping order
-> dispatch / vehicle / driver
-> cold-chain temperature tracking
-> delivery
-> proof of delivery
-> finance payment follow-up
```

## Boundary With Other Workspaces

- Orders: owns customer due date, fulfillment risk, margin, and payment priority.
- Planning / APS: owns feasibility, material plan, capacity plan, and work-order suggestions.
- Production: owns finished production status.
- Quality: owns release, hold, and quality blocking.
- Warehouse: owns stock availability, picking, outbound review, and location handling.
- Logistics: owns dispatch, route, vehicle, driver, cold-chain record, delivery status, and POD.
- Finance: consumes delivery and POD status for billing and collection follow-up.

## API Needs

| Need | Candidate restserver Module |
| --- | --- |
| Shipment list/detail | `sale`, `shipwarehouse`, shipping-related tables |
| Order and customer link | `sale`, `product_order`, customer tables |
| Warehouse outbound status | `inventory`, warehouse outbound tables |
| Quality release status | quality-related tables or production quality extension |
| Vehicle and driver | logistics/vehicle/driver tables if available |
| Temperature logs | cold-chain or IoT temperature tables if available |
| Proof of delivery | shipping receipt / delivery confirmation tables |

## First-Version Decisions

- Logistics shows dispatch and delivery risk; it does not optimize routes yet.
- Cold-chain tracking is represented as operational status and document readiness.
- Proof of delivery is included because it closes the shipment and supports billing.

## Deferred

- Route optimization.
- Real-time GPS map.
- IoT temperature streaming.
- Driver mobile workflow.
- Freight cost settlement.
- Return logistics.

