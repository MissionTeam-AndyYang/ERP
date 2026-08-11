# bom API Group

> Source: `restserver/package/restserver/api/bom_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v1/bom](#get-api-v1-bom) | GET | 查詢BOM | OK | OK |
| [/api/v1/bom/aps](#get-api-v1-bom-aps) | GET | 查詢BOM / APS 資料 | OK | OK |
| [/api/v1/bom/process](#get-api-v1-bom-process) | GET | 查詢BOM / 製程 | OK | OK |
| [/api/v1/bom/tree](#get-api-v1-bom-tree) | GET | 查詢BOM / 樹狀資料 | OK | OK |
| [/api/v2/bom/dashboard](#get-api-v2-bom-dashboard) | GET | 查詢 BOM Center 版本摘要、狀態統計、篩選及分頁清單 | OK | 依 `bom_center_proposal.md` 實作 |
| [/api/v2/bom/{bom_no}/detail](#get-api-v2-bom-bom_no-detail) | GET | 查詢指定 BOM 的版本清單與選定版本明細 | OK | 依 `bom_center_proposal.md` 實作 |

## GET /api/v1/bom

<a id="get-api-v1-bom"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/bom | GET | 查詢BOM |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| count | String | NO | 分頁筆數 |
| start | String | NO | 分頁起始位置 |
| type | String | NO | 類型篩選 |

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "total": "Integer",
    "count": "Integer",
    "results": [
      {
        "id": "String",
        "no": "String",
        "displayName": "String",
        "unit": "String",
        "data": [
          {
            "version": "String",
            "date": "String",
            "unit": "String",
            "weight": "String",
            "creationTime": "String",
            "comment": "String",
            "items": [
              {
                "id": "Integer",
                "no": "String",
                "displayName": "String",
                "version": "Integer",
                "date": "Integer",
                "unit": "Integer",
                "weight": "Float",
                "comment": "String",
                "creationTime": "Integer"
              }
            ],
            "cost": [
              {
                "id": "Integer",
                "no": "String",
                "displayName": "String",
                "version": "Integer",
                "date": "Integer",
                "unit": "Integer",
                "weight": "Float",
                "comment": "String",
                "creationTime": "Integer"
              }
            ]
          }
        ]
      }
    ]
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.total | Integer | 符合條件的總筆數 |  |
| payload.count | Integer | 本次回傳筆數 |  |
| payload.results[].id | String | 資料 ID |  |
| payload.results[].no | String | 資料編號 |  |
| payload.results[].displayName | String | 顯示名稱 |  |
| payload.results[].unit | String | 單位 |  |
| payload.results[].data[].version | String | 版本 |  |
| payload.results[].data[].date | String | 日期時間 |  |
| payload.results[].data[].unit | String | 單位 |  |
| payload.results[].data[].weight | String | 重量 |  |
| payload.results[].data[].creationTime | String | 資料建立時間 |  |
| payload.results[].data[].comment | String | 備註 |  |
| payload.results[].data[].items[].id | Integer | 資料 ID |  |
| payload.results[].data[].items[].no | String | 資料編號 |  |
| payload.results[].data[].items[].displayName | String | 顯示名稱 |  |
| payload.results[].data[].items[].version | Integer | 版本 |  |
| payload.results[].data[].items[].date | Integer | 日期時間 |  |
| payload.results[].data[].items[].unit | Integer | 單位 |  |
| payload.results[].data[].items[].weight | Float | 重量 |  |
| payload.results[].data[].items[].comment | String | 備註 |  |
| payload.results[].data[].items[].creationTime | Integer | 資料建立時間 |  |
| payload.results[].data[].cost[].id | Integer | 資料 ID |  |
| payload.results[].data[].cost[].no | String | 資料編號 |  |
| payload.results[].data[].cost[].displayName | String | 顯示名稱 |  |
| payload.results[].data[].cost[].version | Integer | 版本 |  |
| payload.results[].data[].cost[].date | Integer | 日期時間 |  |
| payload.results[].data[].cost[].unit | Integer | 單位 |  |
| payload.results[].data[].cost[].weight | Float | 重量 |  |
| payload.results[].data[].cost[].comment | String | 備註 |  |
| payload.results[].data[].cost[].creationTime | Integer | 資料建立時間 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：count、start、type
2. 查詢 bom、sample_price 取得BOM資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| bom | 提供BOM主檔、配方或價格資料 |
| sample_price | 提供BOM主檔、配方或價格資料 |

## GET /api/v1/bom/aps

<a id="get-api-v1-bom-aps"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/bom/aps | GET | 查詢BOM / APS 資料 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| order_no | String | NO | 訂單編號 |
| product_no | String | NO | 製成品編號 |

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "results": [
      {
        "id": "Integer",
        "no": "String",
        "creator_no": "String",
        "date": "Integer",
        "ref_no": "String",
        "item_ref_no": "String",
        "item_ref_displayName": "String",
        "item_no": "String",
        "item_name": "String",
        "unit": "Integer",
        "price": "Float",
        "count": "Float",
        "preparedCount": "Float",
        "amount": "Integer",
        "expectedDate": "Integer",
        "address": "String",
        "payment_type": "Integer",
        "payment_source": "Integer",
        "payment_date": "Integer",
        "payment_period": "Integer",
        "comment": "String",
        "creationTime": "Integer"
      }
    ]
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.results[].id | Integer | 資料 ID |  |
| payload.results[].no | String | 資料編號 |  |
| payload.results[].creator_no | String | 製單人員編號 |  |
| payload.results[].date | Integer | 日期時間 |  |
| payload.results[].ref_no | String | 來源單號 |  |
| payload.results[].item_ref_no | String | 交易對象編號 |  |
| payload.results[].item_ref_displayName | String | 交易對象顯示名稱 |  |
| payload.results[].item_no | String | 料品/品項編號 |  |
| payload.results[].item_name | String | 料品/品項名稱 |  |
| payload.results[].unit | Integer | 單位 |  |
| payload.results[].price | Float | 單價 |  |
| payload.results[].count | Float | 本次回傳筆數 |  |
| payload.results[].preparedCount | Float | 已備數量 |  |
| payload.results[].amount | Integer | 金額或需求量 |  |
| payload.results[].expectedDate | Integer | 預計交貨日期 |  |
| payload.results[].address | String | 地址 |  |
| payload.results[].payment_type | Integer | 收付款類別 |  |
| payload.results[].payment_source | Integer | 收付款來源 |  |
| payload.results[].payment_date | Integer | 收付款日期 |  |
| payload.results[].payment_period | Integer | 付款期間 |  |
| payload.results[].comment | String | 備註 |  |
| payload.results[].creationTime | Integer | 資料建立時間 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：order_no、product_no
2. 查詢 product_order 取得BOM / APS 資料資料
3. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| product_order | 提供BOM主檔、配方或價格資料 |

## GET /api/v1/bom/process

<a id="get-api-v1-bom-process"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/bom/process | GET | 查詢BOM / 製程 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| count | String | NO | 分頁筆數 |
| start | String | NO | 分頁起始位置 |

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "total": "Integer",
    "results": [
      {
        "id": "Integer",
        "no": "String",
        "item_no": "String",
        "version": "Integer",
        "date": "Integer"
      }
    ],
    "count": "Integer"
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.total | Integer | 符合條件的總筆數 |  |
| payload.results[].id | Integer | 資料 ID |  |
| payload.results[].no | String | 資料編號 |  |
| payload.results[].item_no | String | 料品/品項編號 |  |
| payload.results[].version | Integer | 版本 |  |
| payload.results[].date | Integer | 日期時間 |  |
| payload.count | Integer | 本次回傳筆數 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：count、start
2. 查詢 product_process 取得BOM / 製程資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| product_process | 提供BOM主檔、配方或價格資料 |

## GET /api/v1/bom/tree

<a id="get-api-v1-bom-tree"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/bom/tree | GET | 查詢BOM / 樹狀資料 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| product_no | String | NO | 製成品編號 |

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "total": "Integer",
    "results": [
      {
        "id": "Integer",
        "no": "String",
        "category": "Integer",
        "name": "String",
        "unitShipping": "Integer",
        "unitWarehouse": "Integer",
        "unitProduct": "Integer",
        "version": "Integer",
        "comment": "String",
        "creationTime": "Integer"
      }
    ]
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.total | Integer | 符合條件的總筆數 |  |
| payload.results[].id | Integer | 資料 ID |  |
| payload.results[].no | String | 資料編號 |  |
| payload.results[].category | Integer | 類別 |  |
| payload.results[].name | String | 名稱 |  |
| payload.results[].unitShipping | Integer | 貨運單位 |  |
| payload.results[].unitWarehouse | Integer | 倉儲單位 |  |
| payload.results[].unitProduct | Integer | 產製單位 |  |
| payload.results[].version | Integer | 版本 |  |
| payload.results[].comment | String | 備註 |  |
| payload.results[].creationTime | Integer | 資料建立時間 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：product_no
2. 查詢 product 取得BOM / 樹狀資料資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| product | 提供BOM主檔、配方或價格資料 |

## GET /api/v2/bom/dashboard

<a id="get-api-v2-bom-dashboard"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v2/bom/dashboard | GET | 查詢 BOM Center 版本摘要、狀態統計、篩選及分頁清單 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |
| x-timezone | 前端顯示偏好的 IANA timezone；後端仍直接回傳資料庫保存的 UTC timestamp |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| date | Integer | NO | 查詢基準 UTC timestamp；未提供時使用系統時間 |
| keyword | String | NO | BOM no、BOM 簡稱、明細料品 no 或明細料品名稱關鍵字 |
| bomNo | String | NO | 指定商品配方編號 |
| versionStateCode | String | NO | 版本狀態 code：effective、future、historical、unknown |
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
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.serverTimestamp | Integer | API 回應建立時間，UTC timestamp |  |
| payload.summary.bomCount | Integer | 套用篩選條件後的不重複 BOM 數量 |  |
| payload.summary.versionCount | Integer | 套用篩選條件後的 BOM 版本總數 |  |
| payload.summary.effectiveVersionCount | Integer | 依版本狀態判斷為目前有效的 BOM 版本數 |  |
| payload.summary.futureVersionCount | Integer | 生效日期晚於查詢日的 BOM 版本數 |  |
| payload.summary.historicalVersionCount | Integer | 已被較新版本取代或屬歷史版本的 BOM 版本數 |  |
| payload.items[].bomNo | String | 商品配方編號 |  |
| payload.items[].bomName | String | 商品配方簡稱；無值時回傳空字串 |  |
| payload.items[].version | Integer | 商品配方版本 |  |
| payload.items[].dateTimestamp | Integer | 商品配方生效日期的 UTC timestamp；空值時回傳 0 |  |
| payload.items[].unit | Integer | 商品配方單位 code；前端負責多國語系顯示 | Unit enum |
| payload.items[].weight | Float | 商品配方基準重量；依既有 BOM API 的 weight 欄位處理方式 |  |
| payload.items[].versionStateCode | String | 版本狀態 code；前端負責轉換顯示文字 | effective / future / historical / unknown |
| payload.items[].itemCount | Integer | 該 BOM 的直接 bom_item 明細筆數 |  |
| payload.items[].linkedProductCount | Integer | 透過 product_spec.bom_no 關聯的產品版本數 |  |
| payload.total | Integer | 套用篩選後的 BOM 版本總筆數 |  |
| payload.start | Integer | 本次分頁起點 |  |
| payload.count | Integer | 本次實際回傳筆數 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Object | 錯誤 payload，通常為空物件 |  |

### Processing Flow

1. 讀取 date、keyword、bomNo、versionStateCode、start、count 與 x-timezone。
2. 查詢 bom，並以 bom.no、bom.displayName、bom_item.item_no、bom_item.item_name 套用關鍵字。
3. 依 bom.date 與同一 bom.no 的有效版本判斷 versionStateCode。
4. 依 versionStateCode 篩選、排序與分頁。
5. 批次查詢 bom_item 與 product_spec，計算 itemCount 與 linkedProductCount。
6. 組成 summary、items、total、start、count 回傳；不回傳成本、報價、合約或繁中文字串 fallback。

### Database Tables Used

| Table | Purpose |
|----------|------|
| bom | 提供商品配方主檔、版本、生效日期、單位、重量與備註 |
| bom_item | 提供商品配方直接原料明細與關鍵字查詢來源 |
| product_spec | 提供使用該 BOM 的產品版本關聯 |

## GET /api/v2/bom/{bom_no}/detail

<a id="get-api-v2-bom-bom_no-detail"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v2/bom/{bom_no}/detail | GET | 查詢指定 BOM 的版本清單與選定版本明細 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |
| x-timezone | 前端顯示偏好的 IANA timezone；後端仍直接回傳資料庫保存的 UTC timestamp |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| date | Integer | NO | 查詢基準 UTC timestamp；未提供時使用系統時間 |
| version | Integer | NO | 指定要檢視的 bom.version；未提供時取目前有效版本 |

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
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
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.bom.bomNo | String | 商品配方編號 |  |
| payload.bom.bomName | String | 商品配方簡稱；無值時回傳空字串 |  |
| payload.bom.version | Integer | 本次選定的商品配方版本 |  |
| payload.bom.dateTimestamp | Integer | 本次版本生效日期的 UTC timestamp；空值時回傳 0 |  |
| payload.bom.unit | Integer | 本次版本的配方單位 code | Unit enum |
| payload.bom.weight | Float | 本次版本的基準重量；依既有 BOM API 的 weight 欄位處理方式 |  |
| payload.bom.comment | String | 本次版本備註；無值時回傳空字串 |  |
| payload.bom.versionStateCode | String | 本次版本狀態 code；前端負責顯示文字 | effective / future / historical / unknown |
| payload.versions[].version | Integer | 同一 BOM 的版本號 |  |
| payload.versions[].dateTimestamp | Integer | 該版本生效日期的 UTC timestamp；空值時回傳 0 |  |
| payload.versions[].versionStateCode | String | 該版本狀態 code | effective / future / historical / unknown |
| payload.items[].itemNo | String | 原物料 no |  |
| payload.items[].itemName | String | 原物料名稱；無值時回傳空字串 |  |
| payload.items[].unit | Integer | 原物料使用單位 code | Unit enum |
| payload.items[].weight | Float | 原物料用量或重量；依既有 BOM API 的 weight 欄位處理方式 |  |
| payload.linkedProducts[].productNo | String | 關聯製成品 no |  |
| payload.linkedProducts[].productVersion | Integer | 關聯製成品版本 |  |
| payload.linkedProducts[].level | Integer | 產品包裝階層 code |  |
| payload.linkedProducts[].itemType | Integer | 關聯品項類型 code |  |
| payload.linkedProducts[].itemNo | String | 關聯在製品或製成品 no |  |
| payload.linkedProducts[].count | Integer | 產品規格使用的份數；依既有 BOM API 的 count 欄位處理方式 |  |
| payload.linkedProducts[].unit | Integer | 產品規格重量單位 code | Unit enum |
| payload.linkedProducts[].weight | Float | 產品規格內含物重量；依既有 BOM API 的 weight 欄位處理方式 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Object | 錯誤 payload，通常為空物件 |  |

### Processing Flow

1. 讀取 path parameter bom_no 與 query parameter date、version。
2. 查詢同一 bom.no 的所有 bom 版本；若不存在則回傳 record not found。
3. 依 bom.date 與同一 bom.no 的有效版本判斷每個版本的 versionStateCode。
4. 若提供 version，取指定 bom.version；未提供時取目前有效版本，若無有效版本則取可判定日期中的最高版本。
5. 查詢 bom_item 取得直接原料明細；BOM Center V1 不遞迴展開 bom1 / bom2。
6. 查詢 product_spec.bom_no 取得產品版本關聯；不使用 product_spec.bom_version 作為篩選條件。
7. 組成 bom、versions、items、linkedProducts 回傳。

### Database Tables Used

| Table | Purpose |
|----------|------|
| bom | 提供指定商品配方的版本、生效日期、單位、重量與備註 |
| bom_item | 提供商品配方直接原料明細 |
| product_spec | 提供使用該 BOM 的產品版本關聯 |
