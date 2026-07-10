
# 工程師提問

pagination
1. API 回傳的欄位資料，是否有額外預留未來才會使用的欄位？請僅設計目前畫面所需的欄位即可
2. 請重新檢視並補全所有回傳欄位的描述，確保文件完整
2. 針對 `/api/v2/production/dashboard` 
    - 請確認 payload.pagination.total、payload.pagination.start、payload.pagination.count 的資料階層。為了統一規格，建議改為 payload.total、payload.start、payload.count
  - scheduleByLine[].dailyCapacityMinutes

# Production Dashboard API Proposal

> Status: Proposal / Pending Engineer Review
> Target UI Preview: `docs/spec/api-proposal/production_dashboard_static_preview.html`
> Flow / Algorithm: `docs/spec/api-proposal/production_dashboard_flow_algorithm.md`
> Related V1 Rule: 第一版前端畫面優先實作 phase 為 core 的畫面；依整體 read-only integration 順序，Warehouse core 與 Orders core 後的下一個 core 畫面為 `ProductionWorkspaceScreen`。

## Screen Intent

`ProductionWorkspaceScreen` 是第一版 core 畫面，主要回答管理者與生管主管在生產面最關心的問題：

1. 以日期與產線視角，掌握整個廠區預排工單與剩餘產能。
2. 檢視最近一週已排工單所需料品與人員是否足夠，是否能如期生產。
3. 掌握今日工單 MES 現況、製程進度、機台、人員、投入與產出。
4. 分析今日工單的產時效率、原物料損耗率、單品人工費率。
5. 納入品檢狀態，呈現是否影響入庫、出貨或交期。

此 API 提案只處理 read-only 查詢，不建立工單、不調整排程、不寫入 MES 資料、不建立品檢單，也不產生入庫或出貨單。前端可先以此資料取代 Production mock data；待工程師確認資料來源與演算法後，再整合至正式 API 文件並開始後端實作。

## API Summary

| URL | Method | Description | Status | Review Note |
| --- | --- | --- | --- | --- |
| `/api/v2/production/dashboard` | GET | 查詢生產排程、產能、MES、效率損耗與品檢總覽 | Proposal / Pending Engineer Review | 首屏聚合 API，回傳一週排程、今日工單、風險、效率損耗與品質訊號。 |
| `/api/v2/production/work-orders/{work_order_no}/detail` | GET | 查詢單一工單的生產、備料、MES、品檢與關聯單據明細 | Proposal / Pending Engineer Review | 供右側明細、工單 drilldown 或後續 Production detail tab 使用。 |

## Shared Query Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| date | Integer | NO | 查詢基準日 UTC timestamp；未提供時使用伺服器目前時間。 |
| period | String | NO | 查詢期間代碼；第一版建議支援 `7d`、`14d`，預設 `7d`。 |
| production_line_no | String | NO | 產線 no，對應 `production_line.no`。 |
| oneProcess | Integer | NO | 主製程代碼，對應 `work_order.oneProcess` / `production_data.oneProcess`。 |
| secProcess | Integer | NO | 次製程代碼，對應 `work_order.secProcess` / `production_data.secProcess`。 |
| work_order_no | String | NO | 派工單 no，對應 `work_order.no`。 |
| product_order_no | String | NO | 訂購單 no，對應 `work_order.product_order_no` / `production_data.product_order_no`。 |
| status | String | NO | 工單狀態代碼；enum 顯示文字由前端多國語言處理。 |
| riskType | String | NO | 風險類型，允許 `material_shortage`、`staff_shortage`、`capacity_bottleneck`、`quality_hold`、`schedule_delay`、`efficiency_loss`、`loss_over_threshold`。 |
| keyword | String | NO | 關鍵字；第一版可搜尋工單 no、訂單 no、產品 no、產品名稱、產線名稱、批號。 |
| start | Integer | NO | 分頁起始位置，預設 0。 |
| count | Integer | NO | 分頁筆數，預設 50，第一版上限 100。 |

## Numeric Format Rules

| Numeric Meaning | Format |
| --- | --- |
| 單價 | 四捨五入取至小數點第 4 位 |
| 重量或數量 | 四捨五入取至小數點第 2 位 |
| 金額 | 四捨五入取整數 |
| 比率 | 四捨五入取至小數點第 2 位 |
| 工時 | 四捨五入取至小數點第 2 位 |

## GET /api/v2/production/dashboard

### Basic Information

| URL | Method | Description |
| --- | --- | --- |
| `/api/v2/production/dashboard` | GET | 查詢生產排程、產能、MES、效率損耗與品檢總覽 |

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
      "startTimestamp": "Integer",
      "endTimestamp": "Integer"
    },
    "summary": {
      "scheduledWorkOrderCount": "Integer",
      "todayRunningWorkOrderCount": "Integer",
      "readinessRiskCount": "Integer",
      "qualityRiskCount": "Integer",
      "averageEfficiencyRate": "Float",
      "averageMaterialLossRate": "Float",
      "averageUnitLaborCost": "Float"
    },
    "scheduleByLine": [
      {
        "date": "Integer",
        "productionLineNo": "String",
        "productionLineName": "String",
        "oneProcess": "Integer",
        "secProcess": "Integer",
        "dailyCapacityMinutes": "Integer",
        "scheduledMinutes": "Integer",
        "availableMinutes": "Integer",
        "changeoverMinutes": "Integer",
        "utilizationRate": "Float",
        "bottleneckRank": "Integer",
        "riskLevel": "Integer",
        "slots": [
          {
            "workOrderNo": "String",
            "productOrderNo": "String",
            "productNo": "String",
            "productName": "String",
            "batchNumber": "String",
            "plannedStartTimestamp": "Integer",
            "plannedEndTimestamp": "Integer",
            "plannedQuantity": "Float",
            "completedQuantity": "Float",
            "unit": "Integer",
            "status": "String",
            "materialStatus": "String",
            "staffStatus": "String",
            "qualityStatus": "String",
            "deliveryRisk": "String"
          }
        ]
      }
    ],
    "todayWorkOrders": [
      {
        "workOrderNo": "String",
        "productOrderNo": "String",
        "productNo": "String",
        "productName": "String",
        "batchNumber": "String",
        "productionLineNo": "String",
        "productionLineName": "String",
        "oneProcess": "Integer",
        "secProcess": "Integer",
        "plannedStartTimestamp": "Integer",
        "plannedEndTimestamp": "Integer",
        "actualStartTimestamp": "Integer",
        "actualEndTimestamp": "Integer",
        "plannedQuantity": "Float",
        "completedQuantity": "Float",
        "unit": "Integer",
        "progressRate": "Float",
        "status": "String",
        "materialStatus": "String",
        "staffStatus": "String",
        "machineStatus": "String",
        "qualityStatus": "String",
        "qualityBlocksInventory": "Boolean",
        "qualityBlocksShipment": "Boolean",
        "deliveryRisk": "String",
        "ownerEmployeeNo": "String",
        "ownerEmployeeName": "String"
      }
    ],
    "readinessSignals": [
      {
        "workOrderNo": "String",
        "signalType": "String",
        "status": "String",
        "riskLevel": "Integer",
        "ownerDepartment": "Integer",
        "requiredQuantity": "Float",
        "availableQuantity": "Float",
        "gapQuantity": "Float",
        "requiredStaffCount": "Integer",
        "assignedStaffCount": "Integer",
        "comment": "String"
      }
    ],
    "productionMetrics": [
      {
        "workOrderNo": "String",
        "standardMinutes": "Integer",
        "actualMinutes": "Integer",
        "efficiencyRate": "Float",
        "standardInputQuantity": "Float",
        "actualInputQuantity": "Float",
        "outputQuantity": "Float",
        "reuseQuantity": "Float",
        "wasteQuantity": "Float",
        "materialLossQuantity": "Float",
        "materialLossRate": "Float",
        "laborHours": "Float",
        "laborCost": "Float",
        "unitLaborCost": "Float",
        "qualityDefectCount": "Integer",
        "qualityPendingCount": "Integer",
        "qualityDefectRate": "Float",
        "riskLevel": "Integer"
      }
    ],
    "qualitySignals": [
      {
        "workOrderNo": "String",
        "inspectionNo": "String",
        "qualityStatus": "String",
        "sampleCount": "Integer",
        "defectCount": "Integer",
        "pendingCount": "Integer",
        "defectRate": "Float",
        "blocksInventory": "Boolean",
        "blocksShipment": "Boolean",
        "comment": "String"
      }
    ],
    "alerts": [
      {
        "alertType": "String",
        "workOrderNo": "String",
        "productionLineNo": "String",
        "riskLevel": "Integer",
        "ownerDepartment": "Integer",
        "comment": "String"
      }
    ],
    "pagination": {
      "start": "Integer",
      "count": "Integer",
      "total": "Integer"
    }
  }
}
```

### Field Description

| Field Path | Type | Description | Enum |
| --- | --- | --- | --- |
| payload.serverTimestamp | Integer | API 產生資料時的伺服器 UTC timestamp。 |  |
| payload.timezone | String | 回傳資料使用的時區字串；預設可依 `x-timezone` 或伺服器設定。 |  |
| payload.range.period | String | 查詢期間代碼。 | `7d`、`14d` |
| payload.summary.scheduledWorkOrderCount | Integer | 查詢期間內已排定的派工單數量，來源為 `work_order`。 |  |
| payload.summary.todayRunningWorkOrderCount | Integer | 查詢基準日生產中或有 MES 生產數據的工單數量。 |  |
| payload.summary.readinessRiskCount | Integer | 備料、人員或產能任一 readiness signal 非 ready 的工單去重數。 |  |
| payload.summary.qualityRiskCount | Integer | 品檢待判、hold、異常或阻擋入庫/出貨的工單去重數。 |  |
| payload.summary.averageEfficiencyRate | Float | 查詢期間內有實際工時資料工單的平均產時效率。 |  |
| payload.summary.averageMaterialLossRate | Float | 查詢期間內有投入/產出資料工單的平均原物料損耗率。 |  |
| payload.summary.averageUnitLaborCost | Float | 查詢期間內有人工成本資料工單的平均單品人工費率。 |  |
| payload.scheduleByLine[].date | Integer | 排程日期 UTC timestamp。 |  |
| payload.scheduleByLine[].productionLineNo | String | 產線 no，來源為 `production_line.no` 或 `work_order.production_line_no`。 |  |
| payload.scheduleByLine[].productionLineName | String | 產線名稱，來源為 `production_line.name`，缺漏時回傳空字串。 |  |
| payload.scheduleByLine[].oneProcess | Integer | 主製程代碼，來源為 `work_order.oneProcess`。 | 前備(1)、加工(2)、包裝(3)、其他(0) |
| payload.scheduleByLine[].secProcess | Integer | 次製程代碼，來源為 `work_order.secProcess`。 | 依主製程對應 DB 文件定義 |
| payload.scheduleByLine[].dailyCapacityMinutes | Integer | 該產線當日可用產能分鐘數；第一版若缺少班表/產能設定，暫由已確認產能資料表或 0 回傳，不自行推測。 |  |
| payload.scheduleByLine[].scheduledMinutes | Integer | 查詢日該產線已排工單 `work_order.processTime` 加總。 |  |
| payload.scheduleByLine[].availableMinutes | Integer | `dailyCapacityMinutes - scheduledMinutes - changeoverMinutes`，小於 0 時回傳 0。 |  |
| payload.scheduleByLine[].changeoverMinutes | Integer | 換線/清潔時間；若無穩定來源，第一版回傳 0 並由工程師確認後續規則。 |  |
| payload.scheduleByLine[].utilizationRate | Float | 產能利用率，`scheduledMinutes / dailyCapacityMinutes * 100`。 |  |
| payload.scheduleByLine[].bottleneckRank | Integer | 依 `availableMinutes` 由小到大排序的瓶頸名次；無產能基準時回傳 0。 |  |
| payload.scheduleByLine[].riskLevel | Integer | 該產線當日最高風險等級。 | 0 normal、1 notice、2 attention、3 high_risk |
| payload.scheduleByLine[].slots[] | Array | 該產線當日排程的工單時段。 |  |
| payload.todayWorkOrders[].workOrderNo | String | 派工單 no，來源為 `work_order.no`。 |  |
| payload.todayWorkOrders[].productOrderNo | String | 訂購單 no，來源為 `work_order.product_order_no`。 |  |
| payload.todayWorkOrders[].productNo | String | 產品 no，來源為 `work_order.product_no` 或 `production_data.product_no`。 |  |
| payload.todayWorkOrders[].productName | String | 產品名稱，來源為 `work_order.product_name` 或 `production_data.product_name`。 |  |
| payload.todayWorkOrders[].batchNumber | String | 產出批號，優先來源為 `production_data_output.batch_number`；無產出時回傳空字串。 |  |
| payload.todayWorkOrders[].productionLineNo | String | 產線 no。 |  |
| payload.todayWorkOrders[].productionLineName | String | 產線名稱。 |  |
| payload.todayWorkOrders[].plannedStartTimestamp | Integer | 預計開始時間，來源為 `work_order.startTime`。 |  |
| payload.todayWorkOrders[].plannedEndTimestamp | Integer | 預計結束時間，來源為 `work_order.endTime`。 |  |
| payload.todayWorkOrders[].actualStartTimestamp | Integer | 實際開始時間，優先取最早 `production_data_input.time`、`production_data_machine.time` 或 `production_data.date`。 |  |
| payload.todayWorkOrders[].actualEndTimestamp | Integer | 實際結束時間，優先取最後 `production_data_output.time` 或最後機台停止時間；無完成資料回傳 0。 |  |
| payload.todayWorkOrders[].plannedQuantity | Float | 預估生產數量，來源為 `work_order.processCount`。 |  |
| payload.todayWorkOrders[].completedQuantity | Float | 已產出數量，來源為 `production_data_output.count` 加總。 |  |
| payload.todayWorkOrders[].unit | Integer | 單位代碼，來源為 `work_order.processUnit` 或 `production_data_output.unit`。 |  |
| payload.todayWorkOrders[].progressRate | Float | `completedQuantity / plannedQuantity * 100`，無計畫數量時回傳 0。 |  |
| payload.todayWorkOrders[].status | String | 工單狀態代碼，由工單、MES 投入/產出、品檢與完成資料彙總。 | scheduled、material_ready、running、paused、quality_check、completed、blocked、unknown |
| payload.todayWorkOrders[].materialStatus | String | 備料狀態代碼，由 BOM/APS 所需投入與 Warehouse 可用量或 `production_data_input` 領料資料判斷。 | ready、partial、shortage、unknown |
| payload.todayWorkOrders[].staffStatus | String | 人員狀態代碼，由 `work_order.laborCount` 與 `laborList` / `production_data_labor` 判斷。 | ready、support_needed、shortage、unknown |
| payload.todayWorkOrders[].machineStatus | String | 機台狀態代碼，由 `production_data_machine.action` 最新狀態判斷。 | running、paused、stopped、unknown |
| payload.todayWorkOrders[].qualityStatus | String | 品檢狀態代碼；第一版若無 Quality API，僅可由 `warehouse_quality_hold` 或已存在 hold 訊號判斷，無資料回傳 `unknown`。 | not_started、in_progress、pending_decision、released、hold、abnormal、unknown |
| payload.todayWorkOrders[].qualityBlocksInventory | Boolean | 品檢是否阻擋入庫。 |  |
| payload.todayWorkOrders[].qualityBlocksShipment | Boolean | 品檢是否阻擋出貨。 |  |
| payload.todayWorkOrders[].deliveryRisk | String | 工單是否可能影響交期；由排程時間、完成率、readiness 與品檢阻擋彙總。 | normal、attention、high_risk、unknown |
| payload.todayWorkOrders[].ownerEmployeeNo | String | 工單負責人員 no，優先來源為 `work_order.creator_no` 或主管確認的 owner 欄位。 |  |
| payload.todayWorkOrders[].ownerEmployeeName | String | 工單負責人員名稱；無資料回傳空字串。 |  |
| payload.readinessSignals[].signalType | String | readiness 訊號類型。 | material、staff、capacity、machine、quality |
| payload.readinessSignals[].status | String | readiness 狀態。 | ready、attention、blocked、unknown |
| payload.readinessSignals[].riskLevel | Integer | readiness 風險等級。 | 0 normal、1 notice、2 attention、3 high_risk |
| payload.readinessSignals[].ownerDepartment | Integer | 下一步負責部門 enum；由 workflow next owner rule 或固定對應規則彙總。 |  |
| payload.readinessSignals[].comment | String | readiness 摘要；僅描述可由資料支持的缺口或阻擋原因。 |  |
| payload.productionMetrics[].standardMinutes | Integer | 標準/預估投產分鐘數，來源為 `work_order.processTime`。 |  |
| payload.productionMetrics[].actualMinutes | Integer | 實際投產分鐘數，由 `production_data_labor.hours` 或 MES 起訖時間彙總。 |  |
| payload.productionMetrics[].efficiencyRate | Float | 產時效率，`standardMinutes / actualMinutes * 100`；無實際分鐘數回傳 0。 |  |
| payload.productionMetrics[].standardInputQuantity | Float | 標準投入量；第一版優先由 `aps_quantity_item` 或 BOM/APS 資料提供，缺漏時回傳 0。 |  |
| payload.productionMetrics[].actualInputQuantity | Float | 實際投入量，來源為 `production_data_input.action = 領料(1)` 的 `count` 加總。 |  |
| payload.productionMetrics[].outputQuantity | Float | 實際產出量，來源為 `production_data_output.action = 產製(1)` 的 `count` 加總。 |  |
| payload.productionMetrics[].reuseQuantity | Float | 餘料數量，來源為 `production_data_reuse.category = 餘料(1)` 的 `count` 加總。 |  |
| payload.productionMetrics[].wasteQuantity | Float | 廢料數量，來源為 `production_data_reuse.category = 廢料(2)` 的 `count` 加總。 |  |
| payload.productionMetrics[].materialLossQuantity | Float | 原物料損耗量；優先使用 `production_data.materialLoss`，缺漏時由投入、產出、餘料、廢料補算。 |  |
| payload.productionMetrics[].materialLossRate | Float | `materialLossQuantity / actualInputQuantity * 100`；無實際投入量回傳 0。 |  |
| payload.productionMetrics[].laborHours | Float | 人工時數，來源為 `production_data_labor.hours` 加總。 |  |
| payload.productionMetrics[].laborCost | Float | 人工成本；若無人員費率來源，第一版回傳 0 並標示需工程師確認。 |  |
| payload.productionMetrics[].unitLaborCost | Float | `laborCost / outputQuantity`；無人工成本或產出量回傳 0。 |  |
| payload.qualitySignals[].inspectionNo | String | 品檢單號；第一版若僅有倉庫品檢保留，來源為 `warehouse_quality_hold.inspection_no`。 |  |
| payload.qualitySignals[].qualityStatus | String | 品質狀態代碼。 | not_started、in_progress、pending_decision、released、hold、abnormal、unknown |
| payload.qualitySignals[].blocksInventory | Boolean | 是否阻擋入庫。 |  |
| payload.qualitySignals[].blocksShipment | Boolean | 是否阻擋出貨。 |  |
| payload.alerts[].alertType | String | 異常或提醒類型。 | material_shortage、staff_shortage、capacity_bottleneck、quality_hold、schedule_delay、efficiency_loss、loss_over_threshold |
| payload.alerts[].comment | String | 風險摘要。 |  |

## GET /api/v2/production/work-orders/{work_order_no}/detail

### Basic Information

| URL | Method | Description |
| --- | --- | --- |
| `/api/v2/production/work-orders/{work_order_no}/detail` | GET | 查詢單一工單的生產、備料、MES、品檢與關聯單據明細 |

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "workOrder": {
      "workOrderNo": "String",
      "productOrderNo": "String",
      "apsNo": "String",
      "productNo": "String",
      "productName": "String",
      "outputItemNo": "String",
      "outputItemName": "String",
      "productionLineNo": "String",
      "productionLineName": "String",
      "oneProcess": "Integer",
      "secProcess": "Integer",
      "plannedStartTimestamp": "Integer",
      "plannedEndTimestamp": "Integer",
      "plannedQuantity": "Float",
      "unit": "Integer",
      "plannedMinutes": "Integer",
      "requiredStaffCount": "Integer",
      "assignedStaffCount": "Integer",
      "status": "String",
      "comment": "String"
    },
    "materials": [
      {
        "itemNo": "String",
        "itemName": "String",
        "category": "Integer",
        "itemSubCategory": "Integer",
        "batchNumber": "String",
        "requiredQuantity": "Float",
        "issuedQuantity": "Float",
        "returnedQuantity": "Float",
        "availableQuantity": "Float",
        "unit": "Integer",
        "status": "String"
      }
    ],
    "mesEvents": [
      {
        "eventType": "String",
        "refNo": "String",
        "timestamp": "Integer",
        "itemNo": "String",
        "itemName": "String",
        "batchNumber": "String",
        "quantity": "Float",
        "unit": "Integer",
        "employeeNo": "String",
        "employeeName": "String",
        "equipmentNo": "String",
        "equipmentName": "String",
        "comment": "String"
      }
    ],
    "outputs": [
      {
        "itemNo": "String",
        "itemName": "String",
        "category": "Integer",
        "itemSubCategory": "Integer",
        "batchNumber": "String",
        "serialNo": "String",
        "validDateTimestamp": "Integer",
        "quantity": "Float",
        "unit": "Integer"
      }
    ],
    "reuseAndWaste": [
      {
        "itemNo": "String",
        "itemName": "String",
        "category": "Integer",
        "batchNumber": "String",
        "quantity": "Float",
        "unit": "Integer",
        "comment": "String"
      }
    ],
    "labor": [
      {
        "employeeNo": "String",
        "employeeName": "String",
        "employeeType": "Integer",
        "stationNo": "String",
        "stationStage": "Integer",
        "action": "Integer",
        "startTimestamp": "Integer",
        "endTimestamp": "Integer",
        "hours": "Float"
      }
    ],
    "machines": [
      {
        "equipmentNo": "String",
        "equipmentName": "String",
        "timestamp": "Integer",
        "action": "Integer",
        "speed": "Float",
        "temperature": "Float"
      }
    ],
    "quality": {
      "qualityStatus": "String",
      "inspectionNo": "String",
      "sampleCount": "Integer",
      "defectCount": "Integer",
      "pendingCount": "Integer",
      "defectRate": "Float",
      "blocksInventory": "Boolean",
      "blocksShipment": "Boolean",
      "comment": "String"
    },
    "relatedDocuments": [
      {
        "documentType": "String",
        "documentNo": "String",
        "status": "String",
        "timestamp": "Integer"
      }
    ]
  }
}
```

### Field Description

| Field Path | Type | Description | Enum |
| --- | --- | --- | --- |
| payload.workOrder.workOrderNo | String | 派工單 no，來源為 `work_order.no`。 |  |
| payload.workOrder.productOrderNo | String | 訂購單 no，來源為 `work_order.product_order_no`。 |  |
| payload.workOrder.apsNo | String | APS 排程 no，來源為 `work_order.aps_no`。 |  |
| payload.workOrder.outputItemNo | String | 預計產出的料品品項 no，來源為 `work_order.output_item_no`。 |  |
| payload.workOrder.productionLineNo | String | 生產線 no，來源為 `work_order.production_line_no`。 |  |
| payload.workOrder.plannedMinutes | Integer | 預估投產時數分鐘，來源為 `work_order.processTime`。 |  |
| payload.workOrder.requiredStaffCount | Integer | 預估投產人數，來源為 `work_order.laborCount`。 |  |
| payload.workOrder.assignedStaffCount | Integer | 已指派或已有實際人員數；優先由 `laborList` 或 `production_data_labor.employee_no` 去重。 |  |
| payload.materials[] | Array | 工單所需與已領用料品明細；所需量優先來源 `aps_quantity_item`，已領/退料來源 `production_data_input`。 |  |
| payload.mesEvents[] | Array | 生產現場事件，彙整投入、產出、餘廢料、人員、機台資料。 | input、output、reuse、waste、labor、machine |
| payload.outputs[] | Array | 工單產出明細，來源為 `production_data_output`。 |  |
| payload.reuseAndWaste[] | Array | 餘料與廢料明細，來源為 `production_data_reuse`。 | 餘料(1)、廢料(2)、其他(0) |
| payload.labor[] | Array | 人員投入明細，來源為 `production_data_labor`。 |  |
| payload.machines[] | Array | 機台狀態明細，來源為 `production_data_machine`。 | 啟動(1)、暫停(2)、停止(3) |
| payload.quality | Object | 品檢摘要；第一版資料來源需工程師確認，無穩定資料時狀態回傳 `unknown`。 |  |
| payload.relatedDocuments[] | Array | 關聯單據，至少包含訂單、APS、工單、生產數據、品檢或入庫相關單號。 |  |

## Frontend Interaction Notes

| UI Action | API Behavior |
| --- | --- |
| 進入 Production 頁面 | 呼叫 `GET /api/v2/production/dashboard?period=7d`，前端 normalization 成既有 Production page shape。 |
| 切換「週排程與產能」tab | 使用 `scheduleByLine[]`，依日期、產線、製程群組呈現排程與瓶頸。 |
| 切換「MES 工單現況」tab | 使用 `todayWorkOrders[]`、`readinessSignals[]`、`qualitySignals[]`。 |
| 切換「效率損耗品質」tab | 使用 `productionMetrics[]` 與 `qualitySignals[]`。 |
| 點選單一工單 | 呼叫 `GET /api/v2/production/work-orders/{work_order_no}/detail` 顯示右側明細。 |

## Database Tables Used

| Table | Purpose |
| --- | --- |
| work_order | 派工單、排程日期、產線、製程、預估數量、預估工時、預估人數。 |
| production_line | 產線名稱、製程、廠區資訊。 |
| aps_quantity / aps_quantity_item | APS 與預估投入料品需求；第一版用於備料需求參考，資料不足時不推測。 |
| production_data | 生產數據主表、製造日期、產線、產品與 materialLoss。 |
| production_data_input | 投入物、領料、退料、批號、投入數量。 |
| production_data_output | 產出物、產出批號、有效期與產出數量。 |
| production_data_reuse | 餘料與廢料數據。 |
| production_data_labor | 人員工時、站點、上下班/休息/清潔事件。 |
| production_data_machine | 機台啟動、暫停、停止、速度與溫度。 |
| product_order | 訂購單與客戶交期參考，用於 deliveryRisk。 |
| warehouse_quality_hold | 第一版可用的品檢保留/hold 參考；正式 Quality 模組建立後需再調整。 |
| inventory_record / batch_number | 料品批號、庫存與來源單據參考；若已可共用 Warehouse inventory snapshot，應優先重用。 |

## Engineer Review Questions

| 項目 | 需確認原因 | 工程師回覆 | Codex 建議 |
| --- | --- | --- | --- |
| 是否同意下一個 core API 提案為 `ProductionWorkspaceScreen` | 符合 Warehouse → Orders → Production → Quality 的第一版 core 順序。 | 採用 | 建議採用。 |
| `/api/v2/production/dashboard` 是否可作 Production 聚合 endpoint | 需要與既有 workorder / work / productline API 分工清楚。 | 採用 | 建議 v2 endpoint 僅作前端 read-only 聚合，底層可重用既有查詢邏輯。 |
| 生產工單完成狀態如何判斷 | DB 中 `work_order` 未見明確狀態欄，需由 production_data / output / 品檢 / 入庫狀態推導。 | 需由入庫狀態推導。 | 建議第一版以產出量、MES 結束時間與品檢狀態推導；資料不足回傳 `unknown`。 |
| `dailyCapacityMinutes` 的正式來源 | 產線可用產能若無班表或產能日曆，無法準確判斷剩餘產能。 | 是需要 實際的產線產能? 還是僅需 預估的產線產能? | 第一版可使用已確認的產線產能統計表；無資料回傳 0，不自行假設每日工時。 |
| 換線/清潔時間來源 | 畫面需要呈現換線對產能的影響，但目前需確認資料來源。 | 產線上有多台機器， `production_data_machine`用於紀錄機具的啟動、暫停與停止時間。請確認此資料表是否能滿足你的需求。| 若無設定表，第一版回傳 0，並標示後續需補資料表或規則。 |
| 品檢狀態來源 | 使用者要求生產頁加入品檢狀態，但正式 Quality 模組可能尚未完整。 | 相關功能留待下一版實作，現階段於畫面上統一顯示『待實作』| 第一版只使用可驗證的 `warehouse_quality_hold` 或既有 hold 訊號；無資料回傳 `unknown`。 |
| 人工成本與單品人工費率來源 | `production_data_labor.hours` 可算工時，但人員費率/成本來源需確認。 | 目前尚未設計人工費用，請規劃相關設計。 | 人工成本資料不足時回傳 0，不用假設費率。 |
