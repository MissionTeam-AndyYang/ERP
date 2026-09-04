import type { StatusTone } from "@/types/dashboard";

export type PackagingDataSource = "api" | "mock";
export type PackagingIdentityType = "product" | "wip";
export type PackagingStatusCode = "complete" | "partial" | "unavailable" | "error";

export type PackagingQuery = {
  itemNo: string;
  itemCategory: 4 | 5;
  productVersion?: number;
  effectiveDate?: number;
};

export type PackagingSubject = {
  itemNo: string;
  itemName: string;
  itemCategory: number;
  itemCategoryLabel: string;
  itemSubCategory: number;
  productVersion: number;
  versionLabel: string;
  unitShippingLabel: string;
  unitWarehouseLabel: string;
  unitProductLabel: string;
  comment: string;
  sourceLabel: string;
  tone: StatusTone;
};

export type PackagingSummary = {
  packagingSpecCount: number;
  packagingBomCount: number;
  packageLevelCount: number;
  materialLineCount: number;
  totalCount: number;
  totalWeight: number;
};

export type PackagingSpecLine = {
  parentBomNo: string;
  parentBomName: string;
  childCategory: number;
  childCategoryLabel: string;
  childNo: string;
  childName: string;
  childUnitLabel: string;
  count: number;
  childUnit2Label: string;
  weight: number;
  length: number;
  expectedLoss: number;
  actualLoss: number;
  processCount: number;
  comment: string;
};

export type PackagingSpec = {
  specId: string;
  productNo: string;
  productVersion: number;
  wipNo: string;
  packagingLevel: number;
  packagingLevelLabel: string;
  packagingBomNo: string;
  packagingBomName: string;
  count: number;
  unitLabel: string;
  weight: number;
  masterUnitLabel: string;
  masterWeight: number;
  linkedBomNo: string;
  linkedBomVersion: number;
  lineCount: number;
  lines: PackagingSpecLine[];
  sourceLabel: string;
  masterSourceLabel: string;
  lineSourceLabel: string;
  tone: StatusTone;
};

export type PackagingLineage = {
  sourceTypeLabel: string;
  sourceLabel: string;
  tone: StatusTone;
};

export type PackagingModuleReadiness = {
  moduleCode: string;
  moduleLabel: string;
  statusCode: PackagingStatusCode;
  statusLabel: string;
  sourceLabel: string;
  warningCodes: string[];
  tone: StatusTone;
};

export type PackagingWarning = {
  moduleLabel: string;
  code: string;
  message: string;
  refNo: string;
  tone: StatusTone;
};

export type PackagingCapabilityBoundary = {
  readOnly: boolean;
  packagingWriteSupported: boolean;
  packagingApprovalSupported: boolean;
  packagingReleaseSupported: boolean;
  sourceOfTruthTransitionSupported: boolean;
  cutoverSupported: boolean;
  goLiveSupported: boolean;
};

export type PackagingOverviewData = {
  serverTimestamp?: number;
  timezone: string;
  requestIdentity: PackagingQuery;
  subject?: PackagingSubject;
  summary: PackagingSummary;
  packagingSpecs: PackagingSpec[];
  sourceLineage: PackagingLineage[];
  moduleReadiness: PackagingModuleReadiness[];
  warnings: PackagingWarning[];
  capabilityBoundary: PackagingCapabilityBoundary;
};
