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
| payload.count | Integer | 本次回傳筆數 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：count、start、type
2. 查詢 company、payment 取得合約資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| company | 提供合約單據、合約、帳款或統計資料 |
| payment | 提供合約單據、合約、帳款或統計資料 |
