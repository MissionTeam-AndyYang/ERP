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
        "ref_no": "String",
        "creator_no": "String",
        "date": "Integer",
        "displayName": "String",
        "category": "Integer",
        "type": "Integer",
        "itemStyle": "Integer",
        "item_no": "String",
        "item_name": "String",
        "itemCategory": "Integer",
        "itemSubCategory": "Integer",
        "item_ref_no": "String",
        "item_ref_displayName": "String",
        "payment_id": "Integer",
        "unit": "Integer",
        "price": "Float",
        "shippingPrice": "Float",
        "unitConversion": "Float",
        "comment": "String",
        "creationTime": "",
        "item": {
            "itemCategory": "Integer",
            "itemSubCategory": "Integer",
            "item_no": "String",
            "item_name": "String",
        },
        "itemPrice": {
            "String": {
                "unit": "Integer",
                "price":  "Float",
            }
        },
        "transItemCategory": "Integer",
        "transItemAttr": "Integer",
        "paymentType": "Integer",
        "paymentDate": "Integer",
        "paymentPeriod": "Integer",
        "quotation_no": "String",
        "quotationDate": "Integer",
        "unitWarehouse": "Integer",
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
| payload.results[].id | Integer | 合約資料ID |  |
| payload.results[].date | Integer | 生效日期 |  |
| payload.results[].displayName | String | 簡稱 |  |
| payload.results[].category | Integer | 合約類別 | 採購 (1)、訂購 (2) |
| payload.results[].type | Integer | 合約樣式 | 合約類別為<br>1.採購: 採購 (1)、客供 (2)、採買 (3)、購置/保修 (4)<br>2.訂購: 產製 (1)、進銷 (2) |
| payload.results[].itemStyle | Integer | 品項樣式 | 貨品 (1) 、 產品 (2) 、材料 (3)、耗品(4) 、設備(5) |
| payload.results[].item_no | String | 「交易品項」no |  |
| payload.results[].item_name | String | 「交易品項」名稱 |  |
| payload.results[].itemCategory | Integer | 「料品品項」類別 | 原料 (1)、物料 (2)、膠捲 (3) 、在製品 (4) 、製成品 (5) 、貨品 (6) |
| payload.results[].itemSubCategory | Integer | 料品品項」子類別 | 料品品項」類別為<br>1.原料/物料/膠捲:參照material的「subCategory」定義<br>2. 在製品/製成品:參照inproduct/product的「category」定義<br>3. 貨品:參照goods的「subCategory」定義 |
| payload.results[].item_ref_no | String | 客戶/廠商no |  |
| payload.results[].item_ref_displayName | String | 客戶/廠商公司簡稱 |  |
| payload.results[].paid_id | Integer | 帳款資料id |  
| payload.results[].unit | Integer | 	交易單位 |  
| payload.results[].price | Float | 單位價格 |  |
| payload.results[].shippingPrice | Float | 物流價格 |  |
| payload.results[].unitConversion | Float | 規格轉換 |  |
| payload.results[].comment | String | 規格 |  |
| payload.results[].creationTime | Integer | 資料建立時間 |  |
| payload.results[].item.item_no | String | 「料品品項」no |  |
| payload.results[].item.item_name | String | 「料品品項」名稱 |  |
| payload.results[].item.itemCategory | Integer | 「料品品項」類別 | 原料 (1)、物料 (2)、膠捲 (3) 、在製品 (4) 、製成品 (5) 、貨品 (6) |
| payload.results[].item.itemSubCategory | Integer | 「料品品項」子類別 | 料品品項」類別為<br>1.原料/物料/膠捲:參照material的「subCategory」定義<br>2. 在製品/製成品:參照inproduct/product的「category」定義<br>3. 貨品:參照goods的「subCategory」定義 |
| payload.results[].itemprice.String | String | 月份 規則: YYYY/MM |  |
| payload.results[].itemprice.String.unit | Integer | 交易單位 |  |
| payload.results[].itemprice.String.price | Float | 單位價格 |  |
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
