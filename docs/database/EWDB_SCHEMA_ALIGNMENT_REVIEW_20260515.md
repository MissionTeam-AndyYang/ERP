# EWDB Schema Alignment Review

日期：2026-05-15  
來源檔案：

- `docs/database/ewdb20260515.sql`
- `docs/database/食品管理系統Database Schema_0.0.25.docx`
- `docs/database/ERP_2_0_MVP_SCHEMA_PROPOSAL.md`

## 1. 檔案讀取結果

### SQL

`ewdb20260515.sql` 可正常讀取。

- Table 數量：75
- Primary Key 數量：75
- Unique Key 數量：68
- Foreign Key 數量：0
- References 數量：0

### Word Schema

使用者提供的路徑副檔名為 `.doc`，但實際檔案為：

`食品管理系統Database Schema_0.0.25.docx`

檔案可正常解析。

- Word 內 schema table 數量：75
- 與 SQL table 名稱比對：75 / 75 完全對上
- Word 內有 `<PK>` 與 `UNIQUE KEY` 標記
- Word 內未偵測到 `<FK>`、`FK`、`Foreign Key` 或 `REFERENCES` 標記

## 2. 初步結論

這版 Word 與 SQL 的 table 層級一致性很好，代表既有設計已經有完整的業務資料範圍。

目前最大的缺口不是「缺 table」，而是：

1. SQL 沒有實體 Foreign Key。
2. Word 文件也沒有明確 FK 標記。
3. 部分欄位在 Word 與 SQL 之間有拼字或命名差異。
4. 許多關聯目前只能從欄位命名推論，例如 `company_no`、`product_no`、`order_no`、`batchNo`。
5. 若直接進入 SQLAlchemy models，必須先建立一份「關聯對照表」，否則 relationship 會不穩。

## 3. Word 與 SQL 欄位差異

以下是目前偵測到的欄位差異。`doc_only` 代表 Word 有但 SQL 沒有，`sql_only` 代表 SQL 有但 Word 沒有。

| Table | Word only | SQL only | 建議 |
|---|---|---|---|
| `aps_quantity_item` |  | `output_item_no` | 確認是否為新增欄位，若是，補回 Word 文件 |
| `batch_number` | `creator_no` | `creator_id` | 建議統一為 `creator_id` 或改成 `created_by_user_no`，避免 no/id 混用 |
| `batchno_serialno` | `vaildDate` | `validDate` | Word 拼字錯誤，建議統一為 `validDate` 或改為 `valid_date` |
| `bom2_number` |  | `category` | 確認是否為新增分類欄位，補回 Word 文件 |
| `factory` |  | `creationTime`, `id` | Word 使用 `no` 為 PK，但 SQL 多出 `id` 與 `creationTime`，需確認主鍵策略 |
| `inproduct` |  | `customer_no`, `customer_displayName`, `cost_no`, `loss_no` | SQL 比 Word 多出客戶、成本與損耗欄位，需補文件或檢查是否應拆表 |
| `inventory_item_month_statistic` |  | `specified_ref_name` | 補 Word 文件或確認是否為衍生欄位 |
| `inventory_order` |  | `amount` | 補 Word 文件 |
| `item_price` |  | `no`, `whUnitLength`, `costUnitLength`, `estWHPriceLength`, `estCostPriceLength`, `whPriceLength`, `costPriceLength` | SQL 欄位較完整，建議重新審視價格表設計 |
| `material` |  | `type`, `supplier_no`, `supplier_displayName`, `cost_no`, `loss_no` | 建議補文件，並確認供應商欄位是否應 FK 到 company/supplier |
| `order_payment` |  | `balance` | 補 Word 文件 |
| `process_capacity` | `comment` | `commnet` | SQL 拼字錯誤，建議 migration 時修正為 `comment` |
| `process_flow` | `id` |  | Word 有 id，但 SQL 目前 PK 是 `no`，需確認主鍵策略 |
| `product_spec` |  | `expectedLoss`, `actualLoss` | 補 Word 文件 |
| `product_ver` | `id` |  | Word 有 id，但 SQL 目前 PK 是 `no`，需確認主鍵策略 |
| `production_data` |  | `comment` | 補 Word 文件 |
| `production_data_reuse` | `group` |  | SQL 缺少 Word 欄位，需確認是否被移除；若保留，避免直接使用保留字 `group` |
| `quotation` | `id` |  | Word 有 id，但 SQL 目前 PK 是 `no`，需確認主鍵策略 |
| `sample_price` | `comment` |  | SQL 缺少 Word 欄位，需確認是否需要 |
| `shipping_payment` |  | `balance` | 補 Word 文件 |
| `station` | `productionline_no` | `production_line_no` | 建議統一為 `production_line_no` 或 `production_line_id` |
| `warehouse_payment` |  | `days`, `balance` | 補 Word 文件 |
| `warehouse_record` |  | `no`, `comment` | 補 Word 文件 |
| `work_order` | `creator_no` | `creator_id` | 建議統一建立 user/member 關聯策略 |

## 4. Table 範圍判讀

既有 schema 已涵蓋以下業務領域：

### 主資料

- `enterprise`
- `company`
- `employee`
- `member`
- `user_group`
- `factory`
- `production_line`
- `station`
- `equipment`

### 品項與 BOM

- `material`
- `inproduct`
- `product`
- `goods`
- `trans_items`
- `trans_items2`
- `product_ver`
- `product_spec`
- `product_bom_spec`
- `inproduct_bom_spec`
- `bom`
- `bom_item`
- `bom1`
- `bom1_number`
- `bom2`
- `bom2_number`

### 庫存與批號

- `batch_number`
- `batchno_serialno`
- `inventory_order`
- `inventory_record`
- `inventory_delta`
- `inventory_month_statistic`
- `inventory_item_month_statistic`

### 訂單、採購與帳款

- `quotation`
- `contract`
- `product_order`
- `shipping_order`
- `purchase_request`
- `purchase_request_item`
- `purchase_order`
- `goods_receipt_note`
- `order_payment`
- `payment`

### 物流與倉儲計費

- `ship_wh`
- `ship_wh_alias`
- `ship_wh_quotation`
- `ship_wh_contract`
- `shipping_record`
- `warehouse_record`
- `shipping_payment`
- `warehouse_payment`

### 製造與排程

- `aps_quantity`
- `aps_quantity_item`
- `work_order`
- `process`
- `process_flow`
- `process_order`
- `process_capacity`
- `process_labor`
- `product_process`
- `item_hours`
- `item_loss`
- `pl_man_capacity`
- `pl_item_capacity`
- `pl_item_loss`

### 生產數據

- `production_data`
- `production_data_output`
- `production_data_input`
- `production_data_reuse`
- `production_data_machine`
- `production_data_labor`

## 5. 與 ERP 2.0 MVP Schema 的關係

先前整理的 `ERP_2_0_MVP_SCHEMA_PROPOSAL.md` 是「乾淨版 MVP schema」，適合新系統開發。

這次提供的 `ewdb20260515.sql` 與 Word 文件則是「既有業務 schema」，業務範圍更細，但命名與關聯較鬆散。

建議不要直接用其中一份完全取代另一份，而是採用以下策略：

1. 以 `ewdb20260515.sql` 作為 legacy domain source。
2. 以 Word 文件作為欄位語意參考。
3. 以 `ERP_2_0_MVP_SCHEMA_PROPOSAL.md` 作為新系統的標準化方向。
4. Sprint 12B 先建立「核心閉環」所需 models，不一次搬完 75 張表。

## 6. 優先修正建議

### P0：先不要急著把 75 張表全部轉成 SQLAlchemy

原因：

- 目前沒有 FK。
- 部分 PK 策略不一致，例如 `id`、`no` 混用。
- 有些欄位像 `creator_no` / `creator_id`、`productionline_no` / `production_line_no` 尚未統一。
- 直接全量建 ORM 容易形成大量沒有 relationship 的 model。

### P1：先建立關聯對照表

建議新增一份文件：

`docs/database/EWDB_RELATIONSHIP_MAPPING_20260515.md`

內容包含：

| From table | From field | To table | To field | 關聯類型 | 備註 |
|---|---|---|---|---|---|
| `material` | `supplier_no` | `company` | `no` | many-to-one | 推論 |
| `work_order` | `creator_id` | `member` 或 `employee` | `id` | many-to-one | 需確認 |
| `station` | `production_line_no` | `production_line` | `no` | many-to-one | 推論 |

### P2：先修命名與拼字問題

建議優先處理：

- `commnet` -> `comment`
- `vaildDate` -> `validDate` 或 `valid_date`
- `productionline_no` -> `production_line_no`
- `creator_no` / `creator_id` 擇一
- `id` / `no` 作為 PK 的規則需明確化

### P3：再做 SQLAlchemy model 分批落地

建議 Sprint 12B 分成 4 個批次：

1. Master Data models：企業、公司、員工、使用者、品項、產線、站點、設備。
2. Inventory/BOM models：料品、產品、BOM、批號、出入庫。
3. Order/Procurement models：報價、合約、訂購、銷貨、請購、採購、進貨。
4. Production models：APS、工單、派工、報工、投入、產出、機具、人員。

## 7. 建議的下一步

下一步建議先做 Sprint 12B-1：

「建立 EWDB relationship mapping 與核心主資料 SQLAlchemy models」

交付內容：

1. 建立 `docs/database/EWDB_RELATIONSHIP_MAPPING_20260515.md`
2. 先確認以下核心關聯：
   - `company`
   - `material`
   - `inproduct`
   - `product`
   - `employee`
   - `member`
   - `factory`
   - `production_line`
   - `station`
   - `equipment`
3. 建立 SQLAlchemy models 的第一批 base module。
4. 建立 Alembic migration，但先不強制把所有 legacy FK 一次加完。

這樣可以讓後續 FastAPI + SQLAlchemy 的開發更穩，也能避免一開始就被 75 張表與大量推論關聯卡住。
