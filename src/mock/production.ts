import type {
  ProductionScheduleItem,
  ProductionSummaryItem,
  WorkOrder,
  WorkOrderStage
} from "@/types/production";

export const workflowStages: WorkOrderStage[] = ["待生產", "生產中", "品檢", "包裝", "完工"];

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

export const workOrders: WorkOrder[] = [
  {
    id: "MO-240512-001",
    product: "咖哩雞肉調理包",
    batchNo: "B240512-A101",
    line: "A1 調理包產線",
    stage: "生產中",
    tone: "success",
    progress: 72,
    plannedQty: 9600,
    completedQty: 6912,
    owner: "林組長",
    eta: "14:30",
    priority: "高"
  },
  {
    id: "MO-240512-002",
    product: "綜合冷凍蔬菜",
    batchNo: "B240512-B207",
    line: "B2 冷凍蔬菜產線",
    stage: "待生產",
    tone: "warning",
    progress: 12,
    plannedQty: 7200,
    completedQty: 864,
    owner: "陳生管",
    eta: "16:20",
    priority: "高"
  },
  {
    id: "MO-240512-003",
    product: "即食雞胸肉",
    batchNo: "B240512-C315",
    line: "C3 包裝產線",
    stage: "品檢",
    tone: "info",
    progress: 66,
    plannedQty: 4800,
    completedQty: 3168,
    owner: "吳品保",
    eta: "15:10",
    priority: "中"
  },
  {
    id: "MO-240512-004",
    product: "番茄牛肉燉飯",
    batchNo: "B240512-A118",
    line: "A2 調理包產線",
    stage: "包裝",
    tone: "success",
    progress: 84,
    plannedQty: 5200,
    completedQty: 4368,
    owner: "張班長",
    eta: "13:55",
    priority: "中"
  },
  {
    id: "MO-240512-005",
    product: "鮮蔬玉米濃湯",
    batchNo: "B240512-D021",
    line: "D1 充填產線",
    stage: "完工",
    tone: "neutral",
    progress: 100,
    plannedQty: 3600,
    completedQty: 3600,
    owner: "黃組長",
    eta: "已完工",
    priority: "低"
  }
];

export const productionSchedule: ProductionScheduleItem[] = [
  {
    line: "A1",
    slots: [
      { time: "08:00", workOrderId: "MO-001", product: "咖哩雞肉", stage: "生產中", tone: "success" },
      { time: "14:30", workOrderId: "MO-006", product: "麻婆豆腐", stage: "待生產", tone: "warning" }
    ]
  },
  {
    line: "B2",
    slots: [
      { time: "09:30", workOrderId: "MO-002", product: "冷凍蔬菜", stage: "待生產", tone: "warning" },
      { time: "16:20", workOrderId: "MO-007", product: "青花菜", stage: "待生產", tone: "neutral" }
    ]
  },
  {
    line: "C3",
    slots: [
      { time: "10:00", workOrderId: "MO-003", product: "雞胸肉", stage: "品檢", tone: "info" },
      { time: "15:10", workOrderId: "MO-008", product: "舒肥雞腿", stage: "包裝", tone: "success" }
    ]
  },
  {
    line: "D1",
    slots: [
      { time: "07:30", workOrderId: "MO-005", product: "玉米濃湯", stage: "完工", tone: "neutral" },
      { time: "13:00", workOrderId: "MO-009", product: "南瓜濃湯", stage: "生產中", tone: "success" }
    ]
  }
];
