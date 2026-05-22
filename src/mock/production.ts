import type {
  ProductionAlert,
  ProductionScheduleItem,
  ProductionSummaryItem,
  WorkOrder,
  WorkOrderStage
} from "@/types/production";

export const workflowStages: WorkOrderStage[] = ["待排程", "待備料", "生產中", "品檢", "包裝", "完工"];

export const productionSummary: ProductionSummaryItem[] = [
  {
    label: "今日工單",
    value: "12",
    hint: "8 張進行中",
    tone: "info"
  },
  {
    label: "準時率",
    value: "94%",
    hint: "+3% vs 昨日",
    tone: "success"
  },
  {
    label: "待料工單",
    value: "2",
    hint: "B2 產線優先",
    tone: "warning"
  },
  {
    label: "品檢待判",
    value: "3",
    hint: "平均等待 18 分",
    tone: "danger"
  }
];

export const productionOrders: WorkOrder[] = [
  {
    id: "WO-20260522-001",
    product: "咖哩雞肉調理包",
    batchNo: "FG260522-CURRY",
    line: "A1 調理包產線",
    stage: "生產中",
    tone: "success",
    progress: 72,
    plannedQty: 9600,
    completedQty: 6912,
    unit: "盒",
    owner: "林組長",
    eta: "14:30",
    priority: "高",
    sourceOrder: "SO-20260520-018",
    bomNo: "BOM-FG-CURRY-101",
    startTime: "08:00",
    endTime: "14:30",
    qualityStatus: "首件通過",
    materialStatus: "足夠",
    materials: [
      {
        itemNo: "RM-CHICKEN-022",
        itemName: "雞胸肉原料",
        batchNo: "RM260520-CHK",
        requiredQty: 840,
        issuedQty: 840,
        unit: "kg",
        status: "足夠",
        tone: "success"
      },
      {
        itemNo: "IP-SAUCE-220",
        itemName: "咖哩醬半成品",
        batchNo: "IP260521-SAUCE",
        requiredQty: 620,
        issuedQty: 620,
        unit: "kg",
        status: "足夠",
        tone: "success"
      }
    ],
    workflow: [
      { label: "訂單", ref: "SO-20260520-018", status: "完成", tone: "success" },
      { label: "工單", ref: "WO-20260522-001", status: "完成", tone: "success" },
      { label: "備料", ref: "PICK-20260522-004", status: "完成", tone: "success" },
      { label: "生產", ref: "PROC-20260522-011", status: "進行中", tone: "info" },
      { label: "品檢", ref: "QC-待產出", status: "待處理", tone: "warning" }
    ],
    relatedDocuments: [
      { type: "訂單", no: "SO-20260520-018", status: "已核准", tone: "success" },
      { type: "BOM", no: "BOM-FG-CURRY-101", status: "有效", tone: "success" },
      { type: "領料單", no: "PICK-20260522-004", status: "已領料", tone: "success" }
    ]
  },
  {
    id: "WO-20260522-002",
    product: "綜合冷凍蔬菜",
    batchNo: "FG260522-VEG",
    line: "B2 冷凍蔬菜產線",
    stage: "待備料",
    tone: "warning",
    progress: 18,
    plannedQty: 7200,
    completedQty: 0,
    unit: "包",
    owner: "陳生管",
    eta: "16:20",
    priority: "高",
    sourceOrder: "SO-20260521-006",
    bomNo: "BOM-FG-VEG-207",
    startTime: "13:00",
    endTime: "16:20",
    qualityStatus: "未開始",
    materialStatus: "短缺",
    materials: [
      {
        itemNo: "RM-CORN-001",
        itemName: "冷凍玉米粒",
        batchNo: "RM260506-CORN",
        requiredQty: 240,
        issuedQty: 180,
        unit: "kg",
        status: "短缺",
        tone: "danger"
      },
      {
        itemNo: "PK-BAG-010",
        itemName: "耐熱殺菌袋",
        batchNo: "PK260501-BAG",
        requiredQty: 7200,
        issuedQty: 3200,
        unit: "只",
        status: "待領料",
        tone: "warning"
      }
    ],
    workflow: [
      { label: "訂單", ref: "SO-20260521-006", status: "完成", tone: "success" },
      { label: "工單", ref: "WO-20260522-002", status: "完成", tone: "success" },
      { label: "備料", ref: "PICK-20260522-007", status: "進行中", tone: "warning" },
      { label: "生產", ref: "PROC-待建立", status: "待處理", tone: "warning" },
      { label: "請購", ref: "PR-建議建立", status: "待處理", tone: "danger" }
    ],
    relatedDocuments: [
      { type: "訂單", no: "SO-20260521-006", status: "已核准", tone: "success" },
      { type: "BOM", no: "BOM-FG-VEG-207", status: "有效", tone: "success" },
      { type: "庫存警示", no: "LOW-RM-CORN-001", status: "需補貨", tone: "danger" }
    ]
  },
  {
    id: "WO-20260522-003",
    product: "即食雞胸肉",
    batchNo: "FG260522-CHICKEN",
    line: "C3 包裝產線",
    stage: "品檢",
    tone: "info",
    progress: 66,
    plannedQty: 4800,
    completedQty: 3168,
    unit: "包",
    owner: "吳品保",
    eta: "15:10",
    priority: "中",
    sourceOrder: "SO-20260519-011",
    bomNo: "BOM-FG-CHICKEN-315",
    startTime: "10:00",
    endTime: "15:10",
    qualityStatus: "待微生物快篩",
    materialStatus: "足夠",
    materials: [
      {
        itemNo: "RM-CHICKEN-022",
        itemName: "雞胸肉原料",
        batchNo: "RM260520-CHK",
        requiredQty: 520,
        issuedQty: 520,
        unit: "kg",
        status: "足夠",
        tone: "success"
      }
    ],
    workflow: [
      { label: "工單", ref: "WO-20260522-003", status: "完成", tone: "success" },
      { label: "備料", ref: "PICK-20260522-003", status: "完成", tone: "success" },
      { label: "生產", ref: "PROC-20260522-008", status: "完成", tone: "success" },
      { label: "品檢", ref: "QC-20260522-015", status: "進行中", tone: "info" },
      { label: "入庫", ref: "INV-待建立", status: "待處理", tone: "warning" }
    ],
    relatedDocuments: [
      { type: "工單", no: "WO-20260522-003", status: "生產完成", tone: "success" },
      { type: "品檢", no: "QC-20260522-015", status: "待判定", tone: "info" }
    ]
  }
];

export const workOrders = productionOrders;

export const productionSchedule: ProductionScheduleItem[] = [
  {
    line: "A1",
    utilization: 88,
    slots: [
      { time: "08:00", workOrderId: "WO-20260522-001", product: "咖哩雞肉調理包", stage: "生產中", tone: "success" },
      { time: "14:30", workOrderId: "WO-20260522-006", product: "麻婆豆腐調理包", stage: "待排程", tone: "warning" }
    ]
  },
  {
    line: "B2",
    utilization: 64,
    slots: [
      { time: "09:30", workOrderId: "WO-20260522-002", product: "綜合冷凍蔬菜", stage: "待備料", tone: "warning" },
      { time: "16:20", workOrderId: "WO-20260522-007", product: "青花菜", stage: "待排程", tone: "neutral" }
    ]
  },
  {
    line: "C3",
    utilization: 76,
    slots: [
      { time: "10:00", workOrderId: "WO-20260522-003", product: "即食雞胸肉", stage: "品檢", tone: "info" },
      { time: "15:10", workOrderId: "WO-20260522-008", product: "舒肥雞腿", stage: "包裝", tone: "success" }
    ]
  }
];

export const productionAlerts: ProductionAlert[] = [
  {
    id: "MAT-01",
    title: "B2 產線待料",
    description: "冷凍玉米粒與耐熱殺菌袋不足，會影響 WO-20260522-002 開線。",
    tone: "danger"
  },
  {
    id: "QC-01",
    title: "品檢待判",
    description: "WO-20260522-003 已完成生產，等待 QC-20260522-015 判定後才能入庫。",
    tone: "info"
  },
  {
    id: "CAP-01",
    title: "A1 產能接近滿載",
    description: "A1 今日利用率 88%，後續插單需先檢查備料與換線時間。",
    tone: "warning"
  }
];
