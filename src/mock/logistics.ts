import type { LogisticsSummary, Shipment } from "@/types/logistics";

export const logisticsSummary: LogisticsSummary[] = [
  {
    label: "今日出貨",
    value: "18",
    hint: "已派車 13、待派 5",
    tone: "info"
  },
  {
    label: "交付高風險",
    value: "3",
    hint: "品檢 1、倉庫 1、派車 1",
    tone: "danger"
  },
  {
    label: "冷鏈注意",
    value: "2",
    hint: "1 筆短暫偏溫",
    tone: "warning"
  },
  {
    label: "簽收完成",
    value: "9",
    hint: "電子簽收 8、紙本 1",
    tone: "success"
  }
];

export const shipments: Shipment[] = [
  {
    id: "SHIP-20260524-002",
    salesOrder: "SO-20260523-018",
    customer: "全聯中區 DC",
    channel: "冷凍食品",
    destination: "台中常溫/冷凍轉運中心",
    route: "中區冷凍 R2",
    product: "咖哩雞肉調理包",
    batchNo: "FG260523-CURRY",
    quantity: 12000,
    unit: "盒",
    requestedArrivalTime: "2026-05-24 10:30",
    plannedDepartureTime: "2026-05-24 07:30",
    stage: "裝車中",
    tone: "info",
    deliveryRisk: "正常",
    riskReason: "品檢已放行、倉庫覆核完成，冷鏈車次已到廠裝車。",
    warehouseStatus: "已出庫",
    qualityReleaseStatus: "已放行",
    vehicleNo: "KLA-2389",
    driver: "陳志明",
    temperatureRequirement: "-18°C",
    currentTemperature: "-18.4°C",
    temperatureStatus: "正常",
    documentsReady: true,
    proofOfDeliveryStatus: "未簽收",
    owner: "物流一組",
    documents: [
      { type: "出貨單", no: "SHIP-20260524-002", status: "完整", owner: "物流", tone: "success" },
      { type: "溫度紀錄", no: "TEMP-KLA-2389", status: "完整", owner: "司機", tone: "success" },
      { type: "品檢放行", no: "QC-20260523-006", status: "完整", owner: "品保", tone: "success" }
    ],
    workflow: [
      { label: "訂單", ref: "SO-20260523-018", status: "完成", tone: "success" },
      { label: "品檢", ref: "QC-20260523-006", status: "完成", tone: "success" },
      { label: "出庫", ref: "PICK-20260523-004", status: "完成", tone: "success" },
      { label: "裝車", ref: "KLA-2389", status: "進行中", tone: "info" },
      { label: "簽收", ref: "POD-待回傳", status: "待處理", tone: "info" }
    ]
  },
  {
    id: "SHIP-20260524-007",
    salesOrder: "SO-20260523-022",
    customer: "便利商店北區",
    channel: "即食餐盒",
    destination: "桃園北區 DC",
    route: "北區冷凍 R5",
    product: "綜合冷凍蔬菜",
    batchNo: "FG-待生產",
    quantity: 7200,
    unit: "包",
    requestedArrivalTime: "2026-05-24 11:00",
    plannedDepartureTime: "未排定",
    stage: "暫緩出貨",
    tone: "danger",
    deliveryRisk: "高風險",
    riskReason: "訂單仍受缺料與 B2 產能衝突影響，尚未形成可出貨庫存。",
    warehouseStatus: "阻擋",
    qualityReleaseStatus: "阻擋",
    vehicleNo: null,
    driver: null,
    temperatureRequirement: "-18°C",
    currentTemperature: null,
    temperatureStatus: "注意",
    documentsReady: false,
    proofOfDeliveryStatus: "未簽收",
    owner: "物流二組",
    documents: [
      { type: "出貨單", no: "SHIP-待建立", status: "缺失", owner: "物流", tone: "danger" },
      { type: "品檢放行", no: "QC-待建立", status: "缺失", owner: "品保", tone: "danger" },
      { type: "冷鏈車次", no: "TRUCK-待排", status: "待補", owner: "物流", tone: "warning" }
    ],
    workflow: [
      { label: "訂單", ref: "SO-20260523-022", status: "完成", tone: "success" },
      { label: "計劃", ref: "PLAN-20260523-022", status: "阻擋", tone: "danger" },
      { label: "品檢", ref: "QC-待建立", status: "待處理", tone: "warning" },
      { label: "出庫", ref: "PICK-待建立", status: "阻擋", tone: "danger" },
      { label: "派車", ref: "TRUCK-待排", status: "待處理", tone: "warning" }
    ]
  },
  {
    id: "SHIP-20260523-011",
    salesOrder: "SO-20260523-027",
    customer: "餐飲通路南區",
    channel: "團膳",
    destination: "高雄南區冷鏈倉",
    route: "南區冷藏 R3",
    product: "即食雞胸肉",
    batchNo: "FG260523-CHICKEN",
    quantity: 4800,
    unit: "包",
    requestedArrivalTime: "2026-05-23 17:30",
    plannedDepartureTime: "暫緩",
    stage: "暫緩出貨",
    tone: "warning",
    deliveryRisk: "注意",
    riskReason: "成品已完成，但微生物快篩待判，暫緩入庫與出貨。",
    warehouseStatus: "待覆核",
    qualityReleaseStatus: "待判定",
    vehicleNo: "KLC-7712",
    driver: "林俊宏",
    temperatureRequirement: "0-4°C",
    currentTemperature: "4.8°C",
    temperatureStatus: "注意",
    documentsReady: false,
    proofOfDeliveryStatus: "未簽收",
    owner: "物流一組",
    documents: [
      { type: "出貨單", no: "SHIP-20260523-011", status: "完整", owner: "物流", tone: "success" },
      { type: "品檢放行", no: "QC-20260523-015", status: "待補", owner: "品保", tone: "warning" },
      { type: "溫度紀錄", no: "TEMP-KLC-7712", status: "待補", owner: "司機", tone: "warning" }
    ],
    workflow: [
      { label: "訂單", ref: "SO-20260523-027", status: "完成", tone: "success" },
      { label: "生產", ref: "WO-20260523-003", status: "完成", tone: "success" },
      { label: "品檢", ref: "QC-20260523-015", status: "阻擋", tone: "warning" },
      { label: "出庫", ref: "PICK-暫緩", status: "阻擋", tone: "warning" },
      { label: "派車", ref: "KLC-7712", status: "待處理", tone: "info" }
    ]
  }
];

