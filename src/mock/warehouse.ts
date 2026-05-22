import type {
  WarehouseException,
  WarehouseKpi,
  WarehouseRecord
} from "@/types/warehouse";

export const warehouseKpis: WarehouseKpi[] = [
  {
    label: "庫存品項",
    value: "428",
    hint: "32 個庫位，29 個 workflow 品項已納入追蹤",
    tone: "info"
  },
  {
    label: "即期批號",
    value: "9",
    hint: "7 日內 3 批，30 日內 6 批",
    tone: "danger"
  },
  {
    label: "待入出庫",
    value: "23",
    hint: "入庫 8、出庫 11、移倉 4",
    tone: "warning"
  },
  {
    label: "倉租風險",
    value: "6",
    hint: "超過合約週期或待結算",
    tone: "success"
  }
];

export const warehouseRecords: WarehouseRecord[] = [
  {
    id: "INV-20260522-001",
    itemNo: "RM-CORN-001",
    itemName: "冷凍玉米粒",
    category: "原料",
    warehouseNo: "FZ-A03",
    warehouseName: "冷凍原料庫",
    batchNo: "RM260506-CORN",
    sourceType: "採購",
    sourceNo: "GRN-20260506-018",
    quantity: 180,
    unit: "kg",
    amount: 12600,
    expiryDate: "2026-05-27",
    daysLeft: 5,
    status: "即期優先出庫",
    tone: "danger",
    storageDays: 16,
    storageCharge: 1320,
    paymentStatus: "待結算",
    workflow: [
      { label: "採購單", ref: "PO-20260502-012", status: "完成", tone: "success" },
      { label: "收貨單", ref: "GRN-20260506-018", status: "完成", tone: "success" },
      { label: "批號", ref: "RM260506-CORN", status: "完成", tone: "success" },
      { label: "庫存", ref: "INV-20260522-001", status: "進行中", tone: "warning" },
      { label: "倉租", ref: "WHP-待結算", status: "待處理", tone: "danger" }
    ],
    relatedDocuments: [
      { type: "採購單", no: "PO-20260502-012", status: "已核准", tone: "success" },
      { type: "收貨單", no: "GRN-20260506-018", status: "已驗收", tone: "success" },
      { type: "倉租", no: "WHP-202605-004", status: "待結算", tone: "warning" }
    ]
  },
  {
    id: "INV-20260522-002",
    itemNo: "FG-CURRY-101",
    itemName: "咖哩雞肉調理包",
    category: "成品",
    warehouseNo: "FG-C02",
    warehouseName: "成品冷凍庫",
    batchNo: "FG260520-CURRY",
    sourceType: "生產",
    sourceNo: "WO-20260519-006",
    quantity: 8420,
    unit: "盒",
    amount: 421000,
    expiryDate: "2026-11-20",
    daysLeft: 182,
    status: "可出貨",
    tone: "success",
    storageDays: 2,
    storageCharge: 0,
    paymentStatus: "未產生",
    workflow: [
      { label: "工單", ref: "WO-20260519-006", status: "完成", tone: "success" },
      { label: "製程", ref: "PROC-20260520-011", status: "完成", tone: "success" },
      { label: "批號", ref: "FG260520-CURRY", status: "完成", tone: "success" },
      { label: "庫存", ref: "INV-20260522-002", status: "完成", tone: "success" },
      { label: "出貨", ref: "SO-20260522-009", status: "進行中", tone: "info" }
    ],
    relatedDocuments: [
      { type: "訂單", no: "PO-D-20260518-003", status: "待出貨", tone: "info" },
      { type: "工單", no: "WO-20260519-006", status: "已完工", tone: "success" },
      { type: "出貨單", no: "SO-20260522-009", status: "揀貨中", tone: "warning" }
    ]
  },
  {
    id: "INV-20260522-003",
    itemNo: "PK-BAG-010",
    itemName: "耐熱殺菌袋",
    category: "包材",
    warehouseNo: "PK-D04",
    warehouseName: "包材庫",
    batchNo: "PK260501-BAG",
    sourceType: "採購",
    sourceNo: "GRN-20260501-004",
    quantity: 3200,
    unit: "只",
    amount: 9600,
    expiryDate: "2027-05-01",
    daysLeft: 344,
    status: "低於安全庫存",
    tone: "warning",
    storageDays: 21,
    storageCharge: 480,
    paymentStatus: "本月預估",
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
    itemNo: "IP-SAUCE-220",
    itemName: "咖哩醬半成品",
    category: "半成品",
    warehouseNo: "CH-B01",
    warehouseName: "冷藏半成品庫",
    batchNo: "IP260521-SAUCE",
    sourceType: "生產",
    sourceNo: "PROC-20260521-014",
    quantity: 620,
    unit: "kg",
    amount: 74400,
    expiryDate: "2026-06-04",
    daysLeft: 13,
    status: "待投產領用",
    tone: "info",
    storageDays: 1,
    storageCharge: 0,
    paymentStatus: "未產生",
    workflow: [
      { label: "工單", ref: "WO-20260521-002", status: "完成", tone: "success" },
      { label: "製程", ref: "PROC-20260521-014", status: "完成", tone: "success" },
      { label: "批號", ref: "IP260521-SAUCE", status: "完成", tone: "success" },
      { label: "庫存", ref: "INV-20260522-004", status: "完成", tone: "success" },
      { label: "投產", ref: "WO-20260523-001", status: "待處理", tone: "info" }
    ],
    relatedDocuments: [
      { type: "工單", no: "WO-20260521-002", status: "已入庫", tone: "success" },
      { type: "後續工單", no: "WO-20260523-001", status: "待領用", tone: "info" }
    ]
  }
];

export const warehouseExceptions: WarehouseException[] = [
  {
    id: "EXP-01",
    title: "即期批號需優先處理",
    description: "RM260506-CORN 距效期 5 天，建議優先出庫或轉生產。",
    tone: "danger"
  },
  {
    id: "LOW-01",
    title: "包材低於安全庫存",
    description: "PK-BAG-010 目前 3,200 只，低於安全庫存 6,000 只。",
    tone: "warning"
  },
  {
    id: "PAY-01",
    title: "倉租待結算",
    description: "冷凍原料庫本月已有 6 筆紀錄需確認倉租帳款。",
    tone: "info"
  }
];
