import { defaultLanguage, type LanguageCode } from "@/i18n/dictionary";
import type { StatusTone } from "@/types/dashboard";

type EnumDictionary = Record<string, string>;

type OrdersEnumKind =
  | "commitmentDecision"
  | "deliveryRisk"
  | "dependencyArea"
  | "dependencyStatus"
  | "orderPriority"
  | "paymentRisk"
  | "paymentStatus"
  | "paymentType"
  | "productionFeasibility"
  | "riskReason"
  | "riskType"
  | "stage"
  | "status"
  | "workflowStep";

const zhTW: Record<OrdersEnumKind, EnumDictionary> = {
  commitmentDecision: {
    deferred: "待下一版承諾檢查",
    feasible: "可承諾",
    coordination_required: "需協調",
    not_feasible: "不可承諾",
    unknown: "未判定"
  },
  deliveryRisk: {
    normal: "正常",
    attention: "注意",
    high_risk: "高風險",
    unknown: "未判定"
  },
  dependencyArea: {
    inventory: "庫存",
    purchasing: "採購",
    production: "生產",
    quality: "品檢",
    shipping: "出貨",
    payment: "收款",
    unknown: "依賴"
  },
  dependencyStatus: {
    ready: "可用",
    pending: "待處理",
    blocked: "阻擋",
    unknown: "未知"
  },
  orderPriority: {
    high: "高",
    medium: "中",
    low: "低",
    unknown: "中"
  },
  paymentRisk: {
    normal: "正常",
    unpaid: "未收款",
    partial_paid: "部分收款",
    overdue: "逾期",
    missing_payment_record: "缺少帳款資料",
    unknown: "未知"
  },
  paymentStatus: {
    unpaid: "未收款",
    partial_paid: "部分收款",
    paid: "已收款",
    overdue: "逾期",
    unknown: "未知"
  },
  paymentType: {
    daily: "日結",
    monthly: "月結",
    unknown: "未知"
  },
  productionFeasibility: {
    deferred: "待下一版產能檢查",
    feasible: "可生產",
    coordination_required: "需協調",
    not_feasible: "不可如期",
    unknown: "未判定"
  },
  riskReason: {
    overdue_due_date: "交期已逾期",
    payment_risk: "收款風險",
    due_date_approaching: "交期接近",
    empty: "無明顯風險",
    unknown: "未判定"
  },
  riskType: {
    due_date_urgent: "交期急迫",
    payment_risk: "收款風險",
    unknown: "風險"
  },
  stage: {
    accepted: "已接單",
    material_preparing: "備料中",
    scheduled: "已排產",
    in_production: "生產中",
    shipped: "已出貨",
    unknown: "待確認"
  },
  status: {
    done: "完成",
    in_progress: "進行中",
    pending: "待處理",
    blocked: "阻擋",
    unknown: "未知",
    not_started: "未開始",
    scheduled: "已排程",
    completed: "完成",
    ready: "可用",
    partial_shipped: "部分出貨",
    shipped: "已出貨"
  },
  workflowStep: {
    order_received: "接單",
    commitment_check: "承諾檢查",
    material_request: "請購需求",
    purchase_readiness: "採購準備",
    warehouse_readiness: "倉庫準備",
    production: "生產",
    quality_check: "品檢",
    shipping: "出貨",
    payment: "收款",
    unknown: "流程"
  }
};

const en: Record<OrdersEnumKind, EnumDictionary> = {
  commitmentDecision: {
    deferred: "Deferred",
    feasible: "Committable",
    coordination_required: "Needs coordination",
    not_feasible: "Not committable",
    unknown: "Unknown"
  },
  deliveryRisk: {
    normal: "Normal",
    attention: "Attention",
    high_risk: "High risk",
    unknown: "Unknown"
  },
  dependencyArea: {
    inventory: "Inventory",
    purchasing: "Purchasing",
    production: "Production",
    quality: "Quality",
    shipping: "Shipping",
    payment: "Payment",
    unknown: "Dependency"
  },
  dependencyStatus: {
    ready: "Ready",
    pending: "Pending",
    blocked: "Blocked",
    unknown: "Unknown"
  },
  orderPriority: {
    high: "High",
    medium: "Medium",
    low: "Low",
    unknown: "Medium"
  },
  paymentRisk: {
    normal: "Normal",
    unpaid: "Unpaid",
    partial_paid: "Partial paid",
    overdue: "Overdue",
    missing_payment_record: "Missing payment record",
    unknown: "Unknown"
  },
  paymentStatus: {
    unpaid: "Unpaid",
    partial_paid: "Partial paid",
    paid: "Paid",
    overdue: "Overdue",
    unknown: "Unknown"
  },
  paymentType: {
    daily: "Daily",
    monthly: "Monthly",
    unknown: "Unknown"
  },
  productionFeasibility: {
    deferred: "Deferred",
    feasible: "Feasible",
    coordination_required: "Needs coordination",
    not_feasible: "Not feasible",
    unknown: "Unknown"
  },
  riskReason: {
    overdue_due_date: "Due date overdue",
    payment_risk: "Payment risk",
    due_date_approaching: "Due date approaching",
    empty: "No visible risk",
    unknown: "Unknown"
  },
  riskType: {
    due_date_urgent: "Urgent due date",
    payment_risk: "Payment risk",
    unknown: "Risk"
  },
  stage: {
    accepted: "Accepted",
    material_preparing: "Material preparing",
    scheduled: "Scheduled",
    in_production: "In production",
    shipped: "Shipped",
    unknown: "Pending confirmation"
  },
  status: {
    done: "Done",
    in_progress: "In progress",
    pending: "Pending",
    blocked: "Blocked",
    unknown: "Unknown",
    not_started: "Not started",
    scheduled: "Scheduled",
    completed: "Completed",
    ready: "Ready",
    partial_shipped: "Partially shipped",
    shipped: "Shipped"
  },
  workflowStep: {
    order_received: "Order received",
    commitment_check: "Commitment check",
    material_request: "Material request",
    purchase_readiness: "Purchase readiness",
    warehouse_readiness: "Warehouse readiness",
    production: "Production",
    quality_check: "Quality check",
    shipping: "Shipping",
    payment: "Payment",
    unknown: "Workflow"
  }
};

const ja: Record<OrdersEnumKind, EnumDictionary> = {
  commitmentDecision: {
    deferred: "次版で判定",
    feasible: "確約可能",
    coordination_required: "調整要",
    not_feasible: "確約不可",
    unknown: "未判定"
  },
  deliveryRisk: {
    normal: "正常",
    attention: "注意",
    high_risk: "高リスク",
    unknown: "未判定"
  },
  dependencyArea: {
    inventory: "在庫",
    purchasing: "購買",
    production: "生産",
    quality: "品質",
    shipping: "出荷",
    payment: "入金",
    unknown: "依存"
  },
  dependencyStatus: {
    ready: "準備完了",
    pending: "保留",
    blocked: "ブロック",
    unknown: "不明"
  },
  orderPriority: {
    high: "高",
    medium: "中",
    low: "低",
    unknown: "中"
  },
  paymentRisk: {
    normal: "正常",
    unpaid: "未入金",
    partial_paid: "一部入金",
    overdue: "期限超過",
    missing_payment_record: "入金記録不足",
    unknown: "不明"
  },
  paymentStatus: {
    unpaid: "未入金",
    partial_paid: "一部入金",
    paid: "入金済",
    overdue: "期限超過",
    unknown: "不明"
  },
  paymentType: {
    daily: "日締め",
    monthly: "月締め",
    unknown: "不明"
  },
  productionFeasibility: {
    deferred: "次版で判定",
    feasible: "生産可能",
    coordination_required: "調整要",
    not_feasible: "納期困難",
    unknown: "未判定"
  },
  riskReason: {
    overdue_due_date: "納期超過",
    payment_risk: "入金リスク",
    due_date_approaching: "納期接近",
    empty: "明確なリスクなし",
    unknown: "未判定"
  },
  riskType: {
    due_date_urgent: "納期急迫",
    payment_risk: "入金リスク",
    unknown: "リスク"
  },
  stage: {
    accepted: "受注済",
    material_preparing: "材料準備中",
    scheduled: "計画済",
    in_production: "生産中",
    shipped: "出荷済",
    unknown: "確認待ち"
  },
  status: {
    done: "完了",
    in_progress: "進行中",
    pending: "保留",
    blocked: "ブロック",
    unknown: "不明",
    not_started: "未開始",
    scheduled: "計画済",
    completed: "完了",
    ready: "準備完了",
    partial_shipped: "一部出荷",
    shipped: "出荷済"
  },
  workflowStep: {
    order_received: "受注",
    commitment_check: "確約確認",
    material_request: "材料依頼",
    purchase_readiness: "購買準備",
    warehouse_readiness: "倉庫準備",
    production: "生産",
    quality_check: "品質確認",
    shipping: "出荷",
    payment: "入金",
    unknown: "工程"
  }
};

const vi: Record<OrdersEnumKind, EnumDictionary> = {
  commitmentDecision: {
    deferred: "Hoãn sang phiên bản sau",
    feasible: "Có thể cam kết",
    coordination_required: "Cần phối hợp",
    not_feasible: "Không thể cam kết",
    unknown: "Chưa xác định"
  },
  deliveryRisk: {
    normal: "Bình thường",
    attention: "Cần chú ý",
    high_risk: "Rủi ro cao",
    unknown: "Chưa xác định"
  },
  dependencyArea: {
    inventory: "Tồn kho",
    purchasing: "Mua hàng",
    production: "Sản xuất",
    quality: "Chất lượng",
    shipping: "Giao hàng",
    payment: "Thu tiền",
    unknown: "Phụ thuộc"
  },
  dependencyStatus: {
    ready: "Sẵn sàng",
    pending: "Chờ xử lý",
    blocked: "Bị chặn",
    unknown: "Không rõ"
  },
  orderPriority: {
    high: "Cao",
    medium: "Trung bình",
    low: "Thấp",
    unknown: "Trung bình"
  },
  paymentRisk: {
    normal: "Bình thường",
    unpaid: "Chưa thu",
    partial_paid: "Thu một phần",
    overdue: "Quá hạn",
    missing_payment_record: "Thiếu dữ liệu thanh toán",
    unknown: "Không rõ"
  },
  paymentStatus: {
    unpaid: "Chưa thu",
    partial_paid: "Thu một phần",
    paid: "Đã thu",
    overdue: "Quá hạn",
    unknown: "Không rõ"
  },
  paymentType: {
    daily: "Theo ngày",
    monthly: "Theo tháng",
    unknown: "Không rõ"
  },
  productionFeasibility: {
    deferred: "Hoãn sang phiên bản sau",
    feasible: "Có thể sản xuất",
    coordination_required: "Cần phối hợp",
    not_feasible: "Không kịp tiến độ",
    unknown: "Chưa xác định"
  },
  riskReason: {
    overdue_due_date: "Quá hạn giao hàng",
    payment_risk: "Rủi ro thu tiền",
    due_date_approaching: "Sắp đến hạn giao",
    empty: "Không có rủi ro rõ ràng",
    unknown: "Chưa xác định"
  },
  riskType: {
    due_date_urgent: "Gấp hạn giao",
    payment_risk: "Rủi ro thu tiền",
    unknown: "Rủi ro"
  },
  stage: {
    accepted: "Đã nhận đơn",
    material_preparing: "Chuẩn bị vật tư",
    scheduled: "Đã lập lịch",
    in_production: "Đang sản xuất",
    shipped: "Đã giao",
    unknown: "Chờ xác nhận"
  },
  status: {
    done: "Hoàn tất",
    in_progress: "Đang xử lý",
    pending: "Chờ xử lý",
    blocked: "Bị chặn",
    unknown: "Không rõ",
    not_started: "Chưa bắt đầu",
    scheduled: "Đã lập lịch",
    completed: "Hoàn tất",
    ready: "Sẵn sàng",
    partial_shipped: "Giao một phần",
    shipped: "Đã giao"
  },
  workflowStep: {
    order_received: "Nhận đơn",
    commitment_check: "Kiểm tra cam kết",
    material_request: "Yêu cầu vật tư",
    purchase_readiness: "Sẵn sàng mua hàng",
    warehouse_readiness: "Sẵn sàng kho",
    production: "Sản xuất",
    quality_check: "Kiểm tra chất lượng",
    shipping: "Giao hàng",
    payment: "Thu tiền",
    unknown: "Quy trình"
  }
};

const enumDictionaries: Record<LanguageCode, Record<OrdersEnumKind, EnumDictionary>> = {
  "zh-TW": zhTW,
  en,
  ja,
  vi
};

export function ordersEnumLabel(kind: OrdersEnumKind, value: number | string | undefined, language: LanguageCode) {
  const key = value === undefined || value === null || value === "" ? "unknown" : String(value);
  const selected = enumDictionaries[language][kind];
  const fallback = enumDictionaries[defaultLanguage][kind];

  return selected[key] ?? selected.unknown ?? fallback[key] ?? fallback.unknown ?? key;
}

export function ordersRiskTone(risk?: string, riskLevel?: number): StatusTone {
  if (risk === "high_risk" || risk === "overdue" || risk === "missing_payment_record" || (riskLevel ?? 0) >= 3) {
    return "danger";
  }
  if (risk === "attention" || risk === "partial_paid" || risk === "unpaid" || (riskLevel ?? 0) >= 2) {
    return "warning";
  }
  return "success";
}

export function ordersStatusTone(status?: string, riskLevel?: number): StatusTone {
  if (status === "blocked" || status === "overdue" || (riskLevel ?? 0) >= 3) {
    return "danger";
  }
  if (status === "pending" || status === "in_progress" || status === "partial_paid" || (riskLevel ?? 0) >= 2) {
    return "warning";
  }
  if (status === "done" || status === "ready" || status === "paid" || status === "completed") {
    return "success";
  }
  return "info";
}
