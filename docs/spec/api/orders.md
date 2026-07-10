# Orders API Group

> Source: `restserver/package/restserver/api/v2/orders_uri.py`
> Proposal Source: `docs/spec/api-proposal/orders_dashboard_proposal.md`
> Flow Source: `docs/spec/api-proposal/orders_dashboard_flow_algorithm.md`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v2/orders/dashboard](#get-api-v2-orders-dashboard) | GET | 查詢訂單履約風險總覽 | OK | 第一版 read-only；已依工程師確認後的提案與程式碼補齊 `shipments`、`deliveryRisks`、`marginSignals`、`paymentSignals` 資料結構。ATP/CTP 暫不實作，`commitmentChecks` 固定回傳空陣列。 |
| [/api/v2/orders/{order_no}/fulfillment](#get-api-v2-orders-order_no-fulfillment) | GET | 查詢單一訂單履約追蹤明細 | OK | 彙總訂單、請購、採購、進貨、派工、生產、出貨與收款節點。 |

## GET /api/v2/orders/dashboard

<a id="get-api-v2-orders-dashboard"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v2/orders/dashboard | GET | 查詢訂單履約風險總覽 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |
| x-timezone | 時區代碼，例如 Asia/Taipei |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|----------|----------------|
| date | Integer | NO | 查詢截止 UTC timestamp；未提供時使用伺服器目前時間。 |
| period | String | NO | 查詢期間代碼，支援 `7d`、`30d`、`90d`，預設 `30d`。 |
| customer_no | String | NO | 客戶 no，對應 `product_order.item_ref_no`。 |
| order_no | String | NO | 訂購單 no，對應 `product_order.no`。 |
| commitmentDecision | String | NO | 第一版僅支援 `deferred`。 |
| deliveryRisk | String | NO | 交期風險篩選：`normal`、`attention`、`high_risk`。 |
| stage | String | NO | 訂單履約階段篩選。 |
| keyword | String | NO | 搜尋訂購單 no、客戶名稱、產品 no、產品名稱。 |
| start | Integer | NO | 分頁起始位置，預設 0。 |
| count | Integer | NO | 分頁筆數，預設 50，上限 100。 |

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
    "range": {
      "period": "String",
      "startTimestamp": "Integer",
      "endTimestamp": "Integer"
    },
    "summary": {
      "openOrderCount": "Integer",
      "highRiskOrderCount": "Integer",
      "commitmentRate": "Float",
      "estimatedMarginRiskCount": "Integer",
      "paymentRiskCount": "Integer",
      "totalOrderAmount": "Integer"
    },
    "total": "Integer",
    "count": "Integer",
    "start": "Integer",
    "orders": [
      {
        "orderNo": "String",
        "customerNo": "String",
        "customerName": "String",
        "productNo": "String",
        "productName": "String",
        "quantity": "Float",
        "unit": "Integer",
        "orderAmount": "Integer",
        "estimatedCost": "Integer",
        "estimatedMarginRate": "Float",
        "actualMarginRate": "Float",
        "dueTimestamp": "Integer",
        "shipmentSummary": {
          "shipmentCount": "Integer",
          "shippedQuantity": "Float",
          "remainingQuantity": "Float",
          "firstShipTimestamp": "Integer",
          "lastShipTimestamp": "Integer",
          "shippingStatus": "String"
        },
        "committedTimestamp": "Integer",
        "stage": "String",
        "deliveryRisk": "String",
        "commitmentDecision": "String",
        "productionFeasibility": "String",
        "riskReason": "String",
        "materialStatus": "String",
        "productionStatus": "String",
        "qualityStatus": "String",
        "shippingStatus": "String",
        "paymentStatus": "String",
        "ownerDepartment": "Integer",
        "priority": "String"
      }
    ],
    "shipments": [
      {
        "orderNo": "String",
        "shippingOrderNo": "String",
        "shipTimestamp": "Integer",
        "expectedQuantity": "Float",
        "shippedQuantity": "Float",
        "amount": "Integer",
        "paymentNo": "String",
        "paymentStatus": "String",
        "paymentType": "String",
        "paymentDueTimestamp": "Integer"
      }
    ],
    "commitmentChecks": [],
    "deliveryRisks": [
      {
        "orderNo": "String",
        "riskType": "String",
        "riskLevel": "Integer",
        "ownerDepartment": "Integer",
        "dueTimestamp": "Integer",
        "comment": "String"
      }
    ],
    "marginSignals": [
      {
        "orderNo": "String",
        "estimatedMarginRate": "Float",
        "actualMarginRate": "Float",
        "marginRisk": "String",
        "estimatedCost": "Integer",
        "actualCost": "Integer"
      }
    ],
    "paymentSignals": [
      {
        "orderNo": "String",
        "paymentStatus": "String",
        "shippingOrderNo": "String",
        "paymentNo": "String",
        "paymentType": "String",
        "paymentDueTimestamp": "Integer",
        "receivedAmount": "Integer",
        "remainingAmount": "Integer",
        "paymentRisk": "String"
      }
    ]
  }
}
```

### Field Description

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| payload.serverTimestamp | Integer | 後端產生 response 的 UTC timestamp。 |  |
| payload.timezone | String | 後端採用的時區代碼；優先取 `x-timezone` header，未提供時由程式預設值回傳。 |  |
| payload.range.period | String | 實際採用的查詢期間代碼。 | 7d、30d、90d |
| payload.range.startTimestamp | Integer | 查詢起始 UTC timestamp，由 `date` 與 `period` 推算。 |  |
| payload.range.endTimestamp | Integer | 查詢截止 UTC timestamp，由 request `date` 或伺服器目前時間決定。 |  |
| payload.summary.openOrderCount | Integer | 未完成出貨的訂購單數；以 `product_order.count` 與該訂單所有 `shipping_order.checkedCount` 加總比較，`shippedQuantity < orderQuantity` 即列入。此欄不混入未收款訂單。 |  |
| payload.summary.highRiskOrderCount | Integer | `deliveryRisk = high_risk` 的訂購單數。 |  |
| payload.summary.commitmentRate | Float | 第一版 ATP/CTP 待下一版再實作，固定回傳 0.0。 |  |
| payload.summary.estimatedMarginRiskCount | Integer | 預估成本缺漏或毛利資料不足的訂單數；目前實作以 `estimatedCost = 0` 判斷。 |  |
| payload.summary.paymentRiskCount | Integer | 出貨後存在未收、逾期、部分收款或帳款資料缺漏的訂單數；同一訂單只計一次。 |  |
| payload.summary.totalOrderAmount | Integer | 查詢條件內訂單金額加總，來源為 `product_order.amount`。 |  |
| payload.total | Integer | 套用查詢條件與風險篩選後的訂單總筆數。 |  |
| payload.count | Integer | 本次 response 實際回傳的 `orders[]` 筆數。 |  |
| payload.start | Integer | 本次 response 的分頁起始位置。 |  |
| payload.orders[].orderNo | String | 訂購單 no，來源為 `product_order.no`。 |  |
| payload.orders[].customerNo | String | 客戶 no，來源為 `product_order.item_ref_no`。 |  |
| payload.orders[].customerName | String | 客戶名稱，來源為 `product_order.item_ref_displayName`。 |  |
| payload.orders[].productNo | String | 產品 no，來源為 `product_order.item_no`。 |  |
| payload.orders[].productName | String | 產品名稱，來源為 `product_order.item_name`。 |  |
| payload.orders[].quantity | Float | 訂購數量，來源為 `product_order.count`，數量取至小數點第 2 位。 |  |
| payload.orders[].unit | Integer | 單位代碼，來源為 `product_order.unit`；前端負責 enum 顯示文字轉換。 |  |
| payload.orders[].orderAmount | Integer | 訂單金額，來源為 `product_order.amount`，金額四捨五入取整數。 |  |
| payload.orders[].estimatedCost | Integer | 預估成本；目前第一版尚未串接成本來源，實作固定為 0。 |  |
| payload.orders[].estimatedMarginRate | Float | 預估毛利率，公式為 `(orderAmount - estimatedCost) / orderAmount * 100`；`orderAmount` 為 0 時回傳 0.0。 |  |
| payload.orders[].actualMarginRate | Float | 實際毛利率；目前第一版尚未串接實際成本來源，實作固定為 0.0。 |  |
| payload.orders[].dueTimestamp | Integer | 客戶要求交期，來源為 `product_order.expectedDate`。 |  |
| payload.orders[].shipmentSummary.shipmentCount | Integer | 此訂單關聯的出貨單筆數，來源為 `shipping_order`。 |  |
| payload.orders[].shipmentSummary.shippedQuantity | Float | 此訂單已出貨數量加總，來源為 `shipping_order.checkedCount`。 |  |
| payload.orders[].shipmentSummary.remainingQuantity | Float | 尚未出貨數量，公式為 `max(orderQuantity - shippedQuantity, 0)`。 |  |
| payload.orders[].shipmentSummary.firstShipTimestamp | Integer | 第一筆出貨日期，來源為此訂單所有 `shipping_order.date` 最小值；無資料回傳 0。 |  |
| payload.orders[].shipmentSummary.lastShipTimestamp | Integer | 最近一筆出貨日期，來源為此訂單所有 `shipping_order.date` 最大值；無資料回傳 0。 |  |
| payload.orders[].shipmentSummary.shippingStatus | String | 出貨狀態彙總；已出貨數量大於等於訂單數量為 `shipped`，大於 0 且未足量為 `partial_shipped`，否則為 `pending`。 | pending、partial_shipped、shipped |
| payload.orders[].committedTimestamp | Integer | 第一版 ATP/CTP 待下一版再實作，固定回傳 0。 |  |
| payload.orders[].stage | String | 訂單目前整體履約階段摘要；由出貨、生產、派工、請購、採購、進貨等狀態推導。 | accepted、material_preparing、scheduled、in_production、shipped |
| payload.orders[].deliveryRisk | String | 交期或帳款風險等級；逾期、出貨後付款資料缺漏或逾期未收為 `high_risk`，7 日內到期為 `attention`，其餘為 `normal`。 | normal、attention、high_risk |
| payload.orders[].commitmentDecision | String | 第一版 ATP/CTP 待下一版再實作，固定回傳 `deferred`。 | deferred |
| payload.orders[].productionFeasibility | String | 第一版 ATP/CTP 待下一版再實作，固定回傳 `deferred`。 | deferred |
| payload.orders[].riskReason | String | 風險原因代碼；由 delivery risk 與 payment risk 推導。 | overdue_due_date、payment_risk、due_date_approaching、empty |
| payload.orders[].materialStatus | String | 材料準備狀態；有進貨資料為 `ready`，有請購或採購資料為 `pending`，否則為 `unknown`。 | ready、pending、unknown |
| payload.orders[].productionStatus | String | 生產狀態；有生產資料為 `in_progress`，有工單為 `scheduled`，已出貨且有工單為 `completed`，否則為 `not_started`。 | not_started、scheduled、in_progress、completed |
| payload.orders[].qualityStatus | String | 品檢狀態；第一版尚未串接品檢資料，固定回傳 `unknown`。 | unknown |
| payload.orders[].shippingStatus | String | 訂單出貨狀態，與 `shipmentSummary.shippingStatus` 相同。 | pending、partial_shipped、shipped |
| payload.orders[].paymentStatus | String | 收款狀態；由出貨單與 `order_payment` 推導。 | unpaid、partial_paid、paid、overdue、unknown |
| payload.orders[].ownerDepartment | Integer | 下一步主要負責部門 enum；由履約階段與付款風險推導，前端負責顯示文字轉換。 |  |
| payload.orders[].priority | String | 訂單處理優先度；高交期風險或付款資料缺漏為 `high`，交期注意或部分收款為 `medium`，其餘為 `low`。 | high、medium、low |
| payload.shipments[].orderNo | String | 出貨單對應的訂購單 no，來源為 `shipping_order.product_order_no`。 |  |
| payload.shipments[].shippingOrderNo | String | 出貨單 no，來源為 `shipping_order.no`。 |  |
| payload.shipments[].shipTimestamp | Integer | 出貨日期，來源為 `shipping_order.date`。 |  |
| payload.shipments[].expectedQuantity | Float | 預計出貨數量，來源為 `shipping_order.expectedCount`。 |  |
| payload.shipments[].shippedQuantity | Float | 實際檢核或出貨數量，來源為 `shipping_order.checkedCount`。 |  |
| payload.shipments[].amount | Integer | 出貨金額；優先依出貨單金額欄位回填，若無則由出貨數量與單價推算，金額取整數。 |  |
| payload.shipments[].paymentNo | String | 對應收款單 no，來源為 `order_payment.no`；無對應資料回傳空字串。 |  |
| payload.shipments[].paymentStatus | String | 此出貨單對應收款狀態。 | unpaid、partial_paid、paid、overdue、unknown |
| payload.shipments[].paymentType | String | 付款或結算方式代碼，依訂單付款條件推導。 | daily、monthly、unknown |
| payload.shipments[].paymentDueTimestamp | Integer | 應收款到期日；月結統一呼叫 `g_cal_due_date` 推算，資料不足時回傳 0。 |  |
| payload.commitmentChecks | Array | 第一版 ATP/CTP 待下一版再實作，固定回傳空陣列。 |  |
| payload.deliveryRisks[].orderNo | String | 風險所屬訂購單 no。 |  |
| payload.deliveryRisks[].riskType | String | 風險類型；目前實作產生交期急迫或付款風險。 | due_date_urgent、payment_risk |
| payload.deliveryRisks[].riskLevel | Integer | 風險等級；2 表示注意，3 表示高風險。 | 2、3 |
| payload.deliveryRisks[].ownerDepartment | Integer | 風險主要負責部門 enum；付款風險為財務，交期風險依訂單 ownerDepartment 回填。 |  |
| payload.deliveryRisks[].dueTimestamp | Integer | 風險參考到期日；目前來源為 `product_order.expectedDate`。 |  |
| payload.deliveryRisks[].comment | String | 系統產生的風險補充說明；例如 due date approaching、due date overdue or payment risk、payment risk。 |  |
| payload.marginSignals[].orderNo | String | 毛利訊號所屬訂購單 no。 |  |
| payload.marginSignals[].estimatedMarginRate | Float | 預估毛利率，與 `orders[].estimatedMarginRate` 相同。 |  |
| payload.marginSignals[].actualMarginRate | Float | 實際毛利率，與 `orders[].actualMarginRate` 相同。 |  |
| payload.marginSignals[].marginRisk | String | 毛利風險；第一版成本尚未串接時回傳 `cost_missing`，若有預估成本則回傳 `normal`。 | normal、cost_missing |
| payload.marginSignals[].estimatedCost | Integer | 預估成本，與 `orders[].estimatedCost` 相同。 |  |
| payload.marginSignals[].actualCost | Integer | 實際成本；目前第一版尚未串接實際成本來源，固定回傳 0。 |  |
| payload.paymentSignals[].orderNo | String | 收款訊號所屬訂購單 no。 |  |
| payload.paymentSignals[].paymentStatus | String | 此出貨單對應收款狀態。 | unpaid、partial_paid、paid、overdue、unknown |
| payload.paymentSignals[].shippingOrderNo | String | 收款訊號對應的出貨單 no。 |  |
| payload.paymentSignals[].paymentNo | String | 對應收款單 no，來源為 `order_payment.no`；無對應資料回傳空字串。 |  |
| payload.paymentSignals[].paymentType | String | 付款或結算方式代碼。 | daily、monthly、unknown |
| payload.paymentSignals[].paymentDueTimestamp | Integer | 應收款到期日。 |  |
| payload.paymentSignals[].receivedAmount | Integer | 已收金額，公式為 `max(totalAmount - remainingAmount, 0)`。 |  |
| payload.paymentSignals[].remainingAmount | Integer | 未收餘額；有 `order_payment` 時依 `balance` 或付款總額推導，無對應資料時以出貨金額視為未收。 |  |
| payload.paymentSignals[].paymentRisk | String | 收款風險代碼。 | normal、unpaid、partial_paid、overdue、missing_payment_record |

### Processing Flow

1. 解析查詢條件與期間，建立 `startTimestamp` / `endTimestamp`，並將 `start`、`count` 限制在合法分頁範圍。
2. 查詢 `product_order` 作為主資料，套用客戶、訂單、關鍵字與期間篩選。
3. 依查詢到的訂單批次查詢 `shipping_order`、`purchase_request`、`purchase_order`、`goods_receipt_note`、`work_order`、`production_data`、`order_payment`、`payment`。
4. 依訂單彙總出貨摘要、材料狀態、生產狀態、付款狀態、交期風險、下一步負責部門與優先度。
5. 第一版略過 ATP/CTP，固定回傳 `commitmentChecks = []`、`commitmentDecision = deferred`、`productionFeasibility = deferred`、`committedTimestamp = 0`。
6. 月結付款到期日統一呼叫 `restserver/package/arap/arap.py` 的 `g_cal_due_date`。
7. 組裝 `summary`、`orders`、`shipments`、`deliveryRisks`、`marginSignals`、`paymentSignals`。
8. 先對 `orders[]` 分頁，再只保留分頁訂單對應的 shipments / risks / margin / payment signals。

### Database Tables Used

| Table | Purpose |
|----------|------|
| product_order | 訂購單主資料、客戶、產品、數量、金額、交期與付款條件。 |
| shipping_order | 出貨狀態、出貨數量、出貨日期與出貨金額推導。 |
| order_payment | 訂單帳款與收款狀態。 |
| payment | 付款條件參考。 |
| purchase_request | 訂單關聯請購狀態。 |
| purchase_order | 採購準備狀態。 |
| goods_receipt_note | 進貨與到貨狀態。 |
| work_order | 派工與排程狀態。 |
| production_data | 生產實績狀態。 |

## GET /api/v2/orders/{order_no}/fulfillment

<a id="get-api-v2-orders-order_no-fulfillment"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v2/orders/{order_no}/fulfillment | GET | 查詢單一訂單履約追蹤明細 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |
| x-timezone | 時區代碼，例如 Asia/Taipei |

### Path Parameters

| Parameter | Type | Required | Description |
|----------|----------|----------|----------------|
| order_no | String | YES | 訂購單 no，對應 `product_order.no`。 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|----------|----------------|
| date | Integer | NO | 查詢基準 UTC timestamp；未提供時使用伺服器目前時間。 |

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "orderNo": "String",
    "workflow": [
      {
        "stepCode": "String",
        "refNo": "String",
        "status": "String",
        "ownerDepartment": "Integer",
        "startTimestamp": "Integer",
        "endTimestamp": "Integer",
        "comment": "String"
      }
    ],
    "dependencies": [
      {
        "area": "String",
        "status": "String",
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
|----------|----------|------|---|
| payload.orderNo | String | 訂購單 no，來源為 path parameter `order_no` 與 `product_order.no`。 |  |
| payload.workflow[].stepCode | String | 履約流程節點代碼；代表接單後從承諾檢查、請購、採購、進貨、生產、品檢、出貨到收款的節點。 | order_received、commitment_check、material_request、purchase_readiness、warehouse_readiness、production、quality_check、shipping、payment |
| payload.workflow[].refNo | String | 對應來源單據 no；多筆來源單據第一版以逗號串接。 |  |
| payload.workflow[].status | String | 流程節點狀態；由該節點對應資料是否存在、是否完成或是否缺資料推導。 | done、in_progress、pending、blocked、unknown |
| payload.workflow[].ownerDepartment | Integer | 該流程節點主要負責部門 enum，前端負責顯示文字轉換。 |  |
| payload.workflow[].startTimestamp | Integer | 該流程節點最早來源日期；無來源資料回傳 0。 |  |
| payload.workflow[].endTimestamp | Integer | 該流程節點最近完成或更新日期；無來源資料回傳 0。 |  |
| payload.workflow[].comment | String | 節點補充說明；來源為主單備註或程式彙總文字，無資料回傳空字串。 |  |
| payload.dependencies[].area | String | 履約依賴領域。 | inventory、purchasing、production、quality、shipping、payment |
| payload.dependencies[].status | String | 依賴狀態；由對應 workflow 或付款狀態推導。 | ready、pending、blocked、unknown |
| payload.dependencies[].riskLevel | Integer | 依賴風險等級；0 表示正常或未知，2 表示注意，3 表示高風險。 | 0、2、3 |
| payload.dependencies[].ownerDepartment | Integer | 依賴領域主要負責部門 enum。 |  |
| payload.dependencies[].comment | String | 依賴狀態補充說明。 |  |

### Processing Flow

1. 依 `order_no` 查詢 `product_order`，若不存在則回傳指定 `orderNo` 與空 `workflow` / `dependencies`。
2. 批次查詢此訂單相關請購、採購、進貨、派工、生產、出貨與收款資料。
3. 建立固定 workflow 節點：`order_received`、`commitment_check`、`material_request`、`purchase_readiness`、`warehouse_readiness`、`production`、`quality_check`、`shipping`、`payment`。
4. 同一節點若有多筆來源單據，以逗號串接 `refNo`。
5. 第一版 ATP/CTP 與品檢訊號尚未串接，因此 `commitment_check` 與 `quality_check` 可能回傳 `unknown`。
6. 依 workflow 狀態建立 dependencies，供前端呈現訂單履約依賴與阻塞原因。

### Database Tables Used

| Table | Purpose |
|----------|------|
| product_order | 訂購單主資料與接單節點。 |
| purchase_request | 請購節點與材料需求狀態。 |
| purchase_order | 採購節點與供應商準備狀態。 |
| goods_receipt_note | 進貨與倉庫可用狀態。 |
| work_order | 派工、排程與生產節點。 |
| production_data | 生產實績狀態。 |
| shipping_order | 出貨節點與出貨完成狀態。 |
| order_payment | 收款節點與付款狀態。 |
