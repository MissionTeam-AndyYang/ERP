# shipwarehouse API Group

> Source: `restserver/package/restserver/api/shipwarehouse_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v1/shipwarehouse](#get-api-v1-shipwarehouse) | GET | 查詢物流倉儲 | OK | OK |
| [/api/v1/shipwarehouse](#post-api-v1-shipwarehouse) | POST | 新增物流倉儲 | Need Review | Executor method is not present in code. |
| [/api/v1/shipwarehouse](#put-api-v1-shipwarehouse) | PUT | 更新物流倉儲 | Need Review | Executor method is not present in code. |
| [/api/v1/shipwarehouse](#delete-api-v1-shipwarehouse) | DELETE | 刪除物流倉儲 | Need Review | Executor method is not present in code. |
| [/api/v1/shipwarehouse/contract](#get-api-v1-shipwarehouse-contract) | GET | 查詢物流倉儲 / 合約 | OK | OK |
| [/api/v1/shipwarehouse/contract](#post-api-v1-shipwarehouse-contract) | POST | 新增物流倉儲 / 合約 | Need Review | Executor method is not present in code. |
| [/api/v1/shipwarehouse/contract](#put-api-v1-shipwarehouse-contract) | PUT | 更新物流倉儲 / 合約 | Need Review | Executor method is not present in code. |
| [/api/v1/shipwarehouse/contract](#delete-api-v1-shipwarehouse-contract) | DELETE | 刪除物流倉儲 / 合約 | Need Review | Executor method is not present in code. |
| [/api/v1/shipwarehouse/shiparap](#get-api-v1-shipwarehouse-shiparap) | GET | 查詢物流倉儲 / 物流應收應付 | OK | OK |
| [/api/v1/shipwarehouse/shippayment](#get-api-v1-shipwarehouse-shippayment) | GET | 查詢物流倉儲 / 物流帳款 | OK | OK |
| [/api/v1/shipwarehouse/shippayment](#post-api-v1-shipwarehouse-shippayment) | POST | 新增物流倉儲 / 物流帳款 | Need Review | Executor method is not present in code. |
| [/api/v1/shipwarehouse/shippayment](#put-api-v1-shipwarehouse-shippayment) | PUT | 更新物流倉儲 / 物流帳款 | Need Review | Executor method is not present in code. |
| [/api/v1/shipwarehouse/shippayment](#delete-api-v1-shipwarehouse-shippayment) | DELETE | 刪除物流倉儲 / 物流帳款 | Need Review | Executor method is not present in code. |
| [/api/v1/shipwarehouse/shiprec](#get-api-v1-shipwarehouse-shiprec) | GET | 查詢物流倉儲 / 運輸紀錄 | OK | OK |
| [/api/v1/shipwarehouse/shiprec](#post-api-v1-shipwarehouse-shiprec) | POST | 新增物流倉儲 / 運輸紀錄 | Need Review | Executor method is not present in code. |
| [/api/v1/shipwarehouse/shiprec](#put-api-v1-shipwarehouse-shiprec) | PUT | 更新物流倉儲 / 運輸紀錄 | Need Review | Executor method is not present in code. |
| [/api/v1/shipwarehouse/shiprec](#delete-api-v1-shipwarehouse-shiprec) | DELETE | 刪除物流倉儲 / 運輸紀錄 | Need Review | Executor method is not present in code. |
| [/api/v1/shipwarehouse/warehousearap](#get-api-v1-shipwarehouse-warehousearap) | GET | 查詢物流倉儲 / 倉儲應收應付 | OK | OK |
| [/api/v1/shipwarehouse/warehousepayment](#get-api-v1-shipwarehouse-warehousepayment) | GET | 查詢物流倉儲 / 倉儲帳款 | OK | OK |
| [/api/v1/shipwarehouse/warehousepayment](#post-api-v1-shipwarehouse-warehousepayment) | POST | 新增物流倉儲 / 倉儲帳款 | Need Review | Executor method is not present in code. |
| [/api/v1/shipwarehouse/warehousepayment](#put-api-v1-shipwarehouse-warehousepayment) | PUT | 更新物流倉儲 / 倉儲帳款 | Need Review | Executor method is not present in code. |
| [/api/v1/shipwarehouse/warehousepayment](#delete-api-v1-shipwarehouse-warehousepayment) | DELETE | 刪除物流倉儲 / 倉儲帳款 | Need Review | Executor method is not present in code. |
| [/api/v1/shipwarehouse/warehouserec](#get-api-v1-shipwarehouse-warehouserec) | GET | 查詢物流倉儲 / 倉儲紀錄 | OK | OK |
| [/api/v1/shipwarehouse/warehouserec](#post-api-v1-shipwarehouse-warehouserec) | POST | 新增物流倉儲 / 倉儲紀錄 | Need Review | Executor method is not present in code. |
| [/api/v1/shipwarehouse/warehouserec](#put-api-v1-shipwarehouse-warehouserec) | PUT | 更新物流倉儲 / 倉儲紀錄 | Need Review | Executor method is not present in code. |
| [/api/v1/shipwarehouse/warehouserec](#delete-api-v1-shipwarehouse-warehouserec) | DELETE | 刪除物流倉儲 / 倉儲紀錄 | Need Review | Executor method is not present in code. |

## GET /api/v1/shipwarehouse

<a id="get-api-v1-shipwarehouse"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/shipwarehouse | GET | 查詢物流倉儲 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| count | Integer | NO | 分頁筆數 |
| start | Integer | NO | 分頁起始位置 |

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
        "id": "Integer",
        "no": "String",
        "name": "String",
        "category": "Integer",
        "type": "Integer",
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
| payload.count | Integer | 本次回傳筆數 |  |
| payload.results[].id | Integer | 資料 ID |  |
| payload.results[].no | String | 資料編號 |  |
| payload.results[].name | String | 名稱 |  |
| payload.results[].category | Integer | 類別 |  |
| payload.results[].type | Integer | 類型 |  |
| payload.results[].creationTime | Integer | 資料建立時間 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：count、start
2. 查詢 ship_wh_alias 取得物流倉儲資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| ship_wh_alias | 提供物流倉儲查詢、統計或紀錄資料 |

## POST /api/v1/shipwarehouse

<a id="post-api-v1-shipwarehouse"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/shipwarehouse | POST | 新增物流倉儲 |

### Request Header

| Header | Description |
|----------|----------|
| Content-Type | application/json |
| x-auth-token | 存取金鑰 |

### Query Parameters

None

### Request Body

Need Review: request body is read in code, but no explicit schema or field check was found.

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {}
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 建立物流倉儲資料
2. 回傳建立結果與必要識別資訊

### Database Tables Used

None

## PUT /api/v1/shipwarehouse

<a id="put-api-v1-shipwarehouse"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/shipwarehouse | PUT | 更新物流倉儲 |

### Request Header

| Header | Description |
|----------|----------|
| Content-Type | application/json |
| x-auth-token | 存取金鑰 |

### Query Parameters

None

### Request Body

Need Review: request body is read in code, but no explicit schema or field check was found.

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {}
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 依條件更新物流倉儲資料
2. 回傳更新結果

### Database Tables Used

None

## DELETE /api/v1/shipwarehouse

<a id="delete-api-v1-shipwarehouse"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/shipwarehouse | DELETE | 刪除物流倉儲 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

None

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {}
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 依條件刪除或取消物流倉儲資料
2. 回傳刪除或取消結果

### Database Tables Used

None

## GET /api/v1/shipwarehouse/contract

<a id="get-api-v1-shipwarehouse-contract"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/shipwarehouse/contract | GET | 查詢物流倉儲 / 合約 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| count | Integer | NO | 分頁筆數 |
| start | Integer | NO | 分頁起始位置 |

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
        "id": "Integer",
        "no": "String",
        "businessNo": "String",
        "displayName": "String",
        "name": "String",
        "address": "String",
        "phone": "String",
        "fax": "String",
        "contactName": "String",
        "contactPhone": "String",
        "contactTitle": "String",
        "contactEmail": "String",
        "received_id": "Integer",
        "paid_id": "Integer",
        "bankDisplayName": "String",
        "bankName": "String",
        "bankCurrency": "Integer",
        "bankBranch": "String",
        "bankAccount": "String",
        "bankNo": "String",
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
| payload.count | Integer | 本次回傳筆數 |  |
| payload.results[].id | Integer | 資料 ID |  |
| payload.results[].no | String | 資料編號 |  |
| payload.results[].businessNo | String | 統一編號或商業識別編號 |  |
| payload.results[].displayName | String | 顯示名稱 |  |
| payload.results[].name | String | 名稱 |  |
| payload.results[].address | String | 地址 |  |
| payload.results[].phone | String | 電話 |  |
| payload.results[].fax | String | 傳真 |  |
| payload.results[].contactName | String | 聯絡人姓名 |  |
| payload.results[].contactPhone | String | 聯絡人電話 |  |
| payload.results[].contactTitle | String | 聯絡人職稱 |  |
| payload.results[].contactEmail | String | 聯絡人 Email |  |
| payload.results[].received_id | Integer | 收款帳戶 ID |  |
| payload.results[].paid_id | Integer | 付款帳戶 ID |  |
| payload.results[].bankDisplayName | String | 銀行顯示名稱 |  |
| payload.results[].bankName | String | 銀行名稱 |  |
| payload.results[].bankCurrency | Integer | 銀行帳戶幣別 |  |
| payload.results[].bankBranch | String | 銀行分行 |  |
| payload.results[].bankAccount | String | 銀行帳戶名稱 |  |
| payload.results[].bankNo | String | 銀行帳號 |  |
| payload.results[].comment | String | 備註 |  |
| payload.results[].creationTime | Integer | 資料建立時間 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：count、start
2. 查詢 company、payment、ship_wh、ship_wh_contract 取得物流倉儲 / 合約資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| company | 提供物流倉儲查詢、統計或紀錄資料 |
| payment | 提供物流倉儲查詢、統計或紀錄資料 |
| ship_wh | 提供物流倉儲查詢、統計或紀錄資料 |
| ship_wh_contract | 提供物流倉儲查詢、統計或紀錄資料 |

## POST /api/v1/shipwarehouse/contract

<a id="post-api-v1-shipwarehouse-contract"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/shipwarehouse/contract | POST | 新增物流倉儲 / 合約 |

### Request Header

| Header | Description |
|----------|----------|
| Content-Type | application/json |
| x-auth-token | 存取金鑰 |

### Query Parameters

None

### Request Body

Need Review: request body is read in code, but no explicit schema or field check was found.

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {}
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 建立物流倉儲 / 合約資料
2. 回傳建立結果與必要識別資訊

### Database Tables Used

None

## PUT /api/v1/shipwarehouse/contract

<a id="put-api-v1-shipwarehouse-contract"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/shipwarehouse/contract | PUT | 更新物流倉儲 / 合約 |

### Request Header

| Header | Description |
|----------|----------|
| Content-Type | application/json |
| x-auth-token | 存取金鑰 |

### Query Parameters

None

### Request Body

Need Review: request body is read in code, but no explicit schema or field check was found.

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {}
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 依條件更新物流倉儲 / 合約資料
2. 回傳更新結果

### Database Tables Used

None

## DELETE /api/v1/shipwarehouse/contract

<a id="delete-api-v1-shipwarehouse-contract"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/shipwarehouse/contract | DELETE | 刪除物流倉儲 / 合約 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

None

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {}
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 依條件刪除或取消物流倉儲 / 合約資料
2. 回傳刪除或取消結果

### Database Tables Used

None

## GET /api/v1/shipwarehouse/shiparap

<a id="get-api-v1-shipwarehouse-shiparap"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/shipwarehouse/shiparap | GET | 查詢物流倉儲 / 物流應收應付 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| order_no | String | YES | 訂單編號 |

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
        "businessNo": "String",
        "displayName": "String",
        "name": "String",
        "address": "String",
        "phone": "String",
        "fax": "String",
        "contactName": "String",
        "contactPhone": "String",
        "contactTitle": "String",
        "contactEmail": "String",
        "received_id": "Integer",
        "paid_id": "Integer",
        "bankDisplayName": "String",
        "bankName": "String",
        "bankCurrency": "Integer",
        "bankBranch": "String",
        "bankAccount": "String",
        "bankNo": "String",
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
| payload.results[].businessNo | String | 統一編號或商業識別編號 |  |
| payload.results[].displayName | String | 顯示名稱 |  |
| payload.results[].name | String | 名稱 |  |
| payload.results[].address | String | 地址 |  |
| payload.results[].phone | String | 電話 |  |
| payload.results[].fax | String | 傳真 |  |
| payload.results[].contactName | String | 聯絡人姓名 |  |
| payload.results[].contactPhone | String | 聯絡人電話 |  |
| payload.results[].contactTitle | String | 聯絡人職稱 |  |
| payload.results[].contactEmail | String | 聯絡人 Email |  |
| payload.results[].received_id | Integer | 收款帳戶 ID |  |
| payload.results[].paid_id | Integer | 付款帳戶 ID |  |
| payload.results[].bankDisplayName | String | 銀行顯示名稱 |  |
| payload.results[].bankName | String | 銀行名稱 |  |
| payload.results[].bankCurrency | Integer | 銀行帳戶幣別 |  |
| payload.results[].bankBranch | String | 銀行分行 |  |
| payload.results[].bankAccount | String | 銀行帳戶名稱 |  |
| payload.results[].bankNo | String | 銀行帳號 |  |
| payload.results[].comment | String | 備註 |  |
| payload.results[].creationTime | Integer | 資料建立時間 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：order_no
2. 查詢 company、payment、ship_wh_contract、shipping_payment 取得物流倉儲 / 物流應收應付資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| company | 提供物流倉儲查詢、統計或紀錄資料 |
| payment | 提供物流倉儲查詢、統計或紀錄資料 |
| ship_wh_contract | 提供物流倉儲查詢、統計或紀錄資料 |
| shipping_payment | 提供物流倉儲查詢、統計或紀錄資料 |
| shipping_record | 提供物流倉儲查詢、統計或紀錄資料 |

## GET /api/v1/shipwarehouse/shippayment

<a id="get-api-v1-shipwarehouse-shippayment"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/shipwarehouse/shippayment | GET | 查詢物流倉儲 / 物流帳款 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| count | Integer | NO | 分頁筆數 |
| start | Integer | NO | 分頁起始位置 |

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
        "id": "Integer",
        "no": "String",
        "date": "Integer",
        "ref_no": "String",
        "sw_alias_no": "String",
        "displayName": "String",
        "item_no": "String",
        "item_name": "String",
        "item_ref_no": "String",
        "item_ref_displayName": "String",
        "category": "Integer",
        "type": "Integer",
        "itemStyle": "Integer",
        "region": "Integer",
        "unit": "Integer",
        "price": "Float",
        "fee": "Float",
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
| payload.count | Integer | 本次回傳筆數 |  |
| payload.results[].id | Integer | 資料 ID |  |
| payload.results[].no | String | 資料編號 |  |
| payload.results[].date | Integer | 日期時間 |  |
| payload.results[].ref_no | String | 來源單號 |  |
| payload.results[].sw_alias_no | String | 物流倉儲別名no，關連至ship_wh_alias資料表 |  |
| payload.results[].displayName | String | 顯示名稱 |  |
| payload.results[].item_no | String | 料品/品項編號 |  |
| payload.results[].item_name | String | 料品/品項名稱 |  |
| payload.results[].item_ref_no | String | 交易對象編號 |  |
| payload.results[].item_ref_displayName | String | 交易對象顯示名稱 |  |
| payload.results[].category | Integer | 類別 |  |
| payload.results[].type | Integer | 類型 |  |
| payload.results[].itemStyle | Integer | 品項樣式 |  |
| payload.results[].region | Integer | 地區 |  |
| payload.results[].unit | Integer | 單位 |  |
| payload.results[].price | Float | 單價 |  |
| payload.results[].fee | Float | 作業費 / 次 |  |
| payload.results[].comment | String | 備註 |  |
| payload.results[].creationTime | Integer | 資料建立時間 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：count、start
2. 查詢 ship_wh_contract、shipping_payment、shipping_record 取得物流倉儲 / 物流帳款資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| ship_wh_contract | 提供物流倉儲查詢、統計或紀錄資料 |
| shipping_payment | 提供物流倉儲查詢、統計或紀錄資料 |
| shipping_record | 提供物流倉儲查詢、統計或紀錄資料 |

## POST /api/v1/shipwarehouse/shippayment

<a id="post-api-v1-shipwarehouse-shippayment"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/shipwarehouse/shippayment | POST | 新增物流倉儲 / 物流帳款 |

### Request Header

| Header | Description |
|----------|----------|
| Content-Type | application/json |
| x-auth-token | 存取金鑰 |

### Query Parameters

None

### Request Body

Need Review: request body is read in code, but no explicit schema or field check was found.

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {}
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 建立物流倉儲 / 物流帳款資料
2. 回傳建立結果與必要識別資訊

### Database Tables Used

None

## PUT /api/v1/shipwarehouse/shippayment

<a id="put-api-v1-shipwarehouse-shippayment"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/shipwarehouse/shippayment | PUT | 更新物流倉儲 / 物流帳款 |

### Request Header

| Header | Description |
|----------|----------|
| Content-Type | application/json |
| x-auth-token | 存取金鑰 |

### Query Parameters

None

### Request Body

Need Review: request body is read in code, but no explicit schema or field check was found.

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {}
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 依條件更新物流倉儲 / 物流帳款資料
2. 回傳更新結果

### Database Tables Used

None

## DELETE /api/v1/shipwarehouse/shippayment

<a id="delete-api-v1-shipwarehouse-shippayment"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/shipwarehouse/shippayment | DELETE | 刪除物流倉儲 / 物流帳款 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

None

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {}
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 依條件刪除或取消物流倉儲 / 物流帳款資料
2. 回傳刪除或取消結果

### Database Tables Used

None

## GET /api/v1/shipwarehouse/shiprec

<a id="get-api-v1-shipwarehouse-shiprec"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/shipwarehouse/shiprec | GET | 查詢物流倉儲 / 運輸紀錄 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| count | Integer | NO | 分頁筆數 |
| start | Integer | NO | 分頁起始位置 |

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
        "date": "String",
        "count": "Integer",
        "alias": {
          "name": "String",
          "type": "String"
        },
        "contract": {
          "category": "String",
          "type": "String",
          "region": "String",
          "unit": "String",
          "price": "String"
        },
        "order": {
          "date": "String",
          "item_name": "String",
          "item_ref_displayName": "String",
          "unit": "String",
          "price": "String",
          "contractPrice": "String"
        }
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
| payload.results[].date | String | 日期時間 |  |
| payload.results[].count | Integer | 本次回傳筆數 |  |
| payload.results[].alias.name | String | 名稱 |  |
| payload.results[].alias.type | String | 類型 |  |
| payload.results[].contract.category | String | 類別 |  |
| payload.results[].contract.type | String | 類型 |  |
| payload.results[].contract.region | String | 地區 |  |
| payload.results[].contract.unit | String | 單位 |  |
| payload.results[].contract.price | String | 單價 |  |
| payload.results[].order.date | String | 日期時間 |  |
| payload.results[].order.item_name | String | 料品/品項名稱 |  |
| payload.results[].order.item_ref_displayName | String | 交易對象顯示名稱 |  |
| payload.results[].order.unit | String | 單位 |  |
| payload.results[].order.price | String | 單價 |  |
| payload.results[].order.contractPrice | String | contract Price 的業務資料 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：count、start
2. 查詢 goods_receipt_note、payment、product_order、purchase_order 取得物流倉儲 / 運輸紀錄資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| goods_receipt_note | 提供物流倉儲查詢、統計或紀錄資料 |
| payment | 提供物流倉儲查詢、統計或紀錄資料 |
| product_order | 提供物流倉儲查詢、統計或紀錄資料 |
| purchase_order | 提供物流倉儲查詢、統計或紀錄資料 |
| ship_wh_alias | 提供物流倉儲查詢、統計或紀錄資料 |
| ship_wh_contract | 提供物流倉儲查詢、統計或紀錄資料 |
| shipping_order | 提供物流倉儲查詢、統計或紀錄資料 |
| shipping_record | 提供物流倉儲查詢、統計或紀錄資料 |

## POST /api/v1/shipwarehouse/shiprec

<a id="post-api-v1-shipwarehouse-shiprec"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/shipwarehouse/shiprec | POST | 新增物流倉儲 / 運輸紀錄 |

### Request Header

| Header | Description |
|----------|----------|
| Content-Type | application/json |
| x-auth-token | 存取金鑰 |

### Query Parameters

None

### Request Body

Need Review: request body is read in code, but no explicit schema or field check was found.

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {}
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 建立物流倉儲 / 運輸紀錄資料
2. 回傳建立結果與必要識別資訊

### Database Tables Used

None

## PUT /api/v1/shipwarehouse/shiprec

<a id="put-api-v1-shipwarehouse-shiprec"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/shipwarehouse/shiprec | PUT | 更新物流倉儲 / 運輸紀錄 |

### Request Header

| Header | Description |
|----------|----------|
| Content-Type | application/json |
| x-auth-token | 存取金鑰 |

### Query Parameters

None

### Request Body

Need Review: request body is read in code, but no explicit schema or field check was found.

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {}
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 依條件更新物流倉儲 / 運輸紀錄資料
2. 回傳更新結果

### Database Tables Used

None

## DELETE /api/v1/shipwarehouse/shiprec

<a id="delete-api-v1-shipwarehouse-shiprec"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/shipwarehouse/shiprec | DELETE | 刪除物流倉儲 / 運輸紀錄 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

None

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {}
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 依條件刪除或取消物流倉儲 / 運輸紀錄資料
2. 回傳刪除或取消結果

### Database Tables Used

None

## GET /api/v1/shipwarehouse/warehousearap

<a id="get-api-v1-shipwarehouse-warehousearap"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/shipwarehouse/warehousearap | GET | 查詢物流倉儲 / 倉儲應收應付 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| order_category | String | NO | order_category 查詢條件 |
| order_no | String | YES | 訂單編號 |

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
        "businessNo": "String",
        "displayName": "String",
        "name": "String",
        "address": "String",
        "phone": "String",
        "fax": "String",
        "contactName": "String",
        "contactPhone": "String",
        "contactTitle": "String",
        "contactEmail": "String",
        "received_id": "Integer",
        "paid_id": "Integer",
        "bankDisplayName": "String",
        "bankName": "String",
        "bankCurrency": "Integer",
        "bankBranch": "String",
        "bankAccount": "String",
        "bankNo": "String",
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
| payload.results[].businessNo | String | 統一編號或商業識別編號 |  |
| payload.results[].displayName | String | 顯示名稱 |  |
| payload.results[].name | String | 名稱 |  |
| payload.results[].address | String | 地址 |  |
| payload.results[].phone | String | 電話 |  |
| payload.results[].fax | String | 傳真 |  |
| payload.results[].contactName | String | 聯絡人姓名 |  |
| payload.results[].contactPhone | String | 聯絡人電話 |  |
| payload.results[].contactTitle | String | 聯絡人職稱 |  |
| payload.results[].contactEmail | String | 聯絡人 Email |  |
| payload.results[].received_id | Integer | 收款帳戶 ID |  |
| payload.results[].paid_id | Integer | 付款帳戶 ID |  |
| payload.results[].bankDisplayName | String | 銀行顯示名稱 |  |
| payload.results[].bankName | String | 銀行名稱 |  |
| payload.results[].bankCurrency | Integer | 銀行帳戶幣別 |  |
| payload.results[].bankBranch | String | 銀行分行 |  |
| payload.results[].bankAccount | String | 銀行帳戶名稱 |  |
| payload.results[].bankNo | String | 銀行帳號 |  |
| payload.results[].comment | String | 備註 |  |
| payload.results[].creationTime | Integer | 資料建立時間 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：order_category、order_no
2. 查詢 company、payment、ship_wh_contract、warehouse_payment 取得物流倉儲 / 倉儲應收應付資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| company | 提供物流倉儲查詢、統計或紀錄資料 |
| payment | 提供物流倉儲查詢、統計或紀錄資料 |
| ship_wh_contract | 提供物流倉儲查詢、統計或紀錄資料 |
| warehouse_payment | 提供物流倉儲查詢、統計或紀錄資料 |
| warehouse_record | 提供物流倉儲查詢、統計或紀錄資料 |

## GET /api/v1/shipwarehouse/warehousepayment

<a id="get-api-v1-shipwarehouse-warehousepayment"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/shipwarehouse/warehousepayment | GET | 查詢物流倉儲 / 倉儲帳款 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| count | Integer | NO | 分頁筆數 |
| start | Integer | NO | 分頁起始位置 |

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
        "id": "Integer",
        "no": "String",
        "date": "Integer",
        "ref_no": "String",
        "sw_alias_no": "String",
        "displayName": "String",
        "item_no": "String",
        "item_name": "String",
        "item_ref_no": "String",
        "item_ref_displayName": "String",
        "category": "Integer",
        "type": "Integer",
        "itemStyle": "Integer",
        "region": "Integer",
        "unit": "Integer",
        "price": "Float",
        "fee": "Float",
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
| payload.count | Integer | 本次回傳筆數 |  |
| payload.results[].id | Integer | 資料 ID |  |
| payload.results[].no | String | 資料編號 |  |
| payload.results[].date | Integer | 日期時間 |  |
| payload.results[].ref_no | String | 來源單號 |  |
| payload.results[].sw_alias_no | String | 物流倉儲別名no，關連至ship_wh_alias資料表 |  |
| payload.results[].displayName | String | 顯示名稱 |  |
| payload.results[].item_no | String | 料品/品項編號 |  |
| payload.results[].item_name | String | 料品/品項名稱 |  |
| payload.results[].item_ref_no | String | 交易對象編號 |  |
| payload.results[].item_ref_displayName | String | 交易對象顯示名稱 |  |
| payload.results[].category | Integer | 類別 |  |
| payload.results[].type | Integer | 類型 |  |
| payload.results[].itemStyle | Integer | 品項樣式 |  |
| payload.results[].region | Integer | 地區 |  |
| payload.results[].unit | Integer | 單位 |  |
| payload.results[].price | Float | 單價 |  |
| payload.results[].fee | Float | 作業費 / 次 |  |
| payload.results[].comment | String | 備註 |  |
| payload.results[].creationTime | Integer | 資料建立時間 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：count、start
2. 查詢 ship_wh_contract、warehouse_payment、warehouse_record 取得物流倉儲 / 倉儲帳款資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| ship_wh_contract | 提供物流倉儲查詢、統計或紀錄資料 |
| warehouse_payment | 提供物流倉儲查詢、統計或紀錄資料 |
| warehouse_record | 提供物流倉儲查詢、統計或紀錄資料 |

## POST /api/v1/shipwarehouse/warehousepayment

<a id="post-api-v1-shipwarehouse-warehousepayment"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/shipwarehouse/warehousepayment | POST | 新增物流倉儲 / 倉儲帳款 |

### Request Header

| Header | Description |
|----------|----------|
| Content-Type | application/json |
| x-auth-token | 存取金鑰 |

### Query Parameters

None

### Request Body

Need Review: request body is read in code, but no explicit schema or field check was found.

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {}
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 建立物流倉儲 / 倉儲帳款資料
2. 回傳建立結果與必要識別資訊

### Database Tables Used

None

## PUT /api/v1/shipwarehouse/warehousepayment

<a id="put-api-v1-shipwarehouse-warehousepayment"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/shipwarehouse/warehousepayment | PUT | 更新物流倉儲 / 倉儲帳款 |

### Request Header

| Header | Description |
|----------|----------|
| Content-Type | application/json |
| x-auth-token | 存取金鑰 |

### Query Parameters

None

### Request Body

Need Review: request body is read in code, but no explicit schema or field check was found.

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {}
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 依條件更新物流倉儲 / 倉儲帳款資料
2. 回傳更新結果

### Database Tables Used

None

## DELETE /api/v1/shipwarehouse/warehousepayment

<a id="delete-api-v1-shipwarehouse-warehousepayment"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/shipwarehouse/warehousepayment | DELETE | 刪除物流倉儲 / 倉儲帳款 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

None

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {}
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 依條件刪除或取消物流倉儲 / 倉儲帳款資料
2. 回傳刪除或取消結果

### Database Tables Used

None

## GET /api/v1/shipwarehouse/warehouserec

<a id="get-api-v1-shipwarehouse-warehouserec"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/shipwarehouse/warehouserec | GET | 查詢物流倉儲 / 倉儲紀錄 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| count | Integer | NO | 分頁筆數 |
| start | Integer | NO | 分頁起始位置 |

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
        "date": "String",
        "count": "Integer",
        "days": "String",
        "alias": {
          "name": "String",
          "type": "String"
        },
        "contract": {
          "category": "String",
          "type": "String",
          "unit": "String",
          "price": "String"
        },
        "batch": {
          "no": "String",
          "item_name": "String",
          "itemCategory": "String",
          "itemSubCategory": "String",
          "validDate": "String"
        }
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
| payload.results[].date | String | 日期時間 |  |
| payload.results[].count | Integer | 本次回傳筆數 |  |
| payload.results[].days | String | 存放天數 |  |
| payload.results[].alias.name | String | 名稱 |  |
| payload.results[].alias.type | String | 類型 |  |
| payload.results[].contract.category | String | 類別 |  |
| payload.results[].contract.type | String | 類型 |  |
| payload.results[].contract.unit | String | 單位 |  |
| payload.results[].contract.price | String | 單價 |  |
| payload.results[].batch.no | String | 資料編號 |  |
| payload.results[].batch.item_name | String | 料品/品項名稱 |  |
| payload.results[].batch.itemCategory | String | 料品類別 |  |
| payload.results[].batch.itemSubCategory | String | 料品子類別 |  |
| payload.results[].batch.validDate | String | 效期日期 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：count、start
2. 查詢 batch_number、ship_wh_alias、ship_wh_contract、warehouse_record 取得物流倉儲 / 倉儲紀錄資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| batch_number | 提供物流倉儲查詢、統計或紀錄資料 |
| ship_wh_alias | 提供物流倉儲查詢、統計或紀錄資料 |
| ship_wh_contract | 提供物流倉儲查詢、統計或紀錄資料 |
| warehouse_record | 提供物流倉儲查詢、統計或紀錄資料 |

## POST /api/v1/shipwarehouse/warehouserec

<a id="post-api-v1-shipwarehouse-warehouserec"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/shipwarehouse/warehouserec | POST | 新增物流倉儲 / 倉儲紀錄 |

### Request Header

| Header | Description |
|----------|----------|
| Content-Type | application/json |
| x-auth-token | 存取金鑰 |

### Query Parameters

None

### Request Body

Need Review: request body is read in code, but no explicit schema or field check was found.

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {}
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 建立物流倉儲 / 倉儲紀錄資料
2. 回傳建立結果與必要識別資訊

### Database Tables Used

None

## PUT /api/v1/shipwarehouse/warehouserec

<a id="put-api-v1-shipwarehouse-warehouserec"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/shipwarehouse/warehouserec | PUT | 更新物流倉儲 / 倉儲紀錄 |

### Request Header

| Header | Description |
|----------|----------|
| Content-Type | application/json |
| x-auth-token | 存取金鑰 |

### Query Parameters

None

### Request Body

Need Review: request body is read in code, but no explicit schema or field check was found.

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {}
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 依條件更新物流倉儲 / 倉儲紀錄資料
2. 回傳更新結果

### Database Tables Used

None

## DELETE /api/v1/shipwarehouse/warehouserec

<a id="delete-api-v1-shipwarehouse-warehouserec"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/shipwarehouse/warehouserec | DELETE | 刪除物流倉儲 / 倉儲紀錄 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

None

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {}
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 依條件刪除或取消物流倉儲 / 倉儲紀錄資料
2. 回傳刪除或取消結果

### Database Tables Used

None
