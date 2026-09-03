# Item / Transaction Item Frontend Governed Integration Report

Date: 2026-09-03  
Work Package: ERP2-UX-ITEM-TRANSITEM-GOV-IMPL-001  
Scope: Bounded non-production Frontend / UX integration  

## Summary

The `/items` frontend has been updated to support governed Item / Transaction Item read-only integration:

- Item dashboard through `GET /api/v2/items/dashboard`.
- Transaction Item dashboard through `GET /api/v2/transitems/dashboard`.
- Item detail drilldown through `GET /api/v2/items/{item_no}/detail`.
- Company detail drilldown through `GET /api/v2/transitems/companies/{company_no}/detail`.
- Transaction item detail drilldown through `GET /api/v2/transitems/transitems/{transaction_item_no}/detail`.
- Customer / supplier relationship context is shown through company summary, payment terms, contract summary, and transaction item linkage.

Mock data remains available only through the explicit UI data-source toggle. API mode does not silently fall back to mock data.

## Environment

| Item | Value |
|---|---|
| Frontend root | `C:\Users\andyy\Desktop\Codex-workspace\projects\ERP-2.0` |
| Node | `v24.15.0` |
| npm | `11.12.1` |
| package-lock lockfileVersion | `3` |
| Backend base URL used for validation | `http://127.0.0.1:5016` |
| API token used | `test-token` |
| Timezone header | `Asia/Taipei` |

## Validation Commands

```powershell
npm run lint
npm run build
npm run test
```

| Check | Result | Evidence |
|---|---|---|
| `npm run lint` | PASS | ESLint completed with no errors. |
| `npm run build` | PASS | Next.js production build completed successfully; `/items` was included in generated routes. |
| `npm run test` | GAP | `FRONTEND_TEST_SCRIPT_STANDARDIZATION_GAP`: `package.json` does not currently define a `test` script. |

## Real Backend Validation

Backend service start:

```powershell
$env:PYTHONPATH='restserver'
$env:FLASK_HOST='127.0.0.1'
$env:FLASK_PORT='5016'
$env:FLASK_DEBUG='false'
$env:ERP2_WH_INV_STAGING_MODE='1'
.\.venv\Scripts\python.exe restserver\package\restserver\run.py
```

Backend service started on `http://127.0.0.1:5016`, but DB-backed dashboard requests returned HTTP 400 because MariaDB was not reachable:

```txt
mariadb.OperationalError: Can't connect to server on 'localhost' (10061)
```

Validated requests:

| Endpoint | Result |
|---|---|
| `GET /api/v2/items/dashboard?count=5` | HTTP 400, DB connection refused |
| `GET /api/v2/transitems/dashboard?count=5` | HTTP 400, DB connection refused |
| `GET /api/v2/items/dashboard?count=1` without token | HTTP 400 |

## Browser Smoke

Frontend dev server was started with:

```powershell
$env:NEXT_PUBLIC_API_BASE_URL='http://127.0.0.1:5016'
$env:NEXT_PUBLIC_API_TOKEN='test-token'
$env:NEXT_PUBLIC_API_TIMEZONE='Asia/Taipei'
npm run dev -- --hostname 127.0.0.1 --port 3022
```

Browser check for `/items` confirmed:

| UX Behavior | Result |
|---|---|
| Dashboard shell renders | PASS |
| API mode shows error when backend returns 400 | PASS |
| API mode silently shows mock rows | PASS, not observed |
| Development-only `Local Candidate` copy appears | PASS, not observed |
| Loading state appears while request is pending | PASS |
| Empty state appears when data is empty after error | PASS |
| Browser console errors | PASS, none observed |

Additional UI smoke was performed in explicit mock mode only to verify the new detail panel interaction surface. This is not counted as governed real-backend data evidence.

| UI Behavior In Explicit Mock Mode | Result |
|---|---|
| User-selected mock mode renders dashboard rows | PASS |
| Clicking a material item `查看` button opens the detail panel | PASS |
| Material detail panel shows inventory, BOM usage, and recent batch sections | PASS |
| Mock mode shows no API error | PASS |

## Detail Drilldown Behavior

Implemented frontend drilldown behavior:

| User action | API |
|---|---|
| View material item detail | `/api/v2/items/{item_no}/detail` |
| View company detail | `/api/v2/transitems/companies/{company_no}/detail` |
| View transaction item detail | `/api/v2/transitems/transitems/{transaction_item_no}/detail` |

Real detail data could not be validated in this run because the dashboard endpoints could not return selectable real records while MariaDB was unavailable. This is an environment blocker, not a frontend contract blocker.

## Safe Stop / Re-entry Condition

Safe Stop branch: real-backend data validation is blocked until the backend environment can connect to MariaDB.

CIO / CTO re-entry condition:

1. Start MariaDB with the expected ERP test database.
2. Start restserver on `http://127.0.0.1:5016`.
3. Re-run `/items` browser smoke in API mode.
4. Verify dashboard records, then click one material item, one company, and one transaction item to confirm detail API rendering.

## Documentation Alignment

Updated `docs/engineering/FRONTEND_ENVIRONMENT_SETUP_GUIDE_20260619.md` so API mode error handling matches the current rule:

- API error in API mode shows an error state.
- Valid API empty arrays show real empty states.
- Mock data is shown only when the user intentionally selects mock mode.
