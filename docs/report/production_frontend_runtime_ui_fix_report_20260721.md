# Production Frontend Runtime and UI Fix Report

Date: 2026-07-21

## Scope

- Screen: Production Workspace (`/production`)
- Frontend files:
  - `src/app/production/page.tsx`
  - `src/services/production-api.ts`
  - `src/hooks/use-production-dashboard.ts`
  - `src/i18n/production-enums.ts`
  - `src/types/production.ts`
- Backend verification:
  - Confirmed the production dashboard and work order detail API already provide `plannedStartTimestamp` and `plannedEndTimestamp`.
  - No backend code change was required for the date display issue.

## Issues Fixed

1. Fixed runtime crash when `productionData.orders` is an empty array.
   - Root cause: the page initialized selected order with `productionData.orders[0].id`.
   - Fix: use optional fallback and derived selected order logic.

2. Fixed `NaN%` and unstable progress bar width.
   - Added safe numeric helpers for percentage and progress width.
   - Percentage display is formatted to 2 decimal places.
   - Hour and person-hour display is formatted to 2 decimal places.

3. Fixed blank production date display.
   - Frontend now uses `plannedStartTimestamp` first and falls back to actual timestamps when available.
   - Empty date/time values display `-` instead of a blank string.

4. Fixed flow status content.
   - Detail workflow now displays the planned operational flow:
     `Work order -> Material -> Production -> Quality -> Inventory`.
   - MES events are no longer rendered as the primary workflow steps.
   - Mock and API fallback data are normalized to the same workflow structure.

5. Fixed duplicated/raw alert boxes.
   - Repeated production alerts are grouped by alert type and comment code.
   - Raw keys such as `production.alert.capacity_config_missing` are converted through the frontend i18n enum dictionary.
   - Alert cards display a grouped count when the same alert appears multiple times.

## Verification

- `npm.cmd run lint`: Passed
- `npm.cmd run build`: Passed
- Browser smoke test on `http://127.0.0.1:3000/production`: Passed
  - No `Runtime TypeError`
  - No `Cannot read properties of undefined`
  - No `NaN`
  - No raw `production.alert.*` key visible
  - Flow status includes work order, material, production, quality, inventory steps
