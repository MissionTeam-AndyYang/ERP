# aps API Group

> Source: `restserver/package/restserver/api/aps_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v1/aps/quantity](#get-api-v1-aps-quantity) | GET | 查詢APS 資料 / 製造需求數量 | OK | OK |

## GET /api/v1/aps/quantity

<a id="get-api-v1-aps-quantity"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/aps/quantity | GET | 查詢APS 資料 / 製造需求數量 |

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
        "product_order": {
          "no":  "String",
          "unit": "Integer",
          "item_name":  "String",
          "item_ref_displayName":  "String",
          "price": "Float",
          "count": "Integer",
          "amount": "Integer",
          "preparedCount": "Integer",
          "paymentType": "Integer",
          "contractCategory": "Integer",
          "contractType": "Integer",
          "contractItemStyle": "Integer",
          "contractComment": "String",
        },
        "process": [
          {
            "no":  "String",
            "item_name":  "String",
            "oneProcess": "Integer",
            "secProcess": "Integer",
            "unit": "Integer",
            "amount": "Float",
            "hours": "Float",
          }
        ]
      }
    ],
   
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.total | Integer | 符合條件的總筆數 |  |
| payload.count | Integer | 本次回傳筆數 |  |
| payload.results[].product_order.no | String | 訂購單號 |  |
| payload.results[].product_order.item_name | String | 「交易品項」名稱 |  |
| payload.results[].product_order.item_ref_displayName | String | 交易對象 |  |
| payload.results[].product_order.unit | Integer | 交易單位 |  |
| payload.results[].product_order.price | Float | 交易單價 |  |
| payload.results[].product_order.count | Integer | 交易數量 |  |
| payload.results[].product_order.preparedCount | Integer | 備貨總量 |  |
| payload.results[].product_order.paymentType | Integer | 收付款類別 | 現結 (0)、月結 (1) |
| payload.results[].product_order.contractCategory  | Integer | 合約類別 |  採購 (1)、訂購 (2) |
| payload.results[].product_order.contractType | Integer | 合約樣式 | 合約類別為<br>1.採購: 採購 (1)、客供 (2)、採買 (3)、購置/保修 (4)<br>2.訂購: 產製 (1)、進銷 (2)|
| payload.results[].product_order.contractItemStyle | Integer | 品項樣式 | 貨品 (1) 、 產品 (2) 、材料 (3)、耗品(4) 、設備(5) |
| payload.results[].product_order.contractComment | String | 合約規格 | |
| payload.results[].process[].no | String | APS編號 |  |
| payload.results[].process[].oneProcess | Integer | 主製程 |  |
| payload.results[].process[].secProcess | Integer | 次製程 |  |
| payload.results[].process[].item_name | String | 產出「料品品項」名稱 |  |
| payload.results[].process[].unit | Integer | 重量或數量單位 |  |
| payload.results[].process[].amount | Float | 所需重量或數量 |  |
| payload.results[].process[].hours | Float | 所需時數 |  |



### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：count、start
2. 查詢 aps_quantity、contract、product_order 取得APS 資料 / 製造需求數量資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| aps_quantity | 提供APS排程、生產或產能資料 |
| contract | 提供APS排程、生產或產能資料 |
| product_order | 提供APS排程、生產或產能資料 |
