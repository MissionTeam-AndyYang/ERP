# EWDB Word Inferred FK Candidates

日期：2026-05-15

本文件從 Word 欄位描述中的「關連至 / 關聯至 / 對應至 XXX 資料表」推論 FK。

| From table | From field | To table(s) | To field | Confidence | Source |
|---|---|---|---|---|---|
| `aps_quantity` | `item_name` | `inproduct / product` | `no` | denormalized_or_label | 產出的料品品項名稱，關連至inproduct/product資料表；varchar(60) |
| `aps_quantity` | `item_no` | `inproduct / product` | `no` | needs_review | 產出的料品品項no，關連至inproduct/product資料表；UNIQUE KEY；varchar(60) |
| `aps_quantity` | `product_order_no` | `product_order` | `no` | high | 訂購訂單no，關連至product_order資料表；UNIQUE KEY；varchar(60) |
| `aps_quantity_item` | `item_name` | `material` | `no` | denormalized_or_label | 投入的料品品項名稱，關連至material資料表；varchar(60) |
| `aps_quantity_item` | `item_no` | `material` | `no` | high | 投入的料品品項no，關連至material資料表；UNIQUE KEY；varchar(60) |
| `aps_quantity_item` | `product_order_no` | `product_order` | `no` | high | 訂購訂單no，關連至product_order資料表；UNIQUE KEY；varchar(60) |
| `batch_number` | `creator_no` | `employee` | `no` | high | 製單人員no，關連至employee資料表；varchar(60) |
| `batch_number` | `item_name` | `material / inproduct / product` | `no` | denormalized_or_label | 品項名稱，關連至material/inproduct/product資料表；varchar(60) |
| `batch_number` | `item_no` | `material / inproduct / product` | `no` | needs_review | 品項no，關連至material/inproduct/product資料表；varchar(60) |
| `batch_number` | `item_ref_displayName` | `company` | `no` | denormalized_or_label | 客戶/廠商公司簡稱，關連至company資料表；varchar(60) |
| `batch_number` | `item_ref_no` | `company` | `no` | high | 客戶/廠商no，關連至company資料表；varchar(60) |
| `batch_number` | `ref_no` | `goods_receipt_note / work_order / process_order` | `no` | needs_review | 進貨單no /銷貨單no/領退餘廢產單 no，關連至goods_receipt_note/work_order/process_order資料表；UNIQUE KEY；varchar(60) |
| `batchno_serialno` | `ref_order_no` | `goods_receipt_note / work_order / process_orderr / inventory_order` | `no` | needs_review | 進貨單no /銷貨單no/領退餘廢產單 no/ 出入庫單no，關連至goods_receipt_note/work_order/process_orderr/inventory_order資料表；UNIQUE KEY；varchar(60) |
| `bom_item` | `bom_no` | `bom` | `no` | high | 商品配方no，關連至bom資料表；UNIQUE KEY；varchar(60) |
| `bom_item` | `item_name` | `material` | `no` | denormalized_or_label | 原料名稱，關連至material資料表；varchar(60) |
| `bom_item` | `item_no` | `material` | `no` | high | 原物料no，關連至material資料表；UNIQUE KEY；varchar(60) |
| `bom1` | `child_id` | `material / bom1_number` | `id` | needs_review | 子級料品品項no或BOM no，關連至material /bom1_number資料表；UNIQUE KEY；varchar(60) |
| `bom1` | `child_name` | `material / bom1_number` | `no` | denormalized_or_label | 子級料品品項或BOM簡稱，關連至material /bom1_number資料表；varchar(60) |
| `bom1` | `parent_name` | `bom1_number` | `no` | denormalized_or_label | 父級BOM簡稱，關連至bom1_number資料表；varchar(60) |
| `bom1` | `parent_no` | `bom1_number` | `no` | high | 父級BOM編號，關連至bom1_number資料表；UNIQUE KEY；varchar(60) |
| `bom1_number` | `bom_no` | `bom` | `no` | high | 商品配方no，關連至bom資料表；varchar(60)；類型為加工時，此欄位才會有值。 |
| `bom2` | `child_id` | `material / bom2_number` | `id` | needs_review | 子級料品品項 no或BOM no，關連至material /bom2_number資料表；varchar(60) |
| `bom2` | `child_name` | `material / bom2_number` | `no` | denormalized_or_label | 子級料品品項或BOM簡稱，關連至material /bom2_number資料表；varchar(60) |
| `bom2` | `parent_name` | `bom2_number` | `no` | denormalized_or_label | 父級BOM簡稱，關連至bom2_number資料表；varchar(60) |
| `bom2` | `parent_no` | `bom2_number` | `no` | high | 父級BOM編號，關連至bom2_number資料表；varchar(60) |
| `bom2_number` | `bom_no` | `product` | `no` | high | 料品品項no，關連至product資料表；varchar(60) |
| `company` | `paid_id` | `payment` | `id` | high | 付款資料id，關連至payment資料表 (客戶)；varchar(60) |
| `company` | `received_id` | `payment` | `id` | high | 收款資料id，關連至payment資料表 (供應商/廠商)；varchar(60) |
| `contract` | `creator_no` | `employee` | `no` | high | 製單人員no，關連至employee資料表；varchar(60) |
| `contract` | `item_name` | `trans_items / trans_items2` | `no` | denormalized_or_label | 交易品項名稱，關連至trans_items / trans_items2資料表；varchar(60) |
| `contract` | `item_no` | `trans_items / trans_items2` | `no` | needs_review | 交易品項no，關連至trans_items / trans_items2資料表；varchar(60) |
| `contract` | `item_ref_displayName` | `company` | `no` | denormalized_or_label | 客戶/廠商公司簡稱，關連至company資料表；varchar(60) |
| `contract` | `item_ref_no` | `company` | `no` | high | 客戶/廠商no，關連至company資料表；varchar(60) |
| `contract` | `payment_id` | `payment` | `id` | high | 帳款資料id，關連至payment資料表；int |
| `contract` | `ref_no` | `quotation` | `no` | high | 議價單編號，關連至quotation資料表；varchar(60) |
| `equipment` | `station_no` | `station` | `no` | high | 站點，關連至station資料表；varchar(60) |
| `goods_receipt_note` | `creator_no` | `employee` | `no` | high | 製單人員no，關連至employee資料表；varchar(60) |
| `goods_receipt_note` | `item_name` | `trans_items` | `no` | denormalized_or_label | 交易品項名稱，關連至trans_items資料表 |
| `goods_receipt_note` | `item_no` | `trans_items` | `no` | high | 交易品項no，關連至trans_items資料表 |
| `goods_receipt_note` | `item_ref_displayName` | `company` | `no` | denormalized_or_label | 客戶/廠商公司簡稱，關連至company資料表；varchar(60) |
| `goods_receipt_note` | `item_ref_no` | `company` | `no` | high | 客戶/廠商no，關連至company資料表；varchar(60) |
| `goods_receipt_note` | `purchase_order_no` | `purchase_order` | `no` | high | 採購單no，關連至purchase_order資料表；varchar(60) |
| `inproduct_bom_spec` | `inproduct_no` | `inproduct` | `no` | high | 料品品項no，關連至inproduct資料表；UNIQUE KEY；varchar(60) |
| `inventory_delta` | `in_ref_id` | `inventory_record` | `id` | high | 入庫紀錄id，關聯至inventory_record資料表 JSON Array；longtext |
| `inventory_delta` | `out_ref_id` | `inventory_record` | `id` | high | 出庫紀錄id，關聯至inventory_record資料表 JSON Array；longtext |
| `inventory_delta` | `specified_name` | `material / inproduct / product` | `no` | denormalized_or_label | 1.原物料；原物料名稱，關聯至material資料表2.在製品；在製品名稱，關聯至inproduct資料表3.製成品；製成品名稱，關聯至product資料表4.批號；無 |
| `inventory_delta` | `specified_no` | `material / inproduct / product / batch_number` | `no` | needs_review | 項目編號；UNIQUE KEY；varchar(60)1.原物料；原物料no，關聯至material資料表2.在製品；在製品no，關聯至inproduct資料表3.製成品；製成品no，關聯至product資料表4.批號；批號no，關聯至batch_number資料表 |
| `inventory_delta` | `specified_ref_name` | `company / material / inproduct / product` | `no` | denormalized_or_label | 項目名稱；varchar(60)1.原物料2.在製品3.製成品客戶/廠商公司簡稱，關連至company資料表；varchar(60)4.批號原物料/在製品/製成品 no，關連至material/inproduct/product資料表；varchar(60) |
| `inventory_delta` | `specified_ref_no` | `company / material / inproduct / product` | `no` | needs_review | 項目編號；varchar(60)1.原物料2.在製品3.製成品客戶/廠商no，關連至company資料表；varchar(60)4.批號原物料/在製品/製成品 no，關連至material/inproduct/product資料表；varchar(60) |
| `inventory_delta` | `warehouse_displayName` | `ship_wh_alias` | `no` | denormalized_or_label | 倉儲別名名稱，關聯至ship_wh_alias資料表；UNIQUE KEY；varchar(60) |
| `inventory_delta` | `warehouse_no` | `ship_wh_alias` | `no` | high | 倉儲別名no，關聯至ship_wh_alias資料表；varchar(60) |
| `Inventory_item_month_statistic` | `specified_name` | `material / inproduct / product` | `no` | denormalized_or_label | 1.原物料；原物料名稱，關聯至material資料表2.在製品；在製品名稱，關聯至inproduct資料表3.製成品；製成品名稱，關聯至product資料表4.批號；無 |
| `Inventory_item_month_statistic` | `specified_no` | `material / inproduct / product / batch_number` | `no` | needs_review | 項目編號；UNIQUE KEY；varchar(60)1.原物料；原物料no，關聯至material資料表2.在製品；在製品no，關聯至inproduct資料表3.製成品；製成品no，關聯至product資料表4.批號；批號no，關聯至batch_number資料表 |
| `Inventory_item_month_statistic` | `specified_no` | `material / inproduct / product / batch_number` | `no` | needs_review | 項目編號；UNIQUE KEY；varchar(60)1.原物料；原物料no，關聯至material資料表2.在製品；在製品no，關聯至inproduct資料表3.製成品；製成品no，關聯至product資料表4.批號；批號no，關聯至batch_number資料表 |
| `Inventory_item_month_statistic` | `specified_ref_no` | `company / material / inproduct / product` | `no` | needs_review | 項目編號；UNIQUE KEY；varchar(60)1.原物料2.在製品3.製成品客戶/廠商no，關連至company資料表；varchar(60)4.批號原物料/在製品/製成品 no，關連至material/inproduct/product資料表；varchar(60) |
| `Inventory_item_month_statistic` | `warehouse_displayName` | `ship_wh_alias` | `no` | denormalized_or_label | 倉儲別名名稱，關聯至ship_wh_alias資料表；UNIQUE KEY；varchar(60) |
| `Inventory_item_month_statistic` | `warehouse_no` | `ship_wh_alias` | `no` | high | 倉儲別名no，關聯至ship_wh_alias資料表；varchar(60) |
| `Inventory_month_statistic` | `warehouse_displayName` | `ship_wh_alias` | `no` | denormalized_or_label | 倉儲別名名稱，關聯至ship_wh_alias資料表；UNIQUE KEY；varchar(60) |
| `Inventory_month_statistic` | `warehouse_no` | `ship_wh_alias` | `no` | high | 倉儲別名no，關聯至ship_wh_alias資料表；varchar(60) |
| `inventory_order` | `creator_no` | `employee` | `no` | high | 製單人員no，關連至employee資料表；varchar(60) |
| `inventory_order` | `item_name` | `material / inproduct / product` | `no` | denormalized_or_label | 原物料/在製品/製成品no名稱，關連至material/inproduct/product資料表；varchar(60) |
| `inventory_order` | `item_no` | `material / inproduct / product` | `no` | needs_review | 原物料/在製品/製成品no，關連至material/inproduct/product資料表；varchar(60) |
| `inventory_order` | `item_ref_displayName` | `company` | `no` | denormalized_or_label | 客戶/廠商公司簡稱，關連至company資料表；varchar(60) |
| `inventory_order` | `item_ref_no` | `company` | `no` | high | 客戶/廠商no，關連至company資料表；varchar(60) |
| `inventory_record` | `item_name` | `material / inproduct / product` | `no` | denormalized_or_label | 品項名稱，關連至material/inproduct/product資料表；varchar(60) |
| `inventory_record` | `item_no` | `material / inproduct / product` | `no` | needs_review | 原物料/在製品/製成品id，關連至material/inproduct/product資料表；varchar(60) |
| `inventory_record` | `item_ref_displayName` | `company` | `no` | denormalized_or_label | 客戶/廠商公司簡稱，關連至company資料表；varchar(60) |
| `inventory_record` | `item_ref_no` | `company` | `no` | high | 客戶/廠商no，關連至company資料表；varchar(60) |
| `inventory_record` | `ref_no` | `goods_receipt_note / shipping_order / process_order / inventory_order` | `no` | needs_review | 進料/出品/領料/退料/餘料/廢料/產品/出入庫單no，關聯至goods_receipt_note/shipping_order/process_order/ inventory_order資料表；varchar(60) |
| `inventory_record` | `warehouse_displayName` | `ship_wh_alias` | `no` | denormalized_or_label | 倉儲別名名稱，關聯至ship_wh_alias資料表；varchar(60) |
| `inventory_record` | `warehouse_no` | `ship_wh_alias` | `no` | high | 倉儲別名no，關聯至ship_wh_alias資料表；varchar(60) |
| `item_hours` | `item_no` | `inproduct / product` | `no` | needs_review | 料品品項no，關連至inproduct / product資料表；UNIQUE KEY；varchar(60) |
| `item_loss` | `item_no` | `material / inproduct / product` | `no` | needs_review | 料品品項no，關連至material / inproduct / product資料表；UNIQUE KEY；varchar(60) |
| `item_price` | `item_name` | `material / inproduct / product / goods` | `no` | denormalized_or_label | 料品品項名稱，關連至material / inproduct / product / goods資料表；varchar(60) |
| `item_price` | `item_no` | `material / inproduct / product / goods` | `no` | needs_review | 料品品項編號，關連至material / inproduct / product / goods資料表；UNIQUE KEY；varchar(60) |
| `member` | `user_no` | `employee` | `no` | high | 員工no，關連至employee資料表；UNIQUE KEY；varchar(60) |
| `order_item_month_statistic` | `specified_name` | `company` | `no` | denormalized_or_label | 公司名稱，關聯至company資料表；varchar(60) |
| `order_item_month_statistic` | `specified_no` | `company` | `no` | high | 公司no，關聯至company資料表；UNIQUE KEY；varchar(60) |
| `order_payment` | `item_ref_displayName` | `company` | `no` | denormalized_or_label | 客戶/廠商公司簡稱，關連至company資料表；varchar(60) |
| `order_payment` | `item_ref_no` | `company` | `no` | high | 客戶/廠商no，關連至company資料表；varchar(60) |
| `order_payment` | `ref_no` | `product_order / purchase_order` | `no` | needs_review | 採購單 no/訂購單 no，關聯至product_order /purchase_order資料表；varchar(60) |
| `order_payment` | `ref_sub_no` | `goods_receipt_note / shipping_order` | `no` | needs_review | 進貨單 no/銷貨單 no，關聯至goods_receipt_note /shipping_order資料表；varchar(60) |
| `pl_item_capacity` | `item_name` | `inproduct / product` | `no` | denormalized_or_label | 產出料品品項名稱，關連至inproduct/product資料表；varchar(60) |
| `pl_item_capacity` | `item_no` | `inproduct / product` | `no` | needs_review | 產出料品品項no，關連至inproduct/product資料表；UNIQUE Key；varchar(60) |
| `pl_item_capacity` | `pl_name` | `production_line` | `no` | denormalized_or_label | 產線名稱，關聯至production_line資料表；varchar(60) |
| `pl_item_capacity` | `pl_no` | `production_line` | `no` | high | 產線no，關聯至production_line資料表；UNIQUE KEY；varchar(60) |
| `pl_item_loss` | `item_name` | `material / inproduct` | `no` | denormalized_or_label | 投入料品品項品項名稱，關連至material/inproduct資料表；varchar(60) |
| `pl_item_loss` | `item_no` | `material / inproduct` | `no` | needs_review | 投入料品品項no，關連至material/inproduct資料表；UNIQUE KEY；varchar(60) |
| `pl_item_loss` | `pl_item_capacity_no` | `pl_item_capacity` | `no` | needs_review | 產線料品產能，關聯至pl_item_capacity資料表；UNIQUE  KEY；varchar(60) |
| `pl_man_capacity` | `pl_name` | `production_line` | `no` | denormalized_or_label | 產線名稱，關聯至production_line資料表；varchar(60) |
| `pl_man_capacity` | `pl_no` | `production_line` | `no` | high | 產線no，關聯至production_line資料表；UNIQUE KEY；varchar(60) |
| `process_flow` | `product_process_no` | `product_process` | `no` | high | 工序no，關連至product_process資料表；UNIQUE KEY；varchar(60) |
| `process_labor` | `creator_no` | `employee` | `no` | high | 製單人員no，關連至employee資料表；varchar(60) |
| `process_labor` | `employee_no` | `employee` | `no` | high | 員工編號，關連至employee資料表；UNIQUE KEY；varchar(60) |
| `process_labor` | `production_line_no` | `production_line` | `no` | high | 產線no，關連至production_line資料表；varchar(60) |
| `process_labor` | `station_no` | `station` | `no` | high | 站點 no，關連至station資料表；varchar(60) |
| `process_labor` | `work_order_no` | `work_order` | `no` | high | 派工單no，關連至work_order資料表；UNIQUE KEY；varchar(60) |
| `process_order` | `creator_no` | `employee` | `no` | high | 製單人員no，關連至employee資料表；varchar(60) |
| `process_order` | `item_name` | `material / inproduct / product` | `no` | denormalized_or_label | 料品品項名稱，關連至material/ inproduct/ product資料表；varchar(60) |
| `process_order` | `item_no` | `material / inproduct / product` | `no` | needs_review | 料品品項no，關連至material/ inproduct/ product資料表；varchar(60) |
| `process_order` | `item_ref_displayName` | `company` | `no` | denormalized_or_label | 客戶/廠商公司簡稱，關連至company資料表；varchar(60) |
| `process_order` | `item_ref_no` | `company` | `no` | high | 客戶/廠商no，關連至company資料表；varchar(60) |
| `process_order` | `work_order_no` | `work_order` | `no` | high | 派工單no，關連至work_order資料表；varchar(60) |
| `product_bom_spec` | `bom2_no` | `bom2_number` | `no` | high | bom編號，關連至bom2_number資料表的no；UNIQUE KEY；varchar(60) |
| `product_bom_spec` | `product_no` | `product` | `no` | high | 製成品no，關連至product 資料表；UNIQUE KEY；varchar(60) |
| `product_order` | `creator_no` | `employee` | `no` | high | 製單人員no，關連至employee資料表；varchar(60) |
| `product_order` | `item_name` | `trans_items` | `no` | denormalized_or_label | 交易品項名稱，關連至trans_items資料表；varchar(60) |
| `product_order` | `item_no` | `trans_items` | `no` | high | 交易品項no，關連至trans_items資料表；varchar(60) |
| `product_order` | `item_ref_displayName` | `company` | `no` | denormalized_or_label | 客戶/廠商公司簡稱，關連至company資料表；varchar(60) |
| `product_order` | `item_ref_no` | `company` | `no` | high | 客戶/廠商no，關連至company資料表；varchar(60) |
| `product_order` | `ref_no` | `contract` | `no` | high | 合約no，關連至contract資料表；varchar(60) |
| `product_process` | `item_no` | `inproduct / product` | `no` | needs_review | 料品品項no，關連至inproduct/product資料表；UNIQUE KEY；varchar(60) |
| `product_spec` | `product_no` | `product` | `no` | high | 製成品no，關連至product 資料表；UNIQUE KEY；varchar(60) |
| `product_ver` | `item_no` | `product` | `no` | high | 製成品資料編號；UNIQUE KEY；varchar(60)，關連至product 資料表；UNIQUE KEY；varchar(60) |
| `production_data` | `creator_no` | `employee` | `no` | high | 製單人員no，關連至employee資料表；varchar(60) |
| `production_data` | `customer_displayName` | `company` | `no` | denormalized_or_label | 客戶公司簡稱，關連至company資料表；varchar(60) |
| `production_data` | `customer_no` | `company` | `no` | high | 客戶no，關連至company資料表；varchar(60) |
| `production_data` | `item_name` | `inproduct / product` | `no` | denormalized_or_label | 產出的料品品項名稱，關連至inproduct/ product資料表；varchar(60) |
| `production_data` | `item_no` | `inproduct / product` | `no` | needs_review | 產出的料品品項no，關連至inproduct/ product資料表 |
| `production_data` | `product_name` | `product` | `no` | denormalized_or_label | 交易品項名稱，關連至product 資料表；varchar(60) |
| `production_data` | `product_no` | `product` | `no` | high | 交易品項no，關連至product資料表；varchar(60) |
| `production_data` | `product_order_no` | `product_order` | `no` | high | 銷售訂單編號，關連至product_order資料表；varchar(60) |
| `production_data` | `production_line_no` | `production_line` | `no` | high | 產線no，關連至production_line資料表；varchar(60) |
| `production_data` | `work_order_no` | `work_order` | `no` | high | 派工單no，關連至work_order資料表；UNIQUE KEY；varchar(60) |
| `production_data_input` | `item_name` | `material / product` | `no` | denormalized_or_label | 投入的料品品項名稱，關連至material/ product資料表；varchar(60) |
| `production_data_input` | `item_no` | `material / product` | `no` | needs_review | 投入的料品品項no，關連至material/ product資料表；UNIQUE KEY；varchar(60) |
| `production_data_input` | `process_order_no` | `process_order` | `no` | high | 餘廢退產單no，關連至process_order資料表；varchar(60) |
| `production_data_input` | `work_order_no` | `work_order` | `no` | high | 派工單no，關連至work_order資料表；UNIQUE KEY；varchar(60) |
| `production_data_labor` | `employee_name` | `employee` | `no` | denormalized_or_label | 員工名稱，關連至employee資料表；varchar(60) |
| `production_data_labor` | `employee_no` | `employee` | `no` | high | 員工no，關連至employee資料表；UNIQUE KEY；varchar(60) |
| `production_data_labor` | `station_no` | `station` | `no` | high | 站點no，關連至station資料表；varchar(60) |
| `production_data_labor` | `work_order_no` | `work_order` | `no` | high | 派工單no，關連至work_order資料表；UNIQUE KEY；varchar(60) |
| `production_data_machine` | `equipment_name` | `equipment` | `no` | denormalized_or_label | 機具名稱，關連至equipment資料表；varchar(60) |
| `production_data_machine` | `equipment_no` | `equipment` | `no` | high | 機具no，關連至equipment資料表；UNIQUE KEY；varchar(60) |
| `production_data_machine` | `work_order_no` | `work_order` | `no` | high | 派工單no，關連至work_order資料表；UNIQUE KEY；varchar(60) |
| `production_data_output` | `item_name` | `inproduct / product` | `no` | denormalized_or_label | 產出的料品品項名稱，關連至inproduct/ product資料表；varchar(60) |
| `production_data_output` | `item_no` | `inproduct / product` | `no` | needs_review | 產出的料品品項no，關連至inproduct/ product資料表；UNIQUE KEY；varchar(60) |
| `production_data_output` | `process_order_no` | `process_order` | `no` | high | 餘廢退產單no，關連至process_order資料表；varchar(60) |
| `production_data_output` | `work_order_no` | `work_order` | `no` | high | 派工單no，關連至work_order資料表；UNIQUE KEY；varchar(60) |
| `production_data_reuse` | `item_name` | `inproduct` | `no` | denormalized_or_label | 餘廢料品項名稱，關連至inproduct資料表；varchar(60) |
| `production_data_reuse` | `item_no` | `inproduct` | `no` | high | 餘廢料品項no，關連至inproduct資料表；UNIQUE KEY；varchar(60) |
| `production_data_reuse` | `process_order_no` | `process_order` | `no` | high | 餘廢退產單no，關連至process_order資料表；UNIQUE KEY；varchar(60) |
| `production_data_reuse` | `work_order_no` | `work_order` | `no` | high | 派工單no，關連至work_order資料表；UNIQUE KEY；varchar(60) |
| `production_line` | `factory_no` | `factory` | `no` | high | 廠區no，關連至factory 資料表；varchar(60) |
| `production_line` | `process_no` | `process` | `no` | high | 製程no，關連至process資料表；varchar(60) |
| `purchase_order` | `creator_no` | `employee` | `no` | high | 製單人員no，關連至employee資料表；varchar(60) |
| `purchase_order` | `item_name` | `trans_items` | `no` | denormalized_or_label | 交易品項名稱，關連至trans_items資料表；varchar(60) |
| `purchase_order` | `item_no` | `trans_items` | `no` | high | 交易品項no，關連至trans_items資料表；varchar(60) |
| `purchase_order` | `item_ref_displayName` | `company` | `no` | denormalized_or_label | 客戶/廠商公司簡稱，關連至company資料表；varchar(60) |
| `purchase_order` | `item_ref_no` | `company` | `no` | high | 客戶/廠商no，關連至company資料表；varchar(60) |
| `purchase_order` | `purchase_request_no` | `purchase_request` | `no` | high | 請購單no，關連至purchase_request資料表；varchar(60) |
| `purchase_order` | `ref_no` | `contract` | `no` | high | 合約no，關連至contract資料表；varchar(60) |
| `purchase_request` | `creator_no` | `employee` | `no` | high | 製單人員no，關連至employee資料表；varchar(60) |
| `purchase_request` | `product_order_no` | `product_order` | `no` | high | 訂購單no，關連至product_order資料表；varchar(60) |
| `purchase_request_item` | `item_no` | `material` | `no` | high | 料品品項no，關連至material資料表；varchar(60) |
| `purchase_request_item` | `purchase_request_no` | `purchase_request` | `no` | high | 請購單no，關連至purchase_request資料表；UNIQUE KEY；varchar(60) |
| `quotation` | `creator_no` | `employee` | `no` | high | 製單人員no，關連至employee資料表；varchar(60) |
| `quotation` | `item_name` | `trans_items / trans_items2` | `no` | denormalized_or_label | 交易品項名稱，關連至trans_items/ trans_items2資料表 |
| `quotation` | `item_no` | `trans_items / trans_items2` | `no` | needs_review | 交易品項no，關連至trans_items / trans_items2資料表 |
| `quotation` | `item_ref_displayName` | `company` | `no` | denormalized_or_label | 客戶/廠商公司簡稱，關連至company資料表；varchar(60) |
| `quotation` | `item_ref_no` | `company` | `no` | high | 客戶/廠商no，關連至company資料表；varchar(60) |
| `sample_price` | `item_no` | `bom` | `no` | high | 商品配方no，關連至bom資料表；UNIQUE KEY；varchar(60) |
| `session` | `user_no` | `employee` | `no` | high | 員工no，關連至employee資料表；varchar(60) |
| `ship_wh` | `company_displayName` | `company` | `no` | denormalized_or_label | 廠商公司簡稱，關連至company資料表；varchar(60) |
| `ship_wh` | `company_no` | `company` | `no` | high | 廠商資料no，關連至company資料表；varchar(60) |
| `ship_wh_contract` | `item_name` | `ship_wh` | `no` | denormalized_or_label | 物流倉儲資料displayName，關連至ship_wh資料表；varchar(60) |
| `ship_wh_contract` | `item_no` | `ship_wh` | `no` | high | 物流倉儲資料no，關連至ship_wh資料表；varchar(60) |
| `ship_wh_contract` | `item_ref_displayName` | `company` | `no` | denormalized_or_label | 客戶/廠商公司簡稱，關連至company資料表；varchar(60) |
| `ship_wh_contract` | `item_ref_no` | `company` | `no` | high | 客戶/廠商no，關連至company資料表；varchar(60) |
| `ship_wh_contract` | `ref_no` | `ship_wh_quotation` | `no` | high | 物流倉儲議價no，關連至ship_wh_quotation資料表；varchar(60) |
| `ship_wh_contract` | `sw_alias_no` | `ship_wh_alias` | `no` | high | 物流倉儲別名no，關連至ship_wh_alias資料表；varchar(60) |
| `ship_wh_quotation` | `item_name` | `ship_wh` | `no` | denormalized_or_label | 物流倉儲簡稱，關連至ship_wh資料表；varchar(60) |
| `ship_wh_quotation` | `item_no` | `ship_wh` | `no` | high | 物流倉儲no，關連至ship_wh資料表；varchar(60) |
| `ship_wh_quotation` | `item_ref_displayName` | `company` | `no` | denormalized_or_label | 客戶/廠商公司簡稱，關連至company資料表；varchar(60) |
| `ship_wh_quotation` | `item_ref_no` | `company` | `no` | high | 客戶/廠商no，關連至company資料表；varchar(60) |
| `shipping_order` | `creator_no` | `employee` | `no` | high | 製單人員no，關連至employee資料表；varchar(60) |
| `shipping_order` | `item_name` | `trans_items` | `no` | denormalized_or_label | 交易品項名稱，關連至trans_items資料表；varchar(60) |
| `shipping_order` | `item_no` | `trans_items` | `no` | high | 交易品項no，關連至trans_items資料表；varchar(60) |
| `shipping_order` | `item_ref_displayName` | `company` | `no` | denormalized_or_label | 客戶/廠商公司簡稱，關連至company資料表；varchar(60) |
| `shipping_order` | `item_ref_no` | `company` | `no` | high | 客戶/廠商no，關連至company資料表；varchar(60) |
| `shipping_order` | `product_order_no` | `product_order` | `no` | high | 訂購單no，關連至product_order資料表；varchar(60) |
| `shipping_payment` | `item_ref_displayName` | `company` | `no` | denormalized_or_label | 客戶/廠商公司簡稱，關連至company資料表；varchar(60) |
| `shipping_payment` | `item_ref_no` | `company` | `no` | high | 客戶/廠商no，關連至company資料表；varchar(60) |
| `shipping_payment` | `record_no` | `shipping_record` | `no` | needs_review | 物流紀錄，關聯至shipping_record資料表；varchar(60) |
| `shipping_payment` | `ref_no` | `product_order / purchase_order` | `no` | needs_review | 採購單 no/訂購單 no，關聯至product_order /purchase_order資料表；varchar(60) |
| `shipping_payment` | `ref_sub_no` | `goods_receipt_note / shipping_order` | `no` | needs_review | 進貨單 no/ 銷貨單 no，關聯至goods_receipt_note /shipping_order資料表；varchar(60) |
| `shipping_record` | `contract_no` | `ship_wh_contract` | `no` | high | 物流合約no，關連至ship_wh_contract資料表；varchar(60) |
| `shipping_record` | `item_name` | `ship_wh` | `no` | denormalized_or_label | 物流名稱 (交易品項)，關連至ship_wh資料表；varchar(60) |
| `shipping_record` | `item_no` | `ship_wh` | `no` | high | 物流no (交易品項)，關連至ship_wh資料表；varchar(60) |
| `shipping_record` | `item_ref_displayName` | `company` | `no` | denormalized_or_label | 客戶/廠商公司簡稱，關連至company資料表；varchar(60) |
| `shipping_record` | `item_ref_no` | `company` | `no` | high | 客戶/廠商no，關連至company資料表；varchar(60) |
| `shipping_record` | `ref_no` | `goods_receipt_note / shipping_order` | `no` | needs_review | 進貨單 no/ 銷貨單 no，關聯至goods_receipt_note /shipping_order資料表；varchar(60) |
| `shipping_record` | `ref_parent_no` | `product_order / purchase_order` | `no` | needs_review | 採購單 no/訂購單 no，關聯至product_order /purchase_order資料表；varchar(60) |
| `shipping_record` | `sw_alias_name` | `ship_wh_alias` | `no` | denormalized_or_label | 物流別名名稱，關連至ship_wh_alias資料表；varchar(60) |
| `shipping_record` | `sw_alias_no` | `ship_wh_alias` | `no` | high | 物流別名no，關連至ship_wh_alias資料表；varchar(60) |
| `station` | `productionline_no` | `production_line` | `no` | high | 產線，關連至production_line資料表；varchar(60) |
| `trans_items` | `company_displayName` | `company` | `no` | denormalized_or_label | 客戶公司簡稱，關連至company資料表；varchar(60) |
| `trans_items` | `company_no` | `company` | `no` | high | 客戶資料no，關連至company資料表；varchar(60) |
| `trans_items` | `item_name` | `material / inproduct / product` | `no` | denormalized_or_label | 料品品項名稱，關連至material/inproduct/product資料表；varchar(60) |
| `trans_items` | `item_no` | `material / inproduct / product` | `no` | needs_review | 料品品項no，關連至material/inproduct/product資料表；varchar(60) |
| `trans_items2` | `company_displayName` | `company` | `no` | denormalized_or_label | 客戶公司簡稱，關連至company資料表；varchar(60) |
| `trans_items2` | `company_no` | `company` | `no` | high | 客戶資料no，關連至company資料表；varchar(60) |
| `user_group` | `users` | `employee` | `no` | denormalized_or_label | 員工no，關聯至employee資料表；longtext |
| `warehouse_payment` | `batch_no` | `batch_number` | `no` | high | 批號no，關聯至batch_number資料表；varchar(60) |
| `warehouse_payment` | `item_ref_displayName` | `company` | `no` | denormalized_or_label | 客戶/廠商公司簡稱，關連至company資料表；varchar(60) |
| `warehouse_payment` | `item_ref_no` | `company` | `no` | high | 客戶/廠商no，關連至company資料表；varchar(60) |
| `warehouse_payment` | `record_no` | `warehouse_record` | `no` | needs_review | 倉儲紀錄id，關聯至warehouse_record資料表；varchar(60) |
| `warehouse_record` | `batch_no` | `batch_number` | `no` | high | 批號，關連至batch_number資料表；varchar(20) |
| `warehouse_record` | `contract_no` | `ship_wh_contract` | `no` | high | 倉儲合約no，關連至ship_wh_contract資料表；varchar(60) |
| `warehouse_record` | `item_name` | `ship_wh` | `no` | denormalized_or_label | 倉儲名稱 (交易品項)，關連至ship_wh資料表；varchar(60) |
| `warehouse_record` | `item_no` | `ship_wh` | `no` | high | 倉儲no (交易品項)，關連至ship_wh資料表；varchar(60) |
| `warehouse_record` | `item_ref_displayName` | `company` | `no` | denormalized_or_label | 客戶/廠商公司簡稱，關連至company資料表；varchar(60) |
| `warehouse_record` | `item_ref_no` | `company` | `no` | high | 客戶/廠商no，關連至company資料表；varchar(60) |
| `warehouse_record` | `ref_no` | `inventory_record` | `no` | needs_review | 出入庫紀錄id，關連至inventory_record資料表；int |
| `warehouse_record` | `sw_alias_name` | `ship_wh_alias` | `no` | denormalized_or_label | 倉儲別名，關連至ship_wh_alias資料表；varchar(60) |
| `warehouse_record` | `sw_alias_no` | `ship_wh_alias` | `no` | high | 倉儲別名no，關連至ship_wh_alias資料表；varchar(60) |
| `work_order` | `aps_no` | `aps_quantity` | `no` | high | APS排程編號，關連至aps_quantity資料表；varchar(60) |
| `work_order` | `creator_no` | `employee` | `no` | high | 製單人員no，關連至employee資料表；varchar(60) |
| `work_order` | `customer_displayName` | `company` | `no` | denormalized_or_label | 客戶公司簡稱，關連至company資料表；varchar(60) |
| `work_order` | `customer_no` | `company` | `no` | high | 客戶no，關連至company資料表；varchar(60) |
| `work_order` | `laborList` | `employee` | `no` | denormalized_or_label | 預估投產人數清單；員工no，關連至employee資料表(JOSN Array)；longtext |
| `work_order` | `output_item_name` | `inproduct / product` | `no` | denormalized_or_label | 產出的料品品項名稱，關連至inproduct/ product資料表；varchar(60) |
| `work_order` | `output_item_no` | `inproduct / product` | `no` | needs_review | 產出的料品品項no，關連至inproduct/ product資料表 |
| `work_order` | `product_name` | `product` | `no` | denormalized_or_label | 交易品項名稱，關連至product 資料表；varchar(60) |
| `work_order` | `product_no` | `product` | `no` | high | 交易品項no，關連至product資料表；varchar(60) |
| `work_order` | `product_order_no` | `product_order` | `no` | high | 訂購單id，關連至product_order資料表；varchar(60) |
| `work_order` | `production_line_no` | `production_line` | `no` | high | 生產線no，關連至production_line資料表；varchar(60) |
