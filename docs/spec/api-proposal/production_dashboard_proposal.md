# 工程師提問V4
 1. 產線每日可派工時目前皆為固定分鐘數。是否可透過新增資料表來紀錄故障停用的分鐘數？或者你有其他更佳的建議？


# 工程師提問V3
1. 針對；`dailyCapacityMinutes` 是當日可排工時分鐘數，還需要班表、產線日曆或每日可排工時設定。
   - 請規劃並設計『每日可排工時設定』，以支援完整的計算。

## 工程師提問V3理解與本次調整

| 工程師提問V3 | 理解與確認 | 本次文件調整 |
| --- | --- | --- |
| 請規劃並設計「每日可排工時設定」。 | 採用。`production_line` 仍維持產線基本資料與每小時產出能力來源；`dailyCapacityMinutes` 應改由每日可排工時設定提供，避免以每小時產能自行推導班表、休息、停線或加班資訊。 | 新增 `[新增提案] production_line_daily_capacity` 資料表設計，並同步補充 `dailyCapacityMinutes`、`capacityStatus`、`availableMinutes`、瓶頸排序與 alert 判斷邏輯。 |
| 無每日可排工時設定時如何處理？ | 不可推測日產能，也不可把 0 解讀為產線無產能。若該日該產線缺少設定，API 回傳 `dailyCapacityMinutes = 0`、`availableMinutes = 0`、`capacityStatus = missing_config`，並產生 `capacity_config_missing` alert。 | 補充 response 欄位、Field Description、Database Tables Used 與 Engineer Review Questions。 |

# 工程師提問V2
1. `production_line`資料表是否足以支援計算 `dailyCapacityMinutes`？ 我對 `dailyCapacityMinutes` 與 `scheduledMinutes` 的差異尚不清楚。是否表示 `dailyCapacityMinutes` 不等於 `scheduledMinutes`，代表當日產能尚未完全排滿？
2. `changeoverMinutes` 留待下一版規劃與實作，現階段於畫面上統一顯示『待實作』。

## 工程師提問V2理解與本次調整

| 工程師提問V2 | 理解與確認 | 本次文件調整 |
| --- | --- | --- |
| `production_line` 是否足以支援計算 `dailyCapacityMinutes`？ | 不足以單獨支援。`production_line.capacity` 是產線每小時產出能力，適合用於未來產量/吞吐量評估；`dailyCapacityMinutes` 是當日可排工時分鐘數，還需要班表、產線日曆或每日可排工時設定。 | 明確定義 `dailyCapacityMinutes`、`scheduledMinutes`、`availableMinutes` 差異；若尚無班表/產能日曆，`dailyCapacityMinutes = 0`，不以 `production_line.capacity` 自行換算。 |
| `dailyCapacityMinutes` 與 `scheduledMinutes` 的差異。 | `dailyCapacityMinutes` 代表該產線當日可排工時上限；`scheduledMinutes` 代表當日已排工單的 `work_order.processTime` 加總。當 `dailyCapacityMinutes > scheduledMinutes + changeoverMinutes`，代表仍有剩餘可排工時。 | 補充欄位描述與 flow 演算法說明，避免將已排工時誤認為總產能。 |
| `changeoverMinutes` 第一版顯示「待實作」。 | 採用。API 不計算預估換線/清潔時間，避免使用 `production_data_machine` 事後啟停紀錄推導計畫換線時間。 | `changeoverMinutes` 改為固定回傳 0，新增 `changeoverStatus = deferred` 供前端顯示「待實作」。 |


# 工程師提問

1. API 回傳的欄位資料，是否有額外預留未來才會使用的欄位？請僅設計目前畫面所需的欄位即可
2. 請重新檢視並補全所有回傳欄位的描述，確保文件完整
3. 針對 `/api/v2/production/dashboard` 
    - 請確認 payload.pagination.total、payload.pagination.start、payload.pagination.count 的資料階層。為了統一規格，建議改為 payload.total、payload.start、payload.count

## 工程師提問理解與本次調整

| 工程師提問 / 回覆 | 理解與確認 | 本次文件調整 |
| --- | --- | --- |
| API 欄位不預留未來才使用的欄位，只設計目前畫面需要欄位。 | 採用。第一版 Production 畫面維持 read-only core dashboard 與 work order detail；尚未實作的 Quality 細節不再展開 sample、defect、hold、blocksInventory、blocksShipment 等欄位。 | 移除 `qualitySignals[]`、`summary.qualityRiskCount`、`qualityBlocksInventory`、`qualityBlocksShipment`、production metrics 品檢統計欄位與 detail `quality` object；保留 `qualityStatus = deferred` 供前端顯示「待實作」。 |
| Dashboard 分頁欄位改為 `payload.total`、`payload.start`、`payload.count`。 | 採用，與既有 Orders / Warehouse 正式 API 文件風格一致。 | 移除 `payload.pagination` object，改為 top-level `total`、`start`、`count`。 |
| 生產工單完成狀態需由入庫狀態推導。 | 採用。單純有產出資料不等於工單完成；完成需確認產出批號已產生對應入庫紀錄。 | `status` enum 新增 `pending_inventory`，完成判斷改為「產出量達標且有製造入庫紀錄才為 completed」。 |
| `dailyCapacityMinutes` 是實際產能或預估產能？ | 第一版畫面目的是排程可行性與接單/排程參考，應採「規劃可排工時」口徑，不用 MES 實際運轉結果倒推。 | 更新 `dailyCapacityMinutes` 描述為當日可排工時；無班表、產線日曆或每日可排工時設定時回傳 0。 |
| `production_data_machine` 是否可滿足換線/清潔時間需求？ | 不足以直接作為換線/清潔規則來源。它可用於實際機台啟停與機台狀態，不宜推測計畫換線/清潔時間。 | `changeoverMinutes` 第一版維持 0，待後續建立製程/產線換線規則表；`production_data_machine` 僅用於 machineStatus 與實際時間參考。 |
| 品檢相關功能留待下一版，現階段畫面統一顯示「待實作」。 | 採用。API 不查詢或推導品檢細節，避免前後端誤認第一版已有品質判斷。 | `qualityStatus` 統一回傳 `deferred`，相關 enum 與說明同步更新。 |
| 備料可用量採用共用 Warehouse snapshot calculator，此類問題後續直接採用共用函式。 | 採用。Production 不重寫庫存快照與可用量算法。 | 備料 readiness 來源改為共用 Warehouse inventory snapshot / available quantity 封裝。 |
| 目前尚未設計人工費用，請規劃相關設計。 | 已檢視 DB，現有 `labor_wage` 可作第一版人工費率來源；若費率缺漏則該筆人工成本以 0 回傳並產生資料缺漏提醒。 | 補充 `labor_wage` lookup 與 `laborCost / unitLaborCost` 演算法，Database Tables Used 加入 `labor_wage`。 |
| 工程師建議：生產投入需以領料扣除退料；工時需判斷 action；入庫狀態可用 `inventory_record.category/source/batchNumber`；`process_labor` 代表預估投入人員。 | 採用。投入量、人工工時、入庫完成狀態與人員 readiness 需依工程師建議更新。 | 更新 `actualInputQuantity`、`laborHours`、`status = completed/pending_inventory` 與 `requiredStaffCount/assignedStaffCount` 來源描述。 |

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
5. 品檢功能留待下一版；第一版僅提供 `qualityStatus = deferred`，由前端顯示「待實作」。

此 API 提案只處理 read-only 查詢，不建立工單、不調整排程、不寫入 MES 資料、不建立品檢單，也不產生入庫或出貨單。前端可先以此資料取代 Production mock data；待工程師確認資料來源與演算法後，再整合至正式 API 文件並開始後端實作。

## API Summary

| URL | Method | Description | Status | Review Note |
| --- | --- | --- | --- | --- |
| `/api/v2/production/dashboard` | GET | 查詢生產排程、產能、MES、效率與損耗總覽 | Proposal / Pending Engineer Review | 首屏聚合 API，回傳一週排程、今日工單、風險、效率與損耗；品檢第一版僅回傳 `deferred`。 |
| `/api/v2/production/work-orders/{work_order_no}/detail` | GET | 查詢單一工單的生產、備料、MES 與關聯單據明細 | Proposal / Pending Engineer Review | 供右側明細、工單 drilldown 或後續 Production detail tab 使用。 |

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
| riskType | String | NO | 風險類型，允許 `material_shortage`、`staff_shortage`、`capacity_bottleneck`、`capacity_config_missing`、`schedule_delay`、`efficiency_loss`、`loss_over_threshold`、`labor_cost_missing`。 |
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
| `/api/v2/production/dashboard` | GET | 查詢生產排程、產能、MES、效率與損耗總覽 |

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
      "averageEfficiencyRate": "Float",
      "averageMaterialLossRate": "Float",
      "averageUnitLaborCost": "Float"
    },
    "total": "Integer",
    "start": "Integer",
    "count": "Integer",
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
        "capacityStatus": "String",
        "changeoverMinutes": "Integer",
        "changeoverStatus": "String",
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
        "riskLevel": "Integer"
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
    ]
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
| payload.summary.averageEfficiencyRate | Float | 查詢期間內有實際工時資料工單的平均產時效率。 |  |
| payload.summary.averageMaterialLossRate | Float | 查詢期間內有投入/產出資料工單的平均原物料損耗率。 |  |
| payload.summary.averageUnitLaborCost | Float | 查詢期間內可由 `labor_wage` 與 `production_data_labor` 計算人工成本之工單平均單品人工費率；費率缺漏的工單不納入平均。 |  |
| payload.total | Integer | 套用查詢條件與風險篩選後的工單總筆數。 |  |
| payload.start | Integer | 本次 response 的分頁起始位置。 |  |
| payload.count | Integer | 本次 response 實際回傳的 `todayWorkOrders[]` 筆數。 |  |
| payload.scheduleByLine[].date | Integer | 排程日期 UTC timestamp。 |  |
| payload.scheduleByLine[].productionLineNo | String | 產線 no，來源為 `production_line.no` 或 `work_order.production_line_no`。 |  |
| payload.scheduleByLine[].productionLineName | String | 產線名稱，來源為 `production_line.name`，缺漏時回傳空字串。 |  |
| payload.scheduleByLine[].oneProcess | Integer | 主製程代碼，來源為 `work_order.oneProcess`。 | 前備(1)、加工(2)、包裝(3)、其他(0) |
| payload.scheduleByLine[].secProcess | Integer | 次製程代碼，來源為 `work_order.secProcess`。 | 依主製程對應 DB 文件定義 |
| payload.scheduleByLine[].dailyCapacityMinutes | Integer | 該產線當日可排工時上限，單位為分鐘；第一版規劃由 `[新增提案] production_line_daily_capacity.availableMinutes` 提供。`production_line.capacity` 是每小時產出能力，不足以單獨換算此欄；若缺少每日可排工時設定，回傳 0。 |  |
| payload.scheduleByLine[].scheduledMinutes | Integer | 查詢日該產線已排工單 `work_order.processTime` 加總。 |  |
| payload.scheduleByLine[].availableMinutes | Integer | 剩餘可排工時，公式為 `dailyCapacityMinutes - scheduledMinutes - changeoverMinutes`，小於 0 時回傳 0；若 `dailyCapacityMinutes` 為 0，表示缺少可排工時基準，不代表產線完全無產能。 |  |
| payload.scheduleByLine[].capacityStatus | String | 每日可排工時設定狀態；`configured` 表示已設定並可計算，`missing_config` 表示缺少設定，`closed` 表示該日休線或不可排，`disabled` 表示設定停用。enum 顯示文字由前端多國語言處理。 | configured、missing_config、closed、disabled |
| payload.scheduleByLine[].changeoverMinutes | Integer | 預估換線/清潔時間；第一版留待下一版規劃與實作，固定回傳 0。 |  |
| payload.scheduleByLine[].changeoverStatus | String | 換線/清潔時間功能狀態；第一版固定回傳 `deferred`，前端顯示「待實作」。 | deferred |
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
| payload.todayWorkOrders[].status | String | 工單狀態代碼，由工單、MES 投入/產出、機台狀態與入庫狀態彙總；產出量達標但尚未入庫時回傳 `pending_inventory`。 | scheduled、material_ready、running、paused、pending_inventory、completed、blocked、unknown |
| payload.todayWorkOrders[].materialStatus | String | 備料狀態代碼，由 BOM/APS 所需投入與 Warehouse 可用量或 `production_data_input` 領料資料判斷。 | ready、partial、shortage、unknown |
| payload.todayWorkOrders[].staffStatus | String | 人員狀態代碼；排程前 readiness 優先由 `process_labor` 預估投入人員與 `work_order.laborCount` 判斷，已開工後可輔以 `production_data_labor` 實際投入人員判斷。 | ready、support_needed、shortage、unknown |
| payload.todayWorkOrders[].machineStatus | String | 機台狀態代碼，由 `production_data_machine.action` 最新狀態判斷。 | running、paused、stopped、unknown |
| payload.todayWorkOrders[].qualityStatus | String | 品檢功能留待下一版實作；第一版固定回傳 `deferred`，前端顯示「待實作」。 | deferred |
| payload.todayWorkOrders[].deliveryRisk | String | 工單是否可能影響交期；由排程時間、完成率、readiness、機台與入庫狀態彙總。 | normal、attention、high_risk、unknown |
| payload.todayWorkOrders[].ownerEmployeeNo | String | 工單負責人員 no，優先來源為 `work_order.creator_no` 或主管確認的 owner 欄位。 |  |
| payload.todayWorkOrders[].ownerEmployeeName | String | 工單負責人員名稱；無資料回傳空字串。 |  |
| payload.readinessSignals[].signalType | String | readiness 訊號類型。 | material、staff、capacity、machine、quality |
| payload.readinessSignals[].status | String | readiness 狀態。 | ready、attention、blocked、unknown |
| payload.readinessSignals[].riskLevel | Integer | readiness 風險等級。 | 0 normal、1 notice、2 attention、3 high_risk |
| payload.readinessSignals[].ownerDepartment | Integer | 下一步負責部門 enum；由 workflow next owner rule 或固定對應規則彙總。 |  |
| payload.readinessSignals[].comment | String | readiness 摘要；僅描述可由資料支持的缺口或阻擋原因。 |  |
| payload.productionMetrics[].standardMinutes | Integer | 標準/預估投產分鐘數，來源為 `work_order.processTime`。 |  |
| payload.productionMetrics[].actualMinutes | Integer | 實際投產分鐘數；第一版以 `production_data_labor.action = 上下班(1)` 的 `hours` 加總後換算分鐘，排除 `休息(2)`，`清潔(3)` 留待下一版換線/間接工時規劃。 |  |
| payload.productionMetrics[].efficiencyRate | Float | 產時效率，`standardMinutes / actualMinutes * 100`；無實際分鐘數回傳 0。 |  |
| payload.productionMetrics[].standardInputQuantity | Float | 標準投入量；第一版優先由 `aps_quantity_item` 或 BOM/APS 資料提供，缺漏時回傳 0。 |  |
| payload.productionMetrics[].actualInputQuantity | Float | 實際淨投入量，公式為 `sum(action = 領料(1)) - sum(action = 退料(2))`，小於 0 時回傳 0。 |  |
| payload.productionMetrics[].outputQuantity | Float | 實際產出量，來源為 `production_data_output.action = 產製(1)` 的 `count` 加總。 |  |
| payload.productionMetrics[].reuseQuantity | Float | 餘料數量，來源為 `production_data_reuse.category = 餘料(1)` 的 `count` 加總。 |  |
| payload.productionMetrics[].wasteQuantity | Float | 廢料數量，來源為 `production_data_reuse.category = 廢料(2)` 的 `count` 加總。 |  |
| payload.productionMetrics[].materialLossQuantity | Float | 原物料損耗量；優先使用 `production_data.materialLoss`，缺漏時由投入、產出、餘料、廢料補算。 |  |
| payload.productionMetrics[].materialLossRate | Float | `materialLossQuantity / actualInputQuantity * 100`；無實際投入量回傳 0。 |  |
| payload.productionMetrics[].laborHours | Float | 人工工作時數；第一版以 `production_data_labor.action = 上下班(1)` 的 `hours` 加總，排除 `休息(2)`，`清潔(3)` 留待下一版換線/間接工時規劃。 |  |
| payload.productionMetrics[].laborCost | Float | 人工成本；依 `production_data_labor.hours` 搭配 `labor_wage` 生效日、員工型態與階級計算。費率缺漏的工時以 0 計，並產生 `labor_cost_missing` alert。 |  |
| payload.productionMetrics[].unitLaborCost | Float | `laborCost / outputQuantity`；無人工成本或產出量回傳 0。 |  |
| payload.alerts[].alertType | String | 異常或提醒類型。 | material_shortage、staff_shortage、capacity_bottleneck、capacity_config_missing、schedule_delay、efficiency_loss、loss_over_threshold、labor_cost_missing |
| payload.alerts[].comment | String | 風險摘要。 |  |

## [新增提案] production_line_daily_capacity

此資料表用於支援 Production Dashboard 第一版的 `dailyCapacityMinutes` 計算，只記錄「某產線某日期可排工時」；不取代 `production_line.capacity`，也不記錄實際 MES 運轉結果。

| Field | Type | Required | Index | Description |
| --- | --- | --- | --- | --- |
| id | BIGINT UNSIGNED | YES | PK | 流水 id。 |
| no | VARCHAR(60) | YES | UNIQUE | 每日可排工時設定 no。 |
| date | INT | YES | UNIQUE(date, production_line_no) / INDEX | 排程日期 UTC timestamp；需與 API 查詢日期歸屬規則一致。 |
| production_line_no | VARCHAR(60) | YES | UNIQUE(date, production_line_no) / INDEX | 產線 no，對應 `production_line.no`。 |
| availableMinutes | INT | YES |  | 該產線該日期可排工時分鐘數；不含不可排休息、停線或保養時間。 |
| status | INT | YES | INDEX | 設定狀態：啟用(1)、停用(2)、休線(3)。 |
| comment | TEXT | NO |  | 設定備註，例如加班、保養、臨時停線原因。 |
| creator_no | VARCHAR(60) | NO | INDEX | 建立人員 no。 |
| creationTime | INT | YES |  | 建立時間 UTC timestamp。 |
| lastUpdateTime | INT | NO |  | 最後更新時間 UTC timestamp。 |

### production_line_daily_capacity 計算規則

1. 查詢鍵為 `date + production_line_no`。
2. `status = 啟用(1)` 時，`dailyCapacityMinutes = availableMinutes`、`capacityStatus = configured`。
3. `status = 休線(3)` 時，`dailyCapacityMinutes = 0`、`capacityStatus = closed`。
4. `status = 停用(2)` 時，`dailyCapacityMinutes = 0`、`capacityStatus = disabled`。
5. 查無設定時，`dailyCapacityMinutes = 0`、`capacityStatus = missing_config`，並產生 `capacity_config_missing` alert。
6. `availableMinutes` 小於 0 時應視為資料異常；第一版 API 回傳 0，並產生 `capacity_config_missing` alert 供工程師或管理者檢查設定。

## GET /api/v2/production/work-orders/{work_order_no}/detail

### Basic Information

| URL | Method | Description |
| --- | --- | --- |
| `/api/v2/production/work-orders/{work_order_no}/detail` | GET | 查詢單一工單的生產、備料、MES 與關聯單據明細 |

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
| payload.workOrder.assignedStaffCount | Integer | 已指派或已有實際人員數；排程前優先由 `process_labor.employee_no` 去重，已開工後可輔以 `production_data_labor.employee_no` 去重。 |  |
| payload.materials[] | Array | 工單所需與已領用料品明細；所需量優先來源 `aps_quantity_item`，已領/退料來源 `production_data_input`，可用量統一呼叫 Warehouse inventory snapshot / available quantity 共用封裝。 |  |
| payload.mesEvents[] | Array | 生產現場事件，彙整投入、產出、餘廢料、人員、機台資料。 | input、output、reuse、waste、labor、machine |
| payload.outputs[] | Array | 工單產出明細，來源為 `production_data_output`。 |  |
| payload.reuseAndWaste[] | Array | 餘料與廢料明細，來源為 `production_data_reuse`。 | 餘料(1)、廢料(2)、其他(0) |
| payload.labor[] | Array | 人員投入明細，來源為 `production_data_labor`。 |  |
| payload.machines[] | Array | 機台狀態明細，來源為 `production_data_machine`。 | 啟動(1)、暫停(2)、停止(3) |
| payload.relatedDocuments[] | Array | 關聯單據，至少包含訂單、APS、工單、生產數據、領退餘廢產單與入庫相關單號。 |  |

## Frontend Interaction Notes

| UI Action | API Behavior |
| --- | --- |
| 進入 Production 頁面 | 呼叫 `GET /api/v2/production/dashboard?period=7d`，前端 normalization 成既有 Production page shape。 |
| 切換「週排程與產能」tab | 使用 `scheduleByLine[]`，依日期、產線、製程群組呈現排程與瓶頸。 |
| 切換「MES 工單現況」tab | 使用 `todayWorkOrders[]` 與 `readinessSignals[]`；品檢區塊第一版顯示 `qualityStatus = deferred` 的「待實作」。 |
| 切換「效率損耗」tab | 第一版使用 `productionMetrics[]` 呈現效率、損耗與人工費率；品檢統計延至下一版。 |
| 點選單一工單 | 呼叫 `GET /api/v2/production/work-orders/{work_order_no}/detail` 顯示右側明細。 |

## Database Tables Used

| Table | Purpose |
| --- | --- |
| work_order | 派工單、排程日期、產線、製程、預估數量、預估工時、預估人數。 |
| production_line | 產線名稱、製程、廠區資訊。 |
| [新增提案] production_line_daily_capacity | 產線每日可排工時設定，支援 `dailyCapacityMinutes`、`capacityStatus`、`availableMinutes` 與產能瓶頸判斷。 |
| process_labor | 預估投入人員資料，用於排程前人員 readiness 與已指派人員數判斷。 |
| aps_quantity / aps_quantity_item | APS 與預估投入料品需求；第一版用於備料需求參考，資料不足時不推測。 |
| production_data | 生產數據主表、製造日期、產線、產品與 materialLoss。 |
| production_data_input | 投入物、領料、退料、批號、投入數量。 |
| production_data_output | 產出物、產出批號、有效期與產出數量。 |
| production_data_reuse | 餘料與廢料數據。 |
| production_data_labor | 人員工時、站點、上下班/休息/清潔事件。 |
| production_data_machine | 機台啟動、暫停、停止、速度與溫度。 |
| labor_wage | 人工時薪；依生效日、員工型態與階級提供人工成本計算費率。 |
| product_order | 訂購單與客戶交期參考，用於 deliveryRisk。 |
| process_order | 領料、退料、餘料、廢料與產品單據，作為製造流程與入庫來源參考。 |
| inventory_record / batch_number | 料品批號、庫存、來源單據與製造入庫狀態參考；工單完成狀態以 `inventory_record.category = 入庫(1)`、`inventory_record.source = 產品(5)`、`inventory_record.batchNumber = production_data_output.batch_number` 判斷，備料可用量應優先重用 Warehouse inventory snapshot。 |

## Engineer Review Questions

| 項目 | 需確認原因 | 工程師回覆 | Codex 建議 |
| --- | --- | --- | --- |
| 是否同意下一個 core API 提案為 `ProductionWorkspaceScreen` | 符合 Warehouse → Orders → Production → Quality 的第一版 core 順序。 | 採用 | 建議採用。 |
| `/api/v2/production/dashboard` 是否可作 Production 聚合 endpoint | 需要與既有 workorder / work / productline API 分工清楚。 | 採用 | 建議 v2 endpoint 僅作前端 read-only 聚合，底層可重用既有查詢邏輯。 |
| 生產工單完成狀態如何判斷 | DB 中 `work_order` 未見明確狀態欄，需由 production_data / output / 入庫狀態推導。 | 需由入庫狀態推導。 | 已採用。第一版完成條件需納入製造入庫紀錄；產出量達標但尚未入庫時回傳 `pending_inventory`，不可直接判斷為 `completed`。 |
| `dailyCapacityMinutes` 的正式來源 | 產線可用產能若無班表或產能日曆，無法準確判斷剩餘產能。 | `production_line`資料表是否足以支援計算？`dailyCapacityMinutes` 與 `scheduledMinutes` 是否表示尚未排滿？ | 已釐清。`production_line.capacity` 是每小時產出能力，不足以單獨計算每日可排分鐘；`dailyCapacityMinutes` 是當日可排工時上限，`scheduledMinutes` 是已排工時，兩者差額才表示剩餘可排工時。 |
| `production_line_daily_capacity` 新增提案 | 需由工程師確認資料表命名、欄位命名、日期歸屬與建立/更新欄位是否符合既有 DB convention。 | 工程師提問V3要求規劃「每日可排工時設定」。 | 建議採此表作為第一版 `dailyCapacityMinutes` 正式來源；確認後再整合至正式 DB schema、正式 API 文件與後端實作。 |
| 換線/清潔時間來源 | 畫面需要呈現換線對產能的影響，但目前需確認資料來源。 | `changeoverMinutes` 留待下一版規劃與實作，現階段畫面統一顯示「待實作」。 | 已採用。第一版固定 `changeoverMinutes = 0`、`changeoverStatus = deferred`；`production_data_machine` 不用於推導計畫換線/清潔時間。 |
| 品檢狀態來源 | 使用者要求生產頁加入品檢狀態，但正式 Quality 模組可能尚未完整。 | 相關功能留待下一版實作，現階段於畫面上統一顯示「待實作」。 | 已採用。第一版不回傳品檢明細資料，僅以 `qualityStatus = deferred` 供前端顯示「待實作」。 |
| 人工成本與單品人工費率來源 | `production_data_labor.hours` 可算工時，但人員費率/成本來源需確認。 | 目前尚未設計人工費用，請規劃相關設計。 | 已補充初版算法：使用既有 `labor_wage` 依生效日、員工型態、階級取得 `hourly`，乘以 `production_data_labor.hours` 計算人工成本；費率缺漏時產生 `labor_cost_missing`。 |
