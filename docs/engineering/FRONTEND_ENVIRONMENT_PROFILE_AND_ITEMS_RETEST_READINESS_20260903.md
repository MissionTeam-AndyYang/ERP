# Frontend Environment Profile and `/items` Real-Backend Retest Readiness

Date: 2026-09-03  
Work Package: ERP2-UX-ENV-PROFILE-AND-RETTEST-RDY-001  
Scope: Frontend / UX profile and retest readiness only  

## 1. Supported Runtime

| Item | Supported / Observed Value |
|---|---|
| Frontend root | `C:\Users\andyy\Desktop\Codex-workspace\projects\ERP-2.0` |
| Node requirement | `>=20.9.0`, inherited from installed Next.js package |
| Observed Node | `v24.15.0` |
| Observed npm | `11.12.1` |
| Next.js | `16.2.6` |
| Package manager | npm |
| Lockfile | `package-lock.json`, lockfileVersion `3` |

Use Node 22 LTS or newer for shared development unless the engineering environment standard pins another Node version that still satisfies `>=20.9.0`.

## 2. Dependency Definition

The frontend is a single Next.js app at repository root. It is not currently configured as a monorepo or npm workspace.

Authoritative dependency files:

- `package.json`
- `package-lock.json`

Do not delete or regenerate `package-lock.json` without team agreement.

## 3. Commands

Install from the lockfile:

```powershell
npm ci
```

Run lint:

```powershell
npm run lint
```

Run production build:

```powershell
npm run build
```

Run local development server:

```powershell
npm run dev
```

Run on an explicit local port:

```powershell
npm run dev -- --hostname 127.0.0.1 --port 3001
```

Run production preview after build:

```powershell
npm run start
```

Run production preview on an explicit local port:

```powershell
npm run start -- --hostname 127.0.0.1 --port 3001
```

## 4. Test Script Status

`package.json` currently does not define `test`.

Treatment:

- Record `FRONTEND_TEST_SCRIPT_STANDARDIZATION_GAP` in validation reports until a team-standard frontend test command is added.
- Do not treat `npm run test` failure as a product behavior failure while the script is absent.
- Required validation commands for the current frontend are `npm run lint` and `npm run build`, plus route smoke testing.

## 5. Frontend API Configuration

Create `.env.local` for local or shared development. This file is local-only and must not be committed.

```txt
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:5016
NEXT_PUBLIC_API_TIMEZONE=Asia/Taipei
NEXT_PUBLIC_API_TOKEN=test-token
```

Configuration classes:

| Class | `NEXT_PUBLIC_API_BASE_URL` | Usage |
|---|---|---|
| Local Development | `http://127.0.0.1:<backend-port>` | Engineer machine with local restserver. |
| Shared DEV / Integration | Engineering-provided shared DEV API URL | Cross-role API integration validation. |
| Controlled TEST | Test-environment API URL approved by Engineering B / Backend | Governed retest and release evidence. |

Do not use Production API URLs, Production credentials, or Production data for this retest package.

## 6. Mock / Fixture Rules

- API mode must call the backend API and must not silently fall back to mock data.
- If API mode receives an error, the page must show an error state.
- If API mode receives valid empty arrays, the page must show real empty states.
- Mock data may be used only when the user explicitly selects the mock / demonstration data source toggle.
- Manual mock-mode smoke can verify UI mechanics, but it is not governed real-backend evidence.

## 7. Clean Rebuild Procedure

From the repository root:

```powershell
git status
npm ci
npm run lint
npm run build
```

Expected result:

- `npm ci` installs from `package-lock.json`.
- `npm run lint` passes.
- `npm run build` passes and includes `/items` in the generated route list.

If `npm run dev` reports `Missing script: "dev"`, verify the current directory. The repository root `package.json` defines `dev`.

## 8. `/items` Real-Backend Retest Procedure

Prerequisites from Engineering B / Backend:

1. Backend restserver is running on the agreed non-production URL.
2. MariaDB or the agreed backing database is reachable from restserver.
3. Required `/api/v2/items/*` and `/api/v2/transitems/*` endpoints return HTTP 200 with the test dataset.
4. CORS allows `Content-Type`, `Accept`, `x-timezone`, and `x-auth-token`.
5. A non-production API token is available if token auth is enabled.
6. Test data includes at least one material item, one company, one transaction item, and one linked contract where possible.

Recommended direct API precheck:

```powershell
$headers=@{'x-auth-token'='test-token';'x-timezone'='Asia/Taipei'}
Invoke-RestMethod -Uri 'http://127.0.0.1:5016/api/v2/items/dashboard?count=5' -Headers $headers
Invoke-RestMethod -Uri 'http://127.0.0.1:5016/api/v2/transitems/dashboard?count=5' -Headers $headers
```

Start frontend:

```powershell
$env:NEXT_PUBLIC_API_BASE_URL='http://127.0.0.1:5016'
$env:NEXT_PUBLIC_API_TOKEN='test-token'
$env:NEXT_PUBLIC_API_TIMEZONE='Asia/Taipei'
npm run dev -- --hostname 127.0.0.1 --port 3001
```

Open:

```txt
http://127.0.0.1:3001/items
```

## 9. Dashboard Checks

Verify in API mode:

- Source badge indicates backend/API mode.
- No mock/demo rows are shown unless mock mode is selected.
- KPI counts match direct API totals.
- Material item table renders `items[]`.
- Transaction item view renders `transactionItems[]`.
- Customer / supplier view renders `companies[]`.
- Search keyword triggers API-mode refresh and preserves no-silent-mock behavior.
- Refresh button re-requests backend data.

## 10. Detail Checks

Item detail:

- Click `查看` on one material item row.
- Confirm the frontend calls `/api/v2/items/{item_no}/detail`.
- Confirm the detail panel renders item identity, inventory summary, BOM usage, recent batches, and maintenance suggestions.
- Empty `bomUsage[]`, `recentBatches[]`, or `maintenanceSuggestions[]` must render empty states, not mock rows.

Company detail:

- Switch to `客戶／廠商`.
- Click `查看` on one company card.
- Confirm the frontend calls `/api/v2/transitems/companies/{company_no}/detail`.
- Confirm the detail panel renders company identity, contact fields, receivable/payment terms, transaction items, and contracts.
- Empty `transactionItems[]` or `contracts[]` must render empty states.

Transaction item detail:

- Switch to `交易品項`.
- Click `查看` on one transaction item card.
- Confirm the frontend calls `/api/v2/transitems/transitems/{transaction_item_no}/detail`.
- Confirm the detail panel renders transaction item identity, linked company, linked item, contracts, pricing, and data quality state.
- Empty `contracts[]` or `linkedItems[]` must render empty states.

## 11. Error / Empty State Checks

API error check:

- Stop backend or point `NEXT_PUBLIC_API_BASE_URL` to an unavailable non-production URL.
- Open `/items` in API mode.
- Expected: visible error message saying the page did not switch to demonstration data.
- Expected: no mock sample rows.

Valid empty data check:

- Use a backend query/test dataset that returns valid empty arrays.
- Expected: KPI and sections render real zero/empty states.
- Expected: no mock sample rows.

Auth / permission check:

- Remove `NEXT_PUBLIC_API_TOKEN` when token auth is required.
- Expected: backend returns an auth error and frontend shows API error state.
- Expected: no mock sample rows.

## 12. Current Safe Stop

As of this readiness package, real-backend retest is blocked if the backend can start but cannot connect to MariaDB:

```txt
mariadb.OperationalError: Can't connect to server on 'localhost' (10061)
```

Re-enter governed `/items` real-backend validation only after Engineering B / Backend confirms the non-production backend URL, token, database reachability, and dataset readiness.

