# BOM Center Frontend API Integration Report

Date: 2026-08-12
Scope: `BOMCenterScreen` (`/bom`)
Proposal basis: `docs/spec/api-proposal/bom_center_proposal.md`

## Implementation Summary

- Replaced the previous mock-oriented `/bom` page with a V1 read-only BOM Center screen.
- Integrated the engineer-confirmed backend APIs:
  - `GET /api/v2/bom/dashboard`
  - `GET /api/v2/bom/{bom_no}/detail`
- Added API / Mock source toggle.
- Added keyword search, `versionStateCode` filter, pagination, and page size controls.
- API mode preserves real backend behavior:
  - Empty arrays render as empty states.
  - API errors render an error banner.
  - Mock data is shown only when the user explicitly selects Mock mode.
- Added frontend enum-to-label mapping with multi-language support for:
  - Unit enum
  - `versionStateCode`
  - linked product `level`
  - linked product `itemType`
- Added selected BOM detail panel with version switching and fallback summary display.
- Updated `docs/spec/api-proposal/planned_screen_list_naming.md` to mark BOM Center frontend integration status.

## Verification

| Check | Result |
| --- | --- |
| `npm.cmd run lint` | Pass |
| `npm.cmd run build` | Pass |
| Browser smoke: `/bom` API mode | Pass |
| Browser smoke: API error does not show mock fallback | Pass |
| Browser smoke: Mock mode displays BOM V1 data | Pass |
| Browser smoke: page size and version status controls | Pass |
| Browser smoke: selected BOM detail panel displays material and linked product data | Pass |

## Runtime Review Notes

- The frontend calls dashboard with `keyword`, `versionStateCode`, `start`, and `count`.
- The frontend calls detail with selected `bomNo` and selected `version`.
- The page intentionally excludes costing, quotation, contract, mutation, approval, and recursive bom1 / bom2 tree views per V1 scope.
- Local browser smoke used `http://localhost:3000/bom`. API mode displayed the expected error banner when the local backend endpoint was unavailable, while Mock mode showed BOM sample data, material rows, linked product rows, pagination, and version status filtering.
