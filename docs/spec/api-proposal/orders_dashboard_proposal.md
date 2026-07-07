# 工程師提問
1. 查詢參數的命名規則統一為 xxx_no，因此請將 orderNo 修正為 order_no。

2. 針對`/api/v2/orders/{orderNo}/dashboard`
    - 一筆訂購訂單 (`product_order`) 可能對應到多筆出貨單 (`shipping_order`)。請重新檢視回傳資料中關於出貨資訊的資料結構設計是否合適，例如 shipTimestamp 等欄位。
    - 出貨單在完成出庫後才會產生收款。有些客戶採用月結方式結算，有些則採用當日結算。請重新檢視回傳資料中關於出貨資訊的資料結構設計是否合適，例如 `paymentStatus` 等欄位。
    - summary.openOrderCount 是否表示尚未完成出貨加上尚未收款的訂單總數？是否可以定義為『未完成出貨的訂單』？
    - 請針對 summary.paymentRiskCount，詳細說明其計算邏輯與判斷依據。
    - 針對 orders[].channel，請說明其對應的資料表欄位來源。
    - 請比較 orders[].stage 與 `/api/v2/orders/{orderNo}/fulfillment` 中 stepCode 欄位的差異。
    - 請詳細說明 orders[].xxxStatus 的各欄位，並指出其來源資料表或邏輯計算方式。
    - 請進一步解釋 orders[].productionFeasibility 的含義與判斷依據。

3. 針對`/api/v2/orders/{orderNo}/fulfillment`
   - 請說明回傳 workflow 資料結構中各欄位分別對應至哪個資料表的欄位。
   - 請詳細解釋 dependencies 的各欄位，並指出其來源資料表。
   - 回傳資料中的備註欄位統一命名為 comment，請將原本的 note 更名為 comment。

## 工程師提問理解與文件更新

| 工程師提問 | 理解與確認 | 本次文件更新 |
| --- | --- | --- |
| 查詢參數 `orderNo` 改為 `order_no`。 | 採用。Query parameter 與 path parameter 採 `order_no`，以符合 `xxx_no` 命名規則；response 內用於前端 mapper 的 `orderNo` 暫時維持 camelCase，若工程師要求 response 全面 snake_case，需另行確認。 | Shared Query Parameters、detail endpoint path、Frontend Interaction Notes 已更新。 |
| 一筆 `product_order` 可能對應多筆 `shipping_order`，需重檢出貨資料結構。 | 採用。移除單一 `shipTimestamp` 欄位，改為 `orders[].shipmentSummary` 與 top-level `shipments[]`，以支援多筆出貨單。 | Success Response Data、Field Description、流程文件已更新。 |
| 出貨完成後才會產生收款，且存在月結/當日結算。 | 採用。付款訊號改以出貨單與帳款資料為基礎，新增 `settlementType`、`shippingOrderNo`、`paymentNo`、`paymentDueTimestamp` 等欄位。 | `paymentSignals[]`、`summary.paymentRiskCount` 說明與流程文件已更新。 |
| `summary.openOrderCount` 是否可定義為未完成出貨訂單。 | 採用。`openOrderCount` 明確定義為「未完成出貨的訂購單數」，不混入未收款訂單。 | Summary 欄位說明與演算法已更新。 |
| `summary.paymentRiskCount` 需詳細說明計算邏輯。 | 採用。以出貨後已產生應收、逾期未收、部分收款或付款資料缺漏等條件判斷。 | Field Description 與 flow Step 7 已補充。 |
| `orders[].channel` 需說明資料來源。 | 現有 DB/API 文件無穩定欄位可支援通路，因此第一版 API 不回傳 `channel`，避免推測不存在資料；前端若仍需顯示可在 mapper 補空字串。 | Success Response Data 與 Field Description 已移除 `channel`。 |
| 比較 `orders[].stage` 與 fulfillment `stepCode` 差異。 | `stage` 是訂單目前整體階段的單一摘要；`stepCode` 是履約明細中的每一個流程節點。 | 新增「Stage vs Workflow StepCode」章節。 |
| 詳細說明 `orders[].xxxStatus` 欄位來源與計算方式。 | 採用。補充 material、production、quality、shipping、payment status 的來源資料表與邏輯。 | 新增「Orders Status Fields」章節。 |
| 說明 `orders[].productionFeasibility` 含義與判斷依據。 | `productionFeasibility` 表示此訂單能否依承諾/交期生產完成，主要由物料、產能、人員、品檢/出貨阻擋組合判斷。 | 新增「Production Feasibility」章節，流程文件同步更新。 |
| workflow / dependencies 欄位需對應資料表欄位。 | 採用。補充欄位來源與演算法。 | Fulfillment Field Description 與流程文件已更新。 |
| 備註欄位統一命名 `comment`。 | 採用。所有 response 中原 `note` 改為 `comment`。 | JSON Structure、Field Description、流程文件已更新。 |

# Orders Dashboard API Proposal

> Status: Proposal / Pending Engineer Review
> Target UI Preview: `docs/spec/api-proposal/orders_dashboard_static_preview.html`
> Flow / Algorithm: `docs/spec/api-proposal/orders_dashboard_flow_algorithm.md`
> Related V1 Rule: 第一版前端畫面優先實作 phase 為 core 的畫面；依整體 read-only integration 順序，Warehouse core 後的下一個 core 畫面為 `OrdersWorkspaceScreen`。


## Screen Intent

`OrdersWorkspaceScreen` 是第一版 core 畫面，主要回答管理者最關心的三件事：

1. 交期與生產是否做得出來。
2. 預估與實際毛利是否有風險。
3. 收款或帳款是否可能影響營運。

此 API 提案只處理 read-only 查詢，不建立訂單、不修改合約、不產生請購單、不建立工單，也不更新收款狀態。前端可先以此資料取代 Orders mock data，後續若工程師確認資料來源與演算法，再進入正式 API 文件與後端實作。

## API Summary

| URL | Method | Description | Status | Review Note |
| --- | --- | --- | --- | --- |
| `/api/v2/orders/dashboard` | GET | 查詢訂單履約風險總覽 | Proposal / Pending Engineer Review | 首屏聚合 API，回傳 KPI、訂單清單、接單承諾、交期風險、毛利與收款摘要。 |
| `/api/v2/orders/{order_no}/fulfillment` | GET | 查詢單一訂單履約追蹤明細 | Proposal / Pending Engineer Review | 供右側明細或履約 tab 顯示訂單從接單、備料、生產、品檢、出貨到收款的 read-only 狀態。 |

## Shared Query Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| date | Integer | NO | 查詢基準/截止時間，UTC timestamp；未提供時使用伺服器目前時間。 |
| period | String | NO | 查詢期間代碼；第一版建議支援 `7d`、`30d`、`90d`，預設 `30d`。 |
| customer_no | String | NO | 客戶 no，對應 `product_order.item_ref_no` / `company.no`。 |
| order_no | String | NO | 訂購單 no，對應 `product_order.no`。 |
| commitmentDecision | String | NO | 接單承諾結果；允許 `committable`、`coordination_required`、`not_committable`。 |
| deliveryRisk | String | NO | 交期風險；允許 `normal`、`attention`、`high_risk`。 |
| stage | String | NO | 訂單履約階段代碼；前端負責多國語系轉換。 |
| keyword | String | NO | 關鍵字；第一版可搜尋訂單 no、客戶名稱、產品 no、產品名稱。 |
| start | Integer | NO | 分頁起始位置，預設 0。 |
| count | Integer | NO | 分頁筆數，預設 50，第一版上限 100。 |

## Numeric Format Rules

| Numeric Meaning | Format |
| --- | --- |
| 單價 | 四捨五入取至小數點第 4 位 |
| 重量或數量 | 四捨五入取至小數點第 2 位 |
| 金額 | 四捨五入取整數 |
| 比率 | 四捨五入取至小數點第 2 位 |

## GET /api/v2/orders/dashboard

### Basic Information

| URL | Method | Description |
| --- | --- | --- |
| `/api/v2/orders/dashboard` | GET | 查詢訂單履約風險總覽 |

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
        "settlementType": "String",
        "paymentDueTimestamp": "Integer"
      }
    ],
    "commitmentChecks": [
      {
        "orderNo": "String",
        "checkType": "String",
        "status": "String",
        "riskLevel": "Integer",
        "availableQuantity": "Float",
        "requiredQuantity": "Float",
        "gapQuantity": "Float",
        "comment": "String"
      }
    ],
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
        "settlementType": "String",
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
| --- | --- | --- | --- |
| payload.serverTimestamp | Integer | 後端產生 response 的 UTC timestamp。 |  |
| payload.timezone | String | 後端採用的時區代碼；預設可依 `x-timezone` header 或 UTC 回傳。 |  |
| payload.range.period | String | 實際採用的查詢期間代碼。 |  |
| payload.range.startTimestamp | Integer | 查詢起始 UTC timestamp，由 `date - period` 推算。 |  |
| payload.range.endTimestamp | Integer | 查詢截止 UTC timestamp，由 request `date` 或伺服器目前時間決定。 |  |
| payload.summary.openOrderCount | Integer | 未完成出貨的訂購單數；以 `product_order.count` 與此訂單所有 `shipping_order.checkedCount` 加總比較，`shippedQuantity < orderQuantity` 即列入。此欄不混入未收款訂單。 |  |
| payload.summary.highRiskOrderCount | Integer | `deliveryRisk = high_risk` 的訂購單數。 |  |
| payload.summary.commitmentRate | Float | 可承諾訂單比例；公式為 `committableCount / checkedOrderCount * 100`，分母為 0 時回傳 0.0。 |  |
| payload.summary.estimatedMarginRiskCount | Integer | 預估毛利低於門檻或成本資料不足的訂單數。 |  |
| payload.summary.paymentRiskCount | Integer | 收款風險訂單數；同一訂單只計 1 次。判斷條件包含：已有出貨單但查無對應 `order_payment`、已到 `paymentDueTimestamp` 但 `remainingAmount > 0`、部分收款未結清、或 `paymentRisk = overdue`。 |  |
| payload.summary.totalOrderAmount | Integer | 查詢條件內訂單金額加總，來源為 `product_order.amount`。 |  |
| payload.orders[].orderNo | String | 訂購單 no，來源為 `product_order.no`。 |  |
| payload.orders[].customerNo | String | 客戶 no，來源為 `product_order.item_ref_no`。 |  |
| payload.orders[].customerName | String | 客戶名稱，來源為 `product_order.item_ref_displayName`，必要時可由 `company.displayName/name` 補齊。 |  |
| payload.orders[].productNo | String | 交易品項 no，來源為 `product_order.item_no`。 |  |
| payload.orders[].productName | String | 交易品項名稱，來源為 `product_order.item_name`。 |  |
| payload.orders[].quantity | Float | 訂購數量，來源為 `product_order.count`。 |  |
| payload.orders[].unit | Integer | 單位代碼，來源為 `product_order.unit`，前端負責 enum 顯示文字轉換。 |  |
| payload.orders[].orderAmount | Integer | 訂單金額，來源為 `product_order.amount`。 |  |
| payload.orders[].estimatedCost | Integer | 預估成本；第一版可由 BOM / APS / 成本資料來源計算，若資料不足回傳 0 並以 margin signal 標示。 |  |
| payload.orders[].estimatedMarginRate | Float | 預估毛利率；公式為 `(orderAmount - estimatedCost) / orderAmount * 100`，`orderAmount` 為 0 時回傳 0.0。 |  |
| payload.orders[].actualMarginRate | Float | 實際毛利率；出貨或結算資料不足時回傳 0.0，並由 `marginSignals[].marginRisk` 標示資料不足。 |  |
| payload.orders[].dueTimestamp | Integer | 客戶要求交期，來源為 `product_order.expectedDate`。 |  |
| payload.orders[].shipmentSummary.shipmentCount | Integer | 此訂單對應的出貨單筆數，來源為 `shipping_order.product_order_no = product_order.no`。 |  |
| payload.orders[].shipmentSummary.shippedQuantity | Float | 此訂單所有出貨單已確認出貨數量加總，來源為 `shipping_order.checkedCount`。 |  |
| payload.orders[].shipmentSummary.remainingQuantity | Float | 未出貨數量；公式為 `product_order.count - shippedQuantity`，最低回傳 0。 |  |
| payload.orders[].shipmentSummary.firstShipTimestamp | Integer | 第一筆出貨單日期，來源為此訂單 `shipping_order.date` 最小值；無出貨單時回傳 0。 |  |
| payload.orders[].shipmentSummary.lastShipTimestamp | Integer | 最近一筆出貨單日期，來源為此訂單 `shipping_order.date` 最大值；無出貨單時回傳 0。 |  |
| payload.orders[].shipmentSummary.shippingStatus | String | 此訂單彙總出貨狀態，依所有 `shipping_order.checkedCount` 與訂單數量判斷。 | pending、partial_shipped、shipped、blocked |
| payload.orders[].committedTimestamp | Integer | 承諾交期；第一版若無持久化欄位，可由 ATP/CTP 檢核推算最早可行日期，無法推算時回傳 0。 |  |
| payload.orders[].stage | String | 訂單履約階段代碼，前端負責多國語系轉換。 | pending_confirmation、accepted、material_preparing、scheduled、in_production、quality_check、ready_to_ship、shipped |
| payload.orders[].deliveryRisk | String | 交期風險代碼，前端負責多國語系轉換與 tone mapping。 | normal、attention、high_risk |
| payload.orders[].commitmentDecision | String | 接單承諾結果代碼。 | committable、coordination_required、not_committable |
| payload.orders[].productionFeasibility | String | 生產可行性代碼。 | feasible、coordination_required、not_feasible |
| payload.orders[].riskReason | String | 主要風險原因摘要；可由最高風險的 delivery risk / commitment check 組成。 |  |
| payload.orders[].materialStatus | String | 物料準備狀態代碼，前端負責顯示文字。 | ready、shortage、pending、unknown |
| payload.orders[].productionStatus | String | 生產狀態代碼，依工單與生產資料判斷。 | not_started、scheduled、in_progress、completed、blocked、unknown |
| payload.orders[].qualityStatus | String | 品檢狀態代碼。 | pending、checking、released、hold、unknown |
| payload.orders[].shippingStatus | String | 出貨狀態代碼。 | pending、ready、partial_shipped、shipped、blocked |
| payload.orders[].paymentStatus | String | 收款狀態代碼。 | unpaid、partial_paid、paid、overdue、unknown |
| payload.orders[].ownerDepartment | Integer | 下一步主要負責部門；前端負責 enum 顯示文字轉換。 |  |
| payload.orders[].priority | String | 管理優先級。 | high、medium、low |
| payload.commitmentChecks[].checkType | String | ATP/CTP 檢核類型。 | atp_inventory、material_gap、capacity、staff、quality_shipping |
| payload.commitmentChecks[].status | String | 檢核狀態代碼，前端負責顯示文字。 | pass、attention、blocked、unknown |
| payload.commitmentChecks[].riskLevel | Integer | 風險等級；數值越高表示風險越高。 |  |
| payload.commitmentChecks[].availableQuantity | Float | 此檢核可用數量或能力。 |  |
| payload.commitmentChecks[].requiredQuantity | Float | 此檢核需求數量或能力。 |  |
| payload.commitmentChecks[].gapQuantity | Float | 缺口數量或能力；公式為 `requiredQuantity - availableQuantity`，無缺口回傳 0。 |  |
| payload.commitmentChecks[].comment | String | 檢核說明或阻擋原因；不得回傳前端顯示用固定翻譯文字。 |  |
| payload.commitmentChecks[].orderNo | String | 此檢核對應的訂購單 no，來源為 `product_order.no`。 |  |
| payload.shipments[].orderNo | String | 訂購單 no，來源為 `shipping_order.product_order_no`。 |  |
| payload.shipments[].shippingOrderNo | String | 出貨單 no，來源為 `shipping_order.no`。 |  |
| payload.shipments[].shipTimestamp | Integer | 出貨單日期，來源為 `shipping_order.date`。 |  |
| payload.shipments[].expectedQuantity | Float | 出貨單預計數量，來源為 `shipping_order.expectedCount`。 |  |
| payload.shipments[].shippedQuantity | Float | 出貨單已確認數量，來源為 `shipping_order.checkedCount`。 |  |
| payload.shipments[].amount | Integer | 出貨單金額，來源為 `shipping_order.amount + addDeleteAmount`。 |  |
| payload.shipments[].paymentNo | String | 帳款編號，來源為 `order_payment.no`；尚未產生帳款時回傳空字串。 |  |
| payload.shipments[].paymentStatus | String | 此出貨單關聯帳款狀態。 | unpaid、partial_paid、paid、overdue、unknown |
| payload.shipments[].settlementType | String | 結算方式，依 `product_order.payment_type` / `payment.paymentType` 推導。 | daily、monthly、unknown |
| payload.shipments[].paymentDueTimestamp | Integer | 應收款到期日；日結通常以出貨日或付款條件推算，月結依付款條件與月結週期推算，無法推算時回傳 0。 |  |
| payload.deliveryRisks[].orderNo | String | 此風險對應的訂購單 no，來源為 `product_order.no`。 |  |
| payload.deliveryRisks[].riskType | String | 交期風險類型。 | material_shortage、capacity_shortage、staff_shortage、quality_hold、shipping_blocked、due_date_urgent、margin_risk、payment_risk |
| payload.deliveryRisks[].riskLevel | Integer | 風險等級；數值越高表示越接近阻擋履約。 |  |
| payload.deliveryRisks[].ownerDepartment | Integer | 風險下一步負責部門，前端負責顯示文字。 |  |
| payload.deliveryRisks[].dueTimestamp | Integer | 此風險對應的處理期限或訂單交期；主要來源為 `product_order.expectedDate`，若是付款風險則可使用 `paymentDueTimestamp`。 |  |
| payload.deliveryRisks[].comment | String | 風險說明或阻擋原因；不得回傳前端顯示用固定翻譯文字。 |  |
| payload.marginSignals[].orderNo | String | 此毛利訊號對應的訂購單 no，來源為 `product_order.no`。 |  |
| payload.marginSignals[].estimatedMarginRate | Float | 預估毛利率；由訂單金額與預估成本計算。 |  |
| payload.marginSignals[].actualMarginRate | Float | 實際毛利率；成本結算不足時回傳 0.0 並以 `marginRisk` 標示。 |  |
| payload.marginSignals[].marginRisk | String | 毛利風險代碼。 | normal、low_margin、cost_missing、actual_loss |
| payload.marginSignals[].estimatedCost | Integer | 預估成本，來源可為 BOM / APS / 成本計算資料；資料不足時回傳 0。 |  |
| payload.marginSignals[].actualCost | Integer | 實際成本，來源為生產與財務結算資料；資料不足時回傳 0。 |  |
| payload.paymentSignals[].orderNo | String | 此收款訊號對應的訂購單 no，來源為 `product_order.no` 或 `order_payment.ref_no`。 |  |
| payload.paymentSignals[].paymentStatus | String | 收款狀態代碼，依帳款與剩餘應收判斷。 | unpaid、partial_paid、paid、overdue、unknown |
| payload.paymentSignals[].shippingOrderNo | String | 此收款訊號對應的出貨單 no；若為訂單層級但未綁定單一出貨單，可回傳空字串。 |  |
| payload.paymentSignals[].paymentNo | String | 帳款編號，來源為 `order_payment.no`。 |  |
| payload.paymentSignals[].settlementType | String | 結算方式。 | daily、monthly、unknown |
| payload.paymentSignals[].paymentDueTimestamp | Integer | 應收款到期 UTC timestamp；依付款條件與結算方式推算，無法推算時回傳 0。 |  |
| payload.paymentSignals[].receivedAmount | Integer | 已收金額；若資料表僅能提供帳款金額與未收狀態，需工程師確認來源。 |  |
| payload.paymentSignals[].remainingAmount | Integer | 剩餘應收金額；通常由應收金額減已收金額計算。 |  |
| payload.paymentSignals[].paymentRisk | String | 收款風險代碼。 | normal、unpaid、partial_paid、overdue、missing_payment_record |

## Stage vs Workflow StepCode

| 欄位 | 位置 | 意義 | 用途 |
| --- | --- | --- | --- |
| `orders[].stage` | Dashboard 訂單清單 | 單一訂單目前整體履約階段摘要，只回傳一個目前狀態。 | 供列表排序、篩選與快速判斷訂單目前卡在哪一段。 |
| `workflow[].stepCode` | Fulfillment detail | 履約流程中的每一個節點，一張訂單會有多個 step。 | 供右側 detail / 履約 tab 顯示完整流程軌跡與每一步來源單據。 |

`stage` 可由 workflow steps 彙總而來，但不等於任一固定 step：例如一張訂單可能同時有 `material_request = done`、`production = in_progress`、`quality_check = pending`，此時 `orders[].stage = in_production`。

## Orders Status Fields

| Field | Meaning | Source / Logic |
| --- | --- | --- |
| `materialStatus` | 物料是否足以支援此訂單履約。 | 優先由 `purchase_request`、`purchase_order`、Warehouse 可用庫存與 BOM/APS material gap 判斷；缺資料回傳 `unknown`。 |
| `productionStatus` | 工單與生產進度。 | 由 `work_order.product_order_no`、`production_data.work_order_no`、生產投入/產出資料判斷；沒有工單為 `not_started` 或 `unknown`。 |
| `qualityStatus` | 品檢或品質放行狀態。 | 第一版若尚無正式 Quality API，可由 quality hold、production output 是否待檢或 workflow blocker 判斷；無資料回傳 `unknown`。 |
| `shippingStatus` | 出貨進度。 | 由 `shipping_order.product_order_no`、`expectedCount`、`checkedCount` 彙總判斷。 |
| `paymentStatus` | 收款狀態。 | 由 `shipping_order` 完成後關聯 `order_payment` / `payment` 判斷；無出貨或無帳款資料時依規則回傳 `unknown` 或 `unpaid`。 |

## Production Feasibility

`orders[].productionFeasibility` 表示「依目前資料，這張訂單能否按交期完成生產並支援履約」，不是單純是否已有工單。

判斷依據：

1. `material_gap` 是否有缺口。
2. `capacity` 是否可在交期前排入產線。
3. `staff` 是否有足夠人力或技能。
4. `quality_shipping` 是否存在品質或出貨阻擋。
5. 既有 `work_order` 是否已排產、進行中或完成。

建議彙總：

```txt
若 material / capacity / staff 任一 critical check blocked:
  productionFeasibility = not_feasible
若任一 check attention 或 unknown:
  productionFeasibility = coordination_required
否則:
  productionFeasibility = feasible
```

## GET /api/v2/orders/{order_no}/fulfillment

### Basic Information

| URL | Method | Description |
| --- | --- | --- |
| `/api/v2/orders/{order_no}/fulfillment` | GET | 查詢單一訂單履約追蹤明細 |

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
| --- | --- | --- | --- |
| payload.orderNo | String | 訂購單 no，來源為 `product_order.no`。 |  |
| payload.workflow[].stepCode | String | 履約步驟代碼，前端負責多國語系轉換。 | order_received、commitment_check、material_request、purchase_readiness、warehouse_readiness、production、quality_check、shipping、payment |
| payload.workflow[].refNo | String | 對應來源單據 no，例如 `product_order.no`、`purchase_request.no`、`work_order.no`、`shipping_order.no` 或 `order_payment.no`。 |  |
| payload.workflow[].status | String | 步驟狀態代碼。 | done、in_progress、pending、blocked、unknown |
| payload.workflow[].ownerDepartment | Integer | 此步驟負責部門。 |  |
| payload.workflow[].startTimestamp | Integer | 步驟開始時間；依 step 來源表取 `date` 或 `creationTime`，無資料時回傳 0。 |  |
| payload.workflow[].endTimestamp | Integer | 步驟完成時間；出貨取 `shipping_order.date`，收款取 `order_payment.date` 或付款完成時間，無資料或未完成時回傳 0。 |  |
| payload.workflow[].comment | String | 步驟摘要或阻擋原因；來源優先取對應單據 `comment`，無資料時回傳空字串。 |  |
| payload.dependencies[].area | String | 依賴領域。 | inventory、purchasing、production、quality、shipping、payment |
| payload.dependencies[].status | String | 依賴狀態。 | ready、pending、blocked、unknown |
| payload.dependencies[].riskLevel | Integer | 依賴風險等級。 |  |
| payload.dependencies[].ownerDepartment | Integer | 下一步負責部門。 |  |
| payload.dependencies[].comment | String | 依賴或風險說明；由各 dependency 的缺口、阻擋或狀態資料組成。 |  |

### Fulfillment Workflow Source Mapping

| stepCode | refNo Source | status Source / Logic | start/end Source |
| --- | --- | --- | --- |
| order_received | `product_order.no` | 訂單存在即 `done`。 | `product_order.date` / `creationTime` |
| commitment_check | 即時計算，無固定來源單號時可回傳空字串 | 依 `commitmentChecks[]` 彙總。 | 查詢時計算，無持久化時間時回傳 0 |
| material_request | `purchase_request.no` | 依請購/採購是否完成判斷。 | `purchase_request.date` / `creationTime` |
| purchase_readiness | `purchase_order.no` | 依採購單與到貨資料判斷。 | `purchase_order.date` / 到貨日期 |
| warehouse_readiness | 出入庫或庫存相關單號 | 依 Warehouse 可用庫存、預留、品檢保留判斷。 | 對應庫存/倉庫紀錄時間 |
| production | `work_order.no` | 依 `work_order`、`production_data` 判斷。 | `work_order.date`、生產資料時間 |
| quality_check | 品檢或 hold 相關單號；第一版無來源時空字串 | 依 Quality / hold 訊號判斷。 | 品檢或 hold 紀錄時間 |
| shipping | `shipping_order.no` | 依此訂單所有出貨單彙總。 | `shipping_order.date` |
| payment | `order_payment.no` | 依帳款與收款狀態判斷。 | `order_payment.date` / 付款完成時間 |

### Fulfillment Dependency Source Mapping

| area | status Source / Logic | ownerDepartment | comment Source |
| --- | --- | --- | --- |
| inventory | Warehouse 可用庫存、預留、品檢保留與 ATP 檢核。 | 庫存不足時為 Warehouse 或 Planning，依缺口來源決定。 | ATP 缺口、批號可用性或安全水位摘要。 |
| purchasing | `purchase_request` / `purchase_order` 狀態。 | Purchasing。 | 未完成採購、到貨延遲或供應商確認摘要。 |
| production | `work_order`、`aps_quantity`、`production_data`。 | Production / Planning。 | 產能、人員或工單阻擋摘要。 |
| quality | Quality hold、檢驗狀態或 production output 待檢狀態。 | Quality。 | 品檢未放行、hold 或檢驗中摘要。 |
| shipping | `shipping_order` 與物流/倉庫出貨狀態。 | Logistics / Warehouse。 | 未建立出貨單、出貨未完成或出貨阻擋摘要。 |
| payment | `order_payment` / `payment`。 | Finance。 | 未收款、部分收款、逾期或帳款未產生摘要。 |

## Frontend Interaction Notes

| UI Action | API Behavior |
| --- | --- |
| 進入 Orders 頁面 | 呼叫 `GET /api/v2/orders/dashboard?period=30d`，前端將 response normalization 成既有 Orders page shape。 |
| 切換「接單承諾」tab | 使用 dashboard 中的 `commitmentChecks[]` 與 `orders[].commitmentDecision`，必要時以同 query 重新查詢。 |
| 切換「交期風險」tab | 使用 `deliveryRisks[]` 與 `orders[].deliveryRisk` 篩選高風險訂單。 |
| 點選單一訂單 | 呼叫 `GET /api/v2/orders/{order_no}/fulfillment`，顯示履約 workflow 與 dependencies。 |
| 切換「毛利與收款」tab | 使用 `marginSignals[]` 與 `paymentSignals[]`；前端負責格式化金額與比率。 |

## Database Tables Used

| Table | Purpose |
| --- | --- |
| product_order | 訂購單主資料、客戶、品項、數量、金額與交期。 |
| contract | 客戶合約與訂單來源合約。 |
| quotation | 報價資料；第一版可作客戶報價與前期 pipeline 參考。 |
| shipping_order | 出貨狀態、出貨數量與出貨日期。 |
| order_payment | 訂單帳款與收款狀態。 |
| payment | 付款條件與帳款規則。 |
| work_order | 生產排程與工單狀態。 |
| production_data | 生產實績與完成狀態。 |
| purchase_request | 訂單關聯材料請購狀態。 |
| purchase_order | 採購準備狀態。 |
| inventory_record | 出貨與庫存異動參考。 |
| aps_quantity / aps_quantity_item | ATP/CTP 可行性與物料/產能建議資料。 |

## Engineer Review Questions

| 項目 | 需確認原因 | 工程師回覆 | Codex 建議 |
| --- | --- | --- | --- |
| 是否同意下一個 core API 提案為 `OrdersWorkspaceScreen` | 第一版前端規劃優先 phase 為 core；Warehouse extension 已延後。 | 依照既定規劃安排，目前第一版前端畫面優先實作 phase 為 core 的畫面。 | 建議採用，符合 integration plan 的 Warehouse → Orders → Production → Quality 順序。 |
| 新增聚合 endpoint 是否採 `/api/v2/orders/dashboard` | 既有前端曾用 `/api/v1/orders/dashboard` mock fallback，但新後端實作已採 v2 模式。 | 同意採用`/api/v2/orders/dashboard` | 建議新聚合 API 採 `/api/v2/orders/dashboard`；既有 `/api/v1/sale/productorder` 作資料來源或相容層。 |
| `committedTimestamp` 第一版是否需要持久化欄位 | 若沒有保存承諾日，只能由 ATP/CTP 即時計算最早可行日期。 | 目前系統並未設計「保存承諾日」，若略過此步驟會產生哪些影響？另外，請詳細說明 ATP 與 CTP 的概念，因為我對這兩者尚不清楚。 | 第一版 read-only 可即時計算；若未來要保存承諾結果，再新增 workflow / decision table。 |
| 毛利資料不足時如何處理 | 實際成本可能要等生產與財務結算完成。 | 採用建議 | 資料不足時回傳 0 並以 `marginRisk = cost_missing` 標示，不推測實際毛利。 |
| 品檢與出貨阻擋狀態來源 | Orders 需要跨 Quality / Logistics / Warehouse 的 blocker 訊號。 | 不清楚 Quality、Logistics、Warehouse 的 blocker 訊號具體指涉為何。請詳細說明，並指出其對應到回傳資料中的哪些欄位。| 第一版先由可取得的 work_order、shipping_order、warehouse/quality hold 訊號組成；無資料時回傳 unknown。 |
