# trace API Group

> Source: `restserver/package/restserver/api/v2/trace_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v2/trace/dashboard](#get-api-v2-trace-dashboard) | GET | 查詢溯源中心批號追溯摘要、追溯狀態、風險與分頁清單 | OK | 依 `traceability_center_proposal.md` 工程師提問 V2 調整為摘要查詢，不建立完整 overview 流程 |
| [/api/v2/trace/batches/{batch_no}/overview](#get-api-v2-trace-batches-batch_no-overview) | GET | 查詢指定批號的進貨、產製與銷貨追溯流程 | OK | 依 `traceability_center_proposal.md` 工程師提問 V4，overview 改以 `traceSteps[]` 回傳，不再回傳 `nodes[]`、`edges[]`、`timeline[]` |

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
| itemCategory | Integer | NO | 料品品項類別 code；第一版 Dashboard 僅支援原料(1)與製成品(5)，未提供時預設查詢原料與製成品 |
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
2. 以 `batch_number` 作為批號主清單來源，第一版 Dashboard 預設只查詢 `itemCategory in (1, 5)` 的原料與製成品批號；若指定其他 `itemCategory`，回傳空清單，不再掃描非本版畫面所需批號。
3. Dashboard 僅建立批號摘要列，不建立 `traceSteps[]`，也不逐批號呼叫 overview。
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
| /api/v2/trace/batches/{batch_no}/overview | GET | 查詢指定批號的進貨、產製與銷貨追溯流程 |

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
    "traceSteps": [
      {
        "stepId": "String",
        "stepTypeCode": "String",
        "eventTimestamp": "Integer",
        "refCategory": "Integer",
        "refNo": "String",
        "statusCode": "String",
        "riskLevelCode": "String",
        "inputItems": [
          {
            "itemNo": "String",
            "itemName": "String",
            "itemCategory": "Integer",
            "batchNo": "String",
            "quantity": "Float",
            "unit": "Integer"
          }
        ],
        "outputItems": [
          {
            "itemNo": "String",
            "itemName": "String",
            "itemCategory": "Integer",
            "batchNo": "String",
            "quantity": "Float",
            "unit": "Integer"
          }
        ]
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
| payload.batch.traceDirectionCode | String | 後端依查詢批號類別推導的追溯方向 code；原料為 downstream，製成品為 upstream，在製品或未展開類別為 both | upstream、downstream、both |
| payload.batch.traceStatusCode | String | 此批號追溯流程狀態 code | complete、broken、unknown |
| payload.batch.riskLevelCode | String | 此批號追溯風險等級 code | normal、attention、high_risk |
| payload.batch.riskCode | String | 此批號追溯主要風險 code | normal、broken_chain、expired、quality_hold、unknown |
| payload.traceSteps[].stepId | String | 追溯流程步驟識別值，供前端列表 key 使用 |  |
| payload.traceSteps[].stepTypeCode | String | 流程步驟類型 code；用於區分進貨、產製與銷貨 | receipt、production、sale |
| payload.traceSteps[].eventTimestamp | Integer | 此流程步驟發生時間 UTC timestamp；例如進貨時間、生產時間或銷貨時間 |  |
| payload.traceSteps[].refCategory | Integer | 此流程步驟關聯單據類別 code；無資料時回傳 0 |  |
| payload.traceSteps[].refNo | String | 此流程步驟關聯單號，例如進貨單號、工單號或銷貨／出貨單號 |  |
| payload.traceSteps[].statusCode | String | 此流程步驟狀態 code；前端負責顯示文字 | complete、pending、blocked、missing、unknown |
| payload.traceSteps[].riskLevelCode | String | 此流程步驟風險等級 code | normal、attention、high_risk |
| payload.traceSteps[].inputItems[].itemNo | String | 此步驟投入料品 no；進貨步驟可為空陣列；同一 step 內相同料品、批號、品項類別與單位會加總為單筆 |  |
| payload.traceSteps[].inputItems[].itemName | String | 此步驟投入料品名稱；無資料時回傳空字串 |  |
| payload.traceSteps[].inputItems[].itemCategory | Integer | 此步驟投入料品品項類別 code |  |
| payload.traceSteps[].inputItems[].batchNo | String | 此步驟投入批號；無批號時回傳空字串 |  |
| payload.traceSteps[].inputItems[].quantity | Float | 此步驟實際投入數量，取至小數點第 2 位；以 `production_data_input.action=1` 領料數量加總扣除 `action=2` 退料數量加總後回傳，若淨投入量為 0 則不回傳該投入項目 |  |
| payload.traceSteps[].inputItems[].unit | Integer | 此步驟投入單位 code |  |
| payload.traceSteps[].outputItems[].itemNo | String | 此步驟產出或銷貨料品 no；同一 step 內相同料品、批號、品項類別與單位會加總為單筆 |  |
| payload.traceSteps[].outputItems[].itemName | String | 此步驟產出或銷貨料品名稱；無資料時回傳空字串 |  |
| payload.traceSteps[].outputItems[].itemCategory | Integer | 此步驟產出或銷貨料品品項類別 code |  |
| payload.traceSteps[].outputItems[].batchNo | String | 此步驟產出或銷貨批號；無批號時回傳空字串 |  |
| payload.traceSteps[].outputItems[].quantity | Float | 此步驟產出或銷貨數量，取至小數點第 2 位；若同一批號拆成多筆產出資料，後端加總後回傳單筆 |  |
| payload.traceSteps[].outputItems[].unit | Integer | 此步驟產出或銷貨單位 code |  |

### Processing Flow

1. 驗證 `batch_no` 並讀取 `batch_number` 批號主檔。
2. 透過 Warehouse 庫存快照共用邏輯取得指定批號目前庫存與品檢保留數量。
3. 若批號類別不是原料或製成品，回傳批號 header 與空 `traceSteps[]`，並以 `traceStatusCode=unknown`、`riskCode=unknown` 表示本版不展開；在製品第一版不作為查詢起點展開。
4. 以批號為入口受控展開投產流程，僅納入與查詢批號路徑直接相關的原料、在製品與製成品；物料與膠捲不列入 `traceSteps[]`。
5. 依 `batch_number.refCategory/ref_no` 與 `goods_receipt_note` 建立 `receipt` step，表示此批號何時採購或進貨。
6. 若查詢批號為製成品，從 `production_data_output.batch_number` 找出產出此批號的工單，再以同一 `work_order_no` 取得投入批號；每個 production step 的 `outputItems[]` 只保留目前追溯中的製成品或在製品批號，下一層由投入批號繼續往上游展開。
7. 若查詢批號為原料，從 `production_data_input.batch_number` 找出使用此批號的工單，再以同一 `work_order_no` 取得產出批號；每個 production step 的 `inputItems[]` 只保留目前追溯中的原料或在製品批號，`outputItems[]` 顯示同一工單可確認的核心產出。下一層只能由已確認為 `EItemCategory.INPRODUCT` 的 output 批號繼續往下游展開；若直接產出是製成品、未知類別或其他非在製品資料，該 output 只列為目前 step 的終點，不再放回 trace queue 展開下一層 production step。
8. `process_order_no` 目前尚未建立穩定關聯，`group` 資料也尚未完整，因此第一版 production step 暫不以這兩個欄位分組或過濾。若同一 `work_order_no` 同時混有多組尚未透過資料欄位可靠區隔的投入與產出，需待未來資料治理完成後再提升至更細粒度分組。
9. 建立 production step 時，以目前追溯批號過濾顯示重點：製成品 upstream 保留 focus output、原料 downstream 保留 focus input；不得讓製成品 output 再被放回 downstream queue 造成旁支展開。
10. `receipt`、`production`、`sale` 均維持於 `traceSteps[]`，前端依 `stepTypeCode` 判斷流程類型；第一版不另拆獨立 receipt/sale 陣列。
11. `inputItems[]` 與 `outputItems[]` 需依 `itemNo + batchNo + itemCategory + unit` 彙整。`inputItems[].quantity` 需依 `production_data_input.action` 計算淨投入量：`action=1` 領料為正數、`action=2` 退料為負數；淨投入量為 0 的投入項目不回傳，若該投入批號為目前追溯路徑的 focus input，該 production step 不建立，也不加入下一層 trace queue；`outputItems[].quantity` 依 `production_data_output.count` 加總。`production_data_input.category` 使用 `EItemCategory`；`production_data_output.category` 不可直接與 `EItemCategory` 比對。後端回傳 `traceSteps[].outputItems[].itemCategory` 或判斷 output 是否為 downstream 終點時，需優先以 `production_data_output.batch_number` 對應的 `batch_number.itemCategory` 作為 API 統一使用的 `EItemCategory`，批號主檔缺漏時才用 `EOutputCategory` fallback。
12. 若同一 `work_order_no` 因多個追溯批號被重複命中同一 `stepId`，需將新的 focus `inputItems[]` / `outputItems[]` 合併至既有 step；相同 `itemNo + batchNo + itemCategory + unit` 的既有 output 不可重複加總。
13. overview 建立過程需使用單次請求內的 batch header、batch input、batch output、work order input/output 與 production data 快取，避免同一批號或同一工單重複查詢。
14. 使用 visited batch 集合、最大展開層數、最大批號數與最大 step 數避免循環或過大 payload；遇到缺漏來源時停止展開，不推測不存在的流程。
15. 若正式資料庫文件尚未提供穩定銷貨或出貨批號來源，本版不建立 `sale` step。
16. 依批號效期、品檢保留與追溯流程完整性判斷 `traceStatusCode`、`riskLevelCode` 與 `riskCode`。
17. 回傳批號資訊與 `traceSteps[]`。

### Database Tables Used

| Table | Purpose |
|----------|------|
| batch_number | 批號主檔、料品資訊、來源單據與效期 |
| inventory_record | 批號入出庫與庫存補充；overview 不作為獨立 step 回傳 |
| inventory_item_month_statistic | 由 Warehouse 庫存快照共用邏輯使用的批號庫存月結基準 |
| inventory_delta | 由 Warehouse 庫存快照共用邏輯使用的批號庫存異動補算 |
| production_data | 工單與產製資料主檔 |
| production_data_input | 批號作為生產投入的追溯來源 |
| production_data_output | 批號作為生產產出的追溯來源 |
| warehouse_quality_hold | 品檢保留與品檢風險；overview 不作為獨立 step 回傳 |
