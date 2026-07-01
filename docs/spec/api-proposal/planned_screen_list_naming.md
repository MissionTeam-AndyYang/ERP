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
| P1 | `WarehouseTaskWorkbenchScreen` | Screen | 倉庫任務工作台 | 建議 route：`/warehouse/task-workbench`；由 `WarehousePendingTaskView` drill-down 進入 | 待實作 | `GET /api/v2/warehouse/task-workbench` | 任務專用工作區，顯示今日、逾期與近期入庫、出庫、移倉、品檢與出貨任務，支援 kanban/list、篩選、排序與分頁。 |
| P1.5 | `WarehouseTaskDetailPanel` | Panel | 倉庫任務追蹤面板 | `WarehouseTaskWorkbenchScreen` 右側 panel；窄版可作為 drawer 或 detail route | 待實作 | `GET /api/v2/warehouse/task-workbench/tasks/{taskId}` | 顯示單一任務的來源單據、相關批號、庫存可用性、阻塞原因、下一步負責部門與任務時間線。 |
| P2 | `WarehouseInventoryLotListScreen` | Screen | 庫存批號明細清單 | `/warehouse/inventory/lots` | 已有第一版，需依 runtime review 持續細緻化 | `GET /api/v2/warehouse/inventory/lots` | 批號層級清單畫面，支援倉庫、料品類別、料號、批號、風險、任務、可用狀態、關鍵字、排序與分頁。 |
| P3 | `WarehouseInventoryLotDetailPanel` | Panel | 庫存批號追蹤面板 | `WarehouseInventoryLotListScreen` 右側 panel；窄版可作為 drawer 或 detail route | 已有第一版，需依 runtime review 持續細緻化 | `GET /api/v2/warehouse/inventory/lots/wh/{warehouseNo}/item/{itemNo}/batch/{batchNo}` | 顯示單一批號的庫存摘要、入出庫紀錄、預留、品檢保留、板位異動、未完成任務與風險。 |
| P4 | `WarehouseAnalyticsScreen` | Screen | 倉庫分析工作區 | 建議 route：`/warehouse/analytics`；由 Warehouse nav 或總覽 KPI drill-down 進入 | Proposal / Pending Engineer Review | `GET /api/v2/warehouse/analytics/overview`、`GET /api/v2/warehouse/analytics/value-trend`、`GET /api/v2/warehouse/analytics/space-utilization`、`GET /api/v2/warehouse/analytics/risk-breakdown`、`GET /api/v2/warehouse/analytics/task-sla` | 第一版 read-only 延伸畫面，分析庫存價值、倉位使用、風險分布與任務 SLA；不包含 POST / PUT。 |

## 倉庫中心 Screen State Naming

以下項目是 `WarehouseInventoryLotListScreen` 的篩選狀態或 drill-down 情境，不是獨立畫面。若工程任務要實作這些情境，應寫成「在 `WarehouseInventoryLotListScreen` 支援 `RiskLotListState`」，不要寫成「新增風險批號畫面」。

| Priority | State Code | 顯示名稱 | 所屬畫面 | 觸發來源 | API Query / State |
| --- | --- | --- | --- | --- | --- |
| P1.1 | `TodayTaskWorkbenchState` | 今日任務工作台狀態 | `WarehouseTaskWorkbenchScreen` | 工作台預設入口或 `WarehousePendingTaskView` drill-down | `dateRange=today` |
| P1.2 | `OverdueTaskWorkbenchState` | 逾期任務工作台狀態 | `WarehouseTaskWorkbenchScreen` | 從逾期任務摘要、阻塞任務或看板 lane 進入 | `dateRange=overdue` |
| P1.3 | `RiskTaskWorkbenchState` | 風險任務工作台狀態 | `WarehouseTaskWorkbenchScreen` | 從阻塞、庫存不足、品檢保留或逾期風險摘要進入 | `riskOnly=true` |
| P2.1 | `RiskLotListState` | 風險批號清單狀態 | `WarehouseInventoryLotListScreen` | 從 `WarehouseOverviewScreen` 的風險警示或 `WarehouseRiskAlertView` drill-down | `riskType` / `riskOnly` 類條件 |
| P2.2 | `PendingTaskLotListState` | 待處理批號清單狀態 | `WarehouseInventoryLotListScreen` | 從 `WarehouseTaskWorkbenchScreen` 或 `WarehousePendingTaskView` drill-down | `taskType` 或未完成任務條件 |
| P2.3 | `AvailableLotListState` | 可用庫存批號清單狀態 | `WarehouseInventoryLotListScreen` | 從可用庫存 KPI、追溯或篩選器入口 | `availability=available` |
| P2.4 | `QualityHoldLotListState` | 品檢保留批號清單狀態 | `WarehouseInventoryLotListScreen` | 從品檢保留 KPI、篩選器或 detail drill-down | `availability=quality_hold` |

## Not Standalone Screens

以下名稱在討論中容易造成混淆，統一不作為獨立畫面名稱使用：

| Ambiguous Name | 正確說法 |
| --- | --- |
| Warehouse Detail | 若指完整批號清單，使用 `WarehouseInventoryLotListScreen`；若指右側批號追蹤，使用 `WarehouseInventoryLotDetailPanel`。 |
| 倉庫任務工作台 | 使用 `WarehouseTaskWorkbenchScreen`；它是獨立任務工作區，不是 `WarehousePendingTaskView`。 |
| 任務明細 | 使用 `WarehouseTaskDetailPanel`。 |
| 任務執行畫面 | `WarehouseTaskExecutionScreen` 已延至 V2；Warehouse V1 不以此作為下一步實作目標。 |
| 風險批號畫面 | 使用 `WarehouseInventoryLotListScreen` + `RiskLotListState`。 |
| 待處理批號畫面 | 使用 `WarehouseInventoryLotListScreen` + `PendingTaskLotListState`。 |
| 明細畫面 | 需明確指定 `WarehouseInventorySummaryView`、`WarehouseInventoryLotListScreen` 或 `WarehouseInventoryLotDetailPanel`。 |

## Current Completion Summary

| Area | Current Status | Next Implementation Focus |
| --- | --- | --- |
| `WarehouseOverviewScreen` | 已有第一版，已串接 dashboard / inventory / tasks API 基礎呼叫。 | 依 runtime review 修正欄位對應、空狀態與互動一致性。 |
| `WarehouseTaskWorkbenchScreen` | 待實作；已有 API proposal 與靜態預覽。 | 建立任務 kanban/list、日期範圍、任務風險摘要、篩選、排序、分頁與 drill-down 行為。 |
| `WarehouseTaskDetailPanel` | 待實作；已有 API proposal。 | 建立單一任務追蹤面板，整合來源單據、相關批號、庫存可用性、阻塞原因、下一步負責部門與任務時間線。 |
| `WarehouseTaskExecutionScreen` | Deferred to V2；第一版 read-only 暫不實作含 POST / PUT 的畫面。 | 保留既有 proposal 作為下一版任務執行討論基礎，當前不作為下一步 API 設計目標。 |
| `WarehouseInventoryLotListScreen` | 已有第一版，已串接 inventory lots API。 | 依後端 runtime payload 檢查欄位呈現、篩選結果、分頁與空狀態。 |
| `WarehouseInventoryLotDetailPanel` | 已有第一版，已串接 inventory lot detail API。 | 依後端 runtime payload 檢查入出庫紀錄、預留、品檢、板位、任務與風險資料集呈現。 |
| `WarehouseAnalyticsScreen` | 新增 read-only proposal；待工程師 review。 | 建立庫存價值趨勢、倉位使用趨勢、風險分布與任務 SLA 的 GET-only 分析 API。 |

## V1 Coverage Confirmation

截至 2026-06-26，本文件已涵蓋第一版「倉庫中心」所需實作的全部畫面與附屬狀態。後續若新增未列於本文件的畫面，需先補入本清單並指定 `Screen` / `View` / `Panel` / `State` 類型。

第一版剩餘主要實作項目為：

1. `WarehouseTaskWorkbenchScreen`
2. `WarehouseTaskDetailPanel`

上述兩項完成後，第一版「倉庫中心」畫面骨架可視為完整；後續工作應歸類為 runtime review、API contract 細緻化、互動細節修正、跨模組 drill-down 或 mutation API 設計。

