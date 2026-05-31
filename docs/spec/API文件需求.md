請依據以下來源進行 REST API 分析與文件化：

1. 已產出的資料庫說明文件（docs/spec/database/index.md）
2. restserver/ 目錄下所有 Python API 程式碼

---

## 1. 輸出位置
docs/spec/api/index.md
若已存在 index.md, 改名為 index_YYYYMMDD.md


## 2. 文件架構

使用 Markdown（.md），需符合以下結構：

### (1) 單一入口文件（index.md）

用途：

- 僅作 所有API group 導覽（Navigation）, 提供 anchor link（可跳轉）
- 不包含 Request / Response 細節

禁止：

- 不可放 API 詳細內容
- 不可放 Business Logic

---

### (2) API Module 分組規則

API 必須依照以下規則分類：

- 依據 *_uri.py 檔案名稱進行分類
- 每個 *_uri.py 視為一個 API module

範例：

- auth_uri.py → Auth API Group
- user_uri.py → User API Group

---

### (3) 排序規則

所有 API module 必須依：

- *_uri.py 檔名
- A → Z 排序
- 每個 *_uri.py 必須產生獨立 md 文件

範例：

- auth_uri.py      → auth.md 
- employee_uri.py  → employee.md 
- inventory_uri.py → inventory.md


---
### (4) Module 文件結構

每個 Module 文件（{module}.md）必須包含：

1. API Summary（索引）Anchor Link
2. Individual API Specification（詳細）

API Summary 不得獨立成檔案。


## 3. API Summary
   規則

   - API Summary 僅作「索引」，不得描述細節。
   - 使用表格說明, 需列出：      
      - URL 
      - Method
      - Description
      - Status
      - Review Note
  
   範例：

   | URL | Method | Description | Status | Review Note |
   |----------|----------|----------------|------|------|
   |/user/login|POST|使用帳號密碼登入| OK | OK |


   #### (1) Description欄位
      產生規則優先順序：
      1. Python class/docstring
      2. Python function/docstring
      3. validate schema欄位名稱與程式流程推導
      4. 若無法明確判斷 → Need Review

   #### (2) 狀態欄位 和 Review Note欄位

   請依據以下規則判定欄位狀態：

   - OK（必須同時符合）
      - route 存在於 *_uri.py
      - HTTP method 可從 decorator 明確取得
      - Request schema（若有 validate / schema）可明確解析
      - Response 結構可從 code 推導或明確 return

   - Need Review  （任一符合）
      - 無法從 code 明確找到 request schema
      - response 結構為 dynamic / dict 拼接
      - business logic 需推測
      - database relation 不明確
      - 欄位語意不足


   範例：

   | URL | 狀態 |  Review Note |
   |------|------|------|
   | /user/login | OK | OK |
   | /user/login | Need Review | 無法確認用途 | 


## 4. Individual API Specification
   - URL
   - HTTP Method
   - Description
   - Request Header
   - Query Parameters (若有)
   - Request Body
   - Success Response Data
   - Failed Response Data
   - Processing Flow (程式處理流程)
   - Database Tables Used

      ### 每個 API 必須包含

      ---

      ### (1) 基本資訊
      
      需列出：
      - URL
      - Method
      - Description

      範例:
      | URL | Method | Description |
      |----------|----------|----------------|
      |/user/login|POST|使用帳號密碼登入|
      
         Description欄位產生規則優先順序：
         1. Python class/docstring
         2. Python function/docstring
         3. validate schema欄位名稱與程式流程推導
         4. 若無法明確判斷 → Need Review

      ---


      ### (2) Request Header

      需列出：
      - Content-Type
      - token（若有）

      範例:
      | Header | Description 
      |----------|----------|
      |Content-Type|application/json|
      |x-auth-token|存取金鑰|

      ---

      ### (3) Query Parameters
      若無 → 明確標示 None

      需列出：
      - Parameter 
      - Type
      - Required
      - Description

      範例:
      | Parameter | Type | Required | Description 
      |----------|----------|------|-----|
      |username|string|YES|登入帳號|


      ---

      ### (4) Request Body

      Request Body 規則：

      1. Request Body Structure
         - 使用 JSON code block 呈現完整階層結構。
         - 每個欄位需保留欄位名稱。
         - Value 使用資料型態名稱（String、Integer、Boolean、Array、Object）。

         
      2. Request Body Field Description
         - 使用表格說明欄位, 需列出：   
            - Field Path 
            - Type
            - Required
            - Description
            - Enum  (日後延伸先保留欄位) 
         - 欄位名稱採用完整路徑格式：
         payload.user.employee.no

      3. 當 Object 超過 3 層巢狀時：
         - 保留完整 JSON Structure。
         - 表格僅列出實際欄位，不列出中繼 Object。

      範例:

      ```json
         {
            "registerNo": "String",      
            "total": "Integer",         
            "results": [
               {
                  "devDateTimestamp ": "Integer",  
                  "devGroupNo": "String",        
                  "devComment": "String",      
                  "itemBatchNo": [
                  {
                     "batchNo": "String",       
                     "serialNos": [
                        {
                           "serialNo": "String", 
                           "value": "Float"      
                        }
                     ]
                  }
                  ]
               }
            ]
         }
      ```
      | Field Path | Type | Required | Description | Enum |
      |----------|----------|------|-----|---|
      |results[].itemBatchNo[].batchNo|string|YES|料品品項批號||
      |results[].itemBatchNo[].batchNo[].serialNo|string|YES|料品品項批號流水號||

      ---

      ### (5) Success Response Data
      規則：

      1. Response Data Structure
         - 使用 JSON code block 呈現完整階層結構。
         - 每個欄位需保留欄位名稱。
         - Value 使用資料型態名稱（String、Integer、Boolean、Array、Object）。
         
      2. Response Field Description
         - 使用表格說明欄位, 需列出：
            - Field Path 
            - Type          
            - Description
            - Enum (日後延伸先保留欄位) 
         - 欄位名稱採用完整路徑格式：
         payload.user.employee.no

      3. 當 Object 超過 3 層巢狀時：
         - 保留完整 JSON Structure。
         - 表格僅列出實際欄位，不列出中繼 Object。

         範例:
         ```json
            {
               "code": "Integer",
               "message": "String",
               "data": {
                  "token": "String"
               }
            }
         ```

         | Field Path | Type | Description |Enum|
         |----------|----------|------|---|
         |data.token|string|存取金鑰||

      ###  (6)  Failed Response Data
      規則：
      - 使用表格說明欄位, 需列出：
         - Field Path 
         - Type          
         - Description
         - Enum (日後延伸先保留欄位) 

      範例：
        | Field Path | Type | Description |Enum|
        |----------|----------|------|---|
        |code|Interger|API回傳值||



      ###  (7) Processing Flow
      規則：

      - 必須依據 Python code execution path
      - 不可推測未出現在 code 的步驟

      範例：
      ```
         1.驗證 request body schema
         2.查詢 member 資料表
         3.使用 Argon2 驗證密碼
         4.產生 UUID token
         5.新增 session 資料
         6.回傳 token 與 user 資訊
      ```

      ###  (8) Database Tables Used
      規則：
      - 使用表格說明, 需列出：  
         - Table
         - Purpose          
      
      - 必須從 ORM / SQLAlchemy / query 推導
      - 不可猜測
      - 不可補充不存在關聯

      範例：
      | Table | Purpose| 
      |----------|------|
      |member|驗證帳號|
         
## 5. 文件處理規則

1. 所有內容必須來自程式碼或資料庫文件。
2. 不得推測、補完或自行設計 API。
3. 無法確認之內容必須標示 Need Review。
4. Need Review 優先於推測。
5. 文件內容必須可追溯至實際程式碼。
6. 若程式碼與資料庫文件衝突，以程式碼為主，並標示 Need Review。
