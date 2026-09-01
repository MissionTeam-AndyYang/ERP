# 程式修正V3
1. /api/v2/trace/batches/{batch_no}/overview 的 traceSteps[]
   - 投入數量 action=1 的加總扣除 action=2 的加總作為計算依據。若其結果為零，則不需繼續追溯。請依此邏輯修正後端程式碼

## 程式修正V3回覆

| 項目 | 回覆與文件調整 |
|---|---|
| 淨投入數量判斷 | 已依「程式修正V3」補強。`traceSteps[].inputItems[].quantity` 先依 `production_data_input.action` 計算：`action=1` 領料加總扣除 `action=2` 退料加總，再依 `itemNo + batchNo + itemCategory + unit` 彙總。 |
| 淨投入為 0 的處理 | 若投入批號彙總後淨投入量為 0，該投入項目不回傳於 `inputItems[]`；若該批號是本次追溯路徑的 focus input，該 production step 不建立，也不將其產出批號加入下一層 trace queue。 |
| 製成品 upstream 展開 | 查詢製成品批號往上游追溯時，若某投入批號的淨投入量為 0，該投入項目不回傳，也不再往該投入批號的上游展開。 |
| 測試補強 | 已新增 regression tests，確認原料 downstream 在淨投入為 0 時不建立後續 production step，且製成品 upstream 不會沿著淨投入為 0 的投入批號繼續追溯。 |

# 程式修正V2
1. /api/v2/trace/batches/{batch_no}/overview 的 traceSteps[]
   - 追溯投入物過程需參照 production_data_input 資料表的 action 欄位（領料=1、退料=2）。投入數量應以 action=1 的加總扣除 action=2 的加總，才是該批號的實際投入數量。請依此邏輯修正後端程式碼。
   - 原料批號 A 投入後，產製出在製品批號 B 與在製品批號 C。同一派工單中，在製品批號 B 與在製品批號 C 進一步包裝，產出製成品 D。由於 stepId 重複，程式僅會保留最後一筆資料，導致僅儲存『投入物在製品批號 B 對應產出物製成品 D』或『投入物在製品批號 C 對應產出物製成品 D』其中一組關聯。請修正後端程式碼邏輯，確保所有投入物與產出物的對應關係均能正確保存。

## 程式修正V2回覆

| 項目 | 回覆與文件調整 |
|---|---|
| 投入數量計算 | 已修正。`traceSteps[].inputItems[].quantity` 需依 `production_data_input.action` 計算實際投入量：`action=1` 領料列為正數、`action=2` 退料列為負數，最後依 `itemNo + batchNo + itemCategory + unit` 加總並取至小數點第 2 位；淨投入量為 0 的投入項目不回傳、不繼續追溯。 |
| 產出數量計算 | `traceSteps[].outputItems[].quantity` 維持依 `production_data_output.count` 加總；本次修正僅針對投入物的領料/退料淨額。 |
| stepId 重複合併 | 已修正。當同一 `work_order_no` 因多個追溯批號被重複命中時，不再直接跳過既有 step，而是將新的 focus `inputItems[]` / `outputItems[]` 合併至既有 `traceSteps[]`。 |
| 重複 output 防護 | 合併既有 step 時，以 `itemNo + batchNo + itemCategory + unit` 作為唯一鍵；已存在的 output item 不再次累加，避免在製品 B 與在製品 C 同時指向製成品 D 時，製成品 D 被重複加總。 |
| 測試補強 | 已新增 regression tests，確認投入數量會扣除退料，且同一工單中在製品 B / C 共同產出製成品 D 時，B 與 C 都會保留在 `inputItems[]`，D 只保留單筆不重複加總。 |

# 程式修正
1. 針對 "新版 overview 仍以 work_order_no + process_order_no + group 作為定位 production step 的優先依據。"
   - 請說明為何需要加入 process_order_no 作為判斷條件，目前資料表中的 process_order_no 欄位尚未建立關聯，僅為預留的擴充欄位。
   - 派工單的一個投入物可能對應多個批號，而不同批號會有不同效期。由於不同批號的投入物所產出的成品也必須具備相應的批號，因此 group 的設計目的在於對應並管理此類關係。然而，目前資料庫的資料尚未完整建立，暫時不考慮以 group 進行分組。請依此情境修正後端程式碼，確保邏輯正確。
2. 請在程式碼中補充註解，明確描述函式或欄位的用途、邏輯流程與限制條件，以利工程師後續維護與除錯。

## 程式修正回覆

| 項目 | 回覆與文件調整 |
|---|---|
| `process_order_no` 是否作為 production step 判斷條件 | 已依工程師說明修正。第一版不再以 `process_order_no` 作為 production step 的硬性定位條件，原因是目前資料表中的 `process_order_no` 尚未建立穩定關聯，若用於 input/output 配對，會造成合法 counterpart rows 被誤濾掉。 |
| `group` 是否作為 production step 分組條件 | 已依工程師說明修正。`group` 的設計方向可支援同一派工單中不同投入批號與相應產出批號的關係管理，但目前資料庫資料尚未完整建立，因此第一版暫不以 `group` 進行 production step 分組。 |
| 第一版 production step 範圍 | 第一版改以 `work_order_no` 作為 production step 的主要範圍。後端先取得同一工單的投入與產出資料，再依查詢方向套用批號路徑過濾：製成品 upstream 時，`outputItems[]` 只保留目前追溯中的製成品/在製品批號；原料 downstream 時，`inputItems[]` 只保留目前追溯中的原料/在製品批號。 |
| downstream 展開限制 | 原料 downstream 查詢時，production step 可顯示同一工單直接產出的在製品或製成品；但下一層 trace queue 只放入已由批號主檔或 `EOutputCategory` fallback 確認為 `EItemCategory.INPRODUCT` 的 output 批號。製成品 output 只作為目前 step 的終點，不再繼續往下游展開，避免回推到下游製成品的其他投入物。 |
| 已知限制 | 因第一版暫不使用 `group` 分組，若同一 `work_order_no` 同時混有多組尚未透過資料欄位可靠區隔的投入與產出，後端無法保證可在同一工單內切分每一組批號關係。此限制需待未來 `group` 或其他正式關聯欄位完成資料治理後再提升精準度。 |
| 程式註解 | 已於 `restserver/package/restserver/api/v2/trace.py` 的 production step 建立流程補充註解，明確說明 `process_order_no` 與 `group` 在第一版僅保留參數相容性，不用於分組與查詢過濾。 |


# 演算法修正V3
1. /api/v2/trace/batches/{batch_no}/overview 的 traceSteps[] 仍存在資料異常，請參考 CBatchRecord 演算法進行修正。
    - 案例一：查詢製成品批號 BN1526051503, stepId = "production:Z150515003::group_1",  回傳結果中 outputItems[] 為空值，預期應顯示製成品 BN1526051503 的相關資料。

    - 案例二：查詢原料批號 BN1126042901, stepId = "production:Z150514005::group_1", 回傳結果中 outputItems[] 為空值，預期應顯示製成品 BN1526051308 / BN1526051403 / BN1526051405 的相關資料。
      另有 stepId = "production:Z150515004::group_2"，此回傳資料並非由原料批號直接關聯，因此不需回傳。
   
## 演算法修正V3回覆

| 項目 | 回覆與文件調整 |
|---|---|
| CBatchRecord 演算法參考 | 已參考 `CBatchRecord` 由單據與批號建立追溯關係的方向；但依「程式修正」確認，第一版 overview 不再以 `work_order_no + process_order_no + group` 定位 production step，改以 `work_order_no` 作為主要範圍，並以目前追溯批號作為 input/output 顯示與下一層展開的過濾依據。 |
| 案例一 outputItems 空值 | 後端已補強：查詢製成品批號時，產出該製成品的 production step 必須保留查詢批號於 `outputItems[]`，不可因 counterpart 查詢、`group` 空白差異或 focus filtering 造成空陣列。 |
| 案例二 outputItems 空值 | 後端已補強：查詢原料批號時，若該原料或其直接產出的在製品被投入 production step，同一工單可確認的核心產出需回傳於 `outputItems[]`；不再因 `process_order_no` 或 `group` 缺漏、不一致而使 `outputItems[]` 變成空陣列。 |
| 非直接關聯資料排除 | `production:Z150515004::group_2` 這類非由查詢原料批號路徑直接展開而來的 step 不應回傳。後端只將目前 trace queue 中的原料或在製品批號作為下一層展開來源；`__next_trace_rows()` 於原料 downstream 情境只能回傳已確認為 `EItemCategory.INPRODUCT` 的 output rows。製成品、未知類別、其他類別或無法由批號主檔確認為在製品的 output rows 只保留於目前 step，不再放回 queue 展開下一層，因此不會從下游製成品反向展開其他非查詢原料或旁支在製品。 |
| production output 類別轉換 | 已補強：`production_data_input.category` 使用 `EItemCategory`，但 `production_data_output.category` 使用 `EOutputCategory` 或舊資料值，不可直接拿來與 `EItemCategory` 比對。後端建立 `traceSteps[].outputItems[]` 與判斷是否繼續 downstream 展開時，需優先以 output row 的 `batch_number` 查詢 `batch_number.itemCategory` 作為 API 使用的 `EItemCategory`；若批號主檔缺漏，才以 `EOutputCategory.INPRODUCT(1) -> EItemCategory.INPRODUCT(4)`、`EOutputCategory.PRODUCT(2) -> EItemCategory.PRODUCT(5)` 作為 fallback。 |
| 測試補強 | 已新增與保留 regression tests，確認製成品 step 的 `outputItems[]` 不空、原料往下游 step 可取得工單層級可確認的 output、同工單旁支 output 不會在製成品 upstream 查詢中混入，以及原料 downstream 追到製成品後不再展開下一層非直接 production step。 |

# 演算法修正V2
1. /api/v2/trace/batches/{batch_no}/overview 的 traceSteps[] 仍存在資料異常。
    - 以查詢製成品批號 BN1526051503(摩卡杏仁肉鬆煎捲_2022中秋版) 為例，回傳結果中 outputItems[] 為空值，預期應顯示製成品    BN1526051503 的相關資料。以下為資料結構範例：
    ```json
      {
          "stepId": "production:Z150515003::group_1",
          "stepTypeCode": "production",
          "eventTimestamp": 1778774400,
          "refCategory": 0,
          "refNo": "Z150515003",
          "statusCode": "complete",
          "riskLevelCode": "normal",
          "inputItems": [
              {
                  "itemNo": "SFE0003012",
                  "itemName": "摩卡杏仁肉鬆煎捲_2022中秋版",
                  "itemCategory": 4,
                  "batchNo": "BN1426050603",
                  "quantity": 633.53,
                  "unit": 3
              }
          ],
          "outputItems": [ 預期應顯示 BN1526051503 的相關資料 ]
      }
      ```
    - 以查詢原料批號 BN1126042901(糙米捲蛋黃味 (小) 2025年7月新價) 為例，回傳結果中 outputItems[] 為空值，預期應顯示製成品 BN1526051308 / BN1526051403 / BN1526051405  的相關資料。 以下為資料結構範例：
    ```json
       {
          "stepId": "production:Z150514005::group_1",
          "stepTypeCode": "production",
          "eventTimestamp": 1778688000,
          "refCategory": 0,
          "refNo": "Z150514005",
          "statusCode": "complete",
          "riskLevelCode": "normal",
          "inputItems": [
              {
                  "itemNo": "SFE0022004",
                  "itemName": "肉酥起司捲",
                  "itemCategory": 4,
                  "batchNo": "BN1426051301",
                  "quantity": 74.94,
                  "unit": 3
              }
          ],
          "outputItems": [預期應顯示製成品    BN1526051308 / BN1526051403 / BN1526051405  的相關資料]
      },
     ```
      若回傳資料並非由原料批號直接關聯，則不需回傳。例如
      ```json
      {
          "stepId": "production:Z150515004::group_2",
          "stepTypeCode": "production",
          "eventTimestamp": 1778774400,
          "refCategory": 0,
          "refNo": "Z150515004",
          "statusCode": "complete",
          "riskLevelCode": "normal",
          "inputItems": [
              {
                  "itemNo": "SFE0022001",
                  "itemName": "拌料_咖啡杏仁捲",
                  "itemCategory": 4,
                  "batchNo": "BN1426051505",
                  "quantity": 22.71,
                  "unit": 3
              }
          ],
          "outputItems": []
      },
    ```
   - 請參考 CBatchRecord 演算法，並評估是否可透過 work_order_no + process_order_no + group 的組合來限定 production step 範圍，以進行演算法修正。
2. 針對 /api/v2/trace/batches/{batch_no}/overview 的 traceSteps[] 
   - 請檢視並評估目前的資料結構，確認其是否能支援前端畫面依製程階層方式展開顯示。
   - 請檢視並評估當 traceStepTypeCode 為 receipt 或 sale 時，是否需要獨立存放於另一個陣列。
   
## 演算法修正V2回覆

| 項目 | 回覆與文件調整 |
|---|---|
| `outputItems[]` 空值問題 | 已確認 V2 問題核心不是 `traceSteps[]` 結構不足，而是 production step 查詢與過濾需要更精準處理。依後續「程式修正」確認，第一版改以 `work_order_no` 作為 production step 主要範圍，不再以 `process_order_no` 或 `group` 過濾 counterpart rows，避免合法產出被誤判為空。 |
| 製成品批號查詢 | 製成品查詢仍採 upstream。第一層 production step 必須顯示查詢製成品批號於 `outputItems[]`，並顯示直接投入的在製品/原料於 `inputItems[]`；下一層只沿直接投入批號往上游展開，不反向擴散到其他非查詢製成品。 |
| 原料批號查詢 | 原料查詢仍採 downstream。每層 production step 必須顯示目前追溯中的投入批號於 `inputItems[]`，並顯示同一工單可確認的在製品或製成品於 `outputItems[]`；下一層只沿已確認為在製品的產出批號往下游展開，不混入下游製成品的其他非查詢原料。 |
| 製程階層顯示 | 現有 `traceSteps[]` 可支援前端依製程階層展開顯示。每筆 `production` step 第一版代表一個 `work_order_no` 工單層級產製步驟，`inputItems[]` 與 `outputItems[]` 已在同一 step 中表達投入與產出關係；前端可依 step 順序與 input/output 批號關聯呈現階層。 |
| `receipt` / `sale` 是否獨立陣列 | 第一版不建議拆成另一個陣列。`receipt`、`production`、`sale` 都是同一批號追溯流程中的 step，維持在 `traceSteps[]` 可讓前端用同一種排序、時間軸與階層展開邏輯處理；若未來需要文件完整性或召回評估，再另行設計補充 payload。 |
| 測試補強 | 已新增 regression tests，覆蓋製成品 `outputItems[]` 不可空、原料往下游時 counterpart 欄位缺漏仍需回傳 `outputItems[]`、製成品 output 不再繼續 downstream 展開，以及在製品查詢起點不展開。 |

# 演算法修正
1. 針對 /api/v2/trace/batches/{batch_no}/overview
   - 目前暫不規劃"在製品"批號的追溯功能 
   - 製成品批號向下追溯，可從指定的製成品批號展開，逐層查詢其生產過程。
      - 投產追溯流程包含三個層級：
        1. 製成品批號 → 查詢起點，包含銷貨紀錄。
        2. 在製品批號 → 對應的中間產出。
        3. 原料批號 → 最終投入來源。
      - 僅取得與查詢製成品批號直接相關的投入與產出，不需追溯同一原料批號所產製出的其他非查詢製成品。
   - 原料批號向上追溯，可從指定的原料批號展開，逐層查詢其產製過程。
     - 產製追溯流程包含三個層級：
       1. 原料批號 → 查詢起點，包含進貨紀錄。
       2. 在製品批號 → 該原料投入後產出的中間產品。
       3. 製成品批號 → 由在製品投入產出的最終製成品。  
     - 僅顯示與查詢原料批號直接相關的在製品與製成品，不需追溯該製成品所投入的其他非查詢原料批號所產出的在製品。

2. /api/v2/trace/batches/{batch_no}/overview 的 traceSteps[] 仍存在資料異常。例如在查詢製成品批號時，回傳結果包含不屬於該製成品的投入物，請檢視演算法是否有誤。
   以查詢製成品批號 BN1526051503(摩卡杏仁肉鬆煎捲_2022中秋版) 為例，預期應得到以下結果：
     - 階層1 
       - input: BN1426050603_摩卡杏仁肉鬆煎捲_2022中秋版_633.53公斤	 
       - output: BN1526051503_摩卡杏仁肉鬆煎捲_2022中秋版_2246.00公斤
    - 階層2
      - input: BN1126040201_星巴克咖啡粉_2.84公斤	/ BN1126033102_苦甜黑可可鈕扣_232.19公斤	/ BN1426042701_熟杏仁角_100.84公斤	/ BN1426042702_灌餡_摩卡杏仁肉鬆捲_211.78公斤	
      - output:	BN1426050603_摩卡杏仁肉鬆煎捲_2022中秋版_	880.95公斤
    - 階層3
      - input: BN1126041302_美國加州藍鑽杏仁角 2026年1月新價_396.90公斤 
      - output: BN1426042701_熟杏仁角_387.68公斤	
    - 階層3
      - input: BN1126041703_2022原味煎捲CAS版 (5.5公分)_27.79	公斤	/ BN1126041501_豬肉鬆 2025年1月新價_142.00公斤	
      - output: BN1426042702_灌餡_摩卡杏仁肉鬆捲_332.53公斤	


## 演算法修正回覆

| 項目 | 回覆與文件調整 |
|---|---|
| 在製品批號查詢起點 | 已依本次演算法修正調整：第一版暫不規劃在製品批號作為查詢起點的追溯功能。若查詢批號為在製品，API 回傳批號 header 與空 `traceSteps[]`，並以 `traceStatusCode=unknown`、`riskCode=unknown` 表示本版暫不展開。 |
| 製成品批號追溯 | 已調整為製成品批號往上游路徑式追溯。每一層 production step 的 `outputItems[]` 只保留目前追溯中的製成品或在製品批號，`inputItems[]` 顯示產出該批號所需的核心投入批號；不展開同一原料批號可產出的其他非查詢製成品。 |
| 原料批號追溯 | 已調整為原料批號往下游路徑式追溯。每一層 production step 的 `inputItems[]` 只保留目前追溯中的原料或在製品批號，`outputItems[]` 顯示該批號投入後直接產出的核心批號；不反向展開下游製成品所投入的其他非查詢原料。 |
| traceSteps[] 資料異常 | 後端演算法需以 root itemCategory 決定追溯方向，並以 `work_order_no` 建立 production step 範圍；再依追溯方向過濾 input/output item 與下一層 queue，避免從製成品終點反向展開下游旁支資料。 |
| 效能補強 | 單次 overview 建立過程需快取 batch header、batch input/output、work order input/output 與 production data，降低重複查詢成本。 |


# 工程師提問V4
1. 針對 /api/v2/trace/batches/{batch_no}/overview 
   - 投產/產製追溯流程僅需該批號的進貨時間、製產時間與銷貨時間，以及各產製階段的投入物與產出物關係。當該批號出現問題時，應能追溯至何時購買、產製何產品以及何時銷貨。請評估 nodes[] 是否可簡化，並確認 nodes[] 與 edges[] 是否可整合為單一結構。

## 工程師回覆V4

| 項目 | 回覆與文件調整 |
|---|---|
| `nodes[]` / `edges[]` 是否可簡化 | 可簡化。依工程師提問 V4，第一版 overview 不再以 graph 結構回傳 `nodes[]` 與 `edges[]`，改為單一流程結構 `traceSteps[]`。每一個 step 直接包含事件時間、來源單據、投入物與產出物，前端不需再自行合併節點與連線。 |
| 投產/產製追溯重點 | Overview 第一版改以「進貨 / 生產 / 銷貨」三類流程步驟為主：`receipt` 表示何時購買或進貨、`production` 表示何時投產與產出何產品、`sale` 表示何時銷貨或出貨。 |
| 投入物與產出物關係 | 已新增 `traceSteps[].inputItems[]` 與 `traceSteps[].outputItems[]`。生產步驟中，投入物與產出物被放在同一筆 step 內，取代原本 `production_input` node、`production_output` node 與 edge 的組合。同一 step 內相同 `itemNo + batchNo + itemCategory + unit` 的投入或產出需彙整為單筆；投入物數量需以領料扣退料後的淨投入量呈現。 |
| 銷貨時間資料來源 | 若正式資料庫文件已確認銷貨或出貨資料來源，後端可建立 `stepTypeCode=sale` 的 step；若目前尚無穩定資料表或欄位，`sale` step 不建立，不推測不存在的銷貨資料。 |
| V3 graph 設計處理 | V3 的原始提問與回覆保留作為歷史 review 記錄；但正式 V1 proposal 以 V4 的 `traceSteps[]` 結構為準。`nodeTypeCode` 與 `relationTypeCode` 改列為 V1 不使用、V2 graph 擴充時再評估。 |

# 工程師提問V3
1. 針對 /api/v2/trace/batches/{batch_no}/overview 
   - 目前資料回傳時間過長且資料量過於龐大，導致效能不足。請評估是否能加速回傳時間，或提出其他可改善效能的方法。
   - 目前僅需列出 原料、在製品與製成品，物料與膠捲暫時不需要。
   - 請補充 nodeTypeCode 各數值的詳細說明。
  
## 工程師回覆V3

| 項目 | 回覆與文件調整 |
|---|---|
| Overview 回傳時間與資料量 | `/api/v2/trace/batches/{batch_no}/overview` 依 V3 先限制只處理原料、在製品、製成品三類核心批號；再依 V4 將正式回傳結構簡化為 `traceSteps[]`，降低前端與後端組圖成本。 |
| Overview 效能策略 | 後端應先以查詢批號建立 root，再以 `production_data_input` / `production_data_output` 查詢上下游批號集合；依「程式修正」確認，第一版 production step 以 `work_order_no` 為主要範圍，並於單次請求內快取已查詢的 batch header、batch input/output、work order input/output 與 production data，避免重複查詢。 |
| 展開限制 | 建議第一版設定防護上限：最大展開層數 5、最大核心批號數 100、最大 `traceSteps[]` 筆數 150；若超過上限，停止繼續展開並保留已確認流程，不建立推測資料。 |
| 物料與膠捲處理 | 若生產投入資料中存在物料(2)或膠捲(3)，第一版 overview 不列入 `traceSteps[].inputItems[]` / `traceSteps[].outputItems[]`；未來若前端需要包材追溯，再另行擴充。 |
| 查詢批號本身為物料或膠捲 | 若使用者直接查詢物料或膠捲批號，API 可回傳 `batch` header 與空的 `traceSteps[]`，並以 `traceStatusCode=unknown`、`riskCode=unknown` 表示第一版未展開此類追溯。 |
| `nodeTypeCode` 說明 | V3 原規劃的 `nodeTypeCode` 已依 V4 結論改為 V1 不使用；正式提案改以「5.6 traceStepTypeCode 詳細說明」描述 `receipt`、`production`、`sale`。 |

# 工程師提問V2
1. 針對 /api/v2/trace/dashboard，目前資料回傳時間過長，效能不足。請評估是否能加速回傳時間，或提出其他可改善效能的方法。
2. 針對 /api/v2/trace/batches/{batch_no}/overview 
   - 製成品向下追溯：請確認是否能追溯至原物料的投入並產出在製品，形成完整的投產追溯流程。
   - 原料向上追溯：請確認是否能追溯至原料的採購並產出在製品，形成完整的產製追溯流程。
   - 若目前設計並未支援上述追溯方式，請依此設計為主進行修正。
   - 請舉例說明原物料向上追溯與製成品向下追溯時，API 會回傳哪些資料。

## 工程師回覆V2

| 項目 | 回覆與文件調整 |
|---|---|
| `/api/v2/trace/dashboard` 效能 | Dashboard API 調整為「批號追溯清單摘要」用途，不展開單批號 overview 的 `traceSteps[]`，也不逐筆建立完整追溯流程。後端應採兩階段查詢：先依 `batch_number` 與 query 條件取得候選批號並完成 DB 層排序/分頁，再只針對本頁批號批次查詢庫存摘要、生產投入/產出存在性、品檢保留與最新事件時間。 |
| 庫存計算效能 | Dashboard 不應為所有批號呼叫完整 Warehouse Dashboard；僅需要 `currentQuantity`、主要 `warehouseNo/warehouseName` 與品檢保留訊號時，應以可重用的庫存快照 context / calculator 對本頁批號集合進行 bounded 查詢。若工程師認為目前 `CWarehouseInventoryContextBuilder` 對全量資料成本過高，建議再抽出批號集合專用的 snapshot helper。 |
| `/api/v2/trace/batches/{batch_no}/overview` 追溯方向 | 依本次演算法修正，單批號 overview 改為依查詢批號類別決定追溯方向：原料往下游、製成品往上游；在製品第一版暫不作為查詢起點展開。 |
| 製成品追溯到原物料 | 支援。當查詢製成品批號時，後端應先以 `production_data_output.batch_number` 找到產出此製成品批號的工單，再查詢同一 `work_order_no` 的投入批號；該 production step 的 `outputItems[]` 只保留目前追溯中的批號，避免旁支製成品混入。 |
| 原料追溯到採購與產出 | 支援。當查詢原料批號時，後端應以 `batch_number.refCategory/ref_no` 與 `goods_receipt_note` 或 `inventory_record` 建立採購/進貨/入庫來源步驟，再以 `production_data_input.batch_number` 找到使用此原料批號的工單，並查詢同一 `work_order_no` 的在製品或製成品產出批號；該 production step 的 `inputItems[]` 只保留目前追溯中的批號，下一層只沿在製品 output 展開。 |
| 查詢語意說明 | 本版不再從任一核心批號展開完整上下游。查詢原料批號時聚焦該原料產製路徑；查詢製成品批號時聚焦該製成品來源路徑；查詢在製品批號時暫不展開。 |
| 範例資料 | 已於本文件新增「5.3 追溯範例」說明原料批號與製成品批號查詢時，`batch` 與 `traceSteps[]` 會回傳哪些資料。 |

# 工程師提問

1. 請將 URL Path 由 `/api/v2/traceability/xxx` 更名為 `/api/v2/trace/xxx`。
2. 請將 `primaryRiskCode` 更名為 `riskCode`。
3. 請詳細說明「文件完整性」要顯示的內容有哪些。
4. 目前暫時不需提供「文件完整性」與「召回評估」功能，請簡化回傳欄位。
5. 目前以批號為進入點進行追溯：原料批號向下追溯，製成品批號向上追溯；並同步修改查詢條件。
6. 查詢條件暫不開放 `documentStatusCode`、`traceDirectionCode`、`traceStatusCode`、`riskLevelCode`；亦不開放 `period`，僅保留 `startDate` 與 `endDate`。
7. 此追溯功能是否支援單一原料批號可產出多個在製品（如拌料、灌餡等半成品），並由在製品再投入產出多個製成品？
8. 針對 `/api/v2/traceability/dashboard`
   - `records[].queryTypeCode`、`records[].queryValue` 應由前端自行記錄，不應由後端再回傳。
   - 請確認 `records[].supplierNo/supplierName` 與 `records[].customerNo/customerName` 是否會同時存在數值。若會，請具體舉例；若不會，請將欄位簡化為單一組。

## 工程師回覆

| 項目 | 回覆與文件調整 |
|---|---|
| URL Path | 已調整為 `/api/v2/trace/dashboard` 與 `/api/v2/trace/batches/{batch_no}/overview`。 |
| `primaryRiskCode` | 已更名為 `riskCode`，表示此筆追溯資料最主要的風險代碼。 |
| 文件完整性 | 原規劃的文件完整性是指 COA、溫度紀錄、收貨文件、品檢文件、生產文件、出貨文件等文件狀態。但依工程師確認，第一版暫不提供此功能，因此已移除 `documents[]`、`pendingDocumentCount`、`documentPendingCount`、`documentStatusCode` 與相關查詢條件。 |
| 召回評估 | 第一版暫不提供召回範圍與受影響客戶評估，因此已移除 `impactSummary`、`impactedQuantity`、`impactedCustomerCount`、出貨與召回相關欄位。 |
| 追溯入口 | 第一版以批號為唯一主要追溯入口。依本次演算法修正，overview 僅支援原料與製成品作為查詢起點：原料批號向下追溯；製成品批號向上追溯；在製品批號第一版不作為查詢起點展開，但可作為原料或製成品追溯路徑中的中間批號呈現；物料與膠捲暫不展開。 |
| 查詢條件 | 第一版只保留 `keyword`、`batchNo`、`itemCategory`、`itemNo`、`startDate`、`endDate`、`start`、`count` 與 `x-timezone`。不開放文件狀態、追溯方向、追溯狀態、風險等級與 period 快速區間查詢。 |
| 多層批號關係 | 支援。依 V4 結論，追溯流程以 `traceSteps[]` 表示；同一個 `production` step 可包含多筆 `inputItems[]` 與 `outputItems[]`。實作時需依查詢批號方向過濾 step 內容：原料查詢只保留目前追溯中的投入批號並往產出展開；製成品查詢只保留目前追溯中的產出批號並往投入展開，避免旁支批號混入。 |
| 查詢記錄欄位 | `queryTypeCode` 與 `queryValue` 屬於前端查詢 UI 狀態，不由後端回傳。 |
| 供應商與客戶欄位 | 第一版不在同一筆 dashboard record 同時回傳供應商與客戶兩組欄位，改為單一組 `partnerTypeCode`、`partnerNo`、`partnerName`。`partnerTypeCode` 可為 `supplier`、`customer`、`internal`、`unknown`。 |
| `refCategory` 用途 | `refCategory` 對應 API 回傳中的 `records[].refCategory`、`batch.refCategory`、`traceSteps[].refCategory`，用途是標示該筆資料關聯的來源單據類別，供後端追溯流程建構與前端未來 drill-down 導向使用。第一版僅回傳資料表已能確認的 code，不推測不存在的 code。 |
| 追溯鏈斷點 | 依工程師回覆，追溯流程持續進行至不可再追溯為止，並於此狀態下判定為 `broken`。 |

# TraceabilityWorkspaceScreen API 提案

> Status: API Proposal / Pending Engineer Review  
> Screen: `TraceabilityWorkspaceScreen`  
> Route: `/traceability`  
> Scope: V1 read-only Core  
> Design basis: `AGENTS.md`、`src/app/traceability/page.tsx`、`docs/spec/api/batches.md`、`docs/spec/database/index.md`

## 1. 畫面定位

「溯源中心」第一版定位為批號追溯 read-only 工作區，用於讓管理者從指定原料或製成品批號快速查看可確認的進貨時間、產製時間、銷貨時間，以及各產製階段的投入物與產出物關係。單批號 overview 依查詢批號類別決定追溯方向：原料批號往下游查看該原料投入後直接產出的在製品與製成品；製成品批號往上游查看產出該製成品所需的在製品與原料投入。第一版暫不支援在製品批號作為查詢起點。依工程師提問 V4，正式 V1 proposal 以 `traceSteps[]` 表示流程步驟，不再回傳 `nodes[]` 與 `edges[]`。依工程師提問 V3，第一版 overview 只展開原料(1)、在製品(4)、製成品(5)，物料(2)與膠捲(3)暫不展開。

| 畫面 | 主視角 | 本版邊界 |
|---|---|---|
| `BatchCenterScreen` | 料品 -> 批號 -> 倉庫分布 | 管理目前仍有庫存的批號、可用量、預留量、品檢保留量與效期風險。 |
| `TraceabilityWorkspaceScreen` | 批號 -> 投產流程 -> 進貨/產製/銷貨時間 | 以批號為入口檢視可確認的進貨、產製、銷貨流程，以及投入物與產出物關係。 |
| `WarehouseInventoryMovementLedgerScreen` | 庫存異動流水帳 | 下一版延伸畫面，本次不納入。 |

第一版不提供 POST、PUT、DELETE，不建立召回單、不修改文件狀態、不鎖定庫存、不變更 workflow task。後端只回傳 enum code、數值、時間戳與資料庫欄位；顯示文字與多國語言由前端處理。

## 2. V1 API 清單

| API | Method | 用途 |
|---|---|---|
| `/api/v2/trace/dashboard` | GET | 查詢溯源中心 KPI 與批號追溯清單。 |
| `/api/v2/trace/batches/{batch_no}/overview` | GET | 查詢單一批號的批號資訊與 `traceSteps[]` 投產/產製追溯流程。 |

> 工程師確認前，本文件為 API 提案；確認後才整合至 `docs/spec/api/` 正式 API 文件並進行後端實作。

## 3. 共用 Query Parameters / Header

| Parameter / Header | Type | Required | Description |
|---|---|---:|---|
| `keyword` | String | No | 批號、料號、品名、來源單號、工單號、供應商或客戶關鍵字。 |
| `itemCategory` | Integer | No | 料品品項類別 code；第一版 Dashboard 僅支援原料(1)與製成品(5)，未提供時預設查詢原料與製成品；前端負責顯示文字。 |
| `itemNo` | String | No | 料品 no。 |
| `batchNo` | String | No | 批號。若提供，dashboard 以此批號為主要查詢條件。 |
| `startDate` | String | No | 批號建立日期查詢起日，格式 `YYYY-MM-DD`；需與 `endDate` 同時提供。 |
| `endDate` | String | No | 批號建立日期查詢迄日，格式 `YYYY-MM-DD`；需與 `startDate` 同時提供。 |
| `start` | Integer | No | 分頁起點，預設 0；負值視為 0。 |
| `count` | Integer | No | 回傳筆數，預設 50，最大 100。 |
| `x-timezone` | Header String | No | 前端顯示偏好的 IANA timezone；後端不以此改寫資料庫保存的 UTC timestamp。 |

## 4. GET `/api/v2/trace/dashboard`

### 4.1 Success Response Data

```json
{
  "serverTimestamp": "Integer",
  "summary": {
    "traceableBatchCount": "Integer",
    "completeTraceRate": "Float",
    "brokenTraceCount": "Integer",
    "highRiskTraceCount": "Integer"
  },
  "records": [
    {
      "traceId": "String",
      "traceDirectionCode": "String",
      "itemNo": "String",
      "itemName": "String",
      "itemCategory": "Integer",
      "itemSubCategory": "Integer",
      "itemType": "Integer",
      "batchNo": "String",
      "refCategory": "Integer",
      "refNo": "String",
      "partnerTypeCode": "String",
      "partnerNo": "String",
      "partnerName": "String",
      "workOrderNo": "String",
      "warehouseNo": "String",
      "warehouseName": "String",
      "currentQuantity": "Float",
      "unit": "Integer",
      "traceStatusCode": "String",
      "riskLevelCode": "String",
      "riskCode": "String",
      "latestEventTimestamp": "Integer"
    }
  ],
  "total": "Integer",
  "start": "Integer",
  "count": "Integer"
}
```

### 4.2 Field Description

| Field Path | Type | Description | Source / Enum |
|---|---|---|---|
| `serverTimestamp` | Integer | API 回應建立時間，UTC timestamp。 | 系統時間 |
| `summary.traceableBatchCount` | Integer | 查詢條件內可建立追溯索引的批號數。 | `batch_number`、追溯資料彙總 |
| `summary.completeTraceRate` | Float | `traceStatusCode=complete` 的批號比例，百分比數值取至小數點第 2 位。 | `records[].traceStatusCode` |
| `summary.brokenTraceCount` | Integer | `traceStatusCode=broken` 的追溯紀錄數。 | 追溯鏈判斷結果 |
| `summary.highRiskTraceCount` | Integer | `riskLevelCode=high_risk` 的追溯紀錄數。 | 風險彙總 |
| `records[].traceId` | String | 前端列表用穩定識別值，建議由批號與主要來源單號組成。 | 後端組合 |
| `records[].traceDirectionCode` | String | 後端依批號料品類別推導的追溯方向 code；前端負責顯示文字。 | `upstream`、`downstream`、`both` |
| `records[].itemNo` | String | 料品 no。 | `batch_number.item_no` |
| `records[].itemName` | String | 料品名稱；無值時回傳空字串。 | `batch_number.item_name` |
| `records[].itemCategory` | Integer | 料品品項類別 code。 | `batch_number.itemCategory` |
| `records[].itemSubCategory` | Integer | 料品品項子類別 code。 | `batch_number.itemSubCategory` |
| `records[].itemType` | Integer | 料品型態 code。 | `batch_number.itemType` |
| `records[].batchNo` | String | 批號。 | `batch_number.no` |
| `records[].refCategory` | Integer | 此批號主要來源或關聯單據類別 code，用於追溯流程與前端 drill-down。 | `batch_number.refCategory` 或可確認來源文件 |
| `records[].refNo` | String | 此批號主要來源或關聯單據 no。 | `batch_number.ref_no` 或可確認來源文件 |
| `records[].partnerTypeCode` | String | 此追溯紀錄的主要關聯對象類型 code。 | `supplier`、`customer`、`internal`、`unknown` |
| `records[].partnerNo` | String | 主要關聯對象 no；無值時回傳空字串。 | 供應商、客戶或內部來源資料 |
| `records[].partnerName` | String | 主要關聯對象名稱；無值時回傳空字串。 | 供應商、客戶或內部來源資料 |
| `records[].workOrderNo` | String | 關聯工單 no；無關聯時回傳空字串。 | `production_data` |
| `records[].warehouseNo` | String | 目前主要庫存所在倉庫 no；無庫存或非庫存情境時回傳空字串。 | 庫存快照 |
| `records[].warehouseName` | String | 目前主要庫存所在倉庫名稱；無資料時回傳空字串。 | `ship_wh_alias.displayName`、庫存紀錄 fallback |
| `records[].currentQuantity` | Float | 此批號目前庫存數量，取至小數點第 2 位。 | `CWarehouseInventorySnapshotCalculator` |
| `records[].unit` | Integer | 數量單位 code；前端負責顯示文字。 | `batch_number.unit` |
| `records[].traceStatusCode` | String | 追溯完整性狀態 code；前端負責顯示文字與 tone。 | `complete`、`broken`、`unknown` |
| `records[].riskLevelCode` | String | 此追溯紀錄風險等級 code。 | `normal`、`attention`、`high_risk` |
| `records[].riskCode` | String | 此追溯紀錄主要風險 code。 | `normal`、`broken_chain`、`expired`、`quality_hold`、`unknown` |
| `records[].latestEventTimestamp` | Integer | 此追溯紀錄最近一筆事件時間；無資料時回傳 0。 | `inventory_record`、production、workflow |
| `total` | Integer | 套用篩選後的紀錄總筆數。 | 查詢結果 |
| `start` | Integer | 本次分頁起點。 | Query parameter |
| `count` | Integer | 本次回傳筆數。 | Query parameter / 實際筆數 |

`records[]` 陣列本身不另列說明。API 不回傳前端顯示用繁中文字串，例如 `traceStatusName`、`riskLabel`。

## 5. GET `/api/v2/trace/batches/{batch_no}/overview`

### 5.1 Success Response Data

```json
{
  "serverTimestamp": "Integer",
  "batch": {
    "batchNo": "String",
    "itemNo": "String",
    "itemName": "String",
    "itemCategory": "Integer",
    "itemSubCategory": "Integer",
    "itemType": "Integer",
    "unit": "Integer",
    "validDate": "Integer",
    "validDays": "Integer",
    "refCategory": "Integer",
    "refNo": "String",
    "traceDirectionCode": "String",
    "traceStatusCode": "String",
    "riskLevelCode": "String",
    "riskCode": "String"
  },
  "traceSteps": [
    {
      "stepId": "String",
      "stepTypeCode": "String",
      "eventTimestamp": "Integer",
      "refCategory": "Integer",
      "refNo": "String",
      "statusCode": "String",
      "riskLevelCode": "String",
      "inputItems": [
        {
          "itemNo": "String",
          "itemName": "String",
          "itemCategory": "Integer",
          "batchNo": "String",
          "quantity": "Float",
          "unit": "Integer"
        }
      ],
      "outputItems": [
        {
          "itemNo": "String",
          "itemName": "String",
          "itemCategory": "Integer",
          "batchNo": "String",
          "quantity": "Float",
          "unit": "Integer"
        }
      ]
    }
  ]
}
```

### 5.2 Field Description

| Field Path | Type | Description | Source / Enum |
|---|---|---|---|
| `serverTimestamp` | Integer | API 回應建立時間，UTC timestamp。 | 系統時間 |
| `batch.batchNo` | String | 批號。 | `batch_number.no` |
| `batch.itemNo` | String | 料品 no。 | `batch_number.item_no` |
| `batch.itemName` | String | 料品名稱；無值時回傳空字串。 | `batch_number.item_name` |
| `batch.itemCategory` | Integer | 料品品項類別 code。 | `batch_number.itemCategory` |
| `batch.itemSubCategory` | Integer | 料品品項子類別 code。 | `batch_number.itemSubCategory` |
| `batch.itemType` | Integer | 料品型態 code。 | `batch_number.itemType` |
| `batch.unit` | Integer | 單位 code；前端負責顯示文字。 | `batch_number.unit` |
| `batch.validDate` | Integer | 批號有效期限 UTC timestamp；無資料時回傳 0。 | `batch_number.validDate` |
| `batch.validDays` | Integer | 批號有效天數；無資料時回傳 0。 | `batch_number.validDays` |
| `batch.refCategory` | Integer | 批號原始來源單據類別 code，用於追溯流程與前端 drill-down。 | `batch_number.refCategory` |
| `batch.refNo` | String | 批號原始來源單據 no。 | `batch_number.ref_no` |
| `batch.traceDirectionCode` | String | 後端依批號料品類別推導的追溯方向 code。 | `upstream`、`downstream`、`both` |
| `batch.traceStatusCode` | String | 此批號追溯完整性狀態 code。 | `complete`、`broken`、`unknown` |
| `batch.riskLevelCode` | String | 此批號追溯風險等級 code。 | `normal`、`attention`、`high_risk` |
| `batch.riskCode` | String | 此批號主要追溯風險 code。 | `normal`、`broken_chain`、`expired`、`quality_hold`、`unknown` |
| `traceSteps[].stepId` | String | 追溯流程步驟唯一識別值，供前端列表 key 使用。 | 後端組合 |
| `traceSteps[].stepTypeCode` | String | 流程步驟類型 code；用於區分進貨、產製與銷貨。 | `receipt`、`production`、`sale` |
| `traceSteps[].eventTimestamp` | Integer | 此流程步驟發生時間 UTC timestamp；例如進貨時間、生產時間或銷貨時間。 | 來源資料表 |
| `traceSteps[].refCategory` | Integer | 此流程步驟關聯單據類別 code。 | 來源資料表 |
| `traceSteps[].refNo` | String | 此流程步驟關聯單號，例如進貨單號、工單號或銷貨/出貨單號。 | 來源資料表 |
| `traceSteps[].statusCode` | String | 此流程步驟狀態 code；前端負責顯示文字。 | `complete`、`pending`、`blocked`、`missing`、`unknown` |
| `traceSteps[].riskLevelCode` | String | 此流程步驟風險等級 code。 | `normal`、`attention`、`high_risk` |
| `traceSteps[].inputItems[].itemNo` | String | 此步驟投入料品 no；進貨步驟可為空陣列。 | 來源資料表 |
| `traceSteps[].inputItems[].itemName` | String | 此步驟投入料品名稱；無資料時回傳空字串。 | 來源資料表 |
| `traceSteps[].inputItems[].itemCategory` | Integer | 此步驟投入料品品項類別 code。 | `EItemCategory` |
| `traceSteps[].inputItems[].batchNo` | String | 此步驟投入批號；無批號時回傳空字串。 | 來源資料表 |
| `traceSteps[].inputItems[].quantity` | Float | 此步驟實際投入數量，取至小數點第 2 位；以 `production_data_input.action=1` 領料數量加總扣除 `action=2` 退料數量加總後回傳，若淨投入量為 0 則不回傳該投入項目。 | 來源資料表 |
| `traceSteps[].inputItems[].unit` | Integer | 此步驟投入單位 code。 | 來源資料表 |
| `traceSteps[].outputItems[].itemNo` | String | 此步驟產出或銷貨料品 no。 | 來源資料表 |
| `traceSteps[].outputItems[].itemName` | String | 此步驟產出或銷貨料品名稱；無資料時回傳空字串。 | 來源資料表 |
| `traceSteps[].outputItems[].itemCategory` | Integer | 此步驟產出或銷貨料品品項類別 code。 | `EItemCategory` |
| `traceSteps[].outputItems[].batchNo` | String | 此步驟產出或銷貨批號；無批號時回傳空字串。 | 來源資料表 |
| `traceSteps[].outputItems[].quantity` | Float | 此步驟產出或銷貨數量，取至小數點第 2 位；同一 step 內相同料品、批號、品項類別與單位需加總為單筆。 | 來源資料表 |
| `traceSteps[].outputItems[].unit` | Integer | 此步驟產出或銷貨單位 code。 | 來源資料表 |

`traceSteps[]` 陣列本身不另列說明。API 不回傳前端顯示用繁中文字串，例如 `stepTypeName`、`statusName` 或 `riskLabel`。

### 5.3 追溯範例

#### 5.3.1 原物料批號查詢範例

查詢：

```txt
GET /api/v2/trace/batches/RM-BATCH-001/overview
```

假設 `RM-BATCH-001` 是由採購進貨產生，後續投入 `WO-0001` 產出在製品 `WIP-BATCH-001`，再由 `WO-0002` 產出製成品 `FG-BATCH-001`，API 應回傳：

| Payload 區塊 | 回傳內容 |
|---|---|
| `batch` | `batchNo=RM-BATCH-001`、原料品項資料、`refCategory/refNo` 指向採購進貨或入庫來源、`traceDirectionCode=downstream`。 |
| `traceSteps[]` | 一筆 `receipt` step 表示原料何時進貨；一筆 `production` step 表示 `WO-0001` 投入 `RM-BATCH-001` 並產出 `WIP-BATCH-001`；另一筆 `production` step 表示 `WO-0002` 投入 `WIP-BATCH-001` 並產出 `FG-BATCH-001`；若銷貨/出貨資料來源已確認，再建立一筆 `sale` step 表示製成品何時銷貨。 |

#### 5.3.2 製成品批號查詢範例

查詢：

```txt
GET /api/v2/trace/batches/FG-BATCH-001/overview
```

假設 `FG-BATCH-001` 由 `WO-0002` 產出，投入來源為 `WIP-BATCH-001`，而 `WIP-BATCH-001` 由 `WO-0001` 使用原料批號 `RM-BATCH-001` 產出，API 應回傳：

| Payload 區塊 | 回傳內容 |
|---|---|
| `batch` | `batchNo=FG-BATCH-001`、製成品品項資料、製成品批號來源工單、`traceDirectionCode=upstream`。 |
| `traceSteps[]` | 依時間排序回傳 `receipt`、`production`、`production`、`sale` 等流程步驟；每筆 `production` step 直接列出加總後的 `inputItems[]` 與 `outputItems[]`，因此可看出製成品由哪個在製品投入、該在製品又由哪些原料投入產出。 |

> 以上範例僅描述資料結構與流程關係。若某個採購、入庫、投入、產出或銷貨步驟在資料庫中不存在，API 不建立虛構 step；該追溯鏈段停止展開，並依規則反映於 `traceStatusCode` 與 `riskCode`。

### 5.3.3 第一版追溯範圍限制

依工程師提問 V3，單批號 overview 第一版只列出核心投產追溯所需的原料、在製品與製成品：

| itemCategory | 類別 | Overview V1 處理方式 |
|---:|---|---|
| 1 | 原料 | 可建立 `receipt` step，並往下追溯至使用此原料的 `production` step、在製品與製成品。 |
| 2 | 物料 | 目前暫不列入 `traceSteps[]` 的 `inputItems[]` 或 `outputItems[]`；未來若需要包材追溯再擴充。 |
| 3 | 膠捲 | 暫不列入 `traceSteps[]`；未來若需要包材追溯再擴充。 |
| 4 | 在製品 | 第一版暫不作為查詢起點展開；若在原料或製成品追溯路徑中出現，仍可作為中間批號呈現。 |
| 5 | 製成品 | 可往上追溯至在製品與原料投入，若銷貨/出貨資料來源已確認，可往下呈現 `sale` step。 |

若查詢批號本身為物料或膠捲，API 不回傳 404，因為批號確實存在；但第一版可回傳 `batch` header，並讓 `traceSteps[]` 為空陣列，`traceStatusCode=unknown`、`riskCode=unknown`，表示此類批號暫不納入本版追溯流程展開。

## 5.4 Dashboard 效能設計調整

`GET /api/v2/trace/dashboard` 第一版需避免做完整追溯圖展開。建議後端實作以以下流程為準：

1. 以 `batch_number` 作為主查詢來源，第一版 Dashboard 預設先限定 `itemCategory in (1, 5)` 的原料與製成品批號；若指定其他 `itemCategory`，回傳空清單，再套用 `keyword`、`itemNo`、`batchNo`、`startDate`、`endDate`。
2. 在 DB 層完成初步排序與分頁，先取得本頁批號集合。
3. 僅針對本頁批號集合批次查詢：
   - `inventory_record` 最新事件與入出庫存在性。
   - `production_data_input` / `production_data_output` 是否有投入/產出關聯與第一筆工單 no。
   - `warehouse_quality_hold` 是否有品檢保留。
   - 必要的目前庫存摘要。
4. Dashboard 只計算 `records[]` 清單欄位與 `summary`，不建立 `traceSteps[]`。
5. 若 summary 需要全量統計，應以聚合查詢或 bounded query 完成，不得逐批號呼叫 overview。
6. 若資料量仍大，建議工程師評估新增或確認以下索引：
   - `batch_number(no)`、`batch_number(item_no)`、`batch_number(itemCategory, date)`、`batch_number(refCategory, ref_no)`。
   - `inventory_record(batchNumber, date)`。
   - `production_data_input(batch_number, work_order_no)`。
   - `production_data_output(batch_number, work_order_no)`。
   - `warehouse_quality_hold(batchNumber, date)`。

## 5.5 Overview 效能設計調整

`GET /api/v2/trace/batches/{batch_no}/overview` 第一版需避免一次展開過大的追溯流程。建議後端實作以以下流程為準：

1. 先查詢 root batch，若 root batch 的 `itemCategory` 不是原料(1)或製成品(5)，回傳 root `batch` header 與空 `traceSteps[]`，不再展開；在製品(4)第一版亦不作為查詢起點。
2. 使用 BFS 或受控 DFS 找出需要追溯的主線批號集合。每次以批號找到相關 input/output row 後，必須保留該 row 的 `work_order_no` 作為下一步查詢 production step 的範圍；`process_order_no` 與 `group` 第一版僅保留資料欄位，不作為分組條件。
3. 每次取得上下游批號後，先查詢 `batch_number` header，僅保留 `itemCategory in (1, 4, 5)` 的批號；物料(2)、膠捲(3)不建立 `traceSteps[]` item。
4. 以流程步驟彙整資料：採購/進貨來源建立 `receipt` step；同一 `work_order_no` 的投入與產出合併為一筆 `production` step；已確認的銷貨/出貨來源建立 `sale` step。
5. 製成品往上游追溯時，`production` step 的 `outputItems[]` 只保留目前追溯中的批號，下一層 queue 只加入該 step 的核心 `inputItems[]`。
6. 原料往下游追溯時，`production` step 的 `inputItems[]` 只保留目前追溯中的批號，下一層 queue 只加入該 step 的核心 `outputItems[]`。
7. `production` step 的 `inputItems[]` 與 `outputItems[]` 需依 `itemNo + batchNo + itemCategory + unit` 彙整；投入物需以 `production_data_input.action=1` 領料加總扣除 `action=2` 退料加總後回傳，淨投入量為 0 的投入項目不回傳、不加入下一層 trace queue，產出物依 `production_data_output.count` 加總。
8. 若同一 `work_order_no` 因多個追溯批號被重複命中同一 `stepId`，需將新的 focus `inputItems[]` / `outputItems[]` 合併至既有 step；相同 key 的 output 不再次累加，避免共同產出製成品被重複計算。
9. overview 建立過程需使用單次請求內快取，避免同一批號、同一 work order 或同一 production data 重複查詢。
10. 庫存與品檢資料僅用於判斷 `traceStatusCode`、`riskLevelCode`、`riskCode`，不再作為獨立 step 回傳。
11. 建議第一版防護上限：
   - `maxDepth=5`：最多展開 5 層上下游關係。
   - `maxBatchCount=100`：最多納入 100 個核心批號。
   - `maxTraceStepCount=150`：最多建立 150 筆 `traceSteps[]`。
12. 若達到防護上限，停止後續展開；已確認的 `traceSteps[]` 仍回傳，不建立推測流程。
13. 若資料量仍大，建議工程師確認或新增以下索引：
   - `batch_number(no, itemCategory)`。
   - `production_data_input(batch_number, work_order_no)`。
   - `production_data_output(batch_number, work_order_no)`。
   - `production_data_input(work_order_no)`。
   - `production_data_output(work_order_no)`。
   - `inventory_record(batchNumber, date)`。
   - `warehouse_quality_hold(batchNumber, date)`。

## 5.6 traceStepTypeCode 詳細說明

| traceStepTypeCode | 流程語意 | 建立時機 | 第一版備註 |
|---|---|---|---|
| `receipt` | 進貨或收貨步驟，回答「此批號何時購買或進貨」。 | 原料批號的 `batch_number.refCategory/ref_no` 可對應 `goods_receipt_note`，或可確認為採購/進貨來源時建立。 | `inputItems[]` 可為空，`outputItems[]` 放入進貨形成的批號。 |
| `production` | 產製步驟，回答「此工單投入哪些批號，產出哪些在製品或製成品」。 | 同一 `work_order_no` 可從 `production_data_input` 與 `production_data_output` 取得投入與產出時建立。 | `inputItems[]` 與 `outputItems[]` 需依查詢方向套用批號路徑過濾；`process_order_no` 與 `group` 待資料關聯完整後再納入更細分組。 |
| `sale` | 銷貨或出貨步驟，回答「此批號何時銷貨或出貨」。 | 正式資料庫文件確認銷貨/出貨資料來源，且可與批號或製成品建立關聯時建立。 | 目前若資料來源尚未確認，不建立 `sale` step，不推測不存在的銷貨資料。 |

## 6. Enum Code 建議

| Enum | Values |
|---|---|
| `traceDirectionCode` | `upstream`、`downstream`、`both` |
| `traceStatusCode` | `complete`、`broken`、`unknown` |
| `riskLevelCode` | `normal`、`attention`、`high_risk` |
| `riskCode` | `normal`、`broken_chain`、`expired`、`quality_hold`、`unknown` |
| `partnerTypeCode` | `supplier`、`customer`、`internal`、`unknown` |
| `traceStepTypeCode` | `receipt`、`production`、`sale` |

若工程師確認後進入實作，跨檔共用 enum 應集中定義於 `restserver/package/common/common.py`。

## 7. Database Tables Used

| Table | Purpose |
|---|---|
| `batch_number` | 批號主檔、料品資訊、原始來源單據、效期與單位。 |
| `inventory_record` | 入出庫、庫存異動與批號流向補充；第一版 overview 不作為獨立 step 回傳。 |
| `inventory_item_month_statistic` / `inventory_delta` | 目前庫存快照計算來源；應重用既有 Warehouse 快照邏輯。 |
| `production_data` | 工單、製程與生產事件主資料。 |
| `production_data_input` | 原料、在製品或製成品批號投入製程關聯；第一版 overview 不將物料與膠捲投入列入 `traceSteps[]`。 |
| `production_data_output` | 在製品/製成品批號產出關聯。 |
| `goods_receipt_note` | 採購進貨來源、供應商與收貨文件關聯。 |
| `warehouse_quality_hold` | 品檢保留、放行或阻塞資訊；用於風險判斷，不作為獨立 step 回傳。 |

若正式資料庫文件中尚未提供出貨、銷貨或客戶流向資料表的穩定欄位，第一版不得推測不存在的欄位；召回評估與客戶流向留待下一版規劃。

## 8. 工程師待確認項目

| 項目 | 需要確認原因 | 工程師回覆 |
|---|---|---|
| 出貨/客戶流向資料來源 | 召回範圍需要判斷已出貨數量與受影響客戶；目前第一版暫不納入。 | 目前暫不規劃設計「召回」的功能。 |
| 文件完整性資料來源 | COA、溫度紀錄、品檢文件、出貨文件若未有正式文件表，第一版不應推測。 | 目前暫不規劃設計「文件完整性」的顯示。 |
| `refCategory` code 對照 | `refCategory` 對應 API 回傳中的來源單據類別，需確認正式 code 對照。 | `refCategory` 對應 `records[].refCategory`、`batch.refCategory`、`traceSteps[].refCategory`；用途為標示資料來源單據類別與支援後續 drill-down。 |
| 追溯鏈斷點判斷 | 若缺少必要來源文件或投入/產出關聯，需確認是否判定為 `broken`。 | 追溯流程持續進行至不可再追溯為止，並於此狀態下判定為 `broken`。 |
