import type { StatusTone } from "@/types/dashboard";

export type ManufacturingDefinitionDataSource = "api" | "mock";
export type ManufacturingDefinitionIdentityType = "product" | "wip" | "unknown";
export type ManufacturingResolutionStatus =
  | "RESOLVED_SINGLE_CANDIDATE"
  | "RESOLVED_WITH_WARNINGS"
  | "MULTIPLE_CANDIDATES"
  | "PARTIAL_CANDIDATE"
  | "UNAVAILABLE"
  | "CONFLICT";
export type ManufacturingDefinitionStatus = "candidate" | "partial" | "unavailable";

export type ManufacturingDefinitionQuery = {
  itemNo: string;
  itemCategory: 4 | 5;
  asOfDate?: number;
  bomVersion?: number;
  recipeVersion?: number;
  routingVersion?: number;
  packagingVersion?: number;
};

export type ManufacturingDefinitionSubject = {
  itemNo: string;
  itemName: string;
  itemCategory: number;
  itemCategoryLabel: string;
  identityType: ManufacturingDefinitionIdentityType;
  identityTypeLabel: string;
  versionLabel: string;
  unitWarehouseLabel: string;
  unitProductLabel: string;
  masterStatusLabel: string;
  sourceLabel: string;
  tone: StatusTone;
};

export type ManufacturingVersionReference = {
  domainCode: string;
  domainLabel: string;
  referenceNo: string;
  versionLabel: string;
  statusCode: string;
  statusLabel: string;
  dateLabel: string;
  detailLabel: string;
  tone: StatusTone;
};

export type ManufacturingDomainReference = {
  domainCode: string;
  domainLabel: string;
  statusCode: string;
  statusLabel: string;
  sourceLabel: string;
  warningCodes: string[];
  versions: ManufacturingVersionReference[];
  detailLabel: string;
  tone: StatusTone;
};

export type ManufacturingAuthority = {
  domainCode: string;
  domainLabel: string;
  valueTypeCode: string;
  valueTypeLabel: string;
  value: number;
  unitLabel: string;
  sourceLabel: string;
  sourceRef: string;
  authorityCaveat: string;
  tone: StatusTone;
};

export type ManufacturingEffectivityRow = {
  domainCode: string;
  domainLabel: string;
  effectiveFromLabel: string;
  effectiveToLabel: string;
  currentActive: boolean | null;
  retiredInactive: boolean | null;
  statusCode: string;
  statusLabel: string;
  evidenceRef: string;
  conflictState: string;
  tone: StatusTone;
};

export type ManufacturingLineage = {
  domainCode: string;
  domainLabel: string;
  sourceCode: string;
  sourceLabel: string;
  sourceRef: string;
  sourceParticipant: string;
  acceptedEvidenceClass: string;
  acceptedEvidenceLabel: string;
  acceptanceState: string;
  authorityCaveat: string;
  tone: StatusTone;
};

export type ManufacturingWarning = {
  domainCode: string;
  domainLabel: string;
  code: string;
  message: string;
  refNo: string;
  tone: StatusTone;
};

export type ManufacturingFreezeCompatibility = {
  statusCode: string;
  statusLabel: string;
  resolutionStatus: ManufacturingResolutionStatus;
  previewOnly: boolean;
  freezeReady: boolean;
  approvalSupported: boolean;
  releaseSupported: boolean;
  freezeSupported: boolean;
  productionOrderFreezeImplemented: boolean;
  warningCount: number;
  tone: StatusTone;
};

export type ManufacturingCapabilityBoundary = {
  readOnly: boolean;
  manufacturingDefinitionWriteSupported: boolean;
  productWriteSupported: boolean;
  bomWriteSupported: boolean;
  recipeWriteSupported: boolean;
  routingWriteSupported: boolean;
  packagingWriteSupported: boolean;
  approvalSupported: boolean;
  releaseSupported: boolean;
  freezeSupported: boolean;
  sourceOfTruthTransitionSupported: boolean;
  cutoverSupported: boolean;
  goLiveSupported: boolean;
};

export type ManufacturingDefinitionData = {
  serverTimestamp?: number;
  timezone: string;
  requestIdentity: ManufacturingDefinitionQuery;
  subject?: ManufacturingDefinitionSubject;
  definitionStatus: ManufacturingDefinitionStatus;
  definitionId: string;
  candidateVersions: ManufacturingVersionReference[];
  domainReferences: ManufacturingDomainReference[];
  quantityAuthorities: ManufacturingAuthority[];
  weightAuthorities: ManufacturingAuthority[];
  effectivityAsOfDateLabel: string;
  effectivity: ManufacturingEffectivityRow[];
  resolutionStatus: ManufacturingResolutionStatus;
  resolutionStatusLabel: string;
  warnings: ManufacturingWarning[];
  sourceLineage: ManufacturingLineage[];
  freezeCompatibility: ManufacturingFreezeCompatibility;
  capabilityBoundary: ManufacturingCapabilityBoundary;
};
