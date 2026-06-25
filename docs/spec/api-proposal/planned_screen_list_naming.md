# Planned Screen List And Naming

Purpose: 明確列出「倉庫中心」目前規劃中需要實作、延伸或持續整合的畫面與狀態名稱，作為後續討論、API 文件、前端任務與後端 review 的統一命名基準。

Naming rules:

1. `Screen` 表示可作為獨立頁面或主要工作區的畫面。
2. `View` 表示 `Screen` 內的主要頁籤或區塊，不單獨作為 route。
3. `Panel` 表示依附於畫面的右側資訊面板、drawer 或窄版 detail route。
4. `State` 表示清單的篩選狀態或 drill-down 情境，不是獨立畫面。
5. 文件、issue、commit message 與工程討論應使用 `Screen Code` / `View Code` / `Panel Code` / `State Code`，避免只寫「下一步畫面」「明細畫面」「批號畫面」等模糊名稱。

## 倉庫中心 Implementation Priority

| Priority | Code | Type | 正式畫面名稱 | Route / UI Location | Implementation Status | Primary API | 說明 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P0 | `WarehouseOverviewScreen` | Screen | 倉庫中心總覽 | `/warehouse` | 已有第一版，需持續整合 API 與細緻化 | `GET /api/v2/warehouse/dashboard` | Warehouse 入口畫面，呈現 KPI、庫存價值分類、倉位容量、風險警示摘要與待處理任務摘要。 |
| P0.1 | `WarehouseValueSpaceView` | View | 價值與倉位視圖 | `WarehouseOverviewScreen` 內的「價值與倉位」頁籤 | 已有第一版，需依 API runtime 持續調整 | `GET /api/v2/warehouse/dashboard` | 顯示庫存價值分類、倉位容量、板數與可用空間。 |
| P0.2 | `WarehouseRiskAlertView` | View | 風險警示視圖 | `WarehouseOverviewScreen` 內的「風險警示」頁籤 | 已有第一版，需與庫存明細 drill-down 對齊 | `GET /api/v2/warehouse/dashboard`、`GET /api/v2/warehouse/inventory` | 顯示迴轉、效期與安全水位風險；可導向風險批號清單狀態。 |
| P0.3 | `WarehousePendingTaskView` | View | 待處理入出庫視圖 | `WarehouseOverviewScreen` 內的「待處理入出庫」頁籤 | 已有第一版，需持續與 tasks API 對齊 | `GET /api/v2/warehouse/tasks` | 顯示今日或逾期待處理的入庫、出庫、移倉、盤點或確認任務。 |
| P0.4 | `WarehouseInventorySummaryView` | View | 庫存明細摘要視圖 | `WarehouseOverviewScreen` 內的「庫存明細」頁籤 | 已有第一版，後續應由 P1 清單畫面承接完整功能 | `GET /api/v2/warehouse/inventory` | 目前用於概覽頁快速查看批號層級庫存列；完整查詢、排序、分頁應移至 `WarehouseInventoryLotListScreen`。 |
| P0.5 | `WarehouseCurrentLotPanel` | Panel | 目前批號資訊面板 | `WarehouseOverviewScreen` 右側 panel | 已有第一版，需與 P2 追蹤面板做語意分工 | `GET /api/v2/warehouse/inventory` | 顯示目前選取批號的簡要數量、價值、安全水位、效期、流程狀態與關聯單據摘要。 |
| P1 | `WarehouseInventoryLotListScreen` | Screen | 庫存批號明細清單 | 建議 route：`/warehouse/inventory/lots`；也可先嵌入 `/warehouse` 的「庫存明細」工作區 | 待實作 | `GET /api/v2/warehouse/inventory/lots` | 批號層級清單畫面，支援倉庫、料品類別、料號、批號、風險、任務、可用狀態、關鍵字、排序與分頁。 |
| P2 | `WarehouseInventoryLotDetailPanel` | Panel | 庫存批號追蹤面板 | `WarehouseInventoryLotListScreen` 右側 panel；窄版可作為 drawer 或 detail route | 待實作 | `GET /api/v2/warehouse/inventory/lots/wh/{warehouseNo}/item/{itemNo}/batch/{batchNo}` | 顯示單一批號的庫存摘要、入出庫紀錄、預留、品檢保留、板位異動、未完成任務與風險。 |

## 倉庫中心 Screen State Naming

以下項目是 `WarehouseInventoryLotListScreen` 的篩選狀態或 drill-down 情境，不是獨立畫面。若工程任務要實作這些情境，應寫成「在 `WarehouseInventoryLotListScreen` 支援 `RiskLotListState`」，不要寫成「新增風險批號畫面」。

| Priority | State Code | 顯示名稱 | 所屬畫面 | 觸發來源 | API Query / State |
| --- | --- | --- | --- | --- | --- |
| P1.1 | `RiskLotListState` | 風險批號清單狀態 | `WarehouseInventoryLotListScreen` | 從 `WarehouseOverviewScreen` 的風險警示或 `WarehouseRiskAlertView` drill-down | `riskType` / `riskOnly` 類條件 |
| P1.2 | `PendingTaskLotListState` | 待處理批號清單狀態 | `WarehouseInventoryLotListScreen` | 從 `WarehousePendingTaskView` drill-down | `taskType` 或未完成任務條件 |
| P1.3 | `AvailableLotListState` | 可用庫存批號清單狀態 | `WarehouseInventoryLotListScreen` | 從可用庫存 KPI、追溯或篩選器入口 | `availability=available` |
| P1.4 | `QualityHoldLotListState` | 品檢保留批號清單狀態 | `WarehouseInventoryLotListScreen` | 從品檢保留 KPI、篩選器或 detail drill-down | `availability=quality_hold` |

## Not Standalone Screens

以下名稱在討論中容易造成混淆，統一不作為獨立畫面名稱使用：

| Ambiguous Name | 正確說法 |
| --- | --- |
| Warehouse Detail | 若指完整批號清單，使用 `WarehouseInventoryLotListScreen`；若指右側批號追蹤，使用 `WarehouseInventoryLotDetailPanel`。 |
| 風險批號畫面 | 使用 `WarehouseInventoryLotListScreen` + `RiskLotListState`。 |
| 待處理批號畫面 | 使用 `WarehouseInventoryLotListScreen` + `PendingTaskLotListState`。 |
| 明細畫面 | 需明確指定 `WarehouseInventorySummaryView`、`WarehouseInventoryLotListScreen` 或 `WarehouseInventoryLotDetailPanel`。 |

## Current Completion Summary

| Area | Current Status | Next Implementation Focus |
| --- | --- | --- |
| `WarehouseOverviewScreen` | 已有第一版，已串接 dashboard / inventory / tasks API 基礎呼叫。 | 依 runtime review 修正欄位對應、空狀態與互動一致性。 |
| `WarehouseInventoryLotListScreen` | 待實作。 | 建立清單頁/工作區、篩選列、排序、分頁與 drill-down 行為。 |
| `WarehouseInventoryLotDetailPanel` | 待實作。 | 建立單一批號追蹤面板，整合入出庫紀錄、預留、品檢、板位、任務與風險資料集。 |

