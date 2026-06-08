# device API Group

> Source: `restserver/package/restserver/api/device_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [//device/register](#post-device-register) | POST | 設備註冊 | OK | OK |

## POST //device/register

<a id="post-device-register"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| //device/register | POST | 註冊電子智能秤設備 |

### Request Header

| Header | Description |
|----------|----------|
| Content-Type | application/json |
| x-auth-token | Not required |

### Query Parameters

None

### Request Body

```json
{
  "deviceId": "String",
  "deviceName": "String",
  "deviceRole": "Integer",
  "deviceComment": "String"
}
```

| Field Path | Type | Required | Description | Enum |
|----------|----------|------|-----|---|
| deviceId | String | YES | 設備Hardware ID |  |
| deviceName | String | YES | 設備名稱 |  |
| deviceRole | Integer | YES | 設備角色 |倉庫(1)、前備產線1(2)、前備產線2(3)、加工產線(4)、包裝產線(5)|
| deviceComment | String | YES | 設備備註訊息 |  |

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "serverTimestamp": "Integer",
    "serverId": "String",
    "registerNo": "String"
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳值 |  |
| message | String | API 回傳訊息 |  |
| payload.serverTimestamp | Integer | 伺服器時間 (UTC) |  |
| payload.serverId | String | 伺服器ID |  |
| payload.registerNo | String | 設備註冊碼 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 驗證 request body 必填欄位與資料格式
2. 建立設備註冊資料
3. 回傳結果與資訊

### Database Tables Used

| Table | Purpose |
|----------|------|
| device | 提供設備相關資料 |
