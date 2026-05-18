# EWDB_20260517_3 Final Check

日期：2026-05-17  
檢查檔案：`docs/database/EWDB_20260517_3.sql`

## 結論

`EWDB_20260517_3.sql` 可以作為後續開發基準。

相較 `EWDB_20260517_2.sql`，前一版發現的 6 筆 FK 型別阻塞問題已修正：

- `company.received_id` 已可對應 `payment.id`
- `company.paid_id` 已可對應 `payment.id`
- `contract.payment_id` 已可對應 `payment.id`
- `inventory_delta.in_ref_id` 不再建立不合理 FK
- `inventory_delta.out_ref_id` 不再建立不合理 FK
- `production_line.factory_no` 與 `factory.no` 型別已相容

## 檢查結果

| Item | Result |
|---|---:|
| Tables | 75 |
| Primary Keys | 75 |
| Unique Keys | 69 |
| Foreign Keys | 117 |
| Tables with multiple unique keys | 0 |
| Unique key nullable violations | 0 |
| FK missing table/field | 0 |
| Fatal FK type issues | 0 |
| Workflow missing tables | 0 |

## UNIQUE KEY 檢查

通過。

- 每張表最多一組 `UNIQUE KEY`
- 所有 `UNIQUE KEY` 欄位皆為 `NOT NULL`
- 多欄位 unique key 已使用 composite unique key 表達

## FK 檢查

通過。

- FK 來源欄位與目標欄位皆存在
- 未發現致命型別不相容
- 117 筆 FK 的目標欄位皆有可用索引
- 其中 82 筆目標為單欄 PK 或單欄 UK
- 其餘 35 筆目標為 composite unique key 的第一欄，仍可作為 InnoDB FK 目標索引依據

## Workflow 覆蓋

依 `EWDB_WORKFLOW_20260517.md` 檢查，下列流程所需資料表皆存在。

### 訂單到生產

`quotation -> contract -> product_order -> aps_quantity -> work_order -> process_order -> process_labor`

### 採購到入庫

`product_order -> purchase_request -> purchase_request_item -> purchase_order -> goods_receipt_note -> batch_number -> inventory_record`

### 生產報工

`work_order -> production_data -> production_data_input/output/reuse/machine/labor`

並包含：

`production_line -> station -> equipment`

## 後續建議

可進入下一步：

1. 將 `EWDB_20260517_3.sql` 設為目前最終 DB schema baseline。
2. 建立 SQLAlchemy models。
3. 建立 Alembic initial migration。
4. 依 `EWDB_WORKFLOW_20260517.md` 建立 workflow API 與閉環測試。
