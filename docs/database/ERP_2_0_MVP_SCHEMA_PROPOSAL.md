# ERP 2.0 MVP Core Schema Proposal

來源參考：

- `temp/ewdb20260514.sql`
- `docs/database/ERP_CORE_ERD_REVIEW_20260514.md`
- 第一階段 Prototype 模組：訂單、品項、批號、BOM、生產、倉儲、品保、物流、人員

目的：

建立第二階段 MVP 可落地的乾淨資料模型，支援：

```txt
訂單 → 品項 / BOM → 工單 → 領料 → 生產報工 → 品檢 → 成品入庫 → 出貨 / 派車 → 批號追蹤
```

## 設計原則

1. 不直接全量移植 ewdb 的 124 張表。
2. 保留 ewdb 既有概念，但重整成 header / lines、主資料 / 交易資料、批號 / 異動流水帳。
3. 明確建立 PK / FK，讓 API、ORM、ERD、資料一致性都能維護。
4. 數量與金額使用 `DECIMAL`，避免 `FLOAT`。
5. 日期時間使用 `DATE` / `DATETIME`。
6. 狀態欄位先使用 `VARCHAR` enum-like value，後續可升級成狀態表。
7. 所有核心表保留 `created_at`, `updated_at`。
8. 交易表保留 `created_by_id`，方便稽核與權限追蹤。

## 命名規則

| 類型 | 規則 |
|---|---|
| 表名 | snake_case plural，例如 `sales_orders` |
| 主鍵 | `id BIGINT AUTO_INCREMENT` |
| 業務單號 | `*_no VARCHAR(50)` 並加唯一索引 |
| 外鍵 | `{entity}_id BIGINT` |
| 狀態 | `status VARCHAR(30)` |
| 數量 | `DECIMAL(18,4)` |
| 金額 | `DECIMAL(18,2)` |
| 時間 | `DATETIME` |

## 狀態 Enum 建議

### `item_type`

```txt
finished_good
semi_finished
raw_material
packaging
service
```

### `sales_order_status`

```txt
draft
confirmed
scheduled
in_production
ready_to_ship
shipped
closed
cancelled
```

### `work_order_status`

```txt
draft
released
material_issued
in_production
quality_check
packaging
completed
cancelled
```

### `inventory_transaction_type`

```txt
receive
issue
transfer
adjustment
production_input
production_output
shipment
return
scrap
```

### `quality_status`

```txt
pending
sampling
testing
approved
rejected
exception
```

### `shipment_status`

```txt
draft
picking
loaded
in_transit
delivered
signed
cancelled
```

### `dispatch_status`

```txt
pending
assigned
loading
in_transit
completed
cancelled
```

## 主資料 Master Data

### `roles`

角色與權限群組。

| 欄位 | 型別 | 說明 |
|---|---|---|
| `id` | BIGINT PK | 主鍵 |
| `code` | VARCHAR(50) UNIQUE | 角色代碼 |
| `name` | VARCHAR(100) | 角色名稱 |
| `description` | VARCHAR(255) NULL | 說明 |
| `created_at` | DATETIME | 建立時間 |
| `updated_at` | DATETIME | 更新時間 |

### `users`

系統登入帳號。

| 欄位 | 型別 | 說明 |
|---|---|---|
| `id` | BIGINT PK | 主鍵 |
| `role_id` | BIGINT FK -> roles.id | 角色 |
| `employee_id` | BIGINT FK -> employees.id NULL | 對應員工 |
| `email` | VARCHAR(255) UNIQUE | 登入 email |
| `password_hash` | VARCHAR(255) | 密碼雜湊 |
| `display_name` | VARCHAR(100) | 顯示名稱 |
| `status` | VARCHAR(30) | active / disabled |
| `created_at` | DATETIME | 建立時間 |
| `updated_at` | DATETIME | 更新時間 |

### `employees`

員工、人員、司機、品保、倉管、生管等角色基礎。

| 欄位 | 型別 | 說明 |
|---|---|---|
| `id` | BIGINT PK | 主鍵 |
| `employee_no` | VARCHAR(50) UNIQUE | 員工編號 |
| `name` | VARCHAR(100) | 姓名 |
| `department` | VARCHAR(100) | 部門 |
| `job_title` | VARCHAR(100) | 職稱 |
| `employment_status` | VARCHAR(30) | active / resigned |
| `phone` | VARCHAR(50) NULL | 電話 |
| `joined_date` | DATE NULL | 到職日 |
| `left_date` | DATE NULL | 離職日 |
| `created_at` | DATETIME | 建立時間 |
| `updated_at` | DATETIME | 更新時間 |

### `customers`

客戶主檔，整理自 ewdb `customer`。

| 欄位 | 型別 | 說明 |
|---|---|---|
| `id` | BIGINT PK | 主鍵 |
| `customer_no` | VARCHAR(50) UNIQUE | 客戶編號 |
| `display_name` | VARCHAR(120) | 顯示名稱 |
| `legal_name` | VARCHAR(120) NULL | 公司全名 |
| `business_no` | VARCHAR(30) NULL | 統編 |
| `address` | VARCHAR(255) NULL | 地址 |
| `contact_name` | VARCHAR(100) NULL | 聯絡人 |
| `contact_phone` | VARCHAR(100) NULL | 聯絡電話 |
| `contact_email` | VARCHAR(120) NULL | Email |
| `payment_terms` | VARCHAR(60) NULL | 帳期 |
| `status` | VARCHAR(30) | active / inactive |
| `created_at` | DATETIME | 建立時間 |
| `updated_at` | DATETIME | 更新時間 |

### `suppliers`

供應商主檔，整理自 ewdb `supplier` / `vendor`。

| 欄位 | 型別 | 說明 |
|---|---|---|
| `id` | BIGINT PK | 主鍵 |
| `supplier_no` | VARCHAR(50) UNIQUE | 供應商編號 |
| `display_name` | VARCHAR(120) | 顯示名稱 |
| `legal_name` | VARCHAR(120) NULL | 公司全名 |
| `supplier_type` | VARCHAR(30) | material / packaging / logistics / service |
| `business_no` | VARCHAR(30) NULL | 統編 |
| `address` | VARCHAR(255) NULL | 地址 |
| `contact_name` | VARCHAR(100) NULL | 聯絡人 |
| `contact_phone` | VARCHAR(100) NULL | 聯絡電話 |
| `contact_email` | VARCHAR(120) NULL | Email |
| `payment_terms` | VARCHAR(60) NULL | 帳期 |
| `status` | VARCHAR(30) | active / inactive |
| `created_at` | DATETIME | 建立時間 |
| `updated_at` | DATETIME | 更新時間 |

### `items`

統一品項主檔，合併 ewdb `product`, `material`, `goods`, `inproduct` 的核心概念。

| 欄位 | 型別 | 說明 |
|---|---|---|
| `id` | BIGINT PK | 主鍵 |
| `item_no` | VARCHAR(50) UNIQUE | SKU / 品項編號 |
| `name` | VARCHAR(120) | 品項名稱 |
| `item_type` | VARCHAR(30) | finished_good / raw_material / packaging 等 |
| `category` | VARCHAR(60) NULL | 分類 |
| `unit` | VARCHAR(20) | 基礎單位 |
| `storage_condition` | VARCHAR(100) NULL | 保存條件 |
| `shelf_life_days` | INT NULL | 效期天數 |
| `supplier_id` | BIGINT FK -> suppliers.id NULL | 預設供應商 |
| `status` | VARCHAR(30) | active / inactive |
| `created_at` | DATETIME | 建立時間 |
| `updated_at` | DATETIME | 更新時間 |

### `products`

成品延伸主檔。若 `items.item_type = finished_good`，可在此有成品資料。

| 欄位 | 型別 | 說明 |
|---|---|---|
| `id` | BIGINT PK | 主鍵 |
| `item_id` | BIGINT FK -> items.id UNIQUE | 成品品項 |
| `customer_id` | BIGINT FK -> customers.id NULL | 主要客戶 |
| `default_bom_id` | BIGINT FK -> bom_headers.id NULL | 預設 BOM |
| `default_production_line_id` | BIGINT FK -> production_lines.id NULL | 預設產線 |
| `status` | VARCHAR(30) | development / trial / mass_production / inactive |
| `created_at` | DATETIME | 建立時間 |
| `updated_at` | DATETIME | 更新時間 |

### `product_versions`

產品版本與規格版本。

| 欄位 | 型別 | 說明 |
|---|---|---|
| `id` | BIGINT PK | 主鍵 |
| `product_id` | BIGINT FK -> products.id | 成品 |
| `version_code` | VARCHAR(30) | 版本 |
| `spec_summary` | VARCHAR(255) NULL | 規格摘要 |
| `effective_date` | DATE NULL | 生效日 |
| `status` | VARCHAR(30) | draft / active / archived |
| `created_at` | DATETIME | 建立時間 |
| `updated_at` | DATETIME | 更新時間 |

### `bom_headers`

BOM / 配方表頭，整理自 ewdb `bom`。

| 欄位 | 型別 | 說明 |
|---|---|---|
| `id` | BIGINT PK | 主鍵 |
| `bom_no` | VARCHAR(50) UNIQUE | BOM 編號 |
| `product_id` | BIGINT FK -> products.id | 對應成品 |
| `version_code` | VARCHAR(30) | BOM 版本 |
| `name` | VARCHAR(120) | BOM 名稱 |
| `batch_size` | DECIMAL(18,4) | 標準批量 |
| `unit` | VARCHAR(20) | 批量單位 |
| `status` | VARCHAR(30) | draft / trial / approved / archived |
| `effective_date` | DATE NULL | 生效日 |
| `created_at` | DATETIME | 建立時間 |
| `updated_at` | DATETIME | 更新時間 |

### `bom_lines`

BOM 明細，整理自 ewdb `bom1`, `bom2`, `product_bom_spec`。

| 欄位 | 型別 | 說明 |
|---|---|---|
| `id` | BIGINT PK | 主鍵 |
| `bom_header_id` | BIGINT FK -> bom_headers.id | BOM 表頭 |
| `component_item_id` | BIGINT FK -> items.id | 原料/半成品/包材 |
| `line_no` | INT | 行號 |
| `quantity` | DECIMAL(18,4) | 用量 |
| `unit` | VARCHAR(20) | 單位 |
| `expected_loss_rate` | DECIMAL(8,4) DEFAULT 0 | 預估耗損率 |
| `process_step` | VARCHAR(100) NULL | 製程步驟 |
| `created_at` | DATETIME | 建立時間 |
| `updated_at` | DATETIME | 更新時間 |

### `warehouses`

倉庫主檔，整理自 ewdb `warehouse`。

| 欄位 | 型別 | 說明 |
|---|---|---|
| `id` | BIGINT PK | 主鍵 |
| `warehouse_no` | VARCHAR(50) UNIQUE | 倉庫編號 |
| `name` | VARCHAR(120) | 倉庫名稱 |
| `warehouse_type` | VARCHAR(30) | raw / frozen / finished_good / packaging |
| `temperature_zone` | VARCHAR(50) NULL | 常溫 / 冷藏 / 冷凍 |
| `status` | VARCHAR(30) | active / inactive |
| `created_at` | DATETIME | 建立時間 |
| `updated_at` | DATETIME | 更新時間 |

### `warehouse_locations`

庫位。原 ewdb 庫位概念不足，建議新增。

| 欄位 | 型別 | 說明 |
|---|---|---|
| `id` | BIGINT PK | 主鍵 |
| `warehouse_id` | BIGINT FK -> warehouses.id | 倉庫 |
| `location_code` | VARCHAR(50) | 庫位代碼 |
| `name` | VARCHAR(120) NULL | 庫位名稱 |
| `status` | VARCHAR(30) | active / inactive |
| `created_at` | DATETIME | 建立時間 |
| `updated_at` | DATETIME | 更新時間 |

### `production_lines`

產線，整理自 ewdb `production_line`。

| 欄位 | 型別 | 說明 |
|---|---|---|
| `id` | BIGINT PK | 主鍵 |
| `line_no` | VARCHAR(50) UNIQUE | 產線編號 |
| `name` | VARCHAR(120) | 產線名稱 |
| `factory` | VARCHAR(100) NULL | 工廠 |
| `process_name` | VARCHAR(100) NULL | 製程 |
| `capacity_per_hour` | DECIMAL(18,4) NULL | 每小時產能 |
| `status` | VARCHAR(30) | active / maintenance / inactive |
| `created_at` | DATETIME | 建立時間 |
| `updated_at` | DATETIME | 更新時間 |

### `vehicles`

物流車輛，原 ewdb 不足，建議新增。

| 欄位 | 型別 | 說明 |
|---|---|---|
| `id` | BIGINT PK | 主鍵 |
| `vehicle_no` | VARCHAR(50) UNIQUE | 車號 |
| `vehicle_type` | VARCHAR(50) | truck / refrigerated_truck |
| `temperature_zone` | VARCHAR(50) NULL | 冷凍/冷藏/常溫 |
| `status` | VARCHAR(30) | active / maintenance / inactive |
| `created_at` | DATETIME | 建立時間 |
| `updated_at` | DATETIME | 更新時間 |

## 交易資料 Transaction Data

### `sales_orders`

訂單表頭，整理自 ewdb `product_order`。

| 欄位 | 型別 | 說明 |
|---|---|---|
| `id` | BIGINT PK | 主鍵 |
| `sales_order_no` | VARCHAR(50) UNIQUE | 訂單編號 |
| `customer_id` | BIGINT FK -> customers.id | 客戶 |
| `order_date` | DATE | 訂單日期 |
| `required_date` | DATE NULL | 客戶需求交期 |
| `ship_to_address` | VARCHAR(255) NULL | 出貨地址 |
| `status` | VARCHAR(30) | sales_order_status |
| `created_by_id` | BIGINT FK -> users.id NULL | 建立人 |
| `created_at` | DATETIME | 建立時間 |
| `updated_at` | DATETIME | 更新時間 |

### `sales_order_lines`

訂單明細。

| 欄位 | 型別 | 說明 |
|---|---|---|
| `id` | BIGINT PK | 主鍵 |
| `sales_order_id` | BIGINT FK -> sales_orders.id | 訂單 |
| `product_id` | BIGINT FK -> products.id | 成品 |
| `line_no` | INT | 行號 |
| `quantity` | DECIMAL(18,4) | 數量 |
| `unit` | VARCHAR(20) | 單位 |
| `unit_price` | DECIMAL(18,2) NULL | 單價 |
| `required_date` | DATE NULL | 明細交期 |
| `status` | VARCHAR(30) | 狀態 |
| `created_at` | DATETIME | 建立時間 |
| `updated_at` | DATETIME | 更新時間 |

### `purchase_orders`

採購表頭，整理自 ewdb `purchase_order`。

| 欄位 | 型別 | 說明 |
|---|---|---|
| `id` | BIGINT PK | 主鍵 |
| `purchase_order_no` | VARCHAR(50) UNIQUE | 採購單號 |
| `supplier_id` | BIGINT FK -> suppliers.id | 供應商 |
| `order_date` | DATE | 採購日期 |
| `expected_date` | DATE NULL | 預計到貨日 |
| `status` | VARCHAR(30) | draft / approved / received / closed / cancelled |
| `created_by_id` | BIGINT FK -> users.id NULL | 建立人 |
| `created_at` | DATETIME | 建立時間 |
| `updated_at` | DATETIME | 更新時間 |

### `purchase_order_lines`

採購明細。

| 欄位 | 型別 | 說明 |
|---|---|---|
| `id` | BIGINT PK | 主鍵 |
| `purchase_order_id` | BIGINT FK -> purchase_orders.id | 採購單 |
| `item_id` | BIGINT FK -> items.id | 品項 |
| `line_no` | INT | 行號 |
| `quantity` | DECIMAL(18,4) | 數量 |
| `unit` | VARCHAR(20) | 單位 |
| `unit_price` | DECIMAL(18,2) NULL | 單價 |
| `expected_date` | DATE NULL | 預計到貨日 |
| `created_at` | DATETIME | 建立時間 |
| `updated_at` | DATETIME | 更新時間 |

### `inventory_batches`

庫存批號餘額，整理自 ewdb `batch_number` 與 `inventory_record`。

| 欄位 | 型別 | 說明 |
|---|---|---|
| `id` | BIGINT PK | 主鍵 |
| `batch_no` | VARCHAR(80) | 批號 |
| `item_id` | BIGINT FK -> items.id | 品項 |
| `warehouse_location_id` | BIGINT FK -> warehouse_locations.id | 庫位 |
| `quantity_on_hand` | DECIMAL(18,4) | 現有量 |
| `unit` | VARCHAR(20) | 單位 |
| `manufactured_date` | DATE NULL | 製造日 |
| `expiry_date` | DATE NULL | 效期 |
| `quality_status` | VARCHAR(30) | pending / approved / rejected / hold |
| `status` | VARCHAR(30) | available / reserved / hold / consumed |
| `created_at` | DATETIME | 建立時間 |
| `updated_at` | DATETIME | 更新時間 |

唯一性建議：

```txt
UNIQUE(batch_no, item_id, warehouse_location_id)
```

### `inventory_transactions`

庫存異動流水帳，整理自 ewdb `inventory_record`, `inventory_order`。

| 欄位 | 型別 | 說明 |
|---|---|---|
| `id` | BIGINT PK | 主鍵 |
| `inventory_batch_id` | BIGINT FK -> inventory_batches.id | 批號庫存 |
| `transaction_type` | VARCHAR(30) | inventory_transaction_type |
| `quantity` | DECIMAL(18,4) | 正負異動量 |
| `unit` | VARCHAR(20) | 單位 |
| `reference_type` | VARCHAR(50) NULL | work_order / shipment / purchase_order |
| `reference_id` | BIGINT NULL | 來源 ID |
| `transaction_at` | DATETIME | 異動時間 |
| `created_by_id` | BIGINT FK -> users.id NULL | 建立人 |
| `created_at` | DATETIME | 建立時間 |

### `work_orders`

工單，整理自 ewdb `work_order`。

| 欄位 | 型別 | 說明 |
|---|---|---|
| `id` | BIGINT PK | 主鍵 |
| `work_order_no` | VARCHAR(50) UNIQUE | 工單號 |
| `sales_order_line_id` | BIGINT FK -> sales_order_lines.id NULL | 訂單明細 |
| `product_id` | BIGINT FK -> products.id | 生產品項 |
| `bom_header_id` | BIGINT FK -> bom_headers.id NULL | 使用 BOM |
| `production_line_id` | BIGINT FK -> production_lines.id NULL | 產線 |
| `planned_quantity` | DECIMAL(18,4) | 預計數量 |
| `completed_quantity` | DECIMAL(18,4) DEFAULT 0 | 完成數量 |
| `unit` | VARCHAR(20) | 單位 |
| `planned_start_at` | DATETIME NULL | 預計開工 |
| `planned_end_at` | DATETIME NULL | 預計完工 |
| `actual_start_at` | DATETIME NULL | 實際開工 |
| `actual_end_at` | DATETIME NULL | 實際完工 |
| `status` | VARCHAR(30) | work_order_status |
| `created_by_id` | BIGINT FK -> users.id NULL | 建立人 |
| `created_at` | DATETIME | 建立時間 |
| `updated_at` | DATETIME | 更新時間 |

### `work_order_materials`

工單領料與用料。

| 欄位 | 型別 | 說明 |
|---|---|---|
| `id` | BIGINT PK | 主鍵 |
| `work_order_id` | BIGINT FK -> work_orders.id | 工單 |
| `item_id` | BIGINT FK -> items.id | 原料/包材 |
| `required_quantity` | DECIMAL(18,4) | 應領數量 |
| `issued_quantity` | DECIMAL(18,4) DEFAULT 0 | 已領數量 |
| `unit` | VARCHAR(20) | 單位 |
| `inventory_batch_id` | BIGINT FK -> inventory_batches.id NULL | 指定批號 |
| `created_at` | DATETIME | 建立時間 |
| `updated_at` | DATETIME | 更新時間 |

### `production_reports`

生產報工，整理自 ewdb `production_data`, `production_data_output`。

| 欄位 | 型別 | 說明 |
|---|---|---|
| `id` | BIGINT PK | 主鍵 |
| `work_order_id` | BIGINT FK -> work_orders.id | 工單 |
| `report_no` | VARCHAR(50) UNIQUE | 報工單號 |
| `reported_at` | DATETIME | 報工時間 |
| `good_quantity` | DECIMAL(18,4) | 良品數量 |
| `defect_quantity` | DECIMAL(18,4) DEFAULT 0 | 不良數量 |
| `loss_quantity` | DECIMAL(18,4) DEFAULT 0 | 損耗數量 |
| `unit` | VARCHAR(20) | 單位 |
| `reported_by_id` | BIGINT FK -> employees.id NULL | 報工人 |
| `created_at` | DATETIME | 建立時間 |

### `quality_inspections`

品檢表頭，補足 ewdb 不足之處。

| 欄位 | 型別 | 說明 |
|---|---|---|
| `id` | BIGINT PK | 主鍵 |
| `inspection_no` | VARCHAR(50) UNIQUE | 檢驗單號 |
| `work_order_id` | BIGINT FK -> work_orders.id NULL | 工單 |
| `inventory_batch_id` | BIGINT FK -> inventory_batches.id NULL | 批號 |
| `inspection_type` | VARCHAR(30) | incoming / in_process / finished_good |
| `status` | VARCHAR(30) | quality_status |
| `result` | VARCHAR(30) NULL | pass / fail |
| `inspector_id` | BIGINT FK -> employees.id NULL | 檢驗員 |
| `inspected_at` | DATETIME NULL | 檢驗時間 |
| `created_at` | DATETIME | 建立時間 |
| `updated_at` | DATETIME | 更新時間 |

### `quality_inspection_items`

檢驗項目。

| 欄位 | 型別 | 說明 |
|---|---|---|
| `id` | BIGINT PK | 主鍵 |
| `quality_inspection_id` | BIGINT FK -> quality_inspections.id | 檢驗單 |
| `check_item` | VARCHAR(120) | 檢驗項 |
| `standard_value` | VARCHAR(120) NULL | 標準 |
| `actual_value` | VARCHAR(120) NULL | 實測 |
| `result` | VARCHAR(30) | pass / fail / pending |
| `created_at` | DATETIME | 建立時間 |
| `updated_at` | DATETIME | 更新時間 |

### `quality_exceptions`

品質異常 / NCR，整理自 ewdb `complaints` 的內部品質面。

| 欄位 | 型別 | 說明 |
|---|---|---|
| `id` | BIGINT PK | 主鍵 |
| `exception_no` | VARCHAR(50) UNIQUE | 異常單號 |
| `quality_inspection_id` | BIGINT FK -> quality_inspections.id NULL | 來源檢驗 |
| `work_order_id` | BIGINT FK -> work_orders.id NULL | 工單 |
| `inventory_batch_id` | BIGINT FK -> inventory_batches.id NULL | 批號 |
| `severity` | VARCHAR(30) | low / medium / high / critical |
| `description` | TEXT | 問題描述 |
| `corrective_action` | TEXT NULL | 矯正措施 |
| `status` | VARCHAR(30) | open / investigating / resolved / closed |
| `owner_id` | BIGINT FK -> employees.id NULL | 負責人 |
| `created_at` | DATETIME | 建立時間 |
| `updated_at` | DATETIME | 更新時間 |

### `finished_goods_batches`

成品批號，連接工單、生產與品保。

| 欄位 | 型別 | 說明 |
|---|---|---|
| `id` | BIGINT PK | 主鍵 |
| `batch_no` | VARCHAR(80) UNIQUE | 成品批號 |
| `work_order_id` | BIGINT FK -> work_orders.id | 來源工單 |
| `product_id` | BIGINT FK -> products.id | 成品 |
| `inventory_batch_id` | BIGINT FK -> inventory_batches.id NULL | 入庫後庫存批號 |
| `quantity` | DECIMAL(18,4) | 數量 |
| `unit` | VARCHAR(20) | 單位 |
| `manufactured_date` | DATE | 製造日 |
| `expiry_date` | DATE NULL | 效期 |
| `quality_status` | VARCHAR(30) | 品保狀態 |
| `created_at` | DATETIME | 建立時間 |
| `updated_at` | DATETIME | 更新時間 |

### `shipments`

出貨表頭，整理自 ewdb `shipping_order`。

| 欄位 | 型別 | 說明 |
|---|---|---|
| `id` | BIGINT PK | 主鍵 |
| `shipment_no` | VARCHAR(50) UNIQUE | 出貨單號 |
| `sales_order_id` | BIGINT FK -> sales_orders.id NULL | 訂單 |
| `customer_id` | BIGINT FK -> customers.id | 客戶 |
| `ship_date` | DATE NULL | 出貨日 |
| `ship_to_address` | VARCHAR(255) NULL | 地址 |
| `status` | VARCHAR(30) | shipment_status |
| `created_by_id` | BIGINT FK -> users.id NULL | 建立人 |
| `created_at` | DATETIME | 建立時間 |
| `updated_at` | DATETIME | 更新時間 |

### `shipment_lines`

出貨明細與批號。

| 欄位 | 型別 | 說明 |
|---|---|---|
| `id` | BIGINT PK | 主鍵 |
| `shipment_id` | BIGINT FK -> shipments.id | 出貨單 |
| `sales_order_line_id` | BIGINT FK -> sales_order_lines.id NULL | 訂單明細 |
| `finished_goods_batch_id` | BIGINT FK -> finished_goods_batches.id | 成品批號 |
| `quantity` | DECIMAL(18,4) | 出貨數量 |
| `unit` | VARCHAR(20) | 單位 |
| `created_at` | DATETIME | 建立時間 |
| `updated_at` | DATETIME | 更新時間 |

### `dispatches`

物流派車。

| 欄位 | 型別 | 說明 |
|---|---|---|
| `id` | BIGINT PK | 主鍵 |
| `dispatch_no` | VARCHAR(50) UNIQUE | 派車單號 |
| `shipment_id` | BIGINT FK -> shipments.id | 出貨單 |
| `vehicle_id` | BIGINT FK -> vehicles.id NULL | 車輛 |
| `driver_employee_id` | BIGINT FK -> employees.id NULL | 司機 |
| `temperature_zone` | VARCHAR(50) NULL | 溫層 |
| `planned_departure_at` | DATETIME NULL | 預計出車 |
| `actual_departure_at` | DATETIME NULL | 實際出車 |
| `delivered_at` | DATETIME NULL | 簽收時間 |
| `status` | VARCHAR(30) | dispatch_status |
| `created_at` | DATETIME | 建立時間 |
| `updated_at` | DATETIME | 更新時間 |

### `work_order_assignments`

工單人員配置。

| 欄位 | 型別 | 說明 |
|---|---|---|
| `id` | BIGINT PK | 主鍵 |
| `work_order_id` | BIGINT FK -> work_orders.id | 工單 |
| `employee_id` | BIGINT FK -> employees.id | 員工 |
| `role_in_work_order` | VARCHAR(50) | 班長 / 操作員 / 品保 |
| `created_at` | DATETIME | 建立時間 |

### `audit_logs`

稽核紀錄。

| 欄位 | 型別 | 說明 |
|---|---|---|
| `id` | BIGINT PK | 主鍵 |
| `user_id` | BIGINT FK -> users.id NULL | 操作人 |
| `entity_type` | VARCHAR(80) | 表/物件 |
| `entity_id` | BIGINT NULL | 物件 ID |
| `action` | VARCHAR(50) | create / update / approve / delete |
| `before_data` | JSON NULL | 變更前 |
| `after_data` | JSON NULL | 變更後 |
| `created_at` | DATETIME | 建立時間 |

## Migration 順序

建議 Alembic migration 拆成 6 個批次，降低一次建立太多表的風險。

### Migration 001：基礎主資料

- `roles`
- `employees`
- `users`
- `customers`
- `suppliers`

### Migration 002：品項與 BOM

- `items`
- `production_lines`
- `products`
- `product_versions`
- `bom_headers`
- `bom_lines`

### Migration 003：倉儲與庫存

- `warehouses`
- `warehouse_locations`
- `inventory_batches`
- `inventory_transactions`

### Migration 004：訂單、採購與工單

- `sales_orders`
- `sales_order_lines`
- `purchase_orders`
- `purchase_order_lines`
- `work_orders`
- `work_order_materials`
- `production_reports`
- `work_order_assignments`

### Migration 005：品保與批號

- `quality_inspections`
- `quality_inspection_items`
- `quality_exceptions`
- `finished_goods_batches`

### Migration 006：出貨、物流與稽核

- `vehicles`
- `shipments`
- `shipment_lines`
- `dispatches`
- `audit_logs`

## 舊表對應建議

| ewdb 舊表 | MVP 新表 |
|---|---|
| `customer` | `customers` |
| `supplier`, `vendor` | `suppliers` |
| `employee` | `employees` |
| `member`, `user_group` | `users`, `roles` |
| `product`, `material`, `goods`, `inproduct` | `items`, `products` |
| `product_ver` | `product_versions` |
| `bom`, `bom1`, `bom2`, `product_bom_spec` | `bom_headers`, `bom_lines` |
| `warehouse` | `warehouses` |
| `batch_number`, `inventory_record` | `inventory_batches`, `inventory_transactions` |
| `product_order` | `sales_orders`, `sales_order_lines` |
| `purchase_order` | `purchase_orders`, `purchase_order_lines` |
| `work_order` | `work_orders` |
| `production_data`, `production_data_output` | `production_reports`, `finished_goods_batches` |
| `production_data_input` | `work_order_materials`, `inventory_transactions` |
| `complaints` | `quality_exceptions` |
| `shipping_order`, `shipping_record` | `shipments`, `shipment_lines` |

## 下一步

確認此 proposal 後，可進入：

```txt
Sprint 12B：依 ERP_2_0_MVP_SCHEMA_PROPOSAL.md 建立 SQLAlchemy models 與 Alembic migration 001-006。
```
