# ERP i18n Phase 1 Extraction Checklist

Date: 2026-05-26
Scope: Low-risk i18n extraction planning after owner accepted stable-shared-labels-first timing.

## Decision

```txt
i18n extraction starts with stable shared labels first.
API-field labels wait until backend payloads and service mappers settle.
```

## Phase 1 Goal

Move stable shared UI language toward dictionary ownership without creating churn in page-specific business fields.

Phase 1 should improve consistency for shell, fallback and empty-state wording while leaving API-driven table/detail labels in page or mapper code until backend contracts are stable.

## Extract Now

| Area | Examples | Risk |
| --- | --- | --- |
| Navigation labels | Dashboard, Warehouse, Orders, Production, Quality, Planning, Purchasing, Logistics, Finance, Traceability, Settings. | Low |
| API source badges | `API data`, `Mock fallback`, `Loading API`, `Read-only`. | Low |
| Common empty-state prefixes | `沒有符合條件的...`, `目前沒有需要優先處理的...`. | Low |
| Common CTA labels | `查看`, `返回`, `切換視圖`, `檢視詳情`. | Low |
| Shared shell labels | Search placeholder patterns, section labels reused across pages. | Low |
| Runtime/fallback warnings | API unavailable fallback wording. | Low |

## Defer Until API Payloads Settle

| Area | Reason |
| --- | --- |
| Table column labels | Columns may change after real backend fields arrive. |
| Detail panel business fields | Mapper may consolidate or rename fields. |
| Backend status labels | Raw codes and canonical workflow states are not final. |
| Unit and quantity labels | Backend may return numeric amount plus unit or display strings. |
| Page-specific KPI labels | KPI formulas and labels may change with real payload density. |
| Advanced filter labels | Filter keys should wait for stable server-side fields. |

## Recommended Implementation Order

1. Inspect current i18n dictionary structure and naming conventions.
2. Add shared entries for API source badges and fallback warnings.
3. Add shared entries for common empty-state wording.
4. Add shell/navigation entries only if the current layout already reads from dictionary or can be changed with minimal churn.
5. Update one or two shared components first, not every page at once.
6. Run lint/build and route smoke for affected pages.

## Guardrails

- Do not change business meaning while extracting strings.
- Do not extract unstable backend-field labels yet.
- Do not introduce a new i18n framework if the project already has a local pattern.
- Keep dictionary keys semantic and stable.
- Prefer small commits by label group.

## Follow-Up After Backend Integration

After Warehouse and Orders payloads are stable:

1. Extract confirmed table and detail labels.
2. Extract mapper-produced display labels where appropriate.
3. Add tests or snapshots only if label mapping becomes complex.
4. Revisit multi-language requirements beyond Traditional Chinese.

## Decision

```txt
i18n_phase_1_shared_labels_first_checklist_created
```
