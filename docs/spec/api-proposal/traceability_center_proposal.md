# 工程師提問V4
1. 針對 /api/v2/trace/batches/{batch_no}/overview 
   - 投產/產製追溯流程僅需該批號的進貨時間、製產時間與銷貨時間，以及各產製階段的投入物與產出物關係。當該批號出現問題時，應能追溯至何時購買、產製何產品以及何時銷貨。請評估 nodes[] 是否可簡化，並確認 nodes[] 與 edges[] 是否可整合為單一結構。

## 工程師回覆V4

| 項目 | 回覆與文件調整 |
|---|---|
| `nodes[]` / `edges[]` 是否可簡化 | 可簡化。依工程師提問 V4，第一版 overview 不再以 graph 結構回傳 `nodes[]` 與 `edges[]`，改為單一流程結構 `traceSteps[]`。每一個 step 直接包含事件時間、來源單據、投入物與產出物，前端不需再自行合併節點與連線。 |
| 投產/產製追溯重點 | Overview 第一版改以「進貨 / 生產 / 銷貨」三類流程步驟為主：`receipt` 表示何時購買或進貨、`production` 表示何時投產與產出何產品、`sale` 表示何時銷貨或出貨。 |
| 投入物與產出物關係 | 已新增 `traceSteps[].inputItems[]` 與 `traceSteps[].outputItems[]`。生產步驟中，投入物與產出物被放在同一筆 step 內，取代原本 `production_input` node、`production_output` node 與 edge 的組合。同一 step 內相同 `itemNo + batchNo + itemCategory + unit` 的投入或產出需加總為單筆。 |
| 銷貨時間資料來源 | 若正式資料庫文件已確認銷貨或出貨資料來源，後端可建立 `stepTypeCode=sale` 的 step；若目前尚無穩定資料表或欄位，`sale` step 不建立，不推測不存在的銷貨資料。 |
| V3 graph 設計處理 | V3 的原始提問與回覆保留作為歷史 review 記錄；但正式 V1 proposal 以 V4 的 `traceSteps[]` 結構為準。`nodeTypeCode` 與 `relationTypeCode` 改列為 V1 不使用、V2 graph 擴充時再評估。 |

# 工程師提問V3
1. 針對 /api/v2/trace/batches/{batch_no}/overview 
   - 目前資料回傳時間過長且資料量過於龐大，導致效能不足。請評估是否能加速回傳時間，或提出其他可改善效能的方法。
   - 目前僅需列出 原料、在製品與製成品，物料與膠捲暫時不需要。
   - 請補充 nodeTypeCode 各數值的詳細說明。
  
## 工程師回覆V3

| 項目 | 回覆與文件調整 |
|---|---|
| Overview 回傳時間與資料量 | `/api/v2/trace/batches/{batch_no}/overview` 依 V3 先限制只處理原料、在製品、製成品三類核心批號；再依 V4 將正式回傳結構簡化為 `traceSteps[]`，降低前端與後端組圖成本。 |
| Overview 效能策略 | 後端應先以查詢批號建立 root，再以 `production_data_input` / `production_data_output` 查詢上下游批號集合；production step 必須以 `work_order_no + process_order_no + group` 限定範圍，並於單次請求內快取已查詢的 batch header、batch input/output、work scope input/output 與 production data，避免重複查詢或誤納入同工單其他製成品資料。 |
| 展開限制 | 建議第一版設定防護上限：最大展開層數 5、最大核心批號數 100、最大 `traceSteps[]` 筆數 150；若超過上限，停止繼續展開並保留已確認流程，不建立推測資料。 |
| 物料與膠捲處理 | 若生產投入資料中存在物料(2)或膠捲(3)，第一版 overview 不列入 `traceSteps[].inputItems[]` / `traceSteps[].outputItems[]`；未來若前端需要包材追溯，再另行擴充。 |
| 查詢批號本身為物料或膠捲 | 若使用者直接查詢物料或膠捲批號，API 可回傳 `batch` header 與空的 `traceSteps[]`，並以 `traceStatusCode=unknown`、`riskCode=unknown` 表示第一版未展開此類追溯。 |
| `nodeTypeCode` 說明 | V3 原規劃的 `nodeTypeCode` 已依 V4 結論改為 V1 不使用；正式提案改以「5.6 traceStepTypeCode 詳細說明」描述 `receipt`、`production`、`sale`。 |

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
| `/api/v2/trace/batches/{batch_no}/overview` 追溯方向 | 單批號 overview 的責任是建立「可確認的完整投產追溯流程」，不應只回傳單一方向。即使 `traceDirectionCode` 仍保留作為前端建議視角，overview 仍需在同一個 `traceSteps[]` 中呈現該批號已確認的進貨、產製與銷貨流程。 |
| 製成品追溯到原物料 | 支援。當查詢製成品批號時，後端應先以 `production_data_output.batch_number` 找到產出此製成品批號的工單與其 `process_order_no/group`，再查詢同一 `work_order_no + process_order_no + group` 的投入批號；若投入批號為在製品，需繼續往前找出產出該在製品的工單與更上游原物料投入。 |
| 原料追溯到採購與產出 | 支援。當查詢原料批號時，後端應以 `batch_number.refCategory/ref_no` 與 `goods_receipt_note` 或 `inventory_record` 建立採購/進貨/入庫來源步驟，再以 `production_data_input.batch_number` 找到使用此原料批號的工單與其 `process_order_no/group`，並只查詢同一 `work_order_no + process_order_no + group` 的在製品或製成品產出批號。 |
| 查詢語意說明 | 工程師提問中的「製成品向下追溯」與「原料向上追溯」本質上是要求 API 能從任一批號切入後，呈現已確認的上下游投產關係；因此文件調整為「overview 預設回傳完整可確認追溯圖」，前端可依 `traceDirectionCode` 或使用者視角決定畫面聚焦方向。 |
| 範例資料 | 已於本文件新增「5.3 追溯範例」說明原料批號與製成品批號查詢時，`batch` 與 `traceSteps[]` 會回傳哪些資料。 |

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
| 追溯入口 | 第一版以批號為唯一主要追溯入口。依工程師提問 V3，overview 只展開原料、在製品與製成品：原料批號向下追溯；製成品批號向上追溯；在製品批號可依資料關聯同時呈現可確認的上下游流程；物料與膠捲暫不展開。 |
| 查詢條件 | 第一版只保留 `keyword`、`batchNo`、`itemCategory`、`itemNo`、`startDate`、`endDate`、`start`、`count` 與 `x-timezone`。不開放文件狀態、追溯方向、追溯狀態、風險等級與 period 快速區間查詢。 |
| 多層批號關係 | 支援。依 V4 結論，追溯流程以 `traceSteps[]` 表示；同一個 `production` step 可包含多筆 `inputItems[]` 與 `outputItems[]`，可呈現單一原料批號投入多個在製品批號，再由多個在製品批號產出多個製成品批號的情境。 |
| 查詢記錄欄位 | `queryTypeCode` 與 `queryValue` 屬於前端查詢 UI 狀態，不由後端回傳。 |
| 供應商與客戶欄位 | 第一版不在同一筆 dashboard record 同時回傳供應商與客戶兩組欄位，改為單一組 `partnerTypeCode`、`partnerNo`、`partnerName`。`partnerTypeCode` 可為 `supplier`、`customer`、`internal`、`unknown`。 |
| `refCategory` 用途 | `refCategory` 對應 API 回傳中的 `records[].refCategory`、`batch.refCategory`、`traceSteps[].refCategory`，用途是標示該筆資料關聯的來源單據類別，供後端追溯流程建構與前端未來 drill-down 導向使用。第一版僅回傳資料表已能確認的 code，不推測不存在的 code。 |
| 追溯鏈斷點 | 依工程師回覆，追溯流程持續進行至不可再追溯為止，並於此狀態下判定為 `broken`。 |

# TraceabilityWorkspaceScreen API 提案

> Status: API Proposal / Pending Engineer Review  
> Screen: `TraceabilityWorkspaceScreen`  
> Route: `/traceability`  
> Scope: V1 read-only Core  
> Design basis: `AGENTS.md`、`src/app/traceability/page.tsx`、`docs/spec/api/batches.md`、`docs/spec/database/index.md`

## 1. 畫面定位

「溯源中心」第一版定位為批號追溯 read-only 工作區，用於讓管理者從指定批號快速查看可確認的進貨時間、產製時間、銷貨時間，以及各產製階段的投入物與產出物關係。單批號 overview 需支援從任一批號切入後，建立已確認的核心投產流程；製成品可回看其上游在製品與原料投入，原料可回看其採購/進貨來源並往下查看產出的在製品或製成品。依工程師提問 V4，正式 V1 proposal 以 `traceSteps[]` 表示流程步驟，不再回傳 `nodes[]` 與 `edges[]`。依工程師提問 V3，第一版 overview 只展開原料(1)、在製品(4)、製成品(5)，物料(2)與膠捲(3)暫不展開。

| 畫面 | 主視角 | 本版邊界 |
|---|---|---|
| `BatchCenterScreen` | 料品 -> 批號 -> 倉庫分布 | 管理目前仍有庫存的批號、可用量、預留量、品檢保留量與效期風險。 |
| `TraceabilityWorkspaceScreen` | 批號 -> 投產流程 -> 進貨/產製/銷貨時間 | 以批號為入口檢視可確認的進貨、產製、銷貨流程，以及投入物與產出物關係。 |
| `WarehouseInventoryMovementLedgerScreen` | 庫存異動流水帳 | 下一版延伸畫面，本次不納入。 |

第一版不提供 POST、PUT、DELETE，不建立召回單、不修改文件狀態、不鎖定庫存、不變更 workflow task。後端只回傳 enum code、數值、時間戳與資料庫欄位；顯示文字與多國語言由前端處理。

## 2. V1 API 清單

| API | Method | 用途 |
|---|---|---|
| `/api/v2/trace/dashboard` | GET | 查詢溯源中心 KPI 與批號追溯清單。 |
| `/api/v2/trace/batches/{batch_no}/overview` | GET | 查詢單一批號的批號資訊與 `traceSteps[]` 投產/產製追溯流程。 |

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
| `records[].refCategory` | Integer | 此批號主要來源或關聯單據類別 code，用於追溯流程與前端 drill-down。 | `batch_number.refCategory` 或可確認來源文件 |
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

`records[]` 陣列本身不另列說明。API 不回傳前端顯示用繁中文字串，例如 `traceStatusName`、`riskLabel`。

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
| `batch.refCategory` | Integer | 批號原始來源單據類別 code，用於追溯流程與前端 drill-down。 | `batch_number.refCategory` |
| `batch.refNo` | String | 批號原始來源單據 no。 | `batch_number.ref_no` |
| `batch.traceDirectionCode` | String | 後端依批號料品類別推導的追溯方向 code。 | `upstream`、`downstream`、`both` |
| `batch.traceStatusCode` | String | 此批號追溯完整性狀態 code。 | `complete`、`broken`、`unknown` |
| `batch.riskLevelCode` | String | 此批號追溯風險等級 code。 | `normal`、`attention`、`high_risk` |
| `batch.riskCode` | String | 此批號主要追溯風險 code。 | `normal`、`broken_chain`、`expired`、`quality_hold`、`unknown` |
| `traceSteps[].stepId` | String | 追溯流程步驟唯一識別值，供前端列表 key 使用。 | 後端組合 |
| `traceSteps[].stepTypeCode` | String | 流程步驟類型 code；用於區分進貨、產製與銷貨。 | `receipt`、`production`、`sale` |
| `traceSteps[].eventTimestamp` | Integer | 此流程步驟發生時間 UTC timestamp；例如進貨時間、生產時間或銷貨時間。 | 來源資料表 |
| `traceSteps[].refCategory` | Integer | 此流程步驟關聯單據類別 code。 | 來源資料表 |
| `traceSteps[].refNo` | String | 此流程步驟關聯單號，例如進貨單號、工單號或銷貨/出貨單號。 | 來源資料表 |
| `traceSteps[].statusCode` | String | 此流程步驟狀態 code；前端負責顯示文字。 | `complete`、`pending`、`blocked`、`missing`、`unknown` |
| `traceSteps[].riskLevelCode` | String | 此流程步驟風險等級 code。 | `normal`、`attention`、`high_risk` |
| `traceSteps[].inputItems[].itemNo` | String | 此步驟投入料品 no；進貨步驟可為空陣列。 | 來源資料表 |
| `traceSteps[].inputItems[].itemName` | String | 此步驟投入料品名稱；無資料時回傳空字串。 | 來源資料表 |
| `traceSteps[].inputItems[].itemCategory` | Integer | 此步驟投入料品品項類別 code。 | `EItemCategory` |
| `traceSteps[].inputItems[].batchNo` | String | 此步驟投入批號；無批號時回傳空字串。 | 來源資料表 |
| `traceSteps[].inputItems[].quantity` | Float | 此步驟投入數量，取至小數點第 2 位；同一 step 內相同料品、批號、品項類別與單位需加總為單筆。 | 來源資料表 |
| `traceSteps[].inputItems[].unit` | Integer | 此步驟投入單位 code。 | 來源資料表 |
| `traceSteps[].outputItems[].itemNo` | String | 此步驟產出或銷貨料品 no。 | 來源資料表 |
| `traceSteps[].outputItems[].itemName` | String | 此步驟產出或銷貨料品名稱；無資料時回傳空字串。 | 來源資料表 |
| `traceSteps[].outputItems[].itemCategory` | Integer | 此步驟產出或銷貨料品品項類別 code。 | `EItemCategory` |
| `traceSteps[].outputItems[].batchNo` | String | 此步驟產出或銷貨批號；無批號時回傳空字串。 | 來源資料表 |
| `traceSteps[].outputItems[].quantity` | Float | 此步驟產出或銷貨數量，取至小數點第 2 位；同一 step 內相同料品、批號、品項類別與單位需加總為單筆。 | 來源資料表 |
| `traceSteps[].outputItems[].unit` | Integer | 此步驟產出或銷貨單位 code。 | 來源資料表 |

`traceSteps[]` 陣列本身不另列說明。API 不回傳前端顯示用繁中文字串，例如 `stepTypeName`、`statusName` 或 `riskLabel`。

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
| `traceSteps[]` | 一筆 `receipt` step 表示原料何時進貨；一筆 `production` step 表示 `WO-0001` 投入 `RM-BATCH-001` 並產出 `WIP-BATCH-001`；另一筆 `production` step 表示 `WO-0002` 投入 `WIP-BATCH-001` 並產出 `FG-BATCH-001`；若銷貨/出貨資料來源已確認，再建立一筆 `sale` step 表示製成品何時銷貨。 |

#### 5.3.2 製成品批號查詢範例

查詢：

```txt
GET /api/v2/trace/batches/FG-BATCH-001/overview
```

假設 `FG-BATCH-001` 由 `WO-0002` 產出，投入來源為 `WIP-BATCH-001`，而 `WIP-BATCH-001` 由 `WO-0001` 使用原料批號 `RM-BATCH-001` 產出，API 應回傳：

| Payload 區塊 | 回傳內容 |
|---|---|
| `batch` | `batchNo=FG-BATCH-001`、製成品品項資料、製成品批號來源工單、`traceDirectionCode=upstream`。 |
| `traceSteps[]` | 依時間排序回傳 `receipt`、`production`、`production`、`sale` 等流程步驟；每筆 `production` step 直接列出加總後的 `inputItems[]` 與 `outputItems[]`，因此可看出製成品由哪個在製品投入、該在製品又由哪些原料投入產出。 |

> 以上範例僅描述資料結構與流程關係。若某個採購、入庫、投入、產出或銷貨步驟在資料庫中不存在，API 不建立虛構 step；該追溯鏈段停止展開，並依規則反映於 `traceStatusCode` 與 `riskCode`。

### 5.3.3 第一版追溯範圍限制

依工程師提問 V3，單批號 overview 第一版只列出核心投產追溯所需的原料、在製品與製成品：

| itemCategory | 類別 | Overview V1 處理方式 |
|---:|---|---|
| 1 | 原料 | 可建立 `receipt` step，並往下追溯至使用此原料的 `production` step、在製品與製成品。 |
| 2 | 物料 | 目前暫不列入 `traceSteps[]` 的 `inputItems[]` 或 `outputItems[]`；未來若需要包材追溯再擴充。 |
| 3 | 膠捲 | 暫不列入 `traceSteps[]`；未來若需要包材追溯再擴充。 |
| 4 | 在製品 | 可同時呈現上游原料投入與下游製成品產出的 `production` step。 |
| 5 | 製成品 | 可往上追溯至在製品與原料投入，若銷貨/出貨資料來源已確認，可往下呈現 `sale` step。 |

若查詢批號本身為物料或膠捲，API 不回傳 404，因為批號確實存在；但第一版可回傳 `batch` header，並讓 `traceSteps[]` 為空陣列，`traceStatusCode=unknown`、`riskCode=unknown`，表示此類批號暫不納入本版追溯流程展開。

## 5.4 Dashboard 效能設計調整

`GET /api/v2/trace/dashboard` 第一版需避免做完整追溯圖展開。建議後端實作以以下流程為準：

1. 以 `batch_number` 作為主查詢來源，先套用 `keyword`、`itemCategory`、`itemNo`、`batchNo`、`startDate`、`endDate`。
2. 在 DB 層完成初步排序與分頁，先取得本頁批號集合。
3. 僅針對本頁批號集合批次查詢：
   - `inventory_record` 最新事件與入出庫存在性。
   - `production_data_input` / `production_data_output` 是否有投入/產出關聯與第一筆工單 no。
   - `warehouse_quality_hold` 是否有品檢保留。
   - 必要的目前庫存摘要。
4. Dashboard 只計算 `records[]` 清單欄位與 `summary`，不建立 `traceSteps[]`。
5. 若 summary 需要全量統計，應以聚合查詢或 bounded query 完成，不得逐批號呼叫 overview。
6. 若資料量仍大，建議工程師評估新增或確認以下索引：
   - `batch_number(no)`、`batch_number(item_no)`、`batch_number(itemCategory, date)`、`batch_number(refCategory, ref_no)`。
   - `inventory_record(batchNumber, date)`。
   - `production_data_input(batch_number, work_order_no)`。
   - `production_data_output(batch_number, work_order_no)`。
   - `warehouse_quality_hold(batchNumber, date)`。

## 5.5 Overview 效能設計調整

`GET /api/v2/trace/batches/{batch_no}/overview` 第一版需避免一次展開過大的追溯流程。建議後端實作以以下流程為準：

1. 先查詢 root batch，若 root batch 的 `itemCategory` 不屬於原料(1)、在製品(4)、製成品(5)，回傳 root `batch` header 與空 `traceSteps[]`，不再展開。
2. 使用 BFS 或受控 DFS 找出需要追溯的核心批號集合。每次以批號找到相關 input/output row 後，必須保留該 row 的 `work_order_no`、`process_order_no` 與 `group`，作為下一步查詢 production step 的範圍。
3. 每次取得上下游批號後，先查詢 `batch_number` header，僅保留 `itemCategory in (1, 4, 5)` 的批號；物料(2)、膠捲(3)不建立 `traceSteps[]` item。
4. 以流程步驟彙整資料：採購/進貨來源建立 `receipt` step；同一 `work_order_no + process_order_no + group` 的投入與產出合併為一筆 `production` step；不得只用 `work_order_no` 合併整張工單；已確認的銷貨/出貨來源建立 `sale` step。
5. `production` step 的 `inputItems[]` 與 `outputItems[]` 需依 `itemNo + batchNo + itemCategory + unit` 加總；同一批號若於同一 production step 拆成多筆投入或產出，回傳時只保留一筆加總後資料。
6. overview 建立過程需使用單次請求內快取，避免同一批號、同一 work scope 或同一 production data 重複查詢。
7. 庫存與品檢資料僅用於判斷 `traceStatusCode`、`riskLevelCode`、`riskCode`，不再作為獨立 step 回傳。
8. 建議第一版防護上限：
   - `maxDepth=5`：最多展開 5 層上下游關係。
   - `maxBatchCount=100`：最多納入 100 個核心批號。
   - `maxTraceStepCount=150`：最多建立 150 筆 `traceSteps[]`。
9. 若達到防護上限，停止後續展開；已確認的 `traceSteps[]` 仍回傳，不建立推測流程。
10. 若資料量仍大，建議工程師確認或新增以下索引：
   - `batch_number(no, itemCategory)`。
   - `production_data_input(batch_number, work_order_no, process_order_no, group)`。
   - `production_data_output(batch_number, work_order_no, process_order_no, group)`。
   - `production_data_input(work_order_no, process_order_no, group)`。
   - `production_data_output(work_order_no, process_order_no, group)`。
   - `inventory_record(batchNumber, date)`。
   - `warehouse_quality_hold(batchNumber, date)`。

## 5.6 traceStepTypeCode 詳細說明

| traceStepTypeCode | 流程語意 | 建立時機 | 第一版備註 |
|---|---|---|---|
| `receipt` | 進貨或收貨步驟，回答「此批號何時購買或進貨」。 | 原料批號的 `batch_number.refCategory/ref_no` 可對應 `goods_receipt_note`，或可確認為採購/進貨來源時建立。 | `inputItems[]` 可為空，`outputItems[]` 放入進貨形成的批號。 |
| `production` | 產製步驟，回答「此製程群組投入哪些批號，產出哪些在製品或製成品」。 | 同一 `work_order_no + process_order_no + group` 可從 `production_data_input` 與 `production_data_output` 取得投入與產出時建立。 | `inputItems[]` 與 `outputItems[]` 必須由同一 work scope 資料組成，避免同工單其他群組或其他製成品混入。 |
| `sale` | 銷貨或出貨步驟，回答「此批號何時銷貨或出貨」。 | 正式資料庫文件確認銷貨/出貨資料來源，且可與批號或製成品建立關聯時建立。 | 目前若資料來源尚未確認，不建立 `sale` step，不推測不存在的銷貨資料。 |

## 6. Enum Code 建議

| Enum | Values |
|---|---|
| `traceDirectionCode` | `upstream`、`downstream`、`both` |
| `traceStatusCode` | `complete`、`broken`、`unknown` |
| `riskLevelCode` | `normal`、`attention`、`high_risk` |
| `riskCode` | `normal`、`broken_chain`、`expired`、`quality_hold`、`unknown` |
| `partnerTypeCode` | `supplier`、`customer`、`internal`、`unknown` |
| `traceStepTypeCode` | `receipt`、`production`、`sale` |

若工程師確認後進入實作，跨檔共用 enum 應集中定義於 `restserver/package/common/common.py`。

## 7. Database Tables Used

| Table | Purpose |
|---|---|
| `batch_number` | 批號主檔、料品資訊、原始來源單據、效期與單位。 |
| `inventory_record` | 入出庫、庫存異動與批號流向補充；第一版 overview 不作為獨立 step 回傳。 |
| `inventory_item_month_statistic` / `inventory_delta` | 目前庫存快照計算來源；應重用既有 Warehouse 快照邏輯。 |
| `production_data` | 工單、製程與生產事件主資料。 |
| `production_data_input` | 原料、在製品或製成品批號投入製程關聯；第一版 overview 不將物料與膠捲投入列入 `traceSteps[]`。 |
| `production_data_output` | 在製品/製成品批號產出關聯。 |
| `goods_receipt_note` | 採購進貨來源、供應商與收貨文件關聯。 |
| `warehouse_quality_hold` | 品檢保留、放行或阻塞資訊；用於風險判斷，不作為獨立 step 回傳。 |

若正式資料庫文件中尚未提供出貨、銷貨或客戶流向資料表的穩定欄位，第一版不得推測不存在的欄位；召回評估與客戶流向留待下一版規劃。

## 8. 工程師待確認項目

| 項目 | 需要確認原因 | 工程師回覆 |
|---|---|---|
| 出貨/客戶流向資料來源 | 召回範圍需要判斷已出貨數量與受影響客戶；目前第一版暫不納入。 | 目前暫不規劃設計「召回」的功能。 |
| 文件完整性資料來源 | COA、溫度紀錄、品檢文件、出貨文件若未有正式文件表，第一版不應推測。 | 目前暫不規劃設計「文件完整性」的顯示。 |
| `refCategory` code 對照 | `refCategory` 對應 API 回傳中的來源單據類別，需確認正式 code 對照。 | `refCategory` 對應 `records[].refCategory`、`batch.refCategory`、`traceSteps[].refCategory`；用途為標示資料來源單據類別與支援後續 drill-down。 |
| 追溯鏈斷點判斷 | 若缺少必要來源文件或投入/產出關聯，需確認是否判定為 `broken`。 | 追溯流程持續進行至不可再追溯為止，並於此狀態下判定為 `broken`。 |
