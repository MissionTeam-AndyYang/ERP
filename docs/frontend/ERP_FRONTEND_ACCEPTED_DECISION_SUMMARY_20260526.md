# ERP Frontend Accepted Decision Summary

Date: 2026-05-26
Scope: Short summary of owner-accepted frontend UX/API-integration decisions from D1-D10.

## Accepted Now

| ID | Decision |
| --- | --- |
| D1 | Valid API empty arrays are real empty data; do not refill mock rows. |
| D2 | API unavailable remains visibly marked with `Mock fallback` badge and warning line during development/demo. |
| D3 | V1 CTAs stay view/navigation/read-only until mutation endpoints, authorization and audit rules exist. |
| D4 | Frontend displays management-readable Chinese labels; backend raw codes are mapped in service/mapper layer. |
| D5 | Avoid mutation-sounding action labels until matching endpoints, permissions and audit rules exist. |
| D6 | i18n extraction starts with stable shared labels; API-field labels wait until payloads settle. |
| D9 | Support page dedicated services/types are created only after backend endpoint priority and response shape are confirmed. |

## Deferred Until API Or Later Version

| ID | Decision |
| --- | --- |
| D7 | Table density and pinned columns wait for Warehouse/Orders real payload density. |
| D8 | AI recovery planning trust model remains V1.3; V1.1/V1.2 focus on visibility and reason analysis. |
| D10 | Cross-page drill-down links wait for stable ids and route/detail policy. |

## Immediate Independent Follow-Up Completed

| Item | File |
| --- | --- |
| Interactive decision register | `docs/frontend/ERP_FRONTEND_INTERACTIVE_DECISION_REGISTER_20260526.md` |
| Status/empty-state policy updates | `docs/frontend/ERP_STATUS_VOCABULARY_AND_EMPTY_STATE_POLICY_20260526.md` |
| i18n phase-1 checklist | `docs/frontend/ERP_I18N_PHASE_1_EXTRACTION_CHECKLIST_20260526.md` |
| Status display mapper inventory | `docs/frontend/ERP_STATUS_DISPLAY_MAPPER_INVENTORY_20260526.md` |
| CTA/mutation wording audit | `docs/frontend/ERP_CTA_MUTATION_WORDING_AUDIT_20260526.md` |
| API fallback/runtime playbook | `docs/frontend/ERP_API_FALLBACK_AND_RUNTIME_PLAYBOOK_20260526.md` |

## Work That Should Wait

- Dedicated support-page service/type files.
- Cross-page links and detail routes.
- Dense table/pinned-column implementation.
- AI recovery planning.
- Any mutation workflow such as release, approve, allocate, dispatch, invoice or inventory adjustment.

## Decision

```txt
frontend_d1_d10_accepted_decisions_consolidated
```
