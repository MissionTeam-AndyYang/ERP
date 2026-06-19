# ERP 2.0 Frontend Environment Setup Guide

Date: 2026-06-19  
Audience: Frontend engineers, backend engineers who need to run the ERP frontend locally, API reviewers.

## Purpose

This guide helps engineers install and run the ERP 2.0 frontend locally.

Use this when you need to:

- Preview the current Next.js ERP frontend.
- Verify API integration from the browser.
- Run lint/build before submitting changes.
- Confirm whether a page is using real API data or mock fallback data.

## Project Stack

| Area | Technology |
| --- | --- |
| Framework | Next.js App Router |
| Language | React + TypeScript |
| Styling | Tailwind CSS |
| Charts | Recharts |
| Icons | lucide-react |
| Package manager | npm with `package-lock.json` |

## Prerequisites

Install:

1. Git
2. Node.js LTS
3. npm, bundled with Node.js
4. Chrome or Edge browser

Recommended:

- Windows 10/11 with PowerShell.
- Node.js 22 LTS or newer, unless the team standard specifies another LTS version.

Verify tools:

```powershell
git --version
node -v
npm -v
```

If `node` or `npm` is not recognized, reinstall Node.js and reopen PowerShell.

## Repository Location

Recommended local path:

```txt
C:\Users\<user>\Desktop\Codex-workspace\projects\ERP-2.0
```

If cloning fresh:

```powershell
git clone https://github.com/MissionTeam-AndyYang/ERP.git ERP-2.0
cd ERP-2.0
```

If the repository already exists:

```powershell
cd C:\Users\andyy\Desktop\Codex-workspace\projects\ERP-2.0
git status
git pull
```

Do not use `git reset --hard` unless you are certain there are no local changes that need to be preserved.

## Install Dependencies

From the project root:

```powershell
npm ci
```

Use `npm ci` for a clean install from `package-lock.json`.

If this is a first-time setup and `npm ci` fails because the lockfile is out of sync, notify the project owner before using:

```powershell
npm install
```

## Environment Variables

Create a local frontend environment file:

```txt
.env.local
```

Recommended content for local API integration:

```txt
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:5000
NEXT_PUBLIC_API_TIMEZONE=Asia/Taipei
NEXT_PUBLIC_API_TOKEN=
```

Field meaning:

| Variable | Required | Description |
| --- | --- | --- |
| `NEXT_PUBLIC_API_BASE_URL` | Optional | Backend API base URL. If omitted, frontend calls same-origin API paths. |
| `NEXT_PUBLIC_API_TIMEZONE` | Recommended | Sent as `x-timezone`; default is `Asia/Taipei`. |
| `NEXT_PUBLIC_API_TOKEN` | Optional | Sent as `x-auth-token` only when backend token auth is enabled. |

Notes:

- `.env.local` is local-only and should not be committed.
- Restart the dev server after changing `.env.local`.
- If `NEXT_PUBLIC_API_BASE_URL` is unavailable or the API errors, pages may show `Mock fallback`.

## Start Development Server

Default:

```powershell
npm.cmd run dev
```

Open:

```txt
http://localhost:3000
```

If port 3000 is already in use:

```powershell
npm.cmd run dev -- -p 3001
```

Open:

```txt
http://localhost:3001
```

Useful routes:

| Page | URL |
| --- | --- |
| Dashboard | `http://localhost:3000/` |
| Warehouse | `http://localhost:3000/warehouse` |
| Orders | `http://localhost:3000/orders` |
| Production | `http://localhost:3000/production` |
| Quality | `http://localhost:3000/quality` |
| Batches | `http://localhost:3000/batches` |
| AI | `http://localhost:3000/ai` |

## Verify API Source In The UI

Most ERP pages show a source badge near the top:

| Badge | Meaning |
| --- | --- |
| `API data` | The page received data from the backend API. |
| `Mock fallback` | The API was unavailable or errored; frontend is showing fallback data. |
| `Loading API` | The request is still pending. |

Accepted frontend rule:

```txt
API unavailable -> show Mock fallback visibly.
Valid API empty array -> show a real empty state, not mock rows.
```

## Run Checks Before Handoff

Run lint:

```powershell
npm.cmd run lint
```

Run production build:

```powershell
npm.cmd run build
```

Optional production preview after build:

```powershell
npm.cmd run start
```

Open:

```txt
http://localhost:3000
```

If port 3000 is in use:

```powershell
npm.cmd run start -- -p 3001
```

## Route Smoke Test

With the dev or production server running, verify a route from PowerShell:

```powershell
Invoke-WebRequest -Uri http://127.0.0.1:3000/warehouse -UseBasicParsing -TimeoutSec 15 | Select-Object StatusCode,RawContentLength
```

Expected:

```txt
StatusCode 200
```

Change the route as needed:

```powershell
http://127.0.0.1:3000/orders
http://127.0.0.1:3000/batches
http://127.0.0.1:3000/ai
```

## Backend API Integration Workflow

When testing with backend:

1. Start backend API server.
2. Set `.env.local`:

```txt
NEXT_PUBLIC_API_BASE_URL=http://<backend-host>:<backend-port>
NEXT_PUBLIC_API_TIMEZONE=Asia/Taipei
NEXT_PUBLIC_API_TOKEN=<only if backend token auth is enabled>
```

3. Restart frontend dev server.
4. Open the target route.
5. Confirm page shows `API data`.
6. Confirm backend logs show the expected request.
7. Run lint/build after mapper or service changes.

Warehouse current integration target:

```txt
GET /api/v2/warehouse/dashboard?includeInventory=true&trendDays=7
```

Reference:

```txt
docs/engineering/WAREHOUSE_FRONTEND_API_INTEGRATION_VERIFICATION_20260619.md
docs/frontend/ERP_API_FALLBACK_AND_RUNTIME_PLAYBOOK_20260526.md
```

## Common Troubleshooting

### `npm ci` fails

Try:

```powershell
npm cache verify
npm ci
```

If it still fails, check:

- Node.js version.
- Network/proxy access.
- Whether `package-lock.json` has been changed.

Do not delete `package-lock.json` without team agreement.

### Port 3000 is already used

Start on another port:

```powershell
npm.cmd run dev -- -p 3001
```

### Page shows `Mock fallback`

Check:

1. Is backend running?
2. Is `NEXT_PUBLIC_API_BASE_URL` correct?
3. Did you restart `npm run dev` after editing `.env.local`?
4. Does backend route match the frontend endpoint?
5. Does the browser devtools Network tab show a failed request?

### Build fails with TypeScript or ESLint error

Run:

```powershell
npm.cmd run lint
npm.cmd run build
```

Fix the first reported error before continuing.

### Environment variable changed but frontend still uses old value

Stop and restart the dev server. Next.js reads `NEXT_PUBLIC_*` values at startup/build time.

## Directory Guide

| Path | Purpose |
| --- | --- |
| `src/app/` | Route pages. |
| `src/components/` | Shared and page-specific UI components. |
| `src/layouts/` | App shell and navigation. |
| `src/services/` | API clients and response mappers. |
| `src/types/` | Shared TypeScript types. |
| `src/mock/` | Mock/fallback data. |
| `src/i18n/` | Local i18n dictionary and language provider. |
| `docs/frontend/` | Frontend UX specs, API readiness docs and decision records. |
| `docs/engineering/` | Engineering setup, integration and verification guides. |

## Engineer Handoff Checklist

Before saying the frontend environment is ready:

- [ ] `git status` reviewed.
- [ ] `npm ci` completed.
- [ ] `.env.local` created if backend API integration is needed.
- [ ] `npm.cmd run dev` starts successfully.
- [ ] Target route opens in browser.
- [ ] Source badge is understood: `API data` or `Mock fallback`.
- [ ] `npm.cmd run lint` passes.
- [ ] `npm.cmd run build` passes.
- [ ] Route smoke returns HTTP 200.

## Quick Command Summary

```powershell
cd C:\Users\andyy\Desktop\Codex-workspace\projects\ERP-2.0
npm ci
npm.cmd run dev
npm.cmd run lint
npm.cmd run build
Invoke-WebRequest -Uri http://127.0.0.1:3000/warehouse -UseBasicParsing -TimeoutSec 15 | Select-Object StatusCode,RawContentLength
```

## Decision

```txt
frontend_environment_setup_guide_created
```
