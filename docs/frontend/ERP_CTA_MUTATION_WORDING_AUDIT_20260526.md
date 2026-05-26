# ERP CTA And Mutation Wording Audit

Date: 2026-05-26
Scope: Frontend copy audit after owner accepted the V1 CTA and mutation wording boundaries.

## Accepted Rules

Owner accepted:

```txt
V1 CTAs are view/navigation/read-only only until mutation endpoints, authorization and audit rules exist.
Frontend avoids mutation-sounding action labels until matching endpoints, permissions and audit rules exist.
```

## Audit Method

Searched frontend source for mutation-sensitive wording:

```txt
放行 / 核准 / 隔離 / 分配 / 調整 / 派車 / 請款 / 開立 / 新增 / 修改 / 刪除
approve / release / allocate / invoice / dispatch / create / update / delete
```

Reviewed whether matches are:

- Read-only statuses.
- View/tab labels.
- Explanatory descriptions.
- Actual action buttons that imply mutation.

## Result

```txt
No immediate V1 mutation-action blocker found.
```

The current matches are mostly read-only status labels, tab/view names, descriptions or mock data fields. They do not currently submit changes or call mutation endpoints.

## Notable Matches And Classification

| Area | Wording | Classification | Decision |
| --- | --- | --- | --- |
| Quality | `放行與阻擋`, `放行` tab label | View/tab label | Acceptable in V1 if it only changes view. |
| Logistics | `派車`, `派車風險` | View/tab label and risk context | Acceptable in V1 if it only changes view. |
| Finance | `請款`, `應收/請款` | View/tab label and financial status context | Acceptable in V1 if it only changes view. |
| Batches | `QA Hold`, `隔離`, `已分配未放行` | Status/risk data | Acceptable as read-only status. |
| AI | `QA 放行` | Source-record reason/status text | Acceptable as read-only explanation. |
| BOM | `已核准`, `量產核准` | Version/status data | Acceptable as read-only status. |
| Items | `需新增` | Master-data task status | Acceptable as read-only task signal, not action. |
| Planning | `可建立或需調整的工單建議` | Recommendation text | Acceptable if no create/adjust action is exposed. |

## Copy Guardrails

Allowed wording in V1:

- `放行狀態`
- `待放行`
- `放行與阻擋`
- `派車風險`
- `待派車`
- `請款狀態`
- `待請款`
- `需新增`
- `需調整`
- `建議`

Avoid as clickable CTA labels until mutation exists:

- `執行放行`
- `核准`
- `建立工單`
- `新增品項`
- `調整庫存`
- `隔離批號`
- `分配庫存`
- `派車`
- `開立請款`
- `送出`

Preferred read-only CTA labels:

- `查看`
- `檢視詳情`
- `切換視圖`
- `查看來源`
- `查看關聯資料`
- `回到總覽`

## Follow-Up

When mutation endpoints become available, each new action should include:

1. Endpoint contract.
2. Required permission.
3. Audit trail fields.
4. Status transition rule.
5. Error and rollback behavior.
6. Confirmation or review step where needed.

## Decision

```txt
cta_mutation_wording_audit_complete_no_immediate_blocker
```

The current frontend remains aligned with the accepted V1 visibility-first boundary. Mutation-sensitive words may remain where they describe status, risk or view scope, but should not be used as direct action CTAs until backend support exists.
