import { warehouseEnumLabel, warehouseRiskTone, warehouseTaskStatusTone } from "@/i18n/warehouse-enums";
import type { StatusTone } from "@/types/dashboard";
import type { BatchRiskLevelCode } from "@/types/batches";

type Dictionary = Record<string, string>;

const locale = "zh-TW";

const riskLevelLabels: Record<BatchRiskLevelCode, string> = {
  normal: "正常",
  attention: "注意",
  high_risk: "高風險",
  unknown: "未分級"
};

const riskLabels: Dictionary = {
  normal: "正常",
  expired: "已逾期",
  near_expiry: "即期",
  quality_hold: "品檢保留",
  reserved: "已預留",
  stock_shortage: "庫存不足",
  workflow_blocked: "流程阻塞",
  unknown: "待確認"
};

const qaStatusLabels: Dictionary = {
  released: "已放行",
  inspection: "檢驗中",
  quality_hold: "品檢保留",
  blocked: "阻擋",
  unknown: "待確認"
};

const batchStageLabels: Dictionary = {
  inbound_pending: "待入庫",
  stocked: "已入庫",
  available: "可用",
  reserved: "已預留",
  quality_hold: "品檢保留",
  production_input: "生產投入",
  production_output: "生產產出",
  shipped: "已出貨",
  unknown: "待確認"
};

const itemTypeLabels: Dictionary = {
  "0": "其他",
  "1": "新料",
  "2": "餘料",
  "3": "廢料",
  unknown: "其他"
};

const inventoryCategoryLabels: Dictionary = {
  "1": "入庫",
  "2": "出庫",
  unknown: "出入庫"
};

const inventorySourceLabels: Dictionary = {
  "0": "其他",
  "1": "採購",
  "2": "生產",
  "3": "銷售",
  "4": "移倉",
  "5": "盤點",
  unknown: "來源"
};

const reservationStatusLabels: Dictionary = {
  "0": "待確認",
  "1": "有效",
  "2": "部分使用",
  "3": "已完成",
  "4": "已取消",
  unknown: "待確認"
};

const qualityHoldStatusLabels: Dictionary = {
  "0": "待確認",
  "1": "保留中",
  "2": "已放行",
  "3": "已阻擋",
  "4": "已取消",
  unknown: "待確認"
};

const qualityHoldReasonLabels: Dictionary = {
  inspection: "檢驗中",
  quality_issue: "品質異常",
  document_missing: "文件待補",
  customer_hold: "客戶保留",
  unknown: "待確認"
};

const palletStatusLabels: Dictionary = {
  "0": "待確認",
  "1": "在庫",
  "2": "移動中",
  "3": "已清空",
  unknown: "待確認"
};

function dictLabel(dictionary: Dictionary, value: number | string | undefined) {
  const key = value === undefined || value === null || value === "" ? "unknown" : String(value);
  return dictionary[key] ?? dictionary.unknown ?? key;
}

export function normalizeBatchRiskLevel(value?: string): BatchRiskLevelCode {
  if (value === "normal" || value === "attention" || value === "high_risk") {
    return value;
  }
  return "unknown";
}

export function batchRiskLevelLabel(value?: string) {
  return riskLevelLabels[normalizeBatchRiskLevel(value)];
}

export function batchRiskLevelTone(value?: string): StatusTone {
  if (value === "high_risk") {
    return "danger";
  }
  if (value === "attention") {
    return "warning";
  }
  if (value === "normal") {
    return "success";
  }
  return "neutral";
}

export function batchRiskLabel(value?: string) {
  return dictLabel(riskLabels, value);
}

export function batchQaStatusLabel(value?: string) {
  return dictLabel(qaStatusLabels, value);
}

export function batchStageLabel(value?: string) {
  return dictLabel(batchStageLabels, value);
}

export function batchItemCategoryLabel(value?: number) {
  return warehouseEnumLabel("itemCategory", value, locale);
}

export function batchItemTypeLabel(value?: number) {
  return dictLabel(itemTypeLabels, value);
}

export function batchUnitLabel(value?: number) {
  return warehouseEnumLabel("unit", value, locale);
}

export function batchDepartmentLabel(value?: number) {
  return warehouseEnumLabel("department", value, locale);
}

export function batchRefCategoryLabel(value?: number) {
  return warehouseEnumLabel("refCategory", value, locale);
}

export function batchTaskTypeLabel(value?: number) {
  return warehouseEnumLabel("taskType", value, locale);
}

export function batchTaskStatusLabel(value?: number) {
  return warehouseEnumLabel("taskStatus", value, locale);
}

export function batchTaskStatusTone(value?: number): StatusTone {
  return warehouseTaskStatusTone(value);
}

export function batchInventoryCategoryLabel(value?: number) {
  return dictLabel(inventoryCategoryLabels, value);
}

export function batchInventorySourceLabel(value?: number) {
  return dictLabel(inventorySourceLabels, value);
}

export function batchReservationStatusLabel(value?: number) {
  return dictLabel(reservationStatusLabels, value);
}

export function batchQualityHoldStatusLabel(value?: number) {
  return dictLabel(qualityHoldStatusLabels, value);
}

export function batchQualityHoldReasonLabel(value?: string) {
  return dictLabel(qualityHoldReasonLabels, value);
}

export function batchPalletStatusLabel(value?: number) {
  return dictLabel(palletStatusLabels, value);
}

export function batchRiskTone(riskLevelCode?: string, riskCodes: string[] = []): StatusTone {
  const normalized = normalizeBatchRiskLevel(riskLevelCode);
  if (normalized !== "unknown") {
    return batchRiskLevelTone(normalized);
  }
  return warehouseRiskTone(undefined, riskCodes);
}
