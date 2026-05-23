# ERP 2.0 Frontend V1 Master Spec and Integration Roadmap

日期：2026-05-23  
適用範圍：ODM 食品加工廠 ERP 2.0 Web 前端第一版  
資料基準：EWDB_20260522.sql、EWDB_20260522_WORKFLOW.md  
設計基準：清晰、專業、簡潔、易操作、管理導向

## 1. 第一版定位

ERP 2.0 前端第一版先以經營者與管理者視角建立完整營運工作區。目標不是一次完成所有資料輸入與簽核，而是先讓核心營運流程可視化，讓使用者能快速回答：

1. 產品能否被報價與接單？
2. 接單後交期與生產是否做得出來？
3. 物料、產能、人員、品質、庫存、出貨是否有阻擋？
4. 出貨後毛利、請款與收款是否可追蹤？
5. 哪些主檔、權限、語言與系統設定會影響流程正確性？

第一版原則：

- 以 Web 作為主要操作介面。
- 先支援經營者與管理者的查詢、警示、判斷與協調。
- 操作者輸入流程保留為第二階段逐步深化。
- 各頁採用一致架構：KPI 摘要、分頁視圖、工作清單、選取明細、流程節點。
- 按鈕可先作為下一階段操作入口，但第一版 API 整合時需標明哪些是真實動作。

## 2. 角色分層

| 角色 | 第一版重點 | 典型問題 |
| --- | --- | --- |
| 經營者 | 營運風險、交期、毛利、資金、庫存價值 | 今天哪些訂單會延誤？毛利是否低於預期？資金卡在哪裡？ |
| 管理者 | 排程、缺料、品質、倉儲、派車、人力協調 | 哪些工單不能如期？哪裡缺料/缺人？哪些批號不能出貨？ |
| 操作者 | 現場執行狀態與任務提示 | 今天要做什麼？哪張單要處理？哪個批號被阻擋？ |

第一版主要先完成經營者與管理者視角；操作者流程以狀態呈現為主，正式輸入與行動流程後續補齊。

## 3. 核心流程

```txt
R&D / Costing
-> Items / BOM
-> Orders
-> Planning / APS
-> Purchasing / Warehouse / Workforce
-> Production
-> Quality
-> Logistics
-> Finance
-> Settings / Master Data
```

流程說明：

1. `R&D / Costing` 建立產品開發、BOM 版本、成本試算與報價基礎。
2. `Items / BOM` 承接已核准的品項與量產 BOM 主檔。
3. `Orders` 判斷接單承諾、交期與履約風險。
4. `Planning / APS` 將訂單需求展開成物料、產能、人員與工單建議。
5. `Purchasing / Warehouse / Workforce` 分別處理缺料、庫存與人力準備。
6. `Production` 執行工單、MES 狀態、效率、損耗與生產品質。
7. `Quality` 決定放行、隔離、返工、報廢與文件完整性。
8. `Logistics` 處理出庫、派車、冷鏈、文件與簽收。
9. `Finance` 追蹤預估/實際毛利、請款、應收與成本差異。
10. `Settings / Master Data` 治理主檔、權限、串接與語言。

## 4. 第一版工作區清單

| 工作區 | 路徑 | 第一版回答的問題 | 狀態 |
| --- | --- | --- | --- |
| Dashboard | `/` | 全廠總覽與跨模組摘要 | 待重新整理 |
| R&D / Costing | `/rd` | 產品是否可報價？BOM 與成本依據是否成立？ | 已建立 |
| Orders | `/orders` | 訂單能否承諾？交期與履約風險在哪？ | 已建立 |
| Planning / APS | `/planning` | 接單後如何轉成物料、產能與工單建議？ | 已建立 |
| Purchasing | `/purchasing` | 哪些料需請購？哪些到貨會影響生產？ | 已建立 |
| Warehouse | `/warehouse` | 庫存價值、倉位、週轉、效期與待處理出入庫 | 已建立 |
| Workforce | `/workforce` | 人力、技能、加班、證照是否支援排程？ | 已建立 |
| Production | `/production` | 工單排程、MES、效率、損耗與品質狀態 | 已建立 |
| Quality | `/quality` | 哪些批號可放行？哪些阻擋入庫/出貨/生產？ | 已建立 |
| Traceability | `/traceability` | 批號、工單、訂單、文件與召回範圍 | 已建立 |
| Logistics | `/logistics` | 今日出貨、派車、冷鏈、文件與簽收 | 已建立 |
| Finance | `/finance` | 毛利、成本差異、請款、收款與應付影響 | 已建立 |
| Items | `/items` | 品項主檔、分類、效期、溫層、安全庫存 | 已建立但可再收斂 |
| BOM | `/bom` | 量產 BOM、配方版本、製程參數 | 已建立但可再收斂 |
| Batches | `/batches` | 批號主檔與批次狀態 | 待後續收斂 |
| AI | `/ai` | 管理摘要、洞察、風險說明輔助 | 待後續收斂 |
| Settings | `/settings` | 主檔治理、權限、串接、語言 | 已建立 |

## 5. 邊界整理

### R&D / Costing vs Items / BOM

`R&D / Costing` 管開發案、試作 BOM、報價成本與量產移轉判斷。  
`Items / BOM` 管已核准後的正式主檔與量產 BOM。

第一版整合時應避免 Planning 或 Orders 引用未核准的開發版 BOM。

### Orders vs Planning / APS

`Orders` 回答能否承諾交期，使用 ATP/CTP 概念。  
`Planning / APS` 回答如何執行，展開 BOM、缺料、產能、人員與工單建議。

Orders 不應直接自動建立請購或工單。

### Planning / APS vs Production

`Planning / APS` 產出建議與阻擋。  
`Production` 管正式排程、工單執行、MES、效率與損耗。

第一版可先用相同 mock 概念，API 整合時需區分建議計劃與正式工單。

### Quality vs Warehouse / Logistics

`Quality` 決定批號是否可放行。  
`Warehouse` 根據放行狀態決定可用庫存。  
`Logistics` 根據放行與出庫狀態決定可否出貨。

未放行批號不應成為可出貨庫存。

### Logistics vs Finance

`Logistics` 管 POD 簽收。  
`Finance` 使用 POD 作為請款 readiness 的重要條件。

第一版可以先顯示 POD 狀態，後續再決定是否未簽收不可請款。

## 6. API 整合順序建議

### Phase 1：唯讀資料總覽

目標：先讓前端從 restserver 讀取真實資料，替換 mock。

順序：

1. `Warehouse`
2. `Orders`
3. `Production`
4. `Quality`
5. `Purchasing`
6. `Planning / APS`
7. `Logistics`
8. `Finance`
9. `R&D / Costing`
10. `Settings / Master Data`

理由：先接營運當日最需要的狀態，再接前段研發與後段治理。

### Phase 2：跨模組阻擋關係

目標：讓頁面不是各自獨立，而能互相引用真實阻擋。

優先整合：

- 品檢未放行 -> Warehouse 可用庫存 / Logistics 出貨阻擋
- 缺料 -> Planning / Purchasing / Production 阻擋
- 工單完成 -> Quality / Warehouse / Logistics 更新
- POD 完成 -> Finance 可請款
- R&D 報價版 BOM -> Orders 報價與毛利基準

### Phase 3：可控操作

目標：導入少量高價值操作，不一次開放全部 CRUD。

建議優先操作：

1. 訂單高風險確認/備註
2. Planning 建議轉請購
3. Planning 建議轉工單
4. Quality 放行/隔離判定
5. Warehouse 出庫覆核
6. Logistics 派車與 POD 回傳
7. Finance 請款標記
8. R&D 報價版 BOM 核准

所有操作需先搭配權限與稽核策略。

## 7. 第一版暫不做

- 完整自動排程最佳化
- 完整電子簽核引擎
- 完整會計總帳
- 完整 HR 薪資與請假
- 完整路線最佳化/GPS
- 完整配方編輯器
- 完整多語內容字典化
- 手機/PDA 現場完整輸入流程

這些不是不重要，而是應放在第二版或第三版，避免第一版失焦。

## 8. 近期待辦建議

1. 重新整理 Dashboard，使其成為經營者第一入口。
2. 製作前端 API 欄位對照表，對應 EWDB_20260522 與 restserver module。
3. 標記每個按鈕第一版是 `placeholder`、`read-only action` 還是 `real mutation`。
4. 統一各工作區狀態用語，例如正常、注意、高風險、阻擋、待處理。
5. 補齊多語 dictionary 結構，先處理導航與核心分頁，再逐步處理頁面文字。
6. 與工程師依 main branch 對齊 API 串接優先順序。
7. 盤點操作者場景，決定哪些需要 PDA/平板專用流程。

## 9. 判斷結論

目前第一版核心規劃完整，適合進入總體收斂與 API 整合準備。接下來不建議再新增大型核心頁，除非有明確營運流程缺口。比較高價值的下一步是：

```txt
Dashboard 收斂
-> API 對照表
-> 權限/操作級別
-> 真實資料唯讀串接
-> 高價值操作逐步開放
```

