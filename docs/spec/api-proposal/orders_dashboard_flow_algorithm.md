# Orders Dashboard API 流程與演算法提案

狀態：Proposal / Pending Engineer Review
對應 API 提案：`docs/spec/api-proposal/orders_dashboard_proposal.md`
對應靜態預覽：`docs/spec/api-proposal/orders_dashboard_static_preview.html`

## 文件定位

本文件描述 `OrdersWorkspaceScreen` 所需 read-only API 的後端查詢流程與演算法。此畫面屬於第一版 core 畫面，優先處理「交期與生產是否做得出來」，其次處理「預估/實際毛利」，第三處理「收款」。

第一版建議 endpoint：

```txt
GET /api/v2/orders/dashboard
GET /api/v2/orders/{orderNo}/fulfillment
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
orderNo
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
5. 查詢主體為 `product_order`；以 `expectedDate`、`date` 或 `creationTime` 的使用規則需工程師確認。第一版建議列表預設抓尚未完成出貨/收款的 open order，再用期間輔助篩選交期與建立時間。

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

1. `shipping_order` 用於判斷是否已出貨、部分出貨、待出貨與出貨日期。
2. `work_order` / `production_data` 用於判斷是否已排產、生產中或完成。
3. `purchase_request` / `purchase_order` 用於判斷材料請購與採購準備。
4. `order_payment` / `payment` 用於判斷收款與帳款風險。

## 共用 Step 4：接單承諾 ATP/CTP 檢核

第一版檢核類型：

| checkType | Purpose | Suggested Sources |
| --- | --- | --- |
| atp_inventory | 成品或可用庫存是否足夠直接履約 | Warehouse inventory snapshot、shipping_order、inventory_record |
| material_gap | BOM 物料與包材是否有缺口 | BOM、warehouse inventory、purchase_request |
| capacity | 產線與製程產能是否可排入交期 | work_order、aps_quantity、production_line |
| staff | 預估人員是否足夠 | work_order.laborCount、process_labor、employee / workforce |
| quality_shipping | 品檢或出貨是否阻擋交期 | quality signal、shipping_order、warehouse hold |

建議狀態：

```txt
pass
attention
blocked
unknown
```

承諾結果：

```txt
if any critical check = blocked:
  commitmentDecision = not_committable
elif any check = attention or unknown:
  commitmentDecision = coordination_required
else:
  commitmentDecision = committable
```

`committedTimestamp` 若無持久化欄位：

1. 所有檢核 pass 時，可用 `product_order.expectedDate`。
2. 需協調或不可承諾時，若 APS 可推算最早可行日期，回傳最早可行日期。
3. 無法推算時回傳 0，不得猜測。

## 共用 Step 5：交期風險判斷

風險類型：

| riskType | 判斷邏輯 |
| --- | --- |
| material_shortage | material_gap 檢核 blocked 或 gapQuantity > 0 |
| capacity_shortage | capacity 檢核 blocked |
| staff_shortage | staff 檢核 blocked |
| quality_hold | 品檢狀態 hold 或 quality_shipping blocked |
| shipping_blocked | shipping_order 尚未 ready 且接近交期 |
| due_date_urgent | 距 dueTimestamp 小於設定天數且未完成出貨 |
| margin_risk | 預估毛利低於門檻或成本資料不足 |
| payment_risk | 收款逾期或剩餘應收未結清 |

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

## 共用 Step 7：毛利與收款訊號

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

1. 使用 `order_payment` / `payment` 判斷已收、未收、部分收款、逾期。
2. 若尚無明確收款資料，`paymentStatus = unknown`，`paymentRisk = normal` 或 `unknown` 需工程師確認。

## GET /orders/dashboard 流程

1. 依共用 Step 1 建立查詢條件。
2. 查詢 `product_order` 取得訂單主資料。
3. 依本頁訂單 no 批次查詢 shipping、work order、purchase、payment、APS 相關資料。
4. 對每張訂單計算 ATP/CTP commitment checks。
5. 對每張訂單彙總 delivery risks、stage、ownerDepartment、priority。
6. 對每張訂單計算 marginSignals、paymentSignals。
7. 組裝 `orders[]`，並依 `start/count` 分頁。
8. 組裝 `summary`。

## GET /orders/{orderNo}/fulfillment 流程

1. 確認 `product_order.no = orderNo` 是否存在；不存在時回傳空 payload 或 404 需工程師確認。
2. 查詢此訂單的請購、採購、工單、生產、品檢、出貨、收款資料。
3. 建立 workflow steps：
   - `order_received`
   - `commitment_check`
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
5. 不寫入 workflow event，不建立任何單據。

## 效能注意事項

1. Dashboard API 是跨表聚合，第一版需限制 `period` 與 `count`，避免一次掃描過多訂單。
2. 先批次取回各資料表資料，再於 Python 以 orderNo map 組合，避免逐筆訂單 N+1 query。
3. `product_order.no`、`product_order.expectedDate`、`shipping_order.product_order_no`、`work_order.product_order_no`、`purchase_request.product_order_no`、`order_payment.ref_no` 需確認是否已有索引。
4. 毛利與 ATP/CTP 若未來計算量過大，建議新增每日或訂單層級快照表；第一版先以 read-only 即時計算並限制範圍。

## 不得推測或需工程師確認

1. 不得自動建立請購單、工單、出貨單或收款資料。
2. 不得在查詢時寫入承諾結果。
3. `committedTimestamp` 是否需持久化欄位，需工程師確認。
4. 實際毛利資料不足時不得用預估毛利代替。
5. 品檢與出貨阻擋若無資料來源，回傳 `unknown`，不得自行判斷為正常。

## Engineer Review Questions

| 項目 | 需確認原因 | 工程師回覆 | Codex 建議 |
| --- | --- | --- | --- |
| 是否同意 Orders 為 Warehouse 後下一個 core API 設計目標 | 符合第一版 phase core 優先原則。 | 待工程師回覆 | 建議採用。 |
| `/api/v2/orders/dashboard` 是否可作新聚合 endpoint | 需與既有 `/api/v1/sale/productorder` 分工清楚。 | 待工程師回覆 | 建議 v2 endpoint 只做 V1 前端 read-only 聚合。 |
| ATP/CTP 第一版資料來源是否足夠 | 影響接單承諾準確性。 | 待工程師回覆 | 先以 inventory、BOM、APS、work_order 可取得資料計算，缺資料回傳 unknown。 |
| 毛利門檻如何設定 | 影響 margin risk 判斷。 | 待工程師回覆 | 未確認前不硬判低毛利，只標示 cost_missing / actual_loss。 |
