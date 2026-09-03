# Backend API Response - ERP2-BOM-PRODUCT-STRUCTURE-RO-EXEC-001-BE-001

## 1. Scope

| Item | Value |
| --- | --- |
| Authorization | ERP2-CIO-BOM-PRODUCT-STRUCTURE-RO-EXEC-001 |
| Work Item | ERP2-BOM-PRODUCT-STRUCTURE-RO-EXEC-001-BE-001 |
| Implementation Type | Bounded non-production Backend/API read-only implementation |
| Product Semantics | Finished-product-root Product Structure visibility |
| Boundary | No Product write, no Recipe/Formula implementation, no migration, no cutover, no Go-Live |

## 2. Files Changed

| File | Purpose |
| --- | --- |
| `restserver/package/common/common.py` | Added shared Product Structure status/warning enum codes |
| `restserver/package/restserver/api/v2/bom.py` | Added Product Structure read-only service/executor logic |
| `restserver/package/restserver/api/v2/bom_uri.py` | Added Product Structure v2 route |
| `restserver/tests/test_bom_center_api.py` | Added Product Structure tests while preserving existing BOM Center coverage |
| `docs/spec/api/bom.md` | Added formal API documentation for the new route |

## 3. Route / Contract

New route:

`GET /api/v2/bom/product-structure/{product_no}`

Supported query parameters:

| Parameter | Meaning |
| --- | --- |
| `productVersion` | Optional product version; default resolves from `product_spec`, then `product.version` |
| `depth` | Optional expansion depth; default 3, bounded 1 to 5 |
| `effectiveDate` | Optional timestamp for BOM version-state evidence |

Response payload exposes:

- `rootProduct`
- `bomEvidence`
- `children`
- nested child nodes
- `hasChildren`
- `warnings`

The response uses enum/code fields only for status/warning semantics. It does not return UI translation fallback strings.

## 4. Data-Access Approach

Implementation is ORM-first and uses existing table models:

| Table | Use |
| --- | --- |
| `product` | root product and product child identity |
| `product_spec` | product version and parent-child structure relationship |
| `inproduct` | WIP / semi-finished child identity |
| `inproduct_bom_spec` | WIP to raw/material BOM bridge |
| `bom` | BOM version evidence and version status |
| `bom_item` | BOM direct raw/material children |
| `material` | raw material / supplies / film identity |
| `goods` | goods identity fallback |

No new repository class was introduced only for naming conformity. No Product write behavior was added.

## 5. Compatibility Evidence

Existing v2 BOM endpoints were preserved:

| Endpoint | Real HTTP Smoke Result |
| --- | --- |
| GET /api/v2/bom/dashboard | PASS, HTTP 200, API code 0 |
| GET /api/v2/bom/{bom_no}/detail | PASS, HTTP 200, API code 0 |

New Product Structure endpoint:

| Endpoint | Real HTTP Smoke Result |
| --- | --- |
| GET /api/v2/bom/product-structure/{product_no} | PASS, HTTP 200, API code 0 |

Real HTTP smoke was executed against Shared DEV formal ERP-compatible fixture using wrapper-based child-process DB configuration and non-production token/session test treatment.

## 6. Tests

Automated backend tests:

| Command | Result |
| --- | --- |
| `.venv\Scripts\python.exe -m pytest restserver/tests/test_bom_center_api.py -q` | 6 passed |
| `.venv\Scripts\python.exe -m pytest restserver/tests -q` | 82 passed |

Product Structure tests added:

- expands finished-product root to WIP and primitive raw-material children;
- returns missing structure status and warning when product spec is missing.

## 7. Read-Only Negative Control

The new API is registered only with HTTP GET. No POST, PUT, DELETE, schema mutation, Product write, Recipe/Formula write, or migration behavior was added.

Shared DEV validation used the read-only participant credential through the Engineering B wrapper. Prior service-window validation confirmed the participant credential rejects unauthorized writes; this implementation did not require any write attempt.

## 8. Known Limitations

1. The first slice expands product structure through current ORM-backed `product_spec`, `inproduct_bom_spec`, and `bom_item` evidence. It does not implement full Recipe/Formula semantics.
2. Legacy recursive `bom1` / `bom2` SQL trees were reviewed as evidence but not adopted for this minimum API slice, because the current formal fixture supports the ORM-backed path.
3. `depth` is bounded to 5 to keep read-only tree expansion predictable.
4. Missing product spec, missing BOM items, missing item master, depth limit, and circular reference are returned as warning codes for frontend handling.

## 9. Final Classification

**PRODUCT_STRUCTURE_READ_ONLY_API_IMPLEMENTED_COMPATIBILITY_PRESERVED_TESTS_PASS_SHARED_DEV_SMOKE_PASS**

This classification means the bounded Product-oriented read-only Product Structure API capability has been implemented, documented, tested, and smoke-validated without expanding authority beyond the accepted CTO scope.
