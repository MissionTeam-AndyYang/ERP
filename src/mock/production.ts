import type {
  ProductionAlert,
  ProductionDaySchedule,
  ProductionSummaryItem,
  WorkOrder,
  WorkOrderStage
} from "@/types/production";

export const workflowStages: WorkOrderStage[] = ["待排程", "待備料", "生產中", "品檢", "包裝", "完工"];

export const productionSummary: ProductionSummaryItem[] = [
  {
    label: "一週預排工單",
    value: "38",
    hint: "可用產能 22.5 hr",
    tone: "info"
  },
  {
    label: "今日 MES 進行中",
    value: "8",
    hint: "3 張需追蹤",
    tone: "success"
  },
  {
    label: "備料/人員風險",
    value: "5",
    hint: "缺料 2、人員支援 3",
    tone: "warning"
  },
  {
    label: "品檢待判/異常",
    value: "4",
    hint: "待判 3、異常 1",
    tone: "danger"
  }
];

export const productionOrders: WorkOrder[] = [
  {
    id: "WO-20260523-001",
    product: "咖哩雞肉調理包",
    batchNo: "FG260523-CURRY",
    processType: "調理",
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
    customerDueDate: "2026-05-24",
    deliveryRisk: "正常",
    scheduleDate: "2026-05-23",
    startTime: "08:00",
    endTime: "14:30",
    changeoverMinutes: 30,
    materialStatus: "足夠",
    staffStatus: "足夠",
    requiredStaff: 9,
    assignedStaff: 10,
    machineStatus: "正常",
    standardHours: 6.5,
    actualHours: 6.1,
    efficiencyRate: 106,
    standardMaterialQty: 1460,
    actualMaterialQty: 1508,
    materialLossRate: 3.3,
    laborHours: 61,
    laborCost: 21350,
    unitLaborCost: 2.23,
    quality: {
      status: "首件通過",
      sampleCount: 24,
      defectCount: 0,
      defectRate: 0,
      pendingCount: 0,
      result: "首件與製程檢查正常",
      tone: "success"
    },
    qualityBlocksInventory: false,
    qualityBlocksShipment: false,
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
        itemName: "咖哩醬在製品",
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
      { label: "APS", ref: "APS-20260522-A1", status: "完成", tone: "success" },
      { label: "工單", ref: "WO-20260523-001", status: "完成", tone: "success" },
      { label: "備料", ref: "PICK-20260523-004", status: "完成", tone: "success" },
      { label: "生產", ref: "PROC-20260523-011", status: "進行中", tone: "info" },
      { label: "品檢", ref: "QC-20260523-006", status: "進行中", tone: "success" }
    ],
    relatedDocuments: [
      { type: "訂單", no: "SO-20260520-018", status: "已核准", tone: "success" },
      { type: "BOM", no: "BOM-FG-CURRY-101", status: "有效", tone: "success" },
      { type: "品檢", no: "QC-20260523-006", status: "首件通過", tone: "success" }
    ]
  },
  {
    id: "WO-20260523-002",
    product: "綜合冷凍蔬菜",
    batchNo: "FG260523-VEG",
    processType: "冷凍",
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
    customerDueDate: "2026-05-24",
    deliveryRisk: "高風險",
    scheduleDate: "2026-05-23",
    startTime: "13:00",
    endTime: "16:20",
    changeoverMinutes: 45,
    materialStatus: "短缺",
    staffStatus: "需支援",
    requiredStaff: 7,
    assignedStaff: 5,
    machineStatus: "待機",
    standardHours: 3.3,
    actualHours: 0,
    efficiencyRate: 0,
    standardMaterialQty: 7440,
    actualMaterialQty: 0,
    materialLossRate: 0,
    laborHours: 0,
    laborCost: 0,
    unitLaborCost: 0,
    quality: {
      status: "未開始",
      sampleCount: 0,
      defectCount: 0,
      defectRate: 0,
      pendingCount: 0,
      result: "等待備料完成後開線",
      tone: "warning"
    },
    qualityBlocksInventory: true,
    qualityBlocksShipment: true,
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
      { label: "APS", ref: "APS-20260522-B2", status: "完成", tone: "success" },
      { label: "工單", ref: "WO-20260523-002", status: "完成", tone: "success" },
      { label: "備料", ref: "PICK-20260523-007", status: "進行中", tone: "warning" },
      { label: "生產", ref: "PROC-待建立", status: "待處理", tone: "warning" }
    ],
    relatedDocuments: [
      { type: "訂單", no: "SO-20260521-006", status: "已核准", tone: "success" },
      { type: "BOM", no: "BOM-FG-VEG-207", status: "有效", tone: "success" },
      { type: "庫存警示", no: "LOW-RM-CORN-001", status: "需補貨", tone: "danger" }
    ]
  },
  {
    id: "WO-20260523-003",
    product: "即食雞胸肉",
    batchNo: "FG260523-CHICKEN",
    processType: "包裝",
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
    customerDueDate: "2026-05-23",
    deliveryRisk: "注意",
    scheduleDate: "2026-05-23",
    startTime: "10:00",
    endTime: "15:10",
    changeoverMinutes: 20,
    materialStatus: "足夠",
    staffStatus: "足夠",
    requiredStaff: 6,
    assignedStaff: 6,
    machineStatus: "正常",
    standardHours: 5.2,
    actualHours: 5.6,
    efficiencyRate: 93,
    standardMaterialQty: 520,
    actualMaterialQty: 548,
    materialLossRate: 5.4,
    laborHours: 33.6,
    laborCost: 11760,
    unitLaborCost: 2.45,
    quality: {
      status: "待判定",
      sampleCount: 36,
      defectCount: 2,
      defectRate: 5.6,
      pendingCount: 3,
      result: "微生物快篩等待判定",
      tone: "info"
    },
    qualityBlocksInventory: true,
    qualityBlocksShipment: true,
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
      { label: "工單", ref: "WO-20260523-003", status: "完成", tone: "success" },
      { label: "備料", ref: "PICK-20260523-003", status: "完成", tone: "success" },
      { label: "生產", ref: "PROC-20260523-008", status: "完成", tone: "success" },
      { label: "品檢", ref: "QC-20260523-015", status: "進行中", tone: "info" },
      { label: "入庫", ref: "INV-待建立", status: "待處理", tone: "warning" }
    ],
    relatedDocuments: [
      { type: "工單", no: "WO-20260523-003", status: "生產完成", tone: "success" },
      { type: "品檢", no: "QC-20260523-015", status: "待判定", tone: "info" }
    ]
  }
];

export const workOrders = productionOrders;

export const productionWeekSchedule: ProductionDaySchedule[] = [
  {
    date: "2026-05-23",
    label: "今天",
    lines: [
      {
        line: "A1",
        processType: "調理",
        dailyCapacityHours: 10,
        usedHours: 7.5,
        availableHours: 2.5,
        changeoverHours: 0.5,
        bottleneckRank: 3,
        tone: "info",
        slots: [
          {
            workOrderId: "WO-20260523-001",
            product: "咖哩雞肉調理包",
            processType: "調理",
            startTime: "08:00",
            endTime: "14:30",
            materialStatus: "足夠",
            staffStatus: "足夠",
            stage: "生產中",
            tone: "success"
          },
          {
            workOrderId: "WO-20260523-006",
            product: "麻婆豆腐調理包",
            processType: "調理",
            startTime: "15:00",
            endTime: "17:00",
            materialStatus: "待領料",
            staffStatus: "需支援",
            stage: "待備料",
            tone: "warning"
          }
        ]
      },
      {
        line: "B2",
        processType: "冷凍",
        dailyCapacityHours: 10,
        usedHours: 6.5,
        availableHours: 3.5,
        changeoverHours: 0.75,
        bottleneckRank: 4,
        tone: "warning",
        slots: [
          {
            workOrderId: "WO-20260523-002",
            product: "綜合冷凍蔬菜",
            processType: "冷凍",
            startTime: "13:00",
            endTime: "16:20",
            materialStatus: "短缺",
            staffStatus: "需支援",
            stage: "待備料",
            tone: "warning"
          }
        ]
      },
      {
        line: "C3",
        processType: "包裝",
        dailyCapacityHours: 9,
        usedHours: 7.5,
        availableHours: 1.5,
        changeoverHours: 0.33,
        bottleneckRank: 2,
        tone: "info",
        slots: [
          {
            workOrderId: "WO-20260523-003",
            product: "即食雞胸肉",
            processType: "包裝",
            startTime: "10:00",
            endTime: "15:10",
            materialStatus: "足夠",
            staffStatus: "足夠",
            stage: "品檢",
            tone: "info"
          }
        ]
      }
    ]
  },
  {
    date: "2026-05-24",
    label: "明天",
    lines: [
      {
        line: "A1",
        processType: "調理",
        dailyCapacityHours: 10,
        usedHours: 8,
        availableHours: 2,
        changeoverHours: 0.5,
        bottleneckRank: 3,
        tone: "warning",
        slots: [
          {
            workOrderId: "WO-20260524-004",
            product: "南瓜濃湯",
            processType: "調理",
            startTime: "08:30",
            endTime: "16:30",
            materialStatus: "足夠",
            staffStatus: "需支援",
            stage: "待排程",
            tone: "warning"
          }
        ]
      },
      {
        line: "B2",
        processType: "冷凍",
        dailyCapacityHours: 10,
        usedHours: 4,
        availableHours: 6,
        changeoverHours: 0.25,
        bottleneckRank: 5,
        tone: "success",
        slots: [
          {
            workOrderId: "WO-20260524-008",
            product: "青花菜",
            processType: "冷凍",
            startTime: "09:00",
            endTime: "13:00",
            materialStatus: "足夠",
            staffStatus: "足夠",
            stage: "待排程",
            tone: "success"
          }
        ]
      }
    ]
  },
  {
    date: "2026-05-25",
    label: "週一",
    lines: [
      {
        line: "S1",
        processType: "殺菌",
        dailyCapacityHours: 8,
        usedHours: 7.5,
        availableHours: 0.5,
        changeoverHours: 1,
        bottleneckRank: 1,
        tone: "danger",
        slots: [
          {
            workOrderId: "WO-20260525-011",
            product: "高溫殺菌調理包",
            processType: "殺菌",
            startTime: "08:00",
            endTime: "15:30",
            materialStatus: "足夠",
            staffStatus: "足夠",
            stage: "待排程",
            tone: "danger"
          }
        ]
      }
    ]
  }
];

export const productionSchedule = productionWeekSchedule[0].lines.map((line) => ({
  line: line.line,
  utilization: Math.round((line.usedHours / line.dailyCapacityHours) * 100),
  slots: line.slots.map((slot) => ({
    time: slot.startTime,
    workOrderId: slot.workOrderId,
    product: slot.product,
    stage: slot.stage,
    tone: slot.tone
  }))
}));

export const productionAlerts: ProductionAlert[] = [
  {
    id: "PLAN-01",
    title: "B2 產線排程風險",
    description: "WO-20260523-002 缺冷凍玉米粒且人員需支援，若 11:00 前未補齊會影響 13:00 開線。",
    tone: "danger"
  },
  {
    id: "QC-01",
    title: "品檢待判",
    description: "WO-20260523-003 已完成生產，等待 QC-20260523-015 判定後才能入庫。",
    tone: "info"
  },
  {
    id: "CAP-01",
    title: "殺菌製程產能不足",
    description: "2026-05-25 S1 殺菌線只剩 0.5 hr，可接單量有限。",
    tone: "warning"
  }
];
