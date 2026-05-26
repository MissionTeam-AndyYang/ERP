# ERP Batches Second-Round Polish Review

Date: 2026-05-26
Scope: Batches support page low-risk polish before backend API integration.

## Review Metadata

| Field | Value |
| --- | --- |
| Page / route | Batches / `/batches` |
| Related API endpoint | `GET /api/v1/batches/dashboard` |
| Data source during review | `mock` with generic support-dashboard API fallback |
| Change scope | Search and empty-state polish only |
| Mutation scope | None |

## UX Polish Completed

| Item | Result |
| --- | --- |
| Search behavior | Added page-level search for batch cards, lifecycle board items and batch-risk tasks. |
| Search fields | Search covers batch no, item text, work order text, warehouse/location text, QA/expiry rows and task text. |
| Empty state | Added controlled empty states for lifecycle board, batch cards and batch-task list. |
| Existing structure | Kept `ModuleHero`, KPI cards, `ProcessBoard`, `DetailCard` and `CompactListPanel`. |
| API contract | No API shape change. Page still uses `useSupportDashboard("/api/v1/batches/dashboard", ...)`. |
| V1 boundary | No release, quarantine, adjustment, recall or shipment mutation UI added. |

## Boundary Confirmation

Accepted page boundary:

```txt
Batches = batch lifecycle and operational control workspace.
Traceability = trace chain, document completeness and recall-scope investigation workspace.
```

This polish stays inside the Batches boundary by improving batch status/lifecycle findability only. It does not add trace-chain visualization, recall-scope investigation or customer/shipment impact analysis.

## Verification

| Check | Result | Notes |
| --- | --- | --- |
| `npm.cmd run lint` | Pass | ESLint completed successfully. |
| `npm.cmd run build` | Pass | Next.js production build completed successfully. |
| `/batches` HTTP route responds | Pass | `Invoke-WebRequest http://127.0.0.1:3000/batches` returned HTTP 200. |
| Browser interaction smoke | Blocked | In-app browser runtime is currently unavailable because the Browser plugin cache is missing `scripts/browser-client.mjs`. |
| Desktop/mobile overflow | Not run | Requires browser runtime to inspect viewport width. |

## Remaining Follow-Up

| Item | Priority | Dependency |
| --- | --- | --- |
| Re-run browser smoke for search, empty states and mobile overflow. | High | Browser runtime restored. |
| Design the future dense operational table workspace. | High | Batch API fields for status, QA release, expiry, quarantine, location and quantity. |
| Decide selected batch detail panel fields. | High | Batch detail API shape. |
| Align batch status vocabulary with Warehouse and Quality. | Medium | Backend status codes and mapper rules. |
| Consider shared empty-state component after AI or another support page repeats the same pattern. | Low | At least three support pages using same pattern. |

## Decision

```txt
accepted_with_browser_smoke_pending
```

Reason:

The change is low-risk and improves batch findability without changing the accepted Batches versus Traceability boundary or promising unsupported batch operations.
