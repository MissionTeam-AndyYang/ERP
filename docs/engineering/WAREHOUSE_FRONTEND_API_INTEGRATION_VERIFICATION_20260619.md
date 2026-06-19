# Warehouse 前後端 API 串接確認指南

## 目的

本文件用於協助工程師在未安裝前端開發環境的情況下，透過已啟動的前端畫面確認 Warehouse Dashboard API 串接結果。

## 本次串接範圍

| 前端畫面 | 後端 API | 說明 |
| --- | --- | --- |
| `/warehouse` | GET `/api/v2/warehouse/dashboard?includeInventory=true&trendDays=7` | Warehouse 經營總覽、庫存價值、倉位、風險、待處理任務、庫存明細與 7 日價值趨勢 |

## 前端環境變數

由有前端環境的人員啟動前端時，請設定：

```txt
NEXT_PUBLIC_API_BASE_URL=http://<backend-host>:<backend-port>
NEXT_PUBLIC_API_TIMEZONE=Asia/Taipei
NEXT_PUBLIC_API_TOKEN=<若後端 TOKEN_ENABLED=1，填入可用 token；未啟用可省略>
```

若未設定 `NEXT_PUBLIC_API_BASE_URL`，前端會呼叫同網域 `/api/v2/warehouse/dashboard`；若該路徑不存在，畫面會自動切回 mock fallback。

## 工程師無前端環境確認方式

工程師不需要安裝 Node.js 或前端套件。請由有前端環境的人員啟動前端，再提供工程師以下其中一種方式確認：

| 方式 | 工程師需要做什麼 | 適用情境 |
| --- | --- | --- |
| 區網 URL | 直接用瀏覽器開啟 `http://<frontend-host>:3000/warehouse` | 工程師與前端啟動者在同一內網 |
| 遠端分享 URL | 由前端啟動者使用公司核准的 tunnel 或遠端分享工具提供 URL | 工程師不在同一網段 |
| 螢幕分享 | 前端啟動者開啟 `/warehouse`，工程師透過會議確認畫面與後端 log | 僅需快速確認流程 |

## 啟動畫面方式

由有前端環境的人員在專案根目錄執行：

```txt
npm.cmd run dev -- -p 3000
```

開啟：

```txt
http://localhost:3000/warehouse
```

若前端成功呼叫後端 API，畫面左上資料來源會顯示 `API data`。若後端未連線或 API 回傳錯誤，會顯示 `Mock fallback` 與錯誤訊息。

## 工程師確認重點

1. Warehouse Dashboard 畫面左上顯示 `API data`。
2. 後端收到 GET `/api/v2/warehouse/dashboard?includeInventory=true&trendDays=7`。
3. 畫面 KPI 與 API payload summary 對應：
   - `summary.totalInventoryValue` → 庫存總價值
   - `summary.availableInventoryValue` → 可用庫存價值提示
   - `summary.usedPallets / totalPallets` → 倉位使用率
   - `summary.riskAlertCount` → 風險品項
   - `pendingInboundCount + pendingOutboundCount` → 今日待處理
4. 類別表格與 API payload `inventoryValueByCategory[]` 對應：
   - `inventoryValue`
   - `valueRatio`
   - `palletCount`
   - `reservedValue`
   - `availableValue`
   - `trend7Days`
   - `itemCount`
5. 倉位卡片與 API payload `capacityByWarehouse[]` 對應。
6. 風險警示與 API payload `riskAlerts[]` 對應。
7. 待處理任務與 API payload `pendingTasks[]` 對應。
8. 庫存明細與 API payload `inventory[]` 對應。

## 驗證狀態

本次已執行：

```txt
npm.cmd run build
npm.cmd run lint
.\.venv\Scripts\python.exe -m pytest restserver\tests\test_warehouse_dashboard.py
```

結果：

```txt
Next build passed
ESLint passed
8 passed
```
