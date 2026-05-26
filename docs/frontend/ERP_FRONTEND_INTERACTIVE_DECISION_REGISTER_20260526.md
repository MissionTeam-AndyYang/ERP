# ERP Frontend Interactive Decision Register

Date: 2026-05-26
Scope: Interactive owner decision record for frontend UX refinement before backend API integration.

## Purpose

This register records frontend UX and API-integration decisions that should be confirmed through one-by-one discussion.

Working mode:

```txt
Ask one decision question -> owner confirms or adjusts -> record decision -> Codex executes independent follow-up work.
```

This avoids mixing product judgment with implementation work while still letting low-risk follow-up tasks proceed independently after each decision.

## Decision Status Values

| Status | Meaning |
| --- | --- |
| `pending_discussion` | Needs owner discussion before implementation. |
| `accepted` | Owner accepted the recommended default. |
| `accepted_with_changes` | Owner accepted the direction with wording/scope changes. |
| `deferred` | Keep recorded but do not implement now. |
| `blocked_by_backend` | Wait for real API payload, backend code or source confirmation. |
| `implemented` | Follow-up work has been completed. |

## Decision Queue

| ID | Topic | Recommended default | Current status | Follow-up after decision |
| --- | --- | --- | --- | --- |
| D1 | Empty array behavior | Valid API empty arrays mean real empty data; do not refill mock rows. | `accepted` | Update fallback policy and service guard notes. |
| D2 | API unavailable display | Keep `Mock fallback` badge and warning line visible during development/demo. | `accepted` | Align fallback wording and verification checklist. |
| D3 | V1 CTA boundary | CTAs are view/navigation only until mutation endpoints, authorization and audit exist. | `accepted` | Audit page CTAs and document any exceptions. |
| D4 | Status display wording | Display management-readable Chinese labels; map backend raw codes in service/mapper layer. | `accepted` | Update status policy from pending review to accepted and use in integration checklist. |
| D5 | Mutation wording | Avoid action verbs that imply unsupported mutations, such as release, approve, allocate or invoice, unless endpoint exists. | `pending_discussion` | Review page copy for mutation-sounding labels. |
| D6 | i18n extraction timing | Extract stable shared labels first; defer API-field labels until payloads settle. | `pending_discussion` | Prepare i18n extraction phase-1 checklist. |
| D7 | Table density and pinned columns | Defer until Warehouse/Orders real payload density is visible. | `pending_discussion` | Record UX preference and revisit after API smoke. |
| D8 | AI recovery planning trust model | Defer V1.3 details; keep V1.1/V1.2 read-only visibility and reason analysis first. | `pending_discussion` | Create V1.3 trust model checklist later. |
| D9 | Support page dedicated services/types | Create only when backend endpoint priority and response shape are confirmed. | `pending_discussion` | Prepare implementation rule, not code. |
| D10 | Cross-page drill-down links | Wait for stable ids and route/detail policy. | `pending_discussion` | Define link policy after backend ids are confirmed. |

## Already Accepted Context

| Topic | Decision |
| --- | --- |
| Batches vs Traceability | Batches is item-centered batch operations; Traceability is chain, document completeness and recall-scope investigation. |
| AI V1.1 | Today's work status visibility and delayed item presentation first. |
| AI V1.2 | Delayed reason analysis. |
| AI V1.3 | AI-assisted recovery planning later. |
| Support page polish order | Items first, then BOM, then Batches, then AI. |
| Batches mutation boundary | Batches V1 remains read-only; no release, quarantine, adjustment, recall, move, allocation or mutation UI. |

## Independent Work After Decisions

After related decisions are accepted, Codex can independently complete:

1. Update decision statuses in this register.
2. Update `ERP_STATUS_VOCABULARY_AND_EMPTY_STATE_POLICY_20260526.md`.
3. Update `ERP_FRONTEND_SECOND_ROUND_UX_BACKLOG_20260526.md`.
4. Create i18n phase-1 checklist.
5. Create CTA/mutation wording audit.
6. Prepare API integration playbook using the accepted fallback and mapper rules.
7. Run lint/build or route smoke when code changes are involved.
8. Commit and push after each completed batch when requested.

## Current Discussion Pointer

Next question:

```txt
D5: Should frontend avoid mutation-sounding labels, such as release, approve, allocate or invoice, until matching endpoints exist?
```

## Decision Log

| Date | ID | Decision | Owner response | Follow-up |
| --- | --- | --- | --- | --- |
| 2026-05-26 | D1 | Valid API empty arrays mean true empty data and should not be replaced by mock fallback rows. | Accepted. | Fallback policy updated from pending review to accepted. |
| 2026-05-26 | D2 | API unavailable should remain visibly marked with `Mock fallback` badge and warning line during development/demo. | Accepted. | Fallback policy updated from pending review to accepted. |
| 2026-05-26 | D3 | V1 CTAs remain view/navigation/read-only only until mutation endpoints, authorization and audit rules exist. | Accepted. | CTA boundary updated from pending review to accepted. |
| 2026-05-26 | D4 | Frontend displays management-readable Chinese labels while backend raw codes are mapped in service/mapper files. | Accepted. | Status wording updated from pending review to accepted. |
