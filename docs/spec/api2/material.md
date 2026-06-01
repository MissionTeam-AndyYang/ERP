# material API Group

> Source: `restserver/package/restserver/api/material_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v1/material](#get-api-v1-material) | GET | Need Review | Need Review | description cannot be determined from docstring or explicit schema semantics |
| [/api/v1/material](#post-api-v1-material) | POST | Need Review | Need Review | description cannot be determined from docstring or explicit schema semantics; request body schema not explicitly parsed |
| [/api/v1/material](#put-api-v1-material) | PUT | Need Review | Need Review | description cannot be determined from docstring or explicit schema semantics; request body schema not explicitly parsed |
| [/api/v1/material](#delete-api-v1-material) | DELETE | Need Review | Need Review | description cannot be determined from docstring or explicit schema semantics |
| [/api/v1/material/itemprice](#get-api-v1-material-itemprice) | GET | Need Review | Need Review | description cannot be determined from docstring or explicit schema semantics |

## GET /api/v1/material

<a id="get-api-v1-material"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/material | GET | Need Review |

### Request Header

| Header | Description |
|----------|----------|
| X_AUTH_TOKEN | Required by CAPIBase unless URI override disables token validation |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| count | String | Need Review | Derived from request.args.get usage; semantic description requires review. |
| start | String | Need Review | Derived from request.args.get usage; semantic description requires review. |
| type | String | Need Review | Derived from request.args.get usage; semantic description requires review. |

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
| payload.count | Need Review | Derived from dict_extra_data key; exact type requires runtime/code review. |  |
| payload.results | Need Review | Derived from dict_extra_data key; exact type requires runtime/code review. |  |
| payload.total | Need Review | Derived from dict_extra_data key; exact type requires runtime/code review. |  |

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
4. CAPIBase calls executor `CMaterial.get(str_timezone, str_id)` when supported.
5. Executor returns `(http_status, code, message, payload_dict)`.
6. CAPIBase wraps the result as JSON unless the URI uses a customized response.
```

### Database Tables Used

| Table | Purpose |
|----------|------|
| material | Referenced by executor source through ORM model. See `docs/spec/database/index.md#material`. |

## POST /api/v1/material

<a id="post-api-v1-material"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/material | POST | Need Review |

### Request Header

| Header | Description |
|----------|----------|
| Content-Type | application/json or multipart/form-data, enforced by CAPIBase |
| X_AUTH_TOKEN | Required by CAPIBase unless URI override disables token validation |

### Query Parameters

None

### Request Body

Need Review

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
4. CAPIBase calls executor `CMaterial.post(str_timezone, str_id)` when supported.
5. Executor returns `(http_status, code, message, payload_dict)`.
6. CAPIBase wraps the result as JSON unless the URI uses a customized response.
```

### Database Tables Used

None

## PUT /api/v1/material

<a id="put-api-v1-material"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/material | PUT | Need Review |

### Request Header

| Header | Description |
|----------|----------|
| Content-Type | application/json or multipart/form-data, enforced by CAPIBase |
| X_AUTH_TOKEN | Required by CAPIBase unless URI override disables token validation |

### Query Parameters

None

### Request Body

Need Review

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
4. CAPIBase calls executor `CMaterial.put(str_timezone, str_id)` when supported.
5. Executor returns `(http_status, code, message, payload_dict)`.
6. CAPIBase wraps the result as JSON unless the URI uses a customized response.
```

### Database Tables Used

None

## DELETE /api/v1/material

<a id="delete-api-v1-material"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/material | DELETE | Need Review |

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
4. CAPIBase calls executor `CMaterial.delete(str_timezone, str_id)` when supported.
5. Executor returns `(http_status, code, message, payload_dict)`.
6. CAPIBase wraps the result as JSON unless the URI uses a customized response.
```

### Database Tables Used

None

## GET /api/v1/material/itemprice

<a id="get-api-v1-material-itemprice"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/material/itemprice | GET | Need Review |

### Request Header

| Header | Description |
|----------|----------|
| X_AUTH_TOKEN | Required by CAPIBase unless URI override disables token validation |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| item_no | String | YES | Derived from request.args.get usage; semantic description requires review. |

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
| payload.count | Need Review | Derived from dict_extra_data key; exact type requires runtime/code review. |  |
| payload.results | Need Review | Derived from dict_extra_data key; exact type requires runtime/code review. |  |

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
4. CAPIBase calls executor `CItemPrice.get(str_timezone, str_id)` when supported.
5. Executor returns `(http_status, code, message, payload_dict)`.
6. CAPIBase wraps the result as JSON unless the URI uses a customized response.
```

### Database Tables Used

| Table | Purpose |
|----------|------|
| item_loss | Referenced by executor source through ORM model. See `docs/spec/database/index.md#item_loss`. |
| item_price | Referenced by executor source through ORM model. See `docs/spec/database/index.md#item_price`. |
