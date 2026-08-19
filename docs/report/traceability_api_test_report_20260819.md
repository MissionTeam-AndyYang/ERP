# Traceability API Test Report 2026-08-19

## Scope

- `GET /api/v2/trace/dashboard`
- `GET /api/v2/trace/batches/{batch_no}/overview`

## Verification Items

| Item | Result |
| --- | --- |
| Dashboard response fields match formal API document | PASS |
| Trace graph nodes / edges include confirmed production input and output relations | PASS |
| Quality hold and expired batch risk codes are returned as enum values | PASS |
| Invalid batch number returns no payload for API wrapper handling | PASS |

## Command

```powershell
.\.venv\Scripts\python.exe -m pytest restserver\tests\test_traceability_api.py -q
.\.venv\Scripts\python.exe -m pytest restserver\tests\test_traceability_api.py restserver\tests\test_batch_center_api.py -q
.\.venv\Scripts\python.exe -c "import sys; sys.path.insert(0, 'restserver'); from package.restserver.app import create_app; app=create_app(); print('\n'.join(sorted([str(rule) for rule in app.url_map.iter_rules() if '/api/v2/trace' in str(rule)])))"
```

## Result

```txt
3 passed in 0.80s
7 passed in 1.04s
/api/v2/trace/batches/<batch_no>/overview
/api/v2/trace/dashboard
```
