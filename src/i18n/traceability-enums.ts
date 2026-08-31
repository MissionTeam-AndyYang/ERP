import { defaultLanguage, type LanguageCode } from "@/i18n/dictionary";
import { warehouseEnumLabel } from "@/i18n/warehouse-enums";
import type { StatusTone } from "@/types/dashboard";
import type {
  TraceDirectionCode,
  TracePartnerTypeCode,
  TraceRiskCode,
  TraceRiskLevelCode,
  TraceStatusCode,
  TraceStepStatusCode,
  TraceStepTypeCode
} from "@/types/traceability";

type Dictionary<T extends string> = Record<T | "unknown", string>;

const traceDirectionLabels: Record<LanguageCode, Dictionary<TraceDirectionCode>> = {
  "zh-TW": {
    upstream: "製成品往上游",
    downstream: "原料往下游",
    both: "雙向",
    unknown: "待確認"
  },
  en: {
    upstream: "Finished goods upstream",
    downstream: "Raw material downstream",
    both: "Both directions",
    unknown: "Unknown"
  },
  ja: {
    upstream: "製品から上流",
    downstream: "原料から下流",
    both: "双方向",
    unknown: "未確認"
  },
  vi: {
    upstream: "Thành phẩm về thượng nguồn",
    downstream: "Nguyên liệu về hạ nguồn",
    both: "Hai chiều",
    unknown: "Chưa xác nhận"
  }
};

const traceStatusLabels: Record<LanguageCode, Dictionary<TraceStatusCode>> = {
  "zh-TW": {
    complete: "完整",
    broken: "斷鏈",
    unknown: "待確認"
  },
  en: {
    complete: "Complete",
    broken: "Broken",
    unknown: "Unknown"
  },
  ja: {
    complete: "完全",
    broken: "途切れ",
    unknown: "未確認"
  },
  vi: {
    complete: "Hoàn chỉnh",
    broken: "Đứt chuỗi",
    unknown: "Chưa xác nhận"
  }
};

const traceRiskLevelLabels: Record<LanguageCode, Dictionary<TraceRiskLevelCode>> = {
  "zh-TW": {
    normal: "正常",
    attention: "注意",
    high_risk: "高風險",
    unknown: "未分級"
  },
  en: {
    normal: "Normal",
    attention: "Attention",
    high_risk: "High risk",
    unknown: "Unrated"
  },
  ja: {
    normal: "正常",
    attention: "注意",
    high_risk: "高リスク",
    unknown: "未分類"
  },
  vi: {
    normal: "Bình thường",
    attention: "Cần chú ý",
    high_risk: "Rủi ro cao",
    unknown: "Chưa phân loại"
  }
};

const traceRiskLabels: Record<LanguageCode, Dictionary<TraceRiskCode>> = {
  "zh-TW": {
    normal: "正常",
    broken_chain: "追溯斷鏈",
    expired: "已逾期",
    quality_hold: "品檢保留",
    unknown: "待確認"
  },
  en: {
    normal: "Normal",
    broken_chain: "Broken chain",
    expired: "Expired",
    quality_hold: "Quality hold",
    unknown: "Unknown"
  },
  ja: {
    normal: "正常",
    broken_chain: "追跡途切れ",
    expired: "期限切れ",
    quality_hold: "品質保留",
    unknown: "未確認"
  },
  vi: {
    normal: "Bình thường",
    broken_chain: "Đứt chuỗi truy xuất",
    expired: "Hết hạn",
    quality_hold: "Giữ chất lượng",
    unknown: "Chưa xác nhận"
  }
};

const partnerTypeLabels: Record<LanguageCode, Dictionary<TracePartnerTypeCode>> = {
  "zh-TW": {
    supplier: "供應商",
    customer: "客戶",
    internal: "內部",
    unknown: "待確認"
  },
  en: {
    supplier: "Supplier",
    customer: "Customer",
    internal: "Internal",
    unknown: "Unknown"
  },
  ja: {
    supplier: "仕入先",
    customer: "顧客",
    internal: "内部",
    unknown: "未確認"
  },
  vi: {
    supplier: "Nhà cung cấp",
    customer: "Khách hàng",
    internal: "Nội bộ",
    unknown: "Chưa xác nhận"
  }
};

const traceStepTypeLabels: Record<LanguageCode, Dictionary<TraceStepTypeCode>> = {
  "zh-TW": {
    receipt: "進貨",
    production: "產製",
    sale: "銷貨",
    unknown: "流程"
  },
  en: {
    receipt: "Receipt",
    production: "Production",
    sale: "Sale",
    unknown: "Step"
  },
  ja: {
    receipt: "入荷",
    production: "生産",
    sale: "販売",
    unknown: "工程"
  },
  vi: {
    receipt: "Nhập hàng",
    production: "Sản xuất",
    sale: "Bán hàng",
    unknown: "Bước"
  }
};

const traceStepStatusLabels: Record<LanguageCode, Dictionary<TraceStepStatusCode>> = {
  "zh-TW": {
    complete: "完成",
    pending: "待處理",
    blocked: "阻塞",
    missing: "缺漏",
    unknown: "待確認"
  },
  en: {
    complete: "Complete",
    pending: "Pending",
    blocked: "Blocked",
    missing: "Missing",
    unknown: "Unknown"
  },
  ja: {
    complete: "完了",
    pending: "未処理",
    blocked: "ブロック",
    missing: "不足",
    unknown: "未確認"
  },
  vi: {
    complete: "Hoàn tất",
    pending: "Chờ xử lý",
    blocked: "Bị chặn",
    missing: "Thiếu",
    unknown: "Chưa xác nhận"
  }
};

function enumLabel<T extends string>(
  dictionaries: Record<LanguageCode, Dictionary<T>>,
  value: T | string | undefined,
  language: LanguageCode = defaultLanguage
) {
  const key = (value || "unknown") as T | "unknown";
  const selected = dictionaries[language] ?? dictionaries[defaultLanguage];
  const fallback = dictionaries[defaultLanguage];
  return selected[key] ?? selected.unknown ?? fallback[key] ?? fallback.unknown ?? String(value ?? "");
}

export function traceDirectionLabel(value?: string, language: LanguageCode = defaultLanguage) {
  return enumLabel(traceDirectionLabels, value, language);
}

export function traceStatusLabel(value?: string, language: LanguageCode = defaultLanguage) {
  return enumLabel(traceStatusLabels, value, language);
}

export function traceRiskLevelLabel(value?: string, language: LanguageCode = defaultLanguage) {
  return enumLabel(traceRiskLevelLabels, value, language);
}

export function traceRiskLabel(value?: string, language: LanguageCode = defaultLanguage) {
  return enumLabel(traceRiskLabels, value, language);
}

export function tracePartnerTypeLabel(value?: string, language: LanguageCode = defaultLanguage) {
  return enumLabel(partnerTypeLabels, value, language);
}

export function traceStepTypeLabel(value?: string, language: LanguageCode = defaultLanguage) {
  return enumLabel(traceStepTypeLabels, value, language);
}

export function traceStepStatusLabel(value?: string, language: LanguageCode = defaultLanguage) {
  return enumLabel(traceStepStatusLabels, value, language);
}

export function traceItemCategoryLabel(value?: number, language: LanguageCode = defaultLanguage) {
  return warehouseEnumLabel("itemCategory", value, language);
}

export function traceRefCategoryLabel(value?: number, language: LanguageCode = defaultLanguage) {
  return warehouseEnumLabel("refCategory", value, language);
}

export function traceUnitLabel(value?: number, language: LanguageCode = defaultLanguage) {
  return warehouseEnumLabel("unit", value, language);
}

export function traceRiskTone(riskLevelCode?: string, riskCode?: string): StatusTone {
  if (riskLevelCode === "high_risk" || riskCode === "broken_chain" || riskCode === "expired") {
    return "danger";
  }
  if (riskLevelCode === "attention" || riskCode === "quality_hold") {
    return "warning";
  }
  if (riskLevelCode === "normal" || riskCode === "normal") {
    return "success";
  }
  return "neutral";
}

export function traceStepStatusTone(statusCode?: string, riskLevelCode?: string): StatusTone {
  if (statusCode === "blocked" || statusCode === "missing" || riskLevelCode === "high_risk") {
    return "danger";
  }
  if (statusCode === "pending" || riskLevelCode === "attention") {
    return "warning";
  }
  if (statusCode === "complete" || riskLevelCode === "normal") {
    return "success";
  }
  return "neutral";
}
