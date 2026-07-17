import { defaultLanguage, type LanguageCode } from "@/i18n/dictionary";
import type { StatusTone } from "@/types/dashboard";

type EnumDictionary = Record<string, string>;

type ProductionEnumKind =
  | "alertType"
  | "capacityStatus"
  | "changeoverStatus"
  | "deliveryRisk"
  | "department"
  | "machineAction"
  | "machineStatus"
  | "materialStatus"
  | "process"
  | "qualityStatus"
  | "readinessSignal"
  | "readinessStatus"
  | "staffStatus"
  | "status"
  | "unit"
  | "workflowStep";

const zhTW: Record<ProductionEnumKind, EnumDictionary> = {
  alertType: {
    material_shortage: "缺料",
    staff_shortage: "人員不足",
    capacity_bottleneck: "產能瓶頸",
    capacity_config_missing: "缺少產能設定",
    capacity_downtime: "產線停用",
    schedule_delay: "排程落後",
    efficiency_loss: "效率損失",
    loss_over_threshold: "損耗超標",
    labor_cost_missing: "人工費率缺漏",
    unknown: "生產提醒"
  },
  capacityStatus: {
    configured: "已設定",
    missing_config: "缺少設定",
    closed: "休線",
    disabled: "停用",
    unknown: "未知"
  },
  changeoverStatus: {
    deferred: "待下一版實作",
    unknown: "未知"
  },
  deliveryRisk: {
    normal: "正常",
    high_risk: "高風險",
    unknown: "未判定"
  },
  department: {
    "1": "業務",
    "2": "研發",
    "3": "採購",
    "4": "生管",
    "5": "製造",
    "6": "品保",
    "7": "倉庫",
    "8": "物流",
    "9": "財務",
    unknown: "待指派"
  },
  machineAction: {
    "1": "啟動",
    "2": "暫停",
    "3": "停止",
    unknown: "未知"
  },
  machineStatus: {
    running: "運轉中",
    paused: "暫停",
    stopped: "停止",
    unknown: "未知"
  },
  materialStatus: {
    ready: "足夠",
    partial: "待補料",
    unknown: "未知"
  },
  process: {
    "0": "其他",
    "1": "前備",
    "2": "加工",
    "3": "包裝",
    unknown: "製程"
  },
  qualityStatus: {
    deferred: "待下一版實作",
    unknown: "未知"
  },
  readinessSignal: {
    material: "備料",
    staff: "人員",
    unknown: "準備狀態"
  },
  readinessStatus: {
    ready: "可用",
    attention: "需注意",
    unknown: "未知"
  },
  staffStatus: {
    ready: "足夠",
    support_needed: "需支援",
    shortage: "不足",
    unknown: "未知"
  },
  status: {
    scheduled: "已排程",
    material_ready: "備料完成",
    running: "生產中",
    paused: "暫停",
    pending_inventory: "待入庫",
    completed: "完成",
    unknown: "未知"
  },
  unit: {
    "0": "其他",
    "1": "公克",
    "2": "公斤",
    "3": "台斤",
    "51": "公分",
    "52": "公尺",
    "101": "個",
    "102": "條",
    "103": "片",
    "104": "張",
    "105": "罐",
    "106": "包",
    "107": "捲",
    "108": "桶",
    "109": "盒",
    "110": "組",
    "111": "箱",
    "112": "支",
    "113": "式",
    "114": "入",
    "115": "袋",
    "116": "顆",
    "117": "瓶",
    "201": "板",
    "202": "件",
    "203": "車",
    "204": "次",
    unknown: "單位"
  },
  workflowStep: {
    order: "訂單",
    aps: "APS",
    work_order: "工單",
    material: "備料",
    production: "生產",
    quality: "品檢",
    inventory: "入庫",
    output: "產出",
    labor: "人員",
    machine: "機台",
    document: "單據",
    unknown: "流程"
  }
};

const en: Record<ProductionEnumKind, EnumDictionary> = {
  alertType: {
    material_shortage: "Material shortage",
    staff_shortage: "Staff shortage",
    capacity_bottleneck: "Capacity bottleneck",
    capacity_config_missing: "Missing capacity config",
    capacity_downtime: "Line downtime",
    schedule_delay: "Schedule delay",
    efficiency_loss: "Efficiency loss",
    loss_over_threshold: "Loss over threshold",
    labor_cost_missing: "Missing labor rate",
    unknown: "Production alert"
  },
  capacityStatus: {
    configured: "Configured",
    missing_config: "Missing config",
    closed: "Closed",
    disabled: "Disabled",
    unknown: "Unknown"
  },
  changeoverStatus: {
    deferred: "Deferred",
    unknown: "Unknown"
  },
  deliveryRisk: {
    normal: "Normal",
    high_risk: "High risk",
    unknown: "Unknown"
  },
  department: {
    "1": "Sales",
    "2": "R&D",
    "3": "Purchasing",
    "4": "Planning",
    "5": "Manufacturing",
    "6": "Quality",
    "7": "Warehouse",
    "8": "Logistics",
    "9": "Finance",
    unknown: "Unassigned"
  },
  machineAction: {
    "1": "Start",
    "2": "Pause",
    "3": "Stop",
    unknown: "Unknown"
  },
  machineStatus: {
    running: "Running",
    paused: "Paused",
    stopped: "Stopped",
    unknown: "Unknown"
  },
  materialStatus: {
    ready: "Ready",
    partial: "Partial",
    unknown: "Unknown"
  },
  process: {
    "0": "Other",
    "1": "Preparation",
    "2": "Processing",
    "3": "Packaging",
    unknown: "Process"
  },
  qualityStatus: {
    deferred: "Deferred",
    unknown: "Unknown"
  },
  readinessSignal: {
    material: "Material",
    staff: "Staff",
    unknown: "Readiness"
  },
  readinessStatus: {
    ready: "Ready",
    attention: "Attention",
    unknown: "Unknown"
  },
  staffStatus: {
    ready: "Ready",
    support_needed: "Needs support",
    shortage: "Shortage",
    unknown: "Unknown"
  },
  status: {
    scheduled: "Scheduled",
    material_ready: "Material ready",
    running: "Running",
    paused: "Paused",
    pending_inventory: "Pending inventory",
    completed: "Completed",
    unknown: "Unknown"
  },
  unit: {
    ...zhTW.unit,
    unknown: "Unit"
  },
  workflowStep: {
    order: "Order",
    aps: "APS",
    work_order: "Work order",
    material: "Material",
    production: "Production",
    quality: "Quality",
    inventory: "Inventory",
    output: "Output",
    labor: "Labor",
    machine: "Machine",
    document: "Document",
    unknown: "Workflow"
  }
};

const ja: Record<ProductionEnumKind, EnumDictionary> = {
  ...en,
  alertType: {
    ...en.alertType,
    material_shortage: "材料不足",
    staff_shortage: "人員不足",
    capacity_bottleneck: "能力ボトルネック",
    unknown: "生産アラート"
  },
  status: {
    scheduled: "計画済",
    material_ready: "材料準備完了",
    running: "生産中",
    paused: "一時停止",
    pending_inventory: "入庫待ち",
    completed: "完了",
    unknown: "不明"
  }
};

const vi: Record<ProductionEnumKind, EnumDictionary> = {
  ...en,
  alertType: {
    ...en.alertType,
    material_shortage: "Thiếu vật tư",
    staff_shortage: "Thiếu nhân sự",
    capacity_bottleneck: "Nghẽn công suất",
    unknown: "Cảnh báo sản xuất"
  },
  status: {
    scheduled: "Đã lập lịch",
    material_ready: "Vật tư sẵn sàng",
    running: "Đang sản xuất",
    paused: "Tạm dừng",
    pending_inventory: "Chờ nhập kho",
    completed: "Hoàn tất",
    unknown: "Không rõ"
  }
};

const enumDictionaries: Record<LanguageCode, Record<ProductionEnumKind, EnumDictionary>> = {
  "zh-TW": zhTW,
  en,
  ja,
  vi
};

export function productionEnumLabel(
  kind: ProductionEnumKind,
  value: number | string | undefined,
  language: LanguageCode
) {
  const key = value === undefined || value === null || value === "" ? "unknown" : String(value);
  const selected = enumDictionaries[language][kind];
  const fallback = enumDictionaries[defaultLanguage][kind];

  return selected[key] ?? selected.unknown ?? fallback[key] ?? fallback.unknown ?? key;
}

export function productionRiskTone(risk?: string, riskLevel?: number): StatusTone {
  if (risk === "high_risk" || (riskLevel ?? 0) >= 3) {
    return "danger";
  }
  if (risk === "unknown" || (riskLevel ?? 0) >= 2) {
    return "warning";
  }
  if ((riskLevel ?? 0) >= 1) {
    return "info";
  }
  return "success";
}

export function productionStatusTone(status?: string, riskLevel?: number): StatusTone {
  if (status === "shortage" || status === "stopped" || status === "blocked" || (riskLevel ?? 0) >= 3) {
    return "danger";
  }
  if (
    status === "partial" ||
    status === "support_needed" ||
    status === "paused" ||
    status === "pending_inventory" ||
    status === "attention" ||
    (riskLevel ?? 0) >= 2
  ) {
    return "warning";
  }
  if (status === "ready" || status === "running" || status === "completed" || status === "configured") {
    return "success";
  }
  return "info";
}
