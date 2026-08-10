# 工程師提問
1. 針對 `/api/v2/bom/center/dashboard`
    - 若同一 bom 編號存在多個版本，items[] 會僅包含 1 筆最新版本的資訊，還是會同時列出多筆不同版本的資料？
2. 針對 `/api/v2/bom/center/{bom_no}/detail`
    - 同一 bom 編號若存在多個版本，是否僅取回最新版本的原料明細?


# BOMCenterScreen API 提案

> Status: Proposal / Pending Engineer Review  
> Screen: `BOMCenterScreen`  
> Route: `/bom`  
> Scope: V1 read-only Core  
> Design basis: `AGENTS.md`、`src/app/bom/page.tsx`、`src/app/rd/page.tsx`、`docs/spec/database/index.md`

## 1. 畫面定位

「BOM 中心」是獨立於「研發成本」的 BOM 版本與配方檢視工作區。第一版只負責讓管理者、研發主管與生管檢視 BOM 版本、有效日期、BOM 明細及產品關聯；不處理成本試算、報價、合約或 BOM 寫入。

`/rd` 的研發成本、成本試算與報價基礎屬於另一個畫面與 API 範圍。本文件不得被解讀為整合型產品研發工作區的替代文件。

## 2. V1 API 清單

| API | Method | 用途 |
|---|---|---|
| `/api/v2/bom/center/dashboard` | GET | BOM 版本摘要、狀態統計、篩選及分頁清單 |
| `/api/v2/bom/center/{bom_no}/detail` | GET | 指定 BOM 的版本清單與選定版本明細 |

以上 API 均為 read-only。第一版不提供 POST、PUT、DELETE，也不執行 BOM 建立、複製、送簽或核准。

## 3. 共用 Query Parameters / Header

| Parameter / Header | Type | Required | Description |
|---|---|---:|---|
| `keyword` | String | No | BOM no、BOM 簡稱、明細料品 no 或明細料品名稱的關鍵字。 |
| `bomNo` | String | No | 指定 `bom.no`；未提供時查詢全部 BOM。 |
| `versionStateCode` | String | No | 版本狀態篩選 code；由前端提供 enum code，不傳顯示文字。 |
| `start` | Integer | No | 分頁起點，預設 0。負值視為 0。 |
| `count` | Integer | No | 回傳筆數，預設 50，最大 100。 |
| `x-timezone` | Header String | Yes | IANA timezone；用於 `dateTimestamp` 的日期轉換。 |

## 4. GET `/api/v2/bom/center/dashboard`

### 4.1 Success Response Data

```json
{
  "serverTimestamp": "Integer",
  "timezone": "String",
  "summary": {
    "bomCount": "Integer",
    "versionCount": "Integer",
    "effectiveVersionCount": "Integer",
    "futureVersionCount": "Integer",
    "historicalVersionCount": "Integer"
  },
  "items": [
    {
      "bomNo": "String",
      "bomName": "String",
      "version": "Integer",
      "dateTimestamp": "Integer",
      "unit": "Integer",
      "weight": "Float",
      "versionStateCode": "String",
      "itemCount": "Integer",
      "linkedProductCount": "Integer"
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
| `timezone` | String | 本次日期欄位使用的 IANA timezone。 | `x-timezone` |
| `summary.bomCount` | Integer | 套用篩選條件後的不重複 BOM 數量。 | `bom.no` |
| `summary.versionCount` | Integer | 套用篩選條件後的 BOM 版本總數。 | `bom.no`、`bom.version` |
| `summary.effectiveVersionCount` | Integer | 依版本狀態判斷為目前有效的 BOM 版本數。 | `bom.date`、`bom.version`、`versionStateCode=effective` |
| `summary.futureVersionCount` | Integer | 生效日期晚於查詢日的 BOM 版本數。 | `bom.date`、`versionStateCode=future` |
| `summary.historicalVersionCount` | Integer | 已被較新版本取代或屬歷史版本的 BOM 版本數。 | `bom.version`、`versionStateCode=historical` |
| `items[].bomNo` | String | 商品配方編號。 | `bom.no` |
| `items[].bomName` | String | 商品配方簡稱；無值時回傳空字串。 | `bom.displayName` |
| `items[].version` | Integer | 商品配方版本。 | `bom.version` |
| `items[].dateTimestamp` | Integer | 商品配方生效日期的 UTC timestamp；資料庫日期為空時回傳 0。 | `bom.date` |
| `items[].unit` | Integer | 商品配方單位 code；前端負責多國語系顯示。 | `bom.unit`、Unit enum |
| `items[].weight` | Float | 商品配方基準重量，取至小數點第 2 位；無值時回傳 0。 | `bom.weight` |
| `items[].versionStateCode` | String | 版本狀態 code；前端負責轉換顯示文字。 | `effective`、`future`、`historical`、`unknown` |
| `items[].itemCount` | Integer | 該 BOM 的直接 `bom_item` 明細筆數。 | `bom_item.bom_no` |
| `items[].linkedProductCount` | Integer | 透過 `product_spec.bom_no` 與 `product_spec.bom_version` 關聯的產品版本數。 | `product_spec` |
| `total` | Integer | 套用篩選後的 BOM 版本總筆數。 | 查詢結果 |
| `start` | Integer | 本次分頁起點。 | Query parameter |
| `count` | Integer | 本次回傳筆數。 | Query parameter / 實際筆數 |

`items[]` 節點本身不另列說明。API 不回傳 `categoryName`、成本、報價、合約或繁中文字串 fallback。

## 5. GET `/api/v2/bom/center/{bom_no}/detail`

### 5.1 Success Response Data

```json
{
  "bom": {
    "bomNo": "String",
    "bomName": "String",
    "version": "Integer",
    "dateTimestamp": "Integer",
    "unit": "Integer",
    "weight": "Float",
    "comment": "String",
    "versionStateCode": "String"
  },
  "versions": [
    {
      "version": "Integer",
      "dateTimestamp": "Integer",
      "versionStateCode": "String"
    }
  ],
  "items": [
    {
      "itemNo": "String",
      "itemName": "String",
      "unit": "Integer",
      "weight": "Float"
    }
  ],
  "linkedProducts": [
    {
      "productNo": "String",
      "productVersion": "Integer",
      "level": "Integer",
      "itemType": "Integer",
      "itemNo": "String",
      "count": "Integer",
      "unit": "Integer",
      "weight": "Float"
    }
  ]
}
```

### 5.2 Field Description

| Field Path | Type | Description | Source / Enum |
|---|---|---|---|
| `bom.bomNo` | String | 商品配方編號。 | `bom.no` |
| `bom.bomName` | String | 商品配方簡稱；無值時回傳空字串。 | `bom.displayName` |
| `bom.version` | Integer | 本次選定的商品配方版本。 | `bom.version` |
| `bom.dateTimestamp` | Integer | 本次版本生效日期的 UTC timestamp；空值回傳 0。 | `bom.date` |
| `bom.unit` | Integer | 本次版本的配方單位 code。 | `bom.unit` |
| `bom.weight` | Float | 本次版本的基準重量，取至小數點第 2 位。 | `bom.weight` |
| `bom.comment` | String | 本次版本備註；無值時回傳空字串。 | `bom.comment` |
| `bom.versionStateCode` | String | 本次版本狀態 code；前端負責顯示文字。 | `effective`、`future`、`historical`、`unknown` |
| `versions[]` | Array | 同一 BOM 的版本摘要，依版本號由新到舊排序；此節點不另列說明。 | `bom.no` |
| `versions[].version` | Integer | 同一 BOM 的版本號。 | `bom.version` |
| `versions[].dateTimestamp` | Integer | 該版本生效日期的 UTC timestamp；空值回傳 0。 | `bom.date` |
| `versions[].versionStateCode` | String | 該版本狀態 code。 | 版本狀態 enum |
| `items[]` | Array | 指定 BOM 版本的直接配方明細；此節點不另列說明。 | `bom_item` |
| `items[].itemNo` | String | 原物料 no。 | `bom_item.item_no` |
| `items[].itemName` | String | 原物料名稱；無值時回傳空字串。 | `bom_item.item_name` |
| `items[].unit` | Integer | 原物料使用單位 code。 | `bom_item.unit` |
| `items[].weight` | Float | 原物料用量或重量，取至小數點第 2 位。 | `bom_item.weight` |
| `linkedProducts[]` | Array | 使用此 BOM 版本的產品版本關聯；此節點不另列說明。 | `product_spec` |
| `linkedProducts[].productNo` | String | 關聯製成品 no。 | `product_spec.product_no` |
| `linkedProducts[].productVersion` | Integer | 關聯製成品版本。 | `product_spec.product_version` |
| `linkedProducts[].level` | Integer | 產品包裝階層 code。 | `product_spec.level` |
| `linkedProducts[].itemType` | Integer | 關聯品項類型 code。 | `product_spec.item_type` |
| `linkedProducts[].itemNo` | String | 關聯在製品或製成品 no。 | `product_spec.item_no` |
| `linkedProducts[].count` | Integer | 產品規格使用的份數。 | `product_spec.count` |
| `linkedProducts[].unit` | Integer | 產品規格重量單位 code。 | `product_spec.unit` |
| `linkedProducts[].weight` | Float | 產品規格內含物重量，取至小數點第 2 位。 | `product_spec.weight` |

## 6. V1 不包含的功能

以下內容屬於 `/rd`「研發成本」或後續版本，不得由 BOM Center API 回傳或推導：

- 成本試算、人工成本、營養標示與毛利。
- 供應商報價、客戶報價及合約。
- 開發需求、打樣、送樣與客戶選樣。
- BOM 新增、修改、版本複製、送簽、核准與作廢。
- 沒有正式資料表支持的 BOM 變更任務與審批狀態。

## 7. Engineer Review Gate

請工程師確認以下事項後，才可建立正式 API 文件與進行後端實作：

1. `/api/v2/bom/center/dashboard` 與 `/api/v2/bom/center/{bom_no}/detail` 的 URL 命名。
    - 工程師回覆: URL path 由 /api/v2/bom/center/xxx 更名為 /api/v2/bom/xxx，並檢視此更名是否會造成 URL path 重複或衝突
2. `versionStateCode` 是否可依 `bom.date` 與同一 `bom.no` 的最高版本計算；若實際業務有正式核准欄位，請指定資料表與欄位。
    - 工程師回覆: 可以
3. `bom_item` 是否只代表原物料明細，以及是否需要把 `bom1`、`bom2` 或 `product_bom_spec` 一併納入 BOM Center 的樹狀展開。
    - 工程師回覆: `bom` 為原料配方不涵蓋物料, 因此`bom_item` 只代表原料明細。
  `bom` 為原料配方，不涵蓋物料，因此 `bom_item` 僅代表原料明細。以下資料表（bom、bom_item、bom1_number、bom1、bom2_number、bom2、inproduct_bom_spec、product_bom_spec、product_bom）涉及原料配方，以及在製品或製成品的原物料組裝。請就你的理解，說明這些資料表所代表的意涵及其相互關聯。
4. `linkedProducts` 是否以 `product_spec` 的 BOM no/version 關聯為準。
    - 工程師回覆: 以 product_spec 的 bom_no 關聯為準，bom_version 暫不列入考量。
5. `date` 的資料庫格式與 timezone 轉換規則。
    - 工程師回覆: date 欄位為 UTC timestamp，建議應如何轉換？目前程式中是否已實作相關的轉換函式？
6. `count`、`weight`、`unit` 的空值回傳規則與數值精度。
    - 工程師回覆: 請依照既有已實作的 API 處理方式進行。
