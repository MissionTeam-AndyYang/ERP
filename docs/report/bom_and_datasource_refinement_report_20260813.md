# BOM Center and Data Source Refinement Test Report

Date: 2026-08-13

## Scope

- Updated BOM Center frontend mapping for `/api/v2/bom/{bom_no}/detail` linked product response changes.
- Added product item name and content item name display in the BOM linked product section.
- Standardized data source status badges across completed API-integrated screens.
- Removed development-stage labels such as `API data`, `Mock fallback`, and `PO-first V1` from completed API-integrated screens.
- Ensured Warehouse and Orders API service errors do not switch to mock data in API mode.

## Verification

| Check | Result | Notes |
| --- | --- | --- |
| `npm.cmd run lint` | Pass | ESLint completed without errors. |
| `npm.cmd run build` | Pass | Next.js production build and TypeScript checks completed. |
| BOM linked product fields | Pass | `productName` and `contents[].itemName` are typed, mapped, and rendered as product/content item names. |
| API/Mock controls on completed API-integrated screens | Pass | Checked BOM, Purchasing, Orders, Production, Warehouse, Warehouse Inventory Lots, Warehouse Task Workbench, and Warehouse Analytics. |
| Development-stage source labels removed | Pass | Target screens no longer show `API data`, `Mock fallback`, `PO-first V1`, `EWDB 20260522`, or internal screen component labels. |
| API mode fallback behavior | Pass | Warehouse and Orders service catch paths now return empty API data with errors instead of mock data. Production, Purchasing, and BOM already preserve API-mode errors without automatic mock dashboard fallback. |
| Browser smoke | Pass | Local pages loaded and exposed API/Mock controls; old development-stage source labels were absent. Backend API was not running locally, so API mode correctly showed empty/error states instead of mock content. |

## Updated Screens

- `/bom`
- `/purchasing`
- `/orders`
- `/production`
- `/warehouse`
- `/warehouse/inventory/lots`
- `/warehouse/task-workbench`
- `/warehouse/analytics`

## Notes

- Mock data remains available only when the user explicitly switches the data source to Mock.
- API empty arrays are rendered as empty states and are not replaced with mock data.
- Detail panels may keep the currently selected list summary where the page already uses that as a UI fallback, but they no longer source mock detail data in API error mode.
