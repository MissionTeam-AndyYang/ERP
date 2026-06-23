# Warehouse Frontend API Split Review

Date: 2026-06-23
Scope: Frontend review and adjustment for Warehouse API integration questions.

## Questions Reviewed

1. Should risk alerts and inventory details display zero-quantity batches?
2. Does frontend call `/warehouse/dashboard` without inventory detail rows?
3. Does frontend call `/warehouse/tasks` when selecting the pending inbound/outbound task view?
4. Does frontend convert backend enum/action codes into display strings?

## Conclusions

| Question | Conclusion | Change |
| --- | --- | --- |
| Zero-quantity batches | No business reason was found to display zero-quantity batches in risk alerts or inventory detail. Backend should filter them. | Frontend mapper also defensively filters zero `currentQuantity` inventory rows and zero-quantity below-safety-stock risk rows. |
| Dashboard inventory detail | Dashboard should not request inventory detail rows. Inventory detail belongs to the dedicated inventory API. | Dashboard call changed from `includeInventory=true&trendDays=7` to `trendDays=7`. |
| Tasks API integration | The previous implementation used dashboard `pendingTasks`; it did not call `/warehouse/tasks` when the tab was selected. | `tasks` tab now calls `/api/v2/warehouse/tasks?count=100`. |
| Enum/action conversion | Some values were still shown as numeric units or raw action codes. | Added unit mapping and recommended action code mapping in the Warehouse service mapper. |

## Frontend Endpoint Behavior

Current frontend Warehouse API calls:

```txt
Initial /warehouse load:
GET /api/v2/warehouse/dashboard?trendDays=7

Risk view:
GET /api/v2/warehouse/inventory?count=100

Inventory detail view:
GET /api/v2/warehouse/inventory?count=100

Pending inbound/outbound task view:
GET /api/v2/warehouse/tasks?count=100
GET /api/v2/warehouse/inventory?count=100
```

Reason:

- Dashboard should provide summary, capacity, category and risk overview.
- Inventory detail should come from the inventory endpoint.
- Task list should come from the tasks endpoint.
- The tasks view also loads inventory detail so the existing related-detail table can show task-linked inventory rows.

## Backend Recommendation

Backend should filter zero-quantity batches before returning:

```txt
inventory.currentQuantity > 0
riskAlerts.quantity > 0 when the risk is stock-quantity based
```

Frontend now filters defensively, but backend filtering is still preferred because:

- It avoids misleading totals and risk counts.
- It prevents zero-stock historical batches from appearing in operational views.
- It reduces payload size.
- It keeps API behavior consistent for future clients.

## Enum And Action Mapping

Frontend currently maps:

```txt
unit number -> display unit
recommendedActionCode -> display recommendation
```

Unit mapping must follow `docs/spec/database/index.md` `Unit單位定義`, including:

```txt
0  -> 其他
1  -> 公克
2  -> 公斤
3  -> 台斤
51 -> 公分
52 -> 公尺
101 -> 個
102 -> 條
103 -> 片
104 -> 張
105 -> 罐
106 -> 包
107 -> 捲
108 -> 桶
109 -> 盒
110 -> 組
111 -> 箱
112 -> 支
113 -> 式
114 -> 入
115 -> 袋
116 -> 顆
117 -> 瓶
201 -> 板
202 -> 件
203 -> 車
204 -> 次
```

Initial action code mappings:

| Backend code | Frontend display |
| --- | --- |
| `warehouse.action.prioritizeIssueOrProduction` | `優先安排領料或生產使用` |
| `warehouse.action.reviewSlowMovingStock` | `檢討呆滯庫存處理` |
| `warehouse.action.reviewSafetyStock` | `檢查安全庫存與補貨設定` |
| `warehouse.action.reviewExpiryRisk` | `檢查效期風險並安排優先使用` |
| `warehouse.action.reviewQualityHold` | `確認品保 hold 狀態` |

Unknown action codes remain visible as raw values so mapper gaps can be detected during runtime verification.

## Verification

Commands run:

```txt
npm.cmd run lint
npm.cmd run build
Invoke-WebRequest http://127.0.0.1:3000/warehouse
```

Result:

```txt
lint passed
build passed
/warehouse route smoke passed with HTTP 200
```

## Decision

```txt
warehouse_frontend_dashboard_inventory_tasks_split_adjusted
```
