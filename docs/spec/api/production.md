# Production API Group

> Source: `restserver/package/restserver/api/v2/production_uri.py`
> Proposal Source: `docs/spec/api-proposal/production_dashboard_proposal.md`
> Flow Source: `docs/spec/api-proposal/production_dashboard_flow_algorithm.md`

## API Summary

| URL | Method | Description | Status | Review Note |
|---|---|---|---|---|
| [/api/v2/production/dashboard](#get-api-v2-production-dashboard) | GET | 查詢生產排程、產能、MES、效率與損耗總覽 | OK | 第一版 read-only；品檢狀態固定回傳 `deferred`。 |
| [/api/v2/production/work-orders/{work_order_no}/detail](#get-api-v2-production-work-orders-work_order_no-detail) | GET | 查詢單一工單的生產、備料、MES 與關聯單據明細 | OK | 提供 Production 工作區右側明細與工單 drill-down。 |

## GET /api/v2/production/dashboard

<a id="get-api-v2-production-dashboard"></a>

### Basic Information

| URL | Method | Description |
|---|---|---|
| /api/v2/production/dashboard | GET | 查詢生產排程、產能、MES、效率與損耗總覽 |

### Request Header

| Header | Description |
|---|---|
| x-auth-token | 存取金鑰。 |
| x-timezone | 時區代碼，例如 `Asia/Taipei`；未提供時使用系統預設值。 |

### Query Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| date | Integer | NO | 查詢基準 UTC timestamp；未提供時使用伺服器目前時間。 |
| period | String | NO | 查詢期間，支援 `7d`、`14d`，預設 `7d`。 |
| production_line_no | String | NO | 產線 no，對應 `production_line.no`。 |
| oneProcess | Integer | NO | 主製程代碼，對應 `work_order.oneProcess`。 |
| secProcess | Integer | NO | 次製程代碼，對應 `work_order.secProcess`。 |
| work_order_no | String | NO | 派工單 no，對應 `work_order.no`。 |
| product_order_no | String | NO | 訂購單 no，對應 `work_order.product_order_no`。 |
| status | String | NO | 工單狀態篩選；enum 顯示文字由前端轉換。 |
| riskType | String | NO | 風險類型篩選；例如 `material_shortage`、`staff_shortage`、`capacity_bottleneck`、`capacity_config_missing`、`capacity_downtime`、`schedule_delay`、`efficiency_loss`、`loss_over_threshold`、`labor_cost_missing`。 |
| keyword | String | NO | 搜尋工單 no、訂單 no、產品 no、產品名稱、產線名稱或批號。 |
| start | Integer | NO | `todayWorkOrders[]` 分頁起始位置，預設 0。 |
| count | Integer | NO | `todayWorkOrders[]` 分頁筆數，預設 50，上限 100。 |

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "serverTimestamp": "Integer",
    "timezone": "String",
    "range": {"period": "String", "startTimestamp": "Integer", "endTimestamp": "Integer"},
    "summary": {
      "scheduledWorkOrderCount": "Integer",
      "todayRunningWorkOrderCount": "Integer",
      "readinessRiskCount": "Integer",
      "averageEfficiencyRate": "Float",
      "averageMaterialLossRate": "Float",
      "averageUnitLaborCost": "Float"
    },
    "total": "Integer",
    "start": "Integer",
    "count": "Integer",
    "scheduleByLine": [{
      "date": "Integer", "productionLineNo": "String", "productionLineName": "String",
      "oneProcess": "Integer", "secProcess": "Integer", "baseCapacityMinutes": "Integer",
      "downtimeMinutes": "Integer", "dailyCapacityMinutes": "Integer", "scheduledMinutes": "Integer",
      "availableMinutes": "Integer", "capacityStatus": "String", "changeoverMinutes": "Integer",
      "changeoverStatus": "String", "utilizationRate": "Float", "bottleneckRank": "Integer",
      "riskLevel": "Integer",
      "slots": [{
        "workOrderNo": "String", "productOrderNo": "String", "productNo": "String",
        "productName": "String", "batchNumber": "String", "plannedStartTimestamp": "Integer",
        "plannedEndTimestamp": "Integer", "plannedQuantity": "Float", "completedQuantity": "Float",
        "unit": "Integer", "status": "String", "materialStatus": "String",
        "staffStatus": "String", "deliveryRisk": "String"
      }]
    }],
    "todayWorkOrders": [{
      "workOrderNo": "String", "productOrderNo": "String", "productNo": "String",
      "productName": "String", "batchNumber": "String", "productionLineNo": "String",
      "productionLineName": "String", "oneProcess": "Integer", "secProcess": "Integer",
      "plannedStartTimestamp": "Integer", "plannedEndTimestamp": "Integer",
      "actualStartTimestamp": "Integer", "actualEndTimestamp": "Integer",
      "plannedQuantity": "Float", "completedQuantity": "Float", "unit": "Integer",
      "progressRate": "Float", "status": "String", "materialStatus": "String",
      "staffStatus": "String", "machineStatus": "String", "qualityStatus": "String",
      "deliveryRisk": "String", "ownerEmployeeNo": "String", "ownerEmployeeName": "String"
    }],
    "readinessSignals": [{
      "workOrderNo": "String", "signalType": "String", "status": "String", "riskLevel": "Integer",
      "ownerDepartment": "Integer", "requiredQuantity": "Float", "availableQuantity": "Float",
      "gapQuantity": "Float", "requiredStaffCount": "Integer", "assignedStaffCount": "Integer",
      "comment": "String"
    }],
    "productionMetrics": [{
      "workOrderNo": "String", "standardMinutes": "Integer", "actualMinutes": "Integer",
      "efficiencyRate": "Float", "standardInputQuantity": "Float", "actualInputQuantity": "Float",
      "outputQuantity": "Float", "reuseQuantity": "Float", "wasteQuantity": "Float",
      "materialLossQuantity": "Float", "materialLossRate": "Float", "laborHours": "Float",
      "laborCost": "Float", "unitLaborCost": "Float", "riskLevel": "Integer"
    }],
    "alerts": [{
      "alertType": "String", "workOrderNo": "String", "productionLineNo": "String",
      "riskLevel": "Integer", "ownerDepartment": "Integer", "comment": "String"
    }]
  }
}
```

### Field Description

| Field Path | Type | Description | Enum |
|---|---|---|---|
| payload.serverTimestamp | Integer | Response 產生時間，UTC timestamp。 |  |
| payload.timezone | String | 本次查詢採用的時區代碼。 |  |
| payload.range.period | String | 實際採用的查詢期間。 | `7d`, `14d` |
| payload.range.startTimestamp | Integer | 查詢起始 UTC timestamp。 |  |
| payload.range.endTimestamp | Integer | 查詢結束 UTC timestamp。 |  |
| payload.summary.scheduledWorkOrderCount | Integer | 查詢期間內符合條件的已排工單數。 |  |
| payload.summary.todayRunningWorkOrderCount | Integer | 查詢基準日中狀態為 `running` 的工單數。 |  |
| payload.summary.readinessRiskCount | Integer | 查詢基準日中備料或人員狀態不是 `ready` 的不重複工單數。 |  |
| payload.summary.averageEfficiencyRate | Float | 有實際工時工單的平均產時效率；百分比取至小數點 2 位。 |  |
| payload.summary.averageMaterialLossRate | Float | 有實際投入量工單的平均原物料損耗率；百分比取至小數點 2 位。 |  |
| payload.summary.averageUnitLaborCost | Float | 有人工成本資料工單的平均單位人工費率。 |  |
| payload.total | Integer | 套用篩選條件後的工單總筆數。 |  |
| payload.start | Integer | 本次 `todayWorkOrders[]` 分頁起始位置。 |  |
| payload.count | Integer | 本次實際回傳的 `todayWorkOrders[]` 筆數。 |  |
| payload.scheduleByLine[].date | Integer | 排程日期的 UTC timestamp。 |  |
| payload.scheduleByLine[].productionLineNo | String | 產線 no，來源為 `work_order.production_line_no`。 |  |
| payload.scheduleByLine[].productionLineName | String | 產線名稱，來源為 `production_line.name`。 |  |
| payload.scheduleByLine[].oneProcess | Integer | 該日該產線工單的主製程代碼。 |  |
| payload.scheduleByLine[].secProcess | Integer | 該日該產線工單的次製程代碼。 |  |
| payload.scheduleByLine[].baseCapacityMinutes | Integer | 依查詢日期以前最新生效設定取得的原始可排工時分鐘數。 |  |
| payload.scheduleByLine[].downtimeMinutes | Integer | 該日已確認停用區間的交集分鐘數，重疊區間只計算一次。 |  |
| payload.scheduleByLine[].dailyCapacityMinutes | Integer | `max(baseCapacityMinutes - downtimeMinutes, 0)`。 |  |
| payload.scheduleByLine[].scheduledMinutes | Integer | 該日已排工單 `work_order.processTime` 加總。 |  |
| payload.scheduleByLine[].availableMinutes | Integer | `max(dailyCapacityMinutes - scheduledMinutes, 0)`。 |  |
| payload.scheduleByLine[].capacityStatus | String | 產能設定狀態。 | `configured`, `missing_config`, `closed`, `disabled` |
| payload.scheduleByLine[].changeoverMinutes | Integer | 第一版未計算換線／清潔時間，固定回傳 0。 |  |
| payload.scheduleByLine[].changeoverStatus | String | 換線／清潔時間的實作狀態。 | `deferred` |
| payload.scheduleByLine[].utilizationRate | Float | `scheduledMinutes / dailyCapacityMinutes * 100`；分母為 0 時回傳 0。 |  |
| payload.scheduleByLine[].bottleneckRank | Integer | 依剩餘可排工時排序的產線瓶頸排名。 |  |
| payload.scheduleByLine[].riskLevel | Integer | 該產線排程產能風險等級。 | 0、1、3 |
| payload.scheduleByLine[].slots[].workOrderNo | String | 派工單 no。 |  |
| payload.scheduleByLine[].slots[].productOrderNo | String | 關聯訂購單 no。 |  |
| payload.scheduleByLine[].slots[].productNo | String | 產品 no。 |  |
| payload.scheduleByLine[].slots[].productName | String | 產品名稱。 |  |
| payload.scheduleByLine[].slots[].batchNumber | String | 產出批號；無產出時為空字串。 |  |
| payload.scheduleByLine[].slots[].plannedStartTimestamp | Integer | 預計開始時間。 |  |
| payload.scheduleByLine[].slots[].plannedEndTimestamp | Integer | 預計結束時間。 |  |
| payload.scheduleByLine[].slots[].plannedQuantity | Float | 預計生產數量。 |  |
| payload.scheduleByLine[].slots[].completedQuantity | Float | 已產出數量。 |  |
| payload.scheduleByLine[].slots[].unit | Integer | 數量單位 code，由前端轉換顯示文字。 |  |
| payload.scheduleByLine[].slots[].status | String | 工單目前狀態。 | `scheduled`, `material_ready`, `running`, `paused`, `pending_inventory`, `completed` |
| payload.scheduleByLine[].slots[].materialStatus | String | 備料狀態。 | `ready`, `partial`, `unknown` |
| payload.scheduleByLine[].slots[].staffStatus | String | 人員 readiness 狀態。 | `ready`, `support_needed`, `shortage`, `unknown` |
| payload.scheduleByLine[].slots[].deliveryRisk | String | 工單交期風險。 | `normal`, `high_risk`, `unknown` |
| payload.todayWorkOrders[].workOrderNo | String | 派工單 no。 |  |
| payload.todayWorkOrders[].productOrderNo | String | 訂購單 no。 |  |
| payload.todayWorkOrders[].productNo | String | 產品 no。 |  |
| payload.todayWorkOrders[].productName | String | 產品名稱。 |  |
| payload.todayWorkOrders[].batchNumber | String | 產出批號；無產出時為空字串。 |  |
| payload.todayWorkOrders[].productionLineNo | String | 產線 no。 |  |
| payload.todayWorkOrders[].productionLineName | String | 產線名稱。 |  |
| payload.todayWorkOrders[].oneProcess | Integer | 主製程代碼。 |  |
| payload.todayWorkOrders[].secProcess | Integer | 次製程代碼。 |  |
| payload.todayWorkOrders[].plannedStartTimestamp | Integer | 預計開始時間。 |  |
| payload.todayWorkOrders[].plannedEndTimestamp | Integer | 預計結束時間。 |  |
| payload.todayWorkOrders[].actualStartTimestamp | Integer | 由 MES input、machine 或 production data 時間推導的實際開始時間；無資料時為 0。 |  |
| payload.todayWorkOrders[].actualEndTimestamp | Integer | 由 MES output 或 machine 時間推導的實際結束時間；無資料時為 0。 |  |
| payload.todayWorkOrders[].plannedQuantity | Float | 預計生產數量。 |  |
| payload.todayWorkOrders[].completedQuantity | Float | 已產出數量。 |  |
| payload.todayWorkOrders[].unit | Integer | 數量單位 code。 |  |
| payload.todayWorkOrders[].progressRate | Float | `completedQuantity / plannedQuantity * 100`；計畫量為 0 時回傳 0。 |  |
| payload.todayWorkOrders[].status | String | 工單狀態；產出達標但尚未確認製造入庫時為 `pending_inventory`。 | `scheduled`, `material_ready`, `running`, `paused`, `pending_inventory`, `completed` |
| payload.todayWorkOrders[].materialStatus | String | 備料狀態。 | `ready`, `partial`, `unknown` |
| payload.todayWorkOrders[].staffStatus | String | 人員 readiness 狀態。 | `ready`, `support_needed`, `shortage`, `unknown` |
| payload.todayWorkOrders[].machineStatus | String | 依最新 MES machine action 判斷的機台狀態。 | `running`, `paused`, `stopped`, `unknown` |
| payload.todayWorkOrders[].qualityStatus | String | 第一版不查詢品檢明細，固定回傳待實作代碼。 | `deferred` |
| payload.todayWorkOrders[].deliveryRisk | String | 依預計結束時間與查詢基準時間判斷的交期風險。 | `normal`, `high_risk`, `unknown` |
| payload.todayWorkOrders[].ownerEmployeeNo | String | 主要負責人員 no；無資料時為空字串。 |  |
| payload.todayWorkOrders[].ownerEmployeeName | String | 主要負責人員名稱；無資料時為空字串。 |  |
| payload.readinessSignals[].workOrderNo | String | 訊號所屬派工單 no。 |  |
| payload.readinessSignals[].signalType | String | readiness 訊號類型。 | `material`, `staff` |
| payload.readinessSignals[].status | String | 訊號狀態。 | `ready`, `attention` |
| payload.readinessSignals[].riskLevel | Integer | 訊號風險等級。 | 0、1 |
| payload.readinessSignals[].ownerDepartment | Integer | 下一步負責部門 code。 |  |
| payload.readinessSignals[].requiredQuantity | Float | 需求數量。 |  |
| payload.readinessSignals[].availableQuantity | Float | 可用數量；資料不足時保守回傳 0。 |  |
| payload.readinessSignals[].gapQuantity | Float | 需求數量扣除可用數量後的缺口數量。 |  |
| payload.readinessSignals[].requiredStaffCount | Integer | 需求人數。 |  |
| payload.readinessSignals[].assignedStaffCount | Integer | 已指派人數。 |  |
| payload.readinessSignals[].comment | String | 資料狀態或 readiness 補充說明。 |  |
| payload.productionMetrics[].workOrderNo | String | 指標所屬派工單 no。 |  |
| payload.productionMetrics[].standardMinutes | Integer | 標準工時分鐘數。 |  |
| payload.productionMetrics[].actualMinutes | Integer | 實際工時分鐘數。 |  |
| payload.productionMetrics[].efficiencyRate | Float | `standardMinutes / actualMinutes * 100`；實際工時為 0 時回傳 0。 |  |
| payload.productionMetrics[].standardInputQuantity | Float | APS 標準投入數量。 |  |
| payload.productionMetrics[].actualInputQuantity | Float | 扣除退料後的實際投入數量。 |  |
| payload.productionMetrics[].outputQuantity | Float | 生產產出數量。 |  |
| payload.productionMetrics[].reuseQuantity | Float | 餘料數量。 |  |
| payload.productionMetrics[].wasteQuantity | Float | 廢料數量。 |  |
| payload.productionMetrics[].materialLossQuantity | Float | 原物料損耗數量。 |  |
| payload.productionMetrics[].materialLossRate | Float | 原物料損耗率。 |  |
| payload.productionMetrics[].laborHours | Float | `production_data_labor.hours` 中 action 為投入的工時加總。 |  |
| payload.productionMetrics[].laborCost | Float | 依 `labor_wage.hourly` 與投入工時計算的人工成本。費率缺漏時該筆以 0 計算並產生 alert。 |  |
| payload.productionMetrics[].unitLaborCost | Float | `laborCost / outputQuantity`；產出量為 0 時回傳 0。 |  |
| payload.productionMetrics[].riskLevel | Integer | 生產指標風險等級。 | 0、1 |
| payload.alerts[].alertType | String | 警示類型 code。 | `material_shortage`, `staff_shortage`, `capacity_bottleneck`, `capacity_config_missing`, `capacity_downtime`, `schedule_delay`, `efficiency_loss`, `loss_over_threshold`, `labor_cost_missing` |
| payload.alerts[].workOrderNo | String | 警示所屬工單 no；產能設定警示可為空字串。 |  |
| payload.alerts[].productionLineNo | String | 警示所屬產線 no。 |  |
| payload.alerts[].riskLevel | Integer | 警示風險等級。 | 1、3 |
| payload.alerts[].ownerDepartment | Integer | 負責處理部門 code。 |  |
| payload.alerts[].comment | String | 後端產生的資料或風險補充說明；非前端多國語系 enum 顯示文字。 |  |

### Processing Flow

1. 建立單一 DB session，解析 `date`、`period`、篩選條件與分頁參數。
2. 於資料庫端查詢期間內的 `work_order`，批次載入產線、APS、MES、人員、人工費率、訂單與庫存入庫關聯資料。
3. 依工單建立今日工單列、排程列、備料／人員 readiness 與狀態；不以缺少資料推測為 ready。
4. 產能以查詢日期以前最新的 `production_line_daily_capacity` 為基準，扣除已確認且與查詢日相交的 `production_line_downtime`，再計算剩餘可排工時與瓶頸。
5. 由 MES input、output、reuse、labor、machine 與 `labor_wage` 計算效率、損耗與人工成本；投入量須扣除退料。
6. 工單產出量達標且製造入庫紀錄存在時回傳 `completed`；否則回傳 `pending_inventory`。
7. 組合 alerts，依 `status`、`riskType` 完成篩選後，再對 `todayWorkOrders[]` 分頁；summary 與排程聚合不可因分頁而漏算。
8. 回傳標準 `{code, message, payload}` envelope；enum code 與資料值由後端回傳，顯示文字由前端處理。

### Database Tables Used

| Table | Purpose |
|---|---|
| work_order | 工單、排程時間、產線、製程、計畫數量、工時與人數。 |
| production_line | 產線名稱與基本產線資料。 |
| production_line_daily_capacity | 產線每日可排工時與生效日版本。 |
| production_line_downtime | 已確認故障、維修或臨時停用時間。 |
| process_labor | 預估投入人員與人員 readiness。 |
| aps_quantity / aps_quantity_item | APS 與工單物料需求。 |
| production_data | 生產資料主表與製造日期。 |
| production_data_input | 投入、領料、退料、批號與數量。 |
| production_data_output | 產出批號、效期與數量。 |
| production_data_reuse | 餘料與廢料資料。 |
| production_data_labor | 實際人員工時與 action。 |
| production_data_machine | 機台 action、速度與溫度。 |
| labor_wage | 依生效日、員工型態與等級取得人工時薪。 |
| product_order | 訂購單與交期風險參考。 |
| inventory_record / batch_number | 製造產出入庫狀態、批號與來源單據。 |

## GET /api/v2/production/work-orders/{work_order_no}/detail

<a id="get-api-v2-production-work-orders-work_order_no-detail"></a>

### Basic Information

| URL | Method | Description |
|---|---|---|
| /api/v2/production/work-orders/{work_order_no}/detail | GET | 查詢單一工單的生產、備料、MES 與關聯單據明細 |

### Request Header

| Header | Description |
|---|---|
| x-auth-token | 存取金鑰。 |
| x-timezone | 時區代碼，例如 `Asia/Taipei`。 |

### Path Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| work_order_no | String | YES | 派工單 no，對應 `work_order.no`。 |

### Query Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| date | Integer | NO | 狀態與時間計算基準 UTC timestamp；未提供時使用伺服器目前時間。 |

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "workOrder": {
      "workOrderNo": "String", "productOrderNo": "String", "apsNo": "String",
      "productNo": "String", "productName": "String", "outputItemNo": "String",
      "outputItemName": "String", "productionLineNo": "String", "productionLineName": "String",
      "oneProcess": "Integer", "secProcess": "Integer", "plannedStartTimestamp": "Integer",
      "plannedEndTimestamp": "Integer", "plannedQuantity": "Float", "unit": "Integer",
      "plannedMinutes": "Integer", "requiredStaffCount": "Integer", "assignedStaffCount": "Integer",
      "status": "String", "comment": "String"
    },
    "materials": [{
      "itemNo": "String", "itemName": "String", "category": "Integer", "itemSubCategory": "Integer",
      "batchNumber": "String", "requiredQuantity": "Float", "issuedQuantity": "Float",
      "returnedQuantity": "Float", "availableQuantity": "Float", "unit": "Integer", "status": "String"
    }],
    "mesEvents": [{
      "eventType": "String", "refNo": "String", "timestamp": "Integer", "itemNo": "String",
      "itemName": "String", "batchNumber": "String", "quantity": "Float", "unit": "Integer",
      "employeeNo": "String", "employeeName": "String", "equipmentNo": "String",
      "equipmentName": "String", "comment": "String"
    }],
    "outputs": [{
      "itemNo": "String", "itemName": "String", "category": "Integer", "itemSubCategory": "Integer",
      "batchNumber": "String", "serialNo": "String", "validDateTimestamp": "Integer",
      "quantity": "Float", "unit": "Integer"
    }],
    "reuseAndWaste": [{
      "itemNo": "String", "itemName": "String", "category": "Integer", "batchNumber": "String",
      "quantity": "Float", "unit": "Integer", "comment": "String"
    }],
    "labor": [{
      "employeeNo": "String", "employeeName": "String", "employeeType": "Integer",
      "stationNo": "String", "stationStage": "Integer", "action": "Integer",
      "startTimestamp": "Integer", "endTimestamp": "Integer", "hours": "Float"
    }],
    "machines": [{
      "equipmentNo": "String", "equipmentName": "String", "timestamp": "Integer",
      "action": "Integer", "speed": "Float", "temperature": "Float"
    }],
    "relatedDocuments": [{
      "documentType": "String", "documentNo": "String", "status": "String", "timestamp": "Integer"
    }]
  }
}
```

### Field Description

| Field Path | Type | Description | Enum |
|---|---|---|---|
| payload.workOrder.workOrderNo | String | 派工單 no，來源為 `work_order.no`。 |  |
| payload.workOrder.productOrderNo | String | 訂購單 no，來源為 `work_order.product_order_no`。 |  |
| payload.workOrder.apsNo | String | APS 排程 no，來源為 `work_order.aps_no`。 |  |
| payload.workOrder.productNo | String | 產品 no，來源為工單欄位。 |  |
| payload.workOrder.productName | String | 產品名稱，來源為工單欄位。 |  |
| payload.workOrder.outputItemNo | String | 預計產出料品 no。 |  |
| payload.workOrder.outputItemName | String | 預計產出料品名稱。 |  |
| payload.workOrder.productionLineNo | String | 產線 no。 |  |
| payload.workOrder.productionLineName | String | 產線名稱。 |  |
| payload.workOrder.oneProcess | Integer | 主製程代碼。 |  |
| payload.workOrder.secProcess | Integer | 次製程代碼。 |  |
| payload.workOrder.plannedStartTimestamp | Integer | 預計開始時間。 |  |
| payload.workOrder.plannedEndTimestamp | Integer | 預計結束時間。 |  |
| payload.workOrder.plannedQuantity | Float | 預計生產數量。 |  |
| payload.workOrder.unit | Integer | 數量單位 code。 |  |
| payload.workOrder.plannedMinutes | Integer | 預估投入工時分鐘數。 |  |
| payload.workOrder.requiredStaffCount | Integer | 預估需求人數。 |  |
| payload.workOrder.assignedStaffCount | Integer | 已指派／已投入人數。 |  |
| payload.workOrder.status | String | 工單目前狀態。 | `scheduled`, `material_ready`, `running`, `paused`, `pending_inventory`, `completed` |
| payload.workOrder.comment | String | 工單備註。 |  |
| payload.materials[].itemNo | String | 物料 no。 |  |
| payload.materials[].itemName | String | 物料名稱。 |  |
| payload.materials[].category | Integer | 物料類別 code。 |  |
| payload.materials[].itemSubCategory | Integer | 物料子類別 code。 |  |
| payload.materials[].batchNumber | String | 實際領料批號；無資料時為空字串。 |  |
| payload.materials[].requiredQuantity | Float | APS／工單需求數量。 |  |
| payload.materials[].issuedQuantity | Float | 領料數量。 |  |
| payload.materials[].returnedQuantity | Float | 退料數量。 |  |
| payload.materials[].availableQuantity | Float | Warehouse 可用量；第一版資料不足時保守回傳 0，不推測為可用。 |  |
| payload.materials[].unit | Integer | 物料數量單位 code。 |  |
| payload.materials[].status | String | 物料準備狀態。 | `ready`, `unknown` |
| payload.mesEvents[].eventType | String | MES 事件類型。 | `input`, `output`, `labor`, `machine` |
| payload.mesEvents[].refNo | String | 事件關聯單號；無資料時為空字串。 |  |
| payload.mesEvents[].timestamp | Integer | 事件時間 UTC timestamp。 |  |
| payload.mesEvents[].itemNo | String | 事件料品 no。 |  |
| payload.mesEvents[].itemName | String | 事件料品名稱。 |  |
| payload.mesEvents[].batchNumber | String | 事件批號。 |  |
| payload.mesEvents[].quantity | Float | 事件數量。 |  |
| payload.mesEvents[].unit | Integer | 事件數量單位 code。 |  |
| payload.mesEvents[].employeeNo | String | 事件人員 no。 |  |
| payload.mesEvents[].employeeName | String | 事件人員名稱。 |  |
| payload.mesEvents[].equipmentNo | String | 事件機台 no。 |  |
| payload.mesEvents[].equipmentName | String | 事件機台名稱。 |  |
| payload.mesEvents[].comment | String | 事件備註。 |  |
| payload.outputs[].itemNo | String | 產出料品 no。 |  |
| payload.outputs[].itemName | String | 產出料品名稱。 |  |
| payload.outputs[].category | Integer | 產出料品類別 code。 |  |
| payload.outputs[].itemSubCategory | Integer | 產出料品子類別 code。 |  |
| payload.outputs[].batchNumber | String | 產出批號。 |  |
| payload.outputs[].serialNo | String | 產出序號。 |  |
| payload.outputs[].validDateTimestamp | Integer | 產出效期 UTC timestamp。 |  |
| payload.outputs[].quantity | Float | 產出數量。 |  |
| payload.outputs[].unit | Integer | 產出數量單位 code。 |  |
| payload.reuseAndWaste[].itemNo | String | 餘料／廢料料品 no。 |  |
| payload.reuseAndWaste[].itemName | String | 餘料／廢料料品名稱。 |  |
| payload.reuseAndWaste[].batchNumber | String | 餘料／廢料批號。 |  |
| payload.reuseAndWaste[].category | Integer | 料品類別 code。 |  |
| payload.reuseAndWaste[].quantity | Float | 餘料或廢料數量。 |  |
| payload.reuseAndWaste[].unit | Integer | 數量單位 code。 |  |
| payload.reuseAndWaste[].comment | String | 餘料／廢料備註。 |  |
| payload.labor[].employeeNo | String | 人員 no。 |  |
| payload.labor[].employeeName | String | 人員名稱。 |  |
| payload.labor[].employeeType | Integer | 人員型態 code。 |  |
| payload.labor[].stationStage | Integer | 站點階段 code。 |  |
| payload.labor[].action | Integer | 工作 action code。 |  |
| payload.labor[].stationNo | String | 工作站 no。 |  |
| payload.labor[].startTimestamp | Integer | 人員事件開始時間。 |  |
| payload.labor[].endTimestamp | Integer | 人員事件結束時間。 |  |
| payload.labor[].hours | Float | 人員工時。 |  |
| payload.machines[].equipmentNo | String | 機台 no。 |  |
| payload.machines[].equipmentName | String | 機台名稱。 |  |
| payload.machines[].timestamp | Integer | 機台事件時間。 |  |
| payload.machines[].action | Integer | 機台 action code。 | 啟動(1)、暫停(2)、停止(3) |
| payload.machines[].speed | Float | 機台速度。 |  |
| payload.machines[].temperature | Float | 機台溫度。 |  |
| payload.relatedDocuments[].documentType | String | 關聯單據類型。 | `work_order`, `product_order`, `production_data`, `process_order` |
| payload.relatedDocuments[].documentNo | String | 關聯單據 no。 |  |
| payload.relatedDocuments[].status | String | 關聯狀態。 | `scheduled`, `linked` |
| payload.relatedDocuments[].timestamp | Integer | 關聯單據時間；無資料時為 0。 |  |

### Processing Flow

1. 以 `work_order.no` 查詢單一工單；不存在時回傳既有標準錯誤 envelope。
2. 使用單一 DB session 批次載入 APS 物料、MES input/output/reuse/labor/machine、產線、人員、人工費率、入庫與關聯單據。
3. 組合工單基本資料、備料、MES 事件、產出、餘廢料、人員、機台與關聯單據。
4. MES output 事件時間使用 `production_data_output.time`；效期另由 `outputs[].validDateTimestamp` 回傳。
5. Enum 回傳 code，前端負責多國語系顯示文字；數量／工時取至小數點 2 位，金額取整數。

### Database Tables Used

| Table | Purpose |
|---|---|
| work_order | 工單基本資料、排程、產品、產線與計畫數量。 |
| product_order | 關聯訂購單。 |
| production_line | 產線名稱。 |
| aps_quantity_item | APS 物料需求。 |
| production_data | 生產資料主表。 |
| production_data_input | 投入、領料與退料。 |
| production_data_output | 產出、批號與效期。 |
| production_data_reuse | 餘料與廢料。 |
| production_data_labor | 人員與工時。 |
| production_data_machine | 機台事件。 |
| labor_wage | 人工費率。 |
| process_order | 領料、退料、餘料、廢料與產製流程單據。 |
| inventory_record / batch_number | 產出入庫與批號關聯。 |

## Frontend Interaction Notes

| UI Action | API Behavior |
|---|---|
| 進入 Production 頁面 | 呼叫 `GET /api/v2/production/dashboard?period=7d`。 |
| 切換日期或產線 | 由前端保存篩選值並重新組合 query string。 |
| 檢視排程與產能 | 使用 `payload.scheduleByLine[]`。 |
| 檢視今日 MES | 使用 `payload.todayWorkOrders[]`、`readinessSignals[]` 與 `productionMetrics[]`。 |
| 點選單一工單 | 呼叫 `GET /api/v2/production/work-orders/{work_order_no}/detail` 顯示明細。 |
| 顯示 enum | 前端將 code 轉換為多國語系文字；後端不回傳 UI fallback 字串。 |
