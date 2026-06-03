# productline API Group

> Source: `restserver/package/restserver/api/productline_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v1/productline](#get-api-v1-productline) | GET | 查詢產線 | OK | OK |
| [/api/v1/productline/equipment](#get-api-v1-productline-equipment) | GET | 查詢產線 / 設備 | OK | OK |
| [/api/v1/productline/factory](#get-api-v1-productline-factory) | GET | 查詢產線 / 廠區 | OK | OK |
| [/api/v1/productline/process](#get-api-v1-productline-process) | GET | 查詢產線 / 製程 | OK | OK |
| [/api/v1/productline/station](#get-api-v1-productline-station) | GET | 查詢產線 / 站點 | OK | OK |

## GET /api/v1/productline

<a id="get-api-v1-productline"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/productline | GET | 查詢產線 |

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
    "results": [
      {
        "factory": {
          "no": "String",
          "region": "String",
          "location": "String",
          "comment": "String"
        },
        "stations": [
          {
            "no": "String",
            "name": "String",
            "stage": "String",
            "comment": "String",
            "equipments": [
              {
                "no": "String",
                "name": "String",
                "appearance": "String",
                "comment": "String"
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
| payload.results[].factory.no | String | 資料編號 |  |
| payload.results[].factory.region | String | 地區 |  |
| payload.results[].factory.location | String | 地點 |  |
| payload.results[].factory.comment | String | 備註 |  |
| payload.results[].stations[].no | String | 資料編號 |  |
| payload.results[].stations[].name | String | 名稱 |  |
| payload.results[].stations[].stage | String | 製程階段 |  |
| payload.results[].stations[].comment | String | 備註 |  |
| payload.results[].stations[].equipments[].no | String | 資料編號 |  |
| payload.results[].stations[].equipments[].name | String | 名稱 |  |
| payload.results[].stations[].equipments[].appearance | String | 外觀尺寸 |  |
| payload.results[].stations[].equipments[].comment | String | 備註 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 查詢 production_line 取得產線資料
2. 計算符合條件的總筆數與本次回傳筆數
3. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| production_line | 提供產線排程、生產或產能資料 |

## GET /api/v1/productline/equipment

<a id="get-api-v1-productline-equipment"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/productline/equipment | GET | 查詢產線 / 設備 |

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
    "results": [
      {
        "station": {
          "no": "String",
          "name": "String",
          "stage": "String",
          "comment": "String"
        },
        "productionLine": {
          "no": "String",
          "name": "String",
          "oneProcess": "String",
          "secProcess": "String"
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
| payload.results[].station.no | String | 資料編號 |  |
| payload.results[].station.name | String | 名稱 |  |
| payload.results[].station.stage | String | 製程階段 |  |
| payload.results[].station.comment | String | 備註 |  |
| payload.results[].productionLine.no | String | 資料編號 |  |
| payload.results[].productionLine.name | String | 名稱 |  |
| payload.results[].productionLine.oneProcess | String | 主製程 |  |
| payload.results[].productionLine.secProcess | String | 次製程 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 查詢 equipment 取得產線 / 設備資料
2. 計算符合條件的總筆數與本次回傳筆數
3. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| equipment | 提供產線排程、生產或產能資料 |

## GET /api/v1/productline/factory

<a id="get-api-v1-productline-factory"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/productline/factory | GET | 查詢產線 / 廠區 |

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
    "results": [
      {}
    ]
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.total | Integer | 符合條件的總筆數 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 查詢 factory 取得產線 / 廠區資料
2. 計算符合條件的總筆數與本次回傳筆數
3. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| factory | 提供產線排程、生產或產能資料 |

## GET /api/v1/productline/process

<a id="get-api-v1-productline-process"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/productline/process | GET | 查詢產線 / 製程 |

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
    "results": [
      {}
    ]
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.total | Integer | 符合條件的總筆數 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 查詢 process 取得產線 / 製程資料
2. 計算符合條件的總筆數與本次回傳筆數
3. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| process | 提供產線排程、生產或產能資料 |

## GET /api/v1/productline/station

<a id="get-api-v1-productline-station"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/productline/station | GET | 查詢產線 / 站點 |

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
    "results": [
      {
        "productionLine": {
          "no": "String",
          "name": "String",
          "oneProcess": "String",
          "secProcess": "String"
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
| payload.results[].productionLine.no | String | 資料編號 |  |
| payload.results[].productionLine.name | String | 名稱 |  |
| payload.results[].productionLine.oneProcess | String | 主製程 |  |
| payload.results[].productionLine.secProcess | String | 次製程 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 查詢 station 取得產線 / 站點資料
2. 計算符合條件的總筆數與本次回傳筆數
3. 整理查詢結果清單並展開回傳欄位語意

### Database Tables Used

| Table | Purpose |
|----------|------|
| station | 提供產線排程、生產或產能資料 |
