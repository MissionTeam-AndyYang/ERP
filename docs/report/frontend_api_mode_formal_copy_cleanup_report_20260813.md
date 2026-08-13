# Frontend API Mode Formal Copy Cleanup Report - 2026-08-13

## Scope
- BOM Center
- Warehouse Center
- Warehouse Inventory Lots
- Warehouse Task Workbench
- Warehouse Analytics
- Orders Dashboard
- Production Dashboard
- Purchasing Center

## Changes
- Removed the BOM Center bottom explanatory block `版本視角 / 直接明細 / 產品關聯` because it was a development/design note area, not a formal operation area.
- Kept formal BOM product relation information inside the detail panel, where it belongs to the actual business workflow.
- Replaced development-stage visible copy such as `Version State`, `BOM Detail`, `workflow`, `read-only`, `V1`, and API implementation notes with user-facing business language.
- Kept the API/Mock data source toggle because it is an intentional development-stage control requested by the project team.

## Verification Plan
- Run keyword scan for development-stage visible copy in completed frontend screens.
- Run frontend lint.
- Run frontend production build.

## Verification Result
- Keyword scan passed for requested BOM strings: `Version State`, `BOM Detail`, `由後端 versionStateCode`, `版本視角`, `直接明細`.
- `npm run lint` passed.
- `npm run build` passed.
- Local route smoke test passed with HTTP 200 for:
  - `/bom`
  - `/warehouse`
  - `/warehouse/inventory/lots`
  - `/warehouse/task-workbench`
  - `/warehouse/analytics`
  - `/orders`
  - `/production`
  - `/purchasing`
