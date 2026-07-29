import type {
  PurchaseOrderDetail,
  PurchaseOrderItem,
  PurchasingDashboardData,
  PurchasingSummary
} from "@/types/purchasing";

export const purchasingSummary: PurchasingSummary[] = [
  {
    label: "未收採購單",
    value: "12",
    hint: "到期或逾期 3 筆",
    tone: "warning"
  },
  {
    label: "交期風險",
    value: "2 / 4",
    hint: "逾期 2 筆，影響工單 2 筆",
    tone: "danger"
  },
  {
    label: "採購金額",
    value: "$3,642,000",
    hint: "查詢期間進貨單 18 筆",
    tone: "info"
  },
  {
    label: "未連請購",
    value: "5",
    hint: "待入庫交接 6 筆",
    tone: "warning"
  }
];

export const purchaseOrders: PurchaseOrderItem[] = [
  {
    id: "PO-20260724-031",
    purchaseOrderNo: "PO-20260724-031",
    purchaseDate: "2026/7/24",
    purchaseDateTimestamp: 1784822400,
    itemNo: "RM-CORN-001",
    itemName: "冷凍玉米粒",
    unit: "公斤",
    unitCode: 2,
    supplierNo: "SUP-GREEN-01",
    supplierName: "綠田食品",
    orderedCount: 1200,
    receivedCount: 600,
    openCount: 600,
    unitPrice: 72,
    purchaseAmount: 86400,
    expectedArrivalDate: "2026/7/28",
    expectedArrivalTimestamp: 1785168000,
    purchaseRequestNo: "PR-20260723-018",
    purchaseRequestLinkStatusCode: "linked",
    purchaseRequestLinkStatus: "已連請購",
    sourceOrderNo: "SO-20260723-022",
    linkedWorkOrderNo: "WO-20260728-002",
    warehouseStatusCode: "pending_putaway",
    warehouseStatus: "待入庫交接",
    riskLevelCode: 3,
    riskLevel: "高風險",
    riskType: "late_arrival",
    riskTypeLabel: "逾期未到",
    tone: "danger"
  },
  {
    id: "PO-20260725-014",
    purchaseOrderNo: "PO-20260725-014",
    purchaseDate: "2026/7/25",
    purchaseDateTimestamp: 1784908800,
    itemNo: "PK-BAG-010",
    itemName: "耐熱殺菌袋",
    unit: "個",
    unitCode: 101,
    supplierNo: "SUP-PACK-02",
    supplierName: "台灣包材",
    orderedCount: 20000,
    receivedCount: 0,
    openCount: 20000,
    unitPrice: 6.6,
    purchaseAmount: 132000,
    expectedArrivalDate: "2026/7/30",
    expectedArrivalTimestamp: 1785340800,
    purchaseRequestNo: "",
    purchaseRequestLinkStatusCode: "unlinked",
    purchaseRequestLinkStatus: "未連請購",
    sourceOrderNo: "",
    linkedWorkOrderNo: "WO-20260731-006",
    warehouseStatusCode: "not_received",
    warehouseStatus: "尚未到貨",
    riskLevelCode: 1,
    riskLevel: "注意",
    riskType: "purchase_request_unlinked",
    riskTypeLabel: "缺少請購關聯",
    tone: "warning"
  },
  {
    id: "PO-20260726-027",
    purchaseOrderNo: "PO-20260726-027",
    purchaseDate: "2026/7/26",
    purchaseDateTimestamp: 1784995200,
    itemNo: "RM-CHICKEN-022",
    itemName: "雞胸肉原料",
    unit: "公斤",
    unitCode: 2,
    supplierNo: "SUP-POULTRY-03",
    supplierName: "安心禽品",
    orderedCount: 1600,
    receivedCount: 1600,
    openCount: 0,
    unitPrice: 110,
    purchaseAmount: 176000,
    expectedArrivalDate: "2026/7/29",
    expectedArrivalTimestamp: 1785254400,
    purchaseRequestNo: "PR-20260725-006",
    purchaseRequestLinkStatusCode: "linked",
    purchaseRequestLinkStatus: "已連請購",
    sourceOrderNo: "SO-20260726-018",
    linkedWorkOrderNo: "WO-20260729-001",
    warehouseStatusCode: "stocked",
    warehouseStatus: "已入庫",
    riskLevelCode: 0,
    riskLevel: "正常",
    riskType: "normal",
    riskTypeLabel: "正常",
    tone: "success"
  }
];

export const purchasingDashboardMock: PurchasingDashboardData & { details: Record<string, PurchaseOrderDetail> } = {
  range: {
    startDate: "2026-07-01",
    endDate: "2026-07-29",
    startTimestamp: 1782835200,
    endTimestamp: 1785340799
  },
  summary: purchasingSummary,
  purchaseOrders,
  deliveryRisks: [
    {
      ...purchaseOrders[0],
      shortageCount: 600,
      shortageValue: 43200,
      impactSourceType: "work_order",
      impactSourceNo: "WO-20260728-002",
      impactSourceLabel: "生產工單",
      followUpCode: "confirm_supplier_date",
      followUpLabel: "確認供應商交期"
    },
    {
      ...purchaseOrders[1],
      shortageCount: 20000,
      shortageValue: 132000,
      impactSourceType: "safety_stock",
      impactSourceNo: "PK-BAG-010",
      impactSourceLabel: "安全水位",
      followUpCode: "review_source_impact",
      followUpLabel: "檢視來源影響"
    }
  ],
  receipts: [
    {
      id: "GRN-20260728-018",
      no: "GRN-20260728-018",
      purchaseOrderNo: "PO-20260724-031",
      date: "2026/7/28",
      dateTimestamp: 1785168000,
      category: 0,
      categoryLabel: "進貨",
      itemNo: "RM-CORN-001",
      itemName: "冷凍玉米粒",
      expectedCount: 600,
      checkedCount: 600,
      receivedCount: 600,
      receivingStatusCode: "received",
      receivingStatus: "已收貨",
      warehouseStatusCode: "pending_putaway",
      warehouseStatus: "待入庫交接",
      nextOwnerDepartment: 4,
      nextOwnerDepartmentLabel: "倉庫"
    },
    {
      id: "GRN-20260729-021",
      no: "GRN-20260729-021",
      purchaseOrderNo: "PO-20260726-027",
      date: "2026/7/29",
      dateTimestamp: 1785254400,
      category: 0,
      categoryLabel: "進貨",
      itemNo: "RM-CHICKEN-022",
      itemName: "雞胸肉原料",
      expectedCount: 1600,
      checkedCount: 1600,
      receivedCount: 1600,
      receivingStatusCode: "received",
      receivingStatus: "已收貨",
      warehouseStatusCode: "stocked",
      warehouseStatus: "已入庫",
      nextOwnerDepartment: 0,
      nextOwnerDepartmentLabel: "未指定"
    }
  ],
  suppliers: [
    {
      id: "SUP-GREEN-01",
      supplierNo: "SUP-GREEN-01",
      supplierName: "綠田食品",
      purchaseOrderCount: 7,
      openPurchaseOrderCount: 3,
      latePurchaseOrderCount: 1,
      purchaseAmount: 942000,
      pendingReceiptCount: 1800,
      riskLevelCode: 3,
      riskLevel: "高風險",
      tone: "danger"
    },
    {
      id: "SUP-PACK-02",
      supplierNo: "SUP-PACK-02",
      supplierName: "台灣包材",
      purchaseOrderCount: 5,
      openPurchaseOrderCount: 4,
      latePurchaseOrderCount: 0,
      purchaseAmount: 626000,
      pendingReceiptCount: 28000,
      riskLevelCode: 1,
      riskLevel: "注意",
      tone: "warning"
    }
  ],
  total: {
    purchaseOrders: 3,
    deliveryRisks: 2,
    receipts: 2,
    suppliers: 2
  },
  details: {
    "PO-20260724-031": {
      purchaseOrderNo: "PO-20260724-031",
      purchaseDate: "2026/7/24",
      itemNo: "RM-CORN-001",
      itemName: "冷凍玉米粒",
      unit: "公斤",
      supplierName: "綠田食品",
      orderedCount: 1200,
      unitPrice: 72,
      purchaseAmount: 86400,
      expectedArrivalDate: "2026/7/28",
      comment: "分批到貨，第二批需供應商確認車次。",
      purchaseRequestNo: "PR-20260723-018",
      sourceOrderNo: "SO-20260723-022",
      linkedWorkOrderNo: "WO-20260728-002",
      inventory: { currentCount: 600, reservedCount: 420, availableCount: 180 },
      receipts: [
        {
          no: "GRN-20260728-018",
          date: "2026/7/28",
          categoryLabel: "進貨",
          expectedCount: 600,
          checkedCount: 600,
          receivedCount: 600,
          receivingStatus: "已收貨",
          warehouseStatus: "待入庫交接"
        }
      ],
      workflow: [
        {
          taskId: "WF-PO-001",
          taskTypeLabel: "採購",
          refNo: "PO-20260724-031",
          taskStatusLabel: "已完成",
          ownerDepartmentLabel: "採購",
          tone: "success"
        },
        {
          taskId: "WF-GRN-018",
          taskTypeLabel: "入庫",
          refNo: "GRN-20260728-018",
          taskStatusLabel: "待處理",
          ownerDepartmentLabel: "倉庫",
          tone: "warning"
        }
      ],
      relatedDocuments: { quoteNo: "QT-20260718-004", contractNo: "CT-20260701-009" }
    }
  }
};
