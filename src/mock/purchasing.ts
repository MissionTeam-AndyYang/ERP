import type { PurchaseItem, PurchasingSummary } from "@/types/purchasing";

export const purchasingSummary: PurchasingSummary[] = [
  {
    label: "待處理採購需求",
    value: "18",
    hint: "5 筆影響本週生產",
    tone: "warning"
  },
  {
    label: "交期高風險",
    value: "4",
    hint: "缺料 2、延遲 2",
    tone: "danger"
  },
  {
    label: "今日到貨/驗收",
    value: "7",
    hint: "3 筆需品檢文件",
    tone: "info"
  },
  {
    label: "本月採購金額",
    value: "$8.4M",
    hint: "較預算 -3.1%",
    tone: "success"
  }
];

export const purchaseItems: PurchaseItem[] = [
  {
    id: "PUR-20260523-001",
    requestNo: "PR-20260523-018",
    purchaseOrderNo: "PO-20260523-031",
    itemNo: "RM-CORN-001",
    itemName: "冷凍玉米粒",
    category: "原料",
    supplier: "綠田食品",
    quantity: 1200,
    unit: "kg",
    amount: 86400,
    requiredDate: "2026-05-23",
    expectedArrivalDate: "2026-05-23",
    stage: "待核准",
    tone: "danger",
    riskLevel: "高風險",
    riskReason: "B2 產線 13:00 開線缺料，若 11:00 前未核准/到貨會影響 SO-20260523-022。",
    sourceOrder: "SO-20260523-022",
    linkedWorkOrder: "WO-20260523-002",
    currentStock: 180,
    reservedStock: 180,
    availableStock: 0,
    safetyStock: 420,
    leadTimeDays: 2,
    delayDays: 0,
    qualityDocumentStatus: "待補",
    receivingStatus: "待到貨",
    warehouseStatus: "未入庫",
    owner: "採購一組",
    dependencies: [
      { area: "訂單", status: "高風險", note: "SO-20260523-022 交期 2026-05-24", tone: "danger" },
      { area: "生產", status: "受阻", note: "WO-20260523-002 待備料", tone: "danger" },
      { area: "庫存", status: "不足", note: "可用量 0 kg", tone: "danger" },
      { area: "品檢", status: "待文件", note: "COA 待供應商補件", tone: "warning" }
    ],
    workflow: [
      { label: "請購", ref: "PR-20260523-018", status: "完成", tone: "success" },
      { label: "採購單", ref: "PO-20260523-031", status: "進行中", tone: "warning" },
      { label: "到貨", ref: "GRN-待建立", status: "待處理", tone: "danger" },
      { label: "品檢文件", ref: "COA-待補", status: "阻擋", tone: "warning" },
      { label: "入庫", ref: "INV-待建立", status: "待處理", tone: "info" }
    ]
  },
  {
    id: "PUR-20260523-002",
    requestNo: "PR-20260522-011",
    purchaseOrderNo: "PO-20260522-029",
    itemNo: "PK-BAG-010",
    itemName: "耐熱殺菌袋",
    category: "物料",
    supplier: "台灣包材",
    quantity: 20000,
    unit: "只",
    amount: 132000,
    requiredDate: "2026-05-24",
    expectedArrivalDate: "2026-05-25",
    stage: "已下單",
    tone: "warning",
    riskLevel: "注意",
    riskReason: "安全水位不足且供應商交期可能延後 1 天，需確認替代供應商。",
    sourceOrder: null,
    linkedWorkOrder: "WO-20260523-002",
    currentStock: 3200,
    reservedStock: 1400,
    availableStock: 1800,
    safetyStock: 6000,
    leadTimeDays: 4,
    delayDays: 1,
    qualityDocumentStatus: "完整",
    receivingStatus: "待到貨",
    warehouseStatus: "未入庫",
    owner: "採購二組",
    dependencies: [
      { area: "生產", status: "注意", note: "本週多張工單會使用", tone: "warning" },
      { area: "庫存", status: "低水位", note: "低於安全水位 6,000 只", tone: "warning" },
      { area: "入庫", status: "未入庫", note: "預計 2026-05-25", tone: "info" }
    ],
    workflow: [
      { label: "請購", ref: "PR-20260522-011", status: "完成", tone: "success" },
      { label: "採購單", ref: "PO-20260522-029", status: "完成", tone: "success" },
      { label: "到貨", ref: "GRN-待建立", status: "待處理", tone: "warning" },
      { label: "入庫", ref: "INV-待建立", status: "待處理", tone: "info" }
    ]
  },
  {
    id: "PUR-20260523-003",
    requestNo: "PR-20260521-006",
    purchaseOrderNo: "PO-20260521-027",
    itemNo: "RM-CHICKEN-022",
    itemName: "雞胸肉原料",
    category: "原料",
    supplier: "安心禽品",
    quantity: 1600,
    unit: "kg",
    amount: 176000,
    requiredDate: "2026-05-23",
    expectedArrivalDate: "2026-05-23",
    stage: "驗收中",
    tone: "info",
    riskLevel: "正常",
    riskReason: "今日到貨驗收中，文件完整，驗收後可入原料冷凍庫。",
    sourceOrder: "SO-20260523-018",
    linkedWorkOrder: "WO-20260523-001",
    currentStock: 1280,
    reservedStock: 840,
    availableStock: 440,
    safetyStock: 900,
    leadTimeDays: 2,
    delayDays: 0,
    qualityDocumentStatus: "完整",
    receivingStatus: "驗收中",
    warehouseStatus: "待入庫",
    owner: "採購一組",
    dependencies: [
      { area: "生產", status: "正常", note: "WO-20260523-001 料品足夠", tone: "success" },
      { area: "品檢", status: "文件完整", note: "COA/檢驗報告已到", tone: "success" },
      { area: "入庫", status: "待入庫", note: "驗收完成後入冷凍庫", tone: "info" }
    ],
    workflow: [
      { label: "採購單", ref: "PO-20260521-027", status: "完成", tone: "success" },
      { label: "到貨", ref: "GRN-20260523-018", status: "進行中", tone: "info" },
      { label: "品檢文件", ref: "COA-20260523-018", status: "完成", tone: "success" },
      { label: "入庫", ref: "INV-待建立", status: "待處理", tone: "info" }
    ]
  }
];
