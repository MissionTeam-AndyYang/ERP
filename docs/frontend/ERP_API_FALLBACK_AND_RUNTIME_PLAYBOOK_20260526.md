# ERP API Fallback And Runtime Playbook

Date: 2026-05-26
Scope: Runtime verification playbook based on accepted frontend fallback and status-display decisions.

## Accepted Runtime Rules

| ID | Rule | Status |
| --- | --- | --- |
| D1 | Valid API empty arrays mean real empty data and should not be replaced by mock fallback rows. | Accepted |
| D2 | API unavailable remains visibly marked with `Mock fallback` badge and warning line during development/demo. | Accepted |
| D4 | Frontend displays management-readable labels while backend raw codes are mapped in service/mapper files. | Accepted |
| D9 | Dedicated support services/types wait for backend endpoint priority and response shape confirmation. | Accepted |

## Purpose

This playbook explains how to verify endpoints as backend APIs become available.

The goal is to distinguish:

- Endpoint unavailable.
- Endpoint available but truly empty.
- Endpoint available with partial or invalid shape.
- Endpoint available with unknown status codes.

These states should not be collapsed into the same mock fallback behavior.

## Expected Behaviors

| Scenario | Expected frontend behavior | Verification note |
| --- | --- | --- |
| API request fails | Use mock fallback and show `Mock fallback` plus warning text. | Confirms demo remains usable but source is visible. |
| API returns valid empty array | Show real empty state. Do not refill mock rows. | Confirms true empty production states can be tested. |
| API omits optional field | Fallback only that field when current guard supports it. | Record field gap in runtime verification. |
| API returns invalid field type | Fallback only affected field when possible. | Record schema mismatch. |
| API returns unknown status code | Keep UI stable; mapper uses fallback label/tone and records code. | Do not crash or silently hide the record. |
| API returns successful real data | Show `API data` source badge. | Search, tabs and detail sync should still work. |

## Endpoint Verification Sequence

Recommended sequence after backend reports endpoint readiness:

1. Confirm endpoint responds with 2xx.
2. Capture raw payload shape.
3. Compare raw payload against the page API readiness doc.
4. Verify valid empty arrays remain empty.
5. Verify source badge changes to `API data`.
6. Verify unknown or new status values are recorded as mapper gaps.
7. Verify search and selected detail states still work.
8. Run lint/build/route smoke after mapper changes.
9. Document result using the runtime verification template.

## First Endpoint Order

Use the accepted integration priority:

```txt
Warehouse -> Orders -> Production -> Quality -> Planning -> Purchasing -> Logistics -> Finance -> Traceability -> Settings -> R&D -> Workforce
```

Support pages wait for backend priority:

```txt
Batches / Items / BOM / AI dedicated services are created only after endpoint priority and response shape are confirmed.
```

## Runtime Verification Template Alignment

The reusable template remains:

```txt
docs/frontend/ERP_API_RUNTIME_VERIFICATION_TEMPLATE_20260526.md
```

When creating an endpoint-specific runtime report, include:

- Raw response excerpt or summarized shape.
- Empty-array behavior.
- Source badge result.
- Mapper decisions.
- Unknown status codes.
- Follow-up owner.

## Mapper Rules During Runtime

Status mapping should follow:

```txt
backend raw code -> service mapper -> display label + tone -> page component
```

Unknown status fallback:

```txt
label = rawValue || "待確認"
tone = "warning"
```

Use `neutral` only when the unknown value is clearly descriptive and not operational.

## Build And Smoke Expectations

For code changes:

```txt
npm.cmd run lint
npm.cmd run build
route smoke for affected page
```

Interactive browser smoke should be run when the local Browser plugin runtime is available. If unavailable, record that it is blocked rather than claiming browser interaction passed.

## Decision

```txt
api_fallback_runtime_playbook_created
```

The frontend has a concrete verification path for backend API integration without hiding true empty data, unknown statuses or partial schema mismatches.
