# ERP Status Display Mapper Inventory

Date: 2026-05-26
Scope: Frontend status vocabulary and display-mapper inventory before backend API integration.

## Purpose

This document turns the general status vocabulary policy into an implementation-oriented mapper inventory.

The frontend already uses one shared visual tone type:

```ts
type StatusTone = "success" | "warning" | "danger" | "info" | "neutral";
```

The next backend integration step should not scatter raw backend codes through page components. Backend status codes should be normalized in service or mapper files into display-ready labels and tones.

## Mapper Placement Rule

Recommended default:

```txt
Backend code -> service mapper -> page display model -> component
```

Do:

- Keep raw backend status values inside service or mapper files.
- Return management-readable labels to page components.
- Return `tone` from the mapper, not from the JSX page.
- Log or document unknown status values during runtime verification.

Avoid:

- Mapping backend codes directly inside page components.
- Making components understand backend-specific enum names.
- Reusing one generic mapper for different business domains too early.

## Shared Tone Semantics

| Tone | Use for | Operational meaning |
| --- | --- | --- |
| `success` | Ready, released, completed, normal. | Work can proceed or no action is needed. |
| `info` | In progress or ordinary waiting. | Work is moving and should be observed. |
| `warning` | Attention needed but not fully blocking. | Owner should check before it becomes late or blocked. |
| `danger` | Blocking, high risk, expired, missing critical data. | Work cannot proceed normally. |
| `neutral` | Category, scope, inactive or descriptive label. | Not a risk state by itself. |

## Status Domains

| Domain | Example modules | Mapper priority | Notes |
| --- | --- | --- | --- |
| Order stage | Orders, AI | High after Orders payload | Maps quote, commitment, production, shipping, billing and completion stages. |
| Delivery risk | Orders, Logistics, AI | High after Orders/Logistics payload | Should distinguish late risk, blocked shipment and normal promise state. |
| Commitment decision | Orders, Planning, AI | High after Orders payload | ATP/CTP labels must be consistent with Planning material/capacity readiness. |
| Inventory availability | Warehouse, Batches, Planning | High after Warehouse/Batches payload | Must separate on-hand, reserved, quality hold, quarantine and available. |
| Quality release | Quality, Warehouse, Batches, Production | High after Quality/Warehouse payload | `已放行`, `待判定`, `檢驗中`, `QA Hold`, `阻擋` should map consistently. |
| Production execution | Production, Planning, AI | Medium after Production payload | Work-order status and MES progress should not be confused with schedule risk. |
| Purchasing receiving | Purchasing, Warehouse, AI | Medium after Purchasing payload | Should separate PO status, arrival risk and receiving completion. |
| Logistics dispatch/POD | Logistics, Finance, Orders, AI | Medium after Logistics payload | Dispatch state and POD state feed billing readiness. |
| Finance AR/AP | Finance, Orders, AI | Medium after Finance payload | Billing-ready, invoiced, collected and overdue should stay separate. |
| Master data readiness | Items, BOM, Settings | Low until support endpoints are prioritized | Read-only support pages can use display labels first. |
| Trace/recall risk | Traceability, Batches | Medium after Traceability payload | Batches should not own recall-scope statuses. |

## Recommended Mapper Files

When backend payloads are available, add small domain-specific mapper helpers rather than one large global mapper.

| Area | Recommended location | Mapper examples |
| --- | --- | --- |
| Orders | `src/services/orders-api.ts` or `src/services/mappers/orders-status.ts` | `mapOrderStage`, `mapDeliveryRisk`, `mapCommitmentDecision`, `mapPaymentStatus` |
| Warehouse | `src/services/warehouse-api.ts` or `src/services/mappers/warehouse-status.ts` | `mapInventoryRisk`, `mapWarehouseTaskStatus`, `mapCapacityTone`, `mapSourceType` |
| Quality | `src/services/quality-api.ts` or `src/services/mappers/quality-status.ts` | `mapInspectionStatus`, `mapReleaseStatus`, `mapQualityBlocker` |
| Production | `src/services/production-api.ts` or `src/services/mappers/production-status.ts` | `mapWorkOrderStatus`, `mapLineStatus`, `mapMaterialReadiness` |
| Planning | `src/services/planning-api.ts` or `src/services/mappers/planning-status.ts` | `mapScheduleRisk`, `mapCapacityReadiness`, `mapMaterialShortage` |
| Purchasing | `src/services/purchasing-api.ts` or `src/services/mappers/purchasing-status.ts` | `mapPoStatus`, `mapArrivalRisk`, `mapSupplierRisk` |
| Logistics | `src/services/logistics-api.ts` or `src/services/mappers/logistics-status.ts` | `mapDispatchStatus`, `mapPodStatus`, `mapShipmentRisk` |
| Finance | `src/services/finance-api.ts` or `src/services/mappers/finance-status.ts` | `mapBillingReadiness`, `mapArStatus`, `mapApStatus`, `mapMarginRisk` |
| Batches | future `src/services/batches-api.ts` | `mapBatchRisk`, `mapQaStatus`, `mapBatchStage` |
| Items/BOM | future support service files | `mapItemStatus`, `mapBomVersionStatus`, `mapMasterDataTaskStatus` |

## Initial Domain Vocabulary

These are display labels and tone recommendations for frontend integration. Backend codes may differ.

### Order Stage

| Display label | Tone | Meaning |
| --- | --- | --- |
| `需求確認` | `info` | Order or pre-order input is still being clarified. |
| `承諾檢查` | `warning` | Material/capacity/quality feasibility is under review. |
| `可承諾` | `success` | Delivery promise can proceed. |
| `需協調` | `warning` | Delivery can proceed only with owner follow-up. |
| `暫緩接單` | `danger` | Commitment cannot be made safely. |
| `生產中` | `info` | Fulfillment has moved to work-order execution. |
| `待出貨` | `info` | Production/QA is ready enough for dispatch preparation. |
| `已完成` | `success` | Order is fulfilled or operationally complete. |

### Inventory And Batch Availability

| Display label | Tone | Meaning |
| --- | --- | --- |
| `可用` | `success` | Available quantity can be used. |
| `已預留` | `info` | Quantity is reserved for order/work/shipment. |
| `低於安全庫存` | `warning` | Supply should be reviewed. |
| `即期` | `warning` | Expiry is near but not necessarily blocked. |
| `逾期` | `danger` | Expired and should not be used. |
| `QA Hold` | `danger` | Quality hold blocks use or shipment. |
| `隔離` | `danger` | Quarantined quantity is unavailable. |
| `阻擋` | `danger` | Operational blocker exists. |

### Quality Release

| Display label | Tone | Meaning |
| --- | --- | --- |
| `已放行` | `success` | Quality released for use or shipment. |
| `檢驗中` | `info` | Quality inspection is in progress. |
| `待判定` | `warning` | Quality decision is pending. |
| `待補件` | `warning` | Document/sample/data is missing but may be resolved. |
| `QA Hold` | `danger` | Quality has blocked the item/batch/order. |
| `不合格` | `danger` | Failed inspection or nonconformance. |

### Production Execution

| Display label | Tone | Meaning |
| --- | --- | --- |
| `排程中` | `info` | Planned but not yet started. |
| `待備料` | `warning` | Material readiness needs follow-up. |
| `生產中` | `info` | Execution is active. |
| `待品檢` | `warning` | Output needs quality verification. |
| `已完工` | `success` | Work order is complete. |
| `停線` | `danger` | Execution is blocked. |
| `落後` | `danger` | Work is behind expected milestone. |

### Logistics And Finance

| Display label | Tone | Meaning |
| --- | --- | --- |
| `待派車` | `warning` | Shipment needs dispatch arrangement. |
| `裝車中` | `info` | Loading is in progress. |
| `配送中` | `info` | Shipment is on route. |
| `已簽收` | `success` | POD is complete. |
| `異常回報` | `danger` | Delivery exception exists. |
| `待請款` | `warning` | Billing can proceed or needs finance follow-up. |
| `已請款` | `success` | Invoice/billing step is complete. |
| `逾期` | `danger` | Collection/payment is late. |

### Support Master Data

| Display label | Tone | Meaning |
| --- | --- | --- |
| `量產` | `success` | Item/BOM is production-ready. |
| `試產中` | `warning` | Trial state, not fully production approved. |
| `研發中` | `info` | R&D stage. |
| `待維護` | `warning` | Master data needs completion. |
| `需新增` | `info` | New master-data record is needed. |
| `停用` | `neutral` | Inactive or not available for new work. |
| `待變更` | `warning` | Change request exists. |

## Unknown Status Policy

Until backend codes are stable:

```txt
unknown code -> display raw code or fallback label -> neutral/warning tone -> record in runtime verification
```

Recommended fallback:

```ts
{
  label: rawValue || "待確認",
  tone: "warning"
}
```

Use `neutral` only when the unknown value is clearly descriptive and not operational.

## Runtime Verification Checklist

For each endpoint during API integration, record:

1. Raw status fields returned by backend.
2. Display label chosen by mapper.
3. Tone chosen by mapper.
4. Unknown codes encountered.
5. Whether the status is authoritative or derived.
6. Whether the status can block production, shipment, billing or purchasing.

## Backend Confirmation Questions

| Question | Why it matters |
| --- | --- |
| Which statuses are canonical backend enums versus calculated dashboard states? | Determines mapper ownership. |
| Are status codes English, Chinese, numeric, or mixed legacy values? | Affects defensive parsing. |
| Can one record have both a workflow status and a risk status? | Prevents false danger/warning mapping. |
| Which Quality status should block Warehouse available quantity? | Required for Warehouse and Batches consistency. |
| Which Logistics/POD status should enable Finance billing readiness? | Required for Finance and Orders consistency. |
| Should AI display source-module raw status or normalized cross-module work status? | Required for AI V1.1 trust. |

## Implementation Sequence

Recommended sequence after real API payloads exist:

1. Add mapper functions inside the page's existing service file during first endpoint integration.
2. Move mapper helpers into `src/services/mappers/*` only after at least two services need the same domain mapping.
3. Add unit tests for any mapper that affects blocking or financial visibility.
4. Update this inventory with actual backend codes discovered during runtime verification.

## Decision

```txt
status_display_mapper_inventory_created_code_waits_for_backend_codes
```

The frontend has a clear status-display strategy. Mapper code should wait for real backend status values, but page components should remain shielded from raw backend codes.
