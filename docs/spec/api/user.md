# user API Group

> Source: `restserver/package/restserver/api/user_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [//user/device/login](#post-user-device-login) | POST | 使用者 / 設備 / 登入 | OK | OK |
| [//user/device/logout](#delete-user-device-logout) | DELETE | 使用者 / 設備 / 登出 | OK | OK |
| [/api/v1/user/login](#post-api-v1-user-login) | POST | 使用者 / 登入 | OK | OK |
| [/api/v1/user/login](#delete-api-v1-user-login) | DELETE | 刪除使用者 / 登入 | OK | OK |

## POST //user/device/login

<a id="post-user-device-login"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| //user/device/login | POST | 使用者 / 設備 / 登入 |

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
  "registerNo": "String",
  "username": "String",
  "password": "String"
}
```

| Field Path | Type | Required | Description | Enum |
|----------|----------|------|-----|---|
| registerNo | String | YES | 設備註冊編號 |  |
| username | String | YES | 登入帳號 |  |
| password | String | YES | 登入密碼 |  |

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "serverTimestamp": "Integer",
    "serverId": "String",
    "user": {
      "token": "String",
      "role": "Integer",
      "employee": {}
    }
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.serverTimestamp | Integer | 伺服器時間戳記 |  |
| payload.serverId | String | 伺服器識別 |  |
| payload.user.token | String | 登入 token |  |
| payload.user.role | Integer | 角色 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Object | 錯誤 payload；目前程式通常回傳空物件 |  |

### Processing Flow

1. 驗證 request body 欄位：registerNo、username、password
2. 呼叫服務：CLogger.log
3. 查詢或使用資料表：device、employee、session、user_group
4. 組裝回傳 payload 欄位：payload.serverTimestamp、payload.serverId、payload.user.token、payload.user.role

### Database Tables Used

| Table | Purpose |
|----------|------|
| device | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| employee | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| session | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
| user_group | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |

## DELETE //user/device/logout

<a id="delete-user-device-logout"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| //user/device/logout | DELETE | 使用者 / 設備 / 登出 |

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
  "payload": {}
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload | Object | 空物件或無資料 payload |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Object | 錯誤 payload；目前程式通常回傳空物件 |  |

### Processing Flow

1. 呼叫服務：CAuth.logout、CLogger.log
2. 查詢或使用資料表：session

### Database Tables Used

| Table | Purpose |
|----------|------|
| session | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |

## POST /api/v1/user/login

<a id="post-api-v1-user-login"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/user/login | POST | 使用者 / 登入 |

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
  "username": "String",
  "password": "String"
}
```

| Field Path | Type | Required | Description | Enum |
|----------|----------|------|-----|---|
| username | String | YES | 登入帳號 |  |
| password | String | YES | 登入密碼 |  |

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": {
    "token": "String",
    "user": "Object"
  }
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 回傳代碼 |  |
| message | String | API 回傳訊息 |  |
| payload.token | String | 登入 token |  |
| payload.user | Object | 使用者資訊 |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Object | 錯誤 payload；目前程式通常回傳空物件 |  |

### Processing Flow

1. 驗證 request body 欄位：username、password
2. 呼叫服務：CLogger.log
3. 查詢或使用資料表：session
4. 組裝回傳 payload 欄位：payload.token、payload.user

### Database Tables Used

| Table | Purpose |
|----------|------|
| session | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |

## DELETE /api/v1/user/login

<a id="delete-api-v1-user-login"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/user/login | DELETE | 刪除使用者 / 登入 |

### Request Header

| Header | Description |
|----------|----------|
| x-auth-token | 存取金鑰 |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| token | String | NO | 登入 token |

### Request Body

None

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
| payload | Object | 空物件或無資料 payload |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API 錯誤代碼 |  |
| message | String | API 錯誤訊息 |  |
| payload | Object | 錯誤 payload；目前程式通常回傳空物件 |  |

### Processing Flow

1. 讀取查詢條件：token
2. 呼叫服務：CAuth.logout、CLogger.log
3. 查詢或使用資料表：session

### Database Tables Used

| Table | Purpose |
|----------|------|
| session | 程式碼路徑中透過 ORM/服務邏輯使用此資料表 |
