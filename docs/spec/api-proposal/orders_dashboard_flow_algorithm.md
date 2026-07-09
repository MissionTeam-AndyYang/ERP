# Orders Dashboard API 流程與演算法提案

狀態：Proposal / Pending Engineer Review
對應 API 提案：`docs/spec/api-proposal/orders_dashboard_proposal.md`
對應靜態預覽：`docs/spec/api-proposal/orders_dashboard_static_preview.html`

## 文件定位

本文件描述 `OrdersWorkspaceScreen` 所需 read-only API 的後端查詢流程與演算法。此畫面屬於第一版 core 畫面，優先處理「交期與生產是否做得出來」，其次處理「預估/實際毛利」，第三處理「收款」。

第一版建議 endpoint：

```txt
GET /api/v2/orders/dashboard
GET /api/v2/orders/{order_no}/fulfillment
```

## 共用規則

1. 所有 API 僅讀取資料，不寫入任何資料表。
2. enum 僅回傳 code，前端負責多國語系轉換。
3. 金額四捨五入取整數；數量取至小數點第 2 位；單價取至小數點第 4 位；比率取至小數點第 2 位。
4. 後端不得回傳前端路由用的 `drilldownQuery`；前端依目前畫面狀態自行組合 query string。
5. 若資料來源不足，回傳 `unknown`、0 或空陣列，並以 signal 標示資料不足；不得推測不存在的交期、毛利或收款結果。

## 共用 Step 1：解析查詢條件

輸入：

```txt
date
period
customer_no
order_no
commitmentDecision
deliveryRisk
stage
keyword
start
count
x-timezone
```

建議流程：

1. `date` 為查詢截止 UTC timestamp；未提供時使用伺服器目前 UTC timestamp。
2. `period` 支援 `7d`、`30d`、`90d`；未提供或不支援時 fallback 至 `30d`。
3. `start` 小於 0 時以 0 處理。
4. `count` 未提供時預設 50，最大值 100。
5. 查詢主體為 `product_order`；以 `expectedDate`、`date` 或 `creationTime` 的使用規則需工程師確認。第一版 `openOrderCount` 明確定義為未完成出貨的訂單，付款風險另由 `paymentRiskCount` 表示。

## 共用 Step 2：建立訂單基礎資料

主要資料表：

```txt
product_order
company
contract
```

建議欄位對應：

| Response Field | Source / Algorithm |
| --- | --- |
| orderNo | `product_order.no` |
| customerNo | `product_order.item_ref_no` |
| customerName | `product_order.item_ref_displayName`，缺漏時由 `company` 補齊 |
| productNo | `product_order.item_no` |
| productName | `product_order.item_name` |
| quantity | `product_order.count` |
| unit | `product_order.unit` |
| orderAmount | `product_order.amount` |
| dueTimestamp | `product_order.expectedDate` |
| contractNo | `product_order.ref_no` |

## 共用 Step 3：取得出貨、工單、請購與收款資料

關聯資料：

```txt
shipping_order.product_order_no = product_order.no
work_order.product_order_no = product_order.no
purchase_request.product_order_no = product_order.no
order_payment.ref_no = product_order.no
```

處理原則：

1. 一筆 `product_order` 可對應多筆 `shipping_order`，需以 `shipping_order.product_order_no` 批次查詢後依訂單分組。
2. `shipping_order` 用於判斷是否已出貨、部分出貨、待出貨與出貨日期；dashboard 訂單列只回傳 `shipmentSummary`，多筆出貨明細放在 `shipments[]`。
3. `work_order` / `production_data` 用於判斷是否已排產、生產中或完成。
4. `purchase_request` / `purchase_order` 用於判斷材料請購與採購準備。
5. 出貨單完成出庫後才會產生收款；`order_payment` / `payment` 需以出貨單或訂購單關聯判斷帳款狀態。
6. 客戶付款/結算方式可為日結或月結；需依 `product_order.payment_type`、`payment` 條件或既有帳款資料推算 `paymentType` 與 `paymentDueTimestamp`，無法判斷時回傳 `unknown` / 0。

## 共用 Step 4：ATP/CTP 概念與第一版延後範圍

### ATP / CTP 概念

| Term | 中文理解 | 對 Orders 的意義 |
| --- | --- | --- |
| ATP | Available To Promise，可承諾量。 | 先看現有可用庫存與已知入庫/保留後，判斷是否能直接承諾訂單需求。 |
| CTP | Capable To Promise，可產製承諾。 | 若現貨不足，進一步檢查物料、產能、人員、品檢與出貨限制，判斷是否能在交期前生產並交付。 |

第一版 Orders API 暫不實作 ATP/CTP，不寫入承諾結果，也不即時計算可承諾量或可產製承諾。若略過「保存承諾日」欄位，影響如下：

1. 第一版無法提供正式承諾日；未來若改為即時計算，結果會隨庫存、工單、採購與出貨資料變動。
2. 無法追蹤「當初承諾給客戶的日期」與後續變動歷史。
3. 無法支援承諾日審核、版本控管或主管確認紀錄。
4. 第一版可接受此限制，因目前目標是 read-only 風險辨識；若未來要管理正式承諾，需新增承諾結果/決策紀錄資料表。

第一版固定回傳規則：

| Response Field | First Version Rule |
| --- | --- |
| `summary.commitmentRate` | 待下一版再實作，固定回傳 0.0。 |
| `orders[].committedTimestamp` | 待下一版再實作，固定回傳 0。 |
| `orders[].commitmentDecision` | 待下一版再實作，固定回傳 `deferred`。 |
| `orders[].productionFeasibility` | 待下一版再實作，固定回傳 `deferred`。 |
| `commitmentChecks[]` | 待下一版再實作，固定回傳空陣列。 |

下一版檢核類型規劃：

| checkType | Purpose | Suggested Sources |
| --- | --- | --- |
| atp_inventory | 成品或可用庫存是否足夠直接履約 | Warehouse inventory snapshot、shipping_order、inventory_record |
| material_gap | BOM 物料與包材是否有缺口 | BOM、warehouse inventory、purchase_request |
| capacity | 產線與製程產能是否可排入交期 | work_order、aps_quantity、production_line |
| staff | 預估人員是否足夠 | work_order.laborCount、process_labor、employee / workforce |
| quality_shipping | 品檢或出貨是否阻擋交期 | quality signal、shipping_order、warehouse hold |

下一版建議狀態：

```txt
pass
attention
blocked
unknown
```

下一版承諾結果：

```txt
if any critical check = blocked:
  commitmentDecision = not_committable
elif any check = attention or unknown:
  commitmentDecision = coordination_required
else:
  commitmentDecision = committable
```

`committedTimestamp` 若下一版仍無持久化欄位：

1. 所有檢核 pass 時，可用 `product_order.expectedDate`。
2. 需協調或不可承諾時，若 APS 可推算最早可行日期，回傳最早可行日期。
3. 無法推算時回傳 0，不得猜測。

## 共用 Step 5：交期風險判斷

風險類型：

| riskType | 判斷邏輯 |
| --- | --- |
| material_shortage | 第一版不由 ATP/CTP 產生；若既有請購、採購、倉庫或工單資料可明確判斷缺料，才回傳此風險。 |
| capacity_shortage | 第一版不由 CTP 產生；若既有工單或排程資料可明確判斷產能阻擋，才回傳此風險。 |
| staff_shortage | 第一版不由 CTP 產生；若既有人員或工單資料可明確判斷人力阻擋，才回傳此風險。 |
| quality_hold | 品檢狀態 hold 或既有 quality/hold 訊號顯示阻擋。 |
| shipping_blocked | shipping_order 尚未 ready 且接近交期 |
| due_date_urgent | 距 dueTimestamp 小於設定天數且未完成出貨 |
| margin_risk | 預估毛利低於門檻或成本資料不足 |
| payment_risk | 收款逾期或剩餘應收未結清 |

Quality、Logistics、Warehouse blocker 在本 API 中的具體對應：

| Blocker Area | Meaning | Response Fields |
| --- | --- | --- |
| Warehouse blocker | 可用庫存不足、預留/品檢保留導致不可出貨、倉庫尚未完成出庫。第一版不以 ATP/CTP 產生此訊號，只採用既有可讀資料。 | `deliveryRisks[].riskType = material_shortage` 或 `shipping_blocked`、`orders[].materialStatus`、`orders[].shippingStatus` |
| Quality blocker | 品檢未放行、檢驗中或 hold，導致不能生產投入或不能出貨。第一版不以 ATP/CTP 產生此訊號，只採用既有可讀資料。 | `deliveryRisks[].riskType = quality_hold`、`orders[].qualityStatus` |
| Logistics blocker | 出貨單未建立、物流安排未完成、出貨時段或文件阻擋。 | `deliveryRisks[].riskType = shipping_blocked`、`orders[].shippingStatus`、`shipments[]` |

風險等級建議：

```txt
3 = high_risk / blocking
2 = attention / warning
1 = normal notice
0 = no risk
```

`deliveryRisk` 彙總：

```txt
if maxRiskLevel >= 3:
  deliveryRisk = high_risk
elif maxRiskLevel == 2:
  deliveryRisk = attention
else:
  deliveryRisk = normal
```

## 共用 Step 6：履約階段判斷

建議階段順序：

```txt
pending_confirmation
accepted
material_preparing
scheduled
in_production
quality_check
ready_to_ship
shipped
```

判斷原則：

1. 有 `shipping_order` 且已完成出貨數量 >= 訂單數量：`shipped`。
2. 已完成生產但尚未出貨：`ready_to_ship` 或 `quality_check`，需依 quality source 判斷。
3. 有生產資料進行中：`in_production`。
4. 有 `work_order` 但未開始：`scheduled`。
5. 有請購或採購準備但尚未排產：`material_preparing`。
6. 其他正式訂單：`accepted`。
7. 若後續接入報價/合約到正式訂單轉換，未正式接單才用 `pending_confirmation`。

`orders[].stage` 與 fulfillment `workflow[].stepCode` 的差異：

1. `orders[].stage` 是列表用的單一目前階段摘要。
2. `workflow[].stepCode` 是明細用的完整履約流程節點，一張訂單會有多筆。
3. `stage` 可由 workflow 彙總，但不應取代 workflow；例如目前正在生產時，`stage = in_production`，而 workflow 仍需保留 order、material、production、quality、shipping、payment 等所有 step。

`done`、`in_progress`、`pending`、`blocked`、`unknown` 屬於 `workflow[].status`，不是 `orders[].stage` 或 `workflow[].stepCode`。

建議 enum 分工：

| Enum | Response Field | Purpose |
| --- | --- | --- |
| EOrderStage | `orders[].stage` | 訂單目前整體階段摘要。 |
| EOrderFulfillmentStepCode | `workflow[].stepCode` | 履約流程節點代碼。 |
| EOrderWorkflowStepStatus | `workflow[].status` | 單一履約節點的完成狀態。 |

stepCode 對 stage 的彙總關係：

| stepCode | workflow status | stage |
| --- | --- | --- |
| order_received | done | accepted |
| commitment_check | pending / done / blocked | 第一版待下一版再實作；未來可影響 pending_confirmation / accepted |
| material_request | in_progress / blocked | material_preparing |
| purchase_readiness | in_progress / blocked | material_preparing |
| warehouse_readiness | in_progress / blocked | material_preparing |
| production | pending | scheduled |
| production | in_progress | in_production |
| production | done | quality_check 或 ready_to_ship，依品檢狀態判斷 |
| quality_check | pending / in_progress / blocked | quality_check |
| quality_check | done | ready_to_ship |
| shipping | pending / in_progress / blocked | ready_to_ship |
| shipping | done | shipped |
| payment | 任一狀態 | 不改變履約 stage，由 paymentStatus / paymentSignals 表示 |

多單據彙總規則：

1. 一張訂購單可對應 1 筆或多筆採購/進貨/派工/出貨資料，但 `orders[].stage` 仍只回傳單一目前階段摘要。
2. `workflow[].stepCode` 以履約節點彙總，不以單據筆數展開；例如 1 筆採購單與多筆進貨單可彙總在 `purchase_readiness` / `warehouse_readiness`，多筆派工單可彙總在 `production`，多筆出貨單可彙總在 `shipping`。
3. 若同一 stepCode 對應多筆來源單據，第一版可先將 `refNo` 以代表性單號或逗號串接表示；若下一版需要逐筆 drilldown，再新增 workflow step detail 陣列。

以「客戶下訂 1 萬盒餅乾」為例：

| 業務事件 | 來源單據範例 | stepCode | workflow status | stage |
| --- | --- | --- | --- | --- |
| 訂單成立 | `product_order.no = SO-001` | order_received | done | accepted |
| 建立 1 筆採購單 | `purchase_order.no = PO-001` | purchase_readiness | in_progress | material_preparing |
| 分批進貨 | `goods_receipt_note.no = GR-001,GR-002,GR-003` | warehouse_readiness | in_progress | material_preparing |
| 多筆派工產製 | `work_order.no = WO-001,WO-002,WO-003` | production | pending / in_progress | scheduled / in_production |
| 產製後品檢 | 品檢或 hold 訊號 | quality_check | pending / in_progress / blocked | quality_check |
| 分批出貨 | `shipping_order.no = SH-001,SH-002,SH-003` | shipping | in_progress | ready_to_ship |
| 全數出貨 | 多筆 `shipping_order.checkedCount` 加總 >= `product_order.count` | shipping | done | shipped |
| 出貨後收款 | `order_payment.no` / `payment` | payment | pending / in_progress / done | shipped |

## 共用 Step 7：付款到期日推算

`paymentDueTimestamp` 只用於 read-only 風險判斷，不新增或修改帳款資料。

來源優先順序：

1. 若既有帳款資料存在明確到期日欄位，優先使用該帳款到期日。
2. 若無明確到期日，依 `shipping_order.date`、`product_order.payment_type`、付款期間或 `payment` 條件推算。
3. 若必要資料不足，回傳 0，並以 `paymentRisk = unknown` 或 `missing_payment_record` 標示資料不足。

推算規則：

| paymentType | Algorithm |
| --- | --- |
| daily | 以 `shipping_order.date` 為基準；若付款期間存在，使用 `shipping_order.date + payment_period`。 |
| monthly | 統一呼叫 `g_cal_due_date(str_timezone, n_year, n_month, n_day, n_payment_period)`；`n_year/n_month` 來自出貨月份或帳款月份，`n_day` 與 `n_payment_period` 來自付款條件。 |
| unknown | 缺少付款型態、出貨日期或付款條件時回傳 0。 |

已確認 restserver 既有月結付款到期日 util：`restserver/package/arap/arap.py` 的 `g_cal_due_date(str_timezone, n_year, n_month, n_day, n_payment_period)`。後續實作月結付款到期日時應統一集中呼叫此函式，避免 Orders API 與 AR/AP 到期日邏輯不一致。

## 共用 Step 8：毛利與收款訊號

毛利：

```txt
estimatedMarginRate = (orderAmount - estimatedCost) / orderAmount * 100
actualMarginRate = (orderAmount - actualCost) / orderAmount * 100
```

限制：

1. `estimatedCost` 若缺 BOM / APS / 成本資料，回傳 0，`marginRisk = cost_missing`。
2. `actualCost` 若生產與財務尚未結算，回傳 0，`actualMarginRate = 0.0`，不得推測。
3. 毛利門檻第一版需工程師/使用者確認；未確認前可只標示 `cost_missing`，不硬判低毛利。

收款：

1. 使用 `shipping_order` 判斷是否已完成出貨；未出貨時通常尚不產生正式收款風險。
2. 使用 `order_payment` / `payment` 判斷已收、未收、部分收款、逾期。
3. 日結客戶可依共用 Step 7 推算 `paymentDueTimestamp`。
4. 月結客戶可依共用 Step 7 推算 `paymentDueTimestamp`。
5. 若已出貨但查無對應帳款資料，`paymentRisk = missing_payment_record`。
6. 若到期日已過且剩餘應收大於 0，`paymentRisk = overdue`。
7. 若尚無明確收款資料且無法判斷付款條件，`paymentStatus = unknown`。

## GET /orders/dashboard 流程

1. 依共用 Step 1 建立查詢條件。
2. 查詢 `product_order` 取得訂單主資料。
3. 依本頁訂單 no 批次查詢 shipping、work order、purchase、payment 與必要成本資料，避免 N+1 query；ATP/CTP 所需 APS 資料第一版待下一版再實作。
4. 對每張訂單彙總所有出貨單，建立 `shipmentSummary` 與 top-level `shipments[]`。
5. 第一版略過 ATP/CTP，填入固定 deferred 值：`commitmentChecks[] = []`、`commitmentDecision = deferred`、`productionFeasibility = deferred`、`committedTimestamp = 0`。
6. 對每張訂單彙總 delivery risks、stage、ownerDepartment、priority；第一版 delivery risks 不使用 ATP/CTP 計算結果。
7. 對每張訂單計算 marginSignals、paymentSignals，並依共用 Step 7 推算 `paymentDueTimestamp`。
8. 組裝 `orders[]`，並依 `start/count` 分頁。
9. 組裝 `summary`：`openOrderCount` 為未完成出貨訂單數；`paymentRiskCount` 為存在任一收款風險的訂單去重數。

## GET /orders/{order_no}/fulfillment 流程

1. 確認 `product_order.no = order_no` 是否存在；不存在時回傳空 payload 或 404 需工程師確認。
2. 查詢此訂單的請購、採購、工單、生產、品檢、出貨、收款資料。
3. 建立 workflow steps：
   - `order_received`
   - `commitment_check`：第一版待下一版再實作，狀態可回傳 `unknown` 或 `pending`，不得即時計算 ATP/CTP。
   - `material_request`
   - `purchase_readiness`
   - `warehouse_readiness`
   - `production`
   - `quality_check`
   - `shipping`
   - `payment`
4. 建立 dependencies：
   - `inventory`
   - `purchasing`
   - `production`
   - `quality`
   - `shipping`
   - `payment`
5. `workflow[].comment` 優先取來源單據 `comment`，沒有資料時回傳空字串。
6. `dependencies[].comment` 由缺口、阻擋或狀態摘要組成；不得命名為 `note`。
7. 不寫入 workflow event，不建立任何單據。

## 效能注意事項

1. Dashboard API 是跨表聚合，第一版需限制 `period` 與 `count`，避免一次掃描過多訂單。
2. 先批次取回各資料表資料，再於 Python 以 `product_order.no` / `order_no` map 組合，避免逐筆訂單 N+1 query。
3. `product_order.no`、`product_order.expectedDate`、`shipping_order.product_order_no`、`work_order.product_order_no`、`purchase_request.product_order_no`、`order_payment.ref_no`、`order_payment.ref_sub_no` 需確認是否已有索引。
4. 毛利與未來 ATP/CTP 若計算量過大，建議新增每日或訂單層級快照表；第一版先略過 ATP/CTP 並限制查詢範圍。

## 不得推測或需工程師確認

1. 不得自動建立請購單、工單、出貨單或收款資料。
2. 不得在查詢時寫入承諾結果。
3. 第一版不保存承諾日，也不即時計算 ATP/CTP；`committedTimestamp` 固定回傳 0，若未來要追蹤承諾歷史，需新增資料表。
4. 實際毛利資料不足時不得用預估毛利代替。
5. 品檢與出貨阻擋若無資料來源，回傳 `unknown`，不得自行判斷為正常。
6. 無穩定資料來源的 `channel` 不回傳。

## Engineer Review Questions

| 項目 | 需確認原因 | 工程師回覆 | Codex 建議 |
| --- | --- | --- | --- |
| 是否同意 Orders 為 Warehouse 後下一個 core API 設計目標 | 符合第一版 phase core 優先原則。 | 依照既定規劃安排，目前第一版前端畫面優先實作 phase 為 core 的畫面。 | 建議採用。 |
| `/api/v2/orders/dashboard` 是否可作新聚合 endpoint | 需與既有 `/api/v1/sale/productorder` 分工清楚。 | 同意採用`/api/v2/orders/dashboard` | 建議 v2 endpoint 只做 V1 前端 read-only 聚合。 |
| ATP/CTP 第一版資料來源是否足夠 | 影響接單承諾準確性。 | 請詳細說明 ATP 與 CTP 的概念，因為我對這兩者尚不清楚。工程師 V2 已要求第一版先略過 ATP/CTP。 | 已新增 ATP/CTP 概念與不保存承諾日的影響；第一版固定回傳 deferred / 0 / 空陣列，待下一版再實作。 |
| 毛利門檻如何設定 | 影響 margin risk 判斷。 | 目前先保留該欄位，後續於下一版再進一步討論與決定。 | 未確認前不硬判低毛利，只標示 cost_missing / actual_loss。 |
