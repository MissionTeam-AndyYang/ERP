import type {
  WarehouseCapacity,
  WarehouseCategorySummary,
  WarehouseDashboardData,
  WarehouseKpi,
  WarehouseRecord,
  WarehouseRisk,
  WarehouseTask
} from "@/types/warehouse";

export const warehouseKpis: WarehouseKpi[] = [
  {
    label: "庫存總價值",
    value: "$7.42M",
    hint: "製成品 42%、原料 29%、在製品 14%",
    tone: "info"
  },
  {
    label: "倉位使用率",
    value: "72%",
    hint: "已用 310 板，可用 118 板",
    tone: "success"
  },
  {
    label: "風險品項",
    value: "18",
    hint: "呆滯 7、效期 5、低水位 6",
    tone: "danger"
  },
  {
    label: "今日待處理",
    value: "23",
    hint: "入庫 8、出庫 11、移倉 4",
    tone: "warning"
  }
];

export const warehouseCategorySummaries: WarehouseCategorySummary[] = [
  {
    category: "原料",
    amount: 2140000,
    amountRatio: 29,
    reservedAmount: 380000,
    availableAmount: 1760000,
    palletCount: 128,
    itemCount: 94,
    trend7Days: 4.2,
    tone: "info"
  },
  {
    category: "物料",
    amount: 680000,
    amountRatio: 9,
    reservedAmount: 120000,
    availableAmount: 560000,
    palletCount: 42,
    itemCount: 61,
    trend7Days: -1.8,
    tone: "success"
  },
  {
    category: "膠捲",
    amount: 520000,
    amountRatio: 7,
    reservedAmount: 60000,
    availableAmount: 460000,
    palletCount: 36,
    itemCount: 18,
    trend7Days: 2.6,
    tone: "warning"
  },
  {
    category: "在製品",
    amount: 1060000,
    amountRatio: 14,
    reservedAmount: 760000,
    availableAmount: 300000,
    palletCount: 18,
    itemCount: 22,
    trend7Days: 9.5,
    tone: "info"
  },
  {
    category: "製成品",
    amount: 3020000,
    amountRatio: 41,
    reservedAmount: 1280000,
    availableAmount: 1740000,
    palletCount: 86,
    itemCount: 133,
    trend7Days: -3.1,
    tone: "success"
  }
];

export const warehouseCapacities: WarehouseCapacity[] = [
  {
    id: "WH-FZ-A",
    warehouseName: "原料冷凍庫",
    warehouseType: "原料 / 在製品",
    totalPallets: 160,
    usedPallets: 128,
    reservedPallets: 8,
    availablePallets: 24,
    tone: "warning"
  },
  {
    id: "WH-FG-C",
    warehouseName: "成品冷凍庫",
    warehouseType: "製成品",
    totalPallets: 130,
    usedPallets: 86,
    reservedPallets: 12,
    availablePallets: 32,
    tone: "success"
  },
  {
    id: "WH-PK-D",
    warehouseName: "物料包材庫",
    warehouseType: "物料 / 膠捲",
    totalPallets: 96,
    usedPallets: 78,
    reservedPallets: 4,
    availablePallets: 14,
    tone: "warning"
  },
  {
    id: "WH-OUT-E",
    warehouseName: "外部寄倉",
    warehouseType: "彈性寄倉",
    totalPallets: 42,
    usedPallets: 18,
    reservedPallets: 0,
    availablePallets: 24,
    tone: "info"
  }
];

export const warehouseRecords: WarehouseRecord[] = [
  {
    id: "INV-20260522-001",
    itemNo: "RM-CORN-001",
    itemName: "冷凍玉米粒",
    category: "原料",
    warehouseNo: "FZ-A03",
    warehouseName: "原料冷凍庫",
    batchNo: "RM260506-CORN",
    sourceLabel: "採購",
    sourceNo: "GRN-20260506-018",
    quantity: 180,
    reservedQuantity: 180,
    availableQuantity: 0,
    unit: "kg",
    amount: 12600,
    reservedAmount: 12600,
    availableAmount: 0,
    palletCount: 3,
    safetyStock: 420,
    expiryDate: "2026-05-27",
    shelfLifeDays: 90,
    daysLeft: 5,
    turnoverDays: 46,
    status: "效期風險",
    tone: "danger",
    workflow: [
      { label: "採購單", ref: "PO-20260502-012", status: "完成", tone: "success" },
      { label: "收貨單", ref: "GRN-20260506-018", status: "完成", tone: "success" },
      { label: "批號", ref: "RM260506-CORN", status: "完成", tone: "success" },
      { label: "庫存", ref: "INV-20260522-001", status: "進行中", tone: "warning" },
      { label: "出庫建議", ref: "ISSUE-建議建立", status: "待處理", tone: "danger" }
    ],
    relatedDocuments: [
      { type: "採購單", no: "PO-20260502-012", status: "已核准", tone: "success" },
      { type: "收貨單", no: "GRN-20260506-018", status: "已驗收", tone: "success" },
      { type: "庫存警示", no: "EXP-RM-CORN-001", status: "需處理", tone: "danger" }
    ]
  },
  {
    id: "INV-20260522-002",
    itemNo: "FG-CURRY-101",
    itemName: "咖哩雞肉調理包",
    category: "製成品",
    warehouseNo: "FG-C02",
    warehouseName: "成品冷凍庫",
    batchNo: "FG260520-CURRY",
    sourceLabel: "生產",
    sourceNo: "WO-20260519-006",
    quantity: 8420,
    reservedQuantity: 1200,
    availableQuantity: 7220,
    unit: "盒",
    amount: 421000,
    reservedAmount: 60000,
    availableAmount: 361000,
    palletCount: 22,
    safetyStock: 5000,
    expiryDate: "2026-11-20",
    shelfLifeDays: 180,
    daysLeft: 182,
    turnoverDays: 8,
    status: "可出貨",
    tone: "success",
    workflow: [
      { label: "工單", ref: "WO-20260519-006", status: "完成", tone: "success" },
      { label: "製程", ref: "PROC-20260520-011", status: "完成", tone: "success" },
      { label: "批號", ref: "FG260520-CURRY", status: "完成", tone: "success" },
      { label: "庫存", ref: "INV-20260522-002", status: "完成", tone: "success" },
      { label: "出貨", ref: "SO-20260522-009", status: "進行中", tone: "info" }
    ],
    relatedDocuments: [
      { type: "訂單", no: "SO-20260522-009", status: "待出貨", tone: "info" },
      { type: "工單", no: "WO-20260519-006", status: "已完工", tone: "success" },
      { type: "出貨單", no: "SHIP-20260522-009", status: "揀貨中", tone: "warning" }
    ]
  },
  {
    id: "INV-20260522-003",
    itemNo: "PK-BAG-010",
    itemName: "耐熱殺菌袋",
    category: "物料",
    warehouseNo: "PK-D04",
    warehouseName: "物料包材庫",
    batchNo: "PK260501-BAG",
    sourceLabel: "採購",
    sourceNo: "GRN-20260501-004",
    quantity: 3200,
    reservedQuantity: 1400,
    availableQuantity: 1800,
    unit: "只",
    amount: 9600,
    reservedAmount: 4200,
    availableAmount: 5400,
    palletCount: 8,
    safetyStock: 6000,
    expiryDate: "2027-05-01",
    shelfLifeDays: 365,
    daysLeft: 344,
    turnoverDays: 21,
    status: "低於安全水位",
    tone: "warning",
    workflow: [
      { label: "採購單", ref: "PO-20260428-021", status: "完成", tone: "success" },
      { label: "收貨單", ref: "GRN-20260501-004", status: "完成", tone: "success" },
      { label: "批號", ref: "PK260501-BAG", status: "完成", tone: "success" },
      { label: "庫存", ref: "INV-20260522-003", status: "進行中", tone: "warning" },
      { label: "請購", ref: "PR-建議建立", status: "待處理", tone: "danger" }
    ],
    relatedDocuments: [
      { type: "採購單", no: "PO-20260428-021", status: "已入庫", tone: "success" },
      { type: "庫存警示", no: "LOW-PK-BAG-010", status: "需補貨", tone: "danger" }
    ]
  },
  {
    id: "INV-20260522-004",
    itemNo: "FLM-ROLL-018",
    itemName: "封口膠捲 180mm",
    category: "膠捲",
    warehouseNo: "PK-D06",
    warehouseName: "膠捲恆溫庫",
    batchNo: "FLM260415-018",
    sourceLabel: "採購",
    sourceNo: "GRN-20260415-011",
    quantity: 720,
    reservedQuantity: 120,
    availableQuantity: 600,
    unit: "卷",
    amount: 186000,
    reservedAmount: 31000,
    availableAmount: 155000,
    palletCount: 16,
    safetyStock: 500,
    expiryDate: "2027-04-15",
    shelfLifeDays: 365,
    daysLeft: 327,
    turnoverDays: 38,
    status: "迴轉偏慢",
    tone: "warning",
    workflow: [
      { label: "採購單", ref: "PO-20260410-018", status: "完成", tone: "success" },
      { label: "收貨單", ref: "GRN-20260415-011", status: "完成", tone: "success" },
      { label: "批號", ref: "FLM260415-018", status: "完成", tone: "success" },
      { label: "庫存", ref: "INV-20260522-004", status: "進行中", tone: "warning" }
    ],
    relatedDocuments: [
      { type: "採購單", no: "PO-20260410-018", status: "已入庫", tone: "success" },
      { type: "庫齡警示", no: "AGE-FLM-ROLL-018", status: "需檢視", tone: "warning" }
    ]
  },
  {
    id: "INV-20260522-005",
    itemNo: "IP-SAUCE-220",
    itemName: "咖哩醬在製品",
    category: "在製品",
    warehouseNo: "CH-B01",
    warehouseName: "在製品冷藏庫",
    batchNo: "IP260521-SAUCE",
    sourceLabel: "生產",
    sourceNo: "PROC-20260521-014",
    quantity: 620,
    reservedQuantity: 620,
    availableQuantity: 0,
    unit: "kg",
    amount: 74400,
    reservedAmount: 74400,
    availableAmount: 0,
    palletCount: 5,
    safetyStock: 300,
    expiryDate: "2026-06-04",
    shelfLifeDays: 14,
    daysLeft: 13,
    turnoverDays: 1,
    status: "待投產領用",
    tone: "info",
    workflow: [
      { label: "工單", ref: "WO-20260521-002", status: "完成", tone: "success" },
      { label: "製程", ref: "PROC-20260521-014", status: "完成", tone: "success" },
      { label: "批號", ref: "IP260521-SAUCE", status: "完成", tone: "success" },
      { label: "庫存", ref: "INV-20260522-005", status: "完成", tone: "success" },
      { label: "投產", ref: "WO-20260523-001", status: "待處理", tone: "info" }
    ],
    relatedDocuments: [
      { type: "工單", no: "WO-20260521-002", status: "已入庫", tone: "success" },
      { type: "後續工單", no: "WO-20260523-001", status: "待領用", tone: "info" }
    ]
  }
];

export const warehouseRisks: WarehouseRisk[] = [
  {
    id: "AGE-01",
    type: "迴轉超過一個月",
    itemName: "封口膠捲 180mm",
    category: "膠捲",
    batchNo: "FLM260415-018",
    warehouseName: "膠捲恆溫庫",
    metric: "庫齡 38 天",
    recommendation: "檢查後續排產用量，必要時暫緩補貨。",
    tone: "warning"
  },
  {
    id: "EXP-01",
    type: "少於 1/3 效期",
    itemName: "冷凍玉米粒",
    category: "原料",
    batchNo: "RM260506-CORN",
    warehouseName: "原料冷凍庫",
    metric: "剩餘 5 天 / 效期 90 天",
    recommendation: "優先出庫或轉生產，不含物料與膠捲類別。",
    tone: "danger"
  },
  {
    id: "LOW-01",
    type: "低於安全水位",
    itemName: "耐熱殺菌袋",
    category: "物料",
    batchNo: "PK260501-BAG",
    warehouseName: "物料包材庫",
    metric: "3,200 / 安全水位 6,000",
    recommendation: "建立請購或確認已下採購單。",
    tone: "warning"
  }
];

export const warehouseTasks: WarehouseTask[] = [
  {
    id: "WH-IN-20260523-018",
    type: "入庫",
    itemName: "雞胸肉原料",
    batchNo: "RM260523-CHK",
    quantity: 600,
    unit: "kg",
    palletCount: 10,
    owner: "李倉管",
    dueTime: "10:40",
    sourceNo: "GRN-20260523-018",
    status: "待驗收",
    tone: "info"
  },
  {
    id: "WH-OUT-20260523-022",
    type: "出庫",
    itemName: "冷凍玉米粒",
    batchNo: "RM260506-CORN",
    quantity: 180,
    unit: "kg",
    palletCount: 3,
    owner: "周倉管",
    dueTime: "11:20",
    sourceNo: "WO-20260523-001",
    status: "待揀料",
    tone: "danger"
  },
  {
    id: "WH-MV-20260523-006",
    type: "移倉",
    itemName: "咖哩雞肉調理包",
    batchNo: "FG260520-CURRY",
    quantity: 1200,
    unit: "盒",
    palletCount: 4,
    owner: "許組長",
    dueTime: "13:30",
    sourceNo: "SO-20260522-009",
    status: "執行中",
    tone: "warning"
  },
  {
    id: "WH-OUT-20260523-027",
    type: "出庫",
    itemName: "耐熱殺菌袋",
    batchNo: "PK260501-BAG",
    quantity: 1400,
    unit: "只",
    palletCount: 2,
    owner: "陳倉管",
    dueTime: "15:00",
    sourceNo: "WO-20260523-004",
    status: "待確認",
    tone: "info"
  }
];

export const warehouseDashboardMock: WarehouseDashboardData = {
  kpis: warehouseKpis,
  categorySummaries: warehouseCategorySummaries,
  capacities: warehouseCapacities,
  records: warehouseRecords,
  risks: warehouseRisks,
  tasks: warehouseTasks
};
