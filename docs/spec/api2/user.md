# user API Group

> Source: `restserver/package/restserver/api/user_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v1/user/login](#post-api-v1-user-login) | POST | Need Review | Need Review | description cannot be determined from docstring or explicit schema semantics |
| [/api/v1/user/login](#delete-api-v1-user-login) | DELETE | Need Review | Need Review | description cannot be determined from docstring or explicit schema semantics |
| [//user/device/login](#post-user-device-login) | POST | Need Review | Need Review | description cannot be determined from docstring or explicit schema semantics |
| [//user/device/logout](#delete-user-device-logout) | DELETE | Need Review | Need Review | description cannot be determined from docstring or explicit schema semantics |

## POST /api/v1/user/login

<a id="post-api-v1-user-login"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/user/login | POST | Need Review |

### Request Header

| Header | Description |
|----------|----------|
| Content-Type | application/json or multipart/form-data, enforced by CAPIBase |
| X_AUTH_TOKEN | Not required by URI override for this method |

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
| username | String | Need Review | Derived from JSON schema field name; semantic description requires review. |  |
| password | String | Need Review | Derived from JSON schema field name; semantic description requires review. |  |

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": "Object"
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API result code |  |
| message | String | API result message |  |
| payload | Object | Response payload object |  |
| payload.token | Need Review | Derived from dict_extra_data key; exact type requires runtime/code review. |  |
| payload.user | Need Review | Derived from dict_extra_data key; exact type requires runtime/code review. |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | Error code returned by CAPIBase or executor |  |
| message | String | Error message returned by CAPIBase or executor |  |
| payload | Object | Error payload; usually empty unless executor returns extra data |  |

### Processing Flow

```
1. Flask route handler instantiates the URI class.
2. URI class delegates request handling to CAPIBase.run().
3. CAPIBase performs content-type, body, token, and alive-time checks according to URI overrides.
4. CAPIBase calls executor `CLogin.post(str_timezone, str_id)` when supported.
5. Executor returns `(http_status, code, message, payload_dict)`.
6. CAPIBase wraps the result as JSON unless the URI uses a customized response.
```

### Database Tables Used

| Table | Purpose |
|----------|------|
| session | Referenced by executor source through ORM model. See `docs/spec/database/index.md#session`. |

## DELETE /api/v1/user/login

<a id="delete-api-v1-user-login"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/user/login | DELETE | Need Review |

### Request Header

| Header | Description |
|----------|----------|
| X_AUTH_TOKEN | Required by CAPIBase unless URI override disables token validation |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| token | String | Need Review | Derived from request.args.get usage; semantic description requires review. |

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": "Object"
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API result code |  |
| message | String | API result message |  |
| payload | Object | Response payload object |  |
| payload | Object | Payload structure is empty or dynamic in code; confirm with runtime sample if frontend uses it. |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | Error code returned by CAPIBase or executor |  |
| message | String | Error message returned by CAPIBase or executor |  |
| payload | Object | Error payload; usually empty unless executor returns extra data |  |

### Processing Flow

```
1. Flask route handler instantiates the URI class.
2. URI class delegates request handling to CAPIBase.run().
3. CAPIBase performs content-type, body, token, and alive-time checks according to URI overrides.
4. CAPIBase calls executor `CLogin.delete(str_timezone, str_id)` when supported.
5. Executor returns `(http_status, code, message, payload_dict)`.
6. CAPIBase wraps the result as JSON unless the URI uses a customized response.
```

### Database Tables Used

None

## POST //user/device/login

<a id="post-user-device-login"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| //user/device/login | POST | Need Review |

### Request Header

| Header | Description |
|----------|----------|
| Content-Type | application/json or multipart/form-data, enforced by CAPIBase |
| X_AUTH_TOKEN | Not required by URI override for this method |

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
| registerNo | String | YES | Derived from JSON schema field name; semantic description requires review. |  |
| username | String | YES | Derived from JSON schema field name; semantic description requires review. |  |
| password | String | YES | Derived from JSON schema field name; semantic description requires review. |  |

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": "Object"
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API result code |  |
| message | String | API result message |  |
| payload | Object | Response payload object |  |
| payload.serverId | Need Review | Derived from dict_extra_data key; exact type requires runtime/code review. |  |
| payload.serverTimestamp | Need Review | Derived from dict_extra_data key; exact type requires runtime/code review. |  |
| payload.user | Need Review | Derived from dict_extra_data key; exact type requires runtime/code review. |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | Error code returned by CAPIBase or executor |  |
| message | String | Error message returned by CAPIBase or executor |  |
| payload | Object | Error payload; usually empty unless executor returns extra data |  |

### Processing Flow

```
1. Flask route handler instantiates the URI class.
2. URI class delegates request handling to CAPIBase.run().
3. CAPIBase performs content-type, body, token, and alive-time checks according to URI overrides.
4. CAPIBase calls executor `CDeviceLogin.post(str_timezone, str_id)` when supported.
5. Executor returns `(http_status, code, message, payload_dict)`.
6. CAPIBase wraps the result as JSON unless the URI uses a customized response.
```

### Database Tables Used

| Table | Purpose |
|----------|------|
| employee | Referenced by executor source through ORM model. See `docs/spec/database/index.md#employee`. |
| session | Referenced by executor source through ORM model. See `docs/spec/database/index.md#session`. |

## DELETE //user/device/logout

<a id="delete-user-device-logout"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| //user/device/logout | DELETE | Need Review |

### Request Header

| Header | Description |
|----------|----------|
| X_AUTH_TOKEN | Required by CAPIBase unless URI override disables token validation |

### Query Parameters

None

### Request Body

None

### Success Response Data

```json
{
  "code": "Integer",
  "message": "String",
  "payload": "Object"
}
```

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | API result code |  |
| message | String | API result message |  |
| payload | Object | Response payload object |  |
| payload | Object | Payload structure is empty or dynamic in code; confirm with runtime sample if frontend uses it. |  |

### Failed Response Data

| Field Path | Type | Description | Enum |
|----------|----------|------|---|
| code | Integer | Error code returned by CAPIBase or executor |  |
| message | String | Error message returned by CAPIBase or executor |  |
| payload | Object | Error payload; usually empty unless executor returns extra data |  |

### Processing Flow

```
1. Flask route handler instantiates the URI class.
2. URI class delegates request handling to CAPIBase.run().
3. CAPIBase performs content-type, body, token, and alive-time checks according to URI overrides.
4. CAPIBase calls executor `CDeviceLogout.delete(str_timezone, str_id)` when supported.
5. Executor returns `(http_status, code, message, payload_dict)`.
6. CAPIBase wraps the result as JSON unless the URI uses a customized response.
```

### Database Tables Used

None
