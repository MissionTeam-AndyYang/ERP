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
    "count": "Object",
    "results": "Object"
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.total | Integer | 符合條件的總筆數 |  |
| payload.count | Object | 本次回傳筆數 |  |
| payload.results | Object | 查詢結果清單 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Object | 錯誤 payload；目前程式通常回傳空物件 |  |

### Processing Flow

1. 讀取查詢條件：count、start
2. 呼叫服務：CLogger.log
3. 查詢或使用資料表：ship_wh_alias
4. 組裝回傳 payload 欄位：payload.total、payload.count、payload.results

### Database Tables Used

| Table | Purpose |
|----------|------|
| ship_wh_alias | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |

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
| payload | Object | 空物件或無資料 payload |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Object | 錯誤 payload；目前程式通常回傳空物件 |  |

### Processing Flow

Need Review: executor method body could not be traced to concrete business logic.

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
| payload | Object | 空物件或無資料 payload |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Object | 錯誤 payload；目前程式通常回傳空物件 |  |

### Processing Flow

Need Review: executor method body could not be traced to concrete business logic.

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
| payload | Object | 空物件或無資料 payload |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Object | 錯誤 payload；目前程式通常回傳空物件 |  |

### Processing Flow

Need Review: executor method body could not be traced to concrete business logic.

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
    "total": "Object",
    "count": "Object",
    "results": "Object"
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.total | Object | 符合條件的總筆數 |  |
| payload.count | Object | 本次回傳筆數 |  |
| payload.results | Object | 查詢結果清單 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Object | 錯誤 payload；目前程式通常回傳空物件 |  |

### Processing Flow

1. 讀取查詢條件：count、start
2. 呼叫服務：CLogger.log
3. 查詢或使用資料表：company、payment、ship_wh、ship_wh_contract
4. 組裝回傳 payload 欄位：payload.total、payload.count、payload.results

### Database Tables Used

| Table | Purpose |
|----------|------|
| company | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| payment | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| ship_wh | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| ship_wh_contract | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |

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
| payload | Object | 空物件或無資料 payload |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Object | 錯誤 payload；目前程式通常回傳空物件 |  |

### Processing Flow

Need Review: executor method body could not be traced to concrete business logic.

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
| payload | Object | 空物件或無資料 payload |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Object | 錯誤 payload；目前程式通常回傳空物件 |  |

### Processing Flow

Need Review: executor method body could not be traced to concrete business logic.

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
| payload | Object | 空物件或無資料 payload |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Object | 錯誤 payload；目前程式通常回傳空物件 |  |

### Processing Flow

Need Review: executor method body could not be traced to concrete business logic.

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
    "total": "Object",
    "results": "Object"
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.total | Object | 符合條件的總筆數 |  |
| payload.results | Object | 查詢結果清單 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Object | 錯誤 payload；目前程式通常回傳空物件 |  |

### Processing Flow

1. 讀取查詢條件：order_no
2. 呼叫服務：CCShipPayment.get、CLogger.log
3. 查詢或使用資料表：ship_wh_contract、shipping_record
4. 組裝回傳 payload 欄位：payload.total、payload.results

### Database Tables Used

| Table | Purpose |
|----------|------|
| ship_wh_contract | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| shipping_record | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |

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
    "results": []
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.total | Integer | 符合條件的總筆數 |  |
| payload.count | Integer | 本次回傳筆數 |  |
| payload.results | Array | 查詢結果清單 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Object | 錯誤 payload；目前程式通常回傳空物件 |  |

### Processing Flow

1. 讀取查詢條件：count、start
2. 呼叫服務：CLogger.log
3. 查詢或使用資料表：ship_wh_contract、shipping_payment、shipping_record
4. 組裝回傳 payload 欄位：payload.total、payload.count、payload.results

### Database Tables Used

| Table | Purpose |
|----------|------|
| ship_wh_contract | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| shipping_payment | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| shipping_record | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |

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
| payload | Object | 空物件或無資料 payload |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Object | 錯誤 payload；目前程式通常回傳空物件 |  |

### Processing Flow

Need Review: executor method body could not be traced to concrete business logic.

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
| payload | Object | 空物件或無資料 payload |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Object | 錯誤 payload；目前程式通常回傳空物件 |  |

### Processing Flow

Need Review: executor method body could not be traced to concrete business logic.

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
| payload | Object | 空物件或無資料 payload |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Object | 錯誤 payload；目前程式通常回傳空物件 |  |

### Processing Flow

Need Review: executor method body could not be traced to concrete business logic.

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
    "count": "Object",
    "results": "Object"
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.total | Integer | 符合條件的總筆數 |  |
| payload.count | Object | 本次回傳筆數 |  |
| payload.results | Object | 查詢結果清單 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Object | 錯誤 payload；目前程式通常回傳空物件 |  |

### Processing Flow

1. 讀取查詢條件：count、start
2. 呼叫服務：CLogger.log
3. 查詢或使用資料表：goods_receipt_note、payment、product_order、purchase_order、ship_wh_alias、ship_wh_contract、shipping_order、shipping_record
4. 組裝回傳 payload 欄位：payload.total、payload.count、payload.results

### Database Tables Used

| Table | Purpose |
|----------|------|
| goods_receipt_note | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| payment | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| product_order | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| purchase_order | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| ship_wh_alias | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| ship_wh_contract | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| shipping_order | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| shipping_record | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |

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
| payload | Object | 空物件或無資料 payload |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Object | 錯誤 payload；目前程式通常回傳空物件 |  |

### Processing Flow

Need Review: executor method body could not be traced to concrete business logic.

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
| payload | Object | 空物件或無資料 payload |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Object | 錯誤 payload；目前程式通常回傳空物件 |  |

### Processing Flow

Need Review: executor method body could not be traced to concrete business logic.

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
| payload | Object | 空物件或無資料 payload |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Object | 錯誤 payload；目前程式通常回傳空物件 |  |

### Processing Flow

Need Review: executor method body could not be traced to concrete business logic.

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
    "total": "Object",
    "results": "Object"
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.total | Object | 符合條件的總筆數 |  |
| payload.results | Object | 查詢結果清單 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Object | 錯誤 payload；目前程式通常回傳空物件 |  |

### Processing Flow

1. 讀取查詢條件：order_category、order_no
2. 呼叫服務：CCWarehousePayment.get、CLogger.log
3. 查詢或使用資料表：ship_wh_contract、warehouse_record
4. 組裝回傳 payload 欄位：payload.total、payload.results

### Database Tables Used

| Table | Purpose |
|----------|------|
| ship_wh_contract | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| warehouse_record | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |

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
    "results": []
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.total | Integer | 符合條件的總筆數 |  |
| payload.count | Integer | 本次回傳筆數 |  |
| payload.results | Array | 查詢結果清單 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Object | 錯誤 payload；目前程式通常回傳空物件 |  |

### Processing Flow

1. 讀取查詢條件：count、start
2. 呼叫服務：CLogger.log
3. 查詢或使用資料表：ship_wh_contract、warehouse_payment、warehouse_record
4. 組裝回傳 payload 欄位：payload.total、payload.count、payload.results

### Database Tables Used

| Table | Purpose |
|----------|------|
| ship_wh_contract | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| warehouse_payment | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| warehouse_record | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |

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
| payload | Object | 空物件或無資料 payload |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Object | 錯誤 payload；目前程式通常回傳空物件 |  |

### Processing Flow

Need Review: executor method body could not be traced to concrete business logic.

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
| payload | Object | 空物件或無資料 payload |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Object | 錯誤 payload；目前程式通常回傳空物件 |  |

### Processing Flow

Need Review: executor method body could not be traced to concrete business logic.

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
| payload | Object | 空物件或無資料 payload |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Object | 錯誤 payload；目前程式通常回傳空物件 |  |

### Processing Flow

Need Review: executor method body could not be traced to concrete business logic.

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
    "count": "Object",
    "results": "Object"
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.total | Integer | 符合條件的總筆數 |  |
| payload.count | Object | 本次回傳筆數 |  |
| payload.results | Object | 查詢結果清單 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Object | 錯誤 payload；目前程式通常回傳空物件 |  |

### Processing Flow

1. 讀取查詢條件：count、start
2. 呼叫服務：CLogger.log
3. 查詢或使用資料表：batch_number、ship_wh_alias、ship_wh_contract、warehouse_record
4. 組裝回傳 payload 欄位：payload.total、payload.count、payload.results

### Database Tables Used

| Table | Purpose |
|----------|------|
| batch_number | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| ship_wh_alias | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| ship_wh_contract | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| warehouse_record | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |

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
| payload | Object | 空物件或無資料 payload |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Object | 錯誤 payload；目前程式通常回傳空物件 |  |

### Processing Flow

Need Review: executor method body could not be traced to concrete business logic.

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
| payload | Object | 空物件或無資料 payload |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Object | 錯誤 payload；目前程式通常回傳空物件 |  |

### Processing Flow

Need Review: executor method body could not be traced to concrete business logic.

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
| payload | Object | 空物件或無資料 payload |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Object | 錯誤 payload；目前程式通常回傳空物件 |  |

### Processing Flow

Need Review: executor method body could not be traced to concrete business logic.

### Database Tables Used

None
