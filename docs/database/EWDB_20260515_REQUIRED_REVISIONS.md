# EWDB 20260515 修訂建議清單

日期：2026-05-15

來源：

- `docs/database/食品管理系統Database Schema_0.0.25.docx`
- `docs/database/ewdb20260515.sql`
- `docs/database/EWDB_WORD_CONVERTED_SCHEMA_20260515.sql`
- `docs/database/EWDB_WORD_INFERRED_FK_CANDIDATES_20260515.md`
- `docs/database/EWDB_WORD_SQL_REVISION_REPORT_20260515.md`

## 1. 轉換結果

已將 Word schema 轉換成 SQL 草案：

`docs/database/EWDB_WORD_CONVERTED_SCHEMA_20260515.sql`

轉換結果：

- Word table 數：75
- 既有 SQL table 數：75
- Table 名稱：完全對上
- 從 Word 描述推論出的關聯語意：227 筆
- 高信心 FK：119 筆
- 需人工確認的多目標/模糊關聯：38 筆
- 不建議作為 FK 的名稱/displayName 類欄位：70 筆

## 2. ewdb20260515.sql 必修項目

### R1：補 Foreign Key 設計

`ewdb20260515.sql` 目前沒有任何實體 FK。

建議不要一次全部套用，而是依下列順序處理：

1. 先審核 `EWDB_WORD_INFERRED_FK_CANDIDATES_20260515.md` 中標記為 `high` 的 119 筆。
2. 確認目標欄位是否唯一，例如 `no` 是否有 `UNIQUE KEY`。
3. 確認既有資料是否沒有孤兒資料。
4. 再用 Alembic migration 分批補 FK。

優先可補的 FK 類型：

- `creator_no` -> `employee.no`
- `company_no` / `item_ref_no` / `customer_no` -> `company.no`
- `product_order_no` -> `product_order.no`
- `work_order_no` -> `work_order.no`
- `production_line_no` -> `production_line.no`
- `station_no` -> `station.no`
- `equipment_no` -> `equipment.no`
- `purchase_request_no` -> `purchase_request.no`
- `purchase_order_no` -> `purchase_order.no`
- `batch_no` -> `batch_number.no`

### R2：先處理欄位命名不一致

以下差異會影響 SQLAlchemy relationship 命名，建議在補 FK 前先決定標準。

| Table | Word | ewdb20260515.sql | 建議 |
|---|---|---|---|
| `batch_number` | `creator_no` | `creator_id` | 建議統一為 `creator_no` 對 `employee.no`，或全面改為 `creator_id` 對 `employee.id` |
| `work_order` | `creator_no` | `creator_id` | 同上，需統一 |
| `batchno_serialno` | `vaildDate` | `validDate` | Word 拼字錯誤，建議統一為 `valid_date` |
| `process_capacity` | `comment` | `commnet` | SQL 拼字錯誤，建議修為 `comment` |
| `station` | `productionline_no` | `production_line_no` | 建議採用 SQL 的 `production_line_no` |
| `process_flow` | `id` | 無 | 需確認是否以 `no` 作為主鍵即可 |
| `product_ver` | `id` | 無 | 需確認是否以 `no` 作為主鍵即可 |
| `quotation` | `id` | 無 | 需確認是否以 `no` 作為主鍵即可 |

### R3：補 Word 文件缺少但 SQL 已存在的欄位

如果 `ewdb20260515.sql` 才是目前最新版，Word 文件需補回這些欄位，避免後續轉 ORM 時漏欄位。

高優先：

- `material.type`
- `material.supplier_no`
- `material.supplier_displayName`
- `material.cost_no`
- `material.loss_no`
- `inproduct.customer_no`
- `inproduct.customer_displayName`
- `inproduct.cost_no`
- `inproduct.loss_no`
- `item_price.no`
- `inventory_order.amount`
- `warehouse_record.no`
- `warehouse_record.comment`
- `production_data.comment`

### R4：多目標欄位不能直接補單一 FK

以下類型欄位在 Word 中明確指向多張表，不適合直接建立單一 MySQL FK：

- `item_no` -> `material / inproduct / product`
- `output_item_no` -> `inproduct / product`
- `ref_no` -> `goods_receipt_note / shipping_order / process_order / inventory_order`
- `specified_no` -> `material / inproduct / product / batch_number`
- `ref_parent_no` -> `product_order / purchase_order`
- `ref_sub_no` -> `goods_receipt_note / shipping_order`

建議處理方式三選一：

1. 保留 `ref_type + ref_no`，由 application layer 驗證。
2. 拆成多個 nullable FK 欄位，例如 `material_no`、`inproduct_no`、`product_no`。
3. 建立統一品項主檔，例如 ERP 2.0 的 `items`，讓原物料、在製品、製成品、貨品都能用單一 FK。

以長期 ERP 架構來看，建議採第 3 種。

## 3. 不建議作為 FK 的欄位

Word 中有許多 `xxx_name`、`xxx_displayName` 欄位寫著「關連至某資料表」，但這些比較像快照欄位或顯示冗餘欄位，不建議作為 FK。

例如：

- `customer_displayName`
- `item_ref_displayName`
- `warehouse_displayName`
- `product_name`
- `item_name`
- `employee_name`
- `equipment_name`
- `sw_alias_name`

建議：

- FK 使用 `xxx_no` 或 `xxx_id`
- `xxx_name` / `xxx_displayName` 若要保留，定位為歷史快照或顯示快取
- API response 可以透過 relationship join 回傳最新名稱

## 4. 建議修訂順序

### Step 1：確認主鍵策略

先決定新系統以哪個欄位作為主要關聯：

- Legacy 相容：使用 `no`
- ORM 標準化：使用 `id`
- 混合策略：資料表保留 `id` 作 PK，`no` 作 business key 並加 unique

建議採「混合策略」：

- `id`：資料庫內部 PK
- `no`：業務編號，保留 unique
- FK 優先指向 `id`
- 與 legacy 匯入/對帳時使用 `no`

### Step 2：修欄位命名與拼字

先處理 R2 的命名差異，避免後面 migration 與 model relationship 反覆修改。

### Step 3：補唯一索引

確認所有被 FK 指向的 `no` 欄位都有 `UNIQUE KEY`。

### Step 4：先補高信心 FK

先從主流程閉環補：

1. 訂單：`product_order`、`shipping_order`
2. 採購：`purchase_request`、`purchase_order`、`goods_receipt_note`
3. 生產：`work_order`、`process_order`、`production_data`
4. 倉儲：`batch_number`、`inventory_order`、`inventory_record`
5. 人員與產線：`employee`、`production_line`、`station`、`equipment`

### Step 5：處理多目標欄位

多目標欄位不要急著補 FK，應先決定是否導入統一 `items` 主檔。

## 5. 下一步建議

下一步建議進入：

**Sprint 12B-1：FK 審核與 Core Relationship Mapping**

交付內容：

1. 從 119 筆 high FK 中挑出第一批核心閉環 FK。
2. 建立 `EWDB_CORE_RELATIONSHIP_MAPPING_20260515.md`。
3. 決定 `id` / `no` 的最終關聯策略。
4. 產出第一批 Alembic migration 草案。
5. 再建立 SQLAlchemy models。
