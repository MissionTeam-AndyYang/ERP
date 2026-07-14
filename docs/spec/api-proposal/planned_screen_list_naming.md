# Planned Screen List And Naming

Purpose: 明確列出「倉庫中心」目前規劃中需要實作、延伸或持續整合的畫面與狀態名稱，作為後續討論、API 文件、前端任務與後端 review 的統一命名基準。

Naming rules:

1. `Screen` 表示可作為獨立頁面或主要工作區的畫面。
2. `View` 表示 `Screen` 內的主要頁籤或區塊，不單獨作為 route。
3. `Panel` 表示依附於畫面的右側資訊面板、drawer 或窄版 detail route。
4. `State` 表示清單的篩選狀態或 drill-down 情境，不是獨立畫面。
5. 文件、issue、commit message 與工程討論應使用 `Screen Code` / `View Code` / `Panel Code` / `State Code`，避免只寫「下一步畫面」「明細畫面」「批號畫面」等模糊名稱。

## 倉庫中心 Full Screen Roadmap

本表列出目前已規劃的完整畫面範圍，包含已實作、待 runtime review、proposal、deferred to V2 的畫面。它不是只列「下一步正在開發」的畫面；若後續新增畫面，應先補入本表再進行 API 或前端實作討論。

| Priority | Phase | Code | Type | 正式畫面名稱 | Route / UI Location | Implementation Status | Primary API | 說明 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P0 | V1 Core | `WarehouseOverviewScreen` | Screen | 倉庫中心總覽 | `/warehouse` | 已有第一版，需持續 runtime review 與細緻化 | `GET /api/v2/warehouse/dashboard` | Warehouse 入口畫面，呈現 KPI、庫存價值分類、倉位容量、風險警示摘要與待處理任務摘要。 |
| P0.1 | V1 Core | `WarehouseValueSpaceView` | View | 價值與倉位視圖 | `WarehouseOverviewScreen` 內的「價值與倉位」頁籤 | 已有第一版，需依 API runtime 持續調整 | `GET /api/v2/warehouse/dashboard` | 顯示庫存價值分類、倉位容量、板數與可用空間。 |
| P0.2 | V1 Core | `WarehouseRiskAlertView` | View | 風險警示視圖 | `WarehouseOverviewScreen` 內的「風險警示」頁籤 | 已有第一版，需與庫存明細 drill-down 對齊 | `GET /api/v2/warehouse/dashboard`、`GET /api/v2/warehouse/inventory` | 顯示迴轉、效期與安全水位風險；可導向風險批號清單狀態。 |
| P0.3 | V1 Core | `WarehousePendingTaskView` | View | 待處理入出庫視圖 | `WarehouseOverviewScreen` 內的「待處理入出庫」頁籤 | 已有第一版，作為任務工作台摘要入口 | `GET /api/v2/warehouse/tasks` | 顯示今日或逾期待處理的入庫、出庫、移倉、盤點或確認任務；完整任務操作由 `WarehouseTaskWorkbenchScreen` 承接。 |
| P0.4 | V1 Core | `WarehouseInventorySummaryView` | View | 庫存明細摘要視圖 | `WarehouseOverviewScreen` 內的「庫存明細」頁籤 | 已有第一版，作為批號清單摘要入口 | `GET /api/v2/warehouse/inventory` | 用於概覽頁快速查看批號層級庫存列；完整查詢、排序、分頁由 `WarehouseInventoryLotListScreen` 承接。 |
| P0.5 | V1 Core | `WarehouseCurrentLotPanel` | Panel | 目前批號資訊面板 | `WarehouseOverviewScreen` 右側 panel | 已有第一版，需與批號追蹤面板維持語意分工 | `GET /api/v2/warehouse/inventory` | 顯示目前選取批號的簡要數量、價值、安全水位、效期、流程狀態與關聯單據摘要。 |
| P1 | V1 Core | `WarehouseTaskWorkbenchScreen` | Screen | 倉庫任務工作台 | `/warehouse/task-workbench`；由 `WarehousePendingTaskView` drill-down 進入 | 已有第一版，已串接 task workbench API | `GET /api/v2/warehouse/task-workbench` | 任務專用工作區，顯示今日、逾期與近期入庫、出庫、移倉、品檢與出貨任務，支援 kanban/list、篩選、排序與分頁。 |
| P1.5 | V1 Core | `WarehouseTaskDetailPanel` | Panel | 倉庫任務追蹤面板 | `WarehouseTaskWorkbenchScreen` 右側 panel；窄版可作為 drawer 或 detail route | 已有第一版，已串接 task detail API | `GET /api/v2/warehouse/task-workbench/tasks/{taskId}` | 顯示單一任務的來源單據、相關批號、庫存可用性、阻塞原因、下一步負責部門與任務時間線。 |
| P1.8 | V2 Deferred | `WarehouseTaskExecutionScreen` | Screen | 倉庫任務執行工作區 | 建議 route：`/warehouse/task-execution/tasks/{taskId}`；由 `WarehouseTaskDetailPanel` 的處理動作進入 | Deferred to V2；Warehouse V1 read-only 範圍不實作 | `GET /api/v2/warehouse/task-execution/tasks/{taskId}`、`POST /api/v2/warehouse/task-execution/tasks/{taskId}/actions/validate`、`POST /api/v2/warehouse/task-execution/tasks/{taskId}/actions/commit` | 用於任務執行前上下文、批號候選、數量限制、板位資訊、validation 與 commit；因包含 mutation 邊界，延至 V2 review。 |
| P2 | V1 Core | `WarehouseInventoryLotListScreen` | Screen | 庫存批號明細清單 | `/warehouse/inventory/lots` | 已有第一版，已串接 inventory lots API | `GET /api/v2/warehouse/inventory/lots` | 批號層級清單畫面，支援倉庫、料品類別、料號、批號、風險、任務、可用狀態、關鍵字、排序與分頁。 |
| P3 | V1 Core | `WarehouseInventoryLotDetailPanel` | Panel | 庫存批號追蹤面板 | `WarehouseInventoryLotListScreen` 右側 panel；窄版可作為 drawer 或 detail route | 已有第一版，已串接 inventory lot detail API | `GET /api/v2/warehouse/inventory/lots/wh/{warehouseNo}/item/{itemNo}/batch/{batchNo}` | 顯示單一批號的庫存摘要、入出庫紀錄、預留、品檢保留、板位異動、未完成任務與風險。 |
| P4 | V1 Extension | `WarehouseAnalyticsScreen` | Screen | 倉庫分析工作區 | `/warehouse/analytics`；由 Warehouse nav 或總覽 KPI drill-down 進入 | 已有第一版，已串接 analytics overview 與 4 個 detail API | `GET /api/v2/warehouse/analytics/overview`、`GET /api/v2/warehouse/analytics/value-trend`、`GET /api/v2/warehouse/analytics/space-utilization`、`GET /api/v2/warehouse/analytics/risk-breakdown`、`GET /api/v2/warehouse/analytics/task-sla` | read-only 延伸畫面，分析庫存價值、倉位使用、風險分布與任務 SLA；不包含 POST / PUT。 |
| P5 | V2 Deferred | `WarehouseInventoryMovementLedgerScreen` | Screen | 庫存異動流水帳 | 建議 route：`/warehouse/inventory/movements`；由 Analytics、批號追蹤或任務工作台 drill-down 進入 | Deferred to next version；Warehouse V1 core 優先範圍暫不實作 | `GET /api/v2/warehouse/inventory/movements`、`GET /api/v2/warehouse/inventory/movements/summary` | read-only 追溯畫面，以 `inventory_record` 查詢入庫、出庫、批號、來源單據、數量與金額異動；因第一版優先 phase 為 core 的畫面，本畫面延至下一版。 |

## 倉庫中心 Screen State Naming

以下項目是既有 `Screen` 的篩選狀態或 drill-down 情境，不是獨立畫面。若工程任務要實作這些情境，應寫成「在 `WarehouseInventoryLotListScreen` 支援 `RiskLotListState`」或「在 `WarehouseTaskWorkbenchScreen` 支援 `OverdueTaskWorkbenchState`」，不要寫成「新增風險批號畫面」或「新增逾期任務畫面」。

| Priority | State Code | 顯示名稱 | 所屬畫面 | 觸發來源 | API Query / State |
| --- | --- | --- | --- | --- | --- |
| P1.1 | `TodayTaskWorkbenchState` | 今日任務工作台狀態 | `WarehouseTaskWorkbenchScreen` | 工作台預設入口或 `WarehousePendingTaskView` drill-down | `dateRange=today` |
| P1.2 | `OverdueTaskWorkbenchState` | 逾期任務工作台狀態 | `WarehouseTaskWorkbenchScreen` | 從逾期任務摘要、阻塞任務或看板 lane 進入 | `dateRange=overdue` |
| P1.3 | `RiskTaskWorkbenchState` | 風險任務工作台狀態 | `WarehouseTaskWorkbenchScreen` | 從阻塞、庫存不足、品檢保留或逾期風險摘要進入 | `riskOnly=true` |
| P2.1 | `RiskLotListState` | 風險批號清單狀態 | `WarehouseInventoryLotListScreen` | 從 `WarehouseOverviewScreen` 的風險警示或 `WarehouseRiskAlertView` drill-down | `riskType` / `riskOnly` 類條件 |
| P2.2 | `PendingTaskLotListState` | 待處理批號清單狀態 | `WarehouseInventoryLotListScreen` | 從 `WarehouseTaskWorkbenchScreen` 或 `WarehousePendingTaskView` drill-down | `taskType` 或未完成任務條件 |
| P2.3 | `AvailableLotListState` | 可用庫存批號清單狀態 | `WarehouseInventoryLotListScreen` | 從可用庫存 KPI、追溯或篩選器入口 | `availability=available` |
| P2.4 | `QualityHoldLotListState` | 品檢保留批號清單狀態 | `WarehouseInventoryLotListScreen` | 從品檢保留 KPI、篩選器或 detail drill-down | `availability=quality_hold` |

## Orders Workspace Screen Roadmap

本節列出 Orders Dashboard 前端畫面完成後端 API 串接後的正式畫面命名與實作狀態。Orders 第一版採 read-only 履約風險管理範圍，前端已依工程師確認的 `GET /api/v2/orders/dashboard` 與 `GET /api/v2/orders/{order_no}/fulfillment` 進行串接；Enum 顯示字串由前端負責，並支援多國語系轉換。

| Priority | Phase | Code | Type | 正式畫面名稱 | Route / UI Location | Implementation Status | Primary API | 說明 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P0 | V1 Core | `OrdersWorkspaceScreen` | Screen | 訂單履約工作區 | `/orders` | 已有第一版，已串接 Orders Dashboard 與 Fulfillment API | `GET /api/v2/orders/dashboard`、`GET /api/v2/orders/{order_no}/fulfillment` | Orders 模組入口畫面，呈現訂單 KPI、訂單清單、交期風險、接單承諾、毛利與收款摘要，並透過右側 panel 檢視選取訂單履約狀態。 |
| P0.1 | V1 Core | `OrdersOverviewView` | View | 訂單總覽視圖 | `OrdersWorkspaceScreen` 內的「訂單總覽」頁籤 | 已有第一版，已串接 dashboard API | `GET /api/v2/orders/dashboard` | 顯示進行中訂單、客戶、產品、交期、目前階段、交期風險、生產可行性與付款狀態。 |
| P0.2 | V1 Core | `OrdersCommitmentView` | View | 接單承諾視圖 | `OrdersWorkspaceScreen` 內的「接單承諾」頁籤 | 已有第一版，已串接 dashboard API；ATP/CTP 依 API 文件延至下一版 | `GET /api/v2/orders/dashboard` | 顯示接單承諾判定、承諾日期與需要協調的訂單；第一版 `commitmentDecision` 以後端回傳 enum 由前端轉譯。 |
| P0.3 | V1 Core | `OrdersDeliveryRiskView` | View | 交期風險視圖 | `OrdersWorkspaceScreen` 內的「交期風險」頁籤 | 已有第一版，已串接 dashboard API | `GET /api/v2/orders/dashboard` | 聚焦非正常交期風險訂單，呈現風險原因、交期、生產可行性與目前處理狀態。 |
| P0.4 | V1 Core | `OrdersMarginPaymentView` | View | 毛利與收款視圖 | `OrdersWorkspaceScreen` 內的「毛利 / 收款」頁籤 | 已有第一版，已串接 dashboard API | `GET /api/v2/orders/dashboard` | 呈現預估毛利、實際毛利、付款狀態與收款風險摘要；付款與毛利訊號由 dashboard payload 映射。 |
| P0.5 | V1 Core | `OrdersFulfillmentView` | View | 履約進度視圖 | `OrdersWorkspaceScreen` 內的「履約進度」頁籤 | 已有第一版，已串接 dashboard API 與 selected order fulfillment API | `GET /api/v2/orders/dashboard`、`GET /api/v2/orders/{order_no}/fulfillment` | 以訂單履約 workflow 視角檢視備料、生產、品檢、出貨與收款狀態；右側明細由 `OrderFulfillmentDetailPanel` 承接。 |
| P1 | V1 Core | `OrderFulfillmentDetailPanel` | Panel | 訂單履約追蹤面板 | `OrdersWorkspaceScreen` 右側 panel；窄版可作為 drawer 或 detail route | 已有第一版，已串接 fulfillment API，API 失敗時保留 controlled fallback | `GET /api/v2/orders/{order_no}/fulfillment` | 顯示單一訂單的履約依賴、workflow 節點、負責部門、狀態、來源單號與 comment；Enum 由前端多國語系轉換。 |

## Orders Workspace State Naming

以下項目是 `OrdersWorkspaceScreen` 內的篩選狀態或 drill-down 情境，不是獨立畫面。若後續工程任務需實作，應寫成「在 `OrdersWorkspaceScreen` 支援 `HighRiskOrdersState`」，不要寫成「新增高風險訂單畫面」。

| Priority | State Code | 顯示名稱 | 所屬畫面 | 觸發來源 | API Query / State |
| --- | --- | --- | --- | --- | --- |
| P0.3.1 | `HighRiskOrdersState` | 高風險訂單狀態 | `OrdersWorkspaceScreen` | 從 KPI、交期風險視圖或管理看板 drill-down | `deliveryRisk=high_risk` |
| P0.3.2 | `AttentionOrdersState` | 注意訂單狀態 | `OrdersWorkspaceScreen` | 從交期風險摘要或風險篩選器進入 | `deliveryRisk=attention` |
| P0.2.1 | `DeferredCommitmentOrdersState` | 待承諾協調訂單狀態 | `OrdersWorkspaceScreen` | 從接單承諾視圖或承諾檢查 KPI 進入 | `commitmentDecision=deferred` |
| P0.4.1 | `MarginPaymentRiskOrdersState` | 毛利與收款風險訂單狀態 | `OrdersWorkspaceScreen` | 從毛利 / 收款視圖、付款風險 KPI 或財務 drill-down 進入 | 前端以 dashboard payload 的 margin / payment signal 映射；若後端後續提供 query，再同步補齊。 |

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
| `WarehouseTaskWorkbenchScreen` | 已有第一版，已串接 task workbench API。 | 依 runtime payload 檢查任務 lane、篩選、排序、分頁與 mock fallback 邊界。 |
| `WarehouseTaskDetailPanel` | 已有第一版，已串接 task detail API。 | 依 runtime payload 檢查來源單據、相關批號、庫存可用性、阻塞原因、下一步負責部門與任務時間線。 |
| `WarehouseTaskExecutionScreen` | Deferred to V2；第一版 read-only 暫不實作含 POST / PUT 的畫面。 | 保留既有 proposal 作為下一版任務執行討論基礎，當前不作為下一步 API 設計目標。 |
| `WarehouseInventoryLotListScreen` | 已有第一版，已串接 inventory lots API。 | 依後端 runtime payload 檢查欄位呈現、篩選結果、分頁與空狀態。 |
| `WarehouseInventoryLotDetailPanel` | 已有第一版，已串接 inventory lot detail API。 | 依後端 runtime payload 檢查入出庫紀錄、預留、品檢、板位、任務與風險資料集呈現。 |
| `WarehouseAnalyticsScreen` | 已有第一版，已串接 analytics overview 與 4 個 detail API。 | 依工程師實機資料檢查 API payload、篩選條件、drill-down query 與空狀態呈現。 |
| `WarehouseInventoryMovementLedgerScreen` | Deferred to next version；本版略過。 | 暫不進行工程師 review、後端實作或前端串接；文件保留作為下一版追溯畫面討論基礎。 |
| `OrdersWorkspaceScreen` | 已有第一版，已串接 `GET /api/v2/orders/dashboard` 與 `GET /api/v2/orders/{order_no}/fulfillment`。 | 依工程師實機資料檢查 dashboard payload、selected order fulfillment payload、enum 多國語系顯示、空狀態與 fallback 邊界。 |
| `OrderFulfillmentDetailPanel` | 已有第一版，已串接 selected order fulfillment API。 | 依 runtime payload 檢查 workflow 節點、dependencies、來源單號、comment、負責部門與狀態 tone 呈現。 |

## Roadmap Coverage Confirmation

截至 2026-07-03，本文件已涵蓋目前已知的「倉庫中心」完整規劃畫面、附屬 panel、view 與 state。後續若新增未列於本文件的畫面，需先補入本清單並指定 `Screen` / `View` / `Panel` / `State` 類型。

目前 V1 Core 畫面骨架已具備第一版前端實作，後續主要工作為：

1. runtime review 與 API payload 欄位對齊。
2. 空狀態、錯誤狀態與 mock fallback 細緻化。
3. `WarehouseAnalyticsScreen` 的後端 API runtime review。
4. 優先轉入下一個 phase 為 core 的跨模組畫面 API 設計，例如 Orders fulfillment-risk read-only API。
5. `WarehouseInventoryMovementLedgerScreen` 與 `WarehouseTaskExecutionScreen` 皆延至下一版討論。

因此，討論「整個規劃畫面清單」時，應以 `Full Screen Roadmap` 主表為準；討論「現階段下一步實作」時，才依 `Current Completion Summary` 的 next focus 決定。

