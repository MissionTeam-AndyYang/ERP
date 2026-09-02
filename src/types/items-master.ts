import type { StatusTone } from "@/types/dashboard";

export type ItemsMasterDataSource = "api" | "mock";

export type ItemMasterSummary = {
  totalItemCount: number;
  activeItemCount: number;
  finishedGoodsCount: number;
  maintenanceItemCount: number;
  companyCount: number;
  transItemCount: number;
  linkedItemCount: number;
  contractLinkedTransItemCount: number;
  companyDataQualityIssueCount: number;
  transItemDataQualityIssueCount: number;
};

export type ItemCategorySummary = {
  itemCategory: number;
  itemCategoryLabel: string;
  itemCount: number;
  stockItemCount: number;
  bomLinkedItemCount: number;
  maintenanceItemCount: number;
};

export type MaterialItemMasterRow = {
  id: string;
  itemNo: string;
  itemName: string;
  itemCategory: number;
  itemCategoryLabel: string;
  itemSubCategory: number;
  unitWarehouse: number;
  unitWarehouseLabel: string;
  unitProduct: number;
  unitProductLabel: string;
  masterStatusCode: string;
  masterStatusLabel: string;
  maintenanceRiskCode: string;
  maintenanceRiskLabel: string;
  hasStock: boolean;
  currentQuantity: number;
  batchCount: number;
  bomCount: number;
  tone: StatusTone;
};

export type MaintenanceSuggestionRow = {
  suggestionId: string;
  itemNo: string;
  suggestionTypeCode: string;
  suggestionTypeLabel: string;
  riskLevelCode: string;
  riskLevelLabel: string;
  tone: StatusTone;
};

export type PaymentSummary = {
  paymentTypeCode: string;
  paymentTypeLabel: string;
  paymentDate: number;
  paymentPeriod: number;
  paymentSource: number;
  paymentSourceLabel: string;
};

export type CompanyMasterRow = {
  id: string;
  companyNo: string;
  companyDisplayName: string;
  companyName: string;
  businessNo: string;
  transItemCount: number;
  contractCount: number;
  contactName: string;
  contactPhone: string;
  receivablePayment: PaymentSummary;
  payablePayment: PaymentSummary;
  dataQualityCode: string;
  dataQualityLabel: string;
  tone: StatusTone;
};

export type TransactionItemMasterRow = {
  id: string;
  transItemNo: string;
  transItemName: string;
  transItemType: string;
  transItemTypeLabel: string;
  transItemCategory: number;
  transItemCategoryLabel: string;
  transItemAttribute: number;
  companyNo: string;
  companyDisplayName: string;
  itemNo: string;
  itemName: string;
  itemCategory: number;
  itemCategoryLabel: string;
  contractNo: string;
  contractCategory: number;
  contractCategoryLabel: string;
  contractType: number;
  tradeUnit: number;
  tradeUnitLabel: string;
  tradePrice: number;
  shippingPrice: number;
  unitConversion: number;
  dataQualityCode: string;
  dataQualityLabel: string;
  tone: StatusTone;
};

export type ItemAndTransactionMasterData = {
  summary: ItemMasterSummary;
  categorySummary: ItemCategorySummary[];
  items: MaterialItemMasterRow[];
  maintenanceSuggestions: MaintenanceSuggestionRow[];
  companies: CompanyMasterRow[];
  transactionItems: TransactionItemMasterRow[];
  totalItems: number;
  totalTransactionItems: number;
  start: number;
  count: number;
};
