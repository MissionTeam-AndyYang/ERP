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
| `/api/v2/orders/{orderNo}/fulfillment` | GET | 查詢單一訂單履約追蹤明細 | Proposal / Pending Engineer Review | 供右側明細或履約 tab 顯示訂單從接單、備料、生產、品檢、出貨到收款的 read-only 狀態。 |

## Shared Query Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| date | Integer | NO | 查詢基準/截止時間，UTC timestamp；未提供時使用伺服器目前時間。 |
| period | String | NO | 查詢期間代碼；第一版建議支援 `7d`、`30d`、`90d`，預設 `30d`。 |
| customer_no | String | NO | 客戶 no，對應 `product_order.item_ref_no` / `company.no`。 |
| orderNo | String | NO | 訂購單 no，對應 `product_order.no`。 |
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
        "channel": "String",
        "productNo": "String",
        "productName": "String",
        "quantity": "Float",
        "unit": "Integer",
        "orderAmount": "Integer",
        "estimatedCost": "Integer",
        "estimatedMarginRate": "Float",
        "actualMarginRate": "Float",
        "dueTimestamp": "Integer",
        "shipTimestamp": "Integer",
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
    "commitmentChecks": [
      {
        "orderNo": "String",
        "checkType": "String",
        "status": "String",
        "riskLevel": "Integer",
        "availableQuantity": "Float",
        "requiredQuantity": "Float",
        "gapQuantity": "Float",
        "note": "String"
      }
    ],
    "deliveryRisks": [
      {
        "orderNo": "String",
        "riskType": "String",
        "riskLevel": "Integer",
        "ownerDepartment": "Integer",
        "dueTimestamp": "Integer",
        "note": "String"
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
| payload.summary.openOrderCount | Integer | 查詢期間內尚未完成出貨或收款的訂購單數。 |  |
| payload.summary.highRiskOrderCount | Integer | `deliveryRisk = high_risk` 的訂購單數。 |  |
| payload.summary.commitmentRate | Float | 可承諾訂單比例；公式為 `committableCount / checkedOrderCount * 100`，分母為 0 時回傳 0.0。 |  |
| payload.summary.estimatedMarginRiskCount | Integer | 預估毛利低於門檻或成本資料不足的訂單數。 |  |
| payload.summary.paymentRiskCount | Integer | 收款逾期或剩餘應收金額未結清的訂單數。 |  |
| payload.summary.totalOrderAmount | Integer | 查詢條件內訂單金額加總，來源為 `product_order.amount`。 |  |
| payload.orders[].orderNo | String | 訂購單 no，來源為 `product_order.no`。 |  |
| payload.orders[].customerNo | String | 客戶 no，來源為 `product_order.item_ref_no`。 |  |
| payload.orders[].customerName | String | 客戶名稱，來源為 `product_order.item_ref_displayName`，必要時可由 `company.displayName/name` 補齊。 |  |
| payload.orders[].channel | String | 銷售通路或訂單來源；第一版若無穩定資料來源，回傳空字串，不推測。 |  |
| payload.orders[].productNo | String | 交易品項 no，來源為 `product_order.item_no`。 |  |
| payload.orders[].productName | String | 交易品項名稱，來源為 `product_order.item_name`。 |  |
| payload.orders[].quantity | Float | 訂購數量，來源為 `product_order.count`。 |  |
| payload.orders[].unit | Integer | 單位代碼，來源為 `product_order.unit`，前端負責 enum 顯示文字轉換。 |  |
| payload.orders[].orderAmount | Integer | 訂單金額，來源為 `product_order.amount`。 |  |
| payload.orders[].estimatedCost | Integer | 預估成本；第一版可由 BOM / APS / 成本資料來源計算，若資料不足回傳 0 並以 margin signal 標示。 |  |
| payload.orders[].estimatedMarginRate | Float | 預估毛利率；公式為 `(orderAmount - estimatedCost) / orderAmount * 100`，`orderAmount` 為 0 時回傳 0.0。 |  |
| payload.orders[].actualMarginRate | Float | 實際毛利率；出貨或結算資料不足時回傳 0.0，並由 `marginSignals[].marginRisk` 標示資料不足。 |  |
| payload.orders[].dueTimestamp | Integer | 客戶要求交期，來源為 `product_order.expectedDate`。 |  |
| payload.orders[].shipTimestamp | Integer | 已出貨日期，來源為 `shipping_order.date`；尚未出貨時回傳 0。 |  |
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
| payload.deliveryRisks[].riskType | String | 交期風險類型。 | material_shortage、capacity_shortage、staff_shortage、quality_hold、shipping_blocked、due_date_urgent、margin_risk、payment_risk |
| payload.deliveryRisks[].ownerDepartment | Integer | 風險下一步負責部門，前端負責顯示文字。 |  |
| payload.marginSignals[].marginRisk | String | 毛利風險代碼。 | normal、low_margin、cost_missing、actual_loss |
| payload.paymentSignals[].paymentRisk | String | 收款風險代碼。 | normal、unpaid、partial_paid、overdue |

## GET /api/v2/orders/{orderNo}/fulfillment

### Basic Information

| URL | Method | Description |
| --- | --- | --- |
| `/api/v2/orders/{orderNo}/fulfillment` | GET | 查詢單一訂單履約追蹤明細 |

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
        "note": "String"
      }
    ],
    "dependencies": [
      {
        "area": "String",
        "status": "String",
        "riskLevel": "Integer",
        "ownerDepartment": "Integer",
        "note": "String"
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
| payload.workflow[].startTimestamp | Integer | 步驟開始時間；無資料時回傳 0。 |  |
| payload.workflow[].endTimestamp | Integer | 步驟完成時間；無資料或未完成時回傳 0。 |  |
| payload.workflow[].note | String | 步驟摘要或阻擋原因。 |  |
| payload.dependencies[].area | String | 依賴領域。 | inventory、purchasing、production、quality、shipping、payment |
| payload.dependencies[].status | String | 依賴狀態。 | ready、pending、blocked、unknown |
| payload.dependencies[].riskLevel | Integer | 依賴風險等級。 |  |
| payload.dependencies[].ownerDepartment | Integer | 下一步負責部門。 |  |
| payload.dependencies[].note | String | 依賴或風險說明。 |  |

## Frontend Interaction Notes

| UI Action | API Behavior |
| --- | --- |
| 進入 Orders 頁面 | 呼叫 `GET /api/v2/orders/dashboard?period=30d`，前端將 response normalization 成既有 Orders page shape。 |
| 切換「接單承諾」tab | 使用 dashboard 中的 `commitmentChecks[]` 與 `orders[].commitmentDecision`，必要時以同 query 重新查詢。 |
| 切換「交期風險」tab | 使用 `deliveryRisks[]` 與 `orders[].deliveryRisk` 篩選高風險訂單。 |
| 點選單一訂單 | 呼叫 `GET /api/v2/orders/{orderNo}/fulfillment`，顯示履約 workflow 與 dependencies。 |
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
| 是否同意下一個 core API 提案為 `OrdersWorkspaceScreen` | 第一版前端規劃優先 phase 為 core；Warehouse extension 已延後。 | 待工程師回覆 | 建議採用，符合 integration plan 的 Warehouse → Orders → Production → Quality 順序。 |
| 新增聚合 endpoint 是否採 `/api/v2/orders/dashboard` | 既有前端曾用 `/api/v1/orders/dashboard` mock fallback，但新後端實作已採 v2 模式。 | 待工程師回覆 | 建議新聚合 API 採 `/api/v2/orders/dashboard`；既有 `/api/v1/sale/productorder` 作資料來源或相容層。 |
| `committedTimestamp` 第一版是否需要持久化欄位 | 若沒有保存承諾日，只能由 ATP/CTP 即時計算最早可行日期。 | 待工程師回覆 | 第一版 read-only 可即時計算；若未來要保存承諾結果，再新增 workflow / decision table。 |
| 毛利資料不足時如何處理 | 實際成本可能要等生產與財務結算完成。 | 待工程師回覆 | 資料不足時回傳 0 並以 `marginRisk = cost_missing` 標示，不推測實際毛利。 |
| 品檢與出貨阻擋狀態來源 | Orders 需要跨 Quality / Logistics / Warehouse 的 blocker 訊號。 | 待工程師回覆 | 第一版先由可取得的 work_order、shipping_order、warehouse/quality hold 訊號組成；無資料時回傳 unknown。 |
