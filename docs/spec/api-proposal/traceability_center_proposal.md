# 工程師提問V4
1. 針對 /api/v2/trace/batches/{batch_no}/overview 
   - 投產/產製追溯流程僅需該批號的進貨時間、製產時間與銷貨時間，以及各產製階段的投入物與產出物關係。當該批號出現問題時，應能追溯至何時購買、產製何產品以及何時銷貨。請評估 nodes[] 是否可簡化，並確認 nodes[] 與 edges[] 是否可整合為單一結構。

# 工程師提問V3
1. 針對 /api/v2/trace/batches/{batch_no}/overview 
   - 目前資料回傳時間過長且資料量過於龐大，導致效能不足。請評估是否能加速回傳時間，或提出其他可改善效能的方法。
   - 目前僅需列出 原料、在製品與製成品，物料與膠捲暫時不需要。
   - 請補充 nodeTypeCode 各數值的詳細說明。
  
## 工程師回覆V3

| 項目 | 回覆與文件調整 |
|---|---|
| Overview 回傳時間與資料量 | `/api/v2/trace/batches/{batch_no}/overview` 調整為「核心批號追溯圖」，第一版只展開原料、在製品、製成品三類批號節點；不展開物料、膠捲節點，以降低資料量與追溯圖複雜度。 |
| Overview 效能策略 | 後端應先以查詢批號建立 root，再以 `production_data_input` / `production_data_output` 批次查詢上下游批號集合；每一輪只處理尚未拜訪且 itemCategory 屬於原料(1)、在製品(4)、製成品(5) 的批號。不得對每個節點重複查詢完整庫存快照或完整 workflow。 |
| 節點展開限制 | 建議第一版設定防護上限：最大展開層數 5、最大批號節點數 100、最大 edges 數 200；若超過上限，停止繼續展開並保留已確認節點，不建立推測資料。 |
| 物料與膠捲處理 | 若生產投入資料中存在物料(2)或膠捲(3)，第一版 overview 不建立對應 batch / production_input / production_output 節點，也不列入 timeline；未來若前端需要包材追溯，再另行擴充。 |
| 查詢批號本身為物料或膠捲 | 若使用者直接查詢物料或膠捲批號，API 可回傳 `batch` header 與空的 `nodes[]`、`edges[]`、`timeline[]`，並以 `traceStatusCode=unknown`、`riskCode=unknown` 表示第一版未展開此類追溯。 |
| `nodeTypeCode` 說明 | 已於本文件新增「5.6 nodeTypeCode 詳細說明」，逐一說明 `supplier`、`receipt`、`batch`、`inventory`、`production_input`、`production_output`、`quality`、`work_order`、`unknown` 的使用情境與第一版是否會建立。 |

# 工程師提問V2
1. 針對 /api/v2/trace/dashboard，目前資料回傳時間過長，效能不足。請評估是否能加速回傳時間，或提出其他可改善效能的方法。
2. 針對 /api/v2/trace/batches/{batch_no}/overview 
   - 製成品向下追溯：請確認是否能追溯至原物料的投入並產出在製品，形成完整的投產追溯流程。
   - 原料向上追溯：請確認是否能追溯至原料的採購並產出在製品，形成完整的產製追溯流程。
   - 若目前設計並未支援上述追溯方式，請依此設計為主進行修正。
   - 請舉例說明原物料向上追溯與製成品向下追溯時，API 會回傳哪些資料。

## 工程師回覆V2

| 項目 | 回覆與文件調整 |
|---|---|
| `/api/v2/trace/dashboard` 效能 | Dashboard API 調整為「批號追溯清單摘要」用途，不展開完整 nodes / edges / timeline，也不逐筆建立完整追溯圖。後端應採兩階段查詢：先依 `batch_number` 與 query 條件取得候選批號並完成 DB 層排序/分頁，再只針對本頁批號批次查詢庫存摘要、生產投入/產出存在性、品檢保留與最新事件時間。 |
| 庫存計算效能 | Dashboard 不應為所有批號呼叫完整 Warehouse Dashboard；僅需要 `currentQuantity`、主要 `warehouseNo/warehouseName` 與品檢保留訊號時，應以可重用的庫存快照 context / calculator 對本頁批號集合進行 bounded 查詢。若工程師認為目前 `CWarehouseInventoryContextBuilder` 對全量資料成本過高，建議再抽出批號集合專用的 snapshot helper。 |
| `/api/v2/trace/batches/{batch_no}/overview` 追溯方向 | 單批號 overview 的責任是建立「可確認的完整投產追溯圖」，不應只回傳單一方向。即使 `traceDirectionCode` 仍保留作為前端建議視角，overview 仍需在同一張 `nodes[] / edges[]` 中呈現該批號已確認的採購來源、庫存、投入、產出、在製品與製成品關係。 |
| 製成品追溯到原物料 | 支援。當查詢製成品批號時，後端應先以 `production_data_output.batch_number` 找到產出此製成品批號的工單，再以同一工單的 `production_data_input` 找到投入批號；若投入批號為在製品，需繼續往前找出產出該在製品的工單與更上游原物料投入。 |
| 原料追溯到採購與產出 | 支援。當查詢原料批號時，後端應以 `batch_number.refCategory/ref_no` 與 `goods_receipt_note` 或 `inventory_record` 建立採購/進貨/入庫來源節點，再以 `production_data_input.batch_number` 找到使用此原料批號的工單，並以同一工單的 `production_data_output` 找到產出的在製品或製成品批號。 |
| 查詢語意說明 | 工程師提問中的「製成品向下追溯」與「原料向上追溯」本質上是要求 API 能從任一批號切入後，呈現已確認的上下游投產關係；因此文件調整為「overview 預設回傳完整可確認追溯圖」，前端可依 `traceDirectionCode` 或使用者視角決定畫面聚焦方向。 |
| 範例資料 | 已於本文件新增「5.3 追溯範例」說明原料批號與製成品批號查詢時，`batch`、`nodes[]`、`edges[]`、`timeline[]` 會回傳哪些資料。 |

# 工程師提問

1. 請將 URL Path 由 `/api/v2/traceability/xxx` 更名為 `/api/v2/trace/xxx`。
2. 請將 `primaryRiskCode` 更名為 `riskCode`。
3. 請詳細說明「文件完整性」要顯示的內容有哪些。
4. 目前暫時不需提供「文件完整性」與「召回評估」功能，請簡化回傳欄位。
5. 目前以批號為進入點進行追溯：原料批號向下追溯，製成品批號向上追溯；並同步修改查詢條件。
6. 查詢條件暫不開放 `documentStatusCode`、`traceDirectionCode`、`traceStatusCode`、`riskLevelCode`；亦不開放 `period`，僅保留 `startDate` 與 `endDate`。
7. 此追溯功能是否支援單一原料批號可產出多個在製品（如拌料、灌餡等半成品），並由在製品再投入產出多個製成品？
8. 針對 `/api/v2/traceability/dashboard`
   - `records[].queryTypeCode`、`records[].queryValue` 應由前端自行記錄，不應由後端再回傳。
   - 請確認 `records[].supplierNo/supplierName` 與 `records[].customerNo/customerName` 是否會同時存在數值。若會，請具體舉例；若不會，請將欄位簡化為單一組。

## 工程師回覆

| 項目 | 回覆與文件調整 |
|---|---|
| URL Path | 已調整為 `/api/v2/trace/dashboard` 與 `/api/v2/trace/batches/{batch_no}/overview`。 |
| `primaryRiskCode` | 已更名為 `riskCode`，表示此筆追溯資料最主要的風險代碼。 |
| 文件完整性 | 原規劃的文件完整性是指 COA、溫度紀錄、收貨文件、品檢文件、生產文件、出貨文件等文件狀態。但依工程師確認，第一版暫不提供此功能，因此已移除 `documents[]`、`pendingDocumentCount`、`documentPendingCount`、`documentStatusCode` 與相關查詢條件。 |
| 召回評估 | 第一版暫不提供召回範圍與受影響客戶評估，因此已移除 `impactSummary`、`impactedQuantity`、`impactedCustomerCount`、出貨與召回相關欄位。 |
| 追溯入口 | 第一版以批號為唯一主要追溯入口。依工程師提問 V3，overview 只展開原料、在製品與製成品：原料批號向下追溯；製成品批號向上追溯；在製品批號可依資料關聯同時呈現可確認的上下游節點；物料與膠捲暫不展開。 |
| 查詢條件 | 第一版只保留 `keyword`、`batchNo`、`itemCategory`、`itemNo`、`startDate`、`endDate`、`start`、`count` 與 `x-timezone`。不開放文件狀態、追溯方向、追溯狀態、風險等級與 period 快速區間查詢。 |
| 多層批號關係 | 支援。追溯鏈以 `nodes[]` 與 `edges[]` 表示有向無環圖（DAG）或可防循環的關聯圖，可呈現單一原料批號投入多個在製品批號，再由多個在製品批號產出多個製成品批號的情境。 |
| 查詢記錄欄位 | `queryTypeCode` 與 `queryValue` 屬於前端查詢 UI 狀態，不由後端回傳。 |
| 供應商與客戶欄位 | 第一版不在同一筆 dashboard record 同時回傳供應商與客戶兩組欄位，改為單一組 `partnerTypeCode`、`partnerNo`、`partnerName`。`partnerTypeCode` 可為 `supplier`、`customer`、`internal`、`unknown`。 |
| `refCategory` 用途 | `refCategory` 對應 API 回傳中的 `records[].refCategory`、`batch.refCategory`、`nodes[].refCategory`、`timeline[].refCategory`，用途是標示該筆資料關聯的來源單據類別，供後端追溯節點建構與前端未來 drill-down 導向使用。第一版僅回傳資料表已能確認的 code，不推測不存在的 code。 |
| 追溯鏈斷點 | 依工程師回覆，追溯流程持續進行至不可再追溯為止，並於此狀態下判定為 `broken`。 |

# TraceabilityWorkspaceScreen API 提案

> Status: API Proposal / Pending Engineer Review  
> Screen: `TraceabilityWorkspaceScreen`  
> Route: `/traceability`  
> Scope: V1 read-only Core  
> Design basis: `AGENTS.md`、`src/app/traceability/page.tsx`、`docs/spec/api/batches.md`、`docs/spec/database/index.md`

## 1. 畫面定位

「溯源中心」第一版定位為批號追溯 read-only 工作區，用於讓管理者從指定批號快速查看可確認的來源、入庫、庫存、生產投入、產出、品檢與流程節點。單批號 overview 需支援從任一批號切入後，建立已確認的核心投產追溯圖；製成品可回看其上游在製品與原料投入，原料可回看其採購/進貨來源並往下查看產出的在製品或製成品。依工程師提問 V3，第一版 overview 只展開原料(1)、在製品(4)、製成品(5)，物料(2)與膠捲(3)暫不展開。

| 畫面 | 主視角 | 本版邊界 |
|---|---|---|
| `BatchCenterScreen` | 料品 -> 批號 -> 倉庫分布 | 管理目前仍有庫存的批號、可用量、預留量、品檢保留量與效期風險。 |
| `TraceabilityWorkspaceScreen` | 批號 -> 追溯鏈 -> 時間軸 | 以批號為入口檢視可確認的上下游節點、節點關係與追溯斷點。 |
| `WarehouseInventoryMovementLedgerScreen` | 庫存異動流水帳 | 下一版延伸畫面，本次不納入。 |

第一版不提供 POST、PUT、DELETE，不建立召回單、不修改文件狀態、不鎖定庫存、不變更 workflow task。後端只回傳 enum code、數值、時間戳與資料庫欄位；顯示文字與多國語言由前端處理。

## 2. V1 API 清單

| API | Method | 用途 |
|---|---|---|
| `/api/v2/trace/dashboard` | GET | 查詢溯源中心 KPI 與批號追溯清單。 |
| `/api/v2/trace/batches/{batch_no}/overview` | GET | 查詢單一批號的批號資訊、追溯節點、節點關係與時間軸。 |

> 工程師確認前，本文件為 API 提案；確認後才整合至 `docs/spec/api/` 正式 API 文件並進行後端實作。

## 3. 共用 Query Parameters / Header

| Parameter / Header | Type | Required | Description |
|---|---|---:|---|
| `keyword` | String | No | 批號、料號、品名、來源單號、工單號、供應商或客戶關鍵字。 |
| `itemCategory` | Integer | No | 料品品項類別 code；前端負責顯示文字。 |
| `itemNo` | String | No | 料品 no。 |
| `batchNo` | String | No | 批號。若提供，dashboard 以此批號為主要查詢條件。 |
| `startDate` | String | No | 批號建立日期查詢起日，格式 `YYYY-MM-DD`；需與 `endDate` 同時提供。 |
| `endDate` | String | No | 批號建立日期查詢迄日，格式 `YYYY-MM-DD`；需與 `startDate` 同時提供。 |
| `start` | Integer | No | 分頁起點，預設 0；負值視為 0。 |
| `count` | Integer | No | 回傳筆數，預設 50，最大 100。 |
| `x-timezone` | Header String | No | 前端顯示偏好的 IANA timezone；後端不以此改寫資料庫保存的 UTC timestamp。 |

## 4. GET `/api/v2/trace/dashboard`

### 4.1 Success Response Data

```json
{
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
```

### 4.2 Field Description

| Field Path | Type | Description | Source / Enum |
|---|---|---|---|
| `serverTimestamp` | Integer | API 回應建立時間，UTC timestamp。 | 系統時間 |
| `summary.traceableBatchCount` | Integer | 查詢條件內可建立追溯索引的批號數。 | `batch_number`、追溯資料彙總 |
| `summary.completeTraceRate` | Float | `traceStatusCode=complete` 的批號比例，百分比數值取至小數點第 2 位。 | `records[].traceStatusCode` |
| `summary.brokenTraceCount` | Integer | `traceStatusCode=broken` 的追溯紀錄數。 | 追溯鏈判斷結果 |
| `summary.highRiskTraceCount` | Integer | `riskLevelCode=high_risk` 的追溯紀錄數。 | 風險彙總 |
| `records[].traceId` | String | 前端列表用穩定識別值，建議由批號與主要來源單號組成。 | 後端組合 |
| `records[].traceDirectionCode` | String | 後端依批號料品類別推導的追溯方向 code；前端負責顯示文字。 | `upstream`、`downstream`、`both` |
| `records[].itemNo` | String | 料品 no。 | `batch_number.item_no` |
| `records[].itemName` | String | 料品名稱；無值時回傳空字串。 | `batch_number.item_name` |
| `records[].itemCategory` | Integer | 料品品項類別 code。 | `batch_number.itemCategory` |
| `records[].itemSubCategory` | Integer | 料品品項子類別 code。 | `batch_number.itemSubCategory` |
| `records[].itemType` | Integer | 料品型態 code。 | `batch_number.itemType` |
| `records[].batchNo` | String | 批號。 | `batch_number.no` |
| `records[].refCategory` | Integer | 此批號主要來源或關聯單據類別 code，用於追溯節點與前端 drill-down。 | `batch_number.refCategory` 或可確認來源文件 |
| `records[].refNo` | String | 此批號主要來源或關聯單據 no。 | `batch_number.ref_no` 或可確認來源文件 |
| `records[].partnerTypeCode` | String | 此追溯紀錄的主要關聯對象類型 code。 | `supplier`、`customer`、`internal`、`unknown` |
| `records[].partnerNo` | String | 主要關聯對象 no；無值時回傳空字串。 | 供應商、客戶或內部來源資料 |
| `records[].partnerName` | String | 主要關聯對象名稱；無值時回傳空字串。 | 供應商、客戶或內部來源資料 |
| `records[].workOrderNo` | String | 關聯工單 no；無關聯時回傳空字串。 | `production_data` |
| `records[].warehouseNo` | String | 目前主要庫存所在倉庫 no；無庫存或非庫存情境時回傳空字串。 | 庫存快照 |
| `records[].warehouseName` | String | 目前主要庫存所在倉庫名稱；無資料時回傳空字串。 | `ship_wh_alias.displayName`、庫存紀錄 fallback |
| `records[].currentQuantity` | Float | 此批號目前庫存數量，取至小數點第 2 位。 | `CWarehouseInventorySnapshotCalculator` |
| `records[].unit` | Integer | 數量單位 code；前端負責顯示文字。 | `batch_number.unit` |
| `records[].traceStatusCode` | String | 追溯完整性狀態 code；前端負責顯示文字與 tone。 | `complete`、`broken`、`unknown` |
| `records[].riskLevelCode` | String | 此追溯紀錄風險等級 code。 | `normal`、`attention`、`high_risk` |
| `records[].riskCode` | String | 此追溯紀錄主要風險 code。 | `normal`、`broken_chain`、`expired`、`quality_hold`、`unknown` |
| `records[].latestEventTimestamp` | Integer | 此追溯紀錄最近一筆事件時間；無資料時回傳 0。 | `inventory_record`、production、workflow |
| `total` | Integer | 套用篩選後的紀錄總筆數。 | 查詢結果 |
| `start` | Integer | 本次分頁起點。 | Query parameter |
| `count` | Integer | 本次回傳筆數。 | Query parameter / 實際筆數 |

`records[]` 節點本身不另列說明。API 不回傳前端顯示用繁中文字串，例如 `traceStatusName`、`riskLabel`。

## 5. GET `/api/v2/trace/batches/{batch_no}/overview`

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
| `batch.refCategory` | Integer | 批號原始來源單據類別 code，用於追溯節點與前端 drill-down。 | `batch_number.refCategory` |
| `batch.refNo` | String | 批號原始來源單據 no。 | `batch_number.ref_no` |
| `batch.traceDirectionCode` | String | 後端依批號料品類別推導的追溯方向 code。 | `upstream`、`downstream`、`both` |
| `batch.traceStatusCode` | String | 此批號追溯完整性狀態 code。 | `complete`、`broken`、`unknown` |
| `batch.riskLevelCode` | String | 此批號追溯風險等級 code。 | `normal`、`attention`、`high_risk` |
| `batch.riskCode` | String | 此批號主要追溯風險 code。 | `normal`、`broken_chain`、`expired`、`quality_hold`、`unknown` |
| `nodes[].nodeId` | String | 追溯鏈節點唯一識別值。 | 後端組合 |
| `nodes[].nodeTypeCode` | String | 節點類型 code；前端負責顯示文字。第一版詳見「5.6 nodeTypeCode 詳細說明」。 | `supplier`、`receipt`、`batch`、`inventory`、`production_input`、`production_output`、`quality`、`work_order`、`unknown` |
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
| `edges[].relationTypeCode` | String | 節點關係類型 code。 | `source_of`、`received_as`、`stored_in`、`consumed_by`、`produced_as`、`inspected_by` |
| `edges[].quantity` | Float | 關係對應數量，取至小數點第 2 位；無法歸屬時回傳 0。 | 來源資料表 |
| `edges[].unit` | Integer | 關係對應單位 code；無單位時回傳 0。 | 來源資料表 |
| `timeline[].eventId` | String | 時間軸事件唯一識別值。 | 後端組合 |
| `timeline[].eventTimestamp` | Integer | 事件時間 UTC timestamp。 | 來源資料表 |
| `timeline[].eventTypeCode` | String | 事件類型 code；前端負責顯示文字。 | `receipt`、`inventory_in`、`inventory_out`、`production_input`、`production_output`、`quality_hold`、`quality_release`、`task` |
| `timeline[].refCategory` | Integer | 事件關聯單據類別 code。 | 來源資料表 |
| `timeline[].refNo` | String | 事件關聯單據 no。 | 來源資料表 |
| `timeline[].itemNo` | String | 事件關聯料品 no；無資料時回傳空字串。 | 來源資料表 |
| `timeline[].batchNo` | String | 事件關聯批號。 | 來源資料表 |
| `timeline[].quantity` | Float | 事件關聯數量，取至小數點第 2 位。 | 來源資料表 |
| `timeline[].unit` | Integer | 事件關聯單位 code；無資料時回傳 0。 | 來源資料表 |
| `timeline[].ownerDepartment` | Integer | 此事件或下一步處理責任部門 code；無明確資料時回傳 0。 | `workflow_task_state.nextOwnerDepartment` 或來源文件部門 |
| `timeline[].statusCode` | String | 事件狀態 code；前端負責顯示文字。 | `complete`、`pending`、`blocked`、`missing`、`unknown` |

`nodes[]`、`edges[]`、`timeline[]` 節點本身不另列說明。

### 5.3 追溯範例

#### 5.3.1 原物料批號查詢範例

查詢：

```txt
GET /api/v2/trace/batches/RM-BATCH-001/overview
```

假設 `RM-BATCH-001` 是由採購進貨產生，後續投入 `WO-0001` 產出在製品 `WIP-BATCH-001`，再由 `WO-0002` 產出製成品 `FG-BATCH-001`，API 應回傳：

| Payload 區塊 | 回傳內容 |
|---|---|
| `batch` | `batchNo=RM-BATCH-001`、原料品項資料、`refCategory/refNo` 指向採購進貨或入庫來源、`traceDirectionCode=downstream`。 |
| `nodes[]` | 原料批號節點、進貨/入庫或庫存節點、`WO-0001` 工單節點、原料投入節點、`WIP-BATCH-001` 在製品批號節點、`WO-0002` 工單節點、在製品投入節點、`FG-BATCH-001` 製成品批號節點。 |
| `edges[]` | 採購/進貨來源與原料批號的 `received_as/source_of` 關係、原料批號投入工單的 `consumed_by` 關係、工單產出在製品的 `produced_as` 關係、在製品再投入與產出製成品的 `consumed_by/produced_as` 關係。 |
| `timeline[]` | 進貨/入庫事件、原料投入事件、在製品產出事件、在製品投入事件、製成品產出事件、相關品檢或 workflow task 事件。 |

#### 5.3.2 製成品批號查詢範例

查詢：

```txt
GET /api/v2/trace/batches/FG-BATCH-001/overview
```

假設 `FG-BATCH-001` 由 `WO-0002` 產出，投入來源為 `WIP-BATCH-001`，而 `WIP-BATCH-001` 由 `WO-0001` 使用原料批號 `RM-BATCH-001` 產出，API 應回傳：

| Payload 區塊 | 回傳內容 |
|---|---|
| `batch` | `batchNo=FG-BATCH-001`、製成品品項資料、製成品批號來源工單、`traceDirectionCode=upstream`。 |
| `nodes[]` | 製成品批號節點、`WO-0002` 工單節點、在製品投入節點、`WIP-BATCH-001` 在製品批號節點、`WO-0001` 工單節點、原料投入節點、`RM-BATCH-001` 原料批號節點、原料採購/進貨/入庫來源節點。 |
| `edges[]` | 原料批號到原料投入的 `consumed_by` 關係、`WO-0001` 產出在製品的 `produced_as` 關係、在製品投入 `WO-0002` 的 `consumed_by` 關係、`WO-0002` 產出製成品的 `produced_as` 關係。 |
| `timeline[]` | 原料進貨/入庫事件、原料投入事件、在製品產出事件、在製品投入事件、製成品產出事件、相關品檢或 workflow task 事件。 |

> 以上範例僅描述資料結構與節點關係。若某個採購、入庫、投入或產出節點在資料庫中不存在，API 不建立虛構節點；該追溯鏈段停止展開，並依規則反映於 `traceStatusCode` 與 `riskCode`。

### 5.3.3 第一版追溯範圍限制

依工程師提問 V3，單批號 overview 第一版只列出核心投產追溯所需的原料、在製品與製成品：

| itemCategory | 類別 | Overview V1 處理方式 |
|---:|---|---|
| 1 | 原料 | 建立 batch 節點，並可往下追溯至使用此原料的工單、在製品與製成品。 |
| 2 | 物料 | 暫不建立節點、不列入 timeline；未來若需要包材追溯再擴充。 |
| 3 | 膠捲 | 暫不建立節點、不列入 timeline；未來若需要包材追溯再擴充。 |
| 4 | 在製品 | 建立 batch 節點，並可同時呈現上游原料投入與下游製成品產出。 |
| 5 | 製成品 | 建立 batch 節點，並可往上追溯至在製品與原料投入。 |

若查詢批號本身為物料或膠捲，API 不回傳 404，因為批號確實存在；但第一版可回傳 `batch` header，並讓 `nodes[]`、`edges[]`、`timeline[]` 為空陣列，`traceStatusCode=unknown`、`riskCode=unknown`，表示此類批號暫不納入本版追溯圖展開。

## 5.4 Dashboard 效能設計調整

`GET /api/v2/trace/dashboard` 第一版需避免做完整追溯圖展開。建議後端實作以以下流程為準：

1. 以 `batch_number` 作為主查詢來源，先套用 `keyword`、`itemCategory`、`itemNo`、`batchNo`、`startDate`、`endDate`。
2. 在 DB 層完成初步排序與分頁，先取得本頁批號集合。
3. 僅針對本頁批號集合批次查詢：
   - `inventory_record` 最新事件與入出庫存在性。
   - `production_data_input` / `production_data_output` 是否有投入/產出關聯與第一筆工單 no。
   - `warehouse_quality_hold` 是否有品檢保留。
   - 必要的目前庫存摘要。
4. Dashboard 只計算 `records[]` 清單欄位與 `summary`，不建立 `nodes[]`、`edges[]`、`timeline[]`。
5. 若 summary 需要全量統計，應以聚合查詢或 bounded query 完成，不得逐批號呼叫 overview。
6. 若資料量仍大，建議工程師評估新增或確認以下索引：
   - `batch_number(no)`、`batch_number(item_no)`、`batch_number(itemCategory, date)`、`batch_number(refCategory, ref_no)`。
   - `inventory_record(batchNumber, date)`。
   - `production_data_input(batch_number, work_order_no)`。
   - `production_data_output(batch_number, work_order_no)`。
   - `warehouse_quality_hold(batchNumber, date)`。

## 5.5 Overview 效能設計調整

`GET /api/v2/trace/batches/{batch_no}/overview` 第一版需避免一次展開過大的追溯圖。建議後端實作以以下流程為準：

1. 先查詢 root batch，若 root batch 的 `itemCategory` 不屬於原料(1)、在製品(4)、製成品(5)，回傳 root `batch` header 與空 graph，不再展開。
2. 使用 BFS 或受控 DFS 建立追溯圖，每一輪以批號集合批次查詢 `production_data_input` 與 `production_data_output`，避免逐節點 N+1 查詢。
3. 每次取得上下游批號後，先查詢 `batch_number` header，僅保留 `itemCategory in (1, 4, 5)` 的批號；物料(2)、膠捲(3)不建立節點與時間軸事件。
4. 庫存與品檢資料僅針對已納入 graph 的核心批號集合批次查詢，不對被排除的物料與膠捲做庫存快照計算。
5. 建議第一版防護上限：
   - `maxDepth=5`：最多展開 5 層上下游關係。
   - `maxBatchNodeCount=100`：最多建立 100 個 batch 節點。
   - `maxEdgeCount=200`：最多建立 200 條 edge。
6. 若達到防護上限，停止後續展開；已確認的節點與 edge 仍回傳，不建立推測節點。
7. 若資料量仍大，建議工程師確認或新增以下索引：
   - `batch_number(no, itemCategory)`。
   - `production_data_input(batch_number, work_order_no)`。
   - `production_data_output(batch_number, work_order_no)`。
   - `inventory_record(batchNumber, date)`。
   - `warehouse_quality_hold(batchNumber, date)`。

## 5.6 nodeTypeCode 詳細說明

| nodeTypeCode | 節點語意 | 建立時機 | 第一版備註 |
|---|---|---|---|
| `supplier` | 供應商節點，表示原料採購來源的交易對象。 | 當 `goods_receipt_note` 或後續採購資料可明確取得 supplier no/name 時建立。 | 目前若資料來源不足，可先不建立，改以 `receipt` 表示採購/進貨來源。 |
| `receipt` | 進貨/收貨來源節點，表示批號由採購進貨或收貨流程產生。 | 原料批號的 `batch_number.refCategory/ref_no` 可對應 `goods_receipt_note`，或可確認為進貨來源時建立。 | 原料追溯的上游起點之一。 |
| `batch` | 批號節點，表示原料、在製品或製成品批號。 | 批號存在於 `batch_number`，且 `itemCategory` 屬於原料(1)、在製品(4)、製成品(5) 時建立。 | 第一版不建立物料(2)、膠捲(3) batch 節點。 |
| `inventory` | 庫存事件或庫存位置節點，表示批號入庫、出庫或目前庫存所在倉庫。 | 需要呈現批號庫存流向，且 `inventory_record` 有可確認資料時建立。 | 若 overview 資料量過大，可只保留必要入庫/出庫事件於 `timeline[]`，不一定建立獨立 inventory 節點。 |
| `production_input` | 生產投入節點，表示某批號被投入指定工單。 | `production_data_input.batch_number` 命中已納入 graph 的核心批號時建立。 | 物料與膠捲投入第一版不建立此節點。 |
| `production_output` | 生產產出節點，表示指定工單產出某在製品或製成品批號。 | `production_data_output.batch_number` 命中已納入 graph 的核心批號時建立。 | 用於連接工單與產出批號。 |
| `quality` | 品檢節點，表示該批號存在品檢保留、放行或品質阻塞。 | `warehouse_quality_hold` 或後續品檢資料有可確認批號關聯時建立。 | 第一版只回傳 enum code，不回傳繁中文字串。 |
| `work_order` | 工單節點，表示生產投入與產出的共同作業單位。 | 同一 `work_order_no` 同時關聯投入或產出資料時建立。 | 用於串接原料 -> 在製品 -> 製成品的投產鏈。 |
| `unknown` | 未知節點類型，表示資料存在但來源類型無法被正式辨識。 | 僅在資料表有可確認資料但無法歸類至上述類型時使用。 | 應盡量避免；不得用於建立推測節點。 |

## 6. Enum Code 建議

| Enum | Values |
|---|---|
| `traceDirectionCode` | `upstream`、`downstream`、`both` |
| `traceStatusCode` | `complete`、`broken`、`unknown` |
| `riskLevelCode` | `normal`、`attention`、`high_risk` |
| `riskCode` | `normal`、`broken_chain`、`expired`、`quality_hold`、`unknown` |
| `partnerTypeCode` | `supplier`、`customer`、`internal`、`unknown` |
| `nodeTypeCode` | `supplier`、`receipt`、`batch`、`inventory`、`production_input`、`production_output`、`quality`、`work_order`、`unknown` |
| `relationTypeCode` | `source_of`、`received_as`、`stored_in`、`consumed_by`、`produced_as`、`inspected_by` |
| `eventTypeCode` | `receipt`、`inventory_in`、`inventory_out`、`production_input`、`production_output`、`quality_hold`、`quality_release`、`task` |

若工程師確認後進入實作，跨檔共用 enum 應集中定義於 `restserver/package/common/common.py`。

## 7. Database Tables Used

| Table | Purpose |
|---|---|
| `batch_number` | 批號主檔、料品資訊、原始來源單據、效期與單位。 |
| `inventory_record` | 入出庫、庫存異動、批號流向與時間軸事件。 |
| `inventory_item_month_statistic` / `inventory_delta` | 目前庫存快照計算來源；應重用既有 Warehouse 快照邏輯。 |
| `production_data` | 工單、製程與生產事件主資料。 |
| `production_data_input` | 原料、在製品或製成品批號投入製程關聯；第一版 overview 不展開物料與膠捲投入節點。 |
| `production_data_output` | 在製品/製成品批號產出關聯。 |
| `goods_receipt_note` | 採購進貨來源、供應商與收貨文件關聯。 |
| `warehouse_quality_hold` | 品檢保留、放行或阻塞資訊。 |
| `workflow_task_state` | 未完成任務、下一步負責部門與流程阻塞資訊。 |
| `workflow_task_event` | 任務事件時間軸補充。 |
| `warehouse_inventory_reservation` | 預留量與訂單/工單影響範圍補充。 |

若正式資料庫文件中尚未提供出貨、銷貨或客戶流向資料表的穩定欄位，第一版不得推測不存在的欄位；召回評估與客戶流向留待下一版規劃。

## 8. 工程師待確認項目

| 項目 | 需要確認原因 | 工程師回覆 |
|---|---|---|
| 出貨/客戶流向資料來源 | 召回範圍需要判斷已出貨數量與受影響客戶；目前第一版暫不納入。 | 目前暫不規劃設計「召回」的功能。 |
| 文件完整性資料來源 | COA、溫度紀錄、品檢文件、出貨文件若未有正式文件表，第一版不應推測。 | 目前暫不規劃設計「文件完整性」的顯示。 |
| `refCategory` code 對照 | `refCategory` 對應 API 回傳中的來源單據類別，需確認正式 code 對照。 | `refCategory` 對應 `records[].refCategory`、`batch.refCategory`、`nodes[].refCategory`、`timeline[].refCategory`；用途為標示資料來源單據類別與支援後續 drill-down。 |
| 追溯鏈斷點判斷 | 若缺少必要來源文件或投入/產出關聯，需確認是否判定為 `broken`。 | 追溯流程持續進行至不可再追溯為止，並於此狀態下判定為 `broken`。 |
