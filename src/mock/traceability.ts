import type { TraceRecord, TraceSummary } from "@/types/traceability";

export const traceSummary: TraceSummary[] = [
  {
    label: "可追溯批號",
    value: "1,284",
    hint: "近 90 天",
    tone: "info"
  },
  {
    label: "鏈路完整率",
    value: "99.2%",
    hint: "+0.4%",
    tone: "success"
  },
  {
    label: "待補文件",
    value: "7",
    hint: "COA 2、溫度 3、品檢 2",
    tone: "warning"
  },
  {
    label: "召回影響批次",
    value: "3",
    hint: "本月演練",
    tone: "danger"
  }
];

export const traceRecords: TraceRecord[] = [
  {
    id: "TRACE-FG260523-CURRY",
    queryType: "批號",
    queryValue: "FG260523-CURRY",
    direction: "成品到原料",
    itemName: "咖哩雞肉調理包",
    batchNo: "FG260523-CURRY",
    sourceType: "生產",
    supplier: null,
    customer: "全聯中區 DC",
    sourceDocument: "WO-20260523-001",
    workOrder: "WO-20260523-001",
    salesOrder: "SO-20260523-018",
    quantity: 12000,
    unit: "盒",
    warehouseName: "成品冷凍庫",
    shipTo: "全聯中區 DC",
    traceStatus: "完整",
    riskReason: "原料、製程、品檢、入庫、出貨鏈路完整。",
    impactedQty: 2400,
    impactedCustomers: 1,
    nodes: [
      { id: "SO-20260523-018", label: "訂單", ref: "全聯中區 DC", status: "完成", tone: "success" },
      { id: "RM260520-CHK", label: "原料批號", ref: "雞胸肉原料", status: "完整", tone: "success" },
      { id: "IP260521-SAUCE", label: "在製品", ref: "咖哩醬", status: "完整", tone: "success" },
      { id: "WO-20260523-001", label: "工單", ref: "A1 調理包產線", status: "完成", tone: "success" },
      { id: "QC-20260523-006", label: "品檢", ref: "首件通過", status: "完整", tone: "success" },
      { id: "SHIP-20260524-002", label: "出貨", ref: "冷鏈配送", status: "待出貨", tone: "info" }
    ],
    documents: [
      { type: "工單", no: "WO-20260523-001", status: "完整", owner: "生管", tone: "success" },
      { type: "品檢", no: "QC-20260523-006", status: "完整", owner: "品保", tone: "success" },
      { type: "出貨", no: "SHIP-20260524-002", status: "完整", owner: "物流", tone: "success" }
    ]
  },
  {
    id: "TRACE-RM260506-CORN",
    queryType: "批號",
    queryValue: "RM260506-CORN",
    direction: "原料到成品",
    itemName: "冷凍玉米粒",
    batchNo: "RM260506-CORN",
    sourceType: "採購",
    supplier: "綠田食品",
    customer: "便利商店北區",
    sourceDocument: "GRN-20260506-018",
    workOrder: "WO-20260523-002",
    salesOrder: "SO-20260523-022",
    quantity: 180,
    unit: "kg",
    warehouseName: "原料冷凍庫",
    shipTo: null,
    traceStatus: "待補文件",
    riskReason: "供應商 COA 與運輸溫度紀錄待補，且此批原料影響 B2 產線。",
    impactedQty: 7200,
    impactedCustomers: 1,
    nodes: [
      { id: "SUP-GREEN", label: "供應商", ref: "綠田食品", status: "待補文件", tone: "warning" },
      { id: "GRN-20260506-018", label: "收貨", ref: "冷凍玉米粒", status: "完成", tone: "success" },
      { id: "RM260506-CORN", label: "原料批號", ref: "剩餘 180 kg", status: "效期風險", tone: "danger" },
      { id: "WO-20260523-002", label: "工單", ref: "綜合冷凍蔬菜", status: "待備料", tone: "warning" },
      { id: "SO-20260523-022", label: "訂單", ref: "便利商店北區", status: "交期高風險", tone: "danger" }
    ],
    documents: [
      { type: "COA", no: "COA-RM260506-CORN", status: "待補", owner: "採購", tone: "warning" },
      { type: "運輸溫度", no: "TEMP-GRN-20260506-018", status: "待補", owner: "品保", tone: "warning" },
      { type: "收貨單", no: "GRN-20260506-018", status: "完整", owner: "倉庫", tone: "success" }
    ]
  }
];
