# Restserver and Database Recheck 20260522

日期：2026-05-22

## Baseline

- Database: `docs/database/EWDB_20260522.sql`
- Workflow: `docs/database/EWDB_20260522_WORKFLOW.md`
- Backend implementation: `restserver/package`
- Branch checked: `main`

## Scope

This recheck focused on whether the latest `restserver` implementation can be treated as aligned with the EWDB 20260522 database and workflow baseline.

Checked areas:

- SQL table count, unique keys, and foreign-key count.
- SQLAlchemy ORM table names in `restserver/package/dbwrapper/table.py`.
- ORM unique constraints compared with `EWDB_20260522.sql`.
- ORM material column types compared with `EWDB_20260522.sql`.
- Python syntax compilation for `restserver/package`.
- Workflow backbone interpretation and module mapping.

## Findings And Fixes

### Fixed

| Area | Issue | Fix |
| --- | --- | --- |
| ORM table name | `CTablePurchaseRequest.__tablename__` had a trailing space: `purchase_request ` | Changed to `purchase_request` |
| ORM unique constraints | 10 unique-constraint differences from `EWDB_20260522.sql` | Aligned `company`, `bank_account`, `rw_items`, APS, product process/version, statistics, and production reuse constraints |
| ORM column types | 21 non-date material type differences from `EWDB_20260522.sql` | Aligned monetary, quantity, FK, action, version, and timestamp fields |
| Workflow doc | Backbone had typos and only a raw graph | Corrected typo and expanded workflow interpretation |

### Confirmed

- SQL baseline summary: 79 tables, 73 unique keys, 118 FK constraints.
- ORM table summary after fix: 79 tables, no missing SQL tables, no extra ORM tables, no trailing-space table names.
- ORM unique constraints: 0 mismatches against `EWDB_20260522.sql`.
- ORM material column types: 0 non-date mismatches against `EWDB_20260522.sql`.
- Syntax check: `py -m compileall -q restserver\package` passed.

## Workflow Understanding

The 20260522 workflow should be understood as a full factory transaction backbone:

1. `company`, `payment`, and item masters initialize trading and item context.
2. `quotation` and `contract` create the commercial source of demand and supply.
3. `product_order` is the sales-demand pivot.
4. Purchasing moves through request, purchase order, receiving, batch, inventory, warehouse record, and warehouse payment.
5. Production moves through APS quantity, work order, batch number, process order, labor, inventory, and production data.
6. Production data fans out to input, output, reuse, machine, and labor detail tables.
7. Shipping moves from product order to shipping order, shipping record, and shipping payment.

## Verification Limitation

Runtime import and Flask smoke testing were not completed because the current local Python environment does not have `sqlalchemy` installed. Static checks were completed without installing dependencies.

To run runtime verification later:

```powershell
cd C:\Users\andyy\Desktop\Codex-workspace\projects\ERP-2.0
py -m pip install -r restserver\package\requirements.txt
$env:PYTHONPATH='restserver'
py -c "from package.dbwrapper.table import Base; print(len(Base.metadata.tables))"
```

Database-backed API tests also require MariaDB settings from `restserver/package/config/.env.example`.
