# 倉庫經營總覽資料庫新增規劃

日期：2026-06-11
狀態：草案 / 待工程師 Review
基準文件：`docs/spec/database/index.md`
目的：補足 `warehouse_overview_api.md` 中已確認「尚未規劃與實作」的資料來源，供工程師 review 後再進入 SQL schema 與 ORM 實作。


## 工程師提問與建議:

1. 能否詳細說明`warehouse_inventory_reservation` 、 `warehouse_quality_hold` 及 `warehouse_pallet_movement`中的`source_no`分別關聯至那些資料表? 此外，`sourceType`欄位是否是依據`source_no`來源單號而對應的類型? 能否進一步說明不同來源單號對應到的來源類型，例如：進貨單對應採購？
2. 能否詳細說明，為什麼`warehouse_inventory_reservation`需要設置`timezone`欄位, 而 `warehouse_quality_hold`則不需要？請闡述其中的設計考量。
3. `warehouse_inventory_reservation` 和 `warehouse_quality_hold`是否可以僅以 id 作為主鍵 (PK) 與唯一鍵 (UK)? 還是`no`欄位除了作為唯一鍵之外，尚有其他設計考量？
4. 是否可以以`ship_wh`取代`warehouse_capacity`?
`ship_wh`: 代表「交易品項-倉儲物流」，其中 unit 為儲放／運輸單位，maxCapacity 為最大儲放／運輸量。
`ship_wh_quotation`: 代表「倉儲物流議價」，並綁定至ship_wh
`ship_wh_contract`: 代表「倉儲物流合約」，並綁定至ship_wh_alias，當議價成功後產生合約。
整體流程為： ship_wh → ship_wh_quotation → ship_wh_contract。
當儲放／運輸量發生變動時，會產生新的交易品項，並重新進行議價與簽訂合約。
5. 是否能將 `warehouse_pallet_movement` 的資料分散並整合至 `inventory_record`、`warehouse_inventory_reservation`、`warehouse_quality_hold`？這三張資料表分別記載出入庫數量、預留數量與保留數量，若再額外記錄棧板資訊，理論上應可行；還是此設計上另有其他考量？
6. 請購單`purchase_request`、 採購單`purchase_order`、 報價單`quotation` 、 訂購單 `product_order`是否同樣適用『任務處理狀態』的概念？若是，請重新檢視你所設計的資料表 `warehouse_task_state`，確認是否能共用同一資料表。
7. 能否詳細說明目前有哪些風險類型？另外，`riskType`、`riskLevel` 與 `excludedItemCategories` 的資料型態是否適合採用 ENUM？ 改用 VARCHAR(255)，是否還有其他設計上的考量？」
8. 建議 `source_no`欄位更名`ref_no` 、 `source_sub_no`欄位更名`ref_subNo`, 以保持與原資料庫命名規則的一致性。

## 本次調整決議

| 項目 | 決議 |
| --- | --- |
| `sourceType` 命名 | 更名為 `refCategory`，用於表示 `ref_no` 指向的業務來源類別。 |
| `source_no` / `source_sub_no` 命名 | 更名為 `ref_no` / `ref_sub_no`，以符合既有資料庫命名規則。 |
| `id` 與 `no` | 維持原設計：`id` 作 PK，`no` 作 UK 與業務識別碼。 |
| `warehouse_pallet_movement` | 維持原設計，不分散整合至 `inventory_record`、`warehouse_inventory_reservation`、`warehouse_quality_hold`。 |
| `timezone` | 新增規劃表不個別保存 `timezone`；統一保存 UTC timestamp，API 層依使用者時區轉換查詢營業日。 |
| 倉儲總板位 | 優先沿用 `ship_wh.maxCapacity`、`ship_wh_quotation`、`ship_wh_contract`、`ship_wh_alias`，取消新增 `warehouse_capacity`。 |
| 任務狀態 | 將 `warehouse_task_state` 調整為跨模組 `workflow_task_state`，供請購、採購、進貨、生產、訂購出貨與倉庫任務共用。 |
| 盤點 | 第一版 Warehouse dashboard 暫不處理盤點。 |
| 風險型別 | 不使用 DB 原生 ENUM；`riskType` 使用穩定字串代碼，`riskLevel` 使用 INT enum，排除類別以 JSON Array 保存。 |


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
| 倉儲總板位與可用板位 | `ship_wh.maxCapacity`、`ship_wh_contract` 可支援合約倉容量 | 沿用既有 `ship_wh` / `ship_wh_contract` / `ship_wh_alias` |
| 安全水位 | 尚未支援 | [新增] `item_safety_stock` |
| 風險說明文字、建議處理方式 | 可由前端 i18n 或後端規則產生 | [新增] `warehouse_risk_rule`，前端仍負責多國語言顯示 |
| 任務處理狀態、下一步負責部門 | 尚未完整支援 | [新增] `workflow_task_state` |

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
| `inventory_order` | 人工出入庫、移倉來源；第一版 Warehouse dashboard 暫不處理盤點。 |
| `purchase_request` | 請購來源，可用於跨模組 workflow 狀態追蹤；不作為庫存預留來源。 |
| `purchase_order` | 採購來源，可用於跨模組 workflow 狀態追蹤；不作為庫存預留來源。 |
| `product_order` | 訂購來源，可作為成品出貨預留或跨模組 workflow 狀態追蹤來源。 |
| `item_price` | 單位成本候選來源；工程師回覆建議 `item_price.costPriceWeight`。 |

## [新增] warehouse_inventory_reservation

用途：記錄庫存預留來源，支援預留數量、預留價值、可用數量與可用價值計算。

| Field | Type | Required | Key / Index | Description |
| --- | --- | --- | --- | --- |
| id | BIGINT UNSIGNED | YES | PK | [新增] 資料 ID。 |
| no | VARCHAR(60) | YES | UK | [新增] 預留紀錄編號。 |
| date | INT | YES | IDX | [新增] 預留建立時間，UTC timestamp。 |
| refCategory | INT | YES | IDX | [新增] 來源類別；銷售/訂購(1)、生產/工單(2)、倉庫任務(3)、其他(0)。 |
| ref_no | VARCHAR(60) | YES | IDX | [新增] 來源單號，對應 `product_order.no`、`shipping_order.no`、`work_order.no`、`process_order.no`、`inventory_order.no`。 |
| ref_sub_no | VARCHAR(60) | NO |  | [新增] 來源明細編號，若無則空值。 |
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
| `idx_wir_ref` | `refCategory`, `ref_no`, `ref_sub_no` | 追溯預留來源。 |
| `idx_wir_date` | `date` | 查詢期間內預留異動。 |

## [新增] warehouse_quality_hold

用途：記錄品檢保留或隔離庫存，支援品檢保留量、品檢保留價值與可用量扣除。

| Field | Type | Required | Key / Index | Description |
| --- | --- | --- | --- | --- |
| id | BIGINT UNSIGNED | YES | PK | [新增] 資料 ID。 |
| no | VARCHAR(60) | YES | UK | [新增] 品檢保留紀錄編號。 |
| date | INT | YES | IDX | [新增] 保留建立時間，UTC timestamp。 |
| refCategory | INT | YES | IDX | [新增] 來源類別；進貨(1)、生產(2)、倉庫任務(3)、其他(0)。 |
| ref_no | VARCHAR(60) | YES | IDX | [新增] 來源單號，對應 `goods_receipt_note.no`、`process_order.no`、`inventory_order.no`。 |
| ref_sub_no | VARCHAR(60) | NO |  | [新增] 來源明細編號，若無則空值。 |
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

## 沿用既有 ship_wh / ship_wh_contract 作為倉儲容量來源

用途：支援各倉儲總板位、可用板位與容量使用率計算。
本次取消新增 `warehouse_capacity`，優先沿用既有倉儲物流模型：

| 既有 Table / Field | 用途 |
| --- | --- |
| `ship_wh.maxCapacity` | 最大儲放/運輸量，作為合約倉或物流倉容量基準。 |
| `ship_wh.unit` | 儲放/運輸單位；用於判斷是否為板、箱、重量或其他容量單位。 |
| `ship_wh_contract.sw_alias_no` | 關聯至 `ship_wh_alias.no`，取得實際倉儲別名。 |
| `ship_wh_contract.item_no` | 關聯至 `ship_wh.no`，取得容量交易品項。 |
| `ship_wh_quotation.item_no` | 倉儲物流議價項目，流程上位於 `ship_wh` 與 `ship_wh_contract` 之間。 |

若後續確認自有倉沒有對應 `ship_wh_contract` 或 `ship_wh` 資料，再另行評估是否需要極簡容量補充表。

## [新增] warehouse_pallet_movement

用途：補足「出入庫紀錄與棧板對應關係」，支援已佔用板數、預留板數、可用板位與批號追溯。

| Field | Type | Required | Key / Index | Description |
| --- | --- | --- | --- | --- |
| id | BIGINT UNSIGNED | YES | PK | [新增] 資料 ID。 |
| no | VARCHAR(60) | YES | UK | [新增] 棧板異動紀錄編號。 |
| date | INT | YES | IDX | [新增] 棧板異動時間，UTC timestamp。 |
| inventory_record_id | BIGINT UNSIGNED | NO | IDX | [新增] 關聯 `inventory_record.id`。 |
| refCategory | INT | YES | IDX | [新增] 來源類別；入庫(1)、出庫(2)、移倉(3)、預留(4)、品檢保留(5)、釋放(6)。 |
| ref_no | VARCHAR(60) | NO | IDX | [新增] 來源單號。 |
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
| riskLevel | INT | YES |  | [新增] 預設風險等級；正常(1)、注意(2)、警示(3)、危險(4)。 |
| messageCode | VARCHAR(80) | YES |  | [新增] 前端 i18n message key。 |
| messageTemplateZhTw | VARCHAR(255) | NO |  | [新增] 預設繁中風險說明模板。 |
| recommendedActionCode | VARCHAR(80) | YES |  | [新增] 前端 i18n action key。 |
| recommendedActionTemplateZhTw | VARCHAR(255) | NO |  | [新增] 預設繁中建議處理模板。 |
| thresholdValue | FLOAT | NO |  | [新增] 規則門檻值，例如 30 天或 0.3333。 |
| excludedItemCategories | LONGTEXT | NO |  | [新增] 排除料品類別 JSON Array，例如 `[2,3]` 表示物料、膠捲。 |
| status | INT | YES | IDX | [新增] 狀態；啟用(1)、停用(2)。 |
| creationTime | INT | YES |  | [新增] 建立時間，UTC timestamp。 |

## [新增] workflow_task_state

用途：記錄跨模組任務狀態與下一步負責部門，涵蓋請購、採購、進貨、生產、訂購出貨與倉庫任務，避免每次查詢都只能由來源單據即時計算，並支援人工阻塞/解除阻塞。

| Field | Type | Required | Key / Index | Description |
| --- | --- | --- | --- | --- |
| id | BIGINT UNSIGNED | YES | PK | [新增] 資料 ID。 |
| taskId | VARCHAR(80) | YES | UK | [新增] 任務識別碼。 |
| module | INT | YES | IDX | [新增] 模組；採購(1)、業務(2)、生管(3)、製造(4)、倉庫(5)、品保(6)、其他(0)。 |
| taskType | INT | YES | IDX | [新增] 任務類型；請購(1)、採購(2)、進貨(3)、入庫(4)、出庫(5)、移倉(6)、生產(7)、品檢(8)、出貨(9)、其他(0)。 |
| refCategory | INT | YES | IDX | [新增] 來源類別；請購(1)、採購(2)、進貨(3)、訂購(4)、銷貨(5)、工單(6)、領退餘廢產(7)、出入庫單(8)、其他(0)。 |
| ref_no | VARCHAR(60) | YES | IDX | [新增] 來源單號。 |
| ref_sub_no | VARCHAR(60) | NO |  | [新增] 來源明細編號。 |
| itemCategory | INT | NO | IDX | [新增] 料品品項類別。 |
| item_no | VARCHAR(60) | NO | IDX | [新增] 料品品項編號。 |
| item_name | VARCHAR(255) | NO |  | [新增] 料品品項名稱。 |
| batchNumber | VARCHAR(60) | NO | IDX | [新增] 批號。 |
| warehouse_no | VARCHAR(60) | NO | IDX | [新增] 倉儲別名 no。 |
| expectedQuantity | FLOAT | NO |  | [新增] 預期處理數量。 |
| processedQuantity | FLOAT | NO |  | [新增] 已處理數量。 |
| acceptedQuantity | FLOAT | NO |  | [新增] 已接受數量；可用於進貨或品檢結案。 |
| rejectedQuantity | FLOAT | NO |  | [新增] 已拒收/報廢/退回數量；可用於差異結案。 |
| cancelledQuantity | FLOAT | NO |  | [新增] 已取消數量；可用於短交、取消或不再處理的差異結案。 |
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

1. [新增] `item_safety_stock`，並確認 `ship_wh` / `ship_wh_contract` 可支援倉儲容量來源。
2. [新增] `warehouse_inventory_reservation`：支援可用量與預留量。
3. [新增] `warehouse_quality_hold`：支援品檢保留量與可用量扣除。
4. [新增] `warehouse_pallet_movement`：支援出入庫紀錄與棧板異動關係。
5. [新增] `workflow_task_state`：支援跨模組任務狀態、負責部門與阻塞狀態。
6. [新增] `warehouse_risk_rule`：支援風險訊息模板與建議處理方式。

## Review 後需同步的文件

工程師確認後，應再同步更新：

1. `docs/spec/database/index.md`
2. 對應 SQL schema 檔案
3. `restserver/package/dbwrapper/table.py`
4. `docs/spec/api-proposal/warehouse_overview_api.md`
5. `docs/engineering/WAREHOUSE_OVERVIEW_BACKEND_FLOW_ALGORITHM.md`
