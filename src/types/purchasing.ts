import type { StatusTone } from "@/types/dashboard";

export type PurchasingWorkspaceTab = "purchase-orders" | "delivery-risk" | "receiving" | "suppliers";

export type PurchasingDataSource = "api" | "mock";

export type PurchasingSummary = {
  label: string;
  value: string;
  hint: string;
  tone: StatusTone;
};

export type PurchasingRange = {
  startDate: string;
  endDate: string;
  startTimestamp?: number;
  endTimestamp?: number;
};

export type PurchaseOrderItem = {
  id: string;
  purchaseOrderNo: string;
  purchaseDate: string;
  purchaseDateTimestamp?: number;
  itemNo: string;
  itemName: string;
  unit: string;
  unitCode?: number;
  supplierNo: string;
  supplierName: string;
  orderedCount: number;
  receivedCount: number;
  openCount: number;
  unitPrice: number;
  purchaseAmount: number;
  expectedArrivalDate: string;
  expectedArrivalTimestamp?: number;
  purchaseRequestNo: string;
  purchaseRequestLinkStatusCode: string;
  purchaseRequestLinkStatus: string;
  sourceOrderNo: string;
  linkedWorkOrderNo: string;
  warehouseStatusCode: string;
  warehouseStatus: string;
  riskLevelCode: number;
  riskLevel: string;
  riskType: string;
  riskTypeLabel: string;
  tone: StatusTone;
};

export type PurchaseDeliveryRiskItem = PurchaseOrderItem & {
  shortageCount: number;
  shortageValue: number;
  impactSourceType: string;
  impactSourceNo: string;
  impactSourceLabel: string;
  followUpCode: string;
  followUpLabel: string;
};

export type PurchaseReceiptItem = {
  id: string;
  no: string;
  purchaseOrderNo: string;
  date: string;
  dateTimestamp?: number;
  category: number;
  categoryLabel: string;
  itemNo: string;
  itemName: string;
  expectedCount: number;
  checkedCount: number;
  receivedCount: number;
  receivingStatusCode: string;
  receivingStatus: string;
  warehouseStatusCode: string;
  warehouseStatus: string;
  nextOwnerDepartment?: number;
  nextOwnerDepartmentLabel: string;
};

export type PurchaseSupplierItem = {
  id: string;
  supplierNo: string;
  supplierName: string;
  purchaseOrderCount: number;
  openPurchaseOrderCount: number;
  latePurchaseOrderCount: number;
  purchaseAmount: number;
  pendingReceiptCount: number;
  riskLevelCode: number;
  riskLevel: string;
  tone: StatusTone;
};

export type PurchaseReceiptDetail = {
  no: string;
  date: string;
  categoryLabel: string;
  expectedCount: number;
  checkedCount: number;
  receivedCount: number;
  receivingStatus: string;
  warehouseStatus: string;
};

export type PurchaseWorkflowStep = {
  taskId: string;
  taskTypeLabel: string;
  refNo: string;
  taskStatusLabel: string;
  ownerDepartmentLabel: string;
  tone: StatusTone;
};

export type PurchaseOrderDetail = {
  purchaseOrderNo: string;
  purchaseDate: string;
  itemNo: string;
  itemName: string;
  unit: string;
  supplierName: string;
  orderedCount: number;
  unitPrice: number;
  purchaseAmount: number;
  expectedArrivalDate: string;
  comment: string;
  purchaseRequestNo: string;
  sourceOrderNo: string;
  linkedWorkOrderNo: string;
  inventory: {
    currentCount: number;
    reservedCount: number;
    availableCount: number;
  };
  receipts: PurchaseReceiptDetail[];
  workflow: PurchaseWorkflowStep[];
  relatedDocuments: {
    quoteNo: string;
    contractNo: string;
  };
};

export type PurchasingDashboardData = {
  range: PurchasingRange;
  summary: PurchasingSummary[];
  purchaseOrders: PurchaseOrderItem[];
  deliveryRisks: PurchaseDeliveryRiskItem[];
  receipts: PurchaseReceiptItem[];
  suppliers: PurchaseSupplierItem[];
  total: {
    purchaseOrders: number;
    deliveryRisks: number;
    receipts: number;
    suppliers: number;
  };
};
