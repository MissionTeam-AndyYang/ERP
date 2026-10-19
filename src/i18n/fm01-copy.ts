const traditionalChineseCopy = {
  "settings.title": "系統設定",
  "settings.description": "管理 ERP 組織與地點主檔。",
  "page.title": "組織與地點",
  "page.description": "依組織層級檢視法人、公司、廠區、廠別、倉庫與庫位。",
  "page.apiSource": "資料由後端即時讀取",
  "page.hierarchy": "組織階層",
  "page.list": "清單",
  "page.search": "搜尋代碼或名稱",
  "page.entityFilter": "資料類型",
  "page.add": "新增",
  "page.refresh": "重新載入",
  "page.retry": "重試",
  "page.clear": "清除搜尋",
  "page.empty": "目前沒有組織與地點資料。",
  "page.emptyChildren": "目前沒有下層資料。",
  "page.selectPrompt": "選取一筆資料以查看詳細資訊。",
  "page.searchScope": "清單搜尋範圍為目前載入頁面，無法跨頁搜尋。",
  "page.loading": "正在載入資料…",
  "page.errorTitle": "資料無法載入",
  "page.emptySearch": "沒有符合搜尋條件的資料。",
  "page.pageCount": "第 {page} 頁，共 {pages} 頁",
  "page.rows": "共 {count} 筆",
  "page.previous": "上一頁",
  "page.next": "下一頁",
  "detail.title": "資料明細",
  "detail.reference": "參照代碼",
  "detail.displayName": "顯示名稱",
  "detail.identifier": "系統編號",
  "detail.entityType": "資料類型",
  "detail.relationships": "組織關係",
  "detail.parent": "上層資料",
  "detail.site": "所屬廠區",
  "detail.plantAssociation": "關聯廠別（原始關聯值）",
  "detail.warehouse": "所屬倉庫",
  "detail.parentLocation": "上層庫位 ID",
  "detail.status": "狀態",
  "detail.statusUnavailable": "目前資料未包含狀態",
  "detail.edit": "編輯名稱",
  "detail.lifecycle": "檢視受控流程",
  "detail.notFound": "找不到此筆資料，請重新載入清單。",
  "detail.unavailable": "詳細資料暫時無法取得。",
  "create.title": "新增組織與地點",
  "create.description": "一次建立一個主檔；送出功能尚未開放。",
  "create.entityType": "資料類型",
  "create.reference": "參照代碼",
  "create.name": "顯示名稱",
  "create.parent": "上層資料",
  "create.parentChoose": "請選擇上層資料",
  "create.plant": "關聯廠別",
  "create.plantUnavailable": "目前無法驗證同一廠區關係，欄位停用。",
  "create.required": "此欄位為必填。",
  "create.check": "檢查欄位",
  "create.submit": "送出建立申請",
  "create.submitDisabled": "目前尚未開放建立申請；本表單不會送出或儲存資料。",
  "create.cancel": "返回組織與地點",
  "create.validationTitle": "請先修正以下欄位",
  "create.parentLoadError": "無法載入上層資料；建立表單保持停用。",
  "edit.title": "編輯顯示名稱",
  "edit.description": "僅允許編輯顯示名稱；目前只保留本機草稿。",
  "edit.save": "送出變更",
  "edit.disabled": "目前尚未開放受控更新；本頁不會送出修改。",
  "edit.cancel": "取消",
  "edit.invalid": "顯示名稱不可空白。",
  "workflow.title": "組織與地點變更流程",
  "workflow.description": "受控流程介面；目前只提供資料檢視，不會執行變更。",
  "workflow.deactivate": "停用流程",
  "workflow.reactivate": "重新啟用流程",
  "workflow.reason": "申請原因",
  "workflow.evidence": "佐證資料參照",
  "workflow.submit": "送交核准",
  "workflow.approve": "核准",
  "workflow.reject": "退回",
  "workflow.allDisabled": "受控變更所需的狀態、授權、核准與稽核條件尚未具備；所有操作均停用。",
  "workflow.approval": "核准紀錄",
  "workflow.audit": "稽核紀錄",
  "workflow.approvalUnavailable": "核准紀錄目前無法檢視；這不代表已有或沒有核准紀錄。",
  "workflow.auditUnavailable": "稽核紀錄目前無法檢視；不會以預設或示意資料取代。",
  "workflow.steps": "流程階段",
  "workflow.stepReview": "檢視目標資料",
  "workflow.stepChecks": "權限與關聯檢查",
  "workflow.stepApproval": "獨立核准與稽核",
  "workflow.stepExecution": "核准後執行",
  "workflow.notStarted": "目前無流程資料可供檢視",
  "error.apiConfig": "資料服務連線設定尚未完成，未顯示替代資料。",
  "error.network": "目前無法連線到後端。請確認服務狀態後重試。",
  "error.unauthorized": "登入狀態無效或已逾期，請重新登入。",
  "error.forbidden": "目前帳號無權讀取此資料，請洽系統管理員。",
  "error.notFound": "查無此筆資料。",
  "error.conflict": "伺服器回報資料衝突；本畫面未送出任何修改，請重新載入後確認。",
  "error.invalidQuery": "伺服器無法處理目前查詢條件。",
  "error.invalidResponse": "資料格式暫時無法讀取。",
  "error.invalidRoute": "流程連結無效，請返回組織與地點重新選取資料。",
  "error.generic": "讀取資料時發生錯誤；不會以示意資料取代實際資料。",
  "error.correlationId": "追蹤編號",
  "error.dismiss": "關閉訊息"
} as const;

export type Fm01CopyKey = keyof typeof traditionalChineseCopy;

export function fm01Text(key: Fm01CopyKey) {
  return traditionalChineseCopy[key];
}

export function fm01ErrorText(code: string, status?: number, correlationId?: string) {
  let message = fm01Text("error.generic");
  if (code === "API_BASE_URL_MISSING") message = fm01Text("error.apiConfig");
  else if (code === "NETWORK_UNAVAILABLE") message = fm01Text("error.network");
  else if (status === 401) message = fm01Text("error.unauthorized");
  else if (status === 403) message = fm01Text("error.forbidden");
  else if (status === 404 || code === "NOT_FOUND") message = fm01Text("error.notFound");
  else if (status === 409) message = fm01Text("error.conflict");
  else if (status === 400 || status === 422) message = fm01Text("error.invalidQuery");
  else if (code === "INVALID_ROUTE") message = fm01Text("error.invalidRoute");
  else if (code === "INVALID_RESPONSE") message = fm01Text("error.invalidResponse");

  const safeCorrelationId = correlationId && /^[A-Za-z0-9._:-]{1,128}$/.test(correlationId)
    ? `（${fm01Text("error.correlationId")}：${correlationId}）`
    : "";
  return `${message}${safeCorrelationId}`;
}
