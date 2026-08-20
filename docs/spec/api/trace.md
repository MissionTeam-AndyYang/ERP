# trace API Group

> Source: `restserver/package/restserver/api/v2/trace_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v2/trace/dashboard](#get-api-v2-trace-dashboard) | GET | 查詢溯源中心批號追溯摘要、追溯狀態、風險與分頁清單 | OK | 依 `traceability_center_proposal.md` 工程師提問 V2 調整為摘要查詢，不建立完整 graph |
| [/api/v2/trace/batches/{batch_no}/overview](#get-api-v2-trace-batches-batch_no-overview) | GET | 查詢指定批號的追溯鏈節點、節點關係與時間軸 | OK | 依 `traceability_center_proposal.md` 工程師提問 V2 支援完整上下游投產追溯 |

## GET /api/v2/trace/dashboard

<a id="get-api-v2-trace-dashboard"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v2/trace/dashboard | GET | 查詢溯源中心批號追溯摘要、追溯狀態、風險與分頁清單 |

### Request Header

| Header | Description |
|----------|----------|
| x-timezone | 前端顯示偏好的 IANA timezone；後端用於解析 `startDate` / `endDate` |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| keyword | String | NO | 批號、料號、料品名稱、來源單號、工單號、倉庫 no 或倉庫名稱關鍵字 |
| itemCategory | Integer | NO | 料品品項類別 code |
| itemNo | String | NO | 料品 no |
| batchNo | String | NO | 批號 |
| startDate | String | NO | 批號建立日期查詢起日，格式 `YYYY-MM-DD`；需與 `endDate` 同時提供 |
| endDate | String | NO | 批號建立日期查詢迄日，格式 `YYYY-MM-DD`；需與 `startDate` 同時提供 |
| start | Integer | NO | 分頁起點，預設 0 |
| count | Integer | NO | 回傳筆數，預設 50，最大 100 |

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "serverTimestamp": "Integer",
    "summary": {
      "traceableBatchCount": "Integer",
      "completeTraceRate": "Float",
      "brokenTraceCount": "Integer",
      "highRiskTraceCount": "Integer"
    },
    "records": [
      {
        "traceId": "String",
        "traceDirectionCode": "String",
        "itemNo": "String",
        "itemName": "String",
        "itemCategory": "Integer",
        "itemSubCategory": "Integer",
        "itemType": "Integer",
        "batchNo": "String",
        "refCategory": "Integer",
        "refNo": "String",
        "partnerTypeCode": "String",
        "partnerNo": "String",
        "partnerName": "String",
        "workOrderNo": "String",
        "warehouseNo": "String",
        "warehouseName": "String",
        "currentQuantity": "Float",
        "unit": "Integer",
        "traceStatusCode": "String",
        "riskLevelCode": "String",
        "riskCode": "String",
        "latestEventTimestamp": "Integer"
      }
    ],
    "total": "Integer",
    "start": "Integer",
    "count": "Integer"
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| payload.serverTimestamp | Integer | API 回應建立時間，UTC timestamp |  |
| payload.summary.traceableBatchCount | Integer | 套用篩選後 `traceStatusCode=complete` 的批號數 |  |
| payload.summary.completeTraceRate | Float | 可追溯批號比例，單位為百分比，取至小數點第 2 位 |  |
| payload.summary.brokenTraceCount | Integer | 套用篩選後 `traceStatusCode=broken` 的批號數 |  |
| payload.summary.highRiskTraceCount | Integer | 套用篩選後 `riskLevelCode=high_risk` 的批號數 |  |
| payload.records[].traceId | String | 前端清單列使用的追溯識別值，格式為 `TRACE-{batchNo}` |  |
| payload.records[].traceDirectionCode | String | 建議追溯方向 code，由料品品項類別判斷 | upstream、downstream、both |
| payload.records[].itemNo | String | 批號對應料品 no |  |
| payload.records[].itemName | String | 批號對應料品名稱 |  |
| payload.records[].itemCategory | Integer | 料品品項類別 code |  |
| payload.records[].itemSubCategory | Integer | 料品品項子類別 code |  |
| payload.records[].itemType | Integer | 品項型態 code |  |
| payload.records[].batchNo | String | 批號 |  |
| payload.records[].refCategory | Integer | 批號建立時的來源單據類別，固定以 `batch_number.refCategory` 為準 |  |
| payload.records[].refNo | String | 批號建立時的來源單號，固定以 `batch_number.ref_no` 為準 |  |
| payload.records[].partnerTypeCode | String | 批號來源對象類型 code；無法由現有資料判斷時回傳 `unknown` | supplier、customer、internal、unknown |
| payload.records[].partnerNo | String | 來源對象 no；目前資料表未提供穩定對應時回傳空字串 |  |
| payload.records[].partnerName | String | 來源對象名稱；目前資料表未提供穩定對應時回傳空字串 |  |
| payload.records[].workOrderNo | String | 此批號已知關聯的第一筆工單 no；無資料時回傳空字串 |  |
| payload.records[].warehouseNo | String | 此批號目前庫存所在的主要倉庫 no；無目前庫存時回傳空字串 |  |
| payload.records[].warehouseName | String | 此批號目前庫存所在的主要倉庫名稱；無目前庫存時回傳空字串 |  |
| payload.records[].currentQuantity | Float | 此批號目前庫存數量總和，取至小數點第 2 位；無目前庫存時回傳 0 |  |
| payload.records[].unit | Integer | 批號或庫存單位 code；前端負責顯示文字與多國語言轉換 |  |
| payload.records[].traceStatusCode | String | 追溯鏈狀態 code | complete、broken、unknown |
| payload.records[].riskLevelCode | String | 追溯風險等級 code | normal、attention、high_risk |
| payload.records[].riskCode | String | 追溯主要風險 code | normal、broken_chain、expired、quality_hold、unknown |
| payload.records[].latestEventTimestamp | Integer | 此批號已知來源、庫存、workflow 或批號建立資料中的最新事件時間 |  |
| payload.total | Integer | 套用篩選後批號追溯列總數 |  |
| payload.start | Integer | 本次分頁起點 |  |
| payload.count | Integer | 本次回傳筆數 |  |

### Processing Flow

1. 讀取查詢條件並轉換為後端型別。
2. 以 `batch_number` 作為批號主清單來源，套用料品類別、料號、批號、關鍵字與日期區間條件。
3. Dashboard 僅建立批號摘要列，不建立 `nodes[]`、`edges[]`、`timeline[]`，也不逐批號呼叫 overview。
4. 以批號集合限定的庫存摘要查詢取得目前庫存、主要倉庫、品檢保留與最新庫存事件；不重新建立第二套月結/delta 庫存演算法。
5. 批次查詢批號關聯的生產投入、產出生產資料、品檢保留與 workflow event 最新時間。
6. 依料品類別判斷建議追溯方向：原料、物料、膠捲預設 downstream；製成品預設 upstream；在製品或其他預設 both。
7. 依已確認來源、庫存、生產投入、產出與品檢資料判斷追溯狀態與風險 code；不推測不存在的節點或關係。
8. 依批號建立時間排序、套用分頁並回傳 payload。

### Database Tables Used

| Table | Purpose |
|----------|------|
| batch_number | 批號主檔、料品資訊、來源單據與效期 |
| inventory_record | 批號入出庫事件與最新庫存事件時間 |
| inventory_item_month_statistic | 由 Warehouse 庫存快照共用邏輯使用的批號庫存月結基準 |
| inventory_delta | 由 Warehouse 庫存快照共用邏輯使用的批號庫存異動補算 |
| production_data | 工單與產製資料主檔 |
| production_data_input | 批號作為生產投入的追溯來源 |
| production_data_output | 批號作為生產產出的追溯來源 |
| warehouse_quality_hold | 品檢保留與品檢風險 |
| workflow_task_state | 批號相關任務狀態 |
| workflow_task_event | 批號相關 workflow 最新事件 |

## GET /api/v2/trace/batches/{batch_no}/overview

<a id="get-api-v2-trace-batches-batch_no-overview"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v2/trace/batches/{batch_no}/overview | GET | 查詢指定批號的追溯鏈節點、節點關係與時間軸 |

### Request Header

| Header | Description |
|----------|----------|
| x-timezone | 前端顯示偏好的 IANA timezone |

### Query Parameters

None

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
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
      "refCategory": "Integer",
      "refNo": "String",
      "traceDirectionCode": "String",
      "traceStatusCode": "String",
      "riskLevelCode": "String",
      "riskCode": "String"
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
    ]
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| payload.serverTimestamp | Integer | API 回應建立時間，UTC timestamp |  |
| payload.batch.batchNo | String | 查詢批號 |  |
| payload.batch.itemNo | String | 批號對應料品 no |  |
| payload.batch.itemName | String | 批號對應料品名稱 |  |
| payload.batch.itemCategory | Integer | 料品品項類別 code |  |
| payload.batch.itemSubCategory | Integer | 料品品項子類別 code |  |
| payload.batch.itemType | Integer | 品項型態 code |  |
| payload.batch.unit | Integer | 批號單位 code |  |
| payload.batch.validDate | Integer | 批號有效期限 UTC timestamp |  |
| payload.batch.validDays | Integer | 批號有效天數 |  |
| payload.batch.refCategory | Integer | 批號建立時的來源單據類別 |  |
| payload.batch.refNo | String | 批號建立時的來源單號 |  |
| payload.batch.traceDirectionCode | String | 建議追溯方向 code；此欄位供前端聚焦視角使用，不限制 overview 回傳完整上下游投產關係 | upstream、downstream、both |
| payload.batch.traceStatusCode | String | 此批號追溯鏈狀態 code | complete、broken、unknown |
| payload.batch.riskLevelCode | String | 此批號追溯風險等級 code | normal、attention、high_risk |
| payload.batch.riskCode | String | 此批號追溯主要風險 code | normal、broken_chain、expired、quality_hold、unknown |
| payload.nodes[].nodeId | String | 追溯節點識別值，供前端畫鏈路使用 |  |
| payload.nodes[].nodeTypeCode | String | 追溯節點類型 code；採購/進貨來源以 `receipt` 節點表示，內部產製來源以 `work_order`、`production_input`、`production_output` 節點表示 | supplier、receipt、batch、inventory、production_input、production_output、quality、work_order、unknown |
| payload.nodes[].refCategory | Integer | 節點來源單據類別；無資料時回傳 0 |  |
| payload.nodes[].refNo | String | 節點來源單號、工單號或關聯單號；無資料時回傳空字串 |  |
| payload.nodes[].itemNo | String | 節點對應料品 no；無資料時回傳空字串 |  |
| payload.nodes[].batchNo | String | 節點對應批號；無資料時回傳空字串 |  |
| payload.nodes[].quantity | Float | 節點對應數量，取至小數點第 2 位 |  |
| payload.nodes[].unit | Integer | 節點對應單位 code |  |
| payload.nodes[].statusCode | String | 節點狀態 code；無法由現有資料判斷時回傳 `unknown` |  |
| payload.nodes[].riskLevelCode | String | 節點風險等級 code | normal、attention、high_risk |
| payload.nodes[].eventTimestamp | Integer | 節點發生時間或建立時間 UTC timestamp；無資料時回傳 0 |  |
| payload.edges[].edgeId | String | 追溯關係識別值，供前端畫線使用 |  |
| payload.edges[].fromNodeId | String | 來源節點 id |  |
| payload.edges[].toNodeId | String | 目的節點 id |  |
| payload.edges[].relationTypeCode | String | 追溯節點關係 code | source_of、received_as、stored_in、consumed_by、produced_as、inspected_by |
| payload.edges[].quantity | Float | 此關係對應數量，取至小數點第 2 位；無明確數量時回傳 0 |  |
| payload.edges[].unit | Integer | 此關係對應單位 code；無明確單位時回傳 0 |  |
| payload.timeline[].eventId | String | 時間軸事件識別值 |  |
| payload.timeline[].eventTimestamp | Integer | 事件發生時間 UTC timestamp |  |
| payload.timeline[].eventTypeCode | String | 事件類型 code | receipt、inventory_in、inventory_out、production_input、production_output、quality_hold、quality_release、task |
| payload.timeline[].refCategory | Integer | 事件來源單據類別；無資料時回傳 0 |  |
| payload.timeline[].refNo | String | 事件來源單號、工單號或任務關聯單號；無資料時回傳空字串 |  |
| payload.timeline[].itemNo | String | 事件對應料品 no；無資料時回傳空字串 |  |
| payload.timeline[].batchNo | String | 事件對應批號；無資料時回傳空字串 |  |
| payload.timeline[].quantity | Float | 事件對應數量，取至小數點第 2 位 |  |
| payload.timeline[].unit | Integer | 事件對應單位 code |  |
| payload.timeline[].ownerDepartment | Integer | workflow 任務下一步負責部門 code；非任務事件回傳 0 |  |
| payload.timeline[].statusCode | String | 事件狀態 code；無法由現有資料判斷時回傳 `unknown` |  |

### Processing Flow

1. 驗證 `batch_no` 並讀取 `batch_number` 批號主檔。
2. 透過 Warehouse 庫存快照共用邏輯取得指定批號目前庫存與品檢保留數量。
3. 建立批號根節點，並依已確認資料查詢採購/進貨來源、庫存事件、品檢保留、生產投入、生產產出與 workflow 任務。
4. 以批號為節點邊界建立完整可確認投產追溯圖：查詢製成品批號時，可由產出工單往上游展開至在製品與原物料投入；查詢原料批號時，可由採購/進貨來源往下游展開至使用此原料的工單與產出的在製品/製成品。
5. 使用 visited batch 集合避免循環追溯；遇到缺漏來源時停止展開，不推測不存在的節點。
6. 依批號效期、品檢保留與追溯鏈完整性判斷 `traceStatusCode`、`riskLevelCode` 與 `riskCode`。
7. 回傳批號資訊、nodes、edges 與 timeline。

### Database Tables Used

| Table | Purpose |
|----------|------|
| batch_number | 批號主檔、料品資訊、來源單據與效期 |
| inventory_record | 批號入出庫事件與時間軸 |
| inventory_item_month_statistic | 由 Warehouse 庫存快照共用邏輯使用的批號庫存月結基準 |
| inventory_delta | 由 Warehouse 庫存快照共用邏輯使用的批號庫存異動補算 |
| production_data | 工單與產製資料主檔 |
| production_data_input | 批號作為生產投入的追溯節點 |
| production_data_output | 批號作為生產產出的追溯節點 |
| warehouse_quality_hold | 品檢保留節點與品檢時間軸 |
| workflow_task_state | 批號相關任務時間軸與負責部門 |
| workflow_task_event | 批號相關 workflow 最新事件 |
