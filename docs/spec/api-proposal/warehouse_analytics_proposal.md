## 工程師提問
1. 針對 /api/v2/warehouse/analytics/overview，
   - 「請統一查詢參數的設計風格與命名，例如使用 dateFrom / dateTo / period 還是 date / dateRange
   - 請補齊回傳資料結構中所有欄位的詳細說明，確保每個欄位的用途、型別與可能值都清楚定義。
   - 請針對 drilldownQuery 欄位提供完整解釋，如: 欄位的設計目的
2.  請勿直接覆蓋「工程師回覆」欄位的資料，應新增獨立欄位以填寫確認資訊。
# Warehouse Analytics API Proposal

> Status: Proposal / Pending Engineer Review
> Target UI Preview: `docs/spec/api-proposal/warehouse_analytics_static_preview.html`
> Flow / Algorithm: `docs/spec/api-proposal/warehouse_analytics_flow_algorithm.md`
> Related V1 Rule: Warehouse V1 frontend is read-only; this proposal contains GET APIs only.

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

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| dateFrom | Integer | NO | 查詢起始時間，UTC timestamp；未提供時由後端依 period 推算。 |
| dateTo | Integer | NO | 查詢結束時間，UTC timestamp；未提供時以查詢當下為準。 |
| period | String | NO | 查詢期間代碼；建議支援 `7d`、`30d`、`90d`。第一版預設 `30d`。 |
| bucket | String | NO | 趨勢粒度；建議支援 `day`、`week`、`month`。第一版預設 `day`。 |
| warehouse_no | String | NO | 倉儲別名 no；提供時只回傳指定倉儲資料。 |
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
        "quantity": "Float",
        "drilldownQuery": "String"
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
        "averageLeadTimeHours": "Float",
        "drilldownQuery": "String"
      }
    ]
  }
}
```

### Field Description

| Field Path | Type | Description | Enum |
| --- | --- | --- | --- |
| payload.kpi.totalInventoryValue | Integer | 查詢截止時間的目前庫存總價值 |  |
| payload.kpi.valueChangeRate | Float | 與查詢起始時間相比的庫存總價值變化率 |  |
| payload.kpi.usedPallets | Float | 查詢截止時間的已佔用板數 |  |
| payload.kpi.spaceUtilizationRate | Float | 查詢截止時間的總倉位使用率 |  |
| payload.kpi.riskLotCount | Integer | 查詢截止時間存在風險的批號數 |  |
| payload.kpi.openTaskCount | Integer | 查詢截止時間仍開放中的倉庫任務數 |  |
| payload.kpi.overdueTaskRate | Float | 查詢期間內逾期或目前逾期任務比例 |  |
| payload.valueTrend[].itemCategory | Integer | 料品品項類別，前端負責多國語系轉換 | EItemCategory |
| payload.riskBreakdown[].riskType | String | 風險類型代碼，前端負責多國語系轉換 | TURNOVER_OVER_30_DAYS、SHELF_LIFE_LT_ONE_THIRD、BELOW_SAFETY_STOCK、QUALITY_HOLD、INVENTORY_SHORTAGE |
| payload.taskSla[].taskType | Integer | 任務類型，前端負責多國語系轉換 | EWorkflowTaskType |
| payload.*[].drilldownQuery | String | 前端導向既有 read-only 清單畫面時可使用的 query string |  |

## Detail Endpoints

### GET /api/v2/warehouse/analytics/value-trend

回傳 `payload.valueTrend[]` 與 category summary。此 API 可與 overview 共用查詢邏輯，供使用者放大趨勢圖或切換 period/bucket 時使用。

### GET /api/v2/warehouse/analytics/space-utilization

回傳 `payload.spaceTrend[]`、warehouse summary 與容量風險。第一版僅做 read-only 分析，不調整倉位容量、不建立移倉任務。

### GET /api/v2/warehouse/analytics/risk-breakdown

回傳 `payload.riskBreakdown[]` 與各風險對應的 drill-down query。前端可導向 `WarehouseInventoryLotListScreen`，例如：

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
| 首次進入分析頁 | 呼叫 `GET /api/v2/warehouse/analytics/overview?period=30d&bucket=day` |
| 切換期間 | 重新呼叫 overview 或對應 detail endpoint |
| 點選庫存價值趨勢 | 呼叫 value-trend endpoint 或放大 overview valueTrend |
| 點選倉位使用趨勢 | 呼叫 space-utilization endpoint |
| 點選風險分布 | 導向 `WarehouseInventoryLotListScreen` 對應 risk state |
| 點選任務 SLA | 導向 `WarehouseTaskWorkbenchScreen` 對應 task state |

## Engineer Review Questions

| 項目 | 需確認原因 | 工程師回覆 |
| --- | --- | --- |
| 第一版是否接受 `overview` 聚合 API 加 4 個 detail GET endpoint | 影響前端首次載入效能與後端查詢分工。 | 你建議採取何種方式，能夠達到最佳化？ | 
| `period` 第一版是否只支援 `7d`、`30d`、`90d` | 避免長區間查詢造成即時計算壓力。 | 可以，後續如有需求再新增。|
| `spaceTrend` 是否可先用 `warehouse_pallet_movement` 現有紀錄計算 | 影響倉位趨勢準確度與是否需要新增每日快照表。 | 可以，後續如有需求再新增每日快照表。|
| `taskSla.averageLeadTimeHours` 是否以 workflow_task_event 計算 | 需確認事件資料是否足夠完整。 | 目前設計中包含哪些事件資料？|
| 若 workflow_task_event 尚無資料，task SLA 是否退回使用 workflow_task_state creationTime/updateTime | 避免 API 在第一版資料不足時無法回傳。 | 當 workflow_task_event 無資料時，回傳空陣列即可，還是有其他需要考量的情況？ | 
