# ERP 2.0 Engineering Ownership and Verification Plan

Date: 2026-05-24
Purpose: Define collaboration ownership, verification responsibilities and handoff flow for the next ERP 2.0 implementation phase.

## 1. Current Phase

The project has moved from V1 screen planning into API implementation and frontend integration preparation.

Completed baselines:

- Frontend V1 screen planning is stable enough for integration.
- V1 API development specs exist under `docs/frontend/api/`.
- API implementation tracker exists at `docs/backend/API_IMPLEMENTATION_TRACKER_20260524.md`.
- API contract verification script exists at `scripts/verify_v1_api_contracts.py`.
- Latest DB baseline is `EWDB_20260526.sql`; latest workflow baseline remains `EWDB_20260522_WORKFLOW.md`.

## 2. Ownership Summary

| Area | Primary owner | Support owner | Notes |
| --- | --- | --- | --- |
| DB schema verification | Codex | Engineer | Engineer runs DB-backed checks when local DB is required |
| Backend API / restserver code review | Codex | Engineer | Codex reviews code and specs; engineer implements backend fixes/API |
| Frontend design and development | Codex | User | User provides business feedback; Codex implements UI and API service layer |
| API implementation | Engineer | Codex | Engineer implements restserver endpoints; Codex provides specs and review |
| API contract verification | Codex | Engineer | Engineer may run scripts in DB/runtime environment; Codex reviews output |
| Unit/function/integration/system/performance tests | Codex | Engineer | Codex designs scripts and acceptance criteria; engineer runs environment-dependent tests |
| Business priority and approval | User | Codex | User confirms workflow, role ownership and process priorities |

## 3. Role Responsibilities

### User

The user owns business direction and final approval.

Responsibilities:

- Confirm business workflow and department responsibility.
- Decide priority when tradeoffs appear.
- Review UI direction when business interpretation is uncertain.
- Notify Codex when engineer finishes code review or API implementation milestones.

### Engineer

The engineer owns backend implementation and DB/runtime execution in the environment that has database access.

Responsibilities:

- Complete current restserver code review fixes.
- Review API development specs and confirm endpoint implementation path.
- Implement or adjust backend APIs.
- Run DB-backed runtime verification when needed.
- Run API contract verification scripts after endpoints are implemented.
- Share output under `docs/backend/runtime-verification/` or equivalent reviewed result files.

### Codex

Codex owns system planning, frontend implementation, backend/API review support and test design.

Responsibilities:

- Maintain DB/API/frontend/test planning documents.
- Review database schema against workflow and frontend/API needs.
- Review restserver code and API response design.
- Produce and update API development specs.
- Build frontend pages, API service layer and mock fallback.
- Design verification scripts and test plans.
- Review engineer runtime output and recommend next fixes.

## 4. Workstream Plans

### 4.1 DB Schema Verification

Goal:

Confirm that the database schema can support the approved workflow, API specs and frontend V1 screens.

Codex responsibilities:

- Review SQL schema and workflow docs.
- Identify missing or ambiguous data fields for V1 APIs.
- Maintain DB verification checklist.
- Review engineer DB runtime output.

Engineer responsibilities:

- Run DB-backed verification scripts in environment with MariaDB/MySQL.
- Confirm table/field availability for API specs.
- Report schema gaps or required migrations.

Expected outputs:

- DB schema review/update document.
- Runtime verification result under `docs/backend/runtime-verification/`.
- Updated API specs if schema constraints require changes.

### 4.2 Backend API / restserver Code Review

Goal:

Ensure restserver implementation can support V1 read-only APIs and later controlled write actions.

Codex responsibilities:

- Review restserver code by module.
- Compare existing endpoints to API development specs.
- Identify response shape gaps, status mapping gaps, error handling issues and security concerns.
- Update API development docs when implementation decisions change.

Engineer responsibilities:

- Complete high-priority bug fixes from code review.
- Confirm endpoint naming and response shape.
- Implement aggregation/detail APIs.
- Run API contract verification.

Expected outputs:

- API implementation updates in restserver.
- Reviewed runtime/API verification result.
- Updated `docs/backend/API_IMPLEMENTATION_TRACKER_20260524.md`.

### 4.3 Frontend Design, Development and API Integration

Goal:

Move approved screens from mock data toward API-ready and then real API integration.

Codex responsibilities:

- Continue UI refinement without changing confirmed business direction.
- Build shared API client layer.
- Build module services such as Warehouse API service.
- Add mock fallback until backend endpoints are ready.
- Replace mock imports module by module after API verification passes.

Recommended first frontend implementation:

```txt
Shared API client
-> Warehouse service layer
-> Warehouse mock fallback
-> Warehouse page reads through service/hook
-> Warehouse real API integration after backend verification
```

Expected outputs:

- `src/services/api-client.ts`
- `src/services/warehouse-api.ts`
- Warehouse service/hook or equivalent data access layer.
- Build/lint verification.

### 4.4 Test Design and Execution

Goal:

Create a staged test system that matches the project maturity.

Test layers:

| Test layer | Purpose | Owner |
| --- | --- | --- |
| Unit test | Validate data mapping, utilities and service normalization | Codex |
| Function test | Validate page-level behavior and user-visible states | Codex |
| API contract test | Validate endpoint response structure | Codex + Engineer |
| Integration test | Validate frontend service layer against backend APIs | Codex + Engineer |
| System test | Validate end-to-end workflow across modules | Codex + Engineer |
| Performance/stress test | Validate API latency and stability under load | Codex + Engineer |

Recommended sequence:

1. API contract tests for Warehouse.
2. Frontend service layer unit tests for Warehouse mapping.
3. Function test for Warehouse page with mock fallback.
4. Integration test for Warehouse page with real API.
5. Repeat for Orders, Production and Quality.
6. Add Manager Dashboard integration tests after core module APIs are stable.

## 5. Immediate Next Steps

### Step A: Engineer continues backend code review fixes

Trigger:

Engineer reports code review fixes are complete.

Codex reminder to user:

Ask the user to hand the engineer the next review package:

- `docs/backend/API_IMPLEMENTATION_HANDOFF_TO_ENGINEER_20260524.md`
- `docs/backend/API_IMPLEMENTATION_TRACKER_20260524.md`
- `docs/frontend/api/ERP_API_DEVELOPMENT_SPECS_INDEX_20260524.md`

### Step B: Codex starts frontend service layer

This can proceed while backend fixes continue.

First target:

```txt
Warehouse API service layer skeleton with mock fallback
```

Boundary:

- Do not require backend API to exist yet.
- Do not change confirmed Warehouse UI meaning.
- Do not remove mock data until real API passes verification.

### Step C: Engineer confirms Warehouse API implementation path

Required confirmation:

- Endpoint name.
- Existing endpoints to reuse.
- Missing DB fields.
- Response shape differences.
- Implementation blockers.

### Step D: Warehouse API implementation and verification

After implementation:

```powershell
python scripts/verify_v1_api_contracts.py --base-url http://127.0.0.1:5000 --module warehouse --output docs/backend/runtime-verification/WAREHOUSE_API_CONTRACT_YYYYMMDD.md
```

Codex then reviews the output and updates specs or frontend integration code.

## 6. Handoff Rules

1. Use GitHub `main` as the shared source of truth.
2. Commit only reviewed project artifacts.
3. Do not commit `.env.example` if it contains machine-specific credentials.
4. Do not commit raw runtime output until reviewed for secrets and usefulness.
5. Keep API specs and verification scripts updated when implementation decisions change.
6. Prefer read-only integration before controlled write actions.
7. Do not expand new major screens until API integration foundations are stable.

## 7. Current Decision

This plan is the collaboration baseline for the next phase.

While the engineer completes restserver code review fixes, Codex should proceed with frontend API service-layer preparation, starting from Warehouse, and pause backend-dependent integration until API verification output is available.
