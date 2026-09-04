# Packaging Specification Read-Only Frontend / API Integration Proposal

Status: Frontend implemented as bounded read-only API integration  
Route: `/packaging`  
Screen Code: `PackagingSpecificationScreen`  
Primary API: `GET /api/v2/packaging-specification/overview`

## Purpose

Provide a clear read-only screen for Product / WIP packaging specification visibility. The screen helps users inspect:

- packaging level: 箱規、組規、其他
- packaging BOM number and packaging BOM name
- specification count, unit, weight, master unit, master weight
- BOM2 line items: child item, quantity, weight, loss fields, process count, comment
- source lineage from subject, packaging spec, packaging BOM master, and packaging BOM lines
- controlled warnings for missing or downstream-derived packaging context

The screen does not create, update, approve, release, or execute packaging work.

## Frontend Screen Scope

| Code | Type | Display Name | Route / Location | Status |
| --- | --- | --- | --- | --- |
| `PackagingSpecificationScreen` | Screen | 包裝規格唯讀檢視 | `/packaging` | Implemented |
| `PackagingSubjectSummarySection` | View | 包裝主體摘要區 | Top summary in `PackagingSpecificationScreen` | Implemented |
| `PackagingSpecLevelView` | View | 包裝階層與規格區 | Main table in `PackagingSpecificationScreen` | Implemented |
| `PackagingBomLineDetailView` | View | 包材 BOM 明細區 | Detail table below selected packaging spec | Implemented |
| `PackagingSourceWarningPanel` | Panel | 來源與警示面板 | Right-side panel | Implemented |
| `PackagingDomainNavigationView` | View | 關聯模組導覽區 | Bottom navigation | Implemented |

## API Contract Used By Frontend

Endpoint:

```http
GET /api/v2/packaging-specification/overview?itemNo={itemNo}&itemCategory={4|5}&productVersion={productVersion?}&effectiveDate={unix?}
```

Query:

| Field | Required | Description |
| --- | --- | --- |
| `itemNo` | Yes | Product or WIP item number. |
| `itemCategory` | Yes | `5` = Product, `4` = WIP. |
| `productVersion` | Product recommended | Product version. WIP may omit. |
| `effectiveDate` | No | Optional effective date timestamp. |

Frontend consumes these response groups:

| Payload Group | Frontend Usage |
| --- | --- |
| `requestIdentity` | Confirms queried item/category/version. |
| `subject` | Displays Product/WIP identity, name, version, units, and source. |
| `summary` | Displays spec count, BOM count, level count, material line count, total count, total weight. |
| `packagingSpecs[]` | Displays packaging level rows and selected BOM detail. |
| `packagingSpecs[].lines[]` | Displays packaging material lines. |
| `sourceLineage` | Displays explicit source categories and source codes. |
| `warnings[]` | Displays controlled warning messages. |
| `moduleReadiness[]` | Displays readiness/status for packaging specification module. |
| `capabilityBoundary` | Confirms read-only boundaries. |

## Data Source Behavior

- Default mode is API mode.
- API mode calls the backend endpoint directly.
- If API fails, the screen shows an error and does not render mock data.
- If API returns empty arrays, the screen shows true empty states and does not fill demo rows.
- Mock mode is only available through the explicit API/Mock switch.

## Product / WIP Behavior

Product scenario:

- Query `itemCategory=5`.
- Displays direct `product_bom_spec` packaging specs.
- Product version input is enabled.

WIP scenario:

- Query `itemCategory=4`.
- Product version input is disabled.
- If backend returns packaging context from downstream product linkage, the screen displays the WIP context and warning instead of treating it as an error.

## Source And Warning Rules

The frontend maps these source codes into user-readable labels:

| Source Code | Display Meaning |
| --- | --- |
| `product` | 製成品主檔 |
| `inproduct` | 在製品主檔 |
| `product_bom_spec` | product_bom_spec 包裝規格 |
| `bom2_number` | bom2_number 包材 BOM 主檔 |
| `bom2` | bom2 包材 BOM 明細 |
| `product_spec` | product_spec 下游產品關聯 |
| `not_recorded` | 未建立 |

The frontend maps these warning codes into user-readable messages:

| Warning Code | Display Meaning |
| --- | --- |
| `missing_packaging_spec` | 尚未建立包裝規格。 |
| `missing_packaging_bom_master` | 包材 BOM 主檔尚未建立或未回填。 |
| `missing_packaging_bom_lines` | 包材 BOM 明細尚未建立或未回填。 |
| `wip_packaging_context_from_downstream_product` | 在製品包裝情境來自下游製成品關聯，需保留來源產品識別。 |
| `module_unavailable` | 包裝規格模組資料取得失敗。 |

## Read-Only Boundary

This implementation does not add:

- Packaging write / update
- Packaging approval / release
- Product or WIP write
- BOM write
- Production execution
- Source-of-Truth transition
- Cutover
- Go-Live

## Local Full-Stack DEV Requirements

Recommended smoke path:

1. Start backend with the local Flask server that exposes `/api/v2/packaging-specification/overview`.
2. Start frontend with `NEXT_PUBLIC_API_BASE_URL` pointing to the backend host.
3. Open `/packaging`.
4. Confirm API mode renders true backend data or a true API error.
5. Switch to mock mode only when validating the frontend layout without backend data.
6. Test Product and WIP scenario toggles.
7. Confirm no write controls are shown.

Expected frontend checks:

- lint passes
- production build passes
- browser smoke confirms route renders
- API mode does not display mock rows after API failure
- mock mode can be manually selected

