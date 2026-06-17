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
| `trendDays` | 建議預設 7，未來可擴充為 query parameter |

處理流程：

1. 依 `x-timezone` 將查詢時間轉為查詢營業日 `queryDate`。
2. 產生趨勢日期範圍，例如 `queryDate - 6 days` 至 `queryDate`。
3. 對每個 `itemCategory` 找出趨勢起始日前最近一筆 `inventory_month_statistic` 月結基準。
4. 以月結基準的 `endAmount` 作為起始庫存價值。
5. 讀取月結日後至 `queryDate` 的 `inventory_delta`，依 `date`、`warehouse_no`、`category` 彙總每日 `inAmount - outAmount`。
6. 逐日累加每日異動，產生每個日期與料品品項類別的 `inventoryValue`。
7. 回傳 `payload.valueTrend[]`，日期格式固定為 `YYYY-MM-DD`。

計算公式：

```text
dailyDeltaAmount = sum(inventory_delta.inAmount) - sum(inventory_delta.outAmount)
inventoryValue(date D) = latestMonthEndAmount + cumulativeDailyDeltaAmount(monthEndDate < date <= D)
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
| 查無月結基準 | 回傳 `0.0`，並可在 log 中記錄統計資料不足 |
| 查無某日 delta | 視為當日異動金額 0 |
| `warehouse_no` 有指定 | 所有月結與 delta 均需限制相同倉儲 |
| `itemCategory` 有指定 | 僅計算指定料品品項類別 |

## 數字格式

| 欄位 | 格式 |
| --- | --- |
| `valueTrend[].inventoryValue` | 金額，四捨五入取整數 |
| `inventoryValueByCategory[].trend7Days` | 比率，建議取至小數點第 2 位 |

## 效能建議

1. 第一版可於 Dashboard API 即時計算 7 日趨勢，因資料範圍短。
2. 若未來趨勢期間擴大為 30 日、90 日或跨年度，建議新增快取或每日趨勢彙總表。
3. `inventory_delta` 建議確認至少具備以下索引或等效查詢效能：
   - `date`
   - `timezone`
   - `warehouse_no`
   - `category`

## 待工程師確認

| 項目 | 說明 | 工程師回覆 |
| --- | --- | --- |
| 類別層級基準表 | 第一版是否同意使用 `inventory_month_statistic` 作為 Dashboard 類別趨勢基準。 |  |
| 批號層級需求 | 第一版趨勢是否不需要展開至批號或料品層級。 |  |
| `trend7Days` 除以 0 | 是否同意 base value 為 0 時回傳 `0.0`。 |  |
| `trendDays` query parameter | 第一版是否固定 7 日，暫不新增 query parameter。 |  |
| 查無月結資料 | 是否同意第一版回傳空趨勢或 `0.0`，不改用 `inventory_record` 即時計算長區間趨勢。 |  |
