import type { RdDashboardData, RdProject, RdSummary } from "@/types/rd";

export const rdSummary: RdSummary[] = [
  { label: "開發案", value: "14", hint: "試作中 5、報價中 4", tone: "info" },
  { label: "BOM 待審", value: "6", hint: "2 筆影響報價", tone: "warning" },
  { label: "毛利不足", value: "3", hint: "低於目標 18%", tone: "danger" },
  { label: "可量產移轉", value: "4", hint: "等待主檔生效", tone: "success" }
];

export const rdProjects: RdProject[] = [
  {
    id: "RD-20260523-008",
    customer: "全聯中區 DC",
    productName: "咖哩雞肉調理包減鈉版",
    targetChannel: "冷凍食品",
    stage: "報價中",
    decision: "可報價",
    tone: "success",
    priority: "高",
    owner: "研發一組",
    targetLaunchDate: "2026-07-01",
    sampleDueDate: "2026-05-30",
    bomNo: "BOM-FG-CURRY-101",
    bomVersion: "v3.3-Q",
    bomStatus: "報價版",
    targetPrice: 68,
    suggestedQuote: 72,
    minimumQuote: 66,
    targetMarginRate: 20,
    estimatedMarginRate: 21.8,
    totalUnitCost: 56.3,
    materialCost: 32.4,
    packagingCost: 8.6,
    laborCost: 6.8,
    overheadCost: 5.1,
    logisticsCost: 3.4,
    lossRate: 2.8,
    quoteRiskReason: "減鈉配方已試作通過，成本仍符合目標毛利，可進入報價。",
    transferReadiness: "需待客戶確認口味後轉量產 BOM。",
    costLines: [
      { category: "原料", itemName: "雞腿肉丁", version: "RM-CHICKEN-001", unitCost: 98, usageQty: 0.22, lossRate: 2.5, costAmount: 22.1, note: "主料", tone: "success" },
      { category: "原料", itemName: "減鈉咖哩醬基底", version: "WIP-SAUCE-009", unitCost: 64, usageQty: 0.16, lossRate: 3.2, costAmount: 10.3, note: "新配方", tone: "info" },
      { category: "包材", itemName: "耐熱殺菌袋", version: "PK-BAG-010", unitCost: 4.8, usageQty: 1, lossRate: 1.5, costAmount: 4.9, note: "共用包材", tone: "success" },
      { category: "人工", itemName: "A1 調理包標準工時", version: "STD-A1", unitCost: 6.8, usageQty: 1, lossRate: 0, costAmount: 6.8, note: "標準人工", tone: "success" },
      { category: "製造費用", itemName: "殺菌/冷凍製造費", version: "OH-202605", unitCost: 5.1, usageQty: 1, lossRate: 0, costAmount: 5.1, note: "月度費率", tone: "success" },
      { category: "物流", itemName: "冷凍配送攤提", version: "LOG-FROZEN", unitCost: 3.4, usageQty: 1, lossRate: 0, costAmount: 3.4, note: "中區", tone: "success" }
    ],
    workflow: [
      { label: "需求", ref: "REQ-20260520-003", status: "完成", tone: "success" },
      { label: "試作", ref: "TRIAL-20260522-002", status: "完成", tone: "success" },
      { label: "成本", ref: "COST-RD-008", status: "完成", tone: "success" },
      { label: "報價", ref: "QUOTE-待建立", status: "進行中", tone: "info" },
      { label: "量產", ref: "BOM-v3.3-待生效", status: "待處理", tone: "warning" }
    ]
  },
  {
    id: "RD-20260523-011",
    customer: "便利商店北區",
    productName: "番茄牛肉燉飯",
    targetChannel: "即食餐盒",
    stage: "成本試算",
    decision: "需調整",
    tone: "warning",
    priority: "高",
    owner: "研發二組",
    targetLaunchDate: "2026-07-15",
    sampleDueDate: "2026-06-02",
    bomNo: "BOM-FG-RICE-003",
    bomVersion: "v0.9-C",
    bomStatus: "試作版",
    targetPrice: 59,
    suggestedQuote: 64,
    minimumQuote: 61,
    targetMarginRate: 18,
    estimatedMarginRate: 15.4,
    totalUnitCost: 54.1,
    materialCost: 34.8,
    packagingCost: 7.2,
    laborCost: 5.4,
    overheadCost: 4.7,
    logisticsCost: 2,
    lossRate: 4.5,
    quoteRiskReason: "牛肉成本偏高且試作耗損率高，若以客戶目標價報價會低於目標毛利。",
    transferReadiness: "需調整肉料比例或取得替代供應報價後再送報價版。",
    costLines: [
      { category: "原料", itemName: "牛肉丁", version: "RM-BEEF-020", unitCost: 186, usageQty: 0.12, lossRate: 5.5, costAmount: 23.5, note: "成本偏高", tone: "danger" },
      { category: "原料", itemName: "番茄醬基底", version: "WIP-TOMATO-003", unitCost: 48, usageQty: 0.15, lossRate: 3, costAmount: 7.4, note: "試作版", tone: "warning" },
      { category: "包材", itemName: "微波餐盒", version: "PK-TRAY-018", unitCost: 6.9, usageQty: 1, lossRate: 2, costAmount: 7.2, note: "需確認耐熱", tone: "warning" },
      { category: "人工", itemName: "餐盒線標準工時", version: "STD-C2", unitCost: 5.4, usageQty: 1, lossRate: 0, costAmount: 5.4, note: "標準人工", tone: "success" },
      { category: "製造費用", itemName: "調理/包裝製造費", version: "OH-202605", unitCost: 4.7, usageQty: 1, lossRate: 0, costAmount: 4.7, note: "月度費率", tone: "success" },
      { category: "物流", itemName: "冷藏配送攤提", version: "LOG-CHILLED", unitCost: 2, usageQty: 1, lossRate: 0, costAmount: 2, note: "北區", tone: "success" }
    ],
    workflow: [
      { label: "需求", ref: "REQ-20260521-005", status: "完成", tone: "success" },
      { label: "試作", ref: "TRIAL-20260523-004", status: "進行中", tone: "info" },
      { label: "成本", ref: "COST-RD-011", status: "進行中", tone: "warning" },
      { label: "報價", ref: "QUOTE-未建立", status: "待處理", tone: "warning" },
      { label: "量產", ref: "BOM-待核准", status: "待處理", tone: "warning" }
    ]
  },
  {
    id: "RD-20260523-014",
    customer: "餐飲通路南區",
    productName: "即食雞胸肉黑胡椒版",
    targetChannel: "團膳",
    stage: "量產移轉",
    decision: "可報價",
    tone: "success",
    priority: "中",
    owner: "研發一組",
    targetLaunchDate: "2026-06-20",
    sampleDueDate: "2026-05-28",
    bomNo: "BOM-FG-CHICKEN-315",
    bomVersion: "v2.1-P",
    bomStatus: "量產版",
    targetPrice: 78,
    suggestedQuote: 82,
    minimumQuote: 76,
    targetMarginRate: 18,
    estimatedMarginRate: 20.1,
    totalUnitCost: 65.5,
    materialCost: 43.2,
    packagingCost: 6.5,
    laborCost: 7.1,
    overheadCost: 5.2,
    logisticsCost: 3.5,
    lossRate: 2.1,
    quoteRiskReason: "配方、包材、品檢標準已確認，待主檔與量產 BOM 生效。",
    transferReadiness: "可移轉至 Items/BOM，供 Orders 與 Planning 引用。",
    costLines: [
      { category: "原料", itemName: "雞胸肉", version: "RM-CHICKEN-315", unitCost: 142, usageQty: 0.28, lossRate: 2, costAmount: 40.6, note: "主料", tone: "success" },
      { category: "物料", itemName: "黑胡椒調味粉", version: "RM-SPICE-011", unitCost: 82, usageQty: 0.03, lossRate: 1.5, costAmount: 2.6, note: "調味", tone: "success" },
      { category: "包材", itemName: "真空袋", version: "PK-VAC-006", unitCost: 6.4, usageQty: 1, lossRate: 1, costAmount: 6.5, note: "量產包材", tone: "success" },
      { category: "人工", itemName: "C3 包裝線標準工時", version: "STD-C3", unitCost: 7.1, usageQty: 1, lossRate: 0, costAmount: 7.1, note: "標準人工", tone: "success" },
      { category: "製造費用", itemName: "蒸煮/包裝製造費", version: "OH-202605", unitCost: 5.2, usageQty: 1, lossRate: 0, costAmount: 5.2, note: "月度費率", tone: "success" },
      { category: "物流", itemName: "冷藏配送攤提", version: "LOG-CHILLED", unitCost: 3.5, usageQty: 1, lossRate: 0, costAmount: 3.5, note: "南區", tone: "success" }
    ],
    workflow: [
      { label: "需求", ref: "REQ-20260518-002", status: "完成", tone: "success" },
      { label: "試作", ref: "TRIAL-20260520-001", status: "完成", tone: "success" },
      { label: "成本", ref: "COST-RD-014", status: "完成", tone: "success" },
      { label: "報價", ref: "QUOTE-20260522-006", status: "完成", tone: "success" },
      { label: "量產", ref: "BOM-v2.1-P", status: "進行中", tone: "info" }
    ]
  }
];

export const rdDashboardMock: RdDashboardData = {
  summary: rdSummary,
  projects: rdProjects
};
