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
| `/api/v2/bom/dashboard` | GET | BOM 版本摘要、狀態統計、篩選及分頁清單 |
| `/api/v2/bom/{bom_no}/detail` | GET | 指定 BOM 的版本清單與選定版本明細 |

以上 API 均為 read-only。第一版不提供 POST、PUT、DELETE，也不執行 BOM 建立、複製、送簽或核准。

## 3. 共用 Query Parameters / Header

| Parameter / Header | Type | Required | Description |
|---|---|---:|---|
| `keyword` | String | No | BOM no、BOM 簡稱、明細料品 no 或明細料品名稱的關鍵字。 |
| `bomNo` | String | No | 指定 `bom.no`；未提供時查詢全部 BOM。 |
| `version` | Integer | No | 僅適用於 detail API；指定要檢視的 `bom.version`。未提供時取目前有效版本。 |
| `versionStateCode` | String | No | 版本狀態篩選 code；由前端提供 enum code，不傳顯示文字。 |
| `start` | Integer | No | 分頁起點，預設 0。負值視為 0。 |
| `count` | Integer | No | 回傳筆數，預設 50，最大 100。 |
| `x-timezone` | Header String | No | 前端顯示偏好的 IANA timezone；後端仍直接回傳資料庫保存的 UTC timestamp，不以此欄位改寫日期值。 |

## 4. GET `/api/v2/bom/dashboard`

### 4.1 Success Response Data

```json
{
  "serverTimestamp": "Integer",
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
| `summary.bomCount` | Integer | 套用篩選條件後的不重複 BOM 數量。 | `bom.no` |
| `summary.versionCount` | Integer | 套用篩選條件後的 BOM 版本總數。 | `bom.no`、`bom.version` |
| `summary.effectiveVersionCount` | Integer | 依版本狀態判斷為目前有效的 BOM 版本數。 | `bom.date`、`bom.version`、`versionStateCode=effective` |
| `summary.futureVersionCount` | Integer | 生效日期晚於查詢日的 BOM 版本數。 | `bom.date`、`versionStateCode=future` |
| `summary.historicalVersionCount` | Integer | 已被較新版本取代或屬歷史版本的 BOM 版本數。 | `bom.version`、`versionStateCode=historical` |
| `items[].bomNo` | String | 商品配方編號。 | `bom.no` |
| `items[].bomName` | String | 商品配方簡稱；無值時回傳空字串。 | `bom.displayName` |
| `items[].version` | Integer | 商品配方版本。 | `bom.version` |
| `items[].dateTimestamp` | Integer | 商品配方生效日期的 UTC timestamp；`bom.date` 已保存為 UTC timestamp，空值時回傳 0。 | `bom.date` |
| `items[].unit` | Integer | 商品配方單位 code；前端負責多國語系顯示。 | `bom.unit`、Unit enum |
| `items[].weight` | Float | 商品配方基準重量，取至小數點第 2 位；無值時回傳 0。 | `bom.weight` |
| `items[].versionStateCode` | String | 版本狀態 code；前端負責轉換顯示文字。 | `effective`、`future`、`historical`、`unknown` |
| `items[].itemCount` | Integer | 該 BOM 的直接 `bom_item` 明細筆數。 | `bom_item.bom_no` |
| `items[].linkedProductCount` | Integer | 透過 `product_spec.bom_no` 關聯的產品版本數；不使用 `product_spec.bom_version` 篩選。 | `product_spec.bom_no` |
| `total` | Integer | 套用篩選後的 BOM 版本總筆數。 | 查詢結果 |
| `start` | Integer | 本次分頁起點。 | Query parameter |
| `count` | Integer | 本次回傳筆數。 | Query parameter / 實際筆數 |

`items[]` 節點本身不另列說明。API 不回傳 `categoryName`、成本、報價、合約或繁中文字串 fallback。

## 5. GET `/api/v2/bom/{bom_no}/detail`

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
| `bom.dateTimestamp` | Integer | 本次版本生效日期的 UTC timestamp；直接取自已保存為 UTC timestamp 的 `bom.date`，空值回傳 0。 | `bom.date` |
| `bom.unit` | Integer | 本次版本的配方單位 code。 | `bom.unit` |
| `bom.weight` | Float | 本次版本的基準重量，取至小數點第 2 位。 | `bom.weight` |
| `bom.comment` | String | 本次版本備註；無值時回傳空字串。 | `bom.comment` |
| `bom.versionStateCode` | String | 本次版本狀態 code；前端負責顯示文字。 | `effective`、`future`、`historical`、`unknown` |
| `versions[]` | Array | 同一 BOM 的版本摘要，依版本號由新到舊排序；此節點不另列說明。 | `bom.no` |
| `versions[].version` | Integer | 同一 BOM 的版本號。 | `bom.version` |
| `versions[].dateTimestamp` | Integer | 該版本生效日期的 UTC timestamp；直接取自 `bom.date`，空值回傳 0。 | `bom.date` |
| `versions[].versionStateCode` | String | 該版本狀態 code。 | 版本狀態 enum |
| `items[]` | Array | 指定 BOM 版本的直接配方明細；此節點不另列說明。 | `bom_item` |
| `items[].itemNo` | String | 原物料 no。 | `bom_item.item_no` |
| `items[].itemName` | String | 原物料名稱；無值時回傳空字串。 | `bom_item.item_name` |
| `items[].unit` | Integer | 原物料使用單位 code。 | `bom_item.unit` |
| `items[].weight` | Float | 原物料用量或重量，取至小數點第 2 位。 | `bom_item.weight` |
| `linkedProducts[]` | Array | 使用此 BOM 的產品版本關聯；此節點不另列說明。 | `product_spec.bom_no` |
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

## 7. 工程師提問

1. Dashboard 若同一 BOM 編號存在多個版本，`items[]` 是只包含最新版本，還是同時列出多筆版本資料？
2. Detail 若同一 BOM 編號存在多個版本，是否只取回最新版本的原料明細？
3. URL path 是否由 `/api/v2/bom/center/xxx` 改為 `/api/v2/bom/xxx`，以及是否會造成 URL path 重複或衝突？
4. `versionStateCode` 是否可以依 `bom.date` 與同一 `bom.no` 的最高版本計算？
5. `bom_item` 是否只代表原料明細？`bom1`、`bom2`、`inproduct_bom_spec`、`product_bom_spec` 與 `product_bom` 的意涵及關聯為何？
6. `linkedProducts` 是否只依 `product_spec.bom_no` 關聯，暫不考量 `product_spec.bom_version`？
7. `bom.date` 已是 UTC timestamp 時，API 是否仍需依 timezone 轉換？目前程式是否已有相關轉換函式？
8. `count`、`weight`、`unit` 的空值回傳規則與數值精度是否沿用既有 API？

## 8. 工程師回覆與提案結論

| 項目 | 工程師回覆 | 本提案採用的結論 |
|---|---|---|
| 版本清單 | 工程師詢問 Dashboard 是否只回傳最新版本。 | `items[]` 以 BOM 版本為資料列，同一 `bom.no` 的不同版本會各自回傳一筆；如此才能呈現版本總數、未來生效與歷史版本。 |
| Detail 版本 | 工程師詢問 Detail 是否只取最新版本明細。 | Detail 預設取目前有效版本；增加 optional query `version` 後可檢視指定版本。`versions[]` 同時回傳該 BOM 的版本摘要，供前端切換版本後重新查詢。 |
| URL | `/api/v2/bom/center/xxx` 改為 `/api/v2/bom/xxx`，需檢查衝突。 | 已改用 `/api/v2/bom/dashboard` 與 `/api/v2/bom/{bom_no}/detail`。現有正式 BOM API 為 `/api/v1/bom`、`/api/v1/bom/tree`、`/api/v1/bom/process`、`/api/v1/bom/aps`，版本不同，不構成衝突。 |
| 版本狀態 | 可以依 `bom.date` 與版本判斷。 | 保留 `effective`、`future`、`historical`、`unknown`；不把狀態命名為已核准，因 schema 沒有核准欄位。 |
| BOM 原料範圍 | `bom` 為原料配方，不涵蓋物料；`bom_item` 只代表原料明細。 | BOM Center V1 的直接明細只查 `bom_item`；`bom1`、`bom2` 與產品／在製品組裝關聯不在本版樹狀展開。 |
| 產品關聯 | 依 `product_spec.bom_no`，暫不考量 `bom_version`。 | `linkedProducts` 只以 `product_spec.bom_no` 關聯；`product_spec.bom_version` 不作為 V1 過濾條件。 |
| 日期 | `bom.date` 為 UTC timestamp，詢問轉換方式。 | 後端直接回傳 UTC timestamp；前端依使用者 timezone 轉換顯示。`x-timezone` 僅作為前端顯示偏好，不改變 API 日期值。 |
| 數值與空值 | 沿用既有已實作 API。 | 數量／重量取至小數點第 2 位；Integer 空值回傳 0；String 空值回傳空字串；unit 以 code 回傳。若既有 BOM API 實作與此不同，正式化前需先由工程師確認。 |

### 8.1 BOM 相關資料表意涵及關聯

以下是依目前資料庫文件整理的範圍，並非新增資料表或新增欄位：

| 資料表 | 意涵 | 主要關聯 |
|---|---|---|
| `bom` | 原料商品配方的主檔與版本資料，保存 BOM no、版本、生效時間、單位與基準重量。 | `bom.no` 是 `bom_item` 的父級 BOM no；`bom1_number.bom_no` 可關聯至 `bom.no`。 |
| `bom_item` | 原料商品配方的直接原料明細，保存原料 no、名稱、單位與用量／重量。 | `bom_item.bom_no -> bom.no`；`bom_item.item_no -> material.no`。 |
| `bom1_number` | 原料 BOM 的編碼入口，描述以原料或在製品為子項的組裝 BOM。 | `bom1_number.bom_no -> bom.no`；`bom1.parent_no`／`child_id` 使用其編碼形成父子關聯。 |
| `bom1` | 原料／在製品組裝 BOM 的父子明細，`child_category` 區分原料與在製品。 | `bom1.parent_no` 關聯 `bom1_number.no`；子項可指向 `material.no` 或 `bom1_number.no`。 |
| `bom2_number` | 物料 BOM 的編碼入口，供製成品或相關物料的物料組裝規格使用。 | `product_bom_spec.bom2_no -> bom2_number.no`；`bom2` 以 `bom2_number.no` 作為父子組裝關聯。 |
| `bom2` | 物料／膠捲組裝 BOM 的父子明細，保存子項類別、重量、長度或數量。 | `bom2.parent_no` 關聯 `bom2_number.no`；子項可指向物料或膠捲品項。 |
| `inproduct_bom_spec` | 在製品使用的 BOM 規格，`category=1` 指原料 BOM，`category=2` 指物料製成品；以 `bom12_no` 指向 `bom1_number` 或 `bom2_number`。 | `inproduct_no -> inproduct.no`；`item_no`／`item_version` 表示對應原料 BOM 或物料製成品版本。 |
| `product_bom_spec` | 製成品使用的物料 BOM 規格，保存包裝階層、份數、單位與重量。 | `product_no`／`product_version -> product`；`bom2_no -> bom2_number.no`。 |
| `product_spec` | 製成品與原料商品配方的關聯規格，保存製成品版本所使用的 `bom_no`，以及在製品／製成品組裝項目。 | `product_spec.product_no -> product.no`；BOM Center V1 的 `linkedProducts` 以 `product_spec.bom_no` 關聯 `bom.no`。 |
| `product_bom` | 目前 `docs/spec/database/index.md` 未列出此資料表，無法在本版確認其欄位或關聯。 | 不納入 BOM Center V1；若工程師確認它是實際資料表，需先補 DB schema 文件再另行設計 API。 |

因此，BOM Center V1 先呈現「原料商品配方」主檔 (`bom`)、直接原料明細 (`bom_item`) 及產品關聯 (`product_spec`)；在製品／製成品的物料組裝需另定義樹狀展開規則後，才納入後續版本。

## 9. Engineer Review Gate

工程師回覆已納入本版提案。正式 API 文件與後端實作前，仍請確認：

1. `/api/v2/bom/dashboard` 與 `/api/v2/bom/{bom_no}/detail` 的路徑命名。
2. 既有 BOM API 的數值精度與空值行為是否與本提案一致。
3. `bom1`、`bom2` 及 `inproduct_bom_spec`／`product_bom_spec` 後續版本的樹狀展開入口與遞迴規則。
