# Frontend UX Response - ERP2 Packaging Specification Read-Only

Date: 2026-09-04  
Scope: `ERP2-CIO-PACKAGING-SPECIFICATION-RO-RDY-001` frontend/UX implementation  
Route: `/packaging`  
Screen Code: `PackagingSpecificationScreen`

## Summary

Implemented the read-only Packaging Specification frontend screen and API integration support for:

- `GET /api/v2/packaging-specification/overview`
- Product scenario: `itemCategory=5`, with optional `productVersion`
- WIP scenario: `itemCategory=4`, with downstream product packaging context warnings

The screen follows the same API/Mock behavior used by current implemented ERP 2.0 frontend modules:

- API mode is default.
- API errors show an error message.
- API mode does not silently render mock data.
- Empty arrays are shown as empty states.
- Mock mode is only available through explicit user selection.

## Implemented Files

| File | Purpose |
| --- | --- |
| `src/app/packaging/page.tsx` | New read-only Packaging Specification screen. |
| `src/types/packaging.ts` | Frontend types for packaging subject, specs, lines, source lineage, warnings, and boundary. |
| `src/services/packaging-api.ts` | API client, payload mapper, status/source/warning mapping, controlled error result. |
| `src/hooks/use-packaging-overview.ts` | Client hook for API/Mock data loading. |
| `src/mock/packaging.ts` | Manual mock dataset for Product and WIP scenarios. |
| `src/layouts/app-layout.tsx` | Added Packaging Specification navigation item. |
| `src/i18n/dictionary.ts` | Added `nav.packaging` labels for zh-TW, en, ja, vi. |
| `docs/spec/api-proposal/packaging_specification_static_preview.html` | Static preview for engineering review and UX discussion. |
| `docs/spec/api-proposal/packaging_specification_ro_proposal.md` | Frontend/API integration proposal and local DEV smoke requirements. |
| `docs/spec/api-proposal/planned_screen_list_naming.md` | Added Packaging Specification roadmap entries and naming. |

## Screen Coverage

| Code | Status | Notes |
| --- | --- | --- |
| `PackagingSpecificationScreen` | Implemented | `/packaging` route. |
| `PackagingSubjectSummarySection` | Implemented | Product/WIP identity, version, units, source, KPI summary. |
| `PackagingSpecLevelView` | Implemented | Packaging level, BOM, count, weight, source. |
| `PackagingBomLineDetailView` | Implemented | Selected packaging BOM line details. |
| `PackagingSourceWarningPanel` | Implemented | Source lineage, readiness, warnings, and read-only boundary. |
| `PackagingDomainNavigationView` | Implemented | Links to Product/WIP 360, BOM, Routing, and Warehouse inventory lots. |

## Data Mapping Notes

The frontend consumes these backend payload groups:

- `requestIdentity`
- `subject`
- `summary`
- `packagingSpecs[]`
- `packagingSpecs[].lines[]`
- `sourceLineage`
- `warnings[]`
- `moduleReadiness[]`
- `capabilityBoundary`

Frontend enum/string mapping is handled for:

- packaging level: `0` other, `1` box specification, `2` group specification
- unit labels through the existing BOM unit label helper
- source code labels
- warning code labels
- status tones and status labels

## Boundary Confirmation

No write controls were added. The screen does not implement:

- Packaging create/update
- Packaging approval/release
- Product/WIP write
- BOM write
- Production execution
- Source-of-Truth transition
- Cutover
- Go-Live

## Verification

| Check | Result | Evidence |
| --- | --- | --- |
| `npm run lint` | PASS | ESLint completed with no errors. |
| `npm run build` | PASS | Next.js production build completed; `/packaging` included in generated routes. |
| Browser smoke - API mode | PASS | Frontend-only test returned controlled API error/empty state and did not render mock packaging rows. |
| Browser smoke - Mock Product | PASS | Manual mock mode displayed Product packaging levels, BOM rows, and BOM line detail. |
| Browser smoke - Mock WIP | PASS | WIP scenario displayed `INP-SD-001`, WIP identity, downstream product packaging warning, and disabled product version input. |
| Browser smoke - write controls | PASS | No buttons matching create/update/delete/approve/release/save/submit labels were present. |

## Local Full-Stack DEV Notes

For full backend validation, run the frontend with `NEXT_PUBLIC_API_BASE_URL` pointing to the Flask server that exposes:

```text
GET /api/v2/packaging-specification/overview
```

Recommended first smoke path:

1. Open `/packaging`.
2. Keep data source as API mode.
3. Query a known Product item with `itemCategory=5` and a product version.
4. Confirm Product packaging specs and line details appear.
5. Switch to WIP and query a known WIP item with `itemCategory=4`.
6. Confirm downstream product packaging context warnings are visible when applicable.
7. Confirm no mock data appears after API failure or empty arrays.

## Remaining Runtime Review

The frontend-only smoke used the local Next.js server without a Flask API base URL, so API mode correctly showed a controlled backend-unavailable state. A remote/local engineer should run the full stack with the real Flask API to confirm database-backed rows for actual Product/WIP fixtures.

