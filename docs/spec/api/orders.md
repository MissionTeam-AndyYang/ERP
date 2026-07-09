# orders API Group

> Source: `restserver/package/restserver/api/v2/orders_uri.py`
> Proposal Source: `docs/spec/api-proposal/orders_dashboard_proposal.md`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v2/orders/dashboard](#get-api-v2-orders-dashboard) | GET | 查詢訂單履約風險總覽 | OK | 第一版 read-only，ATP/CTP 欄位固定回傳 deferred / 0 / 空陣列。 |
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
    "shipments": [],
    "commitmentChecks": [],
    "deliveryRisks": [],
    "marginSignals": [],
    "paymentSignals": []
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| payload.summary.openOrderCount | Integer | 未完成出貨的訂購單數。 |  |
| payload.summary.highRiskOrderCount | Integer | `deliveryRisk = high_risk` 的訂購單數。 |  |
| payload.summary.commitmentRate | Float | 第一版 ATP/CTP 待下一版再實作，固定回傳 0.0。 |  |
| payload.summary.estimatedMarginRiskCount | Integer | 預估成本缺漏或毛利資料不足的訂單數。 |  |
| payload.summary.paymentRiskCount | Integer | 出貨後存在未收、逾期、部分收款或帳款資料缺漏的訂單數。 |  |
| payload.summary.totalOrderAmount | Integer | 查詢條件內訂單金額加總，來源為 `product_order.amount`。 |  |
| payload.orders[].stage | String | 訂單目前整體履約階段摘要。 | accepted、material_preparing、scheduled、in_production、quality_check、ready_to_ship、shipped |
| payload.orders[].commitmentDecision | String | 第一版固定回傳 `deferred`。 | deferred |
| payload.orders[].productionFeasibility | String | 第一版固定回傳 `deferred`。 | deferred |
| payload.orders[].paymentStatus | String | 收款狀態。 | unpaid、partial_paid、paid、overdue、unknown |
| payload.shipments[].paymentType | String | 付款/結算方式。 | daily、monthly、unknown |
| payload.shipments[].paymentDueTimestamp | Integer | 應收款到期日；月結統一呼叫 `g_cal_due_date` 推算。 |  |

### Processing Flow

1. 解析查詢條件與期間，建立 `startTimestamp` / `endTimestamp`。
2. 查詢 `product_order` 作為主資料，套用客戶、訂單、關鍵字與期間篩選。
3. 批次查詢 `shipping_order`、`purchase_request`、`purchase_order`、`goods_receipt_note`、`work_order`、`production_data`、`order_payment`。
4. 依訂單彙總出貨、付款、備料、生產與履約狀態。
5. 第一版略過 ATP/CTP，固定回傳 `commitmentChecks = []`、`commitmentDecision = deferred`、`productionFeasibility = deferred`、`committedTimestamp = 0`。
6. 月結付款到期日統一呼叫 `restserver/package/arap/arap.py` 的 `g_cal_due_date`。
7. 組裝 summary、orders、shipments、deliveryRisks、marginSignals、paymentSignals。

### Database Tables Used

| Table | Purpose |
|----------|------|
| product_order | 訂購單主資料。 |
| shipping_order | 出貨狀態、出貨數量與出貨日期。 |
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

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| payload.workflow[].stepCode | String | 履約流程節點代碼。 | order_received、commitment_check、material_request、purchase_readiness、warehouse_readiness、production、quality_check、shipping、payment |
| payload.workflow[].refNo | String | 對應來源單據 no；多筆來源單據第一版以逗號串接或代表性單號表示。 |  |
| payload.workflow[].status | String | 流程節點狀態。 | done、in_progress、pending、blocked、unknown |
| payload.dependencies[].area | String | 依賴領域。 | inventory、purchasing、production、quality、shipping、payment |

### Processing Flow

1. 依 `order_no` 查詢 `product_order`，若不存在回傳空 workflow / dependencies。
2. 批次查詢此訂單相關請購、採購、進貨、派工、生產、出貨與收款資料。
3. 建立固定 workflow 節點：order_received、commitment_check、material_request、purchase_readiness、warehouse_readiness、production、quality_check、shipping、payment。
4. 同一節點若有多筆來源單據，以逗號串接 `refNo`。
5. 第一版 `commitment_check` 不計算 ATP/CTP，回傳 `unknown` 或 `pending`。
6. 建立 dependencies，供前端顯示各領域 readiness。

### Database Tables Used

| Table | Purpose |
|----------|------|
| product_order | 訂購單主資料。 |
| purchase_request | 請購節點。 |
| purchase_order | 採購節點。 |
| goods_receipt_note | 進貨與倉庫備料節點。 |
| work_order | 派工生產節點。 |
| production_data | 生產實績節點。 |
| shipping_order | 出貨節點。 |
| order_payment | 收款節點。 |
