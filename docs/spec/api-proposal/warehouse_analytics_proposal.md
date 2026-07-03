# Warehouse Analytics API Proposal

> Status: Proposal / Pending Engineer Review
> Target UI Preview: `docs/spec/api-proposal/warehouse_analytics_static_preview.html`
> Flow / Algorithm: `docs/spec/api-proposal/warehouse_analytics_flow_algorithm.md`
> Related V1 Rule: Warehouse V1 frontend is read-only; this proposal contains GET APIs only.

## 工程師提問V3
1. 針對 `/api/v2/warehouse/analytics/overview`
   - 「第一版避免 silent fallback：若同時提供 `dateFrom/dateTo` 與 `period`，後端需驗證兩者一致；若不一致，回傳參數錯誤，不自動猜測使用哪一個。前端應優先只送一種期間模式：快捷查詢送 `period`，自訂區間送 `dateFrom/dateTo` 並省略 `period`。」 
   是否能將查詢參數改為 `date` 與 `period`，並由後端自行推算 `dateFrom`？

### 工程師回覆V3理解與更新

| 工程師提問V3 | 工程師回覆V3 | 理解與確認 | 文件更新 |
| --- | --- | --- | --- |
| 是否能將查詢參數改為 `date` 與 `period`，並由後端自行推算 `dateFrom`？ | 工程師提問已明確提出此調整方向。 | 採用。第一版 Analytics API 期間查詢統一改為 `date + period`：`date` 為查詢基準/截止 UTC timestamp，未提供時使用伺服器目前時間；`period` 為回溯區間，第一版支援 `7d`、`30d`、`90d`，未提供時預設 `30d`。後端依 `date` 與 `period` 推算 `payload.range.startTimestamp` 與 `payload.range.endTimestamp`，前端不再傳 `dateFrom/dateTo`。 | 已更新 Shared Query Parameters、Period Resolution Rules、Field Description、Frontend Interaction Notes，並同步更新 flow/algorithm。 |


## 工程師提問V2
1. 針對 `/api/v2/warehouse/analytics/overview`
   - 若查詢參數 `dateFrom` 與 `period` 同時存在且回傳數值，若由 `dateFrom` 推算天數後發現與所填 `period` 數值不一致，應如何處理？  
   - 將 `warehouseNo` 調整為 `warehouse_no`，以與其他 API 命名風格保持一致
   - `drilldownQuery` 是否能由前端保存參數數值，並在需要時組合成導向使用者操作的 Query String？  

### 工程師回覆V2理解與更新

| 工程師提問V2 | 工程師回覆V2 | 理解與確認 | 文件更新 |
| --- | --- | --- | --- |
| `dateFrom` 與 `period` 同時存在但推算天數不一致時，應如何處理？ | 原文件未提供獨立工程師回覆；V3 已提出更簡化的 `date + period` 設計。 | V3 已取代此衝突處理需求：前端不再傳 `dateFrom/dateTo`，後端一律由 `date + period` 推算區間，因此不會發生 `dateFrom` 與 `period` 不一致問題。 | 已以 V3 Period Resolution Rules 取代原 V2 規則。 |
| 將 `warehouseNo` 調整為 `warehouse_no`，以與其他 API 命名風格保持一致。 | 工程師提問已明確建議調整為 `warehouse_no`。 | Query parameter 改為 `warehouse_no`；response payload 內的 `warehouseNo` 維持不變，以延續現有 Warehouse API response 欄位風格。 | 已更新 Shared Query Parameters 與相關說明。 |
| `drilldownQuery` 是否能由前端保存參數數值，並在需要時組合成導向使用者操作的 Query String？ | 原文件未提供獨立工程師回覆；本次由 Codex 建議採用前端組合方式。 | 可以。後端不回傳 `drilldownQuery`，只回傳 `riskType`、`taskType`、`warehouseNo` 等結構化欄位；前端依畫面狀態自行組合導向 URL / query string。 | 已移除 response 中的 `drilldownQuery`，並更新 Drill-down Design。 |

## 工程師提問與確認

| 工程師提問 | 工程師回覆 | 理解與確認 | 文件更新 |
| --- | --- | --- | --- |
| 針對 `/api/v2/warehouse/analytics/overview`，請統一查詢參數的設計風格與命名，例如使用 `dateFrom` / `dateTo` / `period` 還是 `date` / `dateRange`。 | 原文件此區未提供獨立工程師回覆；V3 已提出改用 `date + period`。 | 採用 `date + period + bucket`：`date` 為查詢基準/截止時間，`period` 表示回溯區間，`bucket` 表示趨勢粒度。倉儲篩選 query parameter 維持 `warehouse_no`，以符合既有 Warehouse API 風格。 | 已更新 Shared Query Parameters、Period Resolution Rules 與 flow/algorithm。 |
| 請補齊回傳資料結構中所有欄位的詳細說明，確保每個欄位的用途、型別與可能值都清楚定義。 | 原文件此區未提供獨立工程師回覆；本次依提問補齊提案。 | 補齊 `serverTimestamp`、`timezone`、`range`、`kpi`、`valueTrend`、`spaceTrend`、`riskBreakdown`、`taskSla` 全部欄位說明。 | 已擴充 Field Description。 |
| 請針對 `drilldownQuery` 欄位提供完整解釋，例如欄位的設計目的。 | 原文件此區未提供獨立工程師回覆；本次依提問補齊提案。 | V2 已調整為後端不回傳 `drilldownQuery`；前端以 response 結構化欄位與目前畫面狀態自行組合導向 query string。 | 已更新 Drill-down Design，並從 response 移除 `drilldownQuery`。 |
| 請勿直接覆蓋「工程師回覆」欄位的資料，應新增獨立欄位以填寫確認資訊。 | 原文件此區未提供獨立工程師回覆；本次依提問補齊提案。 | 保留工程師原始回覆，新增「理解與確認」與「文件更新」欄位紀錄本次處理結果。 | 已更新本節與文件底部 review table。 |

## Screen Intent

`WarehouseAnalyticsScreen` 是第一版 read-only 範圍內，略過 `WarehouseTaskExecutionScreen` 後的下一步建議畫面。此畫面不處理入庫、出庫、放行、解除阻塞或任何任務執行寫入，而是提供管理者與倉庫主管以下分析：

1. 庫存價值在原料、物料、膠捲、在製品、製成品等類別的變化。
2. 各倉儲空間、板位與可用容量的使用趨勢。
3. 迴轉、效期、安全水位、品檢保留與庫存不足風險的分布。
4. 入庫、出庫、移倉、品檢、出貨任務的準時率、逾期率與阻塞率。
5. 從分析結果 drill-down 至既有 read-only 畫面，例如 `WarehouseInventoryLotListScreen` 或 `WarehouseTaskWorkbenchScreen`。

本提案不包含 POST / PUT / DELETE API。若後續需要調整安全水位、建立任務、解除阻塞或確認出入庫，應延至下一版 mutation API 設計。

## API Summary

| URL | Method | Description | Status | Review Note |
| --- | --- | --- | --- | --- |
| `/api/v2/warehouse/analytics/overview` | GET | 查詢倉庫分析總覽資料 | Proposal / Pending Engineer Review | 首屏聚合 API，回傳 KPI、價值趨勢、倉位使用、風險摘要與任務效率摘要。 |
| `/api/v2/warehouse/analytics/value-trend` | GET | 查詢庫存價值趨勢 | Proposal / Pending Engineer Review | 供價值趨勢圖 drill-down 使用。 |
| `/api/v2/warehouse/analytics/space-utilization` | GET | 查詢倉位與板位使用趨勢 | Proposal / Pending Engineer Review | 供倉儲容量與寄倉規劃分析使用。 |
| `/api/v2/warehouse/analytics/risk-breakdown` | GET | 查詢庫存風險分布 | Proposal / Pending Engineer Review | 供迴轉、效期、安全水位、品檢保留與庫存不足分析使用。 |
| `/api/v2/warehouse/analytics/task-sla` | GET | 查詢倉庫任務處理效率 | Proposal / Pending Engineer Review | 供任務準時率、逾期、阻塞、平均處理時間分析使用。 |

## Shared Query Parameters

### Query Parameter Design Notes

Analytics API 第一版統一採用 `date + period + bucket`：

1. `date` 表示查詢基準/截止時間，UTC timestamp；未提供時使用伺服器目前時間。
2. `period` 表示回溯區間，第一版支援 `7d`、`30d`、`90d`；未提供時預設 `30d`。
3. `bucket` 表示趨勢資料分桶粒度，第一版支援 `day`、`week`、`month`。
4. 不使用 `dateRange`，避免與 `WarehouseTaskWorkbenchScreen` 的 `today`、`overdue`、`next_7_days` 等任務語意型範圍混淆。
5. Query parameter 命名沿用既有 Warehouse API 風格：倉儲篩選使用 `warehouse_no`；response payload 仍使用既有 camelCase 欄位，例如 `warehouseNo`。

### Period Resolution Rules

| Condition | Backend Behavior | Response Range |
| --- | --- | --- |
| 未提供 `date`，未提供 `period` | `date` 使用伺服器目前 UTC timestamp，`period` 使用預設 `30d`。 | `endTimestamp = server now`；`startTimestamp = endTimestamp - 30d`。 |
| 僅提供 `date` | `period` 使用預設 `30d`。 | `endTimestamp = date`；`startTimestamp = date - 30d`。 |
| 僅提供 `period` | `date` 使用伺服器目前 UTC timestamp。 | `endTimestamp = server now`；`startTimestamp = endTimestamp - period`。 |
| 同時提供 `date` 與 `period` | 直接使用 `date` 作為截止時間，依 `period` 回推起始時間。 | `endTimestamp = date`；`startTimestamp = date - period`。 |
| 提供不支援的 `period` | 第一版建議 fallback 至 `30d`，並在 `payload.range.period` 回傳實際採用值。 | `payload.range.period = 30d`。 |

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| date | Integer | NO | 查詢基準/截止時間，UTC timestamp；未提供時使用伺服器目前時間。 |
| period | String | NO | 查詢期間代碼；建議支援 `7d`、`30d`、`90d`。第一版預設 `30d`。 |
| bucket | String | NO | 趨勢粒度；建議支援 `day`、`week`、`month`。第一版預設 `day`。 |
| warehouse_no | String | NO | 倉儲別名 no；提供時只回傳指定倉儲資料，對應資料庫 `warehouse_no` / `ship_wh_alias.no`。 |
| itemCategory | Integer | NO | 料品品項類別；原料(1)、物料(2)、膠捲(3)、在製品(4)、製成品(5)。 |
| taskType | Integer | NO | 任務類型；用於 task SLA endpoint。 |

## Numeric Format Rules

| Numeric Meaning | Format |
| --- | --- |
| 單價 | 四捨五入取至小數點第 4 位 |
| 重量或數量 | 四捨五入取至小數點第 2 位 |
| 金額 | 四捨五入取整數 |
| 比率 | 四捨五入取至小數點第 2 位 |

## GET /api/v2/warehouse/analytics/overview

### Basic Information

| URL | Method | Description |
| --- | --- | --- |
| `/api/v2/warehouse/analytics/overview` | GET | 查詢倉庫分析總覽資料 |

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "serverTimestamp": "Integer",
    "timezone": "String",
    "range": {
      "period": "String",
      "bucket": "String",
      "startTimestamp": "Integer",
      "endTimestamp": "Integer"
    },
    "kpi": {
      "totalInventoryValue": "Integer",
      "valueChangeRate": "Float",
      "usedPallets": "Float",
      "spaceUtilizationRate": "Float",
      "riskLotCount": "Integer",
      "openTaskCount": "Integer",
      "overdueTaskRate": "Float"
    },
    "valueTrend": [
      {
        "bucketStart": "Integer",
        "bucketLabel": "String",
        "itemCategory": "Integer",
        "inventoryValue": "Integer",
        "availableValue": "Integer",
        "reservedValue": "Integer",
        "qualityHoldValue": "Integer"
      }
    ],
    "spaceTrend": [
      {
        "bucketStart": "Integer",
        "warehouseNo": "String",
        "warehouseName": "String",
        "usedPallets": "Float",
        "reservedPallets": "Float",
        "availablePallets": "Float",
        "utilizationRate": "Float"
      }
    ],
    "riskBreakdown": [
      {
        "riskType": "String",
        "riskLevel": "Integer",
        "lotCount": "Integer",
        "inventoryValue": "Integer",
        "quantity": "Float"
      }
    ],
    "taskSla": [
      {
        "taskType": "Integer",
        "openTaskCount": "Integer",
        "completedTaskCount": "Integer",
        "overdueTaskCount": "Integer",
        "blockedTaskCount": "Integer",
        "onTimeRate": "Float",
        "averageLeadTimeHours": "Float"
      }
    ]
  }
}
```

### Field Description

| Field Path | Type | Description | Enum |
| --- | --- | --- | --- |
| code | Integer | API 執行結果代碼；沿用既有 restserver 成功/失敗回傳規則。 |  |
| message | String | API 執行結果訊息；成功時可回傳空字串或成功訊息，錯誤時回傳錯誤摘要。 |  |
| payload.serverTimestamp | Integer | 後端產生此 response 的 UTC timestamp，供前端顯示資料更新時間。 |  |
| payload.timezone | String | 後端採用的時區代碼；預設可依 `x-timezone` header 或系統設定回填。 |  |
| payload.range.period | String | 本次實際採用的查詢期間代碼；回傳 `7d`、`30d`、`90d`，若 request 未提供或提供不支援值，回傳後端實際採用值。 |  |
| payload.range.bucket | String | 本次實際採用的趨勢粒度；允許值第一版為 `day`、`week`、`month`。 |  |
| payload.range.startTimestamp | Integer | 本次查詢實際起始 UTC timestamp；由 `date - period` 推算。 |  |
| payload.range.endTimestamp | Integer | 本次查詢實際截止 UTC timestamp；由 request `date` 或伺服器目前時間決定。 |  |
| payload.kpi.totalInventoryValue | Integer | 查詢截止時間的目前庫存總價值，來源為庫存快照中各類別 `inventoryValue` 加總，金額四捨五入取整數。 |  |
| payload.kpi.valueChangeRate | Float | 與查詢起始時間相比的庫存總價值變化率；公式為 `(endValue - startValue) / startValue * 100`，`startValue` 為 0 時回傳 0.0。 |  |
| payload.kpi.usedPallets | Float | 查詢截止時間已佔用或保留的總板數，來源為 `warehouse_pallet_movement` 與相關保留資料彙總。 |  |
| payload.kpi.spaceUtilizationRate | Float | 查詢截止時間的總倉位使用率；公式為 `usedPallets / totalPallets * 100`，`totalPallets` 為 0 時回傳 0.0。 |  |
| payload.kpi.riskLotCount | Integer | 查詢截止時間存在任一風險類型的批號庫存筆數，依 `warehouseNo + itemNo + batchNo` 去重。 |  |
| payload.kpi.openTaskCount | Integer | 查詢截止時間仍開放中的倉庫任務數，包含 pending、partial、blocked 狀態。 |  |
| payload.kpi.overdueTaskRate | Float | 開放任務中已逾期任務比例；公式為 `overdueTaskCount / openTaskCount * 100`，`openTaskCount` 為 0 時回傳 0.0。 |  |
| payload.valueTrend[].bucketStart | Integer | 此趨勢 bucket 的起始 UTC timestamp。 |  |
| payload.valueTrend[].bucketLabel | String | 前端圖表可直接顯示的 bucket 標籤，例如 `2026-06-17` 或 `2026-W25`。 |  |
| payload.valueTrend[].itemCategory | Integer | 料品品項類別，前端負責多國語系轉換。 | EItemCategory |
| payload.valueTrend[].inventoryValue | Integer | 該 bucket、該料品類別的庫存總價值。 |  |
| payload.valueTrend[].availableValue | Integer | 該 bucket、該料品類別的可用庫存價值；公式為 `inventoryValue - reservedValue - qualityHoldValue`，最低回傳 0。 |  |
| payload.valueTrend[].reservedValue | Integer | 該 bucket、該料品類別的預留庫存價值，來源為 `warehouse_inventory_reservation`。 |  |
| payload.valueTrend[].qualityHoldValue | Integer | 該 bucket、該料品類別的品檢保留價值，來源為 `warehouse_quality_hold`。 |  |
| payload.spaceTrend[].bucketStart | Integer | 此倉位趨勢 bucket 的起始 UTC timestamp。 |  |
| payload.spaceTrend[].warehouseNo | String | 倉儲別名 no，對應 `ship_wh_alias.no`。 |  |
| payload.spaceTrend[].warehouseName | String | 倉儲顯示名稱，來源優先使用 `ship_wh_alias`。 |  |
| payload.spaceTrend[].usedPallets | Float | 該 bucket、該倉儲已佔用板數。 |  |
| payload.spaceTrend[].reservedPallets | Float | 該 bucket、該倉儲已預留板數。 |  |
| payload.spaceTrend[].availablePallets | Float | 該 bucket、該倉儲可用板數；公式為 `totalPallets - usedPallets - reservedPallets`，最低回傳 0。 |  |
| payload.spaceTrend[].utilizationRate | Float | 該 bucket、該倉儲使用率；公式為 `(usedPallets + reservedPallets) / totalPallets * 100`，`totalPallets` 為 0 時回傳 0.0。 |  |
| payload.riskBreakdown[].riskType | String | 風險類型代碼，前端負責多國語系轉換。 | TURNOVER_OVER_30_DAYS、SHELF_LIFE_LT_ONE_THIRD、BELOW_SAFETY_STOCK、QUALITY_HOLD、INVENTORY_SHORTAGE |
| payload.riskBreakdown[].riskLevel | Integer | 風險等級代碼，來源為 `warehouse_risk_rule` 或後端規則判斷；數值越高表示風險越高。 |  |
| payload.riskBreakdown[].lotCount | Integer | 符合該風險類型的批號庫存筆數，依 `warehouseNo + itemNo + batchNo` 去重。 |  |
| payload.riskBreakdown[].inventoryValue | Integer | 符合該風險類型的批號庫存價值加總。 |  |
| payload.riskBreakdown[].quantity | Float | 符合該風險類型的批號庫存數量加總；混合單位情境下僅作同類別內部分析參考。 |  |
| payload.taskSla[].taskType | Integer | 任務類型，前端負責多國語系轉換。 | EWorkflowTaskType |
| payload.taskSla[].openTaskCount | Integer | 該任務類型目前開放任務數，來源為 `workflow_task_state`。 |  |
| payload.taskSla[].completedTaskCount | Integer | 查詢期間內完成的任務數，優先以 `workflow_task_event.eventCode = workflow.task.completed` 判斷；無 completed event 時不以 `updateTime` 推測。 |  |
| payload.taskSla[].overdueTaskCount | Integer | 該任務類型目前逾期且尚未完成/取消的任務數。 |  |
| payload.taskSla[].blockedTaskCount | Integer | 該任務類型目前 blocked 任務數。 |  |
| payload.taskSla[].onTimeRate | Float | 該任務類型準時完成率；僅以有 completed event 且可判斷 dueTimestamp 的資料計算，分母為 0 時回傳 0.0。 |  |
| payload.taskSla[].averageLeadTimeHours | Float | 該任務類型平均處理時數；以 first event 到 completed event 計算，缺少 event 時回傳 0.0 且不得用 `workflow_task_state.updateTime` 推測。 |  |

### Drill-down Design

第一版不由後端回傳 `drilldownQuery`。後端只回傳結構化欄位，前端依使用者操作與目前畫面狀態自行組合導向 URL / query string：

1. 風險分布點選時，前端可使用 `riskBreakdown[].riskType` 組合 `WarehouseInventoryLotListScreen` 查詢條件，例如 `riskType=BELOW_SAFETY_STOCK`。
2. 任務 SLA 點選時，前端可使用 `taskSla[].taskType` 與畫面狀態組合 `WarehouseTaskWorkbenchScreen` 查詢條件，例如 `dateRange=overdue&taskType=5`。
3. 若目前畫面已有 `warehouse_no`、`itemCategory`、`date` 或 `period` 狀態，前端可自行決定是否帶入 drill-down 目標頁。
4. 後端不需要保存前端路由規則，也不得回傳會造成資料寫入的 action code。

## Detail Endpoints

第一版建議保留 `overview` + 4 個 detail GET endpoint。最佳化策略如下：

1. `overview` 用於首屏載入，只回傳 KPI 與首頁可直接呈現的摘要資料。
2. `value-trend`、`space-utilization` 可在前端圖表區進入 viewport 或使用者切換期間時 lazy load。
3. `risk-breakdown` 與 `task-sla` 用於使用者需要展開分析或 drill-down 前的精細統計。
4. 各 detail endpoint 可共用後端查詢模組，但 response 範圍限於該圖表所需資料，避免 `overview` payload 過大。

### GET /api/v2/warehouse/analytics/value-trend

回傳 `payload.valueTrend[]` 與 category summary。此 API 可與 overview 共用查詢邏輯，供使用者放大趨勢圖或切換 period/bucket 時使用。

### GET /api/v2/warehouse/analytics/space-utilization

回傳 `payload.spaceTrend[]`、warehouse summary 與容量風險。第一版僅做 read-only 分析，不調整倉位容量、不建立移倉任務。

### GET /api/v2/warehouse/analytics/risk-breakdown

回傳 `payload.riskBreakdown[]`。前端可依 `riskType` 與目前畫面狀態自行組合 query string，導向 `WarehouseInventoryLotListScreen`，例如：

```txt
/warehouse/inventory/lots?riskType=BELOW_SAFETY_STOCK
```

### GET /api/v2/warehouse/analytics/task-sla

回傳 `payload.taskSla[]` 與任務類型、負責部門、逾期、阻塞統計。前端可導向 `WarehouseTaskWorkbenchScreen`，例如：

```txt
/warehouse/task-workbench?dateRange=overdue&taskType=5
```

## Database Tables Used

| Table | Purpose |
| --- | --- |
| inventory_month_statistic | 類別層級月結庫存價值基準，可用於長區間趨勢。 |
| inventory_item_month_statistic | 料品/批號層級月結庫存量與庫存價值基準。 |
| inventory_delta | 月結後異動補算。 |
| inventory_record | 短區間或資料缺漏時的防護性補算。 |
| warehouse_pallet_movement | 倉位、板位使用與異動紀錄。 |
| warehouse_inventory_reservation | 預留數量、預留價值與預留板數。 |
| warehouse_quality_hold | 品檢保留數量與價值。 |
| item_safety_stock | 安全水位判斷。 |
| warehouse_risk_rule | 風險規則、風險等級與前端 i18n key。 |
| workflow_task_state | 任務目前狀態、任務類型、負責部門、預計完成時間。 |
| workflow_task_event | 任務歷史事件，可用於任務 lead time 與流程效率分析。 |
| ship_wh_alias | 倉儲別名、倉儲顯示名稱與倉儲類型。 |
| batch_number | 批號來源與效期資訊。 |

## Frontend Interaction Notes

| UI Action | API Behavior |
| --- | --- |
| 首次進入分析頁 | 呼叫 `GET /api/v2/warehouse/analytics/overview?period=30d&bucket=day`；未提供 `date` 時由後端使用伺服器目前時間 |
| 切換期間 | KPI 區重新呼叫 overview；已展開的圖表區呼叫對應 detail endpoint |
| 點選庫存價值趨勢 | 呼叫 value-trend endpoint，以取得該圖表需要的完整 bucket 與 category summary |
| 點選倉位使用趨勢 | 呼叫 space-utilization endpoint，以取得倉儲容量與板位趨勢 |
| 點選風險分布 | 導向 `WarehouseInventoryLotListScreen` 對應 risk state |
| 點選任務 SLA | 導向 `WarehouseTaskWorkbenchScreen` 對應 task state |

## 工程師提問追蹤

| 項目 | 需確認原因 | 工程師回覆 | 理解與確認 | 文件更新 | 工程師回覆V2 |
| --- | --- | --- | --- | --- | --- |
| 第一版是否接受 `overview` 聚合 API 加 4 個 detail GET endpoint | 影響前端首次載入效能與後端查詢分工。 | 你建議採取何種方式，能夠達到最佳化？ | 建議保留 `overview` + 4 個 detail GET endpoint，但採「首屏輕量聚合、重圖表 lazy load」：`overview` 回傳 KPI 與首頁所需摘要；使用者放大圖表、切換區間或進入分析 detail 時再呼叫 detail endpoint。此做法可避免單一 API 回傳過大 payload，也能讓前端分段載入。 | 已補充 Detail Endpoints 與 Frontend Interaction Notes 的使用定位；流程文件同步補充效能策略。 | 依照你所建議的方法進行實作。 |
| `period` 第一版是否只支援 `7d`、`30d`、`90d` | 避免長區間查詢造成即時計算壓力。 | 可以，後續如有需求再新增。 | 已確認第一版限制 `7d`、`30d`、`90d`，預設 `30d`。 | Shared Query Parameters 與流程文件維持此限制。 |  |
| `spaceTrend` 是否可先用 `warehouse_pallet_movement` 現有紀錄計算 | 影響倉位趨勢準確度與是否需要新增每日快照表。 | 可以，後續如有需求再新增每日快照表。 | 第一版不新增每日倉位快照表，先使用 `warehouse_pallet_movement` 計算可取得的歷史趨勢。若歷史不足，只回傳可證明的 bucket，不推測不存在的歷史。 | 流程文件 Step 4 已明確限制不足資料時不得推測。 |  |
| `taskSla.averageLeadTimeHours` 是否以 workflow_task_event 計算 | 需確認事件資料是否足夠完整。 | 目前設計中包含哪些事件資料？ | `workflow_task_event` 已規劃共用事件：`workflow.task.created`、`workflow.task.assigned`、`workflow.task.started`、`workflow.task.partiallyProcessed`、`workflow.task.blocked`、`workflow.task.blockResolved`、`workflow.task.completed`、`workflow.task.cancelled`、`workflow.task.refLinked`、`workflow.task.quantityAdjusted`。`averageLeadTimeHours` 只使用 first event 到 `workflow.task.completed`，不以狀態更新時間推測。 | 流程文件 Step 6 已補充事件代碼與 SLA 計算規則。 | 第一版先以這些事件資料為主，後續如有需求再行新增。 |
| 若 workflow_task_event 尚無資料，task SLA 是否退回使用 workflow_task_state creationTime/updateTime | 避免 API 在第一版資料不足時無法回傳。 | 當 workflow_task_event 無資料時，回傳空陣列即可，還是有其他需要考量的情況？ | 採用不推測原則：若查詢期間完全沒有 `workflow_task_event`，`taskSla[]` 可回傳空陣列。`workflow_task_state` 仍可用於 overview KPI 的 `openTaskCount` 與目前逾期判斷，但不拿 `creationTime/updateTime` 反推完成時間或 lead time。 | 流程文件 Step 6 與「不得推測」規則已更新。 |  |
