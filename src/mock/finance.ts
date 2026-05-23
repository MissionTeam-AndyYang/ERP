import type { FinanceOrderCase, FinanceSummary } from "@/types/finance";

export const financeSummary: FinanceSummary[] = [
  {
    label: "本月出貨收入",
    value: "$18.6M",
    hint: "已簽收可請款 $9.8M",
    tone: "success"
  },
  {
    label: "毛利需追蹤",
    value: "5",
    hint: "低於預估或低於門檻",
    tone: "warning"
  },
  {
    label: "待請款",
    value: "$3.2M",
    hint: "POD 完成 8 筆",
    tone: "info"
  },
  {
    label: "逾期應收",
    value: "$1.1M",
    hint: "3 筆超過 7 天",
    tone: "danger"
  }
];

export const financeOrderCases: FinanceOrderCase[] = [
  {
    id: "FIN-SO-20260523-018",
    salesOrder: "SO-20260523-018",
    shipmentNo: "SHIP-20260524-002",
    customer: "全聯中區 DC",
    product: "咖哩雞肉調理包",
    orderAmount: 780000,
    estimatedCost: 612000,
    actualCost: 617760,
    estimatedMarginRate: 21.5,
    actualMarginRate: 20.8,
    marginVarianceRate: -0.7,
    riskLevel: "正常",
    riskReason: "實際成本略高於預估，但仍在毛利門檻內；待 POD 回傳後可請款。",
    arStatus: "待請款",
    invoiceNo: null,
    paymentTerm: "月結 30 天",
    dueDate: "2026-06-24",
    collectedAmount: 0,
    payableImpact: 286000,
    inventoryCostImpact: 186000,
    productionCostImpact: 122000,
    logisticsCostImpact: 23760,
    podStatus: "未簽收",
    owner: "財務一組",
    tone: "success",
    documents: [
      { type: "出貨單", no: "SHIP-20260524-002", status: "完整", owner: "物流", tone: "success" },
      { type: "POD 簽收", no: "POD-待回傳", status: "待補", owner: "物流", tone: "info" },
      { type: "發票", no: "INV-待開立", status: "待補", owner: "財務", tone: "warning" }
    ],
    workflow: [
      { label: "訂單", ref: "SO-20260523-018", status: "完成", tone: "success" },
      { label: "出貨", ref: "SHIP-20260524-002", status: "進行中", tone: "info" },
      { label: "簽收", ref: "POD-待回傳", status: "待處理", tone: "info" },
      { label: "請款", ref: "INV-待開立", status: "待處理", tone: "warning" },
      { label: "收款", ref: "AR-月結", status: "待處理", tone: "info" }
    ]
  },
  {
    id: "FIN-SO-20260523-022",
    salesOrder: "SO-20260523-022",
    shipmentNo: null,
    customer: "便利商店北區",
    product: "綜合冷凍蔬菜",
    orderAmount: 396000,
    estimatedCost: 326000,
    actualCost: null,
    estimatedMarginRate: 17.7,
    actualMarginRate: null,
    marginVarianceRate: null,
    riskLevel: "高風險",
    riskReason: "缺料造成急採與產能重排，預估毛利可能下修；尚未形成可出貨與請款條件。",
    arStatus: "未請款",
    invoiceNo: null,
    paymentTerm: "出貨後 30 天",
    dueDate: "未成立",
    collectedAmount: 0,
    payableImpact: 86000,
    inventoryCostImpact: 0,
    productionCostImpact: 0,
    logisticsCostImpact: 0,
    podStatus: "未簽收",
    owner: "財務二組",
    tone: "danger",
    documents: [
      { type: "計劃風險", no: "PLAN-20260523-022", status: "完整", owner: "計劃", tone: "warning" },
      { type: "出貨單", no: "SHIP-待建立", status: "缺失", owner: "物流", tone: "danger" },
      { type: "成本試算", no: "COST-待更新", status: "待補", owner: "財務", tone: "warning" }
    ],
    workflow: [
      { label: "訂單", ref: "SO-20260523-022", status: "完成", tone: "success" },
      { label: "計劃", ref: "PLAN-20260523-022", status: "阻擋", tone: "danger" },
      { label: "採購", ref: "PR-建議", status: "待處理", tone: "warning" },
      { label: "出貨", ref: "SHIP-待建立", status: "阻擋", tone: "danger" },
      { label: "請款", ref: "INV-未成立", status: "待處理", tone: "warning" }
    ]
  },
  {
    id: "FIN-SO-20260523-027",
    salesOrder: "SO-20260523-027",
    shipmentNo: "SHIP-20260523-011",
    customer: "餐飲通路南區",
    product: "即食雞胸肉",
    orderAmount: 336000,
    estimatedCost: 282000,
    actualCost: 286944,
    estimatedMarginRate: 16.1,
    actualMarginRate: 14.6,
    marginVarianceRate: -1.5,
    riskLevel: "注意",
    riskReason: "品檢待判造成出貨暫緩，實際毛利低於預估 1.5%；需確認是否仍符合接單毛利門檻。",
    arStatus: "未請款",
    invoiceNo: null,
    paymentTerm: "出貨後 30 天",
    dueDate: "未成立",
    collectedAmount: 0,
    payableImpact: 136000,
    inventoryCostImpact: 76000,
    productionCostImpact: 68944,
    logisticsCostImpact: 6000,
    podStatus: "未簽收",
    owner: "財務一組",
    tone: "warning",
    documents: [
      { type: "品檢放行", no: "QC-20260523-015", status: "待補", owner: "品保", tone: "warning" },
      { type: "出貨單", no: "SHIP-20260523-011", status: "完整", owner: "物流", tone: "success" },
      { type: "發票", no: "INV-待開立", status: "待補", owner: "財務", tone: "warning" }
    ],
    workflow: [
      { label: "訂單", ref: "SO-20260523-027", status: "完成", tone: "success" },
      { label: "品檢", ref: "QC-20260523-015", status: "阻擋", tone: "warning" },
      { label: "出貨", ref: "SHIP-20260523-011", status: "阻擋", tone: "warning" },
      { label: "請款", ref: "INV-待開立", status: "待處理", tone: "warning" },
      { label: "收款", ref: "AR-待成立", status: "待處理", tone: "info" }
    ]
  }
];

