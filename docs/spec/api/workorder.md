# workorder API Group

> Source: `restserver/package/restserver/api/workorder_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v1/workorder](#get-api-v1-workorder) | GET | 查詢工單 | OK | OK |
| [/api/v1/workorder/expecteddata](#get-api-v1-workorder-expecteddata) | GET | 查詢工單 / 預期資料 | OK | OK |
| [/api/v1/workorder/productdata](#get-api-v1-workorder-productdata) | GET | 查詢工單 / 生產數據 | OK | OK |
| [/api/v1/workorder/statistics](#get-api-v1-workorder-statistics) | GET | 查詢工單 / 統計 | OK | OK |

## GET /api/v1/workorder

<a id="get-api-v1-workorder"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/workorder | GET | 查詢工單 |

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
  "payload": {
    "total": "Integer",
    "count": "Integer",
    "results": [
      {
        "no": "String",
        "date": "Integer",
        "product_order": "String",
        "customer_no": "String",
        "customer_displayName": "String",
        "product_no": "String",
        "product_name": "String",
        "product_package": "Integer",
        "output_item_no": "String",
        "output_item_name": "String",
        "output_item_category": "Integer",
        "output_item_subCategory": "Integer",
        "oneProcess": "Integer",
        "secProcess": "Integer",
        "product_line": "String",
        "laborCount": "Integer",
        "hours": "Float", 
        "unit":  "Integer",
        "count": "Float"
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
| payload.results[].no | String | 派工單號 |  |
| payload.results[].date | Integer | 日期 |  |
| payload.results[].product_order | String | 訂單編號 |  |
| payload.results[].customer_no | String | 客戶編號 |  |
| payload.results[].customer_displayName | String | 客戶名稱 |  |
| payload.results[].product_no | String | 「「交易品項」編號 |  |
| payload.results[].product_name | String | 「交易品項」名稱 |  |
| payload.results[].product_package | Integer | 「交易品項」類別 |  |
| payload.results[].output_item_no | String | 產出的「料品品項」編號 |  |
| payload.results[].output_item_name | String | 產出的「料品品項」名稱 |  |
| payload.results[].output_item_category | Integer | 產出的「料品品項」類別 |  |
| payload.results[].output_item_subCategory | Integer | 產出的「料品品項」子類別 |  |
| payload.results[].oneProcess | Integer | 主製程 |  |
| payload.results[].secProcess | Integer | 次製程 |  |
| payload.results[].product_line | String | 產線編號 |  |
| payload.results[].laborCount | Integer | 預估投產人數 |  |
| payload.results[].hours | Float | 預估投產時數 |  |
| payload.results[].unit | Integer | 單位 |  |
| payload.results[].count | Float | 預估生產數量 |  |
| payload.results[].comment | String | 備註 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 查詢 production_data_output、work_order 取得工單資料
2. 計算符合條件的總筆數與本次回傳筆數
3. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| production_data_output | 提供工單排程、生產或產能資料 |
| work_order | 提供工單排程、生產或產能資料 |

## GET /api/v1/workorder/expecteddata

<a id="get-api-v1-workorder-expecteddata"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/workorder/expecteddata | GET | 取得投入物/產出物預估的數量 |

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
        "workOrderDate": "Integer",
        "production_line_no": "String",
        "productionLineName": "String",
        "category": "Integer",
        "date": "Integer",
        "item_no": "String",
        "item_name": "String",
        "itemCategory": "Integer",
        "itemSubCategory": "Integer",
        "unit": "Integer",
        "totalExpectedCount": "Float",
        "batch_number": [
            {
              "batch_number": "BN1125082708",
              "validDate":  "Integer",
              "itemType":  "Integer",
              "expectedCount": "Float"
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
| payload.results[].workOrderDate | Integer | 派工日期 |  |
| payload.results[].production_line_no | String | 產線編號 |  |
| payload.results[].productionLineName | String | 產線名稱 |  |
| payload.results[].category | Integer | 類別 | 領退餘廢產單類型 | 領料 (1)、退料 (2)、餘料 (3)、廢料 (4) 、產品 (5)
| payload.results[].date | Integer | 日期 |  |
| payload.results[].item_no | String | 「「料品品項」編號 |  |
| payload.results[].item_name | String | 「「料品品項」名稱 |  |
| payload.results[].itemCategory | Integer | 「料品品項」類別 |  |
| payload.results[].itemSubCategory | Integer | 「料品品項」子類別 |  |
| payload.results[].unit | Integer | 單位 |  |
| payload.results[].totalExpectedCount | String | 總預估數量 |  |
| payload.results[].batch_number[].batch_number | String | 批號 |  |
| payload.results[].batch_number[].validDate | Integer | 效期 |  |
| payload.results[].batch_number[].itemType | Integer | 「料品品項」型態 | 新料 (1)、餘料 (2)、廢料 (3) |
| payload.results[]..batch_number[].expectedCount | String | 總預估數量 |  |
### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：count、start
2. 查詢 batch_number、batchno_serialno、process_order、production_line 取得工單 / 預期資料資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| batch_number | 提供工單排程、生產或產能資料 |
| batchno_serialno | 提供工單排程、生產或產能資料 |
| process_order | 提供工單排程、生產或產能資料 |
| production_line | 提供工單排程、生產或產能資料 |
| work_order | 提供工單排程、生產或產能資料 |

## GET /api/v1/workorder/productdata

<a id="get-api-v1-workorder-productdata"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/workorder/productdata | GET | 查詢工單 / 生產數據 |

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
    "count": "Integer",
    "results": [
      {
        "no": "String",
        "date": "Integer",
        "production_line_no": "String",
        "productionLineName": "String",
        "output_item_no": "String",
        "output_item_name": "String",
        "oneProcess": "Integer",
        "secProcess": "Integer",
        "input": [
          {
            "item_no":  "String",
            "item_name":  "String",
            "itemSubCategory":"Integer",
            "itemCategory":"Integer",
            "batch_number": "String",
            "itemType":"Integer",
            "validDate":"Integer",
            "serial_no": "String",
            "unit":"Integer",
            "subCategory":"Integer",
            "count": "Float",
            "receiveCount": "Float",
            "returnCount": "Float"
          }
        ],
        "output": [
          {
            "time":"Integer",
            "action":"Integer",
            "item_no": "String",
            "item_name": "String",
            "itemCategory":"Integer",
            "itemSubCategory":"Integer",
            "subCategory": "Integer",
            "batch_number": "String",
            "itemType": "Integer",
            "validDate": "Integer",
            "serial_no": "String",
            "unit": "Integer",
            "count": "Float",
            "bomWeight": "Float"
          }
        ],
        "reuse": [
          {
            
          }
        ],
        "labor": [
          {
            "work_order_no": "String",
            "employee_no": "String",
            "employee_name": "String",
            "employee_type": "Integer",
            "employee_jobTitle": "String",
            "employee_level": "Integer",
            "station_no": "String",
            "action": "Integer",
            "stationStage": "Integer",
            "startTime": "Integer",
            "endTime": "Integer",
            "hours": "Float",
            "productionLineNo": "String",
            "productionLineName": "String ",
            "stationName": "String"
          }
        ],
        "labors": {
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
          "laborWage": "Float"
        },
        "machine": [
          {
            "equipment_no": "String",
            "equipment_name": "String",
            "productionLineNo": "String",
            "productionLineName": "String ",
            "stationNo": "String",
            "stationName": "String",
            "stationStage": "Integer",
            "workHours": "Float",
            "workSpeed": "Float",
            "workTemperature": "Float",
            "idleHours": "Float",
            "idleSpeed": "Float",
            "idleTemperature": "Float"
          }
        ],
        "machineRec": [
          {
            "time": "Integer",
            "action": "Integer",
            "equipment_no": "String",
            "equipmentName": "String",
            "productionLineNo": "String",
            "productionLineName": "String ",
            "stationNo": "String",
            "stationName": "String",
            "stationStage": "Integer",
            "speed": "Float",
            "temperature": "Float"
          }
        ],
        "inputLoss": {
            "SFE0022003": "Float"
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
| payload.results[].no | String | 派工單編號 |  |
| payload.results[].date | String | 派工日期 |  |
| payload.results[].production_line_no | String | 產線編號 |  |
| payload.results[].productionLineName | String | 產線名稱 |  |
| payload.results[].output_item_no | String | 產出的「料品品項」編號 |  |
| payload.results[].output_item_name | String | 產出的「料品品項」名稱 |  |
| payload.results[].oneProcess | Integer | 主製程 |  |
| payload.results[].secProcess | Integer | 次製程 |  |
| payload.results[].input[].item_no | String | 「料品品項」編號 |  |
| payload.results[].input[].item_name | String | 「料品品項」名稱 |  |
| payload.results[].input[].itemCategory | Integer | 「料品品項」類別 |  |
| payload.results[].input[].itemSubCategory | Integer | 「料品品項」子類別 |  |
| payload.results[].input[].itemType | Integer | 「料品品項」型態 |  |
| payload.results[].input[].batch_number | String | 批號 |  |
| payload.results[].input[].serial_no | String | 序號 |  |
| payload.results[].input[].validDate | Integer | 效期日期 |  |
| payload.results[].input[].subCategory | Integer | 無使用, 格式統一 |  |
| payload.results[].input[].unit | Integer | 單位 |  |
| payload.results[].input[].count | Float | 投入數量 |  |
| payload.results[].input[].receiveCount | Float | 領取數量 |  |
| payload.results[].input[].returnCount | Float | 退回數量 |  |
| payload.results[].output[].time | Integer | 處理時間 |  |
| payload.results[].output[].action | Integer | 狀態 | 產製(1)、其他(0) |
| payload.results[].output[].item_no | String | 「料品品項」編號 |  |
| payload.results[].output[].item_name | String | 「料品品項」名稱 |  |
| payload.results[].output[].itemCategory | Integer | 「料品品項」類別 |  |
| payload.results[].output[].itemSubCategory | Integer | 「料品品項」子類別 |  |
| payload.results[].output[].subCategory | Integer |  無使用, 格式統一 |  |
| payload.results[].output[].itemType | Integer | 「料品品項」型態 |  |
| payload.results[].output[].batch_number | String | 批號 |  |
| payload.results[].output[].serial_no | String | 序號 |  |
| payload.results[].output[].validDate | Integer | 效期日期 |  |
| payload.results[].output[].unit | Integer | 單位 |  |
| payload.results[].output[].count | Float | 投入數量 |  |
| payload.results[].output[].bomWeight | Float | 毛重量 |  |
| payload.results[].reuse[].time | Integer | 處理時間 |  |
| payload.results[].reuse[].action | Integer | 狀態 | 產製(1)、其他(0) |
| payload.results[].reuse[].item_no | String | 「料品品項」編號 |  |
| payload.results[].reuse[].item_name | String | 「料品品項」名稱 |  |
| payload.results[].reuse[].itemCategory | Integer | 「料品品項」類別 |  |
| payload.results[].reuse[].itemSubCategory | Integer | 「料品品項」子類別 |  |
| payload.results[].reuse[].subCategory | Integer | 餘廢料子類別 |  |
| payload.results[].reuse[].itemType | Integer | 「料品品項」型態 |  |
| payload.results[].reuse[].batch_number | String | 批號 |  |
| payload.results[].reuse[].serial_no | String | 序號 |  |
| payload.results[].reuse[].validDate | Integer | 效期日期 |  |
| payload.results[].reuse[].unit | Integer | 單位 |  |
| payload.results[].reuse[].count | Float | 數量 |  |
| payload.results[].reuse[].bomWeight | Float |  無使用, 格式統一 |  |
| payload.results[].labor[].work_order_no | String | 派工單號 |  |
| payload.results[].labor[].employee_no | String | 員工編號 |  |
| payload.results[].labor[].employee_name | String | 員工名稱 |  |
| payload.results[].labor[].employee_jobTitle | String | 員工職稱 |  |
| payload.results[].labor[].employee_type | Integer | 員工型態 | 正職 (1)、兼職 (2) |
| payload.results[].labor[].employee_level | Integer | 員工階級 |  |
| payload.results[].labor[].action | Integer | 作為 | 上下班 (1) 、休息(2)、清潔 (3) |
| payload.results[].labor[].startTime | Integer | 開始時間 |  |
| payload.results[].labor[].endTime | Integer | 結束時間 |  |
| payload.results[].labor[].hours | Float | 時數 |  |
| payload.results[].labor[].productionLineNo | String | 產線編號 |  |
| payload.results[].labor[].productionLineName | String | 產線名稱 |  |
| payload.results[].labor[].station_no | String | 站點編號 |  |
| payload.results[].labor[].stationName | String | 站點名稱 |  |
| payload.results[].labor[].stationStage | Integer | 製程階段 | 前段 (1)、後段 (2) |
| payload.results[].labors.workPreHours | Float | 前段工作時數 |  |
| payload.results[].labors.workPostHours | Float | 後段工作時數 |  |
| payload.results[].labors.workPreCount | Integer | 前段工作人數 | |
| payload.results[].labors.workPostCount | Integer | 後段工作人數 |  |
| payload.results[].labors.restPreHours | Float | 前段休息時數 |  |
| payload.results[].labors.restPostHours | Float | 後段休息時數 |  |
| payload.results[].labors.restPreCount | Integer | 前段休息人數 | |
| payload.results[].labors.restPostCount | Integer | 後段休息人數 |  |
| payload.results[].labors.cleanPreHours | Float | 前段清潔時數 |  |
| payload.results[].labors.cleanPostHours | Float | 後段清潔時數 |  |
| payload.results[].labors.cleanPreCount | Integer | 前段清潔人數 | |
| payload.results[].labors.cleanPostCount | Integer | 後段清潔人數 |  |
| payload.results[].labors.laborWage | Float | 人工費用 |  |
| payload.results[].machine[].equipment_no | String | 機具編號 |  |
| payload.results[].machine[].equipment_name | String | 機具名稱 |  |
| payload.results[].machine[].productionLineNo | String | 產線編號 |  |
| payload.results[].machine[].productionLineName | String | 產線名稱 |  |
| payload.results[].machine[].station_no | String | 站點編號 |  |
| payload.results[].machine[].stationName | String | 站點名稱 |  |
| payload.results[].machine[].stationStage | Integer | 製程階段 | 前段 (1)、後段 (2) |
| payload.results[].machine[].workHours | Float | 運轉時數 |  |
| payload.results[].machine[].workSpeed | Float | 運轉速度 |  |
| payload.results[].machine[].workTemperature | Float | 運轉溫度 |  |
| payload.results[].machine[].idleHours | Float | 待機時數 |  |
| payload.results[].machine[].idleSpeed | Float | 待機速度 |  |
| payload.results[].machine[].idleTemperature | Float | 待機溫度 |  |
| payload.results[].machineRec[].time | Integer | 時間 |  |
| payload.results[].machineRec[].action | Integer | 機具狀態 | 啟動 (1) 、暫停(2)、停止 (3) |
| payload.results[].machineRec[].equipment_no | String | 機具編號 |  |
| payload.results[].machineRec[].equipment_name | String | 機具名稱 |  |
| payload.results[].machineRec[].productionLineNo | String | 產線編號 |  |
| payload.results[].machineRec[].productionLineName | String | 產線名稱 |  |
| payload.results[].machineRec[].station_no | String | 站點編號 |  |
| payload.results[].machineRec[].stationName | String | 站點名稱 |  |
| payload.results[].machineRec[].stationStage | Integer | 製程階段 | 前段 (1)、後段 (2) |
| payload.results[].machineRec[].speed | Float | 速度 |  |
| payload.results[].machineRec[].temperature | Float | 溫度 |  |
| payload.results[].inputLoss.### | Float | 「料品品項」損耗 | ###: 「料品品項」編號 |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：count、start、type
2. 查詢 employee、production_line、station、work_order 取得工單 / 生產數據資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| employee | 提供工單排程、生產或產能資料 |
| production_line | 提供工單排程、生產或產能資料 |
| station | 提供工單排程、生產或產能資料 |
| work_order | 提供工單排程、生產或產能資料 |

## GET /api/v1/workorder/statistics

<a id="get-api-v1-workorder-statistics"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/workorder/statistics | GET | 查詢工單 / 統計 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| commit | String | NO | 是否提交/確認統計條件 |
| end_time | String | NO | 查詢結束時間 |
| start_time | String | NO | 查詢開始時間 |

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "count": "Integer",
    "results": [
      {
        "date": "String",
        "oneProcess": "Integer",
        "secProcess": "Integer",
        "total": "Integer"
      }
    ]
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.count | Integer | 本次回傳筆數 |  |
| payload.results[].date | String | 日期時間 |  |
| payload.results[].oneProcess | Integer | 主製程 |  |
| payload.results[].secProcess | Integer | 次製程 |  |
| payload.results[].total | Integer | 製造次數 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 讀取查詢條件並轉換為業務篩選條件：commit、end_time、start_time
2. 取得工單 / 統計資料
3. 計算符合條件的總筆數與本次回傳筆數
4. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

None
