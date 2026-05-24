# ERP V1 API Contract Verification Guide

Date: 2026-05-24
Script: `scripts/verify_v1_api_contracts.py`

## Purpose

This guide explains how to verify that implemented V1 APIs return the datasets required by the API development specs.

The verification script checks:

- Endpoint can be reached.
- HTTP status is 2xx.
- Response is valid JSON.
- Response contains the required top-level datasets for the module.

It does not validate database correctness, business values or permission behavior.

## Basic Usage

Start restserver first, then run:

```powershell
python scripts/verify_v1_api_contracts.py --base-url http://127.0.0.1:5000 --module warehouse
```

Write a markdown report:

```powershell
python scripts/verify_v1_api_contracts.py --base-url http://127.0.0.1:5000 --module warehouse --output docs/backend/runtime-verification/WAREHOUSE_API_CONTRACT_20260524.md
```

Verify all V1 modules:

```powershell
python scripts/verify_v1_api_contracts.py --base-url http://127.0.0.1:5000
```

Verify selected modules:

```powershell
python scripts/verify_v1_api_contracts.py --base-url http://127.0.0.1:5000 --module warehouse --module orders --module production --module quality
```

## Supported Module Keys

| Module key | Expected aggregation endpoint |
| --- | --- |
| `warehouse` | `/api/v1/warehouse/dashboard` |
| `orders` | `/api/v1/orders/dashboard` |
| `planning` | `/api/v1/planning/dashboard` |
| `purchasing` | `/api/v1/purchasing/dashboard` |
| `quality` | `/api/v1/quality/dashboard` |
| `production` | `/api/v1/production/dashboard` |
| `traceability` | `/api/v1/traceability/dashboard` |
| `logistics` | `/api/v1/logistics/dashboard` |
| `finance` | `/api/v1/finance/dashboard` |
| `rd` | `/api/v1/rd/dashboard` |
| `workforce` | `/api/v1/workforce/dashboard` |
| `dashboard` | `/api/v1/dashboard/manager` |
| `settings` | `/api/v1/settings/dashboard` |

## Not Yet Covered Support Endpoints

These frontend service endpoints exist with mock fallback, but they are not yet formal module keys in `scripts/verify_v1_api_contracts.py`:

| Support page | Endpoint |
| --- | --- |
| Items / Item Master | `/api/v1/items/dashboard` |
| BOM / Formula | `/api/v1/bom/dashboard` |
| Batches | `/api/v1/batches/dashboard` |
| AI Center | `/api/v1/ai/dashboard` |

Add these to the verification script after their support-page API contracts are promoted into backend implementation scope.

## Expected Result During Development

Before implementation, most new endpoints may fail with HTTP 404. That is expected.

After a module is implemented, that module should pass while unfinished modules may still fail.

## Report Handling

Runtime output should be placed under:

```txt
docs/backend/runtime-verification/
```

Before committing any runtime result:

1. Confirm no DB credentials are included.
2. Confirm no customer/supplier confidential data is exposed.
3. Confirm the report is useful for code review or integration review.

## Relationship To API Specs

The required datasets are based on:

```txt
docs/frontend/api/
```

If an endpoint intentionally uses a different structure, update both:

1. The relevant API development spec.
2. `scripts/verify_v1_api_contracts.py`.
