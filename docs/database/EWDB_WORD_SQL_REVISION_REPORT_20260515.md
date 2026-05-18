# EWDB Word Converted SQL vs ewdb20260515.sql Revision Report

日期：2026-05-15

## Summary

- Word tables: 75
- Existing SQL tables: 75
- Inferred FK candidates: 227
- High-confidence single-target FK candidates: 119
- Needs-review polymorphic or ambiguous FK candidates: 108

## Table Difference

- Word only tables: None
- Existing SQL only tables: None

## Field Difference

| Table | Word only fields | Existing SQL only fields | Suggested action |
|---|---|---|---|
| `aps_quantity_item` |  | output_item_no | Review and align Word/SQL before generating ORM models. |
| `batch_number` | creator_no | creator_id | Review and align Word/SQL before generating ORM models. |
| `batchno_serialno` | vaildDate | validDate | Review and align Word/SQL before generating ORM models. |
| `bom2_number` |  | category | Review and align Word/SQL before generating ORM models. |
| `factory` |  | creationTime, id | Review and align Word/SQL before generating ORM models. |
| `inproduct` |  | customer_no, customer_displayName, cost_no, loss_no | Review and align Word/SQL before generating ORM models. |
| `Inventory_item_month_statistic` |  | specified_ref_name | Review and align Word/SQL before generating ORM models. |
| `inventory_order` |  | amount | Review and align Word/SQL before generating ORM models. |
| `item_price` |  | no, whUnitLength, costUnitLength, estWHPriceLength, estCostPriceLength, whPriceLength, costPriceLength | Review and align Word/SQL before generating ORM models. |
| `material` |  | type, supplier_no, supplier_displayName, cost_no, loss_no | Review and align Word/SQL before generating ORM models. |
| `order_payment` |  | balance | Review and align Word/SQL before generating ORM models. |
| `process_capacity` | comment | commnet | Review and align Word/SQL before generating ORM models. |
| `process_flow` | id |  | Review and align Word/SQL before generating ORM models. |
| `product_spec` |  | expectedLoss, actualLoss | Review and align Word/SQL before generating ORM models. |
| `product_ver` | id |  | Review and align Word/SQL before generating ORM models. |
| `production_data` |  | comment | Review and align Word/SQL before generating ORM models. |
| `production_data_reuse` | group |  | Review and align Word/SQL before generating ORM models. |
| `quotation` | id |  | Review and align Word/SQL before generating ORM models. |
| `sample_price` | comment |  | Review and align Word/SQL before generating ORM models. |
| `shipping_payment` |  | balance | Review and align Word/SQL before generating ORM models. |
| `station` | productionline_no | production_line_no | Review and align Word/SQL before generating ORM models. |
| `warehouse_payment` |  | days, balance | Review and align Word/SQL before generating ORM models. |
| `warehouse_record` |  | no, comment | Review and align Word/SQL before generating ORM models. |
| `work_order` | creator_no | creator_id | Review and align Word/SQL before generating ORM models. |

## Existing SQL Revision Priorities

### P0: Do not apply all FK constraints automatically

Word descriptions contain useful relationship text, but some fields are polymorphic, such as references to `material / inproduct / product`. These cannot be represented by one normal MySQL FK.

### P1: Fix clear naming mismatches

- `process_capacity.commnet` should become `comment`.
- `batchno_serialno.vaildDate` in Word should become `validDate` or the SQL should move to `valid_date` in the new model.
- `station.productionline_no` in Word should align with SQL `production_line_no`.
- `creator_no` vs `creator_id` should be decided before ORM relationship design.

### P2: Add high-confidence FK constraints after data validation

Use `EWDB_WORD_INFERRED_FK_CANDIDATES_20260515.md` as the review checklist. Apply only rows marked `high` after confirming referenced values exist and target columns are unique.

### P3: Convert polymorphic references into explicit design

Fields that point to multiple tables should become either:

- `ref_type` + `ref_no` without physical FK, plus application validation; or
- separate nullable FK columns, one per target table; or
- a unified item master table, which is the cleaner ERP 2.0 direction.

## Generated Files

- Converted SQL: `docs/database/EWDB_WORD_CONVERTED_SCHEMA_20260515.sql`
- FK candidates: `docs/database/EWDB_WORD_INFERRED_FK_CANDIDATES_20260515.md`
- Revision report: `docs/database/EWDB_WORD_SQL_REVISION_REPORT_20260515.md`
