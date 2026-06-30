import { defaultLanguage, type LanguageCode } from "@/i18n/dictionary";
import type { StatusTone } from "@/types/dashboard";

type EnumDictionary = Record<string, string>;

type WarehouseEnumKind =
  | "department"
  | "eventCode"
  | "itemCategory"
  | "laneCode"
  | "nextActionCode"
  | "refCategory"
  | "riskLevel"
  | "riskType"
  | "taskStatus"
  | "taskType"
  | "unit";

const enumDictionaries: Record<LanguageCode, Record<WarehouseEnumKind, EnumDictionary>> = {
  "zh-TW": {
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
    eventCode: {
      "workflow.task.created": "任務建立",
      "workflow.task.assigned": "任務指派",
      "workflow.task.started": "開始處理",
      "workflow.task.partiallyProcessed": "部分處理",
      "workflow.task.blocked": "任務阻塞",
      "workflow.task.blockResolved": "阻塞解除",
      "workflow.task.completed": "任務完成",
      "workflow.task.cancelled": "任務取消",
      "workflow.task.refLinked": "關聯單據",
      "workflow.task.quantityAdjusted": "數量調整",
      unknown: "任務事件"
    },
    itemCategory: {
      "0": "其他",
      "1": "原料",
      "2": "物料",
      "3": "膠捲",
      "4": "在製品",
      "5": "製成品",
      "6": "貨品",
      unknown: "其他"
    },
    laneCode: {
      inbound: "入庫",
      outbound: "出庫",
      quality: "品檢",
      shipment: "出貨",
      blocked: "阻塞",
      all: "全部",
      unknown: "任務"
    },
    nextActionCode: {
      "warehouse.task.resolveBlocker": "解除阻塞",
      "warehouse.task.confirmReceipt": "確認收貨",
      "warehouse.task.arrangeInbound": "安排入庫",
      "warehouse.task.prepareOutbound": "準備出庫",
      "warehouse.task.arrangeTransfer": "安排移倉",
      "warehouse.task.waitQualityDecision": "等待品檢判定",
      "warehouse.task.prepareShipment": "準備出貨",
      unknown: "確認下一步"
    },
    refCategory: {
      "0": "其他",
      "1": "採購",
      "2": "生產",
      "3": "銷售",
      unknown: "來源"
    },
    riskLevel: {
      "0": "正常",
      "1": "正常",
      "2": "注意",
      "3": "高風險",
      unknown: "未分級"
    },
    riskType: {
      OVERDUE: "逾期",
      BLOCKED: "阻塞",
      INVENTORY_SHORTAGE: "庫存不足",
      QUALITY_HOLD: "品檢保留",
      BATCH_NOT_ASSIGNED: "未指定批號",
      unknown: "風險"
    },
    taskStatus: {
      "1": "待處理",
      "2": "部分完成",
      "3": "已完成",
      "4": "阻塞",
      "5": "取消",
      pending: "待處理",
      partial: "部分完成",
      blocked: "阻塞",
      done: "已完成",
      cancelled: "取消",
      unknown: "待處理"
    },
    taskType: {
      "0": "其他",
      "1": "請購",
      "2": "採購",
      "3": "進貨",
      "4": "入庫",
      "5": "出庫",
      "6": "移倉",
      "7": "生產",
      "8": "品檢",
      "9": "出貨",
      unknown: "任務"
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
    }
  },
  en: {
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
    eventCode: {
      "workflow.task.created": "Task created",
      "workflow.task.assigned": "Assigned",
      "workflow.task.started": "Started",
      "workflow.task.partiallyProcessed": "Partially processed",
      "workflow.task.blocked": "Blocked",
      "workflow.task.blockResolved": "Block resolved",
      "workflow.task.completed": "Completed",
      "workflow.task.cancelled": "Cancelled",
      "workflow.task.refLinked": "Reference linked",
      "workflow.task.quantityAdjusted": "Quantity adjusted",
      unknown: "Task event"
    },
    itemCategory: {
      "0": "Other",
      "1": "Raw material",
      "2": "Material",
      "3": "Film",
      "4": "Work in process",
      "5": "Finished goods",
      "6": "Goods",
      unknown: "Other"
    },
    laneCode: {
      inbound: "Inbound",
      outbound: "Outbound",
      quality: "Quality",
      shipment: "Shipment",
      blocked: "Blocked",
      all: "All",
      unknown: "Tasks"
    },
    nextActionCode: {
      "warehouse.task.resolveBlocker": "Resolve blocker",
      "warehouse.task.confirmReceipt": "Confirm receipt",
      "warehouse.task.arrangeInbound": "Arrange inbound",
      "warehouse.task.prepareOutbound": "Prepare outbound",
      "warehouse.task.arrangeTransfer": "Arrange transfer",
      "warehouse.task.waitQualityDecision": "Wait for quality decision",
      "warehouse.task.prepareShipment": "Prepare shipment",
      unknown: "Confirm next step"
    },
    refCategory: {
      "0": "Other",
      "1": "Purchasing",
      "2": "Production",
      "3": "Sales",
      unknown: "Reference"
    },
    riskLevel: {
      "0": "Normal",
      "1": "Normal",
      "2": "Attention",
      "3": "High risk",
      unknown: "Unrated"
    },
    riskType: {
      OVERDUE: "Overdue",
      BLOCKED: "Blocked",
      INVENTORY_SHORTAGE: "Inventory shortage",
      QUALITY_HOLD: "Quality hold",
      BATCH_NOT_ASSIGNED: "Batch not assigned",
      unknown: "Risk"
    },
    taskStatus: {
      "1": "Pending",
      "2": "Partial",
      "3": "Done",
      "4": "Blocked",
      "5": "Cancelled",
      pending: "Pending",
      partial: "Partial",
      blocked: "Blocked",
      done: "Done",
      cancelled: "Cancelled",
      unknown: "Pending"
    },
    taskType: {
      "0": "Other",
      "1": "Requisition",
      "2": "Purchase",
      "3": "Receiving",
      "4": "Inbound",
      "5": "Outbound",
      "6": "Transfer",
      "7": "Production",
      "8": "Quality",
      "9": "Shipment",
      unknown: "Task"
    },
    unit: {
      "0": "Other",
      "1": "g",
      "2": "kg",
      "3": "catty",
      "51": "cm",
      "52": "m",
      "101": "pcs",
      "102": "strip",
      "103": "sheet",
      "104": "sheet",
      "105": "can",
      "106": "pack",
      "107": "roll",
      "108": "barrel",
      "109": "box",
      "110": "set",
      "111": "case",
      "112": "stick",
      "113": "set",
      "114": "entry",
      "115": "bag",
      "116": "piece",
      "117": "bottle",
      "201": "pallet",
      "202": "item",
      "203": "truck",
      "204": "time",
      unknown: "unit"
    }
  },
  ja: {
    department: {
      "1": "営業",
      "2": "研究開発",
      "3": "購買",
      "4": "生産管理",
      "5": "製造",
      "6": "品質保証",
      "7": "倉庫",
      "8": "物流",
      "9": "財務",
      unknown: "未割当"
    },
    eventCode: {
      "workflow.task.created": "タスク作成",
      "workflow.task.assigned": "割当",
      "workflow.task.started": "開始",
      "workflow.task.partiallyProcessed": "一部処理",
      "workflow.task.blocked": "ブロック",
      "workflow.task.blockResolved": "ブロック解除",
      "workflow.task.completed": "完了",
      "workflow.task.cancelled": "取消",
      "workflow.task.refLinked": "関連伝票",
      "workflow.task.quantityAdjusted": "数量調整",
      unknown: "タスクイベント"
    },
    itemCategory: {
      "0": "その他",
      "1": "原料",
      "2": "資材",
      "3": "フィルム",
      "4": "仕掛品",
      "5": "製品",
      "6": "商品",
      unknown: "その他"
    },
    laneCode: {
      inbound: "入庫",
      outbound: "出庫",
      quality: "品質",
      shipment: "出荷",
      blocked: "ブロック",
      all: "すべて",
      unknown: "タスク"
    },
    nextActionCode: {
      "warehouse.task.resolveBlocker": "ブロック解除",
      "warehouse.task.confirmReceipt": "受領確認",
      "warehouse.task.arrangeInbound": "入庫手配",
      "warehouse.task.prepareOutbound": "出庫準備",
      "warehouse.task.arrangeTransfer": "移動手配",
      "warehouse.task.waitQualityDecision": "品質判定待ち",
      "warehouse.task.prepareShipment": "出荷準備",
      unknown: "次の対応確認"
    },
    refCategory: {
      "0": "その他",
      "1": "購買",
      "2": "生産",
      "3": "販売",
      unknown: "参照"
    },
    riskLevel: {
      "0": "正常",
      "1": "正常",
      "2": "注意",
      "3": "高リスク",
      unknown: "未分類"
    },
    riskType: {
      OVERDUE: "期限超過",
      BLOCKED: "ブロック",
      INVENTORY_SHORTAGE: "在庫不足",
      QUALITY_HOLD: "品質保留",
      BATCH_NOT_ASSIGNED: "ロット未指定",
      unknown: "リスク"
    },
    taskStatus: {
      "1": "未処理",
      "2": "一部完了",
      "3": "完了",
      "4": "ブロック",
      "5": "取消",
      pending: "未処理",
      partial: "一部完了",
      blocked: "ブロック",
      done: "完了",
      cancelled: "取消",
      unknown: "未処理"
    },
    taskType: {
      "0": "その他",
      "1": "購買依頼",
      "2": "購買",
      "3": "入荷",
      "4": "入庫",
      "5": "出庫",
      "6": "移動",
      "7": "生産",
      "8": "品質",
      "9": "出荷",
      unknown: "タスク"
    },
    unit: {
      "0": "その他",
      "1": "g",
      "2": "kg",
      "3": "斤",
      "51": "cm",
      "52": "m",
      "101": "個",
      "102": "本",
      "103": "枚",
      "104": "枚",
      "105": "缶",
      "106": "包",
      "107": "巻",
      "108": "桶",
      "109": "箱",
      "110": "組",
      "111": "ケース",
      "112": "本",
      "113": "式",
      "114": "入",
      "115": "袋",
      "116": "粒",
      "117": "瓶",
      "201": "パレット",
      "202": "件",
      "203": "車",
      "204": "回",
      unknown: "単位"
    }
  },
  vi: {
    department: {
      "1": "Kinh doanh",
      "2": "R&D",
      "3": "Mua hàng",
      "4": "Kế hoạch",
      "5": "Sản xuất",
      "6": "Chất lượng",
      "7": "Kho",
      "8": "Vận chuyển",
      "9": "Tài chính",
      unknown: "Chưa phân công"
    },
    eventCode: {
      "workflow.task.created": "Tạo nhiệm vụ",
      "workflow.task.assigned": "Phân công",
      "workflow.task.started": "Bắt đầu",
      "workflow.task.partiallyProcessed": "Xử lý một phần",
      "workflow.task.blocked": "Bị chặn",
      "workflow.task.blockResolved": "Đã gỡ chặn",
      "workflow.task.completed": "Hoàn tất",
      "workflow.task.cancelled": "Hủy",
      "workflow.task.refLinked": "Liên kết chứng từ",
      "workflow.task.quantityAdjusted": "Điều chỉnh số lượng",
      unknown: "Sự kiện nhiệm vụ"
    },
    itemCategory: {
      "0": "Khác",
      "1": "Nguyên liệu",
      "2": "Vật tư",
      "3": "Màng cuộn",
      "4": "Bán thành phẩm",
      "5": "Thành phẩm",
      "6": "Hàng hóa",
      unknown: "Khác"
    },
    laneCode: {
      inbound: "Nhập kho",
      outbound: "Xuất kho",
      quality: "Chất lượng",
      shipment: "Giao hàng",
      blocked: "Bị chặn",
      all: "Tất cả",
      unknown: "Nhiệm vụ"
    },
    nextActionCode: {
      "warehouse.task.resolveBlocker": "Gỡ chặn",
      "warehouse.task.confirmReceipt": "Xác nhận nhận hàng",
      "warehouse.task.arrangeInbound": "Sắp xếp nhập kho",
      "warehouse.task.prepareOutbound": "Chuẩn bị xuất kho",
      "warehouse.task.arrangeTransfer": "Sắp xếp chuyển kho",
      "warehouse.task.waitQualityDecision": "Chờ quyết định chất lượng",
      "warehouse.task.prepareShipment": "Chuẩn bị giao hàng",
      unknown: "Xác nhận bước tiếp theo"
    },
    refCategory: {
      "0": "Khác",
      "1": "Mua hàng",
      "2": "Sản xuất",
      "3": "Bán hàng",
      unknown: "Nguồn"
    },
    riskLevel: {
      "0": "Bình thường",
      "1": "Bình thường",
      "2": "Cần chú ý",
      "3": "Rủi ro cao",
      unknown: "Chưa phân loại"
    },
    riskType: {
      OVERDUE: "Quá hạn",
      BLOCKED: "Bị chặn",
      INVENTORY_SHORTAGE: "Thiếu tồn kho",
      QUALITY_HOLD: "Giữ chất lượng",
      BATCH_NOT_ASSIGNED: "Chưa gán lô",
      unknown: "Rủi ro"
    },
    taskStatus: {
      "1": "Chờ xử lý",
      "2": "Hoàn tất một phần",
      "3": "Hoàn tất",
      "4": "Bị chặn",
      "5": "Hủy",
      pending: "Chờ xử lý",
      partial: "Hoàn tất một phần",
      blocked: "Bị chặn",
      done: "Hoàn tất",
      cancelled: "Hủy",
      unknown: "Chờ xử lý"
    },
    taskType: {
      "0": "Khác",
      "1": "Yêu cầu mua",
      "2": "Mua hàng",
      "3": "Nhận hàng",
      "4": "Nhập kho",
      "5": "Xuất kho",
      "6": "Chuyển kho",
      "7": "Sản xuất",
      "8": "Chất lượng",
      "9": "Giao hàng",
      unknown: "Nhiệm vụ"
    },
    unit: {
      "0": "Khác",
      "1": "g",
      "2": "kg",
      "3": "catty",
      "51": "cm",
      "52": "m",
      "101": "cái",
      "102": "thanh",
      "103": "tấm",
      "104": "tờ",
      "105": "lon",
      "106": "gói",
      "107": "cuộn",
      "108": "thùng",
      "109": "hộp",
      "110": "bộ",
      "111": "kiện",
      "112": "cây",
      "113": "bộ",
      "114": "lần",
      "115": "túi",
      "116": "viên",
      "117": "chai",
      "201": "pallet",
      "202": "món",
      "203": "xe",
      "204": "lần",
      unknown: "đơn vị"
    }
  }
};

export function warehouseEnumLabel(kind: WarehouseEnumKind, value: number | string | undefined, language: LanguageCode) {
  const key = value === undefined || value === null || value === "" ? "unknown" : String(value);
  const selected = enumDictionaries[language][kind];
  const fallback = enumDictionaries[defaultLanguage][kind];

  return selected[key] ?? selected.unknown ?? fallback[key] ?? fallback.unknown ?? key;
}

export function warehouseRiskTone(riskLevel?: number, riskTypes: string[] = []): StatusTone {
  if (riskLevel === 3 || riskTypes.includes("OVERDUE") || riskTypes.includes("BLOCKED")) {
    return "danger";
  }
  if (riskLevel === 2 || riskTypes.length > 0) {
    return "warning";
  }
  return "success";
}

export function warehouseTaskStatusTone(status?: number | string): StatusTone {
  if (status === 4 || status === "blocked") {
    return "danger";
  }
  if (status === 2 || status === "partial") {
    return "warning";
  }
  if (status === 3 || status === "done") {
    return "success";
  }
  return "info";
}

export function warehouseLaneTone(laneCode?: string): StatusTone {
  if (laneCode === "blocked") {
    return "danger";
  }
  if (laneCode === "quality") {
    return "warning";
  }
  if (laneCode === "inbound") {
    return "success";
  }
  return "info";
}
