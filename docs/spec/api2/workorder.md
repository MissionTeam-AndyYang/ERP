# workorder API Group

> Source: `restserver/package/restserver/api/workorder_uri.py`

## API Summary

| URL | Method | Description | Status | Review Note |
|----------|----------|----------------|------|------|
| [/api/v1/workorder](#get-api-v1-workorder) | GET | Need Review | Need Review | description cannot be determined from docstring or explicit schema semantics |
| [/api/v1/workorder](#post-api-v1-workorder) | POST | Need Review | Need Review | description cannot be determined from docstring or explicit schema semantics; request body schema not explicitly parsed |
| [/api/v1/workorder](#put-api-v1-workorder) | PUT | Need Review | Need Review | description cannot be determined from docstring or explicit schema semantics; request body schema not explicitly parsed |
| [/api/v1/workorder](#delete-api-v1-workorder) | DELETE | Need Review | Need Review | description cannot be determined from docstring or explicit schema semantics |
| [/api/v1/workorder/productdata](#get-api-v1-workorder-productdata) | GET | Need Review | Need Review | description cannot be determined from docstring or explicit schema semantics |
| [/api/v1/workorder/expecteddata](#get-api-v1-workorder-expecteddata) | GET | Need Review | Need Review | description cannot be determined from docstring or explicit schema semantics |
| [/api/v1/workorder/statistics](#get-api-v1-workorder-statistics) | GET | Need Review | Need Review | description cannot be determined from docstring or explicit schema semantics |

## GET /api/v1/workorder

<a id="get-api-v1-workorder"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/workorder | GET | Need Review |

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
4. CAPIBase calls executor `CWorkOrder.get(str_timezone, str_id)` when supported.
5. Executor returns `(http_status, code, message, payload_dict)`.
6. CAPIBase wraps the result as JSON unless the URI uses a customized response.
```

### Database Tables Used

| Table | Purpose |
|----------|------|
| work_order | Referenced by executor source through ORM model. See `docs/spec/database/index.md#work_order`. |

## POST /api/v1/workorder

<a id="post-api-v1-workorder"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/workorder | POST | Need Review |

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
4. CAPIBase calls executor `CWorkOrder.post(str_timezone, str_id)` when supported.
5. Executor returns `(http_status, code, message, payload_dict)`.
6. CAPIBase wraps the result as JSON unless the URI uses a customized response.
```

### Database Tables Used

None

## PUT /api/v1/workorder

<a id="put-api-v1-workorder"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/workorder | PUT | Need Review |

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
4. CAPIBase calls executor `CWorkOrder.put(str_timezone, str_id)` when supported.
5. Executor returns `(http_status, code, message, payload_dict)`.
6. CAPIBase wraps the result as JSON unless the URI uses a customized response.
```

### Database Tables Used

None

## DELETE /api/v1/workorder

<a id="delete-api-v1-workorder"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/workorder | DELETE | Need Review |

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
4. CAPIBase calls executor `CWorkOrder.delete(str_timezone, str_id)` when supported.
5. Executor returns `(http_status, code, message, payload_dict)`.
6. CAPIBase wraps the result as JSON unless the URI uses a customized response.
```

### Database Tables Used

None

## GET /api/v1/workorder/productdata

<a id="get-api-v1-workorder-productdata"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/workorder/productdata | GET | Need Review |

### Request Header

| Header | Description |
|----------|----------|
| X_AUTH_TOKEN | Required by CAPIBase unless URI override disables token validation |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| count | Integer | Need Review | Derived from request.args.get usage; semantic description requires review. |
| start | Integer | Need Review | Derived from request.args.get usage; semantic description requires review. |
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
4. CAPIBase calls executor `CProductData.get(str_timezone, str_id)` when supported.
5. Executor returns `(http_status, code, message, payload_dict)`.
6. CAPIBase wraps the result as JSON unless the URI uses a customized response.
```

### Database Tables Used

| Table | Purpose |
|----------|------|
| production_line | Referenced by executor source through ORM model. See `docs/spec/database/index.md#production_line`. |
| work_order | Referenced by executor source through ORM model. See `docs/spec/database/index.md#work_order`. |

## GET /api/v1/workorder/expecteddata

<a id="get-api-v1-workorder-expecteddata"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/workorder/expecteddata | GET | Need Review |

### Request Header

| Header | Description |
|----------|----------|
| X_AUTH_TOKEN | Required by CAPIBase unless URI override disables token validation |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| count | Integer | Need Review | Derived from request.args.get usage; semantic description requires review. |
| start | Integer | Need Review | Derived from request.args.get usage; semantic description requires review. |

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
4. CAPIBase calls executor `CExpectedData.get(str_timezone, str_id)` when supported.
5. Executor returns `(http_status, code, message, payload_dict)`.
6. CAPIBase wraps the result as JSON unless the URI uses a customized response.
```

### Database Tables Used

| Table | Purpose |
|----------|------|
| batch_number | Referenced by executor source through ORM model. See `docs/spec/database/index.md#batch_number`. |
| batchno_serialno | Referenced by executor source through ORM model. See `docs/spec/database/index.md#batchno_serialno`. |
| process_order | Referenced by executor source through ORM model. See `docs/spec/database/index.md#process_order`. |
| production_line | Referenced by executor source through ORM model. See `docs/spec/database/index.md#production_line`. |
| work_order | Referenced by executor source through ORM model. See `docs/spec/database/index.md#work_order`. |

## GET /api/v1/workorder/statistics

<a id="get-api-v1-workorder-statistics"></a>

### Basic Information

| URL | Method | Description |
|----------|----------|----------------|
| /api/v1/workorder/statistics | GET | Need Review |

### Request Header

| Header | Description |
|----------|----------|
| X_AUTH_TOKEN | Required by CAPIBase unless URI override disables token validation |

### Query Parameters

| Parameter | Type | Required | Description |
|----------|----------|------|-----|
| commit | String | Need Review | Derived from request.args.get usage; semantic description requires review. |
| end_time | String | Need Review | Derived from request.args.get usage; semantic description requires review. |
| start_time | String | Need Review | Derived from request.args.get usage; semantic description requires review. |

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
4. CAPIBase calls executor `CStatistic.get(str_timezone, str_id)` when supported.
5. Executor returns `(http_status, code, message, payload_dict)`.
6. CAPIBase wraps the result as JSON unless the URI uses a customized response.
```

### Database Tables Used

None
