# quotation API Group

> Source: `restserver/package/restserver/api/quotation_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v1/quotation](#get-api-v1-quotation) | GET | 查詢報價 | OK | OK |

## GET /api/v1/quotation

<a id="get-api-v1-quotation"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/quotation | GET | 查詢報價 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| count | Integer | NO | 分頁筆數 |
| start | Integer | NO | 分頁起始位置 |
| type | Integer | NO | 類型篩選 |

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
        "date": "Integer",
        "category": "Integer",
        "type": "Integer",
        "itemStyle": "Integer",
        "item_ref_no": "String",
        "item_ref_displayName": "String",
        "item_no": "String",
        "item_name": "String",
        "unit": "Integer",
        "price": "Float",
        "count": "Float",
        "amount": "Float",
        "comment": "String",
        "creationTime": "Integer",
        "transItemCategory": "Integer",
        "transItemAttr": "Integer",
        "paymentType": "Integer",
        "paymentDate": "Integer",
        "paymentPeriod": "Integer",
        "unitWarehouse": "Integer"
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
| payload.results[].id | Integer | ID |  |
| payload.results[].no | String | 編號 |  |
| payload.results[].date | Integer | 報價日期 |  |
| payload.results[].category | Integer | 類別 | 採購 (1)、訂購 (2) |
| payload.results[].type | Integer | 類型 | 合約類別為: <br>1.採購: 採購 (1)、客供 (2)、採買 (3)、購置/保修 (4)<br>2. 訂購: 產製 (1)、進銷 (2) |
| payload.results[].itemStyle | Integer | 品項樣式 | 貨品 (1) 、 產品 (2) 、材料 (3)、耗品(4) 、設備(5) |
| payload.results[].item_ref_no | String | 交易對象編號 |  |
| payload.results[].item_ref_displayName | String | 交易對象顯示名稱 |  |
| payload.results[].item_no | String | 「交易品項」編號 |  |
| payload.results[].item_name | String | 交易品項」名稱 |  |
| payload.results[].unit | Integer | 單位 |  |
| payload.results[].price | Float | 單價 |  |
| payload.results[].count | Float | 需求量 |  |
| payload.results[].amount | Float | 金額 |  |
| payload.results[].comment | String | 備註 |  |
| payload.results[].transItemCategory | Integer | 「交易品項」的樣式 |  |
| payload.results[].transItemAttr | Integer | 「交易品項」的屬性 |  |
| payload.results[].paymentType | Integer | 收付款類別 |  |
| payload.results[].paymentDate | Integer | 收付款日期 |  |
| payload.results[].paymentPeriod | Integer | 付款期間 |  |
| payload.results[].unitWarehouse | Integer | 倉儲單位 |  |
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
2. 查詢 company、payment 取得報價資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| company | 提供報價單據、合約、帳款或統計資料 |
| payment | 提供報價單據、合約、帳款或統計資料 |
