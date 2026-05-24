import type { PlanningCase, PlanningDashboardData, PlanningSummary } from "@/types/planning";

export const planningSummary: PlanningSummary[] = [
  {
    label: "待計劃訂單",
    value: "12",
    hint: "高優先 4 張",
    tone: "info"
  },
  {
    label: "需請購料品",
    value: "9",
    hint: "今日需確認 5 項",
    tone: "warning"
  },
  {
    label: "產能衝突",
    value: "3",
    hint: "B2 冷凍線最吃緊",
    tone: "danger"
  },
  {
    label: "可建立工單",
    value: "7",
    hint: "2 張需主管確認",
    tone: "success"
  }
];

export const planningCases: PlanningCase[] = [
  {
    id: "PLAN-20260523-018",
    sourceOrder: "SO-20260523-018",
    customer: "全聯中區 DC",
    product: "咖哩雞肉調理包",
    itemNo: "FG-CURRY-101",
    quantity: 12000,
    unit: "盒",
    dueDate: "2026-05-24",
    promisedDate: "2026-05-24",
    decision: "可執行",
    tone: "success",
    priority: "高",
    owner: "計劃一組",
    planningNote: "庫存可先出 7,220 盒，剩餘量由 A1 今日工單補足，無需新增請購。",
    materialShortageValue: 0,
    requiredProductionHours: 5.5,
    availableProductionHours: 8,
    purchaseRequestCount: 0,
    suggestedWorkOrderCount: 1,
    checks: [
      { area: "訂單需求", status: "已確認", note: "需求量 12,000 盒，交期 2026-05-24", tone: "success" },
      { area: "BOM 展開", status: "完成", note: "主料、包材與標籤需求已展開", tone: "success" },
      { area: "庫存/批號", status: "足夠", note: "可用庫存與今日產出可覆蓋需求", tone: "success" },
      { area: "產能", status: "可排入", note: "A1 線仍有 2.5 小時緩衝", tone: "success" },
      { area: "品保/出貨", status: "可銜接", note: "首件檢驗正常，冷鏈車次已預排", tone: "success" }
    ],
    materials: [
      { itemNo: "RM-CHICKEN-001", itemName: "雞腿肉丁", category: "原料", requiredQty: 420, availableQty: 680, shortageQty: 0, unit: "kg", requiredDate: "2026-05-23", suggestedAction: "直接備料", tone: "success" },
      { itemNo: "PK-CURRY-BOX", itemName: "咖哩調理包外盒", category: "包材", requiredQty: 4800, availableQty: 6200, shortageQty: 0, unit: "個", requiredDate: "2026-05-23", suggestedAction: "直接備料", tone: "success" }
    ],
    capacity: [
      { processType: "調理", line: "A1 調理包產線", requiredHours: 5.5, availableHours: 8, changeoverMinutes: 35, staffRequired: 8, staffAssigned: 8, status: "可排入", tone: "success" },
      { processType: "包裝", line: "C3 包裝線", requiredHours: 3, availableHours: 4, changeoverMinutes: 20, staffRequired: 6, staffAssigned: 7, status: "可排入", tone: "success" }
    ],
    workOrders: [
      { workOrderNo: "WO-20260523-001", line: "A1 調理包產線", startTime: "10:00", endTime: "14:30", quantity: 4780, unit: "盒", status: "可排入", tone: "success" }
    ]
  },
  {
    id: "PLAN-20260523-022",
    sourceOrder: "SO-20260523-022",
    customer: "便利商店北區",
    product: "綜合冷凍蔬菜",
    itemNo: "FG-VEG-207",
    quantity: 7200,
    unit: "包",
    dueDate: "2026-05-24",
    promisedDate: "2026-05-25",
    decision: "不可執行",
    tone: "danger",
    priority: "高",
    owner: "計劃二組",
    planningNote: "冷凍玉米粒缺料且品質文件未放行，B2 產線人員不足；需先請購/補文件並重排工單。",
    materialShortageValue: 86000,
    requiredProductionHours: 7.5,
    availableProductionHours: 4,
    purchaseRequestCount: 2,
    suggestedWorkOrderCount: 1,
    checks: [
      { area: "訂單需求", status: "已確認", note: "客戶要求 2026-05-24 出貨", tone: "success" },
      { area: "BOM 展開", status: "完成", note: "冷凍玉米粒與包材有缺口", tone: "warning" },
      { area: "庫存/批號", status: "不足", note: "可用原料不足，部分批號受品質文件阻擋", tone: "danger" },
      { area: "採購請購", status: "需建立", note: "需產生 2 張請購建議", tone: "warning" },
      { area: "產能", status: "衝突", note: "B2 線今日可用 4 小時，不足 3.5 小時", tone: "danger" },
      { area: "人員", status: "需支援", note: "晚班需跨線支援 2 人", tone: "warning" }
    ],
    materials: [
      { itemNo: "RM-CORN-001", itemName: "冷凍玉米粒", category: "原料", requiredQty: 520, availableQty: 180, shortageQty: 340, unit: "kg", requiredDate: "2026-05-23", suggestedAction: "請購", tone: "danger" },
      { itemNo: "PK-VEG-BAG", itemName: "冷凍蔬菜包裝袋", category: "包材", requiredQty: 7200, availableQty: 6100, shortageQty: 1100, unit: "個", requiredDate: "2026-05-23", suggestedAction: "請購", tone: "warning" },
      { itemNo: "RM-CARROT-002", itemName: "冷凍紅蘿蔔丁", category: "原料", requiredQty: 280, availableQty: 420, shortageQty: 0, unit: "kg", requiredDate: "2026-05-23", suggestedAction: "直接備料", tone: "success" }
    ],
    capacity: [
      { processType: "冷凍", line: "B2 冷凍蔬菜產線", requiredHours: 7.5, availableHours: 4, changeoverMinutes: 45, staffRequired: 7, staffAssigned: 5, status: "衝突", tone: "danger" },
      { processType: "包裝", line: "C2 包裝線", requiredHours: 3.5, availableHours: 5, changeoverMinutes: 25, staffRequired: 5, staffAssigned: 5, status: "可排入", tone: "success" }
    ],
    workOrders: [
      { workOrderNo: "WO-建議-20260523-022", line: "B2 冷凍蔬菜產線", startTime: "待排", endTime: "待排", quantity: 7200, unit: "包", status: "需調整", tone: "warning" }
    ]
  },
  {
    id: "PLAN-20260523-027",
    sourceOrder: "SO-20260523-027",
    customer: "餐飲通路南區",
    product: "即食雞胸肉",
    itemNo: "FG-CHICKEN-315",
    quantity: 4800,
    unit: "包",
    dueDate: "2026-05-23",
    promisedDate: "2026-05-23",
    decision: "需協調",
    tone: "warning",
    priority: "中",
    owner: "計劃一組",
    planningNote: "工單已完成，主要阻擋在品檢待判；計劃中心需同步提醒訂單與物流暫緩出貨。",
    materialShortageValue: 0,
    requiredProductionHours: 0,
    availableProductionHours: 0,
    purchaseRequestCount: 0,
    suggestedWorkOrderCount: 0,
    checks: [
      { area: "訂單需求", status: "已確認", note: "今日交付，出貨需等待 QC 放行", tone: "warning" },
      { area: "BOM 展開", status: "完成", note: "工單已完成，不需追加物料", tone: "success" },
      { area: "庫存/批號", status: "待放行", note: "成品尚未成為可出貨庫存", tone: "warning" },
      { area: "品保/出貨", status: "阻擋", note: "微生物快篩待判，暫緩入庫與出貨", tone: "warning" }
    ],
    materials: [
      { itemNo: "FG-CHICKEN-315", itemName: "即食雞胸肉成品", category: "原料", requiredQty: 4800, availableQty: 0, shortageQty: 0, unit: "包", requiredDate: "2026-05-23", suggestedAction: "品質放行後備料", tone: "warning" }
    ],
    capacity: [
      { processType: "包裝", line: "C3 包裝線", requiredHours: 0, availableHours: 0, changeoverMinutes: 0, staffRequired: 0, staffAssigned: 0, status: "已完成", tone: "success" }
    ],
    workOrders: [
      { workOrderNo: "WO-20260523-003", line: "C3 包裝線", startTime: "08:00", endTime: "11:40", quantity: 4800, unit: "包", status: "可排入", tone: "success" }
    ]
  }
];

export const planningDashboardMock: PlanningDashboardData = {
  summary: planningSummary,
  cases: planningCases
};
