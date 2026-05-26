# ERP Status Vocabulary And Empty State Policy

Date: 2026-05-26
Scope: Recommended frontend vocabulary and empty/unavailable policy before backend API integration.

## Status Tone Vocabulary

| Tone | Use when | Common labels |
| --- | --- | --- |
| `success` | Ready, complete, released, normal, no blocking action needed. | `正常`, `完成`, `已放行`, `已簽收`, `可報價`, `完整` |
| `info` | In progress, available for observation, waiting for normal next step. | `進行中`, `待出庫`, `裝車中`, `配送中`, `API data`, `Loading API` |
| `warning` | Attention needed, not yet blocking, may become delay/risk. | `注意`, `待處理`, `待判定`, `待補`, `需調整`, `暫緩` |
| `danger` | Blocking, high risk, missing critical data, cannot proceed. | `高風險`, `阻擋`, `缺失`, `斷鏈`, `逾期`, `暫緩出貨` |
| `neutral` | Descriptive scope or category badge. | Module scope labels and non-status descriptors. |

## Cross-Module Recommended Labels

| Concept | Recommended V1 label | Avoid unless backend specifically requires |
| --- | --- | --- |
| Normal risk | `正常` | `OK`, `無風險` |
| Medium risk | `注意` | `警告`, `中風險` |
| High risk | `高風險` | `危急`, `嚴重` |
| Blocking state | `阻擋` | `錯誤`, `失敗` |
| Pending action | `待處理` | `未處理中`, `待辦` |
| Missing document | `缺失` | `錯誤`, `沒有` |
| Waiting for supplemental document | `待補` | `缺資料` |
| Released by quality | `已放行` | `通過`, `可用` |
| Pending quality decision | `待判定` | `未檢` |
| Billing ready | `待請款` or `可請款` | `可開票` unless invoice mutation is implemented |

## Empty State Policy

| Scenario | Frontend behavior | Product wording direction |
| --- | --- | --- |
| User search has no matches | Show controlled empty state inside the current table/card area. | `沒有符合條件的...` |
| View filter has no records | Show controlled empty state that confirms no current risk/action. | `目前沒有需要優先處理的...` |
| API returns valid empty array | Treat as real data; show empty state rather than mock rows. | Keep calm, operational wording. |
| API unavailable | Use mock fallback and show warning line plus `Mock fallback` badge. | Make demo/development source visible. |
| API field missing | Fallback only that field to mock and keep page stable. | Record in runtime verification. |
| Unknown status value | Keep UI stable; record vocabulary gap. | Prefer raw label with neutral/warning fallback after mapper is added. |

## Recommended Empty State Wording

| Workspace | Search empty state | Risk/view empty state |
| --- | --- | --- |
| Warehouse | `沒有符合條件的庫存資料` | `目前沒有符合條件的庫存風險` |
| Orders | `沒有符合條件的訂單` | `目前沒有符合條件的履約風險` |
| Production | `沒有符合條件的生產資料` | `目前沒有符合條件的排程或 MES 風險` |
| Quality | `沒有符合條件的品檢資料` | `目前沒有符合條件的放行阻擋` |
| Planning | `沒有符合條件的計劃案件` | `目前沒有符合條件的物料或產能風險` |
| Purchasing | `沒有符合條件的採購資料` | `目前沒有符合條件的到貨或價格風險` |
| Logistics | `沒有符合條件的出貨單` | `目前沒有需要優先處理的派車風險` |
| Finance | `沒有符合條件的財務案件` | `目前沒有需要優先追蹤的毛利或成本差異` |
| Traceability | `沒有符合條件的溯源資料` | `目前沒有符合條件的文件缺口或召回風險` |
| Settings | `沒有符合條件的設定項目` | `目前沒有符合條件的治理風險` |
| R&D | `沒有符合條件的研發案件` | `目前沒有符合條件的成本試算` |
| Workforce | `沒有符合條件的人力案件` | `目前沒有需要優先處理的人力缺口` |

## API Fallback Policy

Recommended default:

```txt
Use mock only for API unavailable, missing fields or invalid field types.
Do not use mock to replace valid empty arrays.
```

Reason:

Backend integration must be able to prove true empty states. Replacing `[]` with mock rows hides production behavior and makes runtime verification misleading.

## Owner Review Items

| Decision | Recommended default | Status |
| --- | --- | --- |
| Empty array should mean real empty data | Yes | `accepted` |
| API unavailable should remain visibly marked | Yes | `accepted` |
| CTA actions remain view navigation in V1 | Yes | `pending_owner_review` |
| Use management-readable Chinese labels instead of raw backend codes | Yes | `pending_owner_review` |
| Avoid mutation wording until endpoint exists | Yes | `pending_owner_review` |
