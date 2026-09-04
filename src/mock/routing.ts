import type { RoutingDashboardData, RoutingDetail } from "@/types/routing";

export const routingDashboardMock: RoutingDashboardData = {
  summary: {
    itemCount: 2,
    routingVersionCount: 3,
    effectiveRoutingCount: 2,
    warningCount: 1
  },
  kpis: [
    { label: "Product / WIP", value: "2", hint: "可查閱製程路線的品項", tone: "info" },
    { label: "Routing 版本", value: "3", hint: "目前查詢條件下的版本", tone: "neutral" },
    { label: "目前有效", value: "2", hint: "可作 read-only 引用", tone: "success" },
    { label: "待確認", value: "1", hint: "資源、標準表現或參照缺口", tone: "warning" }
  ],
  items: [
    {
      id: "PRD-LEMON-001-route-v2",
      itemNo: "PRD-LEMON-001",
      itemName: "檸檬飲製成品",
      itemTypeCode: "product",
      itemTypeLabel: "製成品",
      routingNo: "ROUTE-LEMON-001",
      routingVersionId: "ROUTE-LEMON-001",
      routingVersion: 2,
      versionStateCode: "effective",
      versionStateLabel: "目前有效",
      tone: "success",
      stepCount: 4,
      warningCount: 0,
      sourceLabel: "product_process / process_flow"
    },
    {
      id: "WIP-SYRUP-001-route-v1",
      itemNo: "WIP-SYRUP-001",
      itemName: "檸檬糖漿在製品",
      itemTypeCode: "wip",
      itemTypeLabel: "在製品",
      routingNo: "ROUTE-SYRUP-001",
      routingVersionId: "ROUTE-SYRUP-001",
      routingVersion: 1,
      versionStateCode: "warning",
      versionStateLabel: "待確認",
      tone: "warning",
      stepCount: 2,
      warningCount: 1,
      sourceLabel: "product_process / process_flow"
    }
  ],
  total: 2,
  start: 0,
  count: 2
};

export const routingDetailMock: Record<string, RoutingDetail> = {
  "PRD-LEMON-001": {
    item: routingDashboardMock.items[0],
    versions: [
      { version: 2, versionStateCode: "effective", versionStateLabel: "目前有效", tone: "success", effectiveDate: "2026/09/01", sourceLabel: "product_process" },
      { version: 1, versionStateCode: "historical", versionStateLabel: "歷史版本", tone: "neutral", effectiveDate: "2026/06/01", sourceLabel: "product_process" }
    ],
    steps: [
      {
        stepNo: 10,
        processNo: "PROC-MIX-001",
        processLabel: "調拌",
        stageLabel: "前備",
        groupLabel: "糖漿前備",
        standardQuantity: 120,
        standardUnit: "公斤",
        standardMinutes: 60,
        standardRateLabel: "120.00 公斤 / hr",
        resourceEligibilityLabel: "L1 前備線 / 2 人",
        sourceRef: "process_flow"
      },
      {
        stepNo: 20,
        processNo: "PROC-FILL-001",
        processLabel: "灌料",
        stageLabel: "前備",
        groupLabel: "充填前處理",
        standardQuantity: 96,
        standardUnit: "公斤",
        standardMinutes: 60,
        standardRateLabel: "96.00 公斤 / hr",
        resourceEligibilityLabel: "L2 充填線 / 3 人",
        sourceRef: "process_capacity"
      },
      {
        stepNo: 30,
        processNo: "PROC-SEAL-001",
        processLabel: "封膜",
        stageLabel: "加工",
        groupLabel: "封膜檢查",
        standardQuantity: 180,
        standardUnit: "瓶",
        standardMinutes: 60,
        standardRateLabel: "180.00 瓶 / hr",
        resourceEligibilityLabel: "L3 封膜線 / 2 人",
        sourceRef: "production_line"
      },
      {
        stepNo: 40,
        processNo: "PROC-CARTON-001",
        processLabel: "入箱",
        stageLabel: "包裝",
        groupLabel: "成品包裝",
        standardQuantity: 60,
        standardUnit: "箱",
        standardMinutes: 60,
        standardRateLabel: "60.00 箱 / hr",
        resourceEligibilityLabel: "PACK-01 / 2 人",
        sourceRef: "process_flow"
      }
    ],
    recipeReferences: [{ typeLabel: "Recipe reference", refNo: "RCP-260901", refName: "檸檬飲基礎製程配方", statusLabel: "已建立", tone: "success" }],
    packagingContexts: [{ typeLabel: "Packaging context", refNo: "PKG-LEMON-001", refName: "瓶裝入箱", statusLabel: "參照中", tone: "neutral" }],
    resourceEligibility: [{ typeLabel: "Resource eligibility", refNo: "LINE-GROUP-A", refName: "前備 / 加工 / 包裝可用線別", statusLabel: "受治理", tone: "success" }],
    standardPerformance: [{ typeLabel: "Standard performance", refNo: "CAP-202609", refName: "標準產出與人力基準", statusLabel: "受治理", tone: "success" }],
    lineage: [
      { sourceTypeLabel: "Routing 定義來源", sourceRef: "product_process", evidenceLabel: "Routing version evidence", statusLabel: "read-only" },
      { sourceTypeLabel: "流程步驟來源", sourceRef: "process_flow", evidenceLabel: "ordered step evidence", statusLabel: "read-only" },
      { sourceTypeLabel: "標準表現來源", sourceRef: "process_capacity", evidenceLabel: "standard performance reference", statusLabel: "read-only" }
    ],
    warnings: []
  },
  "WIP-SYRUP-001": {
    item: routingDashboardMock.items[1],
    versions: [{ version: 1, versionStateCode: "warning", versionStateLabel: "待確認", tone: "warning", effectiveDate: "2026/09/01", sourceLabel: "product_process" }],
    steps: [
      {
        stepNo: 10,
        processNo: "PROC-MIX-001",
        processLabel: "調拌",
        stageLabel: "前備",
        groupLabel: "糖漿前備",
        standardQuantity: 0,
        standardUnit: "公斤",
        standardMinutes: 0,
        standardRateLabel: "待確認",
        resourceEligibilityLabel: "未提供",
        sourceRef: "process_flow"
      }
    ],
    recipeReferences: [{ typeLabel: "Recipe reference", refNo: "RCP-260901", refName: "檸檬糖漿中間配方", statusLabel: "參照中", tone: "neutral" }],
    packagingContexts: [],
    resourceEligibility: [],
    standardPerformance: [],
    lineage: [
      { sourceTypeLabel: "Routing 定義來源", sourceRef: "product_process", evidenceLabel: "Routing version evidence", statusLabel: "read-only" },
      { sourceTypeLabel: "流程步驟來源", sourceRef: "process_flow", evidenceLabel: "ordered step evidence", statusLabel: "read-only" }
    ],
    warnings: [{ code: "missing_standard_performance", message: "標準表現尚未建立治理來源。", refNo: "PROC-MIX-001" }]
  }
};
