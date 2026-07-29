import type { LanguageCode } from "@/i18n/dictionary";
import type { StatusTone } from "@/types/dashboard";

type EnumTable = Record<string, Partial<Record<LanguageCode, string>>>;

const fallbackLanguage: LanguageCode = "zh-TW";

const unitLabels: Record<number, Partial<Record<LanguageCode, string>>> = {
  0: { "zh-TW": "其他", en: "Other", ja: "その他", vi: "Khác" },
  1: { "zh-TW": "公克", en: "g", ja: "g", vi: "g" },
  2: { "zh-TW": "公斤", en: "kg", ja: "kg", vi: "kg" },
  3: { "zh-TW": "台斤", en: "catty", ja: "台斤", vi: "cân Đài Loan" },
  51: { "zh-TW": "公分", en: "cm", ja: "cm", vi: "cm" },
  52: { "zh-TW": "公尺", en: "m", ja: "m", vi: "m" },
  101: { "zh-TW": "個", en: "pcs", ja: "個", vi: "cái" },
  102: { "zh-TW": "條", en: "strip", ja: "本", vi: "thanh" },
  103: { "zh-TW": "片", en: "sheet", ja: "枚", vi: "miếng" },
  104: { "zh-TW": "張", en: "sheet", ja: "枚", vi: "tờ" },
  105: { "zh-TW": "罐", en: "can", ja: "缶", vi: "lon" },
  106: { "zh-TW": "包", en: "pack", ja: "包", vi: "gói" },
  107: { "zh-TW": "捲", en: "roll", ja: "巻", vi: "cuộn" },
  108: { "zh-TW": "桶", en: "pail", ja: "桶", vi: "thùng" },
  109: { "zh-TW": "盒", en: "box", ja: "箱", vi: "hộp" },
  110: { "zh-TW": "組", en: "set", ja: "組", vi: "bộ" },
  111: { "zh-TW": "箱", en: "carton", ja: "箱", vi: "thùng" },
  112: { "zh-TW": "支", en: "piece", ja: "本", vi: "cây" },
  113: { "zh-TW": "式", en: "set", ja: "式", vi: "bộ" },
  114: { "zh-TW": "入", en: "unit", ja: "入り", vi: "đơn vị" },
  115: { "zh-TW": "袋", en: "bag", ja: "袋", vi: "túi" },
  116: { "zh-TW": "顆", en: "piece", ja: "粒", vi: "viên" },
  117: { "zh-TW": "瓶", en: "bottle", ja: "瓶", vi: "chai" },
  201: { "zh-TW": "板", en: "pallet", ja: "パレット", vi: "pallet" },
  202: { "zh-TW": "件", en: "case", ja: "件", vi: "kiện" },
  203: { "zh-TW": "車", en: "truck", ja: "車", vi: "xe" },
  204: { "zh-TW": "次", en: "time", ja: "回", vi: "lần" }
};

const riskLevelLabels: Record<number, Partial<Record<LanguageCode, string>>> = {
  0: { "zh-TW": "正常", en: "Normal", ja: "正常", vi: "Bình thường" },
  1: { "zh-TW": "注意", en: "Notice", ja: "注意", vi: "Cần chú ý" },
  3: { "zh-TW": "高風險", en: "High risk", ja: "高リスク", vi: "Rủi ro cao" }
};

const enumTables: Record<string, EnumTable> = {
  purchaseRequestLinkStatus: {
    linked: { "zh-TW": "已連請購", en: "Linked PR", ja: "購買依頼あり", vi: "Đã liên kết đề nghị mua" },
    unlinked: { "zh-TW": "未連請購", en: "Unlinked PR", ja: "購買依頼なし", vi: "Chưa liên kết đề nghị mua" },
    invalid: { "zh-TW": "關聯異常", en: "Invalid link", ja: "関連異常", vi: "Liên kết lỗi" }
  },
  warehouseStatus: {
    not_received: { "zh-TW": "尚未到貨", en: "Not received", ja: "未入荷", vi: "Chưa nhận" },
    pending_putaway: { "zh-TW": "待入庫交接", en: "Pending putaway", ja: "棚入れ待ち", vi: "Chờ nhập kho" },
    stocked: { "zh-TW": "已入庫", en: "Stocked", ja: "入庫済み", vi: "Đã nhập kho" },
    unknown: { "zh-TW": "狀態未知", en: "Unknown", ja: "不明", vi: "Không rõ" }
  },
  riskType: {
    normal: { "zh-TW": "正常", en: "Normal", ja: "正常", vi: "Bình thường" },
    late_arrival: { "zh-TW": "逾期未到", en: "Late arrival", ja: "入荷遅延", vi: "Trễ hàng" },
    due_today: { "zh-TW": "今日到期", en: "Due today", ja: "本日期限", vi: "Đến hạn hôm nay" },
    open_receipt: { "zh-TW": "尚有未收", en: "Open receipt", ja: "未収あり", vi: "Còn thiếu nhận hàng" },
    purchase_request_unlinked: { "zh-TW": "缺少請購關聯", en: "PR unlinked", ja: "購買依頼未連携", vi: "Thiếu liên kết đề nghị mua" },
    unknown: { "zh-TW": "待確認", en: "Unknown", ja: "確認待ち", vi: "Chờ xác nhận" }
  },
  receiptCategory: {
    "0": { "zh-TW": "進貨", en: "Receipt", ja: "入荷", vi: "Nhận hàng" },
    "1": { "zh-TW": "進貨退回", en: "Return", ja: "返品", vi: "Trả hàng" }
  },
  receivingStatus: {
    received: { "zh-TW": "已收貨", en: "Received", ja: "受領済み", vi: "Đã nhận" },
    returned: { "zh-TW": "已退回", en: "Returned", ja: "返品済み", vi: "Đã trả" },
    unknown: { "zh-TW": "待確認", en: "Unknown", ja: "確認待ち", vi: "Chờ xác nhận" }
  },
  impactSource: {
    work_order: { "zh-TW": "生產工單", en: "Work order", ja: "製造指図", vi: "Lệnh sản xuất" },
    sales_order: { "zh-TW": "訂購單", en: "Sales order", ja: "受注", vi: "Đơn bán hàng" },
    safety_stock: { "zh-TW": "安全水位", en: "Safety stock", ja: "安全在庫", vi: "Tồn an toàn" },
    unknown: { "zh-TW": "未確認來源", en: "Unknown source", ja: "不明な由来", vi: "Nguồn chưa rõ" }
  },
  followUp: {
    review_source_impact: { "zh-TW": "檢視來源影響", en: "Review source impact", ja: "影響元を確認", vi: "Xem ảnh hưởng nguồn" },
    confirm_supplier_date: { "zh-TW": "確認供應商交期", en: "Confirm supplier date", ja: "仕入先納期確認", vi: "Xác nhận ngày giao" },
    unknown: { "zh-TW": "待採購確認", en: "Needs purchasing review", ja: "購買確認待ち", vi: "Chờ mua hàng xác nhận" }
  },
  taskType: {
    "2": { "zh-TW": "採購", en: "Purchase", ja: "購買", vi: "Mua hàng" },
    "3": { "zh-TW": "進貨", en: "Goods receipt", ja: "入荷", vi: "Nhận hàng" },
    "4": { "zh-TW": "入庫", en: "Putaway", ja: "入庫", vi: "Nhập kho" }
  },
  taskStatus: {
    "1": { "zh-TW": "待處理", en: "Pending", ja: "未処理", vi: "Chờ xử lý" },
    "2": { "zh-TW": "部分完成", en: "Partially done", ja: "一部完了", vi: "Hoàn thành một phần" },
    "3": { "zh-TW": "已完成", en: "Done", ja: "完了", vi: "Đã hoàn thành" },
    "4": { "zh-TW": "阻塞", en: "Blocked", ja: "ブロック", vi: "Bị chặn" },
    "5": { "zh-TW": "取消", en: "Canceled", ja: "取消", vi: "Đã hủy" }
  },
  department: {
    "0": { "zh-TW": "未指定", en: "Unassigned", ja: "未指定", vi: "Chưa giao" },
    "1": { "zh-TW": "業務", en: "Sales", ja: "営業", vi: "Kinh doanh" },
    "2": { "zh-TW": "採購", en: "Purchasing", ja: "購買", vi: "Mua hàng" },
    "3": { "zh-TW": "生產", en: "Production", ja: "生産", vi: "Sản xuất" },
    "4": { "zh-TW": "倉庫", en: "Warehouse", ja: "倉庫", vi: "Kho" },
    "5": { "zh-TW": "品保", en: "Quality", ja: "品質", vi: "Chất lượng" }
  }
};

function pickLabel(labels: Partial<Record<LanguageCode, string>> | undefined, language: LanguageCode, fallback: string) {
  return labels?.[language] ?? labels?.[fallbackLanguage] ?? fallback;
}

export function purchasingUnitLabel(value?: number, language: LanguageCode = fallbackLanguage) {
  if (value === undefined || value === null) {
    return "";
  }
  return pickLabel(unitLabels[value], language, String(value));
}

export function purchasingRiskLevelLabel(value?: number, language: LanguageCode = fallbackLanguage) {
  if (value === undefined || value === null) {
    return pickLabel(riskLevelLabels[0], language, "0");
  }
  return pickLabel(riskLevelLabels[value], language, String(value));
}

export function purchasingEnumLabel(kind: keyof typeof enumTables, value?: string | number, language: LanguageCode = fallbackLanguage) {
  if (value === undefined || value === null || value === "") {
    return pickLabel(enumTables[kind].unknown, language, "");
  }
  const key = String(value);
  return pickLabel(enumTables[kind][key], language, key);
}

export function purchasingRiskTone(value?: number): StatusTone {
  if (value === 3) {
    return "danger";
  }
  if (value === 1) {
    return "warning";
  }
  return "success";
}

export function purchasingStatusTone(value?: string | number): StatusTone {
  if (value === "stocked" || value === "received" || value === 3) {
    return "success";
  }
  if (value === "pending_putaway" || value === 2) {
    return "warning";
  }
  if (value === "returned" || value === 4) {
    return "danger";
  }
  return "info";
}
