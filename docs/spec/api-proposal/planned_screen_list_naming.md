
# Planned Screen List And Naming

## 倉管中心

| Screen Code | 正式畫面名稱 | Route / UI Location | Implementation Status | Primary API | 說明 |
| --- | --- | --- | --- | --- | --- |
| `WarehouseOverviewScreen` | 倉庫中心總覽 | `/warehouse` | 已有第一版，需持續整合 API | `GET /api/v2/warehouse/dashboard` | Warehouse 入口畫面，呈現 KPI、庫存價值分類、倉位容量、風險警示摘要與待處理任務摘要。 |
| `WarehouseInventoryLotListScreen` | 庫存批號明細清單 | 建議 route：`/warehouse/inventory/lots`；也可先嵌入 `/warehouse` 的「庫存明細」工作區 | 待實作 | `GET /api/v2/warehouse/inventory/lots` | 批號層級清單畫面，支援倉庫、料品類別、料號、批號、風險、任務、可用狀態、關鍵字、排序與分頁。 |
| `WarehouseInventoryLotDetailPanel` | 庫存批號追蹤面板 | `WarehouseInventoryLotListScreen` 右側 panel；窄版可作為 detail route 或 drawer | 待實作 | `GET /api/v2/warehouse/inventory/lots/wh/{warehouseNo}/item/{itemNo}/batch/{batchNo}` | 顯示單一批號的庫存摘要、入出庫紀錄、預留、品檢保留、板位異動、未完成任務與風險。 |

