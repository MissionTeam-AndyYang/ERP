# 倉庫經營總覽資料庫新增規劃

日期：2026-06-11
狀態：草案 / 待工程師 Review
基準文件：`docs/spec/database/index.md`
目的：補足 `warehouse_overview_api.md` 中已確認「尚未規劃與實作」的資料來源，供工程師 review 後再進入 SQL schema 與 ORM 實作。

## 標記規則

本文件所有新規劃的 table 或欄位皆以 `[新增]` 標記。
既有資料表與欄位只作為基準引用，不在本文件直接修改 `docs/spec/database/index.md`。

## 本次需補足的資料能力

| 需求 | 是否既有可支援 | 建議處理 |
| --- | --- | --- |
| 預留數量、預留價值 | 尚未完整支援 | [新增] `warehouse_inventory_reservation` |
| 可用數量、可用價值 | 可由目前庫存扣除預留與品檢保留後推導 | 不落地或於 API 計算 |
| 品檢保留量、品檢保留價值 | 尚未完整支援 | [新增] `warehouse_quality_hold` |
| 各類別與各倉儲佔用板數 | `batchno_serialno_group` 只支援棧板與批號/流水號關係 | [新增] `warehouse_pallet_movement` |
| 倉儲總板位與可用板位 | 尚未完整支援 | [新增] `warehouse_capacity` |
| 安全水位 | 尚未支援 | [新增] `item_safety_stock` |
| 風險說明文字、建議處理方式 | 可由前端 i18n 或後端規則產生 | [新增] `warehouse_risk_rule`，前端仍負責多國語言顯示 |
| 任務處理狀態、下一步負責部門 | 尚未完整支援 | [新增] `warehouse_task_state` |

## 既有資料表基準

| 既有 Table | 可沿用用途 |
| --- | --- |
| `inventory_record` | 出入庫紀錄、目前庫存數量、庫存價值來源。 |
| `inventory_delta` | 每日庫存異動彙總。 |
| `inventory_item_month_statistic` | 每月料品/批號庫存量與價值。 |
| `inventory_month_statistic` | 每月類別庫存量與價值。 |
| `batch_number` | 批號、有效天數、有效期限、來源單據。 |
| `batchno_serialno` | 批號流水號與倉儲關係。 |
| `batchno_serialno_group` | 棧板編號與批號/流水號關係。 |
| `ship_wh_alias` | 倉儲別名、倉儲名稱、倉儲類型。 |
| `goods_receipt_note` | 採購入庫來源單據。 |
| `shipping_order` | 銷售出庫來源單據。 |
| `process_order` | 生產領料、退料、餘料、廢料、產品入庫/出庫來源。 |
| `inventory_order` | 人工出入庫、移倉、盤點來源。 |
| `item_price` | 單位成本候選來源；工程師回覆建議 `item_price.costPriceWeight`。 |

## [新增] warehouse_inventory_reservation

用途：記錄庫存預留來源，支援預留數量、預留價值、可用數量與可用價值計算。

| Field | Type | Required | Key / Index | Description |
| --- | --- | --- | --- | --- |
| id | BIGINT UNSIGNED | YES | PK | [新增] 資料 ID。 |
| no | VARCHAR(60) | YES | UK | [新增] 預留紀錄編號。 |
| date | INT | YES | IDX | [新增] 預留建立時間，UTC timestamp。 |
| timezone | VARCHAR(60) | NO |  | [新增] 使用者端時區。 |
| sourceType | INT | YES | IDX | [新增] 預留來源類型；採購(1)、銷售(2)、工單(3)、倉庫任務(4)、其他(0)。 |
| source_no | VARCHAR(60) | YES | IDX | [新增] 來源單號，例如訂單、工單、出入庫單。 |
| source_sub_no | VARCHAR(60) | NO |  | [新增] 來源明細編號，若無則空值。 |
| warehouse_no | VARCHAR(60) | NO | IDX | [新增] 倉儲別名 no，關聯至 `ship_wh_alias.no`。 |
| warehouse_displayName | VARCHAR(60) | NO |  | [新增] 倉儲別名名稱。 |
| itemCategory | INT | YES | IDX | [新增] 料品品項類別。 |
| item_no | VARCHAR(60) | YES | IDX | [新增] 料品品項編號。 |
| item_name | VARCHAR(255) | NO |  | [新增] 料品品項名稱。 |
| batchNumber | VARCHAR(60) | NO | IDX | [新增] 批號，關聯至 `batch_number.no`；尚未指定批號時可為空。 |
| unit | INT | NO |  | [新增] 預留數量單位。 |
| reservedQuantity | FLOAT | YES |  | [新增] 預留數量。 |
| unitCost | DOUBLE | NO |  | [新增] 預留計算使用的單位成本。 |
| reservedValue | DOUBLE | NO |  | [新增] 預留價值。 |
| status | INT | YES | IDX | [新增] 預留狀態；有效(1)、已釋放(2)、已取消(3)、已轉出庫(4)。 |
| releaseTime | INT | NO |  | [新增] 預留釋放或完成時間。 |
| comment | TEXT | NO |  | [新增] 備註。 |
| creationTime | INT | YES |  | [新增] 建立時間，UTC timestamp。 |

建議索引：

| Index | Fields | Purpose |
| --- | --- | --- |
| `idx_wir_item_batch_wh_status` | `item_no`, `batchNumber`, `warehouse_no`, `status` | 快速計算庫存明細預留量。 |
| `idx_wir_source` | `sourceType`, `source_no`, `source_sub_no` | 追溯預留來源。 |
| `idx_wir_date` | `date` | 查詢期間內預留異動。 |

## [新增] warehouse_quality_hold

用途：記錄品檢保留或隔離庫存，支援品檢保留量、品檢保留價值與可用量扣除。

| Field | Type | Required | Key / Index | Description |
| --- | --- | --- | --- | --- |
| id | BIGINT UNSIGNED | YES | PK | [新增] 資料 ID。 |
| no | VARCHAR(60) | YES | UK | [新增] 品檢保留紀錄編號。 |
| date | INT | YES | IDX | [新增] 保留建立時間，UTC timestamp。 |
| sourceType | INT | YES | IDX | [新增] 品檢來源類型；進貨(1)、生產(2)、銷退(3)、其他(0)。 |
| source_no | VARCHAR(60) | YES | IDX | [新增] 來源單號。 |
| inspection_no | VARCHAR(60) | NO | IDX | [新增] 品檢單號；若 Quality 模組尚未建立，可先保留。 |
| warehouse_no | VARCHAR(60) | NO | IDX | [新增] 倉儲別名 no。 |
| warehouse_displayName | VARCHAR(60) | NO |  | [新增] 倉儲別名名稱。 |
| itemCategory | INT | YES | IDX | [新增] 料品品項類別。 |
| item_no | VARCHAR(60) | YES | IDX | [新增] 料品品項編號。 |
| item_name | VARCHAR(255) | NO |  | [新增] 料品品項名稱。 |
| batchNumber | VARCHAR(60) | YES | IDX | [新增] 批號。 |
| unit | INT | NO |  | [新增] 保留數量單位。 |
| holdQuantity | FLOAT | YES |  | [新增] 品檢保留數量。 |
| unitCost | DOUBLE | NO |  | [新增] 保留價值計算使用的單位成本。 |
| holdValue | DOUBLE | NO |  | [新增] 品檢保留價值。 |
| status | INT | YES | IDX | [新增] 保留狀態；保留中(1)、已放行(2)、退回(3)、報廢(4)。 |
| releaseTime | INT | NO |  | [新增] 放行、退回或報廢時間。 |
| reason | VARCHAR(255) | NO |  | [新增] 保留原因。 |
| comment | TEXT | NO |  | [新增] 備註。 |
| creationTime | INT | YES |  | [新增] 建立時間，UTC timestamp。 |

## [新增] warehouse_capacity

用途：記錄倉儲總板位與容量設定，支援各倉儲可用板位計算。

| Field | Type | Required | Key / Index | Description |
| --- | --- | --- | --- | --- |
| id | BIGINT UNSIGNED | YES | PK | [新增] 資料 ID。 |
| no | VARCHAR(60) | YES | UK | [新增] 容量設定編號。 |
| warehouse_no | VARCHAR(60) | YES | IDX | [新增] 倉儲別名 no，關聯至 `ship_wh_alias.no`。 |
| warehouse_displayName | VARCHAR(60) | NO |  | [新增] 倉儲別名名稱。 |
| capacityUnit | INT | YES |  | [新增] 容量單位；建議使用 Unit 定義中的 板(201)。 |
| totalPallets | INT | YES |  | [新增] 總板位。 |
| effectiveDate | INT | YES | IDX | [新增] 生效時間，UTC timestamp。 |
| expiryDate | INT | NO |  | [新增] 失效時間；空值表示仍有效。 |
| status | INT | YES | IDX | [新增] 狀態；啟用(1)、停用(2)。 |
| comment | TEXT | NO |  | [新增] 備註。 |
| creationTime | INT | YES |  | [新增] 建立時間，UTC timestamp。 |

## [新增] warehouse_pallet_movement

用途：補足「出入庫紀錄與棧板對應關係」，支援已佔用板數、預留板數、可用板位與批號追溯。

| Field | Type | Required | Key / Index | Description |
| --- | --- | --- | --- | --- |
| id | BIGINT UNSIGNED | YES | PK | [新增] 資料 ID。 |
| no | VARCHAR(60) | YES | UK | [新增] 棧板異動紀錄編號。 |
| date | INT | YES | IDX | [新增] 棧板異動時間，UTC timestamp。 |
| inventory_record_id | BIGINT UNSIGNED | NO | IDX | [新增] 關聯 `inventory_record.id`。 |
| sourceType | INT | YES | IDX | [新增] 來源類型；入庫(1)、出庫(2)、移倉(3)、盤點(4)、預留(5)、釋放(6)。 |
| source_no | VARCHAR(60) | NO | IDX | [新增] 來源單號。 |
| warehouse_no | VARCHAR(60) | YES | IDX | [新增] 倉儲別名 no。 |
| pallet_group_no | VARCHAR(60) | YES | IDX | [新增] 棧板編號，對應 `batchno_serialno_group.group`。 |
| batchNumber | VARCHAR(60) | NO | IDX | [新增] 批號。 |
| serialNo | VARCHAR(60) | NO |  | [新增] 批號流水號。 |
| itemCategory | INT | NO | IDX | [新增] 料品品項類別。 |
| item_no | VARCHAR(60) | NO | IDX | [新增] 料品品項編號。 |
| palletStatus | INT | YES | IDX | [新增] 棧板狀態；佔用(1)、預留(2)、釋放(3)、移出(4)。 |
| palletCount | FLOAT | YES |  | [新增] 板數；整板為 1，允許小數支援併板。 |
| creationTime | INT | YES |  | [新增] 建立時間，UTC timestamp。 |

## [新增] item_safety_stock

用途：定義安全水位，支援低於安全水位風險警示。

| Field | Type | Required | Key / Index | Description |
| --- | --- | --- | --- | --- |
| id | BIGINT UNSIGNED | YES | PK | [新增] 資料 ID。 |
| no | VARCHAR(60) | YES | UK | [新增] 安全水位設定編號。 |
| itemCategory | INT | YES | IDX | [新增] 料品品項類別。 |
| item_no | VARCHAR(60) | YES | IDX | [新增] 料品品項編號。 |
| item_name | VARCHAR(255) | NO |  | [新增] 料品品項名稱。 |
| warehouse_no | VARCHAR(60) | NO | IDX | [新增] 倉儲別名 no；空值表示全倉通用。 |
| unit | INT | NO |  | [新增] 安全水位單位。 |
| safetyStock | FLOAT | YES |  | [新增] 安全水位數量。 |
| effectiveDate | INT | YES | IDX | [新增] 生效時間，UTC timestamp。 |
| expiryDate | INT | NO |  | [新增] 失效時間。 |
| status | INT | YES | IDX | [新增] 狀態；啟用(1)、停用(2)。 |
| comment | TEXT | NO |  | [新增] 備註。 |
| creationTime | INT | YES |  | [新增] 建立時間，UTC timestamp。 |

## [新增] warehouse_risk_rule

用途：定義風險規則、預設嚴重度、風險說明與建議處理方式。
多國語言顯示仍建議由前端依 `riskType`、`messageCode`、`recommendedActionCode` 進行轉換；本表可保存預設繁中模板與後端規則參數。

| Field | Type | Required | Key / Index | Description |
| --- | --- | --- | --- | --- |
| id | BIGINT UNSIGNED | YES | PK | [新增] 資料 ID。 |
| riskType | VARCHAR(60) | YES | UK | [新增] 風險類型，例如 `TURNOVER_OVER_30_DAYS`。 |
| riskLevel | VARCHAR(20) | YES |  | [新增] 預設風險等級；`normal`、`warning`、`danger`。 |
| messageCode | VARCHAR(80) | YES |  | [新增] 前端 i18n message key。 |
| messageTemplateZhTw | VARCHAR(255) | NO |  | [新增] 預設繁中風險說明模板。 |
| recommendedActionCode | VARCHAR(80) | YES |  | [新增] 前端 i18n action key。 |
| recommendedActionTemplateZhTw | VARCHAR(255) | NO |  | [新增] 預設繁中建議處理模板。 |
| thresholdValue | FLOAT | NO |  | [新增] 規則門檻值，例如 30 天或 0.3333。 |
| excludedItemCategories | VARCHAR(255) | NO |  | [新增] 排除料品類別，例如 `2,3` 表示物料、膠捲。 |
| status | INT | YES | IDX | [新增] 狀態；啟用(1)、停用(2)。 |
| creationTime | INT | YES |  | [新增] 建立時間，UTC timestamp。 |

## [新增] warehouse_task_state

用途：記錄倉庫任務狀態與下一步負責部門，避免每次查詢都只能由來源單據即時計算，並支援人工阻塞/解除阻塞。

| Field | Type | Required | Key / Index | Description |
| --- | --- | --- | --- | --- |
| id | BIGINT UNSIGNED | YES | PK | [新增] 資料 ID。 |
| taskId | VARCHAR(80) | YES | UK | [新增] 任務識別碼。 |
| taskType | INT | YES | IDX | [新增] 任務類型；入庫(1)、出庫(2)、移倉(3)、盤點(4)。 |
| sourceType | INT | YES | IDX | [新增] 來源類型；採購(1)、銷售(2)、生產(3)、出入庫單(4)、其他(0)。 |
| source_no | VARCHAR(60) | YES | IDX | [新增] 來源單號。 |
| source_sub_no | VARCHAR(60) | NO |  | [新增] 來源明細編號。 |
| itemCategory | INT | NO | IDX | [新增] 料品品項類別。 |
| item_no | VARCHAR(60) | NO | IDX | [新增] 料品品項編號。 |
| item_name | VARCHAR(255) | NO |  | [新增] 料品品項名稱。 |
| batchNumber | VARCHAR(60) | NO | IDX | [新增] 批號。 |
| warehouse_no | VARCHAR(60) | NO | IDX | [新增] 倉儲別名 no。 |
| expectedQuantity | FLOAT | NO |  | [新增] 預期處理數量。 |
| processedQuantity | FLOAT | NO |  | [新增] 已處理數量。 |
| unit | INT | NO |  | [新增] 任務單位。 |
| palletCount | FLOAT | NO |  | [新增] 任務板數。 |
| dueTimestamp | INT | NO | IDX | [新增] 預計處理時間。 |
| taskStatus | INT | YES | IDX | [新增] 任務狀態；待處理(1)、部分完成(2)、已完成(3)、阻塞(4)、取消(5)。 |
| ownerDepartment | INT | YES | IDX | [新增] 下一步負責部門；參照 `EDepartment`。 |
| blockReasonCode | VARCHAR(80) | NO |  | [新增] 阻塞原因代碼。 |
| blockReason | VARCHAR(255) | NO |  | [新增] 阻塞原因文字。 |
| updateTime | INT | NO |  | [新增] 最後更新時間。 |
| creationTime | INT | YES |  | [新增] 建立時間，UTC timestamp。 |

## 建議實作順序

1. [新增] `item_safety_stock`、`warehouse_capacity`：先補足低風險且獨立的 master/config 資料。
2. [新增] `warehouse_inventory_reservation`：支援可用量與預留量。
3. [新增] `warehouse_quality_hold`：支援品檢保留量與可用量扣除。
4. [新增] `warehouse_pallet_movement`：支援出入庫紀錄與棧板異動關係。
5. [新增] `warehouse_task_state`：支援任務狀態、負責部門與阻塞狀態。
6. [新增] `warehouse_risk_rule`：支援風險訊息模板與建議處理方式。

## Review 後需同步的文件

工程師確認後，應再同步更新：

1. `docs/spec/database/index.md`
2. 對應 SQL schema 檔案
3. `restserver/package/dbwrapper/table.py`
4. `docs/spec/api-proposal/warehouse_overview_api.md`
5. `docs/engineering/WAREHOUSE_OVERVIEW_BACKEND_FLOW_ALGORITHM.md`
