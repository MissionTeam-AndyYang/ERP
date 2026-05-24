import type { QualityDashboardData, QualityInspection, QualitySummary } from "@/types/quality";

export const qualitySummary: QualitySummary[] = [
  {
    label: "今日檢驗批",
    value: "28",
    hint: "21 批已放行",
    tone: "success"
  },
  {
    label: "待判定",
    value: "5",
    hint: "平均等待 18 分",
    tone: "warning"
  },
  {
    label: "阻擋入庫/出貨",
    value: "4",
    hint: "入庫 3、出貨 1",
    tone: "danger"
  },
  {
    label: "文件待補",
    value: "7",
    hint: "COA 2、溫度 3、檢驗 2",
    tone: "info"
  }
];

export const qualityInspections: QualityInspection[] = [
  {
    id: "QC-20260523-006",
    itemName: "咖哩雞肉調理包",
    itemNo: "FG-CURRY-101",
    batchNo: "FG260523-CURRY",
    sourceType: "生產",
    sourceNo: "PROC-20260523-011",
    workOrder: "WO-20260523-001",
    salesOrder: "SO-20260523-018",
    supplier: null,
    line: "A1 調理包產線",
    inspectionType: "首件",
    stage: "檢驗中",
    decision: "放行",
    tone: "success",
    sampleCount: 24,
    defectCount: 0,
    defectRate: 0,
    pendingTests: [],
    issueReason: "首件與製程檢查正常，可持續生產。",
    blocksInventory: false,
    blocksShipment: false,
    blocksProduction: false,
    owner: "吳品保",
    dueTime: "14:30",
    documents: [
      { type: "首件檢驗", no: "FQC-20260523-006", status: "完整", owner: "品保", tone: "success" },
      { type: "金檢紀錄", no: "METAL-20260523-A1", status: "完整", owner: "現場", tone: "success" }
    ],
    workflow: [
      { label: "工單", ref: "WO-20260523-001", status: "完成", tone: "success" },
      { label: "抽樣", ref: "SAMPLE-20260523-006", status: "完成", tone: "success" },
      { label: "檢驗", ref: "QC-20260523-006", status: "進行中", tone: "info" },
      { label: "放行", ref: "REL-待完成", status: "待處理", tone: "success" }
    ]
  },
  {
    id: "QC-20260523-015",
    itemName: "即食雞胸肉",
    itemNo: "FG-CHICKEN-315",
    batchNo: "FG260523-CHICKEN",
    sourceType: "生產",
    sourceNo: "PROC-20260523-008",
    workOrder: "WO-20260523-003",
    salesOrder: "SO-20260523-027",
    supplier: null,
    line: "C3 包裝產線",
    inspectionType: "成品",
    stage: "待判定",
    decision: "待判",
    tone: "warning",
    sampleCount: 36,
    defectCount: 2,
    defectRate: 5.6,
    pendingTests: ["微生物快篩"],
    issueReason: "微生物快篩等待判定，暫緩入庫與出貨。",
    blocksInventory: true,
    blocksShipment: true,
    blocksProduction: false,
    owner: "林檢驗員",
    dueTime: "15:10",
    documents: [
      { type: "成品檢驗", no: "QC-20260523-015", status: "完整", owner: "品保", tone: "success" },
      { type: "微生物快篩", no: "MICRO-20260523-015", status: "待補", owner: "品保", tone: "warning" }
    ],
    workflow: [
      { label: "生產", ref: "WO-20260523-003", status: "完成", tone: "success" },
      { label: "抽樣", ref: "SAMPLE-20260523-015", status: "完成", tone: "success" },
      { label: "檢驗", ref: "QC-20260523-015", status: "進行中", tone: "info" },
      { label: "入庫", ref: "INV-暫緩", status: "阻擋", tone: "warning" },
      { label: "出貨", ref: "SHIP-暫緩", status: "阻擋", tone: "warning" }
    ]
  },
  {
    id: "QC-20260523-018",
    itemName: "冷凍玉米粒",
    itemNo: "RM-CORN-001",
    batchNo: "RM260506-CORN",
    sourceType: "收貨",
    sourceNo: "GRN-20260506-018",
    workOrder: "WO-20260523-002",
    salesOrder: "SO-20260523-022",
    supplier: "綠田食品",
    line: "B2 冷凍蔬菜產線",
    inspectionType: "原料",
    stage: "隔離",
    decision: "隔離",
    tone: "danger",
    sampleCount: 12,
    defectCount: 1,
    defectRate: 8.3,
    pendingTests: ["COA", "運輸溫度紀錄"],
    issueReason: "供應商 COA 與運輸溫度紀錄待補，且原料效期風險高。",
    blocksInventory: true,
    blocksShipment: false,
    blocksProduction: true,
    owner: "QA 主管",
    dueTime: "11:00",
    documents: [
      { type: "COA", no: "COA-RM260506-CORN", status: "待補", owner: "採購", tone: "warning" },
      { type: "運輸溫度", no: "TEMP-GRN-20260506-018", status: "待補", owner: "品保", tone: "warning" },
      { type: "收貨單", no: "GRN-20260506-018", status: "完整", owner: "倉庫", tone: "success" }
    ],
    workflow: [
      { label: "收貨", ref: "GRN-20260506-018", status: "完成", tone: "success" },
      { label: "抽樣", ref: "SAMPLE-20260523-018", status: "完成", tone: "success" },
      { label: "文件", ref: "COA/TEMP-待補", status: "阻擋", tone: "warning" },
      { label: "隔離", ref: "HOLD-RM260506-CORN", status: "進行中", tone: "danger" },
      { label: "生產", ref: "WO-20260523-002", status: "阻擋", tone: "danger" }
    ]
  }
];

export const qualityDashboardMock: QualityDashboardData = {
  summary: qualitySummary,
  inspections: qualityInspections
};
