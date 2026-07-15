# ERP 2.0 Database Schema Index

> Source baseline: `docs/database/EWDB_20260526.sql`  
> Reference document: `docs/database/食品管理系統Database Schema_0.0.26.docx`  
> Generated: 2026-05-28  
> Rule: SQL is the final schema baseline. The Word document is used only as supplemental description. If they conflict, this document follows SQL.

## Table of Contents

- [aps_quantity](#aps_quantity)
- [aps_quantity_item](#aps_quantity_item)
- [bank_account](#bank_account)
- [batch_number](#batch_number)
- [batchno_serialno](#batchno_serialno)
- [batchno_serialno_group](#batchno_serialno_group)
- [bom](#bom)
- [bom1](#bom1)
- [bom1_number](#bom1_number)
- [bom2](#bom2)
- [bom2_number](#bom2_number)
- [bom_item](#bom_item)
- [company](#company)
- [contract](#contract)
- [device](#device)
- [device_log](#device_log)
- [employee](#employee)
- [enterprise](#enterprise)
- [equipment](#equipment)
- [factory](#factory)
- [goods](#goods)
- [goods_receipt_note](#goods_receipt_note)
- [inproduct](#inproduct)
- [inproduct_bom_spec](#inproduct_bom_spec)
- [inventory_delta](#inventory_delta)
- [inventory_item_month_statistic](#inventory_item_month_statistic)
- [inventory_month_statistic](#inventory_month_statistic)
- [inventory_order](#inventory_order)
- [inventory_record](#inventory_record)
- [item_hours](#item_hours)
- [item_loss](#item_loss)
- [item_price](#item_price)
- [labor_wage](#labor_wage)
- [material](#material)
- [member](#member)
- [order_item_month_statistic](#order_item_month_statistic)
- [order_payment](#order_payment)
- [payment](#payment)
- [pl_item_capacity](#pl_item_capacity)
- [pl_item_loss](#pl_item_loss)
- [pl_man_capacity](#pl_man_capacity)
- [process](#process)
- [process_capacity](#process_capacity)
- [process_flow](#process_flow)
- [process_labor](#process_labor)
- [process_order](#process_order)
- [product](#product)
- [product_bom_spec](#product_bom_spec)
- [product_order](#product_order)
- [product_process](#product_process)
- [product_spec](#product_spec)
- [product_ver](#product_ver)
- [production_data](#production_data)
- [production_data_input](#production_data_input)
- [production_data_labor](#production_data_labor)
- [production_data_machine](#production_data_machine)
- [production_data_output](#production_data_output)
- [production_data_reuse](#production_data_reuse)
- [production_line](#production_line)
- [production_line_daily_capacity](#production_line_daily_capacity)
- [production_line_downtime](#production_line_downtime)
- [purchase_order](#purchase_order)
- [purchase_request](#purchase_request)
- [quotation](#quotation)
- [rw_items](#rw_items)
- [sample_price](#sample_price)
- [session](#session)
- [ship_wh](#ship_wh)
- [ship_wh_alias](#ship_wh_alias)
- [ship_wh_contract](#ship_wh_contract)
- [ship_wh_quotation](#ship_wh_quotation)
- [shipping_order](#shipping_order)
- [shipping_payment](#shipping_payment)
- [shipping_record](#shipping_record)
- [station](#station)
- [trans_items](#trans_items)
- [trans_items2](#trans_items2)
- [user_group](#user_group)
- [warehouse_payment](#warehouse_payment)
- [warehouse_record](#warehouse_record)
- [warehouse_inventory_reservation](#warehouse_inventory_reservation)
- [warehouse_quality_hold](#warehouse_quality_hold)
- [warehouse_pallet_movement](#warehouse_pallet_movement)
- [item_safety_stock](#item_safety_stock)
- [warehouse_risk_rule](#warehouse_risk_rule)
- [workflow_task_state](#workflow_task_state)
- [workflow_task_event](#workflow_task_event)
- [workflow_next_owner_rule](#workflow_next_owner_rule)
- [work_order](#work_order)

## Generation Notes

- Total SQL tables documented: 79.
- `Status = OK` means the field meaning can be reasonably determined from SQL schema, constraints, relation, enum definition, or Word description.
- `Status = Need Review` means the field is preserved exactly from SQL but its business meaning or value domain should be confirmed.
- `Index` marks `PK` and `UK(constraint_name)` based on SQL.
- `Foreign Key` uses `table.column -> referenced_table.referenced_column` format based on SQL `ALTER TABLE` constraints.

## aps_quantity


<summary>aps_quantity (製造所需總量時)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| no | VARCHAR(60) | No | UK(uq_aps_quantity_composite) |  | 編號；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| product_order_no | VARCHAR(60) | No | UK(uq_aps_quantity_composite) | aps_quantity.product_order_no -> product_order.no | 訂購訂單no，關連至product_order資料表；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| oneProcess | INT | No | UK(uq_aps_quantity_composite) |  | 主製程；UNIQUE KEY；int數值如下其中之一 前備 (1)、加工 (2)、包裝 (3) 、其他 (0) | 前備 (1)、加工 (2)、包裝 (3) 、其他 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| secProcess | INT | No | UK(uq_aps_quantity_composite) |  | 次製程；UNIQUE KEY；int前備；數值如下其中之一調拌 (1)、塞料 (2)、烘烤(3)、灌料(4) 、其他 (0)加工；數值如下其中之一披覆 (1)、封膜 (2) 、其他 (0)包裝；數值如下其中之一成組 (1)、入箱 (2) 、其他 (0) | 調拌 (1)、塞料 (2)、烘烤(3)、灌料(4) 、其他 (0)加工；數值如下披覆 (1)、封膜 (2) 、其他 (0)包裝；數值如下成組 (1)、入箱 (2) 、其他 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_no | VARCHAR(60) | No | UK(uq_aps_quantity_composite) |  | 產出的料品品項no，關連至inproduct/product資料表；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_name | VARCHAR(60) | Yes |  |  | 產出的料品品項名稱，關連至inproduct/product資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| itemCategory | INT | Yes |  |  | 產出的料品品項類別；int數值如下其中之一：原料 (1)、物料 (2)、膠捲 (3) 、在製品 (4) 、製成品 (5) | 原料 (1)、物料 (2)、膠捲 (3) 、在製品 (4) 、製成品 (5) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| unit | INT | Yes |  |  | 產出數量單位；int數值如下其中之一： 公斤、其他 參照「Unit單位定義」 | 其他 (0)、公克 (1)、公斤 (2)、台斤 (3)、公分 (51)、公尺 (52)、個 (101)、條 (102)、片 (103)、張 (104)、罐 (105)、包 (106)、捲 (107)、桶 (108)、盒 (109)、組 (110)、箱 (111)、支 (112)、式 (113)、入 (114)、袋 (115)、顆 (116)、瓶 (117)、板 (201)、件 (202)、車 (203)、次 (204) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| amount | FLOAT | Yes |  |  | 需求產量或數量 (小數點2位) ；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| minutes | INT | Yes |  |  | 製造所需總分鐘數；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| laborCount | INT | Yes |  |  | 製造所需人力；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## aps_quantity_item


<summary>aps_quantity_item (製造所需料品品項)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| product_order_no | VARCHAR(60) | No | UK(uq_aps_quantity_item_composite) | aps_quantity_item.product_order_no -> product_order.no | 訂購訂單no，關連至product_order資料表；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| output_item_no | VARCHAR(60) | No | UK(uq_aps_quantity_item_composite) |  | 產出的在製品/製成品no，關連至inproduct/product資料表；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| oneProcess | INT | No | UK(uq_aps_quantity_item_composite) |  | 主製程；UNIQUE KEY；int數值如下其中之一 前備 (1)、加工 (2)、包裝 (3) 、其他 (0) | 前備 (1)、加工 (2)、包裝 (3) 、其他 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| secProcess | INT | No | UK(uq_aps_quantity_item_composite) |  | 次製程；UNIQUE KEY；int前備；數值如下其中之一調拌 (1)、塞料 (2)、烘烤(3)、灌料(4) 、其他 (0)加工；數值如下其中之一披覆 (1)、封膜 (2) 、其他 (0) 包裝；數值如下其中之一成組 (1)、入箱 (2) 、其他 (0) | 調拌 (1)、塞料 (2)、烘烤(3)、灌料(4) 、其他 (0)加工；數值如下披覆 (1)、封膜 (2) 、其他 (0) 包裝；數值如下成組 (1)、入箱 (2) 、其他 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_no | VARCHAR(60) | No | UK(uq_aps_quantity_item_composite) | aps_quantity_item.item_no -> material.no | 投入的料品品項no，關連至material資料表；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_name | VARCHAR(60) | Yes |  |  | 投入的料品品項名稱，關連至material資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| itemCategory | INT | Yes |  |  | 投入的料品品項類別；int數值如下其中之一：原料 (1)、物料 (2)、膠捲 (3) 、在製品 (4) 、製成品 (5) | 原料 (1)、物料 (2)、膠捲 (3) 、在製品 (4) 、製成品 (5) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| unit | INT | Yes |  |  | 投入的數量單位；int數值如下其中之一： 公斤、公尺、個、其他 參照「Unit單位定義」 | 其他 (0)、公克 (1)、公斤 (2)、台斤 (3)、公分 (51)、公尺 (52)、個 (101)、條 (102)、片 (103)、張 (104)、罐 (105)、包 (106)、捲 (107)、桶 (108)、盒 (109)、組 (110)、箱 (111)、支 (112)、式 (113)、入 (114)、袋 (115)、顆 (116)、瓶 (117)、板 (201)、件 (202)、車 (203)、次 (204) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| count | FLOAT | Yes |  |  | 投入重量、長度、數量(小數點2位) ；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## bank_account


<summary>bank_account (恆旺食品銀行帳戶)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| category | INT | Yes |  |  | 類型；int數值如下其中之一：零用金(1)、銀行帳戶 (0) | 零用金(1)、銀行帳戶 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| currency | INT | Yes |  |  | 幣別；int數值如下其中之一：美金(1)、新台幣 (0) | 美金(1)、新台幣 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| displayName | VARCHAR(60) | Yes |  |  | 帳戶簡稱 (簡稱) ；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| name | VARCHAR(60) | Yes |  |  | 銀行名稱；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| branch | VARCHAR(60) | Yes |  |  | 分行名稱；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| account | VARCHAR(60) | Yes |  |  | 銀行戶名；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| number | VARCHAR(60) | No | UK(uq_bank_account_composite) |  | 銀行帳號；varchar(60)；UNIQUE KEY |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## batch_number


<summary>batch_number (批號)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| date | INT | Yes |  |  | 進貨或生產日期；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| no | VARCHAR(60) | No | UK(uq_batch_number_composite) |  | 批號；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creator_no | VARCHAR(60) | Yes |  | batch_number.creator_no -> employee.no | 製單人員no，關連至employee資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| ref_no | VARCHAR(60) | No | UK(uq_batch_number_composite) |  | 進貨單no / 銷貨單no / 領退餘廢產單 no，關連至goods_receipt_note/work_order/process_order資料表；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| refCategory | INT | Yes |  |  | 單號類別；int數值如下其中之一 1: 採購 2: 製造 3: 銷貨退回 | 採購(1)、 製造(2)、 銷貨退回(3) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_no | VARCHAR(60) | Yes |  |  | 品項no，關連至material/inproduct/product資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_name | VARCHAR(60) | Yes |  |  | 品項名稱，關連至material/inproduct/product資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_ref_no | VARCHAR(60) | Yes |  | batch_number.item_ref_no -> company.no | 客戶/廠商no，關連至company資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_ref_displayName | VARCHAR(60) | Yes |  |  | 客戶/廠商公司簡稱，關連至company資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| itemCategory | INT | Yes |  |  | 料品品項類別；int數值如下其中之一：原料 (1)、物料 (2)、膠捲 (3) 、在製品 (4) 、製成品 (5) 、貨品 (6)、其他 (0) | 原料 (1)、物料 (2)、膠捲 (3) 、在製品 (4) 、製成品 (5) 、貨品 (6)、其他 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| itemSubCategory | INT | Yes |  |  | 料品品項子類別；int 數值如下其中之一：料品品項類別為原料/物料/膠捲參照material的「subCategory」定義2. 料品品項類別為在製品/製成品參照inproduct/product的「category」定義3. 料品品項類別為貨品 參照goods的「subCategory」定義 | 料品品項類別為<br>1.原料/物料/膠捲:參照material的「subCategory」定義<br>2. 在製品/製成品:參照inproduct/product的「category」定義<br>3. 貨品:參照goods的「subCategory」定義 | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| itemType | INT | Yes |  |  | 品項型態；int數值如下其中之一：新料 (1)、餘料 (2)、廢料 (3) 、其他 (0) | 新料 (1)、餘料 (2)、廢料 (3) 、其他 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| unit | INT | Yes |  |  | 盤點單位；int | 其他 (0)、公克 (1)、公斤 (2)、台斤 (3)、公分 (51)、公尺 (52)、個 (101)、條 (102)、片 (103)、張 (104)、罐 (105)、包 (106)、捲 (107)、桶 (108)、盒 (109)、組 (110)、箱 (111)、支 (112)、式 (113)、入 (114)、袋 (115)、顆 (116)、瓶 (117)、板 (201)、件 (202)、車 (203)、次 (204) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| expectedCount | FLOAT | Yes |  |  | 預定數量；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| checkedCount | FLOAT | Yes |  |  | 檢定數量；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| validDays | INT | Yes |  |  | 有效天數；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| validDate | INT | Yes |  |  | 有效期限；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| validDateNo | VARCHAR(60) | Yes |  |  | 有效期限編號；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| comment | VARCHAR(128) | Yes |  |  | 備註；varchar(128)；varchar(128) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## batchno_serialno


<summary>batchno_serialno (批號流水號)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| batch_number | VARCHAR(60) | No | UK(uq_batchno_serialno_composite) |  | 批號；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| serialNo | VARCHAR(60) | No | UK(uq_batchno_serialno_composite) |  | 序號；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| ref_order_no_category | INT | Yes |  |  | 單號類型；int數值如下其中之一 1: 採購2: 訂購 3: 產製 4: 其他 | 採購 (1)、 訂購 (2)、產製 (3)、 其他 (4) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| ref_order_no | VARCHAR(60) | No | UK(uq_batchno_serialno_composite) |  | 進貨單no / 銷貨單no / 領退餘廢產單 no / 出入庫單no，關連至goods_receipt_note/work_order/process_orderr/inventory_order資料表；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| warehouse_no | VARCHAR(60) | Yes |  |  | 倉庫no，關連至ship_wh_alias；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| time | INT | Yes |  |  | 分派時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| unit | INT | Yes |  |  | 單位；int | 其他 (0)、公克 (1)、公斤 (2)、台斤 (3)、公分 (51)、公尺 (52)、個 (101)、條 (102)、片 (103)、張 (104)、罐 (105)、包 (106)、捲 (107)、桶 (108)、盒 (109)、組 (110)、箱 (111)、支 (112)、式 (113)、入 (114)、袋 (115)、顆 (116)、瓶 (117)、板 (201)、件 (202)、車 (203)、次 (204) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| expectedCount | FLOAT | Yes |  |  | 排定數量；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| count | FLOAT | Yes |  |  | 檢定數量；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| validDate | INT | Yes |  |  | 有效期限 |  | OK | Description, FK, enum, or index context is now sufficient to identify field purpose. |
| updatedTime | INT | Yes |  |  | 資料更新時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## batchno_serialno_group


<summary>batchno_serialno_group (批號成板資料)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT primary identifier. |  | OK | AUTO_INCREMENT primary identifier. |
| time | int(11) | Yes |  |  | 分派時間 |  | OK | Description, FK, enum, or index context is now sufficient to identify field purpose. |
| warehouse_no | varchar(60) | Yes |  | batchno_serialno_group.warehouse_no -> ship_wh_alias.no | 倉儲別名no，關聯至ship_wh_alias資料表；varchar(60) |  | OK | Description, FK, enum, or index context is now sufficient to identify field purpose. |
| group | varchar(60) | No | UK(uq_batchno_serialno_group_composite) |  | 棧板編號 |  | OK | Description, FK, enum, or index context is now sufficient to identify field purpose. |
| batch_number | varchar(60) | No | UK(uq_batchno_serialno_group_composite) |  | 相對應料品品項批號 |  | OK | Description, FK, enum, or index context is now sufficient to identify field purpose. |
| serialNo | varchar(60) | No | UK(uq_batchno_serialno_group_composite) |  | 相對應料品品項批號流水號 |  | OK | Description, FK, enum, or index context is now sufficient to identify field purpose. |
| count | float | Yes |  |  | 相對應料品品項數量或重量 |  | OK | Description, FK, enum, or index context is now sufficient to identify field purpose. |
| comment | varchar(60) | Yes |  |  | Free-form remark field. |  | OK | Free-form remark field. |



## bom


<summary>bom (商品配方)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| no | VARCHAR(60) | No | UK(uq_bom_composite) |  | 編號；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| displayName | VARCHAR(60) | Yes |  |  | 簡稱；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| version | INT | No | UK(uq_bom_composite) |  | 版本；UNIQUE KEY；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| date | INT | Yes |  |  | 生效日；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| unit | INT | Yes |  |  | 庫存單位/產製單位；int數值如下其中之一： 公克、其他 參照「Unit單位定義」 | 其他 (0)、公克 (1)、公斤 (2)、台斤 (3)、公分 (51)、公尺 (52)、個 (101)、條 (102)、片 (103)、張 (104)、罐 (105)、包 (106)、捲 (107)、桶 (108)、盒 (109)、組 (110)、箱 (111)、支 (112)、式 (113)、入 (114)、袋 (115)、顆 (116)、瓶 (117)、板 (201)、件 (202)、車 (203)、次 (204) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| weight | FLOAT | Yes |  |  | 重量；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| comment | VARCHAR(128) | Yes |  |  | 備註；varchar(128) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料更新時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## bom1


<summary>bom1 (原料BOM)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| parent_no | VARCHAR(60) | No | UK(uq_bom1_composite) | bom1.parent_no -> bom1_number.no | 父級BOM編號，關連至bom1_number資料表；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| parent_name | VARCHAR(60) | Yes |  |  | 父級BOM簡稱，關連至bom1_number資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| child_category | INT | Yes |  |  | 子級類別；int數值如下其中之一： 原料 (1)、在製品 (2) 、其他 (0) | 原料 (1)、在製品 (2) 、其他 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| child_id | VARCHAR(60) | No | UK(uq_bom1_composite) |  | 子級料品品項no或BOM no，關連至material /bom1_number 資料表；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| child_name | VARCHAR(60) | Yes |  |  | 子級料品品項或BOM簡稱，關連至material /bom1_number 資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| childUnit | INT | Yes |  |  | 子級材料或在製品單位；int數值如下其中之一： 公克 (1)、單位 (2) 、其他 (0) | 公克 (1)、單位 (2) 、其他 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| weight | FLOAT | No | UK(uq_bom1_composite) |  | 淨重或單位數 (小數點4位) ；UNIQUE KEY；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| expectedLoss | FLOAT | Yes |  |  | 預估(配方)損耗率% (小數點2位) ；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| actualLoss | FLOAT | Yes |  |  | 實際(量產)損耗率% (小數點2位) ；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| processWeight | FLOAT | Yes |  |  | 實際(量產)重量 |  | OK | Description, FK, enum, or index context is now sufficient to identify field purpose. |
| comment | VARCHAR(128) | Yes |  |  | 備註；varchar(128) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## bom1_number


<summary>bom1_number (原料BOM編碼)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| no | VARCHAR(60) | No | UK(uq_bom1_number_composite) |  | BOM編號；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| displayName | VARCHAR(60) | Yes |  |  | 簡稱；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| unit | INT | Yes |  |  | 單位；int 公克、其他 參照「Unit單位定義」 | 其他 (0)、公克 (1)、公斤 (2)、台斤 (3)、公分 (51)、公尺 (52)、個 (101)、條 (102)、片 (103)、張 (104)、罐 (105)、包 (106)、捲 (107)、桶 (108)、盒 (109)、組 (110)、箱 (111)、支 (112)、式 (113)、入 (114)、袋 (115)、顆 (116)、瓶 (117)、板 (201)、件 (202)、車 (203)、次 (204) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| weight | FLOAT | Yes |  |  | 淨重；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| bom_no | VARCHAR(60) | Yes |  | bom1_number.bom_no -> bom.no | 商品配方no，關連至bom資料表；varchar(60)；類型為加工時，此欄位才會有值。 |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| bom_version | INT | Yes |  |  | 商品配方版本；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| comment | VARCHAR(128) | Yes |  |  | 備註；varchar(128) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## bom2


<summary>bom2 (物料BOM)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK>； |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| parent_no | VARCHAR(60) | Yes |  | bom2.parent_no -> bom2_number.no | 父級BOM編號，關連至bom2_number資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| parent_name | VARCHAR(60) | Yes |  |  | 父級BOM簡稱，關連至bom2_number資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| child_category | INT | Yes |  |  | 子級類別；int數值如下其中之一： 物料 (1)、膠捲 (2) 、其他 (0) | 物料 (1)、膠捲 (2) 、其他 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| child_id | VARCHAR(60) | Yes |  |  | 子級料品品項 no或BOM no，關連至material /bom2_number 資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| child_name | VARCHAR(60) | Yes |  |  | 子級料品品項或BOM簡稱，關連至material /bom2_number 資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| childUnit | INT | Yes |  |  | 子級物料重量單位；int數值如下其中之一： 公克、其他 參照「Unit單位定義」 | 公克、其他 參照「Unit單位定義」 | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| weight | FLOAT | Yes |  |  | 總重量 (小數點4位) ；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| childUnit2 | INT | Yes |  |  | 子級物料長度或數量單位；int數值如下其中之一： 公分、個、其他 參照「Unit單位定義」 | 公分、個、其他 參照「Unit單位定義」 | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| length | FLOAT | Yes |  |  | 總長度 (小數點4位) ；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| count | INT | Yes |  |  | 個數數量；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| expectedLoss | FLOAT | Yes |  |  | 預估(配方)損耗率% (小數點2位) ；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| actualLoss | FLOAT | Yes |  |  | 實際(量產)損耗率% (小數點2位) ；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| processCount | FLOAT | Yes |  |  | 實際(量產)個數數量 |  | OK | Description, FK, enum, or index context is now sufficient to identify field purpose. |
| comment | VARCHAR(128) | Yes |  |  | 備註；varchar(128) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## bom2_number


<summary>bom2_number (物料BOM編碼)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| no | VARCHAR(60) | No | UK(uq_bom2_number_composite) |  | BOM編號；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| displayName | VARCHAR(60) | Yes |  |  | 簡稱；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| unit | INT | Yes |  |  | 單位；int數值如下其中之一： 公克、其他 參照「Unit單位定義」 | 其他 (0)、公克 (1)、公斤 (2)、台斤 (3)、公分 (51)、公尺 (52)、個 (101)、條 (102)、片 (103)、張 (104)、罐 (105)、包 (106)、捲 (107)、桶 (108)、盒 (109)、組 (110)、箱 (111)、支 (112)、式 (113)、入 (114)、袋 (115)、顆 (116)、瓶 (117)、板 (201)、件 (202)、車 (203)、次 (204) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| weight | FLOAT | Yes |  |  | 淨重；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| bom_no | VARCHAR(60) | Yes |  | bom2_number.bom_no -> product.no | 料品品項no，關連至product資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| bom_version | INT | Yes |  |  | 料品品項版本；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| comment | VARCHAR(128) | Yes |  |  | 備註；varchar(128) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## bom_item


<summary>bom_item (商品配方項目)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| bom_no | VARCHAR(60) | No | UK(uq_bom_item_composite) | bom_item.bom_no -> bom.no | 商品配方no，關連至bom資料表；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_no | VARCHAR(60) | No | UK(uq_bom_item_composite) | bom_item.item_no -> material.no | 原物料no，關連至material資料表；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_name | VARCHAR(60) | Yes |  |  | 原料名稱，關連至material資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| unit | INT | Yes |  |  | 單位；int數值如下其中之一： 公克、其他 參照「Unit單位定義」 | 其他 (0)、公克 (1)、公斤 (2)、台斤 (3)、公分 (51)、公尺 (52)、個 (101)、條 (102)、片 (103)、張 (104)、罐 (105)、包 (106)、捲 (107)、桶 (108)、盒 (109)、組 (110)、箱 (111)、支 (112)、式 (113)、入 (114)、袋 (115)、顆 (116)、瓶 (117)、板 (201)、件 (202)、車 (203)、次 (204) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| weight | FLOAT | Yes |  |  | 重量；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## company


<summary>company (客戶/廠商)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| no | VARCHAR(60) | No | UK(uq_company_composite) |  | 編號；UNIQUE KEY；varchar(60)； |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| businessNo | VARCHAR(20) | No |  |  | 公司統編；varchar(20)；UNIQUE KEY |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| displayName | VARCHAR(60) | Yes |  |  | 公司簡稱；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| name | VARCHAR(60) | Yes |  |  | 公司名稱；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| address | VARCHAR(60) | Yes |  |  | 公司地址；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| phone | VARCHAR(60) | Yes |  |  | 公司電話；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| fax | VARCHAR(60) | Yes |  |  | 公司傳真；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| contactName | VARCHAR(60) | Yes |  |  | 連絡人姓名；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| contactPhone | longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin | Yes |  |  | 連絡人電話；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| contactTitle | VARCHAR(60) | Yes |  |  | 連絡人職稱；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| contactEmail | VARCHAR(60) | Yes |  |  | 連絡人電郵；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| received_id | BIGINT UNSIGNED | Yes |  | company.received_id -> payment.id | 收款資料id，關連至payment資料表 (供應商/廠商) ；INT |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| paid_id | BIGINT UNSIGNED | Yes |  | company.paid_id -> payment.id | 付款資料id，關連至payment資料表 (客戶) ；INT |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| bankDisplayName | VARCHAR(60) | Yes |  |  | 收款銀行帳戶簡稱 (簡稱) ；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| bankName | VARCHAR(60) | Yes |  |  | 收款銀行名稱；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| bankCurrency | INT | Yes |  |  | 收款銀行幣別；int數值如下其中之一：美金(1)、新台幣 (0) | 美金(1)、新台幣 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| bankBranch | VARCHAR(60) | Yes |  |  | 收款分行名稱；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| bankAccount | VARCHAR(60) | Yes |  |  | 收款銀行戶名；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| bankNo | VARCHAR(60) | Yes |  |  | 收款銀行帳號；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| comment | VARCHAR(128) | Yes |  |  | 備註；varchar(128)；varchar(128) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## contract


<summary>contract (合約)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| no | VARCHAR(60) | No | UK(uq_contract_composite) |  | 編號；UNIQUE KEY；varchar(20) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| ref_no | VARCHAR(60) | Yes |  | contract.ref_no -> quotation.no | 議價單編號，關連至quotation 資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creator_no | VARCHAR(60) | Yes |  | contract.creator_no -> employee.no | 製單人員no，關連至employee資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| date | INT | No | UK(uq_contract_composite) |  | 生效日期；UNIQUE KEY；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| displayName | VARCHAR(60) | Yes |  |  | 簡稱；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| category | INT | Yes |  |  | 合約類別；int 數值如下其中之一：採購 (1)、訂購 (2) | 採購 (1)、訂購 (2) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| type | INT | Yes |  |  | 合約樣式；int 數值如下其中之一：1.合約類別為採購採購 (1)、客供 (2)、採買 (3)、購置/保修 (4)2.合約類別為訂購產製 (1)、進銷 (2) | 合約類別為<br>1.採購: 採購 (1)、客供 (2)、採買 (3)、購置/保修 (4)<br>2.訂購: 產製 (1)、進銷 (2) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| itemStyle | INT | Yes |  |  | 品項樣式；int 數值如下其中之一：貨品 (1) 、 產品 (2) 、材料 (3)、耗品(4) 、設備(5) | 貨品 (1) 、 產品 (2) 、材料 (3)、耗品(4) 、設備(5) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_no | VARCHAR(60) | Yes |  |  | 交易品項no，關連至trans_items / trans_items2 資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_name | VARCHAR(60) | Yes |  |  | 交易品項名稱，關連至trans_items / trans_items2資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| itemCategory | INT | Yes |  |  | 料品品項類別；int數值如下其中之一：原料 (1)、物料 (2)、膠捲 (3) 、在製品 (4) 、製成品 (5) 、貨品 (6) | 原料 (1)、物料 (2)、膠捲 (3) 、在製品 (4) 、製成品 (5) 、貨品 (6) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| itemSubCategory | INT | Yes |  |  | 料品品項子類別；int數值如下其中之一：料品品項類別為原料/物料/膠捲參照material的「subCategory」定義2. 料品品項類別為在製品/製成品參照inproduct/product的「category」定義3. 料品品項類別為貨品 參照goods的「subCategory」定義 | 料品品項類別為<br>1.原料/物料/膠捲:參照material的「subCategory」定義<br>2. 在製品/製成品:參照inproduct/product的「category」定義<br>3. 貨品:參照goods的「subCategory」定義 | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_ref_no | VARCHAR(60) | Yes |  | contract.item_ref_no -> company.no | 客戶/廠商no，關連至company資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_ref_displayName | VARCHAR(60) | Yes |  |  | 客戶/廠商公司簡稱，關連至company資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| payment_id | BIGINT UNSIGNED | Yes |  | contract.payment_id -> payment.id | 帳款資料id，關連至payment資料表；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| unit | INT | Yes |  |  | 交易單位；int | 其他 (0)、公克 (1)、公斤 (2)、台斤 (3)、公分 (51)、公尺 (52)、個 (101)、條 (102)、片 (103)、張 (104)、罐 (105)、包 (106)、捲 (107)、桶 (108)、盒 (109)、組 (110)、箱 (111)、支 (112)、式 (113)、入 (114)、袋 (115)、顆 (116)、瓶 (117)、板 (201)、件 (202)、車 (203)、次 (204) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| price | DOUBLE | Yes |  |  | 單位價格 (含稅價，小數點4位)；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| shippingPrice | DOUBLE | Yes |  |  | 物流價格；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| unitConversion | DOUBLE | Yes |  |  | 規格轉換；交易品項交易單位料品品項盤點單位；double | 其他 (0)、公克 (1)、公斤 (2)、台斤 (3)、公分 (51)、公尺 (52)、個 (101)、條 (102)、片 (103)、張 (104)、罐 (105)、包 (106)、捲 (107)、桶 (108)、盒 (109)、組 (110)、箱 (111)、支 (112)、式 (113)、入 (114)、袋 (115)、顆 (116)、瓶 (117)、板 (201)、件 (202)、車 (203)、次 (204) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| comment | VARCHAR(128) | Yes |  |  | 規格；varchar(128)； |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## device


<summary>device (電子秤設備)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT primary identifier. |  | OK | AUTO_INCREMENT primary identifier. |
| no | VARCHAR(60) | No | UK(uq_device_composite) |  | Business identifier/code field. |  | OK | Business identifier/code field. |
| hardwareId | VARCHAR(128) | No | UK(uq_device_composite) |  | 電子秤設備ID |  | OK | Description, FK, enum, or index context is now sufficient to identify field purpose. |
| name | VARCHAR(60) | Yes |  |  | 電子秤設備名稱 |  | OK | Name/display label field. |
| role | INT | Yes |  |  | 設備角色； | 倉庫(1)、前備1(2) 、前備2(3) 、加工(4) 、包裝(5) | OK | Description, FK, enum, or index context is now sufficient to identify field purpose. |
| comment | VARCHAR(128) | Yes |  |  | Free-form remark field. |  | OK | Free-form remark field. |
| creationTime | INT | Yes |  |  | Creation timestamp field; confirm timestamp unit with backend convention. |  | OK | Creation timestamp field; confirm timestamp unit with backend convention. |



## device_log


<summary>device_log (電子秤設備紀錄)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT primary identifier. |  | OK | AUTO_INCREMENT primary identifier. |
| hardwareId | VARCHAR(128) | No |  |  | 電子秤設備ID |  | OK | Description, FK, enum, or index context is now sufficient to identify field purpose. |
| role | INT | Yes |  |  | 設備角色 | 倉庫(1)、前備1(2) 、前備2(3)、加工(4) 、包裝(5) | OK | Description, FK, enum, or index context is now sufficient to identify field purpose. |
| action | INT | Yes |  |  | 行為 | 採購入庫-進貨(1)、產製入庫-餘/廢/產(2)、產製退回入庫-收料(3)、銷售退回入庫(4)、其他入庫(5)、採購退回出庫(11)、產製出庫-發料(12)、銷售出庫(13)、其他出庫(14)、產製入產-領料(21)、產製出產-餘/廢/產(22)、產製出產-退料(23) | OK | Enum definition and field description identify this as the device log action code. |
| data | longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin | Yes |  |  | 回傳資料 |  | Need Review | Field is documented as returned data, but longtext payload structure is not defined in SQL or database document. |
| creationTime | INT | Yes |  |  | 資料建立時間 |  | OK | Creation timestamp field; confirm timestamp unit with backend convention. |





## employee


<summary>employee (員工)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| no | VARCHAR(60) | No | UK(uq_employee_composite) |  | 編號；UNIQUE KEY；varchar(20) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| name | VARCHAR(60) | Yes |  |  | 員工名稱；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| sex | INT | Yes |  |  | 性別；int 數值如下其中之一 1: 男 (man)2: 女 (woman) | 男(1)、 女(2) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| department | INT | Yes |  |  | 部門；int數值如下其中之一1: 管理部2: 行政部3: 業務部4: 製造部5: 品保部6: 生管部7: 倉庫部8: 總務部9: 採購部10: 研發部11: 財務部 | 管理部(1)、 行政部(2)、業務部(3)、 製造部(4)、 品保部(5)、 生管部(6)、 倉庫部(7)、 總務部(8)、 採購部(9)、 研發部(10)、 財務部(11) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| level | INT | Yes |  |  | 階級；int數值如下其中之一1: 主管2: | 主管(1)、 | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| jobTitle | VARCHAR(60) | Yes |  |  | 職稱；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| joinedDate | INT | Yes |  |  | 到職日期；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| leftDate | INT | Yes |  |  | 離職日；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| identityId | VARCHAR(60) | Yes |  |  | 身份證字號；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| country | VARCHAR(60) | Yes |  |  | 國籍；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| birthday | INT | Yes |  |  | 生日；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| phone | VARCHAR(60) | Yes |  |  | 連絡電話；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| address | VARCHAR(100) | Yes |  |  | 地址 ；varchar(100) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| type | INT | Yes |  |  | 型態；int數值如下其中之一 正職 (1)、兼職 (2) | 正職 (1)、兼職 (2) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| category | INT | Yes |  |  | 身分；int數值如下其中之一 本勞 (1)、外勞 (2)、外配 (3) | 本勞 (1)、外勞 (2)、外配 (3) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| comment | VARCHAR(128) | Yes |  |  | 備註；varchar(128) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## enterprise


<summary>enterprise (企業)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| no | VARCHAR(60) | No | UK(uq_enterprise_composite) |  | 編號；UNIQUE KEY；varchar(60)； |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| businessNo | VARCHAR(60) | No | UK(uq_enterprise_composite) |  | 公司統編；varchar(20)；UNIQUE KEY |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| displayName | VARCHAR(60) | Yes |  |  | 公司簡稱 (簡稱)； varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| name | VARCHAR(60) | Yes |  |  | 公司名稱；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| address | VARCHAR(100) | Yes |  |  | 公司地址；varchar(100) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| phone | VARCHAR(100) | Yes |  |  | 公司電話；varchar(100) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| fax | VARCHAR(100) | Yes |  |  | 公司傳真；varchar(100) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| department | INT | Yes |  |  | 公司部門數目；int(11) |  | OK | Description, FK, enum, or index context is now sufficient to identify field purpose. |
| lar | VARCHAR(100) | Yes |  |  | 公司法人代表；varchar(100) |  | OK | Description, FK, enum, or index context is now sufficient to identify field purpose. |
| comment | VARCHAR(128) | Yes |  |  | 備註；varchar(128)； |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int(11) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## equipment


<summary>equipment (機具)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| no | VARCHAR(60) | No | UK(uq_equipment_composite) |  | 編號；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| station_no | VARCHAR(60) | Yes |  | equipment.station_no -> station.no | 站點，關連至station資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| name | VARCHAR(60) | Yes |  |  | 名稱；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| model | VARCHAR(60) | Yes |  |  | 機器的型號；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| manufacturer | VARCHAR(60) | Yes |  |  | 製造機器的公司名稱；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| purchaseDate | INT | Yes |  |  | 機器的購買日期；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| appearance | VARCHAR(128) | Yes |  |  | 外觀尺寸；varchar(128) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| comment | VARCHAR(128) | Yes |  |  | 說明；varchar(128) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## factory


<summary>factory (廠區)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| no | VARCHAR(60) | No | UK(uq_factory_composite) |  | 編號；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| region | VARCHAR(60) | Yes |  |  | 地區；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| location | VARCHAR(60) | Yes |  |  | 地點；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| comment | VARCHAR(128) | Yes |  |  | 說明；varchar(128) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## goods


<summary>goods (料品品項-貨品)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| no | VARCHAR(60) | No | UK(uq_goods_composite) |  | 編號；UNIQUE KEY；varchar(20) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| category | INT | Yes |  |  | 主類型；int數值如下其中之一： (0)其他 | (0)其他 | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| subCategory | INT | Yes |  |  | 子類型；int數值如下其中之一： (0)其他 | (0)其他 | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| name | VARCHAR(100) | Yes |  |  | 品項名稱；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| unitShipping | INT | Yes |  |  | 貨運單位；int數值如下其中之一： 箱、組、桶、盒、袋、罐、式、包、其他 參照「Unit單位定義」 | 其他 (0)、公克 (1)、公斤 (2)、台斤 (3)、公分 (51)、公尺 (52)、個 (101)、條 (102)、片 (103)、張 (104)、罐 (105)、包 (106)、捲 (107)、桶 (108)、盒 (109)、組 (110)、箱 (111)、支 (112)、式 (113)、入 (114)、袋 (115)、顆 (116)、瓶 (117)、板 (201)、件 (202)、車 (203)、次 (204) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| unitWarehouse | INT | Yes |  |  | 倉儲單位；int數值如下其中之一： 箱、組、桶、盒、袋、罐、式、包、其他 參照「Unit單位定義」 | 其他 (0)、公克 (1)、公斤 (2)、台斤 (3)、公分 (51)、公尺 (52)、個 (101)、條 (102)、片 (103)、張 (104)、罐 (105)、包 (106)、捲 (107)、桶 (108)、盒 (109)、組 (110)、箱 (111)、支 (112)、式 (113)、入 (114)、袋 (115)、顆 (116)、瓶 (117)、板 (201)、件 (202)、車 (203)、次 (204) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| unitProduct | INT | Yes |  |  | 產製單位；int數值如下其中之一： 箱、組、桶、盒、袋、罐、式、包、其他 參照「Unit單位定義」 | 其他 (0)、公克 (1)、公斤 (2)、台斤 (3)、公分 (51)、公尺 (52)、個 (101)、條 (102)、片 (103)、張 (104)、罐 (105)、包 (106)、捲 (107)、桶 (108)、盒 (109)、組 (110)、箱 (111)、支 (112)、式 (113)、入 (114)、袋 (115)、顆 (116)、瓶 (117)、板 (201)、件 (202)、車 (203)、次 (204) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| comment | VARCHAR(128) | Yes |  |  | 備註；varchar(128)；varchar(128) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## goods_receipt_note


<summary>goods_receipt_note (進貨單)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| no | VARCHAR(60) | No | UK(uq_goods_receipt_note_composite) |  | 編號；UNIQUE KEY；varchar(20) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creator_no | VARCHAR(60) | Yes |  | goods_receipt_note.creator_no -> employee.no | 製單人員no，關連至employee資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| purchase_order_no | VARCHAR(60) | Yes |  | goods_receipt_note.purchase_order_no -> purchase_order.no | 採購單no，關連至purchase_order資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| date | INT | Yes |  |  | 進貨/進貨退回日期；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| category | INT | Yes |  |  | 類別；int數值如下其中之一：進貨單 (0)、進貨退回 (1) | 進貨單 (0)、進貨退回 (1) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_ref_no | VARCHAR(60) | Yes |  | goods_receipt_note.item_ref_no -> company.no | 客戶/廠商no，關連至company資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_ref_displayName | VARCHAR(60) | Yes |  |  | 客戶/廠商公司簡稱，關連至company資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_no | VARCHAR(255) | Yes |  | goods_receipt_note.item_no -> trans_items.no | 交易品項no，關連至trans_items資料表 |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_name | VARCHAR(255) | Yes |  |  | 交易品項名稱，關連至trans_items資料表 |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| itemCategory | INT | Yes |  |  | 料品品項類別；int數值如下其中之一：原料 (1)、物料 (2)、膠捲 (3) 、在製品 (4) 、製成品 (5) 、貨品 (6) | 原料 (1)、物料 (2)、膠捲 (3) 、在製品 (4) 、製成品 (5) 、貨品 (6) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| itemSubCategory | INT | Yes |  |  | 料品品項子類別；int數值如下其中之一：數值如下其中之一：1. 料品品項類別為原料/物料/膠捲參照material的「subCategory」定義2. 料品品項類別為在製品/製成品參照inproduct/product的「category」定義3. 料品品項類別為貨品 參照goods的「subCategory」定義 | 數值如下：1. 料品品項類別為原料/物料/膠捲參照material的「subCategory」定義2. 料品品項類別為在製品/製成品參照inproduct/product的「category」定義3. 料品品項類別為貨品 參照goods的「subCategory」定義 | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| unit | INT | Yes |  |  | 採購單位；int | 其他 (0)、公克 (1)、公斤 (2)、台斤 (3)、公分 (51)、公尺 (52)、個 (101)、條 (102)、片 (103)、張 (104)、罐 (105)、包 (106)、捲 (107)、桶 (108)、盒 (109)、組 (110)、箱 (111)、支 (112)、式 (113)、入 (114)、袋 (115)、顆 (116)、瓶 (117)、板 (201)、件 (202)、車 (203)、次 (204) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| price | DOUBLE | Yes |  |  | 採購單位價格 (含稅價，小數點4位)；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| expectedCount | FLOAT | Yes |  |  | 排定數量 (小數點2位) ；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| checkedCount | FLOAT | Yes |  |  | 實際數量 (小數點2位) ；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| feeCount | FLOAT | Yes |  |  | 計價數量 (小數點2位) ；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| amount | INT | Yes |  |  | 總金額 (含稅價，整數；無條件進位) ；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| addDeleteAmount | INT | Yes |  |  | 加扣金額 ；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| comment | VARCHAR(128) | Yes |  |  | 備註；varchar(128) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## inproduct


<summary>inproduct (料品品項-在製品)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| no | VARCHAR(60) | No | UK(uq_inproduct_composite) |  | 編號；UNIQUE KEY；varchar(20) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| category | INT | Yes |  |  | 主類型；int數值如下其中之一：在製品 (1)、混拌料 (2)、塞灌料 (3)、烘烤料(4)、其他 (0)餘廢料數值如下其中之一：餅體 (1)、拌料 (2)、餡料 (3)、巧克力 (4)、膠捲(5)、在製品(6)、鐵桶罐 (7) 、製成品 (8) | 料品品項為<br>1.在製品: 在製品 (1)、混拌料 (2)、塞灌料 (3)、烘烤料(4)、其他 (0)<br>2.餘廢料：餅體 (1)、拌料 (2)、餡料 (3)、巧克力 (4)、膠捲(5)、在製品(6)、鐵桶罐 (7) 、製成品 (8) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| name | VARCHAR(100) | Yes |  |  | 品項名稱；varchar(100) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| unitShipping | INT | Yes |  |  | 貨運單位；int數值如下其中之一： 式、包、支、個、片、條、捲 參照「Unit單位定義」 | 其他 (0)、公克 (1)、公斤 (2)、台斤 (3)、公分 (51)、公尺 (52)、個 (101)、條 (102)、片 (103)、張 (104)、罐 (105)、包 (106)、捲 (107)、桶 (108)、盒 (109)、組 (110)、箱 (111)、支 (112)、式 (113)、入 (114)、袋 (115)、顆 (116)、瓶 (117)、板 (201)、件 (202)、車 (203)、次 (204) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| unitWarehouse | INT | Yes |  |  | 倉儲單位；int數值如下其中之一： 式、包、支、個、片、條、捲 參照「Unit單位定義」 | 其他 (0)、公克 (1)、公斤 (2)、台斤 (3)、公分 (51)、公尺 (52)、個 (101)、條 (102)、片 (103)、張 (104)、罐 (105)、包 (106)、捲 (107)、桶 (108)、盒 (109)、組 (110)、箱 (111)、支 (112)、式 (113)、入 (114)、袋 (115)、顆 (116)、瓶 (117)、板 (201)、件 (202)、車 (203)、次 (204) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| unitProduct | INT | Yes |  |  | 產製單位；int數值如下其中之一： 式、包、支、個、片、條、捲 參照「Unit單位定義」 | 其他 (0)、公克 (1)、公斤 (2)、台斤 (3)、公分 (51)、公尺 (52)、個 (101)、條 (102)、片 (103)、張 (104)、罐 (105)、包 (106)、捲 (107)、桶 (108)、盒 (109)、組 (110)、箱 (111)、支 (112)、式 (113)、入 (114)、袋 (115)、顆 (116)、瓶 (117)、板 (201)、件 (202)、車 (203)、次 (204) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| comment | VARCHAR(128) | Yes |  |  | 備註；varchar(128)；varchar(128) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## inproduct_bom_spec


<summary>inproduct_bom_spec (在製品bom規格)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| inproduct_no | VARCHAR(60) | No | UK(uq_inproduct_bom_spec_composite) | inproduct_bom_spec.inproduct_no -> inproduct.no | 料品品項no，關連至inproduct 資料表；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| category | INT | Yes |  |  | bom類別；int數值如下其中之一： 原料 (1)、物料 (2) | 原料 (1)、物料 (2) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_no | VARCHAR(60) | No | UK(uq_inproduct_bom_spec_composite) |  | 編號；UNIQUE KEY；varchar(60)1.category為 原料商品配方編號2.category為 物料製成品編號 |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_version | INT | No | UK(uq_inproduct_bom_spec_composite) |  | UNIQUE KEY；int1.category為 原料商品配方版本2.category為 物料製成品版本 |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| bom12_no | VARCHAR(60) | No | UK(uq_inproduct_bom_spec_composite) |  | bom編號，關連至bom1_number或 bom2_number資料表的no；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| count | INT | Yes |  |  | 規格份數；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| unit | INT | Yes |  |  | 重量的單位；int數值如下其中之一： 公克、其他 參照「Unit單位定義」 | 其他 (0)、公克 (1)、公斤 (2)、台斤 (3)、公分 (51)、公尺 (52)、個 (101)、條 (102)、片 (103)、張 (104)、罐 (105)、包 (106)、捲 (107)、桶 (108)、盒 (109)、組 (110)、箱 (111)、支 (112)、式 (113)、入 (114)、袋 (115)、顆 (116)、瓶 (117)、板 (201)、件 (202)、車 (203)、次 (204) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| weight | FLOAT | Yes |  |  | 原料淨重或物料淨重數值(小數點2位) ；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## inventory_delta


<summary>inventory_delta (每日庫存Delta)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| warehouse_no | VARCHAR(60)NOT | No | UK(uq_inventory_delta_composite) | inventory_delta.warehouse_no -> ship_wh_alias.no | 倉儲別名no，關聯至ship_wh_alias資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| warehouse_displayName | VARCHAR(60) | No |  |  | 倉儲別名名稱，關聯至ship_wh_alias資料表；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| date | DATE | No | UK(uq_inventory_delta_composite) |  | 日期；UNIQUE KEY；DATE； |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| timezone | VARCHAR(60) | No | UK(uq_inventory_delta_composite) |  | 用戶端時區；UNIQUE KEY；varchar(60) |  | OK | Description, FK, enum, or index context is now sufficient to identify field purpose. |
| kind | INT | Yes |  |  | 類別；int數值如下其中之一 原物料(1)、在製品(2)、製成品(3)、批號(4) 、其他 (0) | 原物料(1)、在製品(2)、製成品(3)、批號(4) 、其他 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| category | INT | Yes |  |  | 類型；int1.原物料；數值如下其中之一 原料 (1)、物料 (2)、膠捲 (3)、其他 (0)2.在製品；數值如下其中之一 (資料庫填0) 在製品 (1)、混拌料 (2)、塞灌料 (3)、烘烤料(4) 、其他 (0)3.製成品；數值如下其中之一 (資料庫填0) 散裝品 (1)、組裝品 (2)、其他 (0)4.批號；數值如下其中之一 原料 (1)、物料 (2)、膠捲 (3)、在製品 (4)、製成品 (5) 、貨品 (6)、其他 (0) | 原料 (1)、物料 (2)、膠捲 (3)、其他 (0)2.在製品；數值如下 (資料庫填0) 在製品 (1)、混拌料 (2)、塞灌料 (3)、烘烤料(4) 、其他 (0)3.製成品；數值如下 (資料庫填0) 散裝品 (1)、組裝品 (2)、其他 (0)4.批號；數值如下 原料 (1)、物料 (2)、膠捲 (3)、在製品 (4)、製成品 (5) 、貨品 (6)、其他 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| specified_no | VARCHAR(60) | No | UK(uq_inventory_delta_composite) |  | 項目編號；UNIQUE KEY；varchar(60)1.原物料； 原物料no，關聯至material資料表2.在製品； 在製品no，關聯至inproduct資料表3.製成品； 製成品no，關聯至product資料表4.批號； 批號 no，關聯至batch_number資料表 |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| specified_name | VARCHAR(255) | Yes |  |  | 1.原物料； 原物料名稱，關聯至material資料表2.在製品； 在製品名稱，關聯至inproduct資料表3.製成品； 製成品名稱，關聯至product資料表4.批號； 無 |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| specified_ref_no | VARCHAR(60) | Yes |  |  | 項目編號；varchar(60)1.原物料2.在製品3.製成品 客戶/廠商no，關連至company資料表；varchar(60)4.批號 原物料/在製品/製成品 no，關連至material/inproduct/product資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| specified_ref_name | VARCHAR(60) | Yes |  |  | 項目名稱；varchar(60)1.原物料2.在製品3.製成品 客戶/廠商公司簡稱，關連至company資料表；varchar(60)4.批號 原物料/在製品/製成品 no，關連至material/inproduct/product資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| in_ref_id | longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin | Yes |  |  | 入庫紀錄id，關聯至inventory_record資料表 JSON Array；longtext |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| out_ref_id | longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin | Yes |  |  | 出庫紀錄id，關聯至inventory_record資料表 JSON Array；longtext |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| inCount | FLOAT | Yes |  |  | 入庫累計數量 (小數點2位) ；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| inAmount | DOUBLE | Yes |  |  | 入庫累計庫存價值 (含稅價，小數點4位) ；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| inPurchaseCount | FLOAT | Yes |  |  | 採購累計數量 (小數點2位) ；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| inPurchaseAmount | DOUBLE | Yes |  |  | 採購累計庫存價值 (含稅價，小數點4位) ；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| outCount | FLOAT | Yes |  |  | 出庫累計數量 (小數點2位) ；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| outAmount | DOUBLE | Yes |  |  | 出庫累計庫存價值 (含稅價，小數點4位) ；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## inventory_item_month_statistic


<summary>inventory_item_month_statistic (每月庫存/庫存價值)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| warehouse_no | VARCHAR(60) | No | UK(uq_inventory_item_month_statistic_composite) | inventory_item_month_statistic.warehouse_no -> ship_wh_alias.no | 倉儲別名no，關聯至ship_wh_alias資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| warehouse_displayName | VARCHAR(60) | Yes |  |  | 倉儲別名名稱，關聯至ship_wh_alias資料表；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| date | DATE | No | UK(uq_inventory_item_month_statistic_composite) |  | 日期；UNIQUE KEY；DATE； |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| timezone | VARCHAR(60) | No | UK(uq_inventory_item_month_statistic_composite) |  | 用戶端時區；UNIQUE KEY；varchar(60) |  | OK | Description, FK, enum, or index context is now sufficient to identify field purpose. |
| kind | INT | Yes |  |  | 類別；int數值如下其中之一 原物料(1)、在製品(2)、製成品(3)、批號(4) | 原物料(1)、在製品(2)、製成品(3)、批號(4) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| category | INT | Yes |  |  | 類型 |類別為 1.原物料: 原料 (1)、物料 (2)、膠捲 (3)、其他 (0)<br>2.在製品: 在製品 (1)、混拌料 (2)、塞灌料 (3)、烘烤料(4) 、其他 (0)<br>3.製成品: 散裝品 (1)、組裝品 (2)、其他 (0)<br>4.批號: 原料 (1)、物料 (2)、膠捲 (3)、在製品 (4)、製成品 (5) 、貨品 (6)、其他 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| specified_no | VARCHAR(60) | No | UK(uq_inventory_item_month_statistic_composite) |  | 項目編號；UNIQUE KEY；varchar(60)1.原物料； 原物料no，關聯至material資料表2.在製品； 在製品no，關聯至inproduct資料表3.製成品； 製成品no，關聯至product資料表4.批號； 批號 no，關聯至batch_number資料表 |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| specified_name | VARCHAR(60) | Yes |  |  | 1.原物料； 原物料名稱，關聯至material資料表2.在製品； 在製品名稱，關聯至inproduct資料表3.製成品； 製成品名稱，關聯至product資料表4.批號； 無 |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| specified_ref_no | VARCHAR(60) | No | UK(uq_inventory_item_month_statistic_composite) |  | 項目編號；UNIQUE KEY；varchar(60)1.原物料2.在製品3.製成品 客戶/廠商no，關連至company資料表；varchar(60)4.批號 原物料/在製品/製成品 no，關連至material/inproduct/product資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| specified_ref_name | VARCHAR(60) | Yes |  |  | 項目名稱 |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| unit | INT | Yes |  |  | 盤點單位；int | 其他 (0)、公克 (1)、公斤 (2)、台斤 (3)、公分 (51)、公尺 (52)、個 (101)、條 (102)、片 (103)、張 (104)、罐 (105)、包 (106)、捲 (107)、桶 (108)、盒 (109)、組 (110)、箱 (111)、支 (112)、式 (113)、入 (114)、袋 (115)、顆 (116)、瓶 (117)、板 (201)、件 (202)、車 (203)、次 (204) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| startCount | FLOAT | Yes |  |  | 期初庫存數量 (小數點2位) ；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| startAmount | DOUBLE | Yes |  |  | 期初庫存價值 (含稅價，小數點4位) ；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| inCount | FLOAT | Yes |  |  | 本期進貨數量 (小數點2位) ；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| inAmount | DOUBLE | Yes |  |  | 本期進貨價值 (含稅價，小數點4位) ；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| endCount | FLOAT | Yes |  |  | 期末庫存數量 (小數點2位) ；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| endAmount | DOUBLE | Yes |  |  | 期末庫存價值 (含稅價，小數點4位) ；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## inventory_month_statistic


<summary>inventory_month_statistic (每月庫存/庫存價值)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| warehouse_no | VARCHAR(60)NOT | No | UK(uq_inventory_month_statistic_composite) | inventory_month_statistic.warehouse_no -> ship_wh_alias.no | 倉儲別名no，關聯至ship_wh_alias資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| warehouse_displayName | VARCHAR(60) | Yes |  |  | 倉儲別名名稱，關聯至ship_wh_alias資料表；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| date | DATE | No | UK(uq_inventory_month_statistic_composite) |  | 日期；UNIQUE KEY；DATE； |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| timezone | VARCHAR(60) | No | UK(uq_inventory_month_statistic_composite) |  | 用戶端時區；UNIQUE KEY；varchar(60) |  | OK | Description, FK, enum, or index context is now sufficient to identify field purpose. |
| category | INT | No | UK(uq_inventory_month_statistic_composite) |  | 類別；int數值如下其中之一 原料 (1)、物料 (2)、膠捲 (3)、在製品(4)、製成品(5) 、貨品 (6) 、其他 (0) | 原料 (1)、物料 (2)、膠捲 (3)、在製品(4)、製成品(5) 、貨品 (6) 、其他 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| startAmount | DOUBLE | Yes |  |  | 期初庫存價值 (含稅價，小數點4位) ；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| inAmount | DOUBLE | Yes |  |  | 本期入庫價值 (含稅價，小數點4位) ；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| outAmount | DOUBLE | Yes |  |  | 本期出庫價值 (含稅價，小數點4位) ；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| inPurchaseAmount | DOUBLE | Yes |  |  | 本期進貨價值 (含稅價，小數點4位) ；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| endAmount | DOUBLE | Yes |  |  | 期末庫存價值 (含稅價，小數點4位) ；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## inventory_order


<summary>inventory_order (出入庫單)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| no | VARCHAR(60) | No | UK(uq_inventory_order_composite) |  | 編號；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creator_no | VARCHAR(60) | Yes |  | inventory_order.creator_no -> employee.no | 製單人員no，關連至employee資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| date | INT | Yes |  |  | 日期；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| category | INT | Yes |  |  | 庫存型態；int數值如下其中之一1: 入庫2: 出庫 | 入庫(1) 、出庫(2) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| subCategory | INT | Yes |  |  | 庫存子型態；int數值如下其中之一庫存型態為入庫: 庫存型態為出庫: 1: 廢品料報廢 2: 公關贈品 3: 研發打樣 | 庫存型態為 <br>1.出庫: 廢品料報廢(1) 、 公關贈品(2) 、研發打樣(3) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_no | VARCHAR(60) | Yes |  |  | 原物料/在製品/製成品no，關連至material/inproduct/product資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_name | VARCHAR(60) | Yes |  |  | 原物料/在製品/製成品no名稱，關連至material/inproduct/product資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_ref_no | VARCHAR(60) | Yes |  | inventory_order.item_ref_no -> company.no | 客戶/廠商no，關連至company資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_ref_displayName | VARCHAR(60) | Yes |  |  | 客戶/廠商公司簡稱，關連至company資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| itemCategory | INT | Yes |  |  | 品項類別；int數值如下其中之一：原料 (1)、物料 (2)、膠捲 (3) 、在製品 (4) 、製成品 (5) 、其他 (0) | 原料 (1)、物料 (2)、膠捲 (3) 、在製品 (4) 、製成品 (5) 、其他 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| itemType | INT | Yes |  |  | 品項型態；int數值如下其中之一：新料 (1)、餘料 (2)、廢料 (3) 、其他 (0) | 新料 (1)、餘料 (2)、廢料 (3) 、其他 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| unit | INT | Yes |  |  | 單位；int | 其他 (0)、公克 (1)、公斤 (2)、台斤 (3)、公分 (51)、公尺 (52)、個 (101)、條 (102)、片 (103)、張 (104)、罐 (105)、包 (106)、捲 (107)、桶 (108)、盒 (109)、組 (110)、箱 (111)、支 (112)、式 (113)、入 (114)、袋 (115)、顆 (116)、瓶 (117)、板 (201)、件 (202)、車 (203)、次 (204) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| price | DOUBLE | Yes |  |  | 銷售單位價格 (含稅價，小數點4位)；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| expectedCount | FLOAT | Yes |  |  | 排定數量 (小數點2位)；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| checkedCount | FLOAT | Yes |  |  | 實際數量 (小數點2位)；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| amount | INT | Yes |  |  | 實際數量之總金額 |  | OK | Description, FK, enum, or index context is now sufficient to identify field purpose. |
| comment | VARCHAR(128) | Yes |  |  | 備註；varchar(128)；varchar(128) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## inventory_record


<summary>inventory_record (出入庫紀錄)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creator_no | VARCHAR(60) | Yes |  | inventory_record.creator_no -> employee.no | 製單人員no，關連至employee資料表 |  | OK | Description, FK, enum, or index context is now sufficient to identify field purpose. |
| group | VARCHAR(60) | Yes |  |  | 群組編號,用於將同批出入庫但位於不同倉儲的紀錄群組化；varchar(60) |  | OK | Description, FK, enum, or index context is now sufficient to identify field purpose. |
| refCategory | INT | Yes |  |  | 關聯訂單類型；int數值如下其中之一進料單(採購) / 進貨退回出品單(銷售) / 銷貨退回領退餘廢產品單(製造)出入庫單(倉庫) | 進料單-採購 / 進貨退回(1)、出品單-銷售 / 銷貨退回(2)、領退餘廢產品單-製造(3)、出入庫單-倉庫(4) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| ref_no | VARCHAR(60) | Yes |  |  | 進料/出品/領料/退料/餘料/廢料/產品/出入庫單no，關聯至goods_receipt_note/shipping_order/process_order/ inventory_order資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| warehouse_no | VARCHAR(60) | Yes |  | inventory_record.warehouse_no -> ship_wh_alias.no | 倉儲別名no，關聯至ship_wh_alias資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| warehouse_displayName | VARCHAR(60) | Yes |  |  | 倉儲別名名稱，關聯至ship_wh_alias資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| date | INT | Yes |  |  | 出入庫時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| category | INT | Yes |  |  | 庫存型態；int數值如下其中之一1: 入庫2: 出庫 | 入庫(1)、 出庫(2) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| source | INT | Yes |  |  | 源由；int數值如下其中之一庫存型態為入庫:採購(1)、退料(2)、餘料(3)、廢料(4)、產品(5) 、銷售退回(6)、其他 (0)庫存型態為出庫:領料(1)、銷售(2)、採購退回(3) 、報廢(4) 、其他 (0) |庫存型態為<br> 1.入庫: 採購(1)、退料(2)、餘料(3)、廢料(4)、產品(5) 、銷售退回(6)、其他 (0)<br>2.出庫: 領料(1)、銷售(2)、採購退回(3) 、報廢(4) 、其他 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| batchNumber | VARCHAR(20) | Yes |  |  | 出入庫批號；varchar(20) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| serialNo | VARCHAR(20) | Yes |  |  | 批號相關聯之序號；varchar(20) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_no | VARCHAR(60) | Yes |  |  | 原物料/在製品/製成品id，關連至material/inproduct/product資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_name | VARCHAR(60) | Yes |  |  | 品項名稱，關連至material/inproduct/product資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_ref_no | VARCHAR(60) | Yes |  | inventory_record.item_ref_no -> company.no | 客戶/廠商no，關連至company資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_ref_displayName | VARCHAR(60) | Yes |  |  | 客戶/廠商公司簡稱，關連至company資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| itemCategory | INT | Yes |  |  | 品項類別；int數值如下其中之一：原料 (1)、物料 (2)、膠捲 (3) 、在製品 (4) 、製成品 (5) 、其他 (0) | 原料 (1)、物料 (2)、膠捲 (3) 、在製品 (4) 、製成品 (5) 、其他 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| itemType | INT | Yes |  |  | 品項型態；int數值如下其中之一：新料 (1)、餘料 (2)、廢料 (3) 、其他 (0) | 新料 (1)、餘料 (2)、廢料 (3) 、其他 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| unit | INT | Yes |  |  | 盤點單位；int | 其他 (0)、公克 (1)、公斤 (2)、台斤 (3)、公分 (51)、公尺 (52)、個 (101)、條 (102)、片 (103)、張 (104)、罐 (105)、包 (106)、捲 (107)、桶 (108)、盒 (109)、組 (110)、箱 (111)、支 (112)、式 (113)、入 (114)、袋 (115)、顆 (116)、瓶 (117)、板 (201)、件 (202)、車 (203)、次 (204) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| count | FLOAT | Yes |  |  | 出入庫數量 (小數點2位) ；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| price | DOUBLE | Yes |  |  | 盤點單位價格 (含稅價，小數點4位) ；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| amount | INT | Yes |  |  | 總金額 (含稅價，小數點4位) ；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| comment | VARCHAR(128) | Yes |  |  | 備註；varchar(128)；varchar(128) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| registerDevId | VARCHAR(60) | Yes |  |  | 註冊之設備ID；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## item_hours


<summary>item_hours (料品品項需時)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_no | VARCHAR(60) | No | UK(uq_item_hours_composite) |  | 料品品項no，關連至inproduct / product資料表；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| itemCategory | INT | Yes |  |  | 品項類別；int數值如下其中之一：原料 (1)、物料 (2)、膠捲 (3) 、在製品 (4) 、製成品 (5) 、其他 (0) | 原料 (1)、物料 (2)、膠捲 (3) 、在製品 (4) 、製成品 (5) 、其他 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| date | INT | No | UK(uq_item_hours_composite) |  | 生效日；UNIQUE KEY；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| unit | INT | Yes |  |  | 產製單位；int | 其他 (0)、公克 (1)、公斤 (2)、台斤 (3)、公分 (51)、公尺 (52)、個 (101)、條 (102)、片 (103)、張 (104)、罐 (105)、包 (106)、捲 (107)、桶 (108)、盒 (109)、組 (110)、箱 (111)、支 (112)、式 (113)、入 (114)、袋 (115)、顆 (116)、瓶 (117)、板 (201)、件 (202)、車 (203)、次 (204) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| estValue | DOUBLE | Yes |  |  | 預估時數；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| value | DOUBLE | Yes |  |  | 實際時數；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## item_loss


<summary>item_loss (料品品項損耗)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_no | VARCHAR(60) | No | UK(uq_item_loss_composite) |  | 料品品項no，關連至material / inproduct / product資料表；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| itemCategory | INT | Yes |  |  | 料品品項類別；int；數值如下其中之一：原料 (1)、物料 (2)、膠捲 (3) 、在製品 (4) 、製成品 (5) 、其他 (0) | 原料 (1)、物料 (2)、膠捲 (3) 、在製品 (4) 、製成品 (5) 、其他 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| date | DATE | No | UK(uq_item_loss_composite) |  | 生效日；UNIQUE KEY；DATE |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| unit | INT | Yes |  |  | 產製單位；int | 其他 (0)、公克 (1)、公斤 (2)、台斤 (3)、公分 (51)、公尺 (52)、個 (101)、條 (102)、片 (103)、張 (104)、罐 (105)、包 (106)、捲 (107)、桶 (108)、盒 (109)、組 (110)、箱 (111)、支 (112)、式 (113)、入 (114)、袋 (115)、顆 (116)、瓶 (117)、板 (201)、件 (202)、車 (203)、次 (204) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| estValue | DOUBLE | Yes |  |  | 預估比率 (小數點2位) ；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| value | DOUBLE | Yes |  |  | 比率 (小數點2位) ；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## item_price


<summary>item_price (料品品項價格)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_no | VARCHAR(60) | No | UK(uq_item_price_composite) |  | 料品品項編號，關連至material / inproduct / product / goods資料表；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_name | VARCHAR(60) | Yes |  |  | 料品品項名稱，關連至material / inproduct / product / goods資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| itemCategory | INT | Yes |  |  | 品項類別；int數值如下其中之一：原料 (1)、物料 (2)、膠捲 (3) 、在製品 (4) 、製成品 (5) 、貨品 (6) 、其他 (0) | 原料 (1)、物料 (2)、膠捲 (3) 、在製品 (4) 、製成品 (5) 、貨品 (6) 、其他 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| date | DATE | No | UK(uq_item_price_composite) |  | 年序月；UNIQUE KEY ；Date |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| whUnitWeight | INT | Yes |  |  | 盤點重量單位(庫存盤點採用的單位) ；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| costUnitWeight | INT | Yes |  |  | 成本重量單位(BOM計算的單位) ；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| estWHPriceWeight | DOUBLE | Yes |  |  | 預估盤點重量單位價格 (含稅價，小數點4位) ；double 定價 |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| estWHPriceWeight1 | DOUBLE | Yes |  |  | 預估盤點「原料」重量單位價格 (含稅價，小數點4位) ； 製成品；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| estWHPriceWeight2 | DOUBLE | Yes |  |  | 預估盤點「物料」重量單位價格 (含稅價，小數點4位) ；double；製成品 |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| estCostPriceWeight | DOUBLE | Yes |  |  | 預估成本重量單位價格 (含稅價，小數點4位) (產製品才有) ；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| estCostPriceWeight1 | DOUBLE | Yes |  |  | 預估成本「原料」重量單位價格 (含稅價，小數點4位) ；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| estCostPriceWeight2 | DOUBLE | Yes |  |  | 預估成本「物料」重量單位價格 (含稅價，小數點4位) ；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| estLaborCost | DOUBLE | Yes |  |  | 預估人工費；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| whPriceWeight | DOUBLE | Yes |  |  | 盤點重量單位價格 (含稅價，小數點4位) ；double ； 時價 |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| whPriceWeight1 | DOUBLE | Yes |  |  | 盤點「原料」重量單位價格 (含稅價，小數點4位) ；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| whPriceWeight2 | DOUBLE | Yes |  |  | 盤點「物料」重量單位價格 (含稅價，小數點4位) ；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| costPriceWeight | DOUBLE | Yes |  |  | 成本重量單位價格 (含稅價，小數點4位) ；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| costPriceWeight1 | DOUBLE | Yes |  |  | 成本「原料」重量單位價格 (含稅價，小數點4位) ；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| costPriceWeight2 | DOUBLE | Yes |  |  | 成本「物料」重量單位價格 (含稅價，小數點4位) ；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| laborCost | DOUBLE | Yes |  |  | 人工費；double；產製品才有 |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## labor_wage


<summary>labor_wage (人工時薪)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT primary identifier. |  | OK | AUTO_INCREMENT primary identifier. |
| date | INT | No | UK(uq_labor_wage_composite) |  | 生效日期 |  | OK | Description, FK, enum, or index context is now sufficient to identify field purpose. |
| type | INT | No | UK(uq_labor_wage_composite) |  | 員工型態 | 正職(1)、兼職(2) | OK | Description, FK, enum, or index context is now sufficient to identify field purpose. |
| level | INT | No | UK(uq_labor_wage_composite) |  | 員工階級 | 主管(1) | OK | Field description and enum identify this as employee wage level; current enum contains `??(1)` only, extend if additional levels are added. |
| hourly | INT | Yes |  |  | 時薪 |  | OK | Description, FK, enum, or index context is now sufficient to identify field purpose. |
| creationTime | INT | Yes |  |  | Creation timestamp field; confirm timestamp unit with backend convention. |  | OK | Creation timestamp field; confirm timestamp unit with backend convention. |



## material


<summary>material (料品品項-原物料)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| no | VARCHAR(60) | No | UK(uq_material_composite) |  | 編號；varchar(20)；UNIQUE KEY |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| category | INT | Yes |  |  | 主類型；int數值如下其中之一：原料 (1)、物料 (2)、膠捲 (3) | 原料 (1)、物料 (2)、膠捲 (3) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| subCategory | INT | Yes |  |  | 子類型；int數值如下其中之一：原料餅體 (1)、拌料 (2)、餡料 (3)、巧克力 (4)、其他 (0)物料紙盒 (1)、紙袋 (2)、塑盒 (3)、塑袋 (4)、鐵盒桶 (5)、外箱 (6)、 膠帶 (7)、膠膜 (8)、內襯 (9) 、環保稅 (10)、其他 (0)膠捲膠捲 (1)、其他 (0) | 原料餅體 (1)、拌料 (2)、餡料 (3)、巧克力 (4)、其他 (0)物料紙盒 (1)、紙袋 (2)、塑盒 (3)、塑袋 (4)、鐵盒桶 (5)、外箱 (6)、 膠帶 (7)、膠膜 (8)、內襯 (9) 、環保稅 (10)、其他 (0)膠捲膠捲 (1)、其他 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| name | VARCHAR(255) | Yes |  |  | 品項名稱； |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| unitShipping | INT | Yes |  |  | 貨運單位；int數值如下其中之一： 箱、組、桶、盒、袋… 參照「Unit單位定義」 | 其他 (0)、公克 (1)、公斤 (2)、台斤 (3)、公分 (51)、公尺 (52)、個 (101)、條 (102)、片 (103)、張 (104)、罐 (105)、包 (106)、捲 (107)、桶 (108)、盒 (109)、組 (110)、箱 (111)、支 (112)、式 (113)、入 (114)、袋 (115)、顆 (116)、瓶 (117)、板 (201)、件 (202)、車 (203)、次 (204) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| unitWarehouse | INT | Yes |  |  | 倉儲單位；int數值如下其中之一： 箱、組、桶、盒、袋、包 參照「Unit單位定義」 | 其他 (0)、公克 (1)、公斤 (2)、台斤 (3)、公分 (51)、公尺 (52)、個 (101)、條 (102)、片 (103)、張 (104)、罐 (105)、包 (106)、捲 (107)、桶 (108)、盒 (109)、組 (110)、箱 (111)、支 (112)、式 (113)、入 (114)、袋 (115)、顆 (116)、瓶 (117)、板 (201)、件 (202)、車 (203)、次 (204) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| unitProduct | INT | Yes |  |  | 產製單位；int數值如下其中之一： 箱、組、桶、盒、袋、包 參照「Unit單位定義」 | 其他 (0)、公克 (1)、公斤 (2)、台斤 (3)、公分 (51)、公尺 (52)、個 (101)、條 (102)、片 (103)、張 (104)、罐 (105)、包 (106)、捲 (107)、桶 (108)、盒 (109)、組 (110)、箱 (111)、支 (112)、式 (113)、入 (114)、袋 (115)、顆 (116)、瓶 (117)、板 (201)、件 (202)、車 (203)、次 (204) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| comment | VARCHAR(128) | Yes |  |  | 備註；varchar(128)；varchar(128) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## member


<summary>member (帳戶人員)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| user_no | VARCHAR(60) | No | UK(uq_member_composite) | member.user_no -> employee.no | 員工no，關連至employee資料表；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| account | VARCHAR(60) | Yes |  |  | 帳號；預設內建 guest 及 admin；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| password | VARCHAR(100) | Yes |  |  | 密碼；varchar(100) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## order_item_month_statistic


<summary>order_item_month_statistic (每月進銷貨金額/訂單帳款統計)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| date | DATE | No | UK(uq_order_item_month_statistic_composite) |  | 日期；UNIQUE KEY；DATE； |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| timezone | VARCHAR(60) | Yes |  |  | 用戶端時區；varchar(60) |  | OK | Description, FK, enum, or index context is now sufficient to identify field purpose. |
| kind | INT | No | UK(uq_order_item_month_statistic_composite) |  | 類別；int；UNIQUE KEY；數值如下其中之一 採購(1)、 訂購 (2) 、物流 (3) 、倉儲 (4)、費用 (5) | 採購(1)、 訂購 (2) 、物流 (3) 、倉儲 (4)、費用 (5) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| category | INT | No | UK(uq_order_item_month_statistic_composite) |  | 類型；int；UNIQUE KEY數值如下其中之一 原料 (1)、物料 (2)、膠捲 (3)、在製品 (4)、製成品 (5)、貨品 (6) | 原料 (1)、物料 (2)、膠捲 (3)、在製品 (4)、製成品 (5)、貨品 (6) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| subCategory | INT | No | UK(uq_order_item_month_statistic_composite) |  | 子類型；int；UNIQUE KEY在製品；數值如下其中之一 半成品 (0) 製成品；數值如下其中之一 散裝品 (1)、組裝品 (2)、其他 (0) | 半成品 (0) 製成品；數值如下 散裝品 (1)、組裝品 (2)、其他 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| type | INT | Yes |  |  | 帳款類型；int；數值如下其中之一現結 (0)、月結 (1) | 現結 (0)、月結 (1) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| specified_no | VARCHAR(60) | No | UK(uq_order_item_month_statistic_composite) | order_item_month_statistic.specified_no -> company.no | 公司no，關聯至company資料表；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| specified_name | VARCHAR(60) | Yes |  |  | 公司名稱，關聯至company資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| payment | INT | Yes |  |  | 帳款金額；計價數量*單價；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| amount | INT | Yes |  |  | 進銷貨金額；採購/訂購；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## order_payment


<summary>order_payment (訂單帳款)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| no | VARCHAR(60) | No | UK(uq_order_payment_composite) |  | 帳款編號；varchar(60)每日一訂單(交易品項?)一組帳款編號，出入庫時產生帳款編號 |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| group_no | VARCHAR(60) | Yes |  |  | 現結/月結帳款群組編號；varchar(60)現結的no與group_no相同；改成一個客戶每月一個帳款編號 |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| date | INT | No | UK(uq_order_payment_composite) |  | 日期；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| arapType | INT | Yes |  |  | 類型；int數值如下其中之一 1: 應收帳款 2: 應付帳款 | 應收帳款(1)、 應付帳款(2)、 | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| refCategory | INT | Yes |  |  | 訂單類別；int數值如下其中之一 採購(1)、訂購 (2) 、費用(3) 、其他 (0) | 採購(1)、訂購 (2) 、費用(3) 、其他 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| ref_no | VARCHAR(60) | Yes |  |  | 採購單 no/訂購單 no，關聯至product_order / purchase_order資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| ref_sub_no | VARCHAR(60) | Yes |  |  | 進貨單 no/ 銷貨單 no，關聯至goods_receipt_note / shipping_order資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_ref_no | VARCHAR(60) | Yes |  | order_payment.item_ref_no -> company.no | 客戶/廠商no，關連至company資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_ref_displayName | VARCHAR(60) | Yes |  |  | 客戶/廠商公司簡稱，關連至company資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| itemCategory | INT | Yes |  |  | 料品品項類型；int數值如下其中之一 原料 (1)、物料 (2)、膠捲 (3)、在製品 (4)、製成品 (5)、貨品 (6) | 原料 (1)、物料 (2)、膠捲 (3)、在製品 (4)、製成品 (5)、貨品 (6) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| itemSubCategory | INT | Yes |  |  | 料品品項子類型；int數值如下其中之一：1. 料品品項類別為原料/物料/膠捲參照material的「subCategory」定義2. 料品品項類別為在製品/製成品參照inproduct/product的「category」定義3. 料品品項類別為貨品 參照goods的「subCategory」定義 | 料品品項類別為<br>1.原料/物料/膠捲:參照material的「subCategory」定義<br>2. 在製品/製成品:參照inproduct/product的「category」定義<br>3. 貨品:參照goods的「subCategory」定義 | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| paymentType | INT | Yes |  |  | 收款類別；int數值如下其中之一：現結 (0)、月結 (1) | 現結 (0)、月結 (1) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| month | DATE | Yes |  |  | 帳款年月；DATE |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| price | DOUBLE | Yes |  |  | 單位價格 (含稅價，小數點4位) ；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| count | FLOAT | Yes |  |  | 計價數量；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| amount | INT | Yes |  |  | 帳款金額 (含稅價) ；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| addDeleteAmount | INT | Yes |  |  | 加/扣款金額 (含稅價)；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| totalAmount | INT | Yes |  |  | 總金額 (加/扣款金額+帳款金額)；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| balance | INT | Yes |  |  | 應收應付餘額 |  | OK | Description, FK, enum, or index context is now sufficient to identify field purpose. |
| creationTime | INT | Yes |  |  | 資料建立時間；int； |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## payment


<summary>payment (帳款資料)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| type | INT | No | UK(uq_payment_composite) |  | 收付款類別；UNIQUE KEY；int數值如下其中之一：現結 (0)、月結 (1) | 現結 (0)、月結 (1) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| source | INT | No | UK(uq_payment_composite) |  | 收付款方式；UNIQUE KEY；int數值如下其中之一：現金 (0)、匯款 (1)、支票 (2) | 現金 (0)、匯款 (1)、支票 (2) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| date | INT | No | UK(uq_payment_composite) |  | 結帳款日；int；UNIQUE KEY |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| period | INT | No | UK(uq_payment_composite) |  | 收付款期；int；UNIQUE KEY若收付款類型為”現結 (0)”，收付款期為”0” |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## pl_item_capacity


<summary>pl_item_capacity (產線料品產能/成本)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| month | DATE | No | UK(uq_pl_item_capacity_composite) |  | 年序月；UNIQUE KEY；Date |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| pl_no | VARCHAR(60) | No | UK(uq_pl_item_capacity_composite) | pl_item_capacity.pl_no -> production_line.no | 產線no，關聯至production_line資料表；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| pl_name | VARCHAR(60) | Yes |  |  | 產線名稱，關聯至production_line資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_no | VARCHAR(60) | No | UK(uq_pl_item_capacity_composite) |  | 產出料品品項no，關連至inproduct/product資料表；UNIQUE Key；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_name | VARCHAR(60) | Yes |  |  | 產出料品品項名稱，關連至inproduct/product資料表； varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| assembly_no | VARCHAR(60) | Yes |  |  | 產出料品品項組裝編號；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| assemblyVer | INT | Yes |  |  | 產出料品品項組裝版本；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| bomWeight | DOUBLE | Yes |  |  | 產出料品品項Bom重量；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| bomUnit | INT | Yes |  |  | 產出料品品項成分單位；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| productCount | INT | Yes |  |  | 產製次數；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| hours | FLOAT | Yes |  |  | 產製時數；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| count | FLOAT | Yes |  |  | 產製數量；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| unit | INT | Yes |  |  | 產製單位；int | 其他 (0)、公克 (1)、公斤 (2)、台斤 (3)、公分 (51)、公尺 (52)、個 (101)、條 (102)、片 (103)、張 (104)、罐 (105)、包 (106)、捲 (107)、桶 (108)、盒 (109)、組 (110)、箱 (111)、支 (112)、式 (113)、入 (114)、袋 (115)、顆 (116)、瓶 (117)、板 (201)、件 (202)、車 (203)、次 (204) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| hourlyOutput | DOUBLE | Yes |  |  | 產出物時產量；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| price | DOUBLE | Yes |  |  | 單價；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| rawMaterialCost | DOUBLE | Yes |  |  | 原料費；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| materialCost | DOUBLE | Yes |  |  | 物料費；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| laborCost | DOUBLE | Yes |  |  | 人工費；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int；日期＋時間 |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## pl_item_loss


<summary>pl_item_loss (產線料品損耗)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| month | DATE | No | UK(uq_pl_item_loss_composite) |  | 年序月；UNIQUE KEY；Date |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| pl_item_capacity_no | VARCHAR(60) | Yes |  |  | 產線料品產能，關聯至pl_item_capacity資料表；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_no | VARCHAR(60) | No | UK(uq_pl_item_loss_composite) |  | 投入料品品項no，關連至material/inproduct資料表；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_name | VARCHAR(60) | Yes |  |  | 投入料品品項品項名稱，關連至material/inproduct資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| itemCategory | INT | Yes |  |  | 料品品項類別；int數值如下其中之一：原料 (1)、物料 (2)、膠捲 (3) 、在製品 (4) 、製成品 (5) 、貨品 (6) | 原料 (1)、物料 (2)、膠捲 (3) 、在製品 (4) 、製成品 (5) 、貨品 (6) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| itemSubCategory | INT | Yes |  |  | 料品品項子類別；int數值如下其中之一：1. 料品品項類別為原料/物料/膠捲參照material的「subCategory」定義2. 料品品項類別為在製品/製成品參照inproduct/product的「category」定義3. 料品品項類別為貨品 參照goods的「subCategory」定義 | 料品品項類別為<br>1.原料/物料/膠捲:參照material的「subCategory」定義<br>2. 在製品/製成品:參照inproduct/product的「category」定義<br>3. 貨品:參照goods的「subCategory」定義 | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| weightRatio | DOUBLE | Yes |  |  | 投入物之產重比；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| lossRate | DOUBLE | Yes |  |  | 投入物之損耗率；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int；日期＋時間 |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## pl_man_capacity


<summary>pl_man_capacity (產線人時產能)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| month | DATE | No | UK(uq_pl_man_capacity_composite) |  | 年序月；UNIQUE KEY；Date |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| pl_no | VARCHAR(60) | No | UK(uq_pl_man_capacity_composite) | pl_man_capacity.pl_no -> production_line.no | 產線no，關聯至production_line資料表；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| pl_name | VARCHAR(60) | Yes |  |  | 產線名稱，關聯至production_line資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| productCount | INT | Yes |  |  | 產製次數；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| laborCount | INT | Yes |  |  | 人數；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| unit | INT | Yes |  |  | 單位；int | 其他 (0)、公克 (1)、公斤 (2)、台斤 (3)、公分 (51)、公尺 (52)、個 (101)、條 (102)、片 (103)、張 (104)、罐 (105)、包 (106)、捲 (107)、桶 (108)、盒 (109)、組 (110)、箱 (111)、支 (112)、式 (113)、入 (114)、袋 (115)、顆 (116)、瓶 (117)、板 (201)、件 (202)、車 (203)、次 (204) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| hourlyOutput | DOUBLE | Yes |  |  | 時產量；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int；日期＋時間 |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## process


<summary>process (製程)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| no | VARCHAR(60) | No | UK(uq_process_composite) |  | 編號；UNIQUE KEY；varchar(20) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| oneProcess | INT | Yes |  |  | 主製程；int數值如下其中之一 前備 (1)、加工 (2)、包裝 (3) | 前備 (1)、加工 (2)、包裝 (3) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| secProcess | INT | Yes |  |  | 次製程；int前備；數值如下其中之一調拌 (1)、塞料 (2)、烘烤(3)、灌料(4) 、其他 (0)加工；數值如下其中之一披覆 (1)、封膜 (2) 、其他 (0) 包裝；數值如下其中之一成組 (1)、入箱 (2) 、其他 (0) | 主製程為<br>1.前備:調拌 (1)、塞料 (2)、烘烤(3)、灌料(4) 、其他 (0)<br>2.加工: 披覆 (1)、封膜 (2) 、其他 (0) <br>3.包裝: 成組 (1)、入箱 (2) 、其他 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| comment | VARCHAR(128) | Yes |  |  | 說明；varchar(128) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## process_capacity


<summary>process_capacity (工序人時產能)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT <PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| date | DATE | No | UK(uq_process_capacity_composite) |  | 年序月；UNIQUE KEY；Date |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| oneProcess | INT | No | UK(uq_process_capacity_composite) |  | 主製程；UNIQUE KEY；int數值如下其中之一 前備 (1)、加工 (2)、包裝 (3) 、其他 (0) | 前備 (1)、加工 (2)、包裝 (3) 、其他 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| secProcess | INT | No | UK(uq_process_capacity_composite) |  | 次製程；UNIQUE KEY；int前備；數值如下其中之一調拌 (1)、塞料 (2)、烘烤(3)、灌料(4) 、其他 (0)加工；數值如下其中之一披覆 (1)、封膜 (2)、其他 (0)包裝；數值如下其中之一成組 (1)、入箱 (2) 、其他 (0) | 調拌 (1)、塞料 (2)、烘烤(3)、灌料(4) 、其他 (0)加工；數值如下披覆 (1)、封膜 (2)、其他 (0)包裝；數值如下成組 (1)、入箱 (2) 、其他 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| unit | INT | Yes |  |  | 單位；int | 其他 (0)、公克 (1)、公斤 (2)、台斤 (3)、公分 (51)、公尺 (52)、個 (101)、條 (102)、片 (103)、張 (104)、罐 (105)、包 (106)、捲 (107)、桶 (108)、盒 (109)、組 (110)、箱 (111)、支 (112)、式 (113)、入 (114)、袋 (115)、顆 (116)、瓶 (117)、板 (201)、件 (202)、車 (203)、次 (204) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| hourlyOutput | DOUBLE | Yes |  |  | 時產量；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| laborCount | INT | Yes |  |  | 人力人數；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| comment | VARCHAR(128) | Yes |  |  | 備註；varchar(128) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## process_flow


<summary>process_flow (工序流程)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK>； |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| no | VARCHAR(60) | No | UK(uq_process_flow_composite) |  | 編號；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| product_process_no | VARCHAR(60) | No | UK(uq_process_flow_composite) | process_flow.product_process_no -> product_process.no | 工序no，關連至product_process資料表；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| order | INT | No | UK(uq_process_flow_composite) |  | 執行優先順序；UNIQUE KEY；int |  | OK | Description, FK, enum, or index context is now sufficient to identify field purpose. |
| oneProcess | INT | Yes |  |  | 主製程；int數值如下其中之一 前備 (1)、加工 (2)、包裝 (3) 、其他 (0) | 前備 (1)、加工 (2)、包裝 (3) 、其他 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| secProcess | INT | Yes |  |  | 次製程；int前備；數值如下其中之一調拌 (1)、塞料 (2)、烘烤(3)、灌料(4) 、其他 (0)加工；數值如下其中之一披覆 (1)、封膜 (2) 、其他 (0) 包裝；數值如下其中之一成組 (1)、入箱 (2) 、其他 (0) | 調拌 (1)、塞料 (2)、烘烤(3)、灌料(4) 、其他 (0)加工；數值如下披覆 (1)、封膜 (2) 、其他 (0) 包裝；數值如下成組 (1)、入箱 (2) 、其他 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## process_labor


<summary>process_labor (人員部署)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| date | INT | Yes |  |  | 日期；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creator_no | VARCHAR(60) | Yes |  | process_labor.creator_no -> employee.no | 製單人員no，關連至employee資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| work_order_no | VARCHAR(60) | No | UK(uq_process_labor_composite) | process_labor.work_order_no -> work_order.no | 派工單no，關連至work_order資料表；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| employee_no | VARCHAR(60) | No | UK(uq_process_labor_composite) | process_labor.employee_no -> employee.no | 員工編號，關連至employee資料表；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| production_line_no | VARCHAR(60) | Yes |  | process_labor.production_line_no -> production_line.no | 產線 no，關連至production_line資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| station_no | VARCHAR(60) | Yes |  | process_labor.station_no -> station.no | 站點 no，關連至station資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## process_order


<summary>process_order (領退餘廢產單)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| no | VARCHAR(60) | No | UK(uq_process_order_composite) |  | 編號；UNIQUE KEY；varchar(20) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creator_no | VARCHAR(60) | Yes |  | process_order.creator_no -> employee.no | 製單人員no，關連至employee資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| work_order_no | VARCHAR(60) | Yes |  | process_order.work_order_no -> work_order.no | 派工單no，關連至work_order資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| refProcess | INT | Yes |  |  | 派工製程；int數值如下其中之一：前備 (1)、加工(2)、包裝 (3) | 前備 (1)、加工(2)、包裝 (3) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| date | INT | Yes |  |  | 日期；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| category | INT | Yes |  |  | 類型；int數值如下其中之一 領料 (1)、退料 (2)、餘料 (3)、廢料 (4) 、產品 (5) | 領料 (1)、退料 (2)、餘料 (3)、廢料 (4) 、產品 (5) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_no | VARCHAR(60) | Yes |  |  | 料品品項no，關連至material / inproduct / product資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_name | VARCHAR(60) | Yes |  |  | 料品品項名稱，關連至material / inproduct / product資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| itemCategory | INT | Yes |  |  | 料品品項類別；int數值如下其中之一：原料 (1)、物料 (2)、膠捲 (3) 、在製品 (4) 、製成品 (5) | 原料 (1)、物料 (2)、膠捲 (3) 、在製品 (4) 、製成品 (5) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| itemSubCategory | INT | Yes |  |  | 料品品項子類別；int數值如下其中之一：1. 料品品項類別為原料/物料/膠捲參照material的「subCategory」定義2. 料品品項類別為在製品/製成品參照inproduct/product的「category」定義3. 料品品項類別為貨品 參照goods的「subCategory」定義 | 1料品品項類別為<br>1.原料/物料/膠捲:參照material的「subCategory」定義<br>2. 在製品/製成品:參照inproduct/product的「category」定義<br>3. 貨品:參照goods的「subCategory」定義| OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_ref_no | VARCHAR(60) | Yes |  | process_order.item_ref_no -> company.no | 客戶/廠商no，關連至company資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_ref_displayName | VARCHAR(60) | Yes |  |  | 客戶/廠商公司簡稱，關連至company資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| unit | INT | Yes |  |  | 單位；int數值如下其中之一： 公斤 (1)、公尺 (2)、個 (3) 、其他 (0) | 其他 (0)、公克 (1)、公斤 (2)、台斤 (3)、公分 (51)、公尺 (52)、個 (101)、條 (102)、片 (103)、張 (104)、罐 (105)、包 (106)、捲 (107)、桶 (108)、盒 (109)、組 (110)、箱 (111)、支 (112)、式 (113)、入 (114)、袋 (115)、顆 (116)、瓶 (117)、板 (201)、件 (202)、車 (203)、次 (204) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| expectedCount | FLOAT | Yes |  |  | 重量、長度、數量(小數點2位) ；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| count | FLOAT | Yes |  |  | 重量、長度、數量(小數點2位) ；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| comment | VARCHAR(128) | Yes |  |  | 備註；varchar(128) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## product


<summary>product (料品品項-製成品)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| no | VARCHAR(60) | No | UK(uq_product_composite) |  | 編號；UNIQUE KEY；varchar(20) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| category | INT | Yes |  |  | 主類型；int數值如下其中之一： 散裝品 (1)、組裝品 (2)、其他 (0) | 散裝品 (1)、組裝品 (2)、其他 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| name | VARCHAR(100) | Yes |  |  | 品項名稱；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| unitShipping | INT | Yes |  |  | 貨運單位；int數值如下其中之一： 箱、組、桶、盒、袋、罐、式、包、其他 參照「Unit單位定義」 | 其他 (0)、公克 (1)、公斤 (2)、台斤 (3)、公分 (51)、公尺 (52)、個 (101)、條 (102)、片 (103)、張 (104)、罐 (105)、包 (106)、捲 (107)、桶 (108)、盒 (109)、組 (110)、箱 (111)、支 (112)、式 (113)、入 (114)、袋 (115)、顆 (116)、瓶 (117)、板 (201)、件 (202)、車 (203)、次 (204) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| unitWarehouse | INT | Yes |  |  | 倉儲單位；int數值如下其中之一： 箱、組、桶、盒、袋、罐、式、包、其他 參照「Unit單位定義」 | 其他 (0)、公克 (1)、公斤 (2)、台斤 (3)、公分 (51)、公尺 (52)、個 (101)、條 (102)、片 (103)、張 (104)、罐 (105)、包 (106)、捲 (107)、桶 (108)、盒 (109)、組 (110)、箱 (111)、支 (112)、式 (113)、入 (114)、袋 (115)、顆 (116)、瓶 (117)、板 (201)、件 (202)、車 (203)、次 (204) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| unitProduct | INT | Yes |  |  | 產製單位；int數值如下其中之一： 箱、組、桶、盒、袋、罐、式、包、其他 參照「Unit單位定義」 | 其他 (0)、公克 (1)、公斤 (2)、台斤 (3)、公分 (51)、公尺 (52)、個 (101)、條 (102)、片 (103)、張 (104)、罐 (105)、包 (106)、捲 (107)、桶 (108)、盒 (109)、組 (110)、箱 (111)、支 (112)、式 (113)、入 (114)、袋 (115)、顆 (116)、瓶 (117)、板 (201)、件 (202)、車 (203)、次 (204) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| version | INT | Yes |  |  | 製成品最新版本；格式為數字1.0；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| comment | VARCHAR(128) | Yes |  |  | 備註；varchar(128)；varchar(128) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## product_bom_spec


<summary>product_bom_spec (製成品規格_物料)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| product_no | VARCHAR(60) | No | UK(uq_product_bom_spec_composite) | product_bom_spec.product_no -> product.no | 製成品no，關連至product 資料表；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| product_version | INT | No | UK(uq_product_bom_spec_composite) |  | 製成品版本；UNIQUE KEY；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| level | INT | Yes |  |  | 製成品包裝階層；int數值如下其中之一： 箱規 (1)、組規 (2)、其他 (0) | 箱規 (1)、組規 (2)、其他 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| bom2_no | VARCHAR(60) | No | UK(uq_product_bom_spec_composite) | product_bom_spec.bom2_no -> bom2_number.no | bom編號，關連至bom2_number資料表的no；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| count | INT | Yes |  |  | 規格份數；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| unit | INT | Yes |  |  | 物料重量的單位；int | 其他 (0)、公克 (1)、公斤 (2)、台斤 (3)、公分 (51)、公尺 (52)、個 (101)、條 (102)、片 (103)、張 (104)、罐 (105)、包 (106)、捲 (107)、桶 (108)、盒 (109)、組 (110)、箱 (111)、支 (112)、式 (113)、入 (114)、袋 (115)、顆 (116)、瓶 (117)、板 (201)、件 (202)、車 (203)、次 (204) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| weight | FLOAT | Yes |  |  | 物料重量；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## product_order


<summary>product_order (訂購單)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| no | VARCHAR(60) | No | UK(uq_product_order_composite) |  | 編號；UNIQUE KEY；varchar(20) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creator_no | VARCHAR(60) | Yes |  | product_order.creator_no -> employee.no | 製單人員no，關連至employee資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| date | INT | Yes |  |  | 訂單日期；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| ref_no | VARCHAR(60) | Yes |  | product_order.ref_no -> contract.no | 合約no，關連至contract資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_ref_no | VARCHAR(60) | Yes |  | product_order.item_ref_no -> company.no | 客戶/廠商no，關連至company資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_ref_displayName | VARCHAR(60) | Yes |  |  | 客戶/廠商公司簡稱，關連至company資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_no | VARCHAR(60) | Yes |  | product_order.item_no -> trans_items.no | 交易品項no，關連至trans_items 資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_name | VARCHAR(60) | Yes |  |  | 交易品項名稱，關連至trans_items資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| unit | INT | Yes |  |  | 銷售單位；int | 其他 (0)、公克 (1)、公斤 (2)、台斤 (3)、公分 (51)、公尺 (52)、個 (101)、條 (102)、片 (103)、張 (104)、罐 (105)、包 (106)、捲 (107)、桶 (108)、盒 (109)、組 (110)、箱 (111)、支 (112)、式 (113)、入 (114)、袋 (115)、顆 (116)、瓶 (117)、板 (201)、件 (202)、車 (203)、次 (204) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| price | DOUBLE | Yes |  |  | 銷售單位價格 (含稅價，小數點4位) ；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| count | FLOAT | Yes |  |  | 訂單數量 (小數點2位) ；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| preparedCount | FLOAT | Yes |  |  | 備貨數量 (小數點2位) ；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| amount | INT | Yes |  |  | 總金額 (含稅價，整數) ；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| expectedDate | INT | Yes |  |  | 預計交貨日期；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| address | VARCHAR(100) | Yes |  |  | 預計交貨地址；varchar(100) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| payment_type | INT | Yes |  |  | 收付款類別；int數值如下其中之一：現結 (0)、月結 (1) | 現結 (0)、月結 (1) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| payment_source | INT | Yes |  |  | 收付款方式；int數值如下其中之一：現金 (0)、匯款 (1)、支票 (2) | 現金 (0)、匯款 (1)、支票 (2) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| payment_date | INT | Yes |  |  | 結帳款日；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| payment_period | INT | Yes |  |  | 收付款期；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| comment | VARCHAR(128) | Yes |  |  | 備註；varchar(128) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## product_process


<summary>product_process (工序)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK>； |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| no | VARCHAR(60) | No | UK(uq_product_process_composite) |  | 編號；UNIQUE KEY；varchar(20) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_no | VARCHAR(60) | No | UK(uq_product_process_composite) |  | 料品品項no，關連至inproduct/product資料表；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| version | INT | No | UK(uq_product_process_composite) |  | 版本；UNIQUE KEY；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| date | INT | Yes |  |  | 生效日；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## product_spec


<summary>product_spec (製成品規格_在製品/製成品)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| product_no | VARCHAR(60) | No | UK(uq_product_spec_composite) | product_spec.product_no -> product.no | 製成品no，關連至product 資料表；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| product_version | INT | No | UK(uq_product_spec_composite) |  | 製成品版本號；UNIQUE KEY；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| bom_no | VARCHAR(60) | Yes |  |  | 商品配方no；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| bom_version | INT | Yes |  |  | 商品配方版本；格式為數字1.0；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| level | INT | Yes |  |  | 製成品包裝階層；int數值如下其中之一： 箱規 (1)、組規 (2)、其他 (0) | 箱規 (1)、組規 (2)、其他 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_type | INT | Yes |  |  | 品項類別；int數值如下其中之一： 在製品 (1)、製成品 (2)、其他 (0) | 在製品 (1)、製成品 (2)、其他 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_no | VARCHAR(60) | No | UK(uq_product_spec_composite) |  | 在製品no或製成品no，關連至inproduct 或 product資料表；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| count | INT | Yes |  |  | 規格份數；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| unit | INT | Yes |  |  | 內含物重量的單位；int | 其他 (0)、公克 (1)、公斤 (2)、台斤 (3)、公分 (51)、公尺 (52)、個 (101)、條 (102)、片 (103)、張 (104)、罐 (105)、包 (106)、捲 (107)、桶 (108)、盒 (109)、組 (110)、箱 (111)、支 (112)、式 (113)、入 (114)、袋 (115)、顆 (116)、瓶 (117)、板 (201)、件 (202)、車 (203)、次 (204) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| weight | FLOAT | Yes |  |  | 內含物重量；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| expectedLoss | FLOAT | Yes |  |  | 預期損耗 |  | OK | Description, FK, enum, or index context is now sufficient to identify field purpose. |
| actualLoss | FLOAT | Yes |  |  | 實際損耗 |  | OK | Description, FK, enum, or index context is now sufficient to identify field purpose. |



## product_ver


<summary>product_ver (製成品歷史版本)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| no | VARCHAR(60) | No | UK(uq_product_ver_composite) |  | 編號；UNIQUE KEY；varchar(60) / 組裝編號；UNIQUE KEY；varchar(60)；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_no | VARCHAR(60) | No | UK(uq_product_ver_composite) | product_ver.item_no -> product.no | 製成品資料編號；UNIQUE KEY；varchar(60)，關連至product 資料表； |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| version | INT | No | UK(uq_product_ver_composite) |  | 版本號；int；UNIQUE KEY |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| date | INT | Yes |  |  | 生效日；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## production_data


<summary>production_data (生產數據)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creator_no | VARCHAR(60) | Yes |  | production_data.creator_no -> employee.no | 製單人員no，關連至employee資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| work_order_no | VARCHAR(60) | No | UK(uq_production_data_composite) | production_data.work_order_no -> work_order.no | 派工單no，關連至work_order資料表；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| product_order_no | VARCHAR(60) | Yes |  | production_data.product_order_no -> product_order.no | 銷售訂單編號，關連至product_order資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| customer_no | VARCHAR(60) | Yes |  | production_data.customer_no -> company.no | 客戶no，關連至company資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| customer_displayName | VARCHAR(60) | Yes |  |  | 客戶公司簡稱，關連至company資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| product_no | VARCHAR(60) | Yes |  | production_data.product_no -> product.no | 交易品項no，關連至product資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| product_name | VARCHAR(60) | Yes |  |  | 交易品項名稱，關連至product 資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| date | INT | Yes |  |  | 製造日期；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| production_line_no | VARCHAR(60) | Yes |  | production_data.production_line_no -> production_line.no | 產線no，關連至production_line資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| oneProcess | INT | Yes |  |  | 主製程；int數值如下其中之一 前備 (1)、加工 (2)、包裝 (3) | 前備 (1)、加工 (2)、包裝 (3) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| secProcess | INT | Yes |  |  | 次製程；int前備；數值如下其中之一調拌 (1)、塞料 (2)、烘烤(3)、灌料(4) 、其他 (0)加工；數值如下其中之一披覆 (1)、封膜 (2) 、其他 (0)包裝；數值如下其中之一成組 (1)、入箱 (2) 、其他 (0) | 調拌 (1)、塞料 (2)、烘烤(3)、灌料(4) 、其他 (0)加工；數值如下披覆 (1)、封膜 (2) 、其他 (0)包裝；數值如下成組 (1)、入箱 (2) 、其他 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_no | VARCHAR(255) | Yes |  |  | 產出的料品品項no，關連至 inproduct / product資料表 |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_name | VARCHAR(60) | Yes |  |  | 產出的料品品項名稱，關連至 inproduct / product資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| materialLoss | FLOAT | Yes |  |  | 損耗 (產出物重量-投入物重量-餘料重量-廢料重量；小數點2位) ；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## production_data_input


<summary>production_data_input (投入物數據)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| work_order_no | VARCHAR(60) | No | UK(uq_production_data_input_composite) | production_data_input.work_order_no -> work_order.no | 派工單no，關連至work_order資料表；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| process_order_no | VARCHAR(60) | Yes |  | production_data_input.process_order_no -> process_order.no | 餘廢退產單no，關連至process_order資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| group | VARCHAR(60) | No | UK(uq_production_data_input_composite) |  | 批號群組編號, 用於將同一批號產出物之投入物群組化 |  | OK | Description, FK, enum, or index context is now sufficient to identify field purpose. |
| time | INT | Yes |  |  | 日期；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| action | INT | No | UK(uq_production_data_input_composite) |  | 狀態；UNIQUE KEY；int數值如下其中之一領料(1)、退料(2)、其他(0) | 領料(1)、退料(2)、其他(0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_no | VARCHAR(60) | No | UK(uq_production_data_input_composite) |  | 投入的料品品項no，關連至 material/ product資料表；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_name | VARCHAR(60) | Yes |  |  | 投入的料品品項名稱，關連至 material/ product資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| category | INT | Yes |  |  | 料品品項類型；int數值如下其中之一原料 (1)、物料(2) 、膠捲(3) 、在製品(4)、其他(0) | 原料 (1)、物料(2) 、膠捲(3) 、在製品(4)、其他(0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| itemSubCategory | INT | Yes |  |  | 料品品項子類型；int數值如下其中之一：1. 料品品項類別為原料/物料/膠捲參照material的「subCategory」定義2. 料品品項類別為在製品/製成品參照inproduct/product的「category」定義3. 料品品項類別為貨品 參照goods的「subCategory」定義 | 料品品項類別為<br>1.原料/物料/膠捲:參照material的「subCategory」定義<br>2. 在製品/製成品:參照inproduct/product的「category」定義<br>3. 貨品:參照goods的「subCategory」定義 | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| batch_number | VARCHAR(60) | No | UK(uq_production_data_input_composite) |  | 投入的料品品項批號；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| serial_no | VARCHAR(60) | No | UK(uq_production_data_input_composite) |  | 投入的料品品項序號；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| unit | INT | Yes |  |  | 投入的料品品項單位；int數值如下其中之一： 公斤、公尺、個 、其他 參照「Unit單位定義」 | 其他 (0)、公克 (1)、公斤 (2)、台斤 (3)、公分 (51)、公尺 (52)、個 (101)、條 (102)、片 (103)、張 (104)、罐 (105)、包 (106)、捲 (107)、桶 (108)、盒 (109)、組 (110)、箱 (111)、支 (112)、式 (113)、入 (114)、袋 (115)、顆 (116)、瓶 (117)、板 (201)、件 (202)、車 (203)、次 (204) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| count | FLOAT | Yes |  |  | 領退料重量、長度、數量(小數點2位) ；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| comment | VARCHAR(128) | Yes |  |  | 備註；varchar(128) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## production_data_labor


<summary>production_data_labor (人員數據)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| work_order_no | VARCHAR(60) | No | UK(uq_production_data_labor_composite) | production_data_labor.work_order_no -> work_order.no | 派工單no，關連至work_order資料表；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| employee_no | VARCHAR(60) | No | UK(uq_production_data_labor_composite) | production_data_labor.employee_no -> employee.no | 員工no，關連至employee資料表；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| employee_name | VARCHAR(60) | Yes |  |  | 員工名稱，關連至employee資料表； varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| employee_type | INT | Yes |  |  | 型態；int數值如下其中之一 正職 (1)、兼職 (2) | 正職 (1)、兼職 (2) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| employee_jobTitle | INT | Yes |  |  | 職稱；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| employee_level | INT | Yes |  |  | 階級；int數值如下其中之一1: 主管2: | 主管2: | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| station_no | VARCHAR(60) | Yes |  | production_data_labor.station_no -> station.no | 站點 no，關連至station資料表； varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| stationStage | INT | No | UK(uq_production_data_labor_composite) |  | 製程階段；UNIQUE KEY；int數值如下其中之一 前段 (1)、後段 (2) | 前段 (1)、後段 (2) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| action | INT | No | UK(uq_production_data_labor_composite) |  | 作為；UNIQUE KEY；int數值如下其中之一： 上下班 (1) 、休息(2)、清潔 (3) | 上下班 (1) 、休息(2)、清潔 (3) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| startTime | INT | No | UK(uq_production_data_labor_composite) |  | 開始時間；UNIQUE KEY；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| endTime | INT | No | UK(uq_production_data_labor_composite) |  | 結束時間；UNIQUE KEY；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| hours | FLOAT | Yes |  |  | 總時數(小數點2位) ；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## production_data_machine


<summary>production_data_machine (機具數據)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| work_order_no | VARCHAR(60) | No | UK(uq_production_data_machine_composite) | production_data_machine.work_order_no -> work_order.no | 派工單no，關連至work_order資料表；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| equipment_no | VARCHAR(60) | No | UK(uq_production_data_machine_composite) | production_data_machine.equipment_no -> equipment.no | 機具no，關連至equipment資料表；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| equipment_name | VARCHAR(60) | Yes |  |  | 機具名稱，關連至equipment資料表； varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| time | INT | Yes |  |  | 日期；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| action | INT | No | UK(uq_production_data_machine_composite) |  | 機具狀態；UNIQUE KEY；int數值如下其中之一： 啟動 (1) 、暫停(2)、停止 (3) | 啟動 (1) 、暫停(2)、停止 (3) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| speed | FLOAT | Yes |  |  | 速度；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| temperature | FLOAT | Yes |  |  | 溫度；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## production_data_output


<summary>production_data_output (產出物數據)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| work_order_no | VARCHAR(60) | No | UK(uq_production_data_output_composite) | production_data_output.work_order_no -> work_order.no | 派工單no，關連至work_order資料表；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| process_order_no | VARCHAR(60) | Yes |  | production_data_output.process_order_no -> process_order.no | 餘廢退產單no，關連至process_order資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| group | VARCHAR(60) | No | UK(uq_production_data_output_composite) |  | 批號群組編號, 用於將同一批號之產出物群組化； |  | OK | Description, FK, enum, or index context is now sufficient to identify field purpose. |
| time | INT | Yes |  |  | 日期；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| action | INT | No | UK(uq_production_data_output_composite) |  | 狀態；UNIQUE KEY；int數值如下其中之一產製(1)、其他(0) | 產製(1)、其他(0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_no | VARCHAR(60) | No | UK(uq_production_data_output_composite) |  | 產出的料品品項no，關連至 inproduct / product資料表；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_name | VARCHAR(60) | Yes |  |  | 產出的料品品項名稱，關連至 inproduct / product資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| category | INT | Yes |  |  | 類型；int數值如下其中之一在製品(1)、製成品 (2)、其他(0) | 在製品(1)、製成品 (2)、其他(0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| itemSubCategory | INT | Yes |  |  | 品項子類別子類型；int數值如下其中之一：1. 料品品項類別為原料/物料/膠捲參照material的「subCategory」定義2. 料品品項類別為在製品/製成品參照inproduct/product的「category」定義3. 料品品項類別為貨品 參照goods的「subCategory」定義 | 料品品項類別為<br>1.原料/物料/膠捲:參照material的「subCategory」定義<br>2. 在製品/製成品:參照inproduct/product的「category」定義<br>3. 貨品:參照goods的「subCategory」定義 | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| batch_number | VARCHAR(60) | No | UK(uq_production_data_output_composite) |  | 產出的料品品項批號；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| serial_no | VARCHAR(60) | No | UK(uq_production_data_output_composite) |  | 產出的料品品項序號；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| valid_date | INT | Yes |  |  | 有效期限；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| valid_date_no | VARCHAR(60) | No |  |  | 有效期限編號； |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| unit | INT | Yes |  |  | 產出的料品品項單位；int數值如下其中之一： 公斤 、其他 參照「Unit單位定義」 | 其他 (0)、公克 (1)、公斤 (2)、台斤 (3)、公分 (51)、公尺 (52)、個 (101)、條 (102)、片 (103)、張 (104)、罐 (105)、包 (106)、捲 (107)、桶 (108)、盒 (109)、組 (110)、箱 (111)、支 (112)、式 (113)、入 (114)、袋 (115)、顆 (116)、瓶 (117)、板 (201)、件 (202)、車 (203)、次 (204) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| count | FLOAT | Yes |  |  | 產出的重量 (小數點2位) ；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| comment | VARCHAR(128) | Yes |  |  | 備註；varchar(128) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## production_data_reuse


<summary>production_data_reuse (餘廢料數據)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| work_order_no | VARCHAR(60) | No | UK(uq_production_data_reuse_composite) | production_data_reuse.work_order_no -> work_order.no | 派工單no，關連至work_order資料表；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| process_order_no | VARCHAR(60) | Yes |  | production_data_reuse.process_order_no -> process_order.no | 餘廢退產單no，關連至process_order資料表；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| group | VARCHAR(60) | No | UK(uq_production_data_reuse_composite) |  | 批號群組編號, 用於將同一批號產出物之餘廢料群組化 |  | OK | Description, FK, enum, or index context is now sufficient to identify field purpose. |
| time | INT | Yes |  |  | 日期；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| action | INT | No | UK(uq_production_data_reuse_composite) |  | 型態；UNIQUE KEY；int數值如下其中之一：產製 (1)、其他 (0) | 產製 (1)、其他 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_no | VARCHAR(60) | No | UK(uq_production_data_reuse_composite) | production_data_reuse.item_no -> inproduct.no | 餘廢料品項no，關連至 inproduct資料表；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_name | VARCHAR(60) | Yes |  |  | 餘廢料品項名稱，關連至 inproduct資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| category | INT | No | UK(uq_production_data_reuse_composite) |  | 餘廢料品項類型；UNIQUE KEY；int數值如下其中之一餘料(1)、廢料 (2)、其他(0) | 餘料(1)、廢料 (2)、其他(0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| itemSubCategory | INT | Yes |  |  | 餘廢料品項子類型；int數值如下其中之一：餅體 (1)、拌料 (2)、餡料 (3)、巧克力 (4)、膠捲(5)、在製品(6)、鐵桶罐 (7) 、製成品 (8)、其他 (0) | 餅體 (1)、拌料 (2)、餡料 (3)、巧克力 (4)、膠捲(5)、在製品(6)、鐵桶罐 (7) 、製成品 (8)、其他 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| batch_number | VARCHAR(60) | No | UK(uq_production_data_reuse_composite) |  | 餘廢料品品項批號；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| serial_no | VARCHAR(60) | No | UK(uq_production_data_reuse_composite) |  | 餘廢料品品項序號；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| unit | INT | Yes |  |  | 餘廢料品品項單位；int數值如下其中之一： 公斤、其他 參照「Unit單位定義」 | 其他 (0)、公克 (1)、公斤 (2)、台斤 (3)、公分 (51)、公尺 (52)、個 (101)、條 (102)、片 (103)、張 (104)、罐 (105)、包 (106)、捲 (107)、桶 (108)、盒 (109)、組 (110)、箱 (111)、支 (112)、式 (113)、入 (114)、袋 (115)、顆 (116)、瓶 (117)、板 (201)、件 (202)、車 (203)、次 (204) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| count | FLOAT | Yes |  |  | 產出的重量 (小數點2位) ；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| comment | VARCHAR(128) | Yes |  |  | 備註；varchar(128) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## production_line


<summary>production_line (產線)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| no | VARCHAR(60) | No | UK(uq_production_line_composite) |  | 編號；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| name | VARCHAR(60) | Yes |  |  | 簡稱；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| process_no | VARCHAR(60) | Yes |  | production_line.process_no -> process.no | 製程no，關連至process資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| oneProcess | INT | Yes |  |  | 主製程；int數值如下其中之一 前備 (1)、加工 (2)、包裝 (3) 、其他 (0) | 前備 (1)、加工 (2)、包裝 (3) 、其他 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| secProcess | INT | Yes |  |  | 次製程；int前備；數值如下其中之一調拌 (1)、塞料 (2)、烘烤(3)、灌料(4) 、其他 (0)加工；數值如下其中之一披覆 (1)、封膜 (2) 、其他 (0)包裝；數值如下其中之一成組 (1)、入箱 (2) 、其他 (0) | 調拌 (1)、塞料 (2)、烘烤(3)、灌料(4) 、其他 (0)加工；數值如下披覆 (1)、封膜 (2) 、其他 (0)包裝；數值如下成組 (1)、入箱 (2) 、其他 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| factory_no | VARCHAR(60) | Yes |  | production_line.factory_no -> factory.no | 廠區no，關連至factory 資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| location | VARCHAR(60) | Yes |  |  | 所在位置；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| capacityUnit | INT | Yes |  |  | 產線效能單位；int數值如下其中之一公斤 (1)、外觀規格 – ”箱”的單位(2) 、外觀規格 – ”組”的單位 (3)、外觀規格 – ”入”的單位 (4) 、外觀規格 – ”式”的單位 (5) | 公斤 (1)、外觀規格 – ”箱”的單位(2) 、外觀規格 – ”組”的單位 (3)、外觀規格 – ”入”的單位 (4) 、外觀規格 – ”式”的單位 (5) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| capacity | FLOAT | Yes |  |  | 時產量 / 每小時最大產能 (小數點2位) ；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| laborCount | INT | Yes |  |  | 人員數 / 人力數量；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| laborEfficiency | FLOAT | Yes |  |  | 每小時每人可完成的工作量 (小數點2位) ；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| comment | VARCHAR(128) | Yes |  |  | 說明；varchar(128) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## production_line_daily_capacity

<summary>production_line_daily_capacity (產線每日可排工時設定)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；流水識別碼。 |  | OK | Engineer-confirmed Production Dashboard extension. |
| no | VARCHAR(60) | No | UK(uq_production_line_daily_capacity_no) |  | 每日可排工時設定編號。 |  | OK | Engineer-confirmed Production Dashboard extension. |
| effectiveDate | INT | No | UK(uq_production_line_daily_capacity_effective_line), IDX |  | 設定生效日；自此日期起套用至該產線，查詢歷史日期不可套用尚未生效的設定。 | UTC timestamp | OK | Engineer-confirmed V5 effective-date version rule. |
| production_line_no | VARCHAR(60) | No | UK(uq_production_line_daily_capacity_effective_line), IDX | production_line_daily_capacity.production_line_no -> production_line.no | 產線 no。 |  | OK | Engineer-confirmed V5 effective-date version rule. |
| availableMinutes | INT | No |  |  | 自生效日起的原始可排工時分鐘數；不含不可排休息、故障停用或維修時間。 |  | OK | Engineer-confirmed Production Dashboard extension. |
| status | INT | No | IDX |  | 設定狀態。 | 啟用(1)、停用(2)、休線(3) | OK | Engineer-confirmed Production Dashboard extension. |
| comment | TEXT | Yes |  |  | 設定備註。 |  | OK | Engineer-confirmed Production Dashboard extension. |
| creator_no | VARCHAR(60) | Yes |  |  | 建立人員 no。 |  | OK | Engineer-confirmed Production Dashboard extension. |
| creationTime | INT | No |  |  | 資料建立時間。 | UTC timestamp | OK | Engineer-confirmed Production Dashboard extension. |
| lastUpdateTime | INT | Yes |  |  | 最後更新時間。 | UTC timestamp | OK | Engineer-confirmed Production Dashboard extension. |



## production_line_downtime

<summary>production_line_downtime (產線故障停用紀錄)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；流水識別碼。 |  | OK | Engineer-confirmed Production Dashboard extension. |
| no | VARCHAR(60) | No | UK(uq_production_line_downtime_no) |  | 產線停用紀錄編號。 |  | OK | Engineer-confirmed Production Dashboard extension. |
| production_line_no | VARCHAR(60) | No | IDX(idx_production_line_downtime_line_time) | production_line_downtime.production_line_no -> production_line.no | 產線 no。 |  | OK | Engineer-confirmed V4/V5 separation rule. |
| startTime | INT | No | IDX(idx_production_line_downtime_line_time) |  | 停用開始時間。 | UTC timestamp | OK | Engineer-confirmed Production Dashboard extension. |
| endTime | INT | No | IDX(idx_production_line_downtime_line_time) |  | 停用結束時間。 | UTC timestamp | OK | Engineer-confirmed Production Dashboard extension. |
| durationMinutes | INT | No |  |  | 經確認的停用分鐘數；跨日查詢時依日期交集切割。 |  | OK | Engineer-confirmed V4/V5 calculation rule. |
| reasonType | INT | No | IDX |  | 停用原因。 | 故障(1)、維修(2)、臨時停用(3)、其他(4) | OK | Engineer-confirmed Production Dashboard extension. |
| status | INT | No | IDX(idx_production_line_downtime_status) |  | 停用紀錄狀態；只有已確認資料納入產能扣減。 | 待確認(1)、已確認(2)、已取消(3) | OK | Engineer-confirmed V4/V5 calculation rule. |
| comment | TEXT | Yes |  |  | 停用原因或主管確認備註。 |  | OK | Engineer-confirmed Production Dashboard extension. |
| creator_no | VARCHAR(60) | Yes |  |  | 建立人員 no。 |  | OK | Engineer-confirmed Production Dashboard extension. |
| creationTime | INT | No |  |  | 資料建立時間。 | UTC timestamp | OK | Engineer-confirmed Production Dashboard extension. |
| lastUpdateTime | INT | Yes |  |  | 最後更新時間。 | UTC timestamp | OK | Engineer-confirmed Production Dashboard extension. |



## purchase_order


<summary>purchase_order (採購單)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| no | VARCHAR(60) | No | UK(uq_purchase_order_composite) |  | 編號；UNIQUE KEY；varchar(20) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creator_no | VARCHAR(60) | Yes |  | purchase_order.creator_no -> employee.no | 製單人員no，關連至employee資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| purchase_request_no | VARCHAR(60) | Yes |  | purchase_order.purchase_request_no -> purchase_request.no | 請購單no，關連至purchase_request資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| date | INT | Yes |  |  | 採購日期；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| ref_no | VARCHAR(60) | Yes |  | purchase_order.ref_no -> contract.no | 合約no，關連至contract資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_ref_no | VARCHAR(60) | Yes |  | purchase_order.item_ref_no -> company.no | 客戶/廠商no，關連至company資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_ref_displayName | VARCHAR(60) | Yes |  |  | 客戶/廠商公司簡稱，關連至company資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_no | VARCHAR(60) | Yes |  | purchase_order.item_no -> trans_items.no | 交易品項no，關連至trans_items資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_name | VARCHAR(60) | Yes |  |  | 交易品項名稱，關連至trans_items資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| unit | INT | Yes |  |  | 採購單位；int | 其他 (0)、公克 (1)、公斤 (2)、台斤 (3)、公分 (51)、公尺 (52)、個 (101)、條 (102)、片 (103)、張 (104)、罐 (105)、包 (106)、捲 (107)、桶 (108)、盒 (109)、組 (110)、箱 (111)、支 (112)、式 (113)、入 (114)、袋 (115)、顆 (116)、瓶 (117)、板 (201)、件 (202)、車 (203)、次 (204) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| price | DOUBLE | Yes |  |  | 採購單位價格 (含稅價，小數點4位) ；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| count | FLOAT | Yes |  |  | 數量 (小數點2位)；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| amount | INT | Yes |  |  | 總金額 (含稅價，小數點4位) ；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| expectedDate | INT | Yes |  |  | 預計進貨日期；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| address | VARCHAR(100) | Yes |  |  | 進貨地址；varchar(100) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| payment_type | INT | Yes |  |  | 收付款類別；int數值如下其中之一：現結 (0)、月結 (1) | 現結 (0)、月結 (1) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| payment_source | INT | Yes |  |  | 收付款方式；int數值如下其中之一：現金 (0)、匯款 (1)、支票 (2) | 現金 (0)、匯款 (1)、支票 (2) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| payment_date | INT | Yes |  |  | 結帳款日；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| payment_period | INT | Yes |  |  | 收付款期；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| comment | VARCHAR(128) | Yes |  |  | 備註；varchar(128) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## purchase_request


<summary>purchase_request (請購單)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK>； |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| no | VARCHAR(60) | No | UK(uq_purchase_request_composite) |  | 編號；UNIQUE KEY；varchar(20) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creator_no | VARCHAR(60) | Yes |  | purchase_request.creator_no -> employee.no | 製單人員no，關連至employee資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| product_order_no | VARCHAR(60) | Yes | UK(uq_purchase_request_composite) | purchase_request.product_order_no -> product_order.no | 訂購單no，關連至product_order資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| date | INT | Yes |  |  | 請購日期；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_no | VARCHAR(60) | Yes | UK(uq_purchase_request_composite) | purchase_request.item_no -> material.no | 料品品項編號 |  | OK | SQL FK defines relation to material.no. |
| unit | INT | Yes |  |  | 料品品項單位 | 其他 (0)、公克 (1)、公斤 (2)、台斤 (3)、公分 (51)、公尺 (52)、個 (101)、條 (102)、片 (103)、張 (104)、罐 (105)、包 (106)、捲 (107)、桶 (108)、盒 (109)、組 (110)、箱 (111)、支 (112)、式 (113)、入 (114)、袋 (115)、顆 (116)、瓶 (117)、板 (201)、件 (202)、車 (203)、次 (204) | OK | Description, FK, enum, or index context is now sufficient to identify field purpose. |
| count | FLOAT | Yes |  |  | 請購數量 |  | OK | Description, FK, enum, or index context is now sufficient to identify field purpose. |
| expectedDate | INT | Yes |  |  | 預期到貨日期 |  | OK | Description, FK, enum, or index context is now sufficient to identify field purpose. |
| comment | VARCHAR(128) | Yes |  |  | 備註；varchar(128) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## quotation


<summary>quotation (報價單)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| no | VARCHAR(60) | No | UK(uq_quotation_composite) |  | 編號；UNIQUE KEY；varchar(20) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creator_no | VARCHAR(60) | Yes |  | quotation.creator_no -> employee.no | 製單人員no，關連至employee資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| date | INT | Yes |  |  | 報價日期；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| category | INT | Yes |  |  | 議價類別；int數值如下其中之一：採購 (1)、訂購 (2) | 採購 (1)、訂購 (2) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| type | INT | Yes |  |  | 合約樣式；int 數值如下其中之一：1.合約類別為採購採購 (1)、客供 (2)、採買 (3)、購置/保修 (4)2.合約類別為訂購產製 (1)、進銷 (2) | 1.合約類別為採購採購 (1)、客供 (2)、採買 (3)、購置/保修 (4)2.合約類別為訂購產製 (1)、進銷 (2) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| itemStyle | INT | Yes |  |  | 品項樣式；int 數值如下其中之一：貨品 (1) 、 產品 (2) 、材料 (3)、耗品(4) 、設備(5) | 貨品 (1) 、 產品 (2) 、材料 (3)、耗品(4) 、設備(5) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_no | VARCHAR(255) | Yes |  |  | 交易品項no，關連至trans_items / trans_items2 資料表 |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_name | VARCHAR(255) | Yes |  |  | 交易品項名稱，關連至trans_items / trans_items2資料表 |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_ref_no | VARCHAR(60) | Yes |  | quotation.item_ref_no -> company.no | 客戶/廠商no，關連至company資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_ref_displayName | VARCHAR(60) | Yes |  |  | 客戶/廠商公司簡稱，關連至company資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| unit | INT | Yes |  |  | 報價單位；int類型為「散裝品」，以外觀規格 – ”箱”的單位類型為「組裝品」，以外觀規格 – ”組”的單位 | 其他 (0)、公克 (1)、公斤 (2)、台斤 (3)、公分 (51)、公尺 (52)、個 (101)、條 (102)、片 (103)、張 (104)、罐 (105)、包 (106)、捲 (107)、桶 (108)、盒 (109)、組 (110)、箱 (111)、支 (112)、式 (113)、入 (114)、袋 (115)、顆 (116)、瓶 (117)、板 (201)、件 (202)、車 (203)、次 (204) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| price | DOUBLE | Yes |  |  | 報價單位價格 (含稅價，小數點4位)； |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| unitConversion | FLOAT | Yes |  |  | 規格轉換；交易品項交易單位料品品項盤點單位 | 其他 (0)、公克 (1)、公斤 (2)、台斤 (3)、公分 (51)、公尺 (52)、個 (101)、條 (102)、片 (103)、張 (104)、罐 (105)、包 (106)、捲 (107)、桶 (108)、盒 (109)、組 (110)、箱 (111)、支 (112)、式 (113)、入 (114)、袋 (115)、顆 (116)、瓶 (117)、板 (201)、件 (202)、車 (203)、次 (204) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| comment | VARCHAR(128) | Yes |  |  | 備註；varchar(128) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## rw_items


<summary>rw_items (餘廢料料品品項)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT primary identifier. |  | OK | AUTO_INCREMENT primary identifier. |
| item_no | varchar(60) | No | UK(uq_rw_items_composite) | rw_items.item_no -> inproduct.no | 餘廢料料品品項 |  | OK | Description, FK, enum, or index context is now sufficient to identify field purpose. |



## sample_price


<summary>sample_price (樣品品項價格)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_no | VARCHAR(60) | No | UK(uq_sample_price_composite) | sample_price.item_no -> bom.no | 商品配方no，關連至bom資料表；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| date | DATE | No | UK(uq_sample_price_composite) |  | 生效日；UNIQUE KEY；Date |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| estWHUnitWeight | INT | Yes |  |  | 預估盤點重量單位(庫存盤點採用的單位) ；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| estWHPriceWeight | DOUBLE | Yes |  |  | 預估盤點重量單位價格 (含稅價，小數點4位) ；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| estCostUnitWeight | INT | Yes |  |  | 預估成本重量單位(BOM計算的單位) ；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| estCostPriceWeight | DOUBLE | Yes |  |  | 預估成本重量單位價格 (含稅價，小數點4位) ；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| estLaborCost | DOUBLE | Yes |  |  | 預估人工費；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| whUnitWeight | INT | Yes |  |  | 盤點重量單位(庫存盤點採用的單位) ；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| whPriceWeight | DOUBLE | Yes |  |  | 盤點重量單位價格 (含稅價，小數點4位) ；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| costUnitWeight | INT | Yes |  |  | 成本重量單位(BOM計算的單位) ；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| costPriceWeight | DOUBLE | Yes |  |  | 成本重量單位價格 (含稅價，小數點4位) ；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| laborCost | DOUBLE | Yes |  |  | 人工費；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| comment | VARCHAR(128) | Yes |  |  | 備註；varchar(128) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## session


<summary>session (連線交談)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| user_no | VARCHAR(60) | Yes |  | session.user_no -> employee.no | 員工no，關連至employee資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| token | VARCHAR(60) | Yes |  |  | 存取金鑰；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| expiredTime | INT | Yes |  |  | 過期時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## ship_wh


<summary>ship_wh (交易品項-物流倉儲)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| no | VARCHAR(60) | No | UK(uq_ship_wh_composite) |  | 編號；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| company_no | VARCHAR(60) | Yes |  | ship_wh.company_no -> company.no | 廠商資料no，關連至company資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| company_displayName | VARCHAR(60) | Yes |  |  | 廠商公司簡稱，關連至company資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| name | VARCHAR(60) | Yes |  |  | 簡稱；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| category | INT | Yes |  |  | 樣式；int數值如下其中之一： 物流 (1)、倉儲 (2) 、其他 (0) | 物流 (1)、倉儲 (2) 、其他 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| attribute | INT | Yes |  |  | 屬性；int數值如下其中之一： 常溫 (1)、冷藏 (2)、冷凍 (3) 、其他 (0) | 常溫 (1)、冷藏 (2)、冷凍 (3) 、其他 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| unit | INT | Yes |  |  | 儲放/運輸單位；int數值如下其中之一： 板 (1)、車 (2)、其他 (0) | 其他 (0)、公克 (1)、公斤 (2)、台斤 (3)、公分 (51)、公尺 (52)、個 (101)、條 (102)、片 (103)、張 (104)、罐 (105)、包 (106)、捲 (107)、桶 (108)、盒 (109)、組 (110)、箱 (111)、支 (112)、式 (113)、入 (114)、袋 (115)、顆 (116)、瓶 (117)、板 (201)、件 (202)、車 (203)、次 (204) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| maxCapacity | INT | Yes |  |  | 最大儲放/運輸量；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| comment | VARCHAR(128) | Yes |  |  | 備註；varchar(128)；varchar(128) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## ship_wh_alias


<summary>ship_wh_alias (物流倉儲別名)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| no | VARCHAR(60) | No | UK(uq_ship_wh_alias_composite) |  | 編號；UNIQUE KEY；varchar(20) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| name | VARCHAR(60) | Yes |  |  | 物流倉儲別名；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| category | INT | Yes |  |  | 樣式；int數值如下其中之一： 物流 (1)、倉儲 (2) 、其他 (0) | 物流 (1)、倉儲 (2) 、其他 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| type | INT | Yes |  |  | 樣式；int數值如下其中之一： 自有 (1)、合約 (2) 、客供 (3) 、其他 (0) | 自有 (1)、合約 (2) 、客供 (3) 、其他 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## ship_wh_contract


<summary>ship_wh_contract (物流倉儲合約)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| no | VARCHAR(60) | No | UK(uq_ship_wh_contract_composite) |  | 編號；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| date | INT | No | UK(uq_ship_wh_contract_composite) |  | 生效日期；UNIQUE KEY；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| ref_no | VARCHAR(60) | Yes |  | ship_wh_contract.ref_no -> ship_wh_quotation.no | 物流倉儲議價no，關連至ship_wh_quotation資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| sw_alias_no | VARCHAR(60) | Yes |  | ship_wh_contract.sw_alias_no -> ship_wh_alias.no | 物流倉儲別名no，關連至ship_wh_alias資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| displayName | VARCHAR(60) | Yes |  |  | 簡稱；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_no | VARCHAR(60) | Yes |  | ship_wh_contract.item_no -> ship_wh.no | 物流倉儲資料no，關連至ship_wh資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_name | VARCHAR(60) | Yes |  |  | 物流倉儲資料displayName，關連至ship_wh資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_ref_no | VARCHAR(60) | Yes |  | ship_wh_contract.item_ref_no -> company.no | 客戶/廠商no，關連至company資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_ref_displayName | VARCHAR(60) | Yes |  |  | 客戶/廠商公司簡稱，關連至company資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| category | INT | Yes |  |  | 合約類別；int數值如下其中之一：物流 (1)、倉儲 (2) | 物流 (1)、倉儲 (2) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| type | INT | Yes |  |  | 合約樣式；int 數值如下其中之一：1.合約類別為物流宅配 (1)、專車 (2)、併車 (3) 、回頭車 (4) 、貨櫃 (5)2.合約類別為倉儲月租 (1)、日租 (2) 、時租 (3) | 合約類別為 <br>1.物流: 宅配 (1)、專車 (2)、併車 (3) 、回頭車 (4) 、貨櫃 (5) <br>2.倉儲: 月租 (1)、日租 (2) 、時租 (3) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| itemStyle | INT | Yes |  |  | 品項樣式；int數值如下其中之一：物流 (1)、倉儲 (2) | 物流 (1)、倉儲 (2) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| region | INT | Yes |  |  | 運送/儲放地點；int數值如下其中之一：台北 (1)、新北 (2)、桃園 (3)、台中 (4)、台南 (5)、 高雄 (6)、基隆 (7)、新竹 (8)、苗栗 (9)、彰化 (10)、南投 (11)、雲林 (12)、嘉義 (13)、屏東 (14)、 宜蘭 (15)、花蓮 (16)、台東 (17)、其他 (0) | 台北 (1)、新北 (2)、桃園 (3)、台中 (4)、台南 (5)、 高雄 (6)、基隆 (7)、新竹 (8)、苗栗 (9)、彰化 (10)、南投 (11)、雲林 (12)、嘉義 (13)、屏東 (14)、 宜蘭 (15)、花蓮 (16)、台東 (17)、其他 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| unit | INT | Yes |  |  | 計價單位；int數值如下其中之一：1.合約類別為物流 才、車 、箱、其他 參照「Unit單位定義」2.合約類別為倉儲 板、其他 參照「Unit單位定義」 | 其他 (0)、公克 (1)、公斤 (2)、台斤 (3)、公分 (51)、公尺 (52)、個 (101)、條 (102)、片 (103)、張 (104)、罐 (105)、包 (106)、捲 (107)、桶 (108)、盒 (109)、組 (110)、箱 (111)、支 (112)、式 (113)、入 (114)、袋 (115)、顆 (116)、瓶 (117)、板 (201)、件 (202)、車 (203)、次 (204) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| price | DOUBLE | Yes |  |  | 含稅價格 ；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| fee | DOUBLE | Yes |  |  | 作業費 / 次；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| comment | VARCHAR(128) | Yes |  |  | 備註；varchar(128) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## ship_wh_quotation


<summary>ship_wh_quotation (物流倉儲議價)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| no | VARCHAR(60) | No | UK(uq_ship_wh_quotation_composite) |  | 編號；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| date | INT | No | UK(uq_ship_wh_quotation_composite) |  | 議價日期；UNIQUE KEY；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_no | VARCHAR(60) | Yes |  | ship_wh_quotation.item_no -> ship_wh.no | 物流倉儲no，關連至ship_wh資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_name | VARCHAR(60) | Yes |  |  | 物流倉儲簡稱，關連至ship_wh資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_ref_no | VARCHAR(60) | Yes |  | ship_wh_quotation.item_ref_no -> company.no | 客戶/廠商no，關連至company資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_ref_displayName | VARCHAR(60) | Yes |  |  | 客戶/廠商公司簡稱，關連至company資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| category | INT | Yes |  |  | 合約類別；int 數值如下其中之一：物流 (1)、倉儲 (2) | 物流 (1)、倉儲 (2) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| type | INT | Yes |  |  | 合約樣式；int 數值如下其中之一：1.合約類別為物流宅配 (1)、專車 (2)、併車 (3) 、回頭車 (4) 、貨櫃 (5)2.合約類別為倉儲月租 (1)、日租 (2) 、時租 (3) | 1.合約類別為物流宅配 (1)、專車 (2)、併車 (3) 、回頭車 (4) 、貨櫃 (5)2.合約類別為倉儲月租 (1)、日租 (2) 、時租 (3) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| itemStyle | INT | Yes |  |  | 品項樣式；int 數值如下其中之一：物流 (1)、倉儲 (2) | 物流 (1)、倉儲 (2) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| region | INT | Yes |  |  | 運送/儲放地點；int數值如下其中之一：台北 (1)、新北 (2)、桃園 (3)、台中 (4)、台南 (5)、 高雄 (6)、基隆 (7)、新竹 (8)、苗栗 (9)、彰化 (10)、南投 (11)、雲林 (12)、嘉義 (13)、屏東 (14)、 宜蘭 (15)、花蓮 (16)、台東 (17)、其他 (0) | 台北 (1)、新北 (2)、桃園 (3)、台中 (4)、台南 (5)、 高雄 (6)、基隆 (7)、新竹 (8)、苗栗 (9)、彰化 (10)、南投 (11)、雲林 (12)、嘉義 (13)、屏東 (14)、 宜蘭 (15)、花蓮 (16)、台東 (17)、其他 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| unit | INT | Yes |  |  | 計價單位；int 數值如下其中之一：1.合約類別為物流 才、車 、箱、其他 參照「Unit單位定義」2.合約類別為倉儲 板、其他 參照「Unit單位定義」 | 其他 (0)、公克 (1)、公斤 (2)、台斤 (3)、公分 (51)、公尺 (52)、個 (101)、條 (102)、片 (103)、張 (104)、罐 (105)、包 (106)、捲 (107)、桶 (108)、盒 (109)、組 (110)、箱 (111)、支 (112)、式 (113)、入 (114)、袋 (115)、顆 (116)、瓶 (117)、板 (201)、件 (202)、車 (203)、次 (204) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| price | DOUBLE | Yes |  |  | 含稅價格 ；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| fee | FLOAT | Yes |  |  | 作業費 / 次；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| comment | VARCHAR(128) | Yes |  |  | 備註；varchar(128) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## shipping_order


<summary>shipping_order (銷貨單)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| no | VARCHAR(60) | No | UK(uq_shipping_order_composite) |  | 編號；UNIQUE KEY；varchar(20) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creator_no | VARCHAR(60) | Yes |  | shipping_order.creator_no -> employee.no | 製單人員no，關連至employee資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| product_order_no | VARCHAR(60) | Yes |  | shipping_order.product_order_no -> product_order.no | 訂購單no，關連至product_order資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| date | INT | Yes |  |  | 出貨日期；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| category | INT | Yes |  |  | 類別；int數值如下其中之一：銷貨單 (0)、銷貨退回 (1) | 銷貨單 (0)、銷貨退回 (1) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_ref_no | VARCHAR(60) | Yes |  | shipping_order.item_ref_no -> company.no | 客戶/廠商no，關連至company資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_ref_displayName | VARCHAR(60) | Yes |  |  | 客戶/廠商公司簡稱，關連至company資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_no | VARCHAR(60) | Yes |  | shipping_order.item_no -> trans_items.no | 交易品項no，關連至trans_items資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_name | VARCHAR(60) | Yes |  |  | 交易品項名稱，關連至trans_items資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| itemCategory | INT | Yes |  |  | 料品品項類別；int數值如下其中之一：原料 (1)、物料 (2)、膠捲 (3) 、在製品 (4) 、製成品 (5) 、貨品 (6) | 原料 (1)、物料 (2)、膠捲 (3) 、在製品 (4) 、製成品 (5) 、貨品 (6) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| itemSubCategory | INT | Yes |  |  | 料品品項子類別；int數值如下其中之一：料品品項類別為原料/物料/膠捲 參照material的「subCategory」定義2. 料品品項類別為在製品/製成品 參照inproduct/product的「category」定義3. 料品品項類別為貨品 參照goods的「subCategory」定義 | 料品品項類別為原料/物料/膠捲 參照material的「subCategory」定義2. 料品品項類別為在製品/製成品 參照inproduct/product的「category」定義3. 料品品項類別為貨品 參照goods的「subCategory」定義 | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| unit | INT | Yes |  |  | 銷售單位；int | 其他 (0)、公克 (1)、公斤 (2)、台斤 (3)、公分 (51)、公尺 (52)、個 (101)、條 (102)、片 (103)、張 (104)、罐 (105)、包 (106)、捲 (107)、桶 (108)、盒 (109)、組 (110)、箱 (111)、支 (112)、式 (113)、入 (114)、袋 (115)、顆 (116)、瓶 (117)、板 (201)、件 (202)、車 (203)、次 (204) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| price | DOUBLE | Yes |  |  | 銷售單位價格 (含稅價，小數點4位) ；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| expectedCount | FLOAT | Yes |  |  | 排定數量 (小數點2位) ；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| checkedCount | FLOAT | Yes |  |  | 實際數量 (小數點2位) ；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| feeCount | FLOAT | Yes |  |  | 計價數量 (小數點2位) ；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| amount | INT | Yes |  |  | 總金額 (含稅價，整數；無條件進位) ；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| addDeleteAmount | INT | Yes |  |  | 加扣金額 ；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| comment | VARCHAR(128) | Yes |  |  | 備註；varchar(128) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## shipping_payment


<summary>shipping_payment (物流帳款)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| no | VARCHAR(60) | No | UK(uq_shipping_payment_composite) |  | 帳款編號；UNIQUE KEY；varchar(60)每日一組ship_wh一組帳款編號 |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| group_no | VARCHAR(60) | Yes |  |  | 現結/月結帳款群組編號；varchar(60)現結的no與group_no相同；改成一個客戶每月一個帳款編號 |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| date | INT | No | UK(uq_shipping_payment_composite) |  | 日期；UNIQUE KEY；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| arapType | INT | Yes |  |  | 類型；數值如下其中之一 1: 應收帳款 2: 應付帳款 | 應收帳款(1)、 應付帳款(2) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| record_no | BIGINT UNSIGNED | Yes |  | shipping_payment.record_no -> shipping_record.id | 物流紀錄，關聯至shipping_record資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| refCategory | INT | Yes |  |  | 訂單類別；數值如下其中之一 採購(1)、訂購 (2)、其他 (0) | 採購(1)、訂購 (2)、其他 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| ref_no | VARCHAR(60) | Yes |  |  | 採購單 no/訂購單 no，關聯至product_order / purchase_order資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| ref_sub_no | VARCHAR(60) | Yes |  |  | 進貨單 no/ 銷貨單 no，關聯至goods_receipt_note / shipping_order資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_ref_no | VARCHAR(60) | Yes |  | shipping_payment.item_ref_no -> company.no | 客戶/廠商no，關連至company資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_ref_displayName | VARCHAR(60) | Yes |  |  | 客戶/廠商公司簡稱，關連至company資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| paymentType | INT | Yes |  |  | 物流付款類別；int數值如下其中之一：現結 (0)、月結 (1) | 現結 (0)、月結 (1) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| month | DATE | Yes |  |  | 帳款年月；DATE |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| price | DOUBLE | Yes |  |  | 單位價格 (含稅價，小數點4位) ；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| count | INT | Yes |  |  | 計價數量；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| amount | INT | Yes |  |  | 帳款金額 (含稅價) ；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| addDeleteAmount | INT | Yes |  |  | 加/扣款金額 (含稅價)；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| totalAmount | INT | Yes |  |  | 總金額 (加/扣款金額+帳款金額) ；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| balance | INT | Yes |  |  | 應收應付餘額 |  | OK | Description, FK, enum, or index context is now sufficient to identify field purpose. |
| creationTime | INT | Yes |  |  | 資料建立時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## shipping_record


<summary>shipping_record (運輸班次)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| date | INT | Yes |  |  | 日期；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| refCategory | INT | Yes |  |  | 訂單類別；int數值如下其中之一 採購(1)、訂購 (2) 、其他 (0) | 採購(1)、訂購 (2) 、其他 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| ref_no | VARCHAR(60) | Yes |  |  | 進貨單 no/ 銷貨單 no，關聯至goods_receipt_note / shipping_order資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| ref_parent_no | VARCHAR(60) | Yes |  |  | 採購單 no/訂購單 no，關聯至product_order / purchase_order資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| contract_no | VARCHAR(60) | Yes |  | shipping_record.contract_no -> ship_wh_contract.no | 物流合約no，關連至ship_wh_contract資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| sw_alias_no | VARCHAR(60) | Yes |  | shipping_record.sw_alias_no -> ship_wh_alias.no | 物流別名no，關連至ship_wh_alias資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| sw_alias_name | VARCHAR(60) | Yes |  |  | 物流別名名稱，關連至ship_wh_alias資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_no | VARCHAR(60) | Yes |  | shipping_record.item_no -> ship_wh.no | 物流no (交易品項)，關連至ship_wh資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_name | VARCHAR(60) | Yes |  |  | 物流名稱 (交易品項)，關連至ship_wh資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_ref_no | VARCHAR(60) | Yes |  | shipping_record.item_ref_no -> company.no | 客戶/廠商no，關連至company資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_ref_displayName | VARCHAR(60) | Yes |  |  | 客戶/廠商公司簡稱，關連至company資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| unit | INT | Yes |  |  | 交易單位；int | 其他 (0)、公克 (1)、公斤 (2)、台斤 (3)、公分 (51)、公尺 (52)、個 (101)、條 (102)、片 (103)、張 (104)、罐 (105)、包 (106)、捲 (107)、桶 (108)、盒 (109)、組 (110)、箱 (111)、支 (112)、式 (113)、入 (114)、袋 (115)、顆 (116)、瓶 (117)、板 (201)、件 (202)、車 (203)、次 (204) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| price | DOUBLE | Yes |  |  | 單價；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| count | INT | Yes |  |  | 物流交易單位排定數量(無條件進位) ；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| checkedCount | INT | Yes |  |  | 物流交易單位實際數量(無條件進位) ；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| comment | VARCHAR(128) | Yes |  |  | 地點；varchar(128) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## station


<summary>station (站點)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| no | VARCHAR(60) | No | UK(uq_station_composite) |  | 編號；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| production_line_no | VARCHAR(60) | Yes |  | station.production_line_no -> production_line.no |  |  | OK | SQL FK defines relation to production_line.no. |
| name | VARCHAR(60) | Yes |  |  | 名稱；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| stage | INT | Yes |  |  | 製程階段；int數值如下其中之一 前段 (1)、後段 (2) | 前段 (1)、後段 (2) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| comment | VARCHAR(128) | Yes |  |  | 說明；varchar(128) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## trans_items


<summary>trans_items (交易品項-貨品/材料/產品)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| no | VARCHAR(60) | No | UK(uq_trans_items_composite) |  | 編號；UNIQUE KEY；varchar(20) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| name | VARCHAR(100) | Yes |  |  | 品項名稱；varchar(100) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| category | INT | Yes |  |  | 樣式；int數值如下其中之一： 貨品 (1)、材料 (2)、產品 (3) 、其他 (0) | 貨品 (1)、材料 (2)、產品 (3) 、其他 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| attribute | INT | Yes |  |  | 屬性；int數值如下其中之一： 其他 (0) | 其他 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| company_no | VARCHAR(60) | Yes |  | trans_items.company_no -> company.no | 客戶資料no，關連至company資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| company_displayName | VARCHAR(60) | Yes |  |  | 客戶公司簡稱，關連至company資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_no | VARCHAR(60) | Yes |  |  | 料品品項no，關連至material/inproduct/product資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_name | VARCHAR(60) | Yes |  |  | 料品品項名稱，關連至material/inproduct/product資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| comment | VARCHAR(128) | Yes |  |  | 備註；varchar(128)；varchar(128) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## trans_items2


<summary>trans_items2 (交易品項-耗品/設備/工程/其他)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| no | VARCHAR(60) | No | UK(uq_trans_items2_composite) |  | 編號；UNIQUE KEY；varchar(20) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| name | VARCHAR(100) | Yes |  |  | 品項名稱；varchar(100) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| category | INT | Yes |  |  | 樣式；int數值如下其中之一： 耗品 (1) 、設備 (2) 、工程 (3) 、其他 (4)、雜項 (5) | 耗品 (1) 、設備 (2) 、工程 (3) 、其他 (4)、雜項 (5) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| attribute | INT | Yes |  |  | 屬性；int數值如下其中之一： 一般 (1)、生產 (2) 、檢測 (3) 、機具 (4) 、其他 (0) | 一般 (1)、生產 (2) 、檢測 (3) 、機具 (4) 、其他 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| company_no | VARCHAR(60) | Yes |  | trans_items2.company_no -> company.no | 客戶資料no，關連至company資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| company_displayName | VARCHAR(60) | Yes |  |  | 客戶公司簡稱，關連至company資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| comment | VARCHAR(128) | Yes |  |  | 備註；varchar(128)；varchar(128) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## user_group


<summary>user_group (使用者群組)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| name | VARCHAR(60) | No | UK(uq_user_group_composite) |  | 使用組名稱；UNIQUE KEY；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| role | INT | Yes |  |  | 角色；int數值如下其中之一1. 管理者2. 執行者(一般使用者)3. 經營者 | 管理者(1)、 一般使用者(2)、 經營者(3) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| users | longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin | Yes |  |  | 員工no，關聯至employee資料表；longtext |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| privileges | longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin | Yes |  |  | 權限清單 | 此欄位為預先保留，尚未定義或確認具體數值 | Need Review | Database document marks this as reserved/undefined; privilege list JSON/text schema and allowed codes are not defined. |



## warehouse_payment


<summary>warehouse_payment (倉儲帳款)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| no | VARCHAR(60) | No | UK(uq_warehouse_payment_composite) |  | 帳款編號；UNIQUE KEY；varchar(60)每日一組帳款編號，出庫時產生帳款編號 |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| group_no | VARCHAR(60) | Yes |  |  | 現結/月結帳款群組編號；varchar(60)現結的no與group_no相同；一個客戶每月一個帳款編號 |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| date | INT | No | UK(uq_warehouse_payment_composite) |  | 日期；UNIQUE KEY；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| arapType | INT | Yes |  |  | 類型；int數值如下其中之一 1: 應收帳款 2: 應付帳款 | 應收帳款(1)、 應付帳款(2) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| batch_no | VARCHAR(60) | Yes |  | warehouse_payment.batch_no -> batch_number.no | 批號no，關聯至batch_number資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| record_no | BIGINT UNSIGNED | Yes |  | warehouse_payment.record_no -> warehouse_record.id | 倉儲紀錄id，關聯至warehouse_record資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_ref_no | VARCHAR(60) | Yes |  | warehouse_payment.item_ref_no -> company.no | 客戶/廠商no，關連至company資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_ref_displayName | VARCHAR(60) | Yes |  |  | 客戶/廠商公司簡稱，關連至company資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| paymentType | INT | Yes |  |  | 倉儲廠商付款類別；int數值如下其中之一：現結 (0)、月結 (1) | 現結 (0)、月結 (1) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| month | DATE | Yes |  |  | 帳款年月；DATE |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| price | DOUBLE | Yes |  |  | 單位價格 (含稅價，小數點4位) ；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| count | INT | Yes |  |  | 計價數量；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| amount | INT | Yes |  |  | 帳款金額 (含稅價) ；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| addDeleteAmount | INT | Yes |  |  | 加/扣款金額 (含稅價)；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| totalAmount | INT | Yes |  |  | 總金額 (加/扣款金額+帳款金額) ；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| balance | INT | Yes |  |  | 應收應付餘額 |  | OK | Description, FK, enum, or index context is now sufficient to identify field purpose. |
| creationTime | INT | Yes |  |  | 資料建立時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## warehouse_record


<summary>warehouse_record (倉租紀錄)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| date | INT | Yes |  |  | 倉儲出庫日；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| ref_no | INT | Yes |  |  | 出入庫紀錄id，關連至inventory_record資料表；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| batch_no | VARCHAR(20) | Yes |  | warehouse_record.batch_no -> batch_number.no | 批號，關連至batch_number資料表；varchar(20) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| contract_no | VARCHAR(60) | Yes |  | warehouse_record.contract_no -> ship_wh_contract.no | 倉儲合約no，關連至ship_wh_contract資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| sw_alias_no | VARCHAR(60) | Yes |  | warehouse_record.sw_alias_no -> ship_wh_alias.no | 倉儲別名no，關連至ship_wh_alias資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| sw_alias_name | VARCHAR(60) | Yes |  |  | 倉儲別名，關連至ship_wh_alias資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_no | VARCHAR(60) | Yes |  | warehouse_record.item_no -> ship_wh.no | 倉儲no (交易品項)，關連至ship_wh資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_name | VARCHAR(60) | Yes |  |  | 倉儲名稱 (交易品項)，關連至ship_wh資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_ref_no | VARCHAR(60) | Yes |  | warehouse_record.item_ref_no -> company.no | 客戶/廠商no，關連至company資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| item_ref_displayName | VARCHAR(60) | Yes |  |  | 客戶/廠商公司簡稱，關連至company資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| inboundTime | INT | Yes |  |  | 原始入庫時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| unit | INT | Yes |  |  | 交易單位；int | 其他 (0)、公克 (1)、公斤 (2)、台斤 (3)、公分 (51)、公尺 (52)、個 (101)、條 (102)、片 (103)、張 (104)、罐 (105)、包 (106)、捲 (107)、桶 (108)、盒 (109)、組 (110)、箱 (111)、支 (112)、式 (113)、入 (114)、袋 (115)、顆 (116)、瓶 (117)、板 (201)、件 (202)、車 (203)、次 (204) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| price | DOUBLE | Yes |  |  | 單價；double |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| count | FLOAT | Yes |  |  | 數量；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| days | FLOAT | Yes |  |  | 存放天數；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| comment | VARCHAR(128) | Yes |  |  | Free-form remark field. |  | OK | Free-form remark field. |
| creationTime | INT | Yes |  |  | 資料建立時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |



## warehouse_inventory_reservation

<summary>warehouse_inventory_reservation ([新增] 倉庫庫存預留紀錄)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | Need Review | [新增] 待工程師依 SQL 實作確認。 |
| no | VARCHAR(60) | No | UK(uq_warehouse_inventory_reservation_composite) |  | 預留紀錄編號 |  | Need Review | [新增] 業務識別碼。 |
| date | INT | No | IDX |  | 預留建立時間，UTC timestamp |  | Need Review | [新增] 第一版不另存 timezone。 |
| refCategory | INT | No | IDX |  | 來源類別 | 銷售/訂購(1)、生產/工單(2)、倉庫任務(3)、其他(0) | Need Review | [新增] 取代 sourceType。 |
| ref_no | VARCHAR(60) | No | IDX |  | 來源單號，對應 product_order、shipping_order、work_order、process_order 或 inventory_order |  | Need Review | [新增] polymorphic reference。 |
| ref_sub_no | VARCHAR(60) | Yes |  |  | 來源明細編號 |  | Need Review | [新增] 若無則空值。 |
| warehouse_no | VARCHAR(60) | Yes | IDX | warehouse_inventory_reservation.warehouse_no -> ship_wh_alias.no | 倉儲別名 no |  | Need Review | [新增] |
| warehouse_displayName | VARCHAR(60) | Yes |  |  | 倉儲別名名稱 |  | Need Review | [新增] |
| itemCategory | INT | No | IDX |  | 料品品項類別 | 原料(1)、物料(2)、膠捲(3)、在製品(4)、製成品(5) | Need Review | [新增] |
| item_no | VARCHAR(60) | No | IDX |  | 料品品項編號 |  | Need Review | [新增] |
| item_name | VARCHAR(255) | Yes |  |  | 料品品項名稱 |  | Need Review | [新增] |
| batchNumber | VARCHAR(60) | Yes | IDX | warehouse_inventory_reservation.batchNumber -> batch_number.no | 批號 |  | Need Review | [新增] 尚未指定批號時可為空。 |
| unit | INT | Yes |  |  | 預留數量單位 | Unit 單位定義 | Need Review | [新增] |
| reservedQuantity | FLOAT | No |  |  | 預留數量 |  | Need Review | [新增] |
| unitCost | DOUBLE | Yes |  |  | 預留計算使用的單位成本 |  | Need Review | [新增] |
| reservedValue | DOUBLE | Yes |  |  | 預留價值 |  | Need Review | [新增] |
| status | INT | No | IDX |  | 預留狀態 | 有效(1)、已釋放(2)、已取消(3)、已轉出庫(4) | Need Review | [新增] |
| releaseTime | INT | Yes |  |  | 預留釋放或完成時間 |  | Need Review | [新增] |
| comment | TEXT | Yes |  |  | 備註 |  | Need Review | [新增] |
| creationTime | INT | No |  |  | 資料建立時間，UTC timestamp |  | Need Review | [新增] |

## warehouse_quality_hold

<summary>warehouse_quality_hold ([新增] 倉庫品檢保留紀錄)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | Need Review | [新增] 待工程師依 SQL 實作確認。 |
| no | VARCHAR(60) | No | UK(uq_warehouse_quality_hold_composite) |  | 品檢保留紀錄編號 |  | Need Review | [新增] |
| date | INT | No | IDX |  | 保留建立時間，UTC timestamp |  | Need Review | [新增] |
| refCategory | INT | No | IDX |  | 來源類別 | 進貨(1)、生產(2)、倉庫任務(3)、其他(0) | Need Review | [新增] |
| ref_no | VARCHAR(60) | No | IDX |  | 來源單號，對應 goods_receipt_note、process_order 或 inventory_order |  | Need Review | [新增] |
| ref_sub_no | VARCHAR(60) | Yes |  |  | 來源明細編號 |  | Need Review | [新增] |
| inspection_no | VARCHAR(60) | Yes | IDX |  | 品檢單號 |  | Need Review | [新增] Quality 模組建立前可先保留。 |
| warehouse_no | VARCHAR(60) | Yes | IDX | warehouse_quality_hold.warehouse_no -> ship_wh_alias.no | 倉儲別名 no |  | Need Review | [新增] |
| warehouse_displayName | VARCHAR(60) | Yes |  |  | 倉儲別名名稱 |  | Need Review | [新增] |
| itemCategory | INT | No | IDX |  | 料品品項類別 | 原料(1)、物料(2)、膠捲(3)、在製品(4)、製成品(5) | Need Review | [新增] |
| item_no | VARCHAR(60) | No | IDX |  | 料品品項編號 |  | Need Review | [新增] |
| item_name | VARCHAR(255) | Yes |  |  | 料品品項名稱 |  | Need Review | [新增] |
| batchNumber | VARCHAR(60) | No | IDX | warehouse_quality_hold.batchNumber -> batch_number.no | 批號 |  | Need Review | [新增] |
| unit | INT | Yes |  |  | 保留數量單位 | Unit 單位定義 | Need Review | [新增] |
| holdQuantity | FLOAT | No |  |  | 品檢保留數量 |  | Need Review | [新增] |
| unitCost | DOUBLE | Yes |  |  | 保留價值計算使用的單位成本 |  | Need Review | [新增] |
| holdValue | DOUBLE | Yes |  |  | 品檢保留價值 |  | Need Review | [新增] |
| status | INT | No | IDX |  | 保留狀態 | 保留中(1)、已放行(2)、退回(3)、報廢(4) | Need Review | [新增] |
| releaseTime | INT | Yes |  |  | 放行、退回或報廢時間 |  | Need Review | [新增] |
| reason | VARCHAR(255) | Yes |  |  | 保留原因 |  | Need Review | [新增] |
| comment | TEXT | Yes |  |  | 備註 |  | Need Review | [新增] |
| creationTime | INT | No |  |  | 資料建立時間，UTC timestamp |  | Need Review | [新增] |

## warehouse_pallet_movement

<summary>warehouse_pallet_movement ([新增] 倉庫棧板異動紀錄)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | Need Review | [新增] |
| no | VARCHAR(60) | No | UK(uq_warehouse_pallet_movement_composite) |  | 棧板異動紀錄編號 |  | Need Review | [新增] |
| date | INT | No | IDX |  | 棧板異動時間，UTC timestamp |  | Need Review | [新增] |
| inventory_record_id | BIGINT UNSIGNED | Yes | IDX | warehouse_pallet_movement.inventory_record_id -> inventory_record.id | 出入庫紀錄 ID |  | Need Review | [新增] |
| refCategory | INT | No | IDX |  | 來源類別 | 入庫(1)、出庫(2)、移倉(3)、預留(4)、品檢保留(5)、釋放(6) | Need Review | [新增] |
| ref_no | VARCHAR(60) | Yes | IDX |  | 來源單號 |  | Need Review | [新增] |
| warehouse_no | VARCHAR(60) | No | IDX | warehouse_pallet_movement.warehouse_no -> ship_wh_alias.no | 倉儲別名 no |  | Need Review | [新增] |
| pallet_group_no | VARCHAR(60) | No | IDX | warehouse_pallet_movement.pallet_group_no -> batchno_serialno_group.group | 棧板編號 |  | Need Review | [新增] |
| batchNumber | VARCHAR(60) | Yes | IDX | warehouse_pallet_movement.batchNumber -> batch_number.no | 批號 |  | Need Review | [新增] |
| serialNo | VARCHAR(60) | Yes |  |  | 批號流水號 |  | Need Review | [新增] |
| itemCategory | INT | Yes | IDX |  | 料品品項類別 |  | Need Review | [新增] |
| item_no | VARCHAR(60) | Yes | IDX |  | 料品品項編號 |  | Need Review | [新增] |
| palletStatus | INT | No | IDX |  | 棧板狀態 | 佔用(1)、預留(2)、釋放(3)、移出(4) | Need Review | [新增] |
| palletCount | FLOAT | No |  |  | 板數 |  | Need Review | [新增] 支援併板小數。 |
| creationTime | INT | No |  |  | 資料建立時間，UTC timestamp |  | Need Review | [新增] |

## item_safety_stock

<summary>item_safety_stock ([新增] 料品安全水位設定)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | Need Review | [新增] |
| no | VARCHAR(60) | No | UK(uq_item_safety_stock_composite) |  | 安全水位設定編號 |  | Need Review | [新增] |
| itemCategory | INT | No | IDX |  | 料品品項類別 | 原料(1)、物料(2)、膠捲(3)、在製品(4)、製成品(5) | Need Review | [新增] |
| item_no | VARCHAR(60) | No | IDX |  | 料品品項編號 |  | Need Review | [新增] |
| item_name | VARCHAR(255) | Yes |  |  | 料品品項名稱 |  | Need Review | [新增] |
| warehouse_no | VARCHAR(60) | Yes | IDX | item_safety_stock.warehouse_no -> ship_wh_alias.no | 倉儲別名 no；空值表示全倉通用 |  | Need Review | [新增] |
| unit | INT | Yes |  |  | 安全水位單位 | Unit 單位定義 | Need Review | [新增] |
| safetyStock | FLOAT | No |  |  | 安全水位數量 |  | Need Review | [新增] |
| effectiveDate | INT | No | IDX |  | 生效時間，UTC timestamp |  | Need Review | [新增] |
| expiryDate | INT | Yes |  |  | 失效時間，UTC timestamp |  | Need Review | [新增] |
| status | INT | No | IDX |  | 狀態 | 啟用(1)、停用(2) | Need Review | [新增] |
| comment | TEXT | Yes |  |  | 備註 |  | Need Review | [新增] |
| creationTime | INT | No |  |  | 資料建立時間，UTC timestamp |  | Need Review | [新增] |

## warehouse_risk_rule

<summary>warehouse_risk_rule ([新增] 倉庫風險規則)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | Need Review | [新增] |
| riskType | VARCHAR(60) | No | UK(uq_warehouse_risk_rule_composite) |  | 風險類型 | TURNOVER_OVER_30_DAYS、SHELF_LIFE_LT_ONE_THIRD、BELOW_SAFETY_STOCK | Need Review | [新增] |
| riskLevel | INT | No |  |  | 預設風險等級 | 正常(1)、注意(2)、警示(3)、危險(4) | Need Review | [新增] |
| messageCode | VARCHAR(80) | No |  |  | 前端 i18n message key |  | Need Review | [新增] |
| messageTemplateZhTw | VARCHAR(255) | Yes |  |  | 預設繁中風險說明模板 |  | Need Review | [新增] |
| recommendedActionCode | VARCHAR(80) | No |  |  | 前端 i18n action key |  | Need Review | [新增] |
| recommendedActionTemplateZhTw | VARCHAR(255) | Yes |  |  | 預設繁中建議處理模板 |  | Need Review | [新增] |
| thresholdValue | FLOAT | Yes |  |  | 規則門檻值 |  | Need Review | [新增] |
| excludedItemCategories | LONGTEXT | Yes |  |  | 排除料品類別 JSON Array |  | Need Review | [新增] |
| status | INT | No | IDX |  | 狀態 | 啟用(1)、停用(2) | Need Review | [新增] |
| creationTime | INT | No |  |  | 資料建立時間，UTC timestamp |  | Need Review | [新增] |

## workflow_task_state

<summary>workflow_task_state ([新增] 跨模組任務狀態)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | Need Review | [新增] |
| taskId | VARCHAR(80) | No | UK(uq_workflow_task_state_composite) |  | 任務識別碼 |  | Need Review | [新增] |
| module | INT | No | IDX |  | 模組 | 採購(1)、業務(2)、生管(3)、製造(4)、倉庫(5)、品保(6)、其他(0) | Need Review | [新增] |
| taskType | INT | No | IDX |  | 任務類型 | 請購(1)、採購(2)、進貨(3)、入庫(4)、出庫(5)、移倉(6)、生產(7)、品檢(8)、出貨(9)、其他(0) | Need Review | [新增] |
| refCategory | INT | No | IDX |  | 來源類別 | 請購(1)、採購(2)、進貨(3)、訂購(4)、銷貨(5)、工單(6)、領退餘廢產(7)、出入庫單(8)、其他(0) | Need Review | [新增] |
| ref_no | VARCHAR(60) | No | IDX |  | 來源單號 |  | Need Review | [新增] |
| ref_sub_no | VARCHAR(60) | Yes |  |  | 來源明細編號 |  | Need Review | [新增] |
| itemCategory | INT | Yes | IDX |  | 料品品項類別 |  | Need Review | [新增] |
| item_no | VARCHAR(60) | Yes | IDX |  | 料品品項編號 |  | Need Review | [新增] |
| item_name | VARCHAR(255) | Yes |  |  | 料品品項名稱 |  | Need Review | [新增] |
| batchNumber | VARCHAR(60) | Yes | IDX |  | 批號 |  | Need Review | [新增] |
| warehouse_no | VARCHAR(60) | Yes | IDX | workflow_task_state.warehouse_no -> ship_wh_alias.no | 倉儲別名 no |  | Need Review | [新增] |
| expectedQuantity | FLOAT | Yes |  |  | 預期處理數量 |  | Need Review | [新增] |
| processedQuantity | FLOAT | Yes |  |  | 已處理數量 |  | Need Review | [新增] |
| acceptedQuantity | FLOAT | Yes |  |  | 已接受數量 |  | Need Review | [新增] |
| rejectedQuantity | FLOAT | Yes |  |  | 已拒收/報廢/退回數量 |  | Need Review | [新增] |
| cancelledQuantity | FLOAT | Yes |  |  | 已取消數量 |  | Need Review | [新增] |
| unit | INT | Yes |  |  | 任務單位 | Unit 單位定義 | Need Review | [新增] |
| palletCount | FLOAT | Yes |  |  | 任務板數 |  | Need Review | [新增] |
| dueTimestamp | INT | Yes | IDX |  | 預計處理時間 |  | Need Review | [新增] |
| taskStatus | INT | No | IDX |  | 任務狀態 | 待處理(1)、部分完成(2)、已完成(3)、阻塞(4)、取消(5) | Need Review | [新增] 第一版由主管人工判斷。 |
| ownerDepartment | INT | No | IDX |  | 下一步負責部門 | 參照 EDepartment | Need Review | [新增] |
| blockReasonCode | VARCHAR(80) | Yes |  |  | 阻塞原因代碼 |  | Need Review | [新增] |
| blockReason | VARCHAR(255) | Yes |  |  | 阻塞原因文字 |  | Need Review | [新增] |
| updateTime | INT | Yes |  |  | 最後更新時間 |  | Need Review | [新增] |
| creationTime | INT | No |  |  | 資料建立時間，UTC timestamp |  | Need Review | [新增] |

## workflow_task_event

<summary>workflow_task_event ([新增] 跨模組任務流程事件歷史)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | Need Review | [新增] 已由工程師確認提案後補入正式 DB schema 文件。 |
| taskId | VARCHAR(80) | No | IDX(idx_workflow_task_event_task_time) | workflow_task_event.taskId -> workflow_task_state.taskId | 對應 workflow_task_state.taskId；一個任務可對應多筆事件 |  | Need Review | [新增] |
| eventCode | VARCHAR(80) | No |  |  | 任務事件代碼；前端依 code 轉換顯示文字 | 例如 workflow.task.created、workflow.task.statusChanged、workflow.task.assigned、workflow.task.blocked、workflow.task.completed | Need Review | [新增] |
| eventTimestamp | BIGINT | No | IDX(idx_workflow_task_event_task_time) |  | 事件發生時間，UTC timestamp |  | Need Review | [新增] |
| fromStatus | INT | Yes |  |  | 事件前任務狀態 | 待處理(1)、部分完成(2)、已完成(3)、阻塞(4)、取消(5) | Need Review | [新增] |
| toStatus | INT | Yes |  |  | 事件後任務狀態 | 待處理(1)、部分完成(2)、已完成(3)、阻塞(4)、取消(5) | Need Review | [新增] |
| fromDepartment | INT | Yes |  |  | 事件前負責部門 | 參照 EDepartment | Need Review | [新增] |
| toDepartment | INT | Yes |  |  | 事件後負責部門 | 參照 EDepartment | Need Review | [新增] |
| actorId | VARCHAR(80) | Yes |  |  | 操作人員或系統流程識別碼 |  | Need Review | [新增] |
| actorName | VARCHAR(128) | Yes |  |  | 操作人員或系統流程顯示名稱 |  | Need Review | [新增] |
| refCategory | INT | Yes | IDX(idx_workflow_task_event_ref) |  | 事件來源類別；僅表示事件發生時的來源上下文，不取代 workflow_task_state 的主任務來源 |  | Need Review | [新增] |
| ref_no | VARCHAR(60) | Yes | IDX(idx_workflow_task_event_ref) |  | 事件來源單號 |  | Need Review | [新增] |
| ref_sub_no | VARCHAR(60) | Yes | IDX(idx_workflow_task_event_ref) |  | 事件來源明細單號 |  | Need Review | [新增] |
| warehouse_no | VARCHAR(60) | Yes | IDX(idx_workflow_task_event_lot) | workflow_task_event.warehouse_no -> ship_wh_alias.no | 倉儲別名 no；不適用時可為 NULL |  | Need Review | [新增] |
| item_no | VARCHAR(60) | Yes | IDX(idx_workflow_task_event_lot) |  | 料品品項 no；不適用時可為 NULL |  | Need Review | [新增] |
| batchNumber | VARCHAR(60) | Yes | IDX(idx_workflow_task_event_lot) | workflow_task_event.batchNumber -> batch_number.no | 批號；不適用時可為 NULL |  | Need Review | [新增] |
| quantity | DECIMAL(18,4) | Yes |  |  | 事件關聯數量；僅保存正數，數量方向由 eventCode 判斷 |  | Need Review | [新增] |
| unit | INT | Yes |  |  | 數量單位 | 參照 Unit enum | Need Review | [新增] |
| reasonCode | VARCHAR(80) | Yes |  |  | 阻塞、退回、取消或調整原因代碼 |  | Need Review | [新增] |
| comment | TEXT | Yes |  |  | 人工備註或系統訊息；欄位命名符合既有資料表的 comment 風格 |  | Need Review | [新增] |
| creationTime | BIGINT | No |  |  | 資料建立時間，UTC timestamp |  | Need Review | [新增] |
| updateTime | BIGINT | Yes |  |  | 資料更新時間，UTC timestamp |  | Need Review | [新增] |

## workflow_next_owner_rule

<summary>workflow_next_owner_rule ([新增] 下一步負責部門規則)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | Need Review | [新增] |
| no | VARCHAR(60) | No | UK(uq_workflow_next_owner_rule_composite) |  | 規則編號 |  | Need Review | [新增] |
| module | INT | No | IDX |  | 適用模組 | 採購(1)、業務(2)、生管(3)、製造(4)、倉庫(5)、品保(6)、其他(0) | Need Review | [新增] |
| taskType | INT | No | IDX |  | 任務類型 | 請購(1)、採購(2)、進貨(3)、入庫(4)、出庫(5)、移倉(6)、生產(7)、品檢(8)、出貨(9)、其他(0) | Need Review | [新增] |
| refCategory | INT | Yes | IDX |  | 來源類別；空值表示不限定來源類別 |  | Need Review | [新增] |
| taskStatus | INT | Yes | IDX |  | 任務狀態條件；空值表示不限定狀態 |  | Need Review | [新增] |
| blockReasonCode | VARCHAR(80) | Yes | IDX |  | 阻塞原因條件；空值表示不限定阻塞原因 |  | Need Review | [新增] |
| fromDepartment | INT | Yes | IDX |  | 目前負責部門；空值表示不限定目前部門 |  | Need Review | [新增] |
| ownerDepartment | INT | No | IDX |  | 下一步負責部門 | 參照 EDepartment | Need Review | [新增] |
| rulePriority | INT | No | IDX |  | 規則優先序；數字越小優先 |  | Need Review | [新增] |
| status | INT | No | IDX |  | 狀態 | 啟用(1)、停用(2) | Need Review | [新增] |
| comment | TEXT | Yes |  |  | 備註 |  | Need Review | [新增] |
| creationTime | INT | No |  |  | 資料建立時間，UTC timestamp |  | Need Review | [新增] |



## work_order

<summary>work_order (派工單)</summary>

| 欄位名稱 | 資料型態 | 允許Null | 索引 | 外鍵 | 欄位說明 | 值定義 | 狀態 | Review Note |
|----------|----------|------|-----|------|----------|----------------|------|------|
| id | BIGINT UNSIGNED | No | PK |  | AUTO_INCREMENT；<PK> |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| no | VARCHAR(60) | No | UK(uq_work_order_composite) |  | 編號；UNIQUE KEY；varchar(20) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creator_no | VARCHAR(60) | Yes |  | work_order.creator_no -> employee.no | 製單人員no，關連至employee資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| product_order_no | VARCHAR(60) | Yes |  | work_order.product_order_no -> product_order.no | 訂購單id，關連至product_order資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| aps_no | VARCHAR(60) | Yes |  | work_order.aps_no -> aps_quantity.no | APS排程編號，關連至aps_quantity資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| date | INT | Yes |  |  | 派工日期；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| product_no | VARCHAR(60) | Yes |  | work_order.product_no -> product.no | 交易品項no，關連至product資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| product_name | VARCHAR(60) | Yes |  |  | 交易品項名稱，關連至product 資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| customer_no | VARCHAR(60) | Yes |  | work_order.customer_no -> company.no | 客戶no，關連至company資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| customer_displayName | VARCHAR(60) | Yes |  |  | 客戶公司簡稱，關連至company資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| output_item_no | VARCHAR(255) | Yes |  |  | 產出的料品品項no，關連至 inproduct / product資料表 |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| output_item_name | VARCHAR(60) | Yes |  |  | 產出的料品品項名稱，關連至 inproduct / product資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| production_line_no | VARCHAR(60) | Yes |  | work_order.production_line_no -> production_line.no | 生產線no，關連至production_line資料表；varchar(60) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| oneProcess | INT | Yes |  |  | 主製程；int數值如下其中之一 前備 (1)、加工 (2)、包裝 (3)、其他 (0) | 前備 (1)、加工 (2)、包裝 (3)、其他 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| secProcess | INT | Yes |  |  | 次製程；int前備；數值如下其中之一調拌 (1)、塞料 (2)、烘烤(3)、灌料(4) 、其他 (0)加工；數值如下其中之一披覆 (1)、封膜 (2) 、其他 (0)包裝；數值如下其中之一成組 (1)、入箱 (2) 、其他 (0) | 調拌 (1)、塞料 (2)、烘烤(3)、灌料(4) 、其他 (0)加工；數值如下披覆 (1)、封膜 (2) 、其他 (0)包裝；數值如下成組 (1)、入箱 (2) 、其他 (0) | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| startTime | INT | Yes |  |  | 預計開始時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| endTime | INT | Yes |  |  | 預計結束時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| processUnit | INT | Yes |  |  | 預估生產的料品品項單位；int數值如下其中之一： 公斤、其他 參照「Unit單位定義」 | 公斤、其他 參照「Unit單位定義」 | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| processCount | FLOAT | Yes |  |  | 預估生產數量 (小數點2位) ；float |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| processTime | INT | Yes |  |  | 預估投產時數 (以分鐘為單位) ；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| laborCount | INT | Yes |  |  | 預估投產人數；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| laborList | longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin | Yes |  |  | 預估投產人數清單；員工no，關連至employee資料表(JOSN Array) ；longtext |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| comment | VARCHAR(128) | Yes |  |  | 備註；varchar(128) |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |
| creationTime | INT | Yes |  |  | 資料建立時間；int |  | OK | Meaning is supported by Word description, SQL constraint, enum, or relation. |

