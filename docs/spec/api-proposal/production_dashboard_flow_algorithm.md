# Production Dashboard API 流程與演算法提案

狀態：Proposal / Pending Engineer Review
對應 API 提案：`docs/spec/api-proposal/production_dashboard_proposal.md`
對應靜態預覽：`docs/spec/api-proposal/production_dashboard_static_preview.html`

## 文件定位

本文描述 `ProductionWorkspaceScreen` 所需 read-only API 的後端查詢流程與演算法。此畫面屬於第一版 core 畫面，優先協助管理者檢視：

1. 一週工單排程與產線可用產能。
2. 今日 MES 工單進度。
3. 備料、人員、機台與品檢是否阻擋如期生產。
4. 產時效率、原物料損耗率與單品人工費率。

第一版建議 endpoint：

```txt
GET /api/v2/production/dashboard
GET /api/v2/production/work-orders/{work_order_no}/detail
```

## 共用規則

1. 所有 API 僅讀取資料，不寫入任何資料表。
2. enum 僅回傳 code，前端負責多國語言轉換。
3. 金額四捨五入取整數；數量與重量取至小數點第 2 位；單價取至小數點第 4 位；比率與工時取至小數點第 2 位。
4. 若資料來源不足，回傳 `unknown`、0、false 或空陣列，並以 alert / signal 標示資料不足；不得自行推測不存在的品檢結果、人工費率或產線日產能。
5. 查詢應以批次查詢與 map 彙整為主，避免針對每一張工單逐筆查詢造成 N+1 query。

## 共用 Step 1：解析查詢條件

輸入：

```txt
date
period
production_line_no
oneProcess
secProcess
work_order_no
product_order_no
status
riskType
keyword
start
count
x-timezone
```

建議流程：

1. `date` 為查詢基準 UTC timestamp；未提供時使用伺服器目前 UTC timestamp。
2. `period` 支援 `7d`、`14d`；未提供或不支援時 fallback 至 `7d`。
3. 依 `date` 與 `period` 建立查詢區間，第一版以工單 `work_order.date` / `startTime` 是否落在區間內為主。
4. `start` 小於 0 時以 0 處理。
5. `count` 未提供時預設 50，最大值 100。
6. keyword 僅套用在工單 no、訂單 no、產品 no、產品名稱、產線名稱、批號等可查詢欄位。

## 共用 Step 2：建立工單基礎資料

主要資料表：

```txt
work_order
production_line
product_order
```

建議欄位對應：

| Response Field | Source / Algorithm |
| --- | --- |
| workOrderNo | `work_order.no` |
| productOrderNo | `work_order.product_order_no` |
| apsNo | `work_order.aps_no` |
| productNo | `work_order.product_no` |
| productName | `work_order.product_name` |
| outputItemNo | `work_order.output_item_no` |
| outputItemName | `work_order.output_item_name` |
| productionLineNo | `work_order.production_line_no` |
| productionLineName | `production_line.name` |
| oneProcess | `work_order.oneProcess` |
| secProcess | `work_order.secProcess` |
| plannedStartTimestamp | `work_order.startTime` |
| plannedEndTimestamp | `work_order.endTime` |
| plannedQuantity | `work_order.processCount` |
| unit | `work_order.processUnit` |
| plannedMinutes | `work_order.processTime` |
| requiredStaffCount | `work_order.laborCount` |
| comment | `work_order.comment` |

## 共用 Step 3：批次取得 MES 相關資料

依本頁工單 no 批次查詢：

```txt
production_data
production_data_input
production_data_output
production_data_reuse
production_data_labor
production_data_machine
warehouse_quality_hold
```

處理原則：

1. 使用 `work_order.no` 對應 `production_data*.work_order_no`。
2. 生產投入由 `production_data_input.action = 領料(1)` 加總，退料由 `action = 退料(2)` 加總。
3. 生產產出由 `production_data_output.action = 產製(1)` 加總。
4. 餘料與廢料由 `production_data_reuse.category` 區分。
5. 人員工時由 `production_data_labor.hours` 加總；已指派人數優先使用 `work_order.laborList`，缺漏時以 `production_data_labor.employee_no` 去重。
6. 機台狀態取每台設備最新一筆 `production_data_machine.action`，並彙總為工單機台狀態。
7. 品檢狀態第一版若無 Quality API，僅採 `warehouse_quality_hold` 或已確認 hold 訊號；無資料回傳 `unknown`。

## 共用 Step 4：產線排程與產能計算

產線群組鍵：

```txt
date + productionLineNo + oneProcess + secProcess
```

建議演算法：

```txt
scheduledMinutes = sum(work_order.processTime)
dailyCapacityMinutes = confirmed capacity source, otherwise 0
changeoverMinutes = confirmed changeover source, otherwise 0
availableMinutes = max(dailyCapacityMinutes - scheduledMinutes - changeoverMinutes, 0)
utilizationRate = scheduledMinutes / dailyCapacityMinutes * 100
```

瓶頸排序：

```txt
if dailyCapacityMinutes <= 0:
  bottleneckRank = 0
else:
  sort by availableMinutes ascending, utilizationRate descending
```

風險等級：

```txt
if dailyCapacityMinutes > 0 and scheduledMinutes + changeoverMinutes > dailyCapacityMinutes:
  riskLevel = 3
elif dailyCapacityMinutes > 0 and utilizationRate >= 90:
  riskLevel = 2
elif dailyCapacityMinutes > 0 and utilizationRate >= 75:
  riskLevel = 1
else:
  riskLevel = 0
```

限制：

1. 若尚無班表、產能日曆或產線日產能設定，`dailyCapacityMinutes` 回傳 0，不自行假設每日 8 小時或 10 小時。
2. 若尚無換線/清潔規則，`changeoverMinutes` 回傳 0，並在 Engineer Review Questions 保留確認項。

## 共用 Step 5：備料 readiness 判斷

來源優先順序：

1. `aps_quantity_item` 或 BOM/APS 提供的工單所需投入料品。
2. `production_data_input` 已領料、退料紀錄。
3. Warehouse inventory snapshot / inventory API 可提供的可用庫存。
4. 若上述資料不足，回傳 `unknown`。

建議狀態：

```txt
if requiredQuantity <= 0 and no material requirement source:
  materialStatus = unknown
elif availableQuantity + issuedQuantity >= requiredQuantity:
  materialStatus = ready
elif issuedQuantity > 0 or availableQuantity > 0:
  materialStatus = partial
else:
  materialStatus = shortage
```

`gapQuantity`：

```txt
gapQuantity = max(requiredQuantity - issuedQuantity - availableQuantity, 0)
```

注意：

1. 若 Warehouse inventory snapshot 已封裝可用庫存計算，Production API 應重用該封裝模組或服務，不重複撰寫庫存快照邏輯。
2. 不得僅因查無資料就判斷為 ready。

## 共用 Step 6：人員 readiness 判斷

來源：

```txt
work_order.laborCount
work_order.laborList
production_data_labor
```

建議演算法：

```txt
requiredStaffCount = work_order.laborCount
assignedStaffCount = count distinct laborList, otherwise count distinct production_data_labor.employee_no

if requiredStaffCount <= 0:
  staffStatus = unknown
elif assignedStaffCount >= requiredStaffCount:
  staffStatus = ready
elif assignedStaffCount > 0:
  staffStatus = support_needed
else:
  staffStatus = shortage
```

限制：

1. `production_data_labor` 代表實際投入或已產生的人員數據，不一定等於排程前已指派人員。
2. 若工程師確認 `laborList` 是正式指派人員清單，第一版應優先使用 `laborList`。

## 共用 Step 7：工單狀態與 MES 現況判斷

建議狀態順序：

```txt
scheduled
material_ready
running
paused
quality_check
completed
blocked
unknown
```

建議判斷：

```txt
if qualityStatus in hold / abnormal:
  status = blocked
elif completedQuantity >= plannedQuantity and plannedQuantity > 0:
  status = quality_check or completed, depending on qualityStatus
elif latest machine action = 暫停(2):
  status = paused
elif has production_data_input or production_data_machine action 啟動(1):
  status = running
elif materialStatus = ready and staffStatus = ready:
  status = material_ready
elif work_order exists:
  status = scheduled
else:
  status = unknown
```

`progressRate`：

```txt
if plannedQuantity > 0:
  progressRate = completedQuantity / plannedQuantity * 100
else:
  progressRate = 0
```

## 共用 Step 8：效率、損耗與人工費率

### 產時效率

```txt
standardMinutes = work_order.processTime
actualMinutes = sum(production_data_labor.hours) * 60
if actualMinutes <= 0:
  actualMinutes = actualEndTimestamp - actualStartTimestamp in minutes

if actualMinutes > 0:
  efficiencyRate = standardMinutes / actualMinutes * 100
else:
  efficiencyRate = 0
```

注意：此欄位定義為「產時效率」，不是完整 OEE。若未來要完整 OEE，需另外納入稼動率、性能與良率定義。

### 原物料損耗

優先來源：

```txt
production_data.materialLoss
```

補算規則：

```txt
actualInputQuantity = sum(production_data_input count where action = 領料)
outputQuantity = sum(production_data_output count where action = 產製)
reuseQuantity = sum(production_data_reuse count where category = 餘料)
wasteQuantity = sum(production_data_reuse count where category = 廢料)

materialLossQuantity = actualInputQuantity - outputQuantity - reuseQuantity - wasteQuantity
materialLossQuantity = max(materialLossQuantity, 0)

if actualInputQuantity > 0:
  materialLossRate = materialLossQuantity / actualInputQuantity * 100
else:
  materialLossRate = 0
```

### 單品人工費率

```txt
laborHours = sum(production_data_labor.hours)
laborCost = confirmed labor cost source, otherwise 0
if laborCost > 0 and outputQuantity > 0:
  unitLaborCost = laborCost / outputQuantity
else:
  unitLaborCost = 0
```

限制：

1. 若尚無人員費率或人工成本來源，`laborCost` 與 `unitLaborCost` 回傳 0。
2. 不得使用假設時薪推導人工成本。

## 共用 Step 9：品檢狀態與阻擋判斷

第一版暫定來源：

```txt
warehouse_quality_hold
confirmed Quality API / quality tables when available
```

建議狀態：

```txt
not_started
in_progress
pending_decision
released
hold
abnormal
unknown
```

判斷原則：

1. 若存在 `warehouse_quality_hold` 且 hold quantity 大於 0，`qualityStatus = hold`。
2. 若有正式 Quality API 回傳待判資料，`qualityStatus = pending_decision`。
3. 若有正式 Quality API 回傳放行，`qualityStatus = released`。
4. 若無任何來源，`qualityStatus = unknown`，`qualityBlocksInventory = false`、`qualityBlocksShipment = false`，並以 alert 或 review note 表示資料不足。
5. 不得因查無品檢資料就判斷為合格。

## 共用 Step 10：交期與風險彙總

風險類型：

| riskType | 判斷邏輯 |
| --- | --- |
| material_shortage | `materialStatus = shortage` 或缺口數量大於 0。 |
| staff_shortage | `staffStatus = shortage` 或 `support_needed`。 |
| capacity_bottleneck | 產線利用率過高或已排工時超過日產能。 |
| quality_hold | `qualityStatus = hold / abnormal / pending_decision` 且阻擋入庫或出貨。 |
| schedule_delay | 目前時間超過預計結束時間且工單未完成。 |
| efficiency_loss | `efficiencyRate` 低於門檻；門檻需工程師/使用者確認，未確認前不硬判。 |
| loss_over_threshold | `materialLossRate` 高於門檻；門檻需工程師/使用者確認，未確認前不硬判。 |

風險等級：

```txt
3 = high_risk / blocking
2 = attention / warning
1 = normal notice
0 = no risk
```

`deliveryRisk` 彙總：

```txt
if any riskLevel >= 3:
  deliveryRisk = high_risk
elif any riskLevel == 2:
  deliveryRisk = attention
elif no reliable due date source:
  deliveryRisk = unknown
else:
  deliveryRisk = normal
```

## GET /production/dashboard 流程

1. 依共用 Step 1 建立查詢條件。
2. 查詢符合期間與條件的 `work_order`，並批次取得 `production_line` 與 `product_order`。
3. 依工單 no 批次查詢 `production_data*`、`warehouse_quality_hold`、APS/BOM/庫存來源。
4. 依共用 Step 4 建立 `scheduleByLine[]`。
5. 依共用 Step 5、6、7 建立 `todayWorkOrders[]` 與 `readinessSignals[]`。
6. 依共用 Step 8 建立 `productionMetrics[]`。
7. 依共用 Step 9 建立 `qualitySignals[]`。
8. 依共用 Step 10 建立 `alerts[]` 與工單 `deliveryRisk`。
9. 彙總 `summary`，並依 `start/count` 處理分頁。

## GET /production/work-orders/{work_order_no}/detail 流程

1. 確認 `work_order.no = work_order_no` 是否存在；不存在時回傳空 payload 或 404 需工程師確認。
2. 查詢此工單的 `production_line`、`product_order`、APS、MES、品檢與關聯資料。
3. 建立 `workOrder` 基礎資料。
4. 建立 `materials[]`：所需量、已領量、退料量、可用量與備料狀態。
5. 建立 `mesEvents[]`：投入、產出、餘料、廢料、人員、機台事件依時間排序。
6. 建立 `outputs[]`、`reuseAndWaste[]`、`labor[]`、`machines[]`。
7. 建立 `quality` 摘要；無來源時回傳 `unknown`。
8. 建立 `relatedDocuments[]`：訂單、APS、工單、生產數據、品檢保留、入庫/出貨相關單據。

## 效能注意事項

1. Dashboard API 是跨表聚合，第一版需限制 `period` 與 `count`，避免一次掃描過多工單。
2. 以工單 no 批次查詢 production data tables，再於 Python 以 dictionary map 組合，避免 N+1 query。
3. `work_order.date`、`work_order.startTime`、`work_order.production_line_no`、`production_data*.work_order_no`、`production_data_output.batch_number`、`warehouse_quality_hold.batchNumber` 應確認是否有索引。
4. 若 Warehouse inventory snapshot 已封裝為可共用物件，Production 備料檢查應重用該物件，避免重複維護庫存快照算法。
5. 若未來 Production dashboard 查詢量增加，建議新增日/工單層級統計快照，不在本提案第一版新增。

## 不得推測或需工程師確認

1. 不得自行假設產線每日可用工時。
2. 不得自行假設換線/清潔時間。
3. 不得因查無品檢資料就判斷為合格。
4. 不得使用假設時薪或人員費率推導人工成本。
5. 不得在查詢時建立工單、品檢、入庫、出貨或 MES 資料。
6. 工單完成狀態若缺少明確欄位，需由工程師確認以產出量、MES 結束時間、品檢與入庫狀態的組合規則。

## Engineer Review Questions

| 項目 | 需確認原因 | 工程師回覆 | Codex 建議 |
| --- | --- | --- | --- |
| 工單狀態是否可由 `production_data*` 推導 | `work_order` 目前未見明確 status 欄位。 |  | 第一版以產出量、MES 事件與品檢狀態推導，資料不足回傳 `unknown`。 |
| 產線日產能資料來源 | 需要計算 `dailyCapacityMinutes`、`availableMinutes` 與瓶頸排序。 |  | 無正式來源時回傳 0，不自行假設每日工時。 |
| 換線/清潔時間資料來源 | 使用者希望掌握產能是否足夠，換線會影響排程可行性。 |  | 無正式來源時第一版回傳 0；後續可新增規則表。 |
| 品檢資料來源 | Production 畫面需要品質狀態，但 Quality 模組可能尚未完整。 |  | 第一版僅用已確認來源；無資料回傳 `unknown`。 |
| 備料可用量是否共用 Warehouse snapshot calculator | 避免重複實作庫存快照與可用量算法。 |  | 建議共用既有 Warehouse snapshot/available quantity 封裝。 |
| 人工成本來源 | `production_data_labor` 有工時，但費率/成本需確認。 |  | 無費率來源時人工成本與單品人工費率回傳 0。 |
