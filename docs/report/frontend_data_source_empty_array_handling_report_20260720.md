# Frontend Data Source And Empty Array Handling Report

Date: 2026-07-20

## Scope

This report covers the frontend rule:

- API success responses with empty arrays must be rendered as real empty data.
- Mock data must not be displayed when the backend successfully returns an empty array.
- During development, users can explicitly switch between API data and mock data.

## Updated Areas

| Area | Change |
| --- | --- |
| Orders Workspace | Added API/Mock source toggle and removed empty-array mock replacement for `orders`. |
| Production Workspace | Added API/Mock source toggle and removed empty-array mock replacement for `orders`, `weekSchedule`, and `alerts`. |
| Warehouse Overview | Added API/Mock source toggle and removed empty-array mock replacement for dashboard KPI/category/capacity arrays. |
| Warehouse Task Workbench | Added API/Mock source toggle for workbench and task detail calls. |
| Warehouse Inventory Lot List | Added API/Mock source toggle for lot list and selected lot detail calls. |
| Warehouse Analytics | Added API/Mock source toggle for all analytics endpoints. |

## Behavior Rules

| Scenario | Expected UI Behavior |
| --- | --- |
| User selects API and backend returns `[]` | Show empty state / zero rows based on the real API response. |
| User selects API and request fails | Use controlled mock fallback and show warning. |
| User selects Mock | Use mock data directly without calling the backend API for that screen. |
| Detail API returns empty nested arrays | Show empty detail sections rather than backfilling mock detail rows. |

## Verification Results

| Check | Result |
| --- | --- |
| `npm.cmd run lint` | Passed |
| `npm.cmd run build` | Passed |
| HTTP smoke `/orders` | Passed, status `200` |
| HTTP smoke `/production` | Passed, status `200` |
| HTTP smoke `/warehouse` | Passed, status `200` |
| HTTP smoke `/warehouse/task-workbench` | Passed, status `200` |
| HTTP smoke `/warehouse/inventory/lots` | Passed, status `200` |
| HTTP smoke `/warehouse/analytics` | Passed, status `200` |

## Notes

The data source toggle is intended for the current development phase. The default mode remains API so backend integration testing observes real backend data first.
