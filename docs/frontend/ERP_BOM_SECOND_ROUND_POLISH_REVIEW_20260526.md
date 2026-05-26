# ERP BOM Second-Round Polish Review

Date: 2026-05-26
Scope: BOM support page low-risk polish before backend API integration.

## Review Metadata

| Field | Value |
| --- | --- |
| Page / route | BOM / `/bom` |
| Related API endpoint | `GET /api/v1/bom/dashboard` |
| Data source during review | `mock` with generic support-dashboard API fallback |
| Change scope | Search and empty-state polish only |
| Mutation scope | None |

## UX Polish Completed

| Item | Result |
| --- | --- |
| Search behavior | Added page-level search for BOM cards, lifecycle board items and change tasks. |
| Search fields | Search covers BOM no, item text, version text, process parameter rows, lifecycle item text and change-task text. |
| Empty state | Added controlled empty states for lifecycle board, BOM cards and change-task list. |
| Existing structure | Kept `ModuleHero`, KPI cards, `ProcessBoard`, `DetailCard` and `CompactListPanel`. |
| API contract | No API shape change. Page still uses `useSupportDashboard("/api/v1/bom/dashboard", ...)`. |
| V1 boundary | No create/update/delete, approval, version activation or formula mutation UI added. |

## Verification

| Check | Result | Notes |
| --- | --- | --- |
| `npm.cmd run lint` | Pass | ESLint completed successfully. |
| `npm.cmd run build` | Pass | Next.js production build completed successfully. |
| `/bom` HTTP route responds | Pass | `Invoke-WebRequest http://127.0.0.1:3000/bom` returned HTTP 200. |
| Browser interaction smoke | Blocked | In-app browser runtime is currently unavailable because the Browser plugin cache is missing `scripts/browser-client.mjs`. |
| Desktop/mobile overflow | Not run | Requires browser runtime to inspect viewport width. |

## Remaining Follow-Up

| Item | Priority | Dependency |
| --- | --- | --- |
| Re-run browser smoke for search, empty states and mobile overflow. | High | Browser runtime restored. |
| Confirm approved-production-only and development/trial filter rules. | High | BOM API fields and business rules. |
| Guard Planning from using development BOM versions. | High | Backend validation and display status mapping. |
| Decide whether BOM deserves a dedicated `bom-api.ts` and `types/bom.ts`. | Medium | Backend API priority confirmation. |
| Add API field readiness doc if backend will implement `/api/v1/bom/dashboard`. | Done | `docs/frontend/ERP_BOM_API_FIELD_READINESS_20260526.md` |
| Consider shared empty-state component after Batches or AI repeats the same pattern. | Low | At least three support pages using same pattern. |

## Decision

```txt
accepted_with_browser_smoke_pending
```

Reason:

The change is low-risk, build-safe in structure, and preserves the support-page role. It improves findability without implying unsupported BOM approval, activation or formula-editing behavior.
