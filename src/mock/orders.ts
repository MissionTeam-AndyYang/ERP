import type { OrderStatusSummary, OrdersDashboardData, SalesOrder } from "@/types/orders";

export const orderSummary: OrderStatusSummary[] = [
  {
    label: "可承諾訂單",
    value: "36",
    hint: "本週需交付 18 張",
    tone: "info"
  },
  {
    label: "交期高風險",
    value: "4",
    hint: "缺料 2、生產 1、品檢 1",
    tone: "danger"
  },
  {
    label: "生產可行性待協調",
    value: "7",
    hint: "需調整產能或人員",
    tone: "warning"
  },
  {
    label: "毛利需追蹤",
    value: "5",
    hint: "低於預估門檻",
    tone: "success"
  }
];

export const salesOrders: SalesOrder[] = [
  {
    id: "SO-20260523-018",
    customer: "全聯中區 DC",
    channel: "冷凍食品",
    product: "咖哩雞肉調理包",
    itemNo: "FG-CURRY-101",
    quantity: 12000,
    unit: "盒",
    orderAmount: 780000,
    estimatedCost: 612000,
    estimatedMarginRate: 21.5,
    actualMarginRate: 20.8,
    dueDate: "2026-05-24",
    shipDate: "2026-05-24",
    stage: "生產中",
    tone: "success",
    deliveryRisk: "正常",
    productionFeasibility: "可生產",
    riskReason: "工單進行中，料品與人員正常。",
    materialStatus: "已備齊",
    productionStatus: "WO-20260523-001 生產中",
    qualityStatus: "首件通過",
    shippingStatus: "已預排冷鏈車次",
    paymentStatus: "月結",
    owner: "業務一組",
    priority: "高",
    committedDate: "2026-05-24",
    commitmentDecision: "可承諾",
    commitmentChecks: [
      { area: "ATP 庫存", status: "部分可用", note: "製成品可用 7,220 盒，剩餘由今日工單補足", tone: "success" },
      { area: "物料缺口", status: "無缺口", note: "主要原料與包材已備齊", tone: "success" },
      { area: "產能", status: "可排入", note: "A1 線今日 14:30 前可完成剩餘量", tone: "success" },
      { area: "人員", status: "足夠", note: "A1 班表符合預排工單需求", tone: "success" },
      { area: "品質/出貨", status: "可銜接", note: "首件已通過，冷鏈車次已預排", tone: "success" }
    ],
    dependencies: [
      { area: "庫存", status: "可用", note: "製成品可用 7,220 盒", tone: "success" },
      { area: "生產", status: "進行中", note: "完成率 72%", tone: "info" },
      { area: "品檢", status: "正常", note: "首件與製程檢查正常", tone: "success" },
      { area: "出貨", status: "已排定", note: "2026-05-24 冷鏈配送", tone: "success" }
    ],
    workflow: [
      { label: "訂單", ref: "SO-20260523-018", status: "完成", tone: "success" },
      { label: "備料", ref: "PICK-20260523-004", status: "完成", tone: "success" },
      { label: "生產", ref: "WO-20260523-001", status: "進行中", tone: "info" },
      { label: "品檢", ref: "QC-20260523-006", status: "進行中", tone: "success" },
      { label: "出貨", ref: "SHIP-20260524-002", status: "待處理", tone: "info" },
      { label: "收款", ref: "AR-月結", status: "待處理", tone: "info" }
    ]
  },
  {
    id: "SO-20260523-022",
    customer: "便利商店北區",
    channel: "即食餐盒",
    product: "綜合冷凍蔬菜",
    itemNo: "FG-VEG-207",
    quantity: 7200,
    unit: "包",
    orderAmount: 396000,
    estimatedCost: 326000,
    estimatedMarginRate: 17.7,
    actualMarginRate: null,
    dueDate: "2026-05-24",
    shipDate: null,
    stage: "備料中",
    tone: "warning",
    deliveryRisk: "高風險",
    productionFeasibility: "不可如期",
    riskReason: "冷凍玉米粒短缺且 B2 產線人員需支援，若未補齊會影響開線。",
    materialStatus: "缺冷凍玉米粒",
    productionStatus: "WO-20260523-002 待備料",
    qualityStatus: "未開始",
    shippingStatus: "未排車",
    paymentStatus: "待出貨後請款",
    owner: "業務二組",
    priority: "高",
    committedDate: "2026-05-25",
    commitmentDecision: "不可承諾",
    commitmentChecks: [
      { area: "ATP 庫存", status: "不足", note: "成品無可用量，需重新生產", tone: "danger" },
      { area: "物料缺口", status: "缺料", note: "冷凍玉米粒可用量不足，且原料批號仍待品質放行", tone: "danger" },
      { area: "產能", status: "需重排", note: "B2 線 13:00 工單受缺料影響", tone: "warning" },
      { area: "人員", status: "需支援", note: "B2 線晚班需跨線支援 2 人", tone: "warning" },
      { area: "品質/出貨", status: "未確定", note: "待原料文件補齊後才能確認可生產日期", tone: "warning" }
    ],
    dependencies: [
      { area: "庫存", status: "不足", note: "冷凍玉米粒可用量不足", tone: "danger" },
      { area: "採購", status: "需確認", note: "需確認今日補料可能性", tone: "warning" },
      { area: "生產", status: "受阻", note: "B2 13:00 開線風險", tone: "danger" },
      { area: "出貨", status: "未排", note: "待生產確認後排車", tone: "warning" }
    ],
    workflow: [
      { label: "訂單", ref: "SO-20260523-022", status: "完成", tone: "success" },
      { label: "備料", ref: "PICK-20260523-007", status: "阻擋", tone: "danger" },
      { label: "生產", ref: "WO-20260523-002", status: "待處理", tone: "warning" },
      { label: "品檢", ref: "QC-待建立", status: "待處理", tone: "warning" },
      { label: "出貨", ref: "SHIP-待排", status: "待處理", tone: "warning" },
      { label: "收款", ref: "AR-待建立", status: "待處理", tone: "info" }
    ]
  },
  {
    id: "SO-20260523-027",
    customer: "餐飲通路南區",
    channel: "團膳",
    product: "即食雞胸肉",
    itemNo: "FG-CHICKEN-315",
    quantity: 4800,
    unit: "包",
    orderAmount: 336000,
    estimatedCost: 282000,
    estimatedMarginRate: 16.1,
    actualMarginRate: 14.6,
    dueDate: "2026-05-23",
    shipDate: null,
    stage: "品檢中",
    tone: "info",
    deliveryRisk: "注意",
    productionFeasibility: "需協調",
    riskReason: "品檢待判，暫緩入庫與出貨。",
    materialStatus: "已備齊",
    productionStatus: "WO-20260523-003 生產完成",
    qualityStatus: "微生物快篩待判",
    shippingStatus: "暫緩出貨",
    paymentStatus: "待出貨後請款",
    owner: "業務三組",
    priority: "中",
    committedDate: "2026-05-23",
    commitmentDecision: "需協調",
    commitmentChecks: [
      { area: "ATP 庫存", status: "待放行", note: "成品已完成但尚未成為可出貨庫存", tone: "warning" },
      { area: "物料缺口", status: "無缺口", note: "工單已完成生產", tone: "success" },
      { area: "產能", status: "已完成", note: "不需新增產能", tone: "success" },
      { area: "人員", status: "正常", note: "不需追加人力", tone: "success" },
      { area: "品質/出貨", status: "阻擋", note: "微生物快篩待判，暫緩入庫與出貨", tone: "warning" }
    ],
    dependencies: [
      { area: "生產", status: "完成", note: "待 QC 放行", tone: "success" },
      { area: "品檢", status: "待判", note: "暫緩入庫/出貨", tone: "info" },
      { area: "出貨", status: "阻擋", note: "需 QC 合格後排車", tone: "warning" }
    ],
    workflow: [
      { label: "訂單", ref: "SO-20260523-027", status: "完成", tone: "success" },
      { label: "備料", ref: "PICK-20260523-003", status: "完成", tone: "success" },
      { label: "生產", ref: "WO-20260523-003", status: "完成", tone: "success" },
      { label: "品檢", ref: "QC-20260523-015", status: "進行中", tone: "info" },
      { label: "出貨", ref: "SHIP-暫緩", status: "阻擋", tone: "warning" },
      { label: "收款", ref: "AR-待建立", status: "待處理", tone: "info" }
    ]
  }
];

export const ordersDashboardMock: OrdersDashboardData = {
  summary: orderSummary,
  orders: salesOrders
};
