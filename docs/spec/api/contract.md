# contract API Group

> Source: `restserver/package/restserver/api/contract_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v1/contract](#get-api-v1-contract) | GET | 查詢合約 | OK | OK |

## GET /api/v1/contract

<a id="get-api-v1-contract"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/contract | GET | 查詢合約 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| count | Integer | NO | 分頁筆數 |
| start | Integer | NO | 分頁起始位置 |
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
| payload.results[].no | String | 編號篩選 |  |
| payload.results[].businessNo | String | businessNo 回傳欄位 |  |
| payload.results[].displayName | String | 顯示名稱 |  |
| payload.results[].name | String | 名稱 |  |
| payload.results[].address | String | address 回傳欄位 |  |
| payload.results[].phone | String | phone 回傳欄位 |  |
| payload.results[].fax | String | fax 回傳欄位 |  |
| payload.results[].contactName | String | contactName 回傳欄位 |  |
| payload.results[].contactPhone | String | contactPhone 回傳欄位 |  |
| payload.results[].contactTitle | String | contactTitle 回傳欄位 |  |
| payload.results[].contactEmail | String | contactEmail 回傳欄位 |  |
| payload.results[].received_id | Integer | received_id 回傳欄位 |  |
| payload.results[].paid_id | Integer | paid_id 回傳欄位 |  |
| payload.results[].bankDisplayName | String | bankDisplayName 回傳欄位 |  |
| payload.results[].bankName | String | bankName 回傳欄位 |  |
| payload.results[].bankCurrency | Integer | bankCurrency 回傳欄位 |  |
| payload.results[].bankBranch | String | bankBranch 回傳欄位 |  |
| payload.results[].bankAccount | String | bankAccount 回傳欄位 |  |
| payload.results[].bankNo | String | bankNo 回傳欄位 |  |
| payload.results[].comment | String | comment 回傳欄位 |  |
| payload.results[].creationTime | Integer | creationTime 回傳欄位 |  |
| payload.count | Integer | 本次回傳筆數 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件：count、start、type
2. 查詢資料表並套用條件：company、payment
3. 組裝回傳 payload 欄位：payload.total、payload.results[].id、payload.results[].no、payload.results[].businessNo、payload.results[].displayName、payload.results[].name、payload.results[].address、payload.results[].phone、payload.results[].fax、payload.results[].contactName、payload.results[].contactPhone、payload.results[].contactTitle、payload.results[].contactEmail、payload.results[].received_id、payload.results[].paid_id、payload.results[].bankDisplayName、payload.results[].bankName、payload.results[].bankCurrency、payload.results[].bankBranch、payload.results[].bankAccount、payload.results[].bankNo、payload.results[].comment、payload.results[].creationTime、payload.count

### Database Tables Used

| Table | Purpose |
|----------|------|
| company | 提供合約單據、合約、帳款或統計資料 |
| payment | 提供合約單據、合約、帳款或統計資料 |
