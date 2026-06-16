# work API Group

> Source: `restserver/package/restserver/api/work_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v1/work/assignment](#get-api-v1-work-assignment) | GET | 取得產製製令分派 | OK | OK |
| [/api/v1/work/process](#get-api-v1-work-process) | GET | 查詢領退餘廢產單 | OK | OK |
| [/api/v1/work/process](#post-api-v1-work-process) | POST | 新增領退餘廢產單 | OK | OK |
| [/api/v1/work/productdata](#get-api-v1-work-productdata) | GET | 查詢訂單生產數據 | OK | OK |
| [/api/v1/work/progress](#get-api-v1-work-progress) | GET | 查詢訂單製造進度 | OK | OK |

## GET /api/v1/work/assignment

<a id="get-api-v1-work-assignment"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/work/assignment | GET | 取得產製製令分派 |

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
        "input": [
          {
           "workOrderDate": "Integer",
            "production_line_no": "String",
            "productionLineName": "String",
            "processDate": "Integer",
            "item_no": "String",
            "item_name": "String",
            "itemCategory": "Integer",
            "itemSubCategory": "Integer",
            "itemType": "String",
            "batch_number": "String",
            "validDate": "Integer",
            "unit": "Integer",
            "count": "Float"
          }
        ],
        "output": [
          {
            "workOrderDate": "Integer",
            "production_line_no": "String",
            "productionLineName": "String",
            "processDate": "Integer",
            "item_no": "String",
            "item_name": "String",
            "itemCategory": "Integer",
            "itemSubCategory": "Integer",
            "itemType": "String",
            "batch_number": "String",
            "validDate": "Integer",
            "unit": "Integer",
            "count": "Float"
          }
        ],
        "reuse": [
          {
           "workOrderDate": "Integer",
            "production_line_no": "String",
            "productionLineName": "String",
            "processDate": "Integer",
            "item_no": "String",
            "item_name": "String",
            "itemCategory": "Integer",
            "itemSubCategory": "Integer",
            "itemType": "String",
            "batch_number": "String",
            "validDate": "Integer",
            "unit": "Integer",
            "count": "Float"
          }
        ],
        "labors": [
          {
            "workOrderDate": "Integer",
            "processDate": "Integer",
            "production_line_no": "String",
            "productionLineName": "String",
            "station_no": "String",
            "stationName": "String",
            "stationStage": "Integer",
            "employee_no": "String",
            "employeeName": "String",
            "employeeType": "Integer",
            "employeeJobTitle": "String"
          }
        ],
        "machines": [
          {
            "time": "Integer",
            "workOrderDate": "Integer",
            "production_line_no": "String",
            "productionLineName": "String",
            "processDate": "Integer",
            "station_no": "String",
            "stationName": "String",
            "stationStage": "Integer",
            "equipment_no": "String",
            "equipmentName": "String"
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
| payload.results[].input[].workOrderDate | Integer | 派工日期 |  |
| payload.results[].input[].production_line_no | String | 產線編號 |  |
| payload.results[].input[].productionLineName | String | 產線名稱 |  |
| payload.results[].input[].processDate | Integer | 產製日期 |  |
| payload.results[].input[].item_no | String | 「料品品項」編號 |  |
| payload.results[].input[].item_name | String | 「料品品項」名稱 |  |
| payload.results[].input[].itemCategory | Integer | 「料品品項」類別 |  |
| payload.results[].input[].itemSubCategory | Integer | 「料品品項」子類別 |  |
| payload.results[].input[].itemType | Integer | 「料品品項」型態 |  |
| payload.results[].input[].batch_number | String | 批號 |  |
| payload.results[].input[].unit | Integer | 單位 |  |
| payload.results[].input[].count | Integer | 數量 |  |
| payload.results[].input[].validDate | String | 效期日期 |  |
| payload.results[].output[].workOrderDate |Integer | 派工日期 |  |
| payload.results[].output[].production_line_no | String | 產線編號 |  |
| payload.results[].output[].productionLineName | String | 產線名稱 |  |
| payload.results[].output[].processDate | Integer | 產製日期 |  |
| payload.results[].output[].item_no | String | 「料品品項」編號 |  |
| payload.results[].output[].item_name | String | 「料品品項」名稱 |  |
| payload.results[].output[].itemCategory | Integer | 「料品品項」類別 |  |
| payload.results[].output[].itemSubCategory | Integer | 「料品品項」子類別 |  |
| payload.results[].output[].itemType | Integer | 「料品品項」型態 |  |
| payload.results[].output[].batch_number | String | 批號 |  |
| payload.results[].output[].validDate | String | 效期日期 |  |
| payload.results[].output[].unit | Integer | 單位 |  |
| payload.results[].output[].count | Float | 數量 |  |
| payload.results[].reuse[].workOrderDate | Integer | 派工日期 |  |
| payload.results[].reuse[].production_line_no | String | 產線編號 |  |
| payload.results[].reuse[].productionLineName | String | 產線名稱 |  |
| payload.results[].reuse[].processDate | Integer | 產製日期 |  |
| payload.results[].reuse[].item_no | String | 「料品品項」編號 |  |
| payload.results[].reuse[].item_name | String | 「料品品項」名稱 |  |
| payload.results[].reuse[].itemCategory | Integer | 「料品品項」類別 |  |
| payload.results[].reuse[].itemSubCategory | Integer | 「料品品項」子類別 |  |
| payload.results[].reuse[].itemType | Integer | 「料品品項」型態 |  |
| payload.results[].reuse[].batch_number | String | 批號 |  |
| payload.results[].reuse[].validDate | String | 效期日期 |  |
| payload.results[].reuse[].unit | Integer | 單位 |  |
| payload.results[].reuse[].count | Float | 數量 |  |
| payload.results[].labors[].workOrderDate | Integer | 派工日期 |  |
| payload.results[].labors[].processDate |  Integer | 產製日期 |  |
| payload.results[].labors[].production_line_no | String | 產線編號 |  |
| payload.results[].labors[].productionLineName | String | 產線名稱 |  |
| payload.results[].labors[].station_no | String | 站點編號 |  |
| payload.results[].labors[].stationName | String | 站點名稱 |  |
| payload.results[].labors[].stationStage | Integer | 製程階段 | 前段 (1)、後段 (2) |
| payload.results[].labors[].employee_no | String | 員工編號 |  |
| payload.results[].labors[].employeeName | String | 員工名稱 |  |
| payload.results[].labors[].employeeType | Integer | 員工型態 | 正職 (1)、兼職 (2) |
| payload.results[].labors[].employeeJobTitle | String | 員工職稱 |  |
| payload.results[].machines[].time | Integer | 時間 |  |
| payload.results[].machines[].workOrderDate | Integer | 派工日期 |  |
| payload.results[].machines[].action | Integer | 機具狀態 | 啟動 (1) 、暫停(2)、停止 (3) |
| payload.results[].machines[].equipment_no | String | 機具編號 |  |
| payload.results[].machines[].equipmentName | String | 機具名稱 |  |
| payload.results[].machines[].production_line_no | String | 產線編號 |  |
| payload.results[].machines[].productionLineName | String | 產線名稱 |  |
| payload.results[].machines[].processDate | Integer | 產製日期 |  |
| payload.results[].machines[].station_no | String | 站點編號 |  |
| payload.results[].machines[].stationName | String | 站點名稱 |  |
| payload.results[].machines[].stationStage | Integer | 製程階段 | 前段 (1)、後段 (2) |


### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：count、start
2. 查詢 batch_number、batchno_serialno、equipment、process_labor 取得製造作業 / 作業分派資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| batch_number | 提供製造作業排程、生產或產能資料 |
| batchno_serialno | 提供製造作業排程、生產或產能資料 |
| equipment | 提供製造作業排程、生產或產能資料 |
| process_labor | 提供製造作業排程、生產或產能資料 |
| process_order | 提供製造作業排程、生產或產能資料 |
| production_line | 提供製造作業排程、生產或產能資料 |
| station | 提供製造作業排程、生產或產能資料 |
| work_order | 提供製造作業排程、生產或產能資料 |

## GET /api/v1/work/process

<a id="get-api-v1-work-process"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/work/process | GET | 查詢領退餘廢產單 |

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
        "creator_no": "String",
        "work_order_no": "String",
        "refProcess": "Integer",
        "date": "Integer",
        "category": "Integer",
        "item_no": "String",
        "item_name": "String",
        "itemCategory": "Integer",
        "itemSubCategory": "Integer",
        "item_ref_no": "String",
        "item_ref_displayName": "String",
        "unit": "Integer",
        "expectedCount": "Float",
        "count": "Float",
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
| payload.results[].creator_no | String | 製單人員編號 |  |
| payload.results[].work_order_no | String | 工單號 |  |
| payload.results[].refProcess | Integer | 派工製程 |  |
| payload.results[].date | Integer | 日期時間 |  |
| payload.results[].category | Integer | 類別 |  |
| payload.results[].item_no | String | 料「料品品項」編號 |  |
| payload.results[].item_name | String | 「料品品項」項名稱 |  |
| payload.results[].itemCategory | Integer | 「料品品項」類別 |  |
| payload.results[].itemSubCategory | Integer | 「料品品項」子類別 |  |
| payload.results[].item_ref_no | String | 交易對象編號 |  |
| payload.results[].item_ref_displayName | String | 交易對象顯示名稱 |  |
| payload.results[].unit | Integer | 單位 |  |
| payload.results[].expectedCount | Float | 預期數量 |  |
| payload.results[].count | Float | 實際數量 |  |
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
2. 查詢 batch_number、process_order 取得製造作業 / 製程資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| batch_number | 提供製造作業排程、生產或產能資料 |
| process_order | 提供製造作業排程、生產或產能資料 |

## POST /api/v1/work/process

<a id="post-api-v1-work-process"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/work/process | POST | 新增領退餘廢產單 |

### Request Header

| Header | Description |
|----------|----------|
| Content-Type | application/json |
| x-auth-token | 存取金鑰 |

### Query Parameters

None

### Request Body

```json
{
  "start_time": "Integer",
  "end_time": "Integer"
}
```

| Field Path | Type | Required | Description | Enum |
|----------|----------|------|-----|---|
| start_time | Integer | YES | 查詢開始時間 |  |
| end_time | Integer | YES | 查詢結束時間 |  |

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

1. 驗證 request body 必填欄位與資料格式：start_time、end_time
2. 建立製造作業 / 製程資料
3. 回傳建立結果與必要識別資訊

### Database Tables Used

| Table | Purpose |
|----------|------|
| work_order | 提供製造作業排程、生產或產能資料 |

## GET /api/v1/work/productdata

<a id="get-api-v1-work-productdata"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/work/productdata | GET | 查詢訂單生產數據 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| product_order_no | String | YES | 訂單編號 |
| oneProcess | Integer | YES | 主製程 |
### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
    "payload": {
        "productLine": [
          {
              "name": "String",
              "count": "Integer",
          }
        ],
        "productData": [
          {
            "oneProcess": "Integer",
            "secProcess": "Integer",
            "input": [
              {
                "item_name": "String",
                "itemCategory": "Integer",
                "itemSubCategory": "Integer",
                "count": "Float",
                "bomCount": "Float",
                "loss": "Float",
                "bomLoss": "Float"
              }
            ],
            "output": [
              {
                "item_name": "String",
                "itemCategory": "Integer",
                "itemSubCategory": "Integer",
                "bom": {
                    "count": "Float",
                    "price": "Float",
                    "hours": "Float", 
                    "hourlyCount": "Float",
                    "rawMaterialCost": "Float",
                    "materialCost": "Float",
                    "laborCost": "Float",
                },
                "product": {
                    "count": "Float",
                    "price": "Float",
                    "hours": "Float", 
                    "hourlyCount": "Float",
                    "rawMaterialCost": "Float",
                    "materialCost": "Float",
                    "laborCost": "Float",
                }
              }
            ],
            "labors": [
              {
                "workPreHours": "Float",
                "workPostHours": "Float",
                "workPreCount": "Integer",
                "workPostCount": "Integer",
                "restPreHours": "Float",
                "restPostHours":"Float",
                "restPreCount": "Integer",
                "restPostCount": "Integer",
                "cleanPreHours": "Float",
                "cleanPostHours": "Float",
                "cleanPreCount": "Integer",
                "cleanPostCount": "Integer",
                "employeeLevel":  "Integer"
              }
            ]
          }
        ],
        "records": {
            "input": [
              {
                "workOrderDate": "Integer",
                "item_no": "String",
                "item_name": "String",
                "itemCategory": "Integer",
                "itemSubCategory": "Integer",
                "batch_number": "String",
                "itemType": "Integer",
                "validDate": "Integer",
                "warehouses": [
                    {
                        "date": "Integer",
                        "warehouse_no": "String",
                        "warehouse_displayName": "String",
                        "unit": "Integer",
                        "count": "Float",
                        "packCount": "Integer"
                    }
                ]
              }
            ],
            "output": [
              {
                "workOrderDate": "Integer",
                "item_no": "String",
                "item_name": "String",
                "itemCategory": "Integer",
                "itemSubCategory": "Integer",
                "batch_number": "String",
                "itemType": "Integer",
                "validDate": "Integer",
                "warehouses": [
                    {
                        "date": "Integer",
                        "warehouse_no": "String",
                        "warehouse_displayName": "String",
                        "unit": "Integer",
                        "count": "Float",
                        "packCount": "Integer",
                    }
                ]
              }       
            ]
        }
    }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.productLine[].name | String | 產線名稱 |  |
| payload.productLine[].count | Integer | 產製次數 |  |
| payload.productData[].oneProcess | Integer | 主製程 |  |
| payload.productData[].secProcess | Integer | 次製程 |  |
| payload.productData[].input[].item_name | String | 「料品品項」名稱 |  |
| payload.productData[].input[].itemCategory | Integer | 「料品品項」類別 |  |
| payload.productData[].input[].itemSubCategory | Integer | 「料品品項」子類別 |  |
| payload.productData[].input[].count | Float | 數量 |  |
| payload.productData[].input[].bomCount | Float | 配方;數量 |  |
| payload.productData[].input[].loss | Float | 損耗 |  |
| payload.productData[].input[].bomLoss | Float | 配方;損耗 |  |
| payload.productData[].output[].item_name | String | 「料品品項」名稱 |  |
| payload.productData[].output[].itemCategory | Integer | 「料品品項」類別 |  |
| payload.productData[].output[].itemSubCategory | Integer | 「料品品項」子類別 |  |
| payload.productData[].output[].bom.count | Float | 配方;產出量 |  |
| payload.productData[].output[].bom.price | Float | 配方;單價 |  |
| payload.productData[].output[].bom.hours | Float | 配方;總時數 |  |
| payload.productData[].output[].bom.hourlyCount | Float | 配方;時產量 |  |
| payload.productData[].output[].bom.rawMaterialCost | Float | 配方;原料費 |  |
| payload.productData[].output[].bom.materialCost | Float | 配方;物料費 |  |
| payload.productData[].output[].bom.laborCost | Float | 配方;人工費 |  |
| payload.productData[].output[].product.count | Float | 量產;產出量 |  |
| payload.productData[].output[].product.price | Float | 量產;單價 |  |
| payload.productData[].output[].product.hours | Float | 量產;總時數 |  |
| payload.productData[].output[].product.hourlyCount | Float | 量產;時產量 |  |
| payload.productData[].output[].product.rawMaterialCost | Float | 量產;原料費 |  |
| payload.productData[].output[].product.materialCost | Float | 量產;物料費 |  |
| payload.productData[].output[].product.laborCost | Float | 量產;人工費 |  |
| payload.productData[].labors[].workPreHours | Float | 前段工作時數 |  |
| payload.productData[].labors[].workPostHours | Float | 後段工作時數 |  |
| payload.productData[].labors[].workPreCount | Integer | 前段工作人數 | |
| payload.productData[].labors[].workPostCount | Integer | 後段工作人數 |  |
| payload.productData[].labors[].restPreHours | Float | 前段休息時數 |  |
| payload.productData[].labors[].restPostHours | Float | 後段休息時數 |  |
| payload.productData[].labors[].restPreCount | Integer | 前段休息人數 | |
| payload.productData[].labors[].restPostCount | Integer | 後段休息人數 |  |
| payload.productData[].labors[].cleanPreHours | Float | 前段清潔時數 |  |
| payload.productData[].labors[].cleanPostHours | Float | 後段清潔時數 |  |
| payload.productData[].labors[].cleanPreCount | Integer | 前段清潔人數 | |
| payload.productData[].labors[].cleanPostCount | Integer | 後段清潔人數 |  |
| payload.productData[].labors[].employeeLevel | Integer | 員工階級 |  |
| payload.records[].input[].workOrderDate | Integer | 派工日期 |  |
| payload.records[].input[].item_no | String | 「料品品項」編號 |  |
| payload.records[].input[].item_name | String | 「料品品項」名稱 |  |
| payload.records[].input[].itemCategory | Integer | 「料品品項」類別 |  |
| payload.records[].input[].itemSubCategory | Integer | 「料品品項」子類別 |  |
| payload.records[].input[].itemType | Integer | 「料品品項」型態 |  |
| payload.records[].input[].batch_number | String | 批號 |  |
| payload.records[].input[].validDate | Integer | 效期日期 |  |
| payload.records[].input[].warehouses[].date | Integer | 日期 |  |
| payload.records[].input[].warehouses[].warehouse_no | String | 倉儲編號 |  |
| payload.records[].input[].warehouses[].warehouse_displayName | String | 倉儲簡稱 |  |
| payload.records[].input[].warehouses[].unit | Integer | 單位 |  |
| payload.records[].input[].warehouses[].count | Float | 數量 |  |
| payload.records[].input[].warehouses[].packCount | Integer | 板數 |  |
| payload.records[].ourput[].workOrderDate | Integer | 派工日期 |  |
| payload.records[].ourput[].item_no | String | 「料品品項」編號 |  |
| payload.records[].ourput[].item_name | String | 「料品品項」名稱 |  |
| payload.records[].ourput[].itemCategory | Integer | 「料品品項」類別 |  |
| payload.records[].ourput[].itemSubCategory | Integer | 「料品品項」子類別 |  |
| payload.records[].ourput[].itemType | Integer | 「料品品項」型態 |  |
| payload.records[].ourput[].batch_number | String | 批號 |  |
| payload.records[].ourput[].validDate | Integer | 效期日期 |  |
| payload.records[].ourput[].warehouses[].date | Integer | 日期 |  |
| payload.records[].ourput[].warehouses[].warehouse_no | String | 倉儲編號 |  |
| payload.records[].ourput[].warehouses[].warehouse_displayName | String | 倉儲簡稱 |  |
| payload.records[].ourput[].warehouses[].unit | Integer | 單位 |  |
| payload.records[].ourput[].warehouses[].count | Float | 數量 |  |
| payload.records[].ourput[].warehouses[].packCount | Integer | 板數 |  |


### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：count、start、type
2. 查詢 employee、production_line、station、work_order 取得製造作業 / 生產數據資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| employee | 提供製造作業排程、生產或產能資料 |
| production_line | 提供製造作業排程、生產或產能資料 |
| station | 提供製造作業排程、生產或產能資料 |
| work_order | 提供製造作業排程、生產或產能資料 |

## GET /api/v1/work/progress

<a id="get-api-v1-work-progress"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/work/progress | GET | 查詢訂單製造進度 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| oneProcess | String | YES | 主製程 |
| product_order_no | String | YES | 訂購單號 |

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
        "oneProcess": "Integer",
        "secProcess": "Integer",
        "item_name": "String",
        "itemCategory": "Integer",
        "itemSubCategory": "Integer",
        "bom": {
          "count": "Integer",
          "amount": "Float",
          "hours": "Float"
        },
        "product": {
          "count": "Integer",
          "amount": "Float",
          "hours": "Float"
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
| payload.results[].oneProcess | Integer | 主製程 |  |
| payload.results[].secProcess | Integer | 次製程 |  |
| payload.results[].item_name | String | 「料品品項」名稱 |  |
| payload.results[].itemCategory | Integer | 「料品品項」類別 |  |
| payload.results[].itemSubCategory | Integer | 「料品品項」子類別 |  |
| payload.results[].bom.count | Integer | 排定;總產次 |  |
| payload.results[].bom.amount | Float | 排定;總產量 |  |
| payload.results[].bom.hours | Float | 排定;總時數 |  |
| payload.results[].product.count | Integer | 進度;已產次 |  |
| payload.results[].product.amount | Float | 進度;已產量 |  |
| payload.results[].product.hours | Float | 進度;已產時 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：oneProcess、product_order_no
2. 查詢 aps_quantity、inproduct、product、production_data 取得製造作業 / 作業進度資料
3. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| aps_quantity | 提供製造作業排程、生產或產能資料 |
| inproduct | 提供製造作業排程、生產或產能資料 |
| product | 提供製造作業排程、生產或產能資料 |
| production_data | 提供製造作業排程、生產或產能資料 |
| production_data_output | 提供製造作業排程、生產或產能資料 |
