# Warehouse 庫存價值趨勢 API 提案

## 文件目的

本文件針對 Warehouse Dashboard 中尚未實作的 `valueTrend` 與 `inventoryValueByCategory[].trend7Days` 欄位，提出資料來源與演算法設計，供工程師 review。

本提案尚未代表 API 已確認或已實作。待工程師確認資料來源、演算法與效能風險後，再更新正式 API 文件並開始程式實作。

## 受影響 API

| API | 欄位 | 目前狀態 |
| --- | --- | --- |
| GET `/api/v2/warehouse/dashboard` | `payload.valueTrend[]` | 第一版保留空陣列 |
| GET `/api/v2/warehouse/dashboard` | `payload.inventoryValueByCategory[].trend7Days` | 第一版固定回傳 `0.0` |

## 建議資料來源

| 資料表 | 用途 |
| --- | --- |
| `inventory_month_statistic` | 類別層級月底庫存價值基準，可用於快速計算各料品品項類別的趨勢 |
| `inventory_item_month_statistic` | 料品/批號層級月底庫存量與庫存價值基準，可在需要批號或料品細分趨勢時使用 |
| `inventory_delta` | 每日入庫/出庫數量與金額異動，用於將月結基準補算至指定日期 |

第一版建議以 `inventory_month_statistic` 加 `inventory_delta` 產生類別層級趨勢，原因是 Dashboard 的趨勢圖與 `trend7Days` 目前均以「料品品項類別」呈現，不需要批號層級明細。

## 建議回傳結構

```json
{
  "valueTrend": [
    {
      "date": "2026-06-17",
      "itemCategory": 1,
      "inventoryValue": 1250000
    }
  ],
  "inventoryValueByCategory": [
    {
      "itemCategory": 1,
      "trend7Days": 4.2
    }
  ]
}
```

## valueTrend 演算法提案

輸入：

| 參數 | 說明 |
| --- | --- |
| `date` | 查詢基準營業日 |
| `x-timezone` | 用於判定營業日 |
| `warehouse_no` | 可選，限制倉儲別名 |
| `itemCategory` | 可選，限制料品品項類別 |
| `trendDays` | 第一版新增 query parameter，但固定接受/使用 `7`；未提供時預設為 `7` |

處理流程：

1. 依 `x-timezone` 將查詢時間轉為查詢營業日 `queryDate`。
2. 讀取 `trendDays` query parameter；第一版僅接受/使用 `7`，未提供時預設為 `7`。
3. 產生趨勢日期範圍，例如 `queryDate - 6 days` 至 `queryDate`。
4. 第一版趨勢畫面目前只呈現料品品項類別層級，尚未呈現批號或料品層級，因此不展開批號/料品明細。
5. 對每個 `itemCategory` 找出趨勢起始日前最近一筆 `inventory_month_statistic` 月結基準。
6. 若查得到月結基準，且 `inventory_delta` 日期可覆蓋至 `queryDate`，以月結基準 `endAmount` 搭配 delta 逐日補算。
7. 若查無月結基準，或 `inventory_delta` 最新日期早於 `queryDate`，第一版因固定 7 日短區間，改用 `inventory_record` 依每日截止時間即時計算各日庫存價值。
8. 回傳 `payload.valueTrend[]`，日期格式固定為 `YYYY-MM-DD`。

計算公式：

```text
dailyDeltaAmount = sum(inventory_delta.inAmount) - sum(inventory_delta.outAmount)
inventoryValue(date D) = latestMonthEndAmount + cumulativeDailyDeltaAmount(monthEndDate < date <= D)
```

`inventory_record` 即時計算公式：

```text
inventoryValue(date D) =
    sum(inventory_record.amount where category = IN and date <= endOfBusinessDay(D))
  - sum(inventory_record.amount where category = OUT and date <= endOfBusinessDay(D))
```

## trend7Days 演算法提案

`trend7Days` 表示該料品品項類別在最近 7 日的庫存價值變化率。

計算公式：

```text
baseDate = queryDate - 7 days
trend7Days = ((inventoryValue(queryDate) - inventoryValue(baseDate)) / inventoryValue(baseDate)) * 100
```

邊界條件：

| 條件 | 建議處理 |
| --- | --- |
| `inventoryValue(baseDate)` 為 0 | 回傳 `0.0`，避免除以 0 |
| 查無月結基準 | 第一版固定 7 日短區間，改用 `inventory_record` 依每日截止時間即時計算 |
| 查無某日 delta | 若 `inventory_delta` 最新日期仍覆蓋到 `queryDate`，視為當日異動金額 0；若最新日期早於 `queryDate`，改用 `inventory_record` 即時計算 |
| `warehouse_no` 有指定 | 所有月結與 delta 均需限制相同倉儲 |
| `itemCategory` 有指定 | 僅計算指定料品品項類別 |

## 數字格式

| 欄位 | 格式 |
| --- | --- |
| `valueTrend[].inventoryValue` | 金額，四捨五入取整數 |
| `inventoryValueByCategory[].trend7Days` | 比率，建議取至小數點第 2 位 |

## 效能建議

1. 第一版可於 Dashboard API 即時計算 7 日趨勢，因資料範圍短。
2. 正常資料完整時，優先使用 `inventory_month_statistic` + `inventory_delta`，避免每日都從 `inventory_record` 長區間掃描。
3. 當月結或 delta 覆蓋不足時，因第一版固定 7 日趨勢，可接受以 `inventory_record` 即時計算作為防護性補算。
4. 若未來趨勢期間擴大為 30 日、90 日或跨年度，建議新增快取或每日趨勢彙總表，不建議長期以 `inventory_record` 即時計算長區間趨勢。
5. `inventory_delta` 建議確認至少具備以下索引或等效查詢效能：
   - `date`
   - `timezone`
   - `warehouse_no`
   - `category`

## 待工程師確認

| 項目 | 說明 | 工程師回覆 |
| --- | --- | --- |
| 類別層級基準表 | 第一版是否同意使用 `inventory_month_statistic` 作為 Dashboard 類別趨勢基準。 | 同意 |
| 批號層級需求 | 第一版趨勢是否不需要展開至批號或料品層級。 | 請確認目前畫面是否已有呈現批號或料品層級。若已有呈現，則需進一步擴充至完整的批號或料品層級，並同步檢查程式邏輯與 API 文件是否一致 |
| `trend7Days` 除以 0 | 是否同意 base value 為 0 時回傳 `0.0`。 | 同意 |
| `trendDays` query parameter | 第一版是否固定 7 日，暫不新增 query parameter。 | 目前第一版僅顯示 7 日趨勢。建議新增 query parameter，並將查詢參數固定為 7。|
| 查無月結資料 | 是否同意第一版回傳空趨勢或 `0.0`，不改用 `inventory_record` 即時計算長區間趨勢。 | 目前第一版僅顯示 7 日趨勢。建議改採用`inventory_record`進行即時計算。待未來查詢區間進一步拉長，再進行效能最佳化與演算法優化。 |

## Codex 理解與文件修正

| 項目 | 理解與處理 |
| --- | --- |
| 類別層級基準表 | 工程師同意第一版使用 `inventory_month_statistic` 作為 Dashboard 類別趨勢基準；文件維持類別層級趨勢設計。 |
| 批號或料品層級 | 目前 Warehouse 第一版畫面未呈現批號或料品層級趨勢圖，僅呈現類別層級趨勢，因此第一版不展開批號/料品層級。 |
| `trend7Days` 除以 0 | 工程師同意 base value 為 0 時回傳 `0.0`。 |
| `trendDays` query parameter | 第一版新增 `trendDays` query parameter，但固定接受/使用 `7`；若未提供則預設為 `7`。 |
| 查無月結資料 | 工程師建議第一版 7 日趨勢可改用 `inventory_record` 即時計算；文件已改為短區間 fallback 策略，未來查詢區間拉長時再做快取或演算法最佳化。 |



