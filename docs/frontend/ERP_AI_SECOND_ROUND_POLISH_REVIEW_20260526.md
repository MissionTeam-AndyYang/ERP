# ERP AI Second-Round Polish Review

Date: 2026-05-26
Scope: AI support page low-risk polish before backend API integration.

## Review Metadata

| Field | Value |
| --- | --- |
| Page / route | AI / `/ai` |
| Related API endpoint | `GET /api/v1/ai/dashboard` |
| Data source during review | `mock` with generic support-dashboard API fallback |
| Change scope | Search and empty-state polish only |
| Mutation scope | None |

## UX Polish Completed

| Item | Result |
| --- | --- |
| Search behavior | Added page-level search for AI insights, decision-flow items and assistant tasks. |
| Search fields | Search covers insight id, risk text, recommendation text, confidence rows, flow item text and assistant-task text. |
| Empty state | Added controlled empty states for AI decision flow, insight cards and assistant-task list. |
| Existing structure | Kept `ModuleHero`, KPI cards, `ProcessBoard`, `DetailCard` and `CompactListPanel`. |
| API contract | No API shape change. Page still uses `useSupportDashboard("/api/v1/ai/dashboard", ...)`. |
| V1 boundary | No autonomous ERP execution, approval, scheduling or mutation UI added. |

## Recovery Planning Boundary

Accepted direction:

```txt
AI V1 = read-only insights + recovery planning assist.
```

This polish intentionally does not redesign the AI page into the final recovery-planning workspace yet. The recommended layout and data-shape notes are recorded in:

```txt
docs/frontend/ERP_AI_V1_RECOVERY_PLANNING_LAYOUT_NOTE_20260526.md
```

## Verification

| Check | Result | Notes |
| --- | --- | --- |
| `npm.cmd run lint` | Pass | ESLint completed successfully. |
| `npm.cmd run build` | Pass | Next.js production build completed successfully. |
| `/ai` HTTP route responds | Pass | `Invoke-WebRequest http://127.0.0.1:3000/ai` returned HTTP 200. |
| Browser interaction smoke | Blocked | In-app browser runtime is currently unavailable because the Browser plugin cache is missing `scripts/browser-client.mjs`. |
| Desktop/mobile overflow | Not run | Requires browser runtime to inspect viewport width. |

## Remaining Follow-Up

| Item | Priority | Dependency |
| --- | --- | --- |
| Re-run browser smoke for search, empty states and mobile overflow. | High | Browser runtime restored. |
| Accept recovery-plan data shape before larger AI UI changes. | High | Owner/backend/product confirmation. |
| Define evidence, confidence and audit trail standards. | High | AI/backend design. |
| Rename or constrain assistant tasks that sound executable. | Medium | Final V1 wording pass. |
| Consider shared empty-state component across support pages. | Low | Items, BOM, Batches and AI now share the same local pattern. |

## Decision

```txt
accepted_with_browser_smoke_pending
```

Reason:

The change improves findability and API-empty behavior while preserving the accepted V1 AI boundary: read-only recommendations and recovery planning assist, not autonomous ERP actions.
