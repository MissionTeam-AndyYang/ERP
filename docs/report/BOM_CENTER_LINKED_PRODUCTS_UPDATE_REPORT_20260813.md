# BOM Center Linked Products Update Report

Date: 2026-08-13  
Scope: `GET /api/v2/bom/{bom_no}/detail` linkedProducts response update

## Change Summary

- Updated backend `linkedProducts` response from one row per `product_spec` to one row per normalized product version.
- Removed `linkedProducts[].level`.
- Added `linkedProducts[].productName`.
- Added `linkedProducts[].productCategory`.
- Added `linkedProducts[].contents[]` for one or more related content items.
- Added `_1` parent product handling:
  - API returns normalized `productNo` without `_1`.
  - If both `product_no` and `product_no + "_1"` exist for the same version, contents use the `_1` parent rows.
- Updated formal API document `docs/spec/api/bom.md`.
- Updated frontend BOM mapper, types, mock data, and display for the new structure.

## Verification

| Check | Command | Result |
|---|---|---|
| BOM backend unit tests | `.\\.venv\\Scripts\\python.exe -m pytest restserver/tests/test_bom_center_api.py -q` | PASS, 4 passed |
| Frontend lint | `npm.cmd run lint` | PASS |

## Notes

- Initial `python -m pytest restserver/tests/test_bom_center_api.py -q` could not run because the system Python did not have `pytest`; the project `.venv` test command was used successfully.
- No database migration was required because this change only modifies API aggregation and response structure.
