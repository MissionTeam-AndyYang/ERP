# EWDB_20260517_2 Final Check

日期：2026-05-17  
檢查檔案：`docs/database/EWDB_20260517_2.sql`

## 結論

`EWDB_20260517_2.sql` 尚不建議直接視為最終可執行資料庫檔。

它已通過大部分結構規則，但仍有 6 筆 FK 欄位型別不相容，若直接匯入 MariaDB/MySQL 並建立 FK，可能會失敗。

## 通過項目

- Table 數量：75
- Primary Key 數量：75
- Unique Key 數量：68
- Foreign Key 數量：119
- 每張表最多一組 `UNIQUE KEY`：通過
- `UNIQUE KEY` 欄位皆為 `NOT NULL`：通過
- `EWDB_WORKFLOW_20260517.md` 內的核心 workflow table：全部存在

## 需修正項目

以下 6 筆 FK 欄位型別不相容：

| From | From type | To | To type | 問題 |
|---|---|---|---|---|
| `company.received_id` | `INT` | `payment.id` | `BIGINT UNSIGNED` | integer size/sign 不一致 |
| `company.paid_id` | `INT` | `payment.id` | `BIGINT UNSIGNED` | integer size/sign 不一致 |
| `contract.payment_id` | `INT` | `payment.id` | `BIGINT UNSIGNED` | integer size/sign 不一致 |
| `inventory_delta.in_ref_id` | `LONGTEXT` | `inventory_record.id` | `BIGINT UNSIGNED` | JSON Array / LONGTEXT 不適合直接 FK |
| `inventory_delta.out_ref_id` | `LONGTEXT` | `inventory_record.id` | `BIGINT UNSIGNED` | JSON Array / LONGTEXT 不適合直接 FK |
| `production_line.factory_no` | `VARCHAR(60)` | `factory.no` | `BIGINT UNSIGNED` | 字串欄位指向數字 PK |

## 建議修正

### 1. Payment FK

建議將以下欄位改為 `BIGINT UNSIGNED`：

- `company.received_id`
- `company.paid_id`
- `contract.payment_id`

或改設計為 reference payment business key，但目前 `payment` 沒有 `no` 欄位，所以短期以 `BIGINT UNSIGNED` 最合理。

### 2. Inventory Delta JSON Array

`inventory_delta.in_ref_id` 與 `inventory_delta.out_ref_id` 的 Word 說明是 JSON Array，且型別為 `LONGTEXT`。

建議不要建立實體 FK。可選方案：

- 保留 `LONGTEXT`，移除這兩條 FK。
- 新增關聯表，例如 `inventory_delta_in_records`、`inventory_delta_out_records`，用 `inventory_delta_id` + `inventory_record_id` 建立正規 FK。

短期建議：先移除 FK。

### 3. Factory FK

目前：

- `factory.no` 是 `BIGINT UNSIGNED NOT NULL AUTO_INCREMENT`
- `production_line.factory_no` 是 `VARCHAR(60)`

建議二選一：

1. 將 `production_line.factory_no` 改為 `BIGINT UNSIGNED`。
2. 將 `factory.no` 改為 `VARCHAR(60)`，並另外新增 `id BIGINT UNSIGNED AUTO_INCREMENT` 作技術 PK。

若要維持目前結構，短期建議改 `production_line.factory_no` 為 `BIGINT UNSIGNED`。

## Workflow 覆蓋

依 `EWDB_WORKFLOW_20260517.md` 檢查，下列流程涉及的資料表都存在：

- 訂單到生產：`quotation`, `contract`, `product_order`, `aps_quantity`, `work_order`, `process_order`, `process_labor`
- 採購到入庫：`product_order`, `purchase_request`, `purchase_request_item`, `purchase_order`, `goods_receipt_note`, `batch_number`, `inventory_record`
- 生產報工：`work_order`, `production_data`, `production_data_input`, `production_data_output`, `production_data_reuse`, `production_data_machine`, `production_data_labor`, `production_line`, `station`, `equipment`

## 判定

狀態：需要小修後才建議作為最終資料庫檔。

建議下一步：

產出 `EWDB_20260517_2_FIXED.sql`，只修正上述 6 筆 FK 問題，不改動其他已確認的 UNIQUE KEY 與 workflow 結構。
