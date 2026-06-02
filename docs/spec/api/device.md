# device API Group

> Source: `restserver/package/restserver/api/device_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [//device/register](#post-device-register) | POST | 新增設備 / register | OK | OK |

## POST //device/register

<a id="post-device-register"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| //device/register | POST | 新增設備 / register |

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
| deviceId | String | YES | deviceId 欄位 |  |
| deviceName | String | YES | deviceName 欄位 |  |
| deviceRole | Integer | YES | deviceRole 欄位 | ELocationType.STORAGE, ELocationType.PREPARING1, ELocationType.PREPARING2, ELocationType.PROCESSING, ELocationType.PACKAGING |
| deviceComment | String | YES | deviceComment 欄位 |  |

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
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.serverTimestamp | Integer | 伺服器時間戳記 |  |
| payload.serverId | String | 伺服器識別 |  |
| payload.registerNo | String | 設備註冊編號 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |

### Processing Flow

1. 驗證 request body 欄位：deviceId、deviceName、deviceRole、deviceComment
2. 查詢資料表並套用條件：device
3. 組裝回傳 payload 欄位：payload.serverTimestamp、payload.serverId、payload.registerNo

### Database Tables Used

| Table | Purpose |
|----------|------|
| device | 提供設備相關資料 |
