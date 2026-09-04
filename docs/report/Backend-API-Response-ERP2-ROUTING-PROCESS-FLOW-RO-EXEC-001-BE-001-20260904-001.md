# Backend API Response - ERP2-ROUTING-PROCESS-FLOW-RO-EXEC-001-BE-001

## 1. 交付摘要

| Item | Result |
|---|---|
| Work Item | ERP2-ROUTING-PROCESS-FLOW-RO-EXEC-001-BE-001 |
| Authorization | ERP2-CIO-ROUTING-PROCESS-FLOW-RO-EXEC-001 |
| Scope | Routing / Process Flow read-only Backend API |
| Result | PASS with Shared DEV fixture limitation |
| Date | 2026-09-04 |

本次完成最小 read-only Routing / Process Flow API family，用於 Product / WIP Routing Version visibility、ordered steps、process identity、stage/group display、Recipe reference、bounded Packaging context、standard-performance reference、source lineage 與 controlled warnings。

## 2. Implemented Route List

| Method | URL | Purpose | Result |
|---|---|---|---|
| GET | `/api/v2/routing/dashboard` | 查詢 Product / WIP Routing Version 摘要清單 | PASS |
| GET | `/api/v2/routing/products/{item_no}/versions` | 查詢指定製成品或在製品的 Routing Version 清單 | PASS |
| GET | `/api/v2/routing/versions/{routing_version_id}/steps` | 查詢指定 Routing Version 的 ordered process steps | PASS |
| GET | `/api/v2/routing/products/{item_no}/current` | 查詢指定製成品或在製品目前生效 Routing | PASS |

Only GET routes were registered. No POST / PUT / PATCH / DELETE route was added.

## 3. Data Contract Summary

| Area | Key Fields |
|---|---|
| Dashboard | `summary`, `routingVersions[]`, `capabilityBoundary`, `total`, `start`, `count` |
| Routing Version | `routingVersionId`, `itemNo`, `itemName`, `itemCategory`, `routingVersion`, `versionStateCode`, `routingStatusCode`, `stepCount`, `warningCodes[]` |
| Ordered Steps | `stepId`, `stepOrder`, `oneProcess`, `secProcess`, `processNo`, `processLabel`, `stageCode`, `groupCode` |
| Recipe Reference | `recipeReference.established`, `recipeNo`, `recipeVersion`, `sourceCode` |
| Packaging Context | `packagingContext.established`, `packagingLevel`, `packagingBomNo`, `quantity`, `unit`, `weight`, `sourceCode` |
| Resource Eligibility | `resourceEligibility.governed=false`, `eligibleResourceRefs=[]`, `sourceCode=not_recorded` |
| Standard Performance | `standardPerformance.governed`, `hourlyOutput`, `laborCount`, `unit`, `sourceDateTimestamp`, `sourceCode` |
| Lineage | `sourceLineage` at routing and step level |
| Warnings | `warnings[]` with `warningCode`, `refNo`, `stepId` |

## 4. Physical Source Mapping

| Product Semantics | Physical Source | Treatment |
|---|---|---|
| Routing Version | `product_process` | Current routing version evidence |
| Ordered Routing Steps | `process_flow` | Ordered by `process_flow.order`, then `id` |
| Process identity / label | `process` | Mapped by `oneProcess + secProcess`; `process.comment` is returned as label key/data text |
| Product item master | `product` | Product name/category reference |
| WIP item master | `inproduct` | WIP name/category reference |
| Recipe reference | `product_spec` | Established when `product_spec.bom_no` exists for item/version |
| Packaging context | `product_bom_spec` | Bounded read-only packaging context only |
| Standard performance | `process_capacity` | Latest row with same `oneProcess + secProcess` and `date <= effectiveDate` |
| Resource eligibility | Not governed in current schema | Returned as not governed with warning |

## 5. Warning / Lineage Treatment

| Warning Code | Meaning |
|---|---|
| `missing_steps` | Routing Version has no `process_flow` rows |
| `missing_item_master` | `product_process.item_no` cannot be resolved to product or inproduct |
| `missing_process_master` | Step process code cannot be resolved in `process` |
| `missing_standard_performance` | No governed `process_capacity` reference was found |
| `missing_recipe_reference` | No established `product_spec.bom_no` reference was found |
| `packaging_context_not_governed` | No bounded `product_bom_spec` packaging context exists |
| `resource_eligibility_not_governed` | No governed resource eligibility source exists in the current schema |

No Chinese display fallback is hardcoded into the API for enum values. Frontend remains responsible for enum-to-language conversion.

## 6. Product / WIP Fixture Coverage

Automated tests cover:

1. Product Routing Version visibility.
2. WIP Routing Version visibility.
3. Effective / future version state calculation.
4. Ordered Routing Steps.
5. Process identity and process label mapping.
6. Stage/group code mapping.
7. Established Recipe reference through `product_spec`.
8. Non-Recipe / missing Recipe warning path.
9. Bounded Packaging context through `product_bom_spec`.
10. Resource eligibility boundary as not governed.
11. Standard-performance reference through `process_capacity`.
12. Missing-step warning behavior.
13. Read-only POST negative control.

## 7. Tests

| Test | Command | Result |
|---|---|---|
| Routing API tests | `.venv\Scripts\python.exe -m pytest restserver\tests\test_routing_process_flow_api.py -q` | 6 passed |
| Full backend tests | `.venv\Scripts\python.exe -m pytest restserver\tests -q` | 92 passed |
| App route import | `create_app()` route-map check | PASS |

## 8. Shared DEV DB-Backed Smoke Status

Shared DEV endpoint and credential wrapper are available, but the current Shared DEV database does not contain the Routing physical source table required for DB-backed Routing smoke.

| Check | Result |
|---|---|
| Shared DEV database identity | `erp2_shared_dev_item_transitem_np` |
| `product_process` table | MISSING |
| DB-backed Routing route smoke | BLOCKED by fixture/schema readiness |

Classification of this limitation: environment / fixture readiness. It is not classified as a Routing API code defect because sqlite-backed automated tests cover the required contract and pass.

## 9. Code / Document Changes

| Path | Purpose |
|---|---|
| `restserver/package/common/common.py` | Added Routing status, warning, and source enums |
| `restserver/package/restserver/api/v2/routing.py` | Added Routing / Process Flow read-only service and executors |
| `restserver/package/restserver/api/v2/routing_uri.py` | Added Routing v2 GET routes |
| `restserver/package/restserver/app.py` | Registered Routing v2 blueprint |
| `restserver/tests/test_routing_process_flow_api.py` | Added routing service and read-only route tests |
| `docs/spec/api/routing.md` | Added formal Routing API document |
| `docs/spec/api/index.md` | Added routing API index entry |

## 10. Limitations

1. No Routing write, Process Master write, Product write, approval, release, or freeze endpoint was added.
2. No Scheduling / Capacity execution behavior was implemented.
3. No Packaging Specification implementation was added; packaging is read-only context only.
4. No Manufacturing Definition implementation was added.
5. No Costing / valuation behavior was added.
6. No Production endpoint, Production data, migration, Source-of-Truth transition, Cutover, or Go-Live was performed.
7. Resource eligibility remains not governed until an accepted physical source is defined.
8. Shared DEV real DB smoke requires Engineering B / data fixture update to include Routing source tables.

## 11. Final Classification

**ROUTING_PROCESS_FLOW_READONLY_API_IMPLEMENTED_TESTED_SHARED_DEV_FIXTURE_TABLE_PENDING**

This means the read-only Routing / Process Flow API implementation, formal API document, and automated tests are complete. DB-backed Shared DEV smoke is pending fixture/schema readiness for routing source tables.

