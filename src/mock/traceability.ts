import type { TraceBatchOverview, TraceabilityDashboardData } from "@/types/traceability";

export const traceabilityDashboardMock: TraceabilityDashboardData = {
  summary: {
    traceableBatchCount: 1284,
    completeTraceRate: 99.2,
    brokenTraceCount: 7,
    highRiskTraceCount: 3
  },
  kpis: [
    { label: "可追溯批號", value: "1,284", hint: "符合目前查詢條件的批號", tone: "info" },
    { label: "鏈路完整率", value: "99.20%", hint: "完整追溯批號比例", tone: "success" },
    { label: "斷鏈追溯", value: "7", hint: "追到不可再追溯的批號", tone: "danger" },
    { label: "高風險追溯", value: "3", hint: "斷鏈、過期或品檢保留", tone: "danger" }
  ],
  records: [
    {
      traceId: "TRACE-FG260523-CURRY",
      traceDirectionCode: "upstream",
      traceDirectionLabel: "製成品往上游",
      itemNo: "FG-CURRY-001",
      itemName: "咖哩雞肉調理包",
      itemCategory: 5,
      itemCategoryLabel: "製成品",
      itemSubCategory: 0,
      itemType: 0,
      batchNo: "FG260523-CURRY",
      refCategory: 2,
      refCategoryLabel: "生產",
      refNo: "WO-20260523-001",
      partnerTypeCode: "internal",
      partnerTypeLabel: "內部",
      partnerNo: "",
      partnerName: "",
      workOrderNo: "WO-20260523-001",
      warehouseNo: "WH-FG-FZ",
      warehouseName: "成品冷凍庫",
      currentQuantity: 12000,
      unit: 109,
      unitLabel: "盒",
      traceStatusCode: "complete",
      traceStatusLabel: "完整",
      riskLevelCode: "normal",
      riskLevelLabel: "正常",
      riskCode: "normal",
      riskLabel: "正常",
      latestEventTimestamp: 1779552000,
      latestEventDate: "2026/5/24",
      tone: "success"
    },
    {
      traceId: "TRACE-RM260506-CORN",
      traceDirectionCode: "downstream",
      traceDirectionLabel: "原料往下游",
      itemNo: "RM-CORN-001",
      itemName: "冷凍玉米粒",
      itemCategory: 1,
      itemCategoryLabel: "原料",
      itemSubCategory: 0,
      itemType: 0,
      batchNo: "RM260506-CORN",
      refCategory: 1,
      refCategoryLabel: "採購",
      refNo: "GRN-20260506-018",
      partnerTypeCode: "supplier",
      partnerTypeLabel: "供應商",
      partnerNo: "SUP-GREEN",
      partnerName: "綠田食品",
      workOrderNo: "WO-20260523-002",
      warehouseNo: "WH-RM-FZ",
      warehouseName: "原料冷凍庫",
      currentQuantity: 180,
      unit: 2,
      unitLabel: "公斤",
      traceStatusCode: "broken",
      traceStatusLabel: "斷鏈",
      riskLevelCode: "high_risk",
      riskLevelLabel: "高風險",
      riskCode: "broken_chain",
      riskLabel: "追溯斷鏈",
      latestEventTimestamp: 1779465600,
      latestEventDate: "2026/5/23",
      tone: "danger"
    }
  ],
  total: 2,
  start: 0,
  count: 2
};

export const traceabilityOverviewMock: Record<string, TraceBatchOverview> = {
  "FG260523-CURRY": {
    batch: {
      batchNo: "FG260523-CURRY",
      itemNo: "FG-CURRY-001",
      itemName: "咖哩雞肉調理包",
      itemCategory: 5,
      itemCategoryLabel: "製成品",
      itemSubCategory: 0,
      itemType: 0,
      unit: 109,
      unitLabel: "盒",
      validDate: 1782144000,
      validDateLabel: "2026/6/23",
      validDays: 30,
      refCategory: 2,
      refCategoryLabel: "生產",
      refNo: "WO-20260523-001",
      traceDirectionCode: "upstream",
      traceDirectionLabel: "製成品往上游",
      traceStatusCode: "complete",
      traceStatusLabel: "完整",
      riskLevelCode: "normal",
      riskLevelLabel: "正常",
      riskCode: "normal",
      riskLabel: "正常",
      tone: "success"
    },
    traceSteps: [
      {
        stepId: "production:WO-20260523-001",
        stepTypeCode: "production",
        stepTypeLabel: "產製",
        eventTimestamp: 1779465600,
        eventDate: "2026/5/23",
        refCategory: 2,
        refCategoryLabel: "生產",
        refNo: "WO-20260523-001",
        statusCode: "complete",
        statusLabel: "完成",
        riskLevelCode: "normal",
        riskLevelLabel: "正常",
        inputItems: [
          {
            itemNo: "WIP-CURRY-SAUCE",
            itemName: "咖哩醬在製品",
            itemCategory: 4,
            itemCategoryLabel: "在製品",
            batchNo: "WIP260523-CURRY",
            quantity: 780,
            unit: 2,
            unitLabel: "公斤"
          }
        ],
        outputItems: [
          {
            itemNo: "FG-CURRY-001",
            itemName: "咖哩雞肉調理包",
            itemCategory: 5,
            itemCategoryLabel: "製成品",
            batchNo: "FG260523-CURRY",
            quantity: 12000,
            unit: 109,
            unitLabel: "盒"
          }
        ],
        tone: "success"
      },
      {
        stepId: "production:WO-20260522-004",
        stepTypeCode: "production",
        stepTypeLabel: "產製",
        eventTimestamp: 1779379200,
        eventDate: "2026/5/22",
        refCategory: 2,
        refCategoryLabel: "生產",
        refNo: "WO-20260522-004",
        statusCode: "complete",
        statusLabel: "完成",
        riskLevelCode: "normal",
        riskLevelLabel: "正常",
        inputItems: [
          {
            itemNo: "RM-CHICKEN-001",
            itemName: "雞胸肉原料",
            itemCategory: 1,
            itemCategoryLabel: "原料",
            batchNo: "RM260520-CHK",
            quantity: 420,
            unit: 2,
            unitLabel: "公斤"
          },
          {
            itemNo: "RM-CORN-001",
            itemName: "冷凍玉米粒",
            itemCategory: 1,
            itemCategoryLabel: "原料",
            batchNo: "RM260506-CORN",
            quantity: 180,
            unit: 2,
            unitLabel: "公斤"
          }
        ],
        outputItems: [
          {
            itemNo: "WIP-CURRY-SAUCE",
            itemName: "咖哩醬在製品",
            itemCategory: 4,
            itemCategoryLabel: "在製品",
            batchNo: "WIP260523-CURRY",
            quantity: 780,
            unit: 2,
            unitLabel: "公斤"
          }
        ],
        tone: "success"
      }
    ]
  },
  "RM260506-CORN": {
    batch: {
      batchNo: "RM260506-CORN",
      itemNo: "RM-CORN-001",
      itemName: "冷凍玉米粒",
      itemCategory: 1,
      itemCategoryLabel: "原料",
      itemSubCategory: 0,
      itemType: 0,
      unit: 2,
      unitLabel: "公斤",
      validDate: 1779897600,
      validDateLabel: "2026/5/28",
      validDays: 22,
      refCategory: 1,
      refCategoryLabel: "採購",
      refNo: "GRN-20260506-018",
      traceDirectionCode: "downstream",
      traceDirectionLabel: "原料往下游",
      traceStatusCode: "broken",
      traceStatusLabel: "斷鏈",
      riskLevelCode: "high_risk",
      riskLevelLabel: "高風險",
      riskCode: "broken_chain",
      riskLabel: "追溯斷鏈",
      tone: "danger"
    },
    traceSteps: [
      {
        stepId: "receipt:GRN-20260506-018",
        stepTypeCode: "receipt",
        stepTypeLabel: "進貨",
        eventTimestamp: 1777996800,
        eventDate: "2026/5/6",
        refCategory: 1,
        refCategoryLabel: "採購",
        refNo: "GRN-20260506-018",
        statusCode: "complete",
        statusLabel: "完成",
        riskLevelCode: "normal",
        riskLevelLabel: "正常",
        inputItems: [],
        outputItems: [
          {
            itemNo: "RM-CORN-001",
            itemName: "冷凍玉米粒",
            itemCategory: 1,
            itemCategoryLabel: "原料",
            batchNo: "RM260506-CORN",
            quantity: 180,
            unit: 2,
            unitLabel: "公斤"
          }
        ],
        tone: "success"
      },
      {
        stepId: "production:WO-20260522-004",
        stepTypeCode: "production",
        stepTypeLabel: "產製",
        eventTimestamp: 1779379200,
        eventDate: "2026/5/22",
        refCategory: 2,
        refCategoryLabel: "生產",
        refNo: "WO-20260522-004",
        statusCode: "missing",
        statusLabel: "缺漏",
        riskLevelCode: "high_risk",
        riskLevelLabel: "高風險",
        inputItems: [
          {
            itemNo: "RM-CORN-001",
            itemName: "冷凍玉米粒",
            itemCategory: 1,
            itemCategoryLabel: "原料",
            batchNo: "RM260506-CORN",
            quantity: 180,
            unit: 2,
            unitLabel: "公斤"
          }
        ],
        outputItems: [],
        tone: "danger"
      }
    ]
  }
};
