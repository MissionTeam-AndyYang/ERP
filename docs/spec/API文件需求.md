請依據以下來源進行 REST API 分析與文件化：

1. 已產出的資料庫說明文件（docs/spec/database/index.md）
2. restserver/ 目錄下所有 Python API 程式碼

---

## 1. 輸出位置
docs/spec/api/index.md
### 檔案初始化規則

- 必須先清空 docs/spec/api/ 內所有檔案
- 清空後再開始生成
- 視為全新專案初始化（not incremental）

## 2. 文件架構

使用 Markdown（.md），需符合以下結構：

### 2.1 單一入口文件（index.md）

用途：

- 僅作 所有API group 導覽（Navigation）, 提供 anchor link（可跳轉）
- 不包含 Request / Response 細節

禁止：

- 不可放 API 詳細內容
- 不可放 Business Logic

---

### 2.2 API Module 分組規則

API 必須依照以下規則分類：

- 依據 *_uri.py 檔案名稱進行分類
- 每個 *_uri.py 視為一個 API module

範例：

- auth_uri.py → Auth API Group
- user_uri.py → User API Group

---

### 2.3 排序規則

所有 API module 必須依：

- *_uri.py 檔名
- A → Z 排序
- 每個 *_uri.py 必須產生獨立 md 文件

範例：

- auth_uri.py      → auth.md 
- employee_uri.py  → employee.md 
- inventory_uri.py → inventory.md


---
## 4. Module 文件結構

每個 Module 文件（{module}.md）必須包含：

1. API Summary（索引）Anchor Link
2. Individual API Specification（詳細）

API Summary 不得獨立成檔案。


## 5. API Summary
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


   ### 5.1 Description欄位 和 狀態欄位 和 Review Note欄位
      規則：
      1. route 名稱
      2. class 名稱
      3. function 名稱
      4. validate schema
      5. Processing Flow
      6. Database Tables Used

      若以上資訊可合理推導 API 目的，
      應產生 Description。

      僅在無法合理推導 API 目的時，
      狀態欄位才標示 Need Review。

   範例：

   | URL | 狀態 |  Review Note |
   |------|------|------|
   | /user/login | OK | OK |
   | /user/login | Need Review | 無法確認用途 | 


## 6. Individual API Specification
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

      ### 6.1 基本資訊
      
      需列出：
      - URL
      - Method
      - Description

      範例:
      | URL | Method | Description |
      |----------|----------|----------------|
      |/user/login|POST|使用帳號密碼登入|
      
      Description欄位產生規則：
      同 5.1

      ---


      ### 6.2 Request Header
      規則
      1. 需列出：
         - Content-Type
         - x-auth-token 被 disable, 必須標示 "Not required", 不得保留原始技術描述
      2. 必須轉換 framework override 為「業務語意」
      3. 不得輸出 framework 描述語句（如 override / base class / required by system）
     

      範例:
      | Header | Description 
      |----------|----------|
      |Content-Type|application/json|
      |x-auth-token|存取金鑰|

      ---

      ### 6.3 Query Parameters
      若無 → 明確標示 None
      若有 → 依據以下規則
      1. 需列出：
         - Parameter 
         - Type
         - Required
         - Description

      2. 推導規則
         -  參數在 if/where/filter 使用語境
         -  ORM filter condition
         -  service function usage
         -  variable naming semantics
         -  API route context
         如果可推導，必須輸出具體語意
         
         只有在以下情況才允許標記 unknown：
         - parameter 未被任何 code 使用
         - request.args.get 後未進入任何 logic

         不得輸出以下內容：
         - Derived from request.args.get usage
         - semantic description requires review

      範例:
      | Parameter | Type | Required | Description 
      |----------|----------|------|-----|
      |username|string|YES|登入帳號|


      ---

      ### 6.4 Request Body

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

      4. 推導規則

         允許從以下來源取得：

          - validate(schema)
          - jsonschema
          - request.get_json()
         -  request.json
         -  request.form

         Required 判定規則：

         若符合以下任一條件：
          - required = true
          - required=[]
          - minLength > 0

         程式碼明確檢查欄位存在
         則標示：YES
         否則標示：NO
         若無法判定：Need Review

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

      ### 6.5 Success Response Data
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

      4. 規則
         允許沿著程式碼路徑進行追蹤：

          - function call
          - class method call
          - helper function
          - service layer
          - response wrapper
          - inheritance

         必須遞迴追蹤：
         - dict
         - list
         - tuple
         - object
         - ORM model
         - dataclass
         - DTO
         - serializer

         直到：

         1. Primitive Type
            - String
            - Integer
            - Float
            - Boolean
            - ...
         或

         2. 無法取得原始結構才允許停止。
         
         ### Response Wrapper 分析規則
         若 API 最終回傳經過共用封裝：

         例如：
         return obj_uri.run()
         必須向上追蹤至實際 Response Builder。

         允許分析：
          - Base URI
          - Common Response Class
          - Response Utility
          - Framework Wrapper

         ### Dict 組裝規則

         若程式碼出現：

         dict_extra_data = {
            "token": str_token,
            "user": dict_user
         }

         或：

         payload = {}
         payload["token"] = str_token

         應視為可解析 Response。

         必須展開實際欄位。

         不得因以下命名而標示 Need Review：
          - dict_data
          - dict_extra_data
          - payload
          - response_data
          - result_data

         若可解析最終 Response Structure, 應產出完整 Success Response Data。
         
         ### Variable Reassignment Rule
         欄位型態必須以最終賦值結果判定。

         例如：

         dict_data = {
            "count": 0
         }

         dict_data["count"] = len(lst_result)

         則：

         count = Integer

         不得因 dict_data 為 Dict
         而將 count 標示為 Object。


         ### Function Return Expansion Rule

         若 Response 欄位來自：

         - function return
         - class method return
         - helper function return
         - service function return

         例如：

         dict_user = self.__find_user_info()

         則必須繼續追蹤：

         __find_user_info()

         內部回傳內容。

         若回傳為 dict：

         {
            "user_no": xxx,
            "user_name": xxx
         }

         則必須展開欄位。

         不得僅輸出：

         "user": "Object"


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

      ###  6.6  Failed Response Data
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



      ###  6.7 Processing Flow

      #### 禁止

      Processing Flow 不可包含以下內容：

      - Flask routing process
      - CAPIBase.run()
      - executor lifecycle
      - framework wrapper flow
      - request lifecycle generic steps

      不得停留於：
      - 呼叫服務
      - 呼叫 helper
      - 呼叫 business layer
      - 呼叫 repository

      例如：

      CContract.get(...)
      CMember.login(...)
      CInventory.create(...)

      不得描述為：

      1. 呼叫服務 CContract.get()


      必須改寫為：
      1. 查詢 Contract 資料
      2. 計算符合條件資料筆數   
      3. 組裝回傳結果
      必須繼續追蹤被呼叫函式內容。

      ---

      #### 必須

      必須描述, 此 API 實際業務邏輯執行流程」
      - 查詢
      - 驗證
      - 計算
      - 新增
      - 修改
      - 刪除
      - 轉換資料
      - 組裝 Response

      等實際業務行為。

      若 Processing Flow 出現：

      - payload.results
      - payload.data
      - payload.items

      則必須追蹤其來源變數。

      例如：

      payload["results"] = results

      必須分析：

      results = ?

      若 results 來自 CContract.get(), 則必須繼續分析 CContract.get()
      若未分析 CContract.get() 則視為文件不完整

      不得停止於 payload 組裝階段。

      #### 範例（login API）

      1. 驗證 username / password
      2. 查詢 member table
      3. 使用 Argon2 驗證密碼
      4. 查詢 employee 資料
      5. 建立 session token
      6. 寫入 session table
      7. 回傳 token + user info

      ---

      ###  6.8 Database Tables Used
      規則：
      - 使用表格說明, 需列出：  
         - Table
         - Purpose          
      - 必須進行跨函式追蹤
         允許：

         API Layer
         → Service Layer
         → Business Layer
         → 從 ORM / SQLAlchemy / query 推導

         只要可由程式碼路徑追溯，即列入文件。
         不得因資料表出現在其他 function 而忽略。

      Purpose 欄位不得描述：

      - 程式碼有使用此資料表
      - ORM 有使用此資料表
      - Service 有使用此資料表
      - Query 有使用此資料表
      - 程式碼路徑中使用此資料表
      ---

      Purpose 必須描述：
      此 API 使用該資料表的實際業務目的,  API 為何存取此資料表。

      ---

      範例：

      query(CTableMember)
      .filter(
         CTableMember.account == account
      )

      應產出：

      | Table | Purpose |
      |---------|---------|
      | member | 驗證登入帳號 |

 

## 7. 文件處理規則
1. 允許：
   允許分析範圍：
   - route decorator (*_uri.py)
   - controller class
   - service / business layer
   - helper function
   - ORM model
   - SQLAlchemy query
   - response wrapper / base response
   - dict / DTO / object mapping
   - 跨檔案分析
   - 跨 class 分析
   - 跨 function 分析

   必須允許跨 function / class 追蹤，不得只看單一函式。  

2. 所有內容必須來自程式碼或資料庫文件。
3. 文件內容必須可追溯至程式碼。
4. Code Review 優先於 Need Review。
5. 若程式碼與資料庫文件衝突，以程式碼為主，並於 Review Note 說明。

## 8. Documentation Quality Rules

   產生文件前，

   必須完成：

    - Request Schema Analysis
    - Query Parameter Analysis
    - Response Analysis
    - ORM Analysis
    - Processing Flow Analysis
    - Database Usage Analysis

   完成上述分析後才允許輸出文件。

## 10. Output Validation Rules

在輸出文件前，必須檢查：

### Success Response Data

禁止出現：

- Object
- Dict
- Array
- List

作為最終葉節點型態。
---

### Processing Flow

禁止出現：

- 呼叫服務
- 呼叫 helper
- 呼叫 repository
- 呼叫 business layer

作為流程步驟。

必須轉換為實際業務行為。

---

### Database Tables Used

Purpose 不得包含：

- 使用此資料表
- ORM 使用
- Query 使用
- 程式碼路徑使用

必須描述業務目的。

---

若違反以上規則：

文件視為未完成。