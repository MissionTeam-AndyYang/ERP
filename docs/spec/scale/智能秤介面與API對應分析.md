# 智能秤介面與 API 對應分析

> 分析日期：2026-06-12  
> 來源文件：
> - `docs/spec/scale/智能秤.md`
> - `docs/spec/scale/智能秤任務.md`
> - `docs/spec/scale/恆旺介面視意圖V6.pptx`
> - `docs/spec/scale/電子智能秤系統REST API_1.06.docx`

## 一、第一頁投影片畫面判讀

第一頁畫面為：

- 角色：倉庫
- 作業：入庫
- 模式：秤重
- 品項類別頁籤：採購
- 畫面主體：採購入庫待處理品項清單、批號/序號/重量/效期列表、秤重上下限與目前重量、品項基本資料。

因此此畫面的主要資料來源應為「採購類別項目」API，完成秤重/入庫後再呼叫資料回傳 API。

## A. API 呼叫資訊

### 主要載入 API

- Endpoint: `/item/purchase`
- Method: `GET`
- Query Parameters:
  - `registerNo`: 需前端補值，設備註冊碼
  - `dateTimestampUTC`: 需前端補值，今日作業日期 UTC timestamp
  - `shift`: 需前端補值，目前班別，對應 Appendix `shift`

### 完成作業回傳 API

- Endpoint: `/item/data`
- Method: `POST`
- Send Data:
  - `registerNo`
  - `total`
  - `results[].devAction`
  - `results[].devComment`
  - `results[].refNo`
  - `results[].refNoSec`
  - `results[].itemBatchNo[].batchNo`
  - `results[].itemBatchNo[].serialNos[].devDateTimestamp`
  - `results[].itemBatchNo[].serialNos[].serialNo`
  - `results[].itemBatchNo[].serialNos[].value`
  - `results[].itemBatchNo[].serialNos[].isValid`

### 候選 API 與選擇原因

| 候選 API | 用途 | 判斷 |
|---|---|---|
| `GET /item/purchase` | 取得採購進貨/採購退貨待作業品項 | 此頁選中「採購」且為倉庫入庫秤重，最符合 |
| `GET /item/info` | 依批號查詢品項資訊 | 適合掃描批號後補查，不是此清單主資料源 |
| `POST /item/data` | 回傳採購、產製、訂購、其他品項更新資料 | 完成秤重/入庫後呼叫，不是畫面初始載入 |

## B. UI 欄位對應表

| UI 欄位 | API 回傳欄位 | 備註 |
|--------|--------------|------|
| 左側品項列表 | `payload.results[].itemName` | 顯示可處理品項名稱 |
| 客戶/廠商 | `payload.results[].itemVendor` | 畫面例：台糖 |
| 品項名稱 | `payload.results[].itemName` | 畫面例：台糖肉酥起司捲(5入)彩盒 |
| 類別 | `payload.results[].itemType` | enum `type`，畫面例：原料 |
| 型態 | `payload.results[].itemCategory` | enum `category`，畫面例：新料品 |
| 批號/板號 | `payload.results[].itemBatchNo[].batchNo` | 此頁為採購 API，實際對應批號；若為板號需改用 `/item/groupInfo` |
| 備註 | `payload.results[].itemComment` | 可為空 |
| 清單：批號 | `payload.results[].itemBatchNo[].batchNo` | 表格第一欄 |
| 清單：序號 | `payload.results[].itemBatchNo[].serialNos[].serialNo` | 入庫新批號時可能由 APP 建立或 API 給空陣列 |
| 清單：重量/數量 | `payload.results[].itemBatchNo[].serialNos[].value` | 已秤/已存在項目；新入庫秤重結果送出時對應 `/item/data` |
| 清單：效期 | `payload.results[].itemBatchNo[].validDateTimestamp` | 前端需格式化日期 |
| 序號筆數 | 無直接單一欄位 | 可由 `serialNos.length` 或 APP 暫存列數計算 |
| 累計重量/數量 | 無直接單一欄位 | 可由畫面已勾選/已秤列的 `value` 加總 |
| 排定重量/數量 | `payload.results[].itemAmount` | 單位見 `itemAmountUnit` |
| 上限 | `payload.results[].itemMaxWeight` | 畫面例：190.00 |
| 下限 | `payload.results[].itemMinWeight` | 畫面例：180.00 |
| 重量 | 無直接回傳欄位 | 來自智能秤即時讀值，送出時對應 `/item/data` 的 `serialNos[].value` |
| 勾選圖示 | 無直接欄位 | APP 操作狀態；送出時可對應 `serialNos[].isValid` |
| 刪除 | 無直接欄位 | APP 本地操作；若影響結果，送出資料需反映在 `/item/data` |

## 二、與 Warehouse Dashboard 的一致性檢查

### 目前沒有直接衝突

智能秤流程中的採購、產製、訂購、其他，能對應 warehouse dashboard 目前的 `sourceType`：

| 智能秤 API 類別 | Dashboard `sourceType` 建議值 |
|---|---|
| `/item/purchase` | 採購 |
| `/item/manufacture` | 生產 |
| `/item/sales` | 出貨 |
| `/item/other` | 調整 |

料品類別 `原料 / 物料 / 膠捲 / 在製品 / 製成品` 也與 dashboard 的 `InventoryCategory` 一致。

### 需要工程確認的整合缺口

1. `智能秤.md` 提到料品品項包含「貨品」，但 REST API 1.06 Appendix `type` 與 dashboard `InventoryCategory` 目前都未包含「貨品」。若貨品會進入倉庫或銷售流程，需補 enum 與前端型別。

2. Warehouse dashboard 目前呼叫 `/api/v1/warehouse/dashboard`，但後端尚未看到對應 endpoint。智能秤 `/item/data` 寫入後，dashboard 應從 `inventory_record`、`batchno_serialno`、`batchno_serialno_group` 等資料聚合。

3. Dashboard `WarehouseTask.type` 目前只有 `入庫 / 出庫 / 移倉 / 盤點`。智能秤流程還有 `退料 / 餘料 / 廢料 / 產製品 / 入產 / 出產` 等細分類。倉庫畫面可維持入庫/出庫，但建議新增 `subType` 或 `sourceSubType`，避免追溯資訊被壓扁。

4. 後端 `/item/info` 與 `/item/groupInfo` 實作目前疑似與 REST API 1.06 欄位語意不一致：
   - 實作回傳 `itemValidDateTimestamp`，docx 欄位為 `validDateTimestamp`
   - 實作中 `itemType` / `itemCategory` 可能與 docx 語意互換

5. 後端存在 `GET /item/data/group` route，但 REST API 1.06 未列此 API。文件已標示為 `Need Review`，需工程決定是否保留並補入規格。

## 三、資料表對應建議

| 智能秤流程資料 | 既有資料表/欄位 | 說明 |
|---|---|---|
| 設備註冊碼與角色 | `device.no`, `device.role` | 決定 APP 角色與可執行作業 |
| 回傳原始資料 | `device_log.data` | 保存設備端送出的 JSON |
| 批號 | `batch_number.no` | 由 server 控管批號 |
| 序號 | `batchno_serialno.serialNo` | 同批號下的實體包裝單位 |
| 棧板/成板 | `batchno_serialno_group.group` | 對應 APP 成板資料 |
| 出入庫紀錄 | `inventory_record` | dashboard 應聚合此表做庫存現況 |
| 倉庫入出庫歷史 | `warehouse_record` | 若 dashboard 要呈現寄倉/倉庫營運明細，可與 `inventory_record` 分工 |

## 四、API 文件已同步調整

已依 `電子智能秤系統REST API_1.06.docx` 更新：

- `docs/spec/api/user.md`
- `docs/spec/api/item.md`

主要調整：

- 將設備 API URL 從 `//item/...`、`//user/...` 對齊為 `/item/...`、`/user/...`
- 補上 required query parameter
- 補上 `total`、`devComment`
- 將 `action/type/category/unit/pageType/valid` 對應至 Appendix enum
- 將 `validDateTimestamp`、`itemType`、`itemCategory`、重量/數量欄位語意對齊 docx
- 將 `GET /item/data/group` 標示為「後端存在但 REST API 1.06 未列」
