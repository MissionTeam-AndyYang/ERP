# 工程師提問
1. 請將 URL Path 由 /api/v2/traceability/xxx 更名為 /api/v2/trace/xxx。
2. 請將 primaryRiskCode 更名為 riskCode
3. 請詳細說明『文件完整性』要顯示的內容有哪些。
3. 目前暫時不需提供『文件完整性』與『召回評估』功能，請簡化回傳欄位。
4. 目前以批號為進入點進行追溯：原料批號向下追溯，製成品批號向上追溯；並同步修改查詢條件。
5. 查詢條件暫不開放 documentStatusCode、 traceDirectionCode、traceStatusCode、riskLevelCode; 亦不開放 period，僅保留 startDate 與 endDate。
6. 此追溯功能是否支援單一原料批號可產出多個在製品（如拌料、灌餡等半成品），並由在製品再投入產出多個製成品？
7. 針對 /api/v2/traceability/dashboard
    - records[].queryTypeCode, records[].queryValue 應由前端自行記錄，不應由後端再回傳。
    - 請確認  records[].supplierNo/ supplierName 與 records[].customerNo/customerName 是否會同時存在數值。若會，請具體舉例；若不會，請將欄位簡化為單一組。
   

# TraceabilityWorkspaceScreen API 提案

> Status: API Proposal / Pending Engineer Review  
> Screen: `TraceabilityWorkspaceScreen`  
> Route: `/traceability`  
> Scope: V1 read-only Core  
> Design basis: `AGENTS.md`、`src/app/traceability/page.tsx`、`src/types/traceability.ts`、`docs/spec/api/batchtrace.md`、`docs/spec/api/batches.md`、`docs/spec/database/index.md`

## 1. 畫面定位

「溯源中心」是以批號追溯、文件完整性與召回範圍評估為主的 read-only 工作區。它承接 Batch Center 已整理出的批號與庫存資訊，但使用目的不同：

| 畫面 | 主視角 | 本版邊界 |
|---|---|---|
| `BatchCenterScreen` | 料品 → 批號 → 倉庫分布 | 管理目前仍有庫存的批號、可用量、預留量、品檢保留量與效期風險。 |
| `TraceabilityWorkspaceScreen` | 批號 / 訂單 / 工單 → 追溯鏈 → 影響範圍 | 查詢批號來源、製程投入/產出、庫存流向、出貨與文件完整性；支援召回範圍判讀。 |
| `WarehouseInventoryMovementLedgerScreen` | 庫存異動流水帳 | 下一版延伸畫面，聚焦所有入出庫異動明細查詢，不作為本次 API 範圍。 |

第一版不提供 POST、PUT、DELETE，不建立召回單、不修改文件狀態、不執行庫存鎖定。後端僅回傳 enum code、數值與資料庫欄位；顯示文字與多國語言由前端處理。

## 2. V1 API 清單

| API | Method | 用途 |
|---|---|---|
| `/api/v2/traceability/dashboard` | GET | 查詢溯源中心 KPI、查詢結果清單與預設選取批號摘要 |
| `/api/v2/traceability/batches/{batch_no}/overview` | GET | 查詢單一批號的完整追溯鏈、時間軸、文件完整性與召回影響範圍 |

> 工程師確認前，本文件為 API 提案；確認後才整合至 `docs/spec/api/` 正式 API 文件並進行後端實作。

## 3. 共用 Query Parameters / Header

| Parameter / Header | Type | Required | Description |
|---|---|---:|---|
| `keyword` | String | No | 批號、料號、品名、來源單號、工單號、訂單號、客戶名稱或供應商名稱關鍵字。 |
| `queryTypeCode` | String | No | 查詢類型 code。可用值：`batch`、`item`、`order`、`work_order`、`document`、`all`；預設 `all`。 |
| `traceDirectionCode` | String | No | 追溯方向 code。可用值：`upstream`、`downstream`、`both`；預設 `both`。 |
| `itemCategory` | Integer | No | 料品品項類別 code；前端負責顯示文字。 |
| `itemNo` | String | No | 料品 no。 |
| `batchNo` | String | No | 批號。 |
| `refCategory` | Integer | No | 來源或關聯單據類別 code。 |
| `refNo` | String | No | 來源或關聯單據 no。 |
| `traceStatusCode` | String | No | 追溯狀態 code。可用值：`complete`、`document_pending`、`broken`、`unknown`。 |
| `documentStatusCode` | String | No | 文件狀態 code。可用值：`complete`、`pending`、`missing`、`not_required`、`unknown`。 |
| `riskLevelCode` | String | No | 風險等級 code。可用值：`normal`、`attention`、`high_risk`。 |
| `startDate` | Integer | No | 查詢區間起始 UTC timestamp；未提供時由後端依 `period` 或預設近 90 天判斷。 |
| `endDate` | Integer | No | 查詢區間結束 UTC timestamp；未提供時預設 API 執行當下。 |
| `period` | String | No | 快速區間 code。可用值：`7d`、`30d`、`90d`、`custom`；若提供 `startDate/endDate`，以自訂區間優先。 |
| `start` | Integer | No | 分頁起點，預設 0；負值視為 0。 |
| `count` | Integer | No | 回傳筆數，預設 50，最大 100。 |
| `x-timezone` | Header String | No | 前端顯示偏好的 IANA timezone；後端不以此改寫資料庫保存的 UTC timestamp。 |

## 4. GET `/api/v2/traceability/dashboard`

### 4.1 Success Response Data

```json
{
  "serverTimestamp": "Integer",
  "summary": {
    "traceableBatchCount": "Integer",
    "completeTraceRate": "Float",
    "pendingDocumentCount": "Integer",
    "highRiskTraceCount": "Integer"
  },
  "records": [
    {
      "traceId": "String",
      "queryTypeCode": "String",
      "queryValue": "String",
      "traceDirectionCode": "String",
      "itemNo": "String",
      "itemName": "String",
      "itemCategory": "Integer",
      "itemSubCategory": "Integer",
      "itemType": "Integer",
      "batchNo": "String",
      "refCategory": "Integer",
      "refNo": "String",
      "sourceRefCategory": "Integer",
      "sourceNo": "String",
      "supplierNo": "String",
      "supplierName": "String",
      "customerNo": "String",
      "customerName": "String",
      "workOrderNo": "String",
      "orderNo": "String",
      "warehouseNo": "String",
      "warehouseName": "String",
      "currentQuantity": "Float",
      "impactedQuantity": "Float",
      "impactedCustomerCount": "Integer",
      "unit": "Integer",
      "traceStatusCode": "String",
      "riskLevelCode": "String",
      "primaryRiskCode": "String",
      "documentPendingCount": "Integer",
      "latestEventTimestamp": "Integer"
    }
  ],
  "total": "Integer",
  "start": "Integer",
  "count": "Integer"
}
```

### 4.2 Field Description

| Field Path | Type | Description | Source / Enum |
|---|---|---|---|
| `serverTimestamp` | Integer | API 回應建立時間，UTC timestamp。 | 系統時間 |
| `summary.traceableBatchCount` | Integer | 查詢條件內可建立追溯索引的批號數。 | `batch_number`、追溯資料彙總 |
| `summary.completeTraceRate` | Float | 追溯狀態為 `complete` 的批號比例，百分比數值取至小數點第 2 位。 | `records[].traceStatusCode` |
| `summary.pendingDocumentCount` | Integer | 文件狀態為 `pending` 或 `missing` 的文件數量。 | 文件完整性彙總 |
| `summary.highRiskTraceCount` | Integer | `riskLevelCode=high_risk` 的追溯紀錄數。 | 風險彙總 |
| `records[].traceId` | String | 前端列表用穩定識別值，建議由查詢類型、批號與主要來源單號組成。 | 後端組合 |
| `records[].queryTypeCode` | String | 此列命中的查詢類型 code；前端負責顯示文字。 | `batch`、`item`、`order`、`work_order`、`document` |
| `records[].queryValue` | String | 此列對應的查詢值，例如批號、料號、訂單號或工單號。 | 查詢命中來源 |
| `records[].traceDirectionCode` | String | 追溯方向 code；前端負責顯示文字。 | `upstream`、`downstream`、`both` |
| `records[].itemNo` | String | 料品 no。 | `batch_number.item_no`、生產投入/產出、庫存紀錄 fallback |
| `records[].itemName` | String | 料品名稱；無值時回傳空字串。 | `batch_number.item_name`、生產投入/產出、庫存紀錄 fallback |
| `records[].itemCategory` | Integer | 料品品項類別 code。 | `batch_number.itemCategory` |
| `records[].itemSubCategory` | Integer | 料品品項子類別 code。 | `batch_number.itemSubCategory` |
| `records[].itemType` | Integer | 料品型態 code。 | `batch_number.itemType` |
| `records[].batchNo` | String | 批號。 | `batch_number.no`、`inventory_record.batchNumber`、production batch 欄位 |
| `records[].refCategory` | Integer | 此列主要關聯單據類別 code。 | 由命中資料表的 refCategory 或 workflow refCategory 取得 |
| `records[].refNo` | String | 此列主要關聯單據 no。 | 由命中資料表的 refNo 或 workflow refNo 取得 |
| `records[].sourceRefCategory` | Integer | 批號原始來源單據類別 code。 | `batch_number.refCategory` |
| `records[].sourceNo` | String | 批號原始來源單據 no。 | `batch_number.ref_no` |
| `records[].supplierNo` | String | 供應商 no；非採購來源或無資料時回傳空字串。 | `goods_receipt_note` 或採購來源文件 |
| `records[].supplierName` | String | 供應商名稱；無值時回傳空字串。 | `goods_receipt_note` 或採購來源文件 |
| `records[].customerNo` | String | 客戶 no；尚未流向客戶或無資料時回傳空字串。 | 出貨/銷貨/訂單來源文件 |
| `records[].customerName` | String | 客戶名稱；無值時回傳空字串。 | 出貨/銷貨/訂單來源文件 |
| `records[].workOrderNo` | String | 關聯工單 no；無關聯時回傳空字串。 | `production_data.work_order_no` |
| `records[].orderNo` | String | 關聯客戶訂單或銷售訂單 no；無關聯時回傳空字串。 | 訂購、出貨或 workflow 關聯 |
| `records[].warehouseNo` | String | 目前主要庫存所在倉庫 no；無庫存或非庫存情境時回傳空字串。 | 庫存快照 |
| `records[].warehouseName` | String | 目前主要庫存所在倉庫名稱；無資料時回傳空字串。 | `ship_wh_alias.displayName`、庫存紀錄 fallback |
| `records[].currentQuantity` | Float | 此批號目前庫存數量，取至小數點第 2 位。 | `CWarehouseInventorySnapshotCalculator` |
| `records[].impactedQuantity` | Float | 若以此批號進行召回評估，可能影響的庫存、在製、已出貨數量加總，取至小數點第 2 位。 | 庫存快照、生產投入/產出、出貨/訂單關聯彙總 |
| `records[].impactedCustomerCount` | Integer | 可能受影響的不重複客戶數；無客戶流向時為 0。 | 出貨/訂單關聯彙總 |
| `records[].unit` | Integer | 數量單位 code；前端負責顯示文字。 | `batch_number.unit`、庫存紀錄 fallback |
| `records[].traceStatusCode` | String | 追溯完整性狀態 code；前端負責顯示文字與 tone。 | `complete`、`document_pending`、`broken`、`unknown` |
| `records[].riskLevelCode` | String | 此追溯紀錄風險等級 code。 | `normal`、`attention`、`high_risk` |
| `records[].primaryRiskCode` | String | 此追溯紀錄主要風險 code。 | `normal`、`document_pending`、`document_missing`、`broken_chain`、`expired`、`quality_hold`、`recall_scope`、`unknown` |
| `records[].documentPendingCount` | Integer | 此批號追溯鏈中待補或缺失文件數量。 | 文件完整性彙總 |
| `records[].latestEventTimestamp` | Integer | 此追溯紀錄最近一筆事件時間；無資料時回傳 0。 | `inventory_record`、production、workflow、出貨文件 |
| `total` | Integer | 套用篩選後的紀錄總筆數。 | 查詢結果 |
| `start` | Integer | 本次分頁起點。 | Query parameter |
| `count` | Integer | 本次回傳筆數。 | Query parameter / 實際筆數 |

`records[]` 節點本身不另列說明。API 不回傳前端顯示用繁中文字串，例如 `traceStatusName`、`riskLabel`、`documentStatusName`。

## 5. GET `/api/v2/traceability/batches/{batch_no}/overview`

### 5.1 Success Response Data

```json
{
  "serverTimestamp": "Integer",
  "batch": {
    "batchNo": "String",
    "itemNo": "String",
    "itemName": "String",
    "itemCategory": "Integer",
    "itemSubCategory": "Integer",
    "itemType": "Integer",
    "unit": "Integer",
    "validDate": "Integer",
    "validDays": "Integer",
    "sourceRefCategory": "Integer",
    "sourceNo": "String",
    "traceStatusCode": "String",
    "riskLevelCode": "String",
    "primaryRiskCode": "String"
  },
  "impactSummary": {
    "currentQuantity": "Float",
    "inProductionQuantity": "Float",
    "shippedQuantity": "Float",
    "impactedQuantity": "Float",
    "impactedCustomerCount": "Integer",
    "pendingDocumentCount": "Integer"
  },
  "nodes": [
    {
      "nodeId": "String",
      "nodeTypeCode": "String",
      "refCategory": "Integer",
      "refNo": "String",
      "itemNo": "String",
      "batchNo": "String",
      "quantity": "Float",
      "unit": "Integer",
      "statusCode": "String",
      "riskLevelCode": "String",
      "eventTimestamp": "Integer"
    }
  ],
  "edges": [
    {
      "edgeId": "String",
      "fromNodeId": "String",
      "toNodeId": "String",
      "relationTypeCode": "String",
      "quantity": "Float",
      "unit": "Integer"
    }
  ],
  "timeline": [
    {
      "eventId": "String",
      "eventTimestamp": "Integer",
      "eventTypeCode": "String",
      "refCategory": "Integer",
      "refNo": "String",
      "itemNo": "String",
      "batchNo": "String",
      "quantity": "Float",
      "unit": "Integer",
      "ownerDepartment": "Integer",
      "statusCode": "String"
    }
  ],
  "documents": [
    {
      "documentTypeCode": "String",
      "refCategory": "Integer",
      "refNo": "String",
      "statusCode": "String",
      "ownerDepartment": "Integer",
      "eventTimestamp": "Integer"
    }
  ]
}
```

### 5.2 Field Description

| Field Path | Type | Description | Source / Enum |
|---|---|---|---|
| `serverTimestamp` | Integer | API 回應建立時間，UTC timestamp。 | 系統時間 |
| `batch.batchNo` | String | 批號。 | `batch_number.no` |
| `batch.itemNo` | String | 料品 no。 | `batch_number.item_no` |
| `batch.itemName` | String | 料品名稱；無值時回傳空字串。 | `batch_number.item_name` |
| `batch.itemCategory` | Integer | 料品品項類別 code。 | `batch_number.itemCategory` |
| `batch.itemSubCategory` | Integer | 料品品項子類別 code。 | `batch_number.itemSubCategory` |
| `batch.itemType` | Integer | 料品型態 code。 | `batch_number.itemType` |
| `batch.unit` | Integer | 單位 code；前端負責顯示文字。 | `batch_number.unit` |
| `batch.validDate` | Integer | 批號有效期限 UTC timestamp；無資料時回傳 0。 | `batch_number.validDate` |
| `batch.validDays` | Integer | 批號有效天數；無資料時回傳 0。 | `batch_number.validDays` |
| `batch.sourceRefCategory` | Integer | 批號原始來源單據類別 code。 | `batch_number.refCategory` |
| `batch.sourceNo` | String | 批號原始來源單據 no。 | `batch_number.ref_no` |
| `batch.traceStatusCode` | String | 此批號追溯完整性狀態 code。 | `complete`、`document_pending`、`broken`、`unknown` |
| `batch.riskLevelCode` | String | 此批號追溯風險等級 code。 | `normal`、`attention`、`high_risk` |
| `batch.primaryRiskCode` | String | 此批號主要追溯風險 code。 | `normal`、`document_pending`、`document_missing`、`broken_chain`、`expired`、`quality_hold`、`recall_scope`、`unknown` |
| `impactSummary.currentQuantity` | Float | 此批號目前庫存數量，取至小數點第 2 位。 | 庫存快照 |
| `impactSummary.inProductionQuantity` | Float | 此批號目前可由生產投入/產出資料判定仍在製程中的數量，取至小數點第 2 位。 | `production_data_input`、`production_data_output` |
| `impactSummary.shippedQuantity` | Float | 此批號已出貨或可由訂單/出貨單關聯判定流向客戶的數量，取至小數點第 2 位。 | 出貨/訂單關聯資料 |
| `impactSummary.impactedQuantity` | Float | 召回評估可能影響總量，取至小數點第 2 位。 | `currentQuantity + inProductionQuantity + shippedQuantity` |
| `impactSummary.impactedCustomerCount` | Integer | 可能受影響的不重複客戶數。 | 出貨/訂單關聯資料 |
| `impactSummary.pendingDocumentCount` | Integer | 待補或缺失文件數量。 | `documents[]` |
| `nodes[].nodeId` | String | 追溯鏈節點唯一識別值。 | 後端組合 |
| `nodes[].nodeTypeCode` | String | 節點類型 code；前端負責顯示文字。 | `supplier`、`receipt`、`batch`、`inventory`、`production_input`、`production_output`、`quality`、`shipment`、`customer`、`document` |
| `nodes[].refCategory` | Integer | 節點關聯單據類別 code。 | 來源資料表 |
| `nodes[].refNo` | String | 節點關聯單據 no。 | 來源資料表 |
| `nodes[].itemNo` | String | 節點關聯料品 no；無關聯時回傳空字串。 | 來源資料表 |
| `nodes[].batchNo` | String | 節點關聯批號；無關聯時回傳空字串。 | 來源資料表 |
| `nodes[].quantity` | Float | 節點關聯數量，取至小數點第 2 位。 | 來源資料表 |
| `nodes[].unit` | Integer | 節點關聯單位 code；無單位時回傳 0。 | 來源資料表 |
| `nodes[].statusCode` | String | 節點狀態 code；前端負責顯示文字。 | `complete`、`pending`、`blocked`、`missing`、`unknown` |
| `nodes[].riskLevelCode` | String | 節點風險等級 code。 | `normal`、`attention`、`high_risk` |
| `nodes[].eventTimestamp` | Integer | 節點主要事件時間；無資料時回傳 0。 | 來源資料表 |
| `edges[].edgeId` | String | 追溯鏈連線唯一識別值。 | 後端組合 |
| `edges[].fromNodeId` | String | 連線起點節點 ID。 | `nodes[].nodeId` |
| `edges[].toNodeId` | String | 連線終點節點 ID。 | `nodes[].nodeId` |
| `edges[].relationTypeCode` | String | 節點關係類型 code。 | `source_of`、`received_as`、`stored_in`、`consumed_by`、`produced_as`、`inspected_by`、`shipped_to`、`documented_by` |
| `edges[].quantity` | Float | 關係對應數量，取至小數點第 2 位；無法歸屬時回傳 0。 | 來源資料表 |
| `edges[].unit` | Integer | 關係對應單位 code；無單位時回傳 0。 | 來源資料表 |
| `timeline[].eventId` | String | 時間軸事件唯一識別值。 | 後端組合 |
| `timeline[].eventTimestamp` | Integer | 事件時間 UTC timestamp。 | 來源資料表 |
| `timeline[].eventTypeCode` | String | 事件類型 code；前端負責顯示文字。 | `receipt`、`inventory_in`、`inventory_out`、`production_input`、`production_output`、`quality_hold`、`quality_release`、`shipment`、`document_check`、`task` |
| `timeline[].refCategory` | Integer | 事件關聯單據類別 code。 | 來源資料表 |
| `timeline[].refNo` | String | 事件關聯單據 no。 | 來源資料表 |
| `timeline[].itemNo` | String | 事件關聯料品 no；無資料時回傳空字串。 | 來源資料表 |
| `timeline[].batchNo` | String | 事件關聯批號。 | 來源資料表 |
| `timeline[].quantity` | Float | 事件關聯數量，取至小數點第 2 位。 | 來源資料表 |
| `timeline[].unit` | Integer | 事件關聯單位 code；無資料時回傳 0。 | 來源資料表 |
| `timeline[].ownerDepartment` | Integer | 此事件或下一步處理責任部門 code；無明確資料時回傳 0。 | `workflow_task_state.nextOwnerDepartment` 或來源文件部門 |
| `timeline[].statusCode` | String | 事件狀態 code；前端負責顯示文字。 | `complete`、`pending`、`blocked`、`missing`、`unknown` |
| `documents[].documentTypeCode` | String | 文件類型 code；前端負責顯示文字。 | `coa`、`temperature`、`receipt`、`quality`、`production`、`shipment`、`contract`、`unknown` |
| `documents[].refCategory` | Integer | 文件關聯單據類別 code。 | 來源資料表 |
| `documents[].refNo` | String | 文件關聯單據 no；缺失但可推導應有文件時，可回傳預期單號或空字串。 | 來源資料表 / 規則推導 |
| `documents[].statusCode` | String | 文件狀態 code；前端負責顯示文字。 | `complete`、`pending`、`missing`、`not_required`、`unknown` |
| `documents[].ownerDepartment` | Integer | 文件責任部門 code；無明確資料時回傳 0。 | 文件來源或流程規則 |
| `documents[].eventTimestamp` | Integer | 文件建立、檢查或最近更新時間；無資料時回傳 0。 | 來源資料表 |

`nodes[]`、`edges[]`、`timeline[]`、`documents[]` 節點本身不另列說明。

## 6. Enum Code 建議

| Enum | Values |
|---|---|
| `queryTypeCode` | `batch`、`item`、`order`、`work_order`、`document` |
| `traceDirectionCode` | `upstream`、`downstream`、`both` |
| `traceStatusCode` | `complete`、`document_pending`、`broken`、`unknown` |
| `riskLevelCode` | `normal`、`attention`、`high_risk` |
| `primaryRiskCode` | `normal`、`document_pending`、`document_missing`、`broken_chain`、`expired`、`quality_hold`、`recall_scope`、`unknown` |
| `nodeTypeCode` | `supplier`、`receipt`、`batch`、`inventory`、`production_input`、`production_output`、`quality`、`shipment`、`customer`、`document` |
| `relationTypeCode` | `source_of`、`received_as`、`stored_in`、`consumed_by`、`produced_as`、`inspected_by`、`shipped_to`、`documented_by` |
| `eventTypeCode` | `receipt`、`inventory_in`、`inventory_out`、`production_input`、`production_output`、`quality_hold`、`quality_release`、`shipment`、`document_check`、`task` |
| `documentTypeCode` | `coa`、`temperature`、`receipt`、`quality`、`production`、`shipment`、`contract`、`unknown` |
| `documentStatusCode` | `complete`、`pending`、`missing`、`not_required`、`unknown` |

若工程師確認後進入實作，跨檔共用 enum 應集中定義於 `restserver/package/common/common.py`。

## 7. Database Tables Used

| Table | Purpose |
|---|---|
| `batch_number` | 批號主檔、料品資訊、原始來源單據、效期與單位。 |
| `inventory_record` | 入出庫、庫存異動、批號流向與時間軸事件。 |
| `inventory_item_month_statistic` / `inventory_delta` | 目前庫存快照計算來源；應重用既有 Warehouse 快照邏輯。 |
| `production_data` | 工單、製程與生產事件主資料。 |
| `production_data_input` | 原料/物料/批號投入製程關聯。 |
| `production_data_output` | 在製品/製成品批號產出關聯。 |
| `goods_receipt_note` | 採購進貨來源、供應商與收貨文件關聯。 |
| `warehouse_quality_hold` | 品檢保留、放行或阻塞資訊。 |
| `workflow_task_state` | 未完成任務、下一步負責部門與流程阻塞資訊。 |
| `workflow_task_event` | 任務事件時間軸補充。 |
| `warehouse_inventory_reservation` | 預留量與訂單/工單影響範圍補充。 |

若正式資料庫文件中尚未提供出貨、銷貨或客戶流向資料表的穩定欄位，第一版不得推測不存在的欄位；可先以現有可關聯資料回傳 `customerNo=""`、`customerName=""`、`shippedQuantity=0`，並於工程師提問區標示需補 schema。

## 8. 工程師待確認項目

| 項目 | 需要確認原因 | 工程師回覆 |
|---|---|---|
| 出貨/客戶流向資料來源 | 召回範圍需要判斷已出貨數量與受影響客戶；目前需確認正式 DB schema 中對應的出貨、銷貨或訂單明細資料表與欄位。 | 目前暫不規劃設計"召回"的功能 |
| 文件完整性資料來源 | COA、溫度紀錄、品檢文件、出貨文件是否已有正式文件表或附件表可查詢，會影響 `documents[]` 的實作方式。 | 目前暫不規劃設計"文件完整性"的顯示 |
| `refCategory` code 對照 | `production_data_input/output` 的工單、製程單與出貨單若沒有既有 refCategory code，需要工程師確認正式 code。 | 請具體說明 refCategory 欄位是由哪個 API 的回傳欄位所對應，並說明 refCategory 的用途。 |
| 追溯鏈斷點判斷 | 若缺少必要來源文件或投入/產出關聯時，是否一律判定 `broken`，或分為 `document_pending` 與 `broken` 兩層。 | 追溯流程持續進行至不可再追溯為止，並於此狀態下判定為 broken。 |  

