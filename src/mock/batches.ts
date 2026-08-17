import type { BatchDashboardData, BatchDetail, BatchDistributionData } from "@/types/batches";

export const batchesDashboardMock: BatchDashboardData = {
  summary: {
    stockItemCount: 86,
    highRiskItemCount: 3,
    stockBatchCount: 42,
    qualityHoldQuantity: 1420,
    nearExpiryBatchCount: 5
  },
  kpis: [
    { label: "批號管理品項", value: "86", hint: "目前有庫存的批號品項", tone: "info" },
    { label: "高風險品項", value: "3", hint: "品檢保留、即期或流程阻塞", tone: "danger" },
    { label: "分倉批號", value: "42", hint: "跨倉庫或產製情境的批號列", tone: "warning" },
    { label: "品檢保留量", value: "1,420", hint: "需等待品保判定", tone: "neutral" }
  ],
  items: [
    {
      itemNo: "FG-CURRY-101",
      itemName: "咖哩雞肉調理包",
      itemCategory: 5,
      itemCategoryLabel: "製成品",
      itemSubCategory: 0,
      itemType: 1,
      itemTypeLabel: "新料",
      totalBatchCount: 4,
      warehouseCount: 3,
      currentQuantity: 18240,
      availableQuantity: 9600,
      reservedQuantity: 5760,
      qualityHoldQuantity: 2880,
      earliestValidDate: "2026/11/08",
      earliestValidTimestamp: 1794067200,
      qaHoldBatchCount: 1,
      nearExpiryBatchCount: 0,
      riskLevelCode: "high_risk",
      riskLevelLabel: "高風險",
      riskCode: "quality_hold",
      riskLabel: "品檢保留",
      ownerDepartment: 6,
      ownerDepartmentLabel: "品保",
      unitLabel: "盒",
      tone: "danger"
    },
    {
      itemNo: "RM-CORN-001",
      itemName: "冷凍玉米粒",
      itemCategory: 1,
      itemCategoryLabel: "原料",
      itemSubCategory: 0,
      itemType: 1,
      itemTypeLabel: "新料",
      totalBatchCount: 3,
      warehouseCount: 2,
      currentQuantity: 1260,
      availableQuantity: 720,
      reservedQuantity: 360,
      qualityHoldQuantity: 180,
      earliestValidDate: "2026/05/31",
      earliestValidTimestamp: 1780156800,
      qaHoldBatchCount: 1,
      nearExpiryBatchCount: 1,
      riskLevelCode: "high_risk",
      riskLevelLabel: "高風險",
      riskCode: "near_expiry",
      riskLabel: "即期",
      ownerDepartment: 7,
      ownerDepartmentLabel: "倉庫",
      unitLabel: "公斤",
      tone: "danger"
    },
    {
      itemNo: "PK-BAG-010",
      itemName: "耐熱殺菌袋 180g",
      itemCategory: 2,
      itemCategoryLabel: "物料",
      itemSubCategory: 0,
      itemType: 1,
      itemTypeLabel: "新料",
      totalBatchCount: 5,
      warehouseCount: 2,
      currentQuantity: 42000,
      availableQuantity: 33000,
      reservedQuantity: 9000,
      qualityHoldQuantity: 0,
      earliestValidDate: "2027/02/12",
      earliestValidTimestamp: 1802361600,
      qaHoldBatchCount: 0,
      nearExpiryBatchCount: 0,
      riskLevelCode: "attention",
      riskLevelLabel: "注意",
      riskCode: "reserved",
      riskLabel: "已預留",
      ownerDepartment: 4,
      ownerDepartmentLabel: "生管",
      unitLabel: "個",
      tone: "warning"
    }
  ],
  total: 3,
  start: 0,
  count: 3
};

export const batchDistributionMock: Record<string, BatchDistributionData> = {
  "FG-CURRY-101": {
    item: {
      itemNo: "FG-CURRY-101",
      itemName: "咖哩雞肉調理包",
      itemCategory: 5,
      itemCategoryLabel: "製成品",
      itemSubCategory: 0,
      itemType: 1,
      itemTypeLabel: "新料",
      unit: 109,
      unitLabel: "盒"
    },
    batches: [
      {
        rowKey: "B240512-A101|WH-FG-A|available",
        batchNo: "B240512-A101",
        warehouseNo: "WH-FG-A",
        warehouseName: "成品倉 A",
        locationCode: "A1-02-03",
        palletCount: 5,
        currentQuantity: 9600,
        availableQuantity: 9600,
        reservedQuantity: 0,
        qualityHoldQuantity: 0,
        unit: 109,
        unitLabel: "盒",
        validDate: "2026/11/08",
        validTimestamp: 1794067200,
        validDays: 180,
        qaStatusCode: "released",
        qaStatusLabel: "已放行",
        batchStageCode: "available",
        batchStageLabel: "可用",
        riskLevelCode: "normal",
        riskLevelLabel: "正常",
        riskCodes: ["normal"],
        riskLabels: ["正常"],
        refCategory: 2,
        refCategoryLabel: "生產",
        refNo: "MO-240512-001",
        relatedDocuments: [
          { refCategory: 2, refCategoryLabel: "生產", refNo: "MO-240512-001" }
        ],
        tone: "success"
      },
      {
        rowKey: "B240513-A102|WH-QA-HOLD|quality_hold",
        batchNo: "B240513-A102",
        warehouseNo: "WH-QA-HOLD",
        warehouseName: "品檢保留區",
        locationCode: "HOLD-01",
        palletCount: 2,
        currentQuantity: 2880,
        availableQuantity: 0,
        reservedQuantity: 2880,
        qualityHoldQuantity: 2880,
        unit: 109,
        unitLabel: "盒",
        validDate: "2026/11/09",
        validTimestamp: 1794153600,
        validDays: 180,
        qaStatusCode: "quality_hold",
        qaStatusLabel: "品檢保留",
        batchStageCode: "quality_hold",
        batchStageLabel: "品檢保留",
        riskLevelCode: "high_risk",
        riskLevelLabel: "高風險",
        riskCodes: ["quality_hold", "reserved"],
        riskLabels: ["品檢保留", "已預留"],
        refCategory: 2,
        refCategoryLabel: "生產",
        refNo: "MO-240513-003",
        relatedDocuments: [
          { refCategory: 2, refCategoryLabel: "生產", refNo: "MO-240513-003" },
          { refCategory: 3, refCategoryLabel: "銷售", refNo: "SO-240526-018" }
        ],
        tone: "danger"
      }
    ],
    total: 2,
    start: 0,
    count: 2
  }
};

export const batchDetailMock: Record<string, BatchDetail> = {
  "B240513-A102": {
    batch: {
      batchNo: "B240513-A102",
      itemNo: "FG-CURRY-101",
      itemName: "咖哩雞肉調理包",
      itemCategory: 5,
      itemCategoryLabel: "製成品",
      itemSubCategory: 0,
      itemType: 1,
      itemTypeLabel: "新料",
      unit: 109,
      unitLabel: "盒",
      validDate: "2026/11/09",
      validTimestamp: 1794153600,
      validDays: 180,
      refCategory: 2,
      refCategoryLabel: "生產",
      refNo: "MO-240513-003",
      creatorNo: "USR-QA-01",
      creationTime: "2026/05/13"
    },
    stockByWarehouse: [
      {
        warehouseNo: "WH-QA-HOLD",
        warehouseName: "品檢保留區",
        locationCode: "HOLD-01",
        palletCount: 2,
        currentQuantity: 2880,
        availableQuantity: 0,
        reservedQuantity: 2880,
        qualityHoldQuantity: 2880,
        unit: 109,
        unitLabel: "盒",
        riskLevelCode: "high_risk",
        riskLevelLabel: "高風險",
        riskCodes: ["quality_hold", "reserved"],
        riskLabels: ["品檢保留", "已預留"],
        tone: "danger"
      }
    ],
    inventoryRecords: [
      {
        recordTime: "2026/05/13",
        refCategory: 2,
        refCategoryLabel: "生產",
        refNo: "MO-240513-003",
        warehouseNo: "WH-QA-HOLD",
        category: 1,
        categoryLabel: "入庫",
        source: 2,
        sourceLabel: "生產",
        quantity: 2880,
        unit: 109,
        unitLabel: "盒",
        amount: 0
      }
    ],
    reservations: [
      {
        reservationNo: "RSV-240526-018",
        refCategory: 3,
        refCategoryLabel: "銷售",
        refNo: "SO-240526-018",
        warehouseNo: "WH-QA-HOLD",
        reservedQuantity: 2880,
        status: 1,
        statusLabel: "有效",
        expiryTimestamp: "2026/05/26"
      }
    ],
    qualityHolds: [
      {
        holdNo: "QH-240513-027",
        warehouseNo: "WH-QA-HOLD",
        holdQuantity: 2880,
        status: 1,
        statusLabel: "保留中",
        reasonCode: "inspection",
        reasonLabel: "檢驗中",
        createdTimestamp: "2026/05/13"
      }
    ],
    palletMovements: [
      {
        movementNo: "PM-240513-001",
        warehouseNo: "WH-QA-HOLD",
        palletNo: "P-HOLD-001",
        palletCount: 2,
        palletStatus: 1,
        palletStatusLabel: "在庫",
        movementTimestamp: "2026/05/13"
      }
    ],
    tasks: [
      {
        taskId: 240513027,
        taskType: 8,
        taskTypeLabel: "品檢",
        taskStatus: 1,
        taskStatusLabel: "待處理",
        nextOwnerDepartment: 6,
        nextOwnerDepartmentLabel: "品保",
        dueTimestamp: "2026/05/14",
        refCategory: 2,
        refCategoryLabel: "生產",
        refNo: "MO-240513-003",
        tone: "info"
      }
    ]
  }
};
