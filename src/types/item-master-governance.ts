export type ItemMasterPrimaryCategory = "RAW" | "MATERIAL" | "FILM" | "WIP" | "FG";

export type ItemMasterLifecycleStatus =
  | "DRAFT"
  | "ACTIVE"
  | "BLOCKED"
  | "INACTIVE"
  | "SUPERSEDED"
  | "RETIRED";

export type ItemMasterOwnershipContext = "COMPANY_PURCHASED" | "CUSTOMER_SUPPLIED" | "BOTH";

export type ItemMasterConversionMode = "FIXED" | "CATCH_WEIGHT";

export type ItemMasterLifecycleAction =
  | "ACTIVATE"
  | "BLOCK"
  | "INACTIVATE"
  | "SUPERSEDE"
  | "RETIRE";

export type ItemMasterRevision = {
  id: string;
  revisionNo: number;
  specificationLineageId?: string;
  specificationCode?: string;
  specificationName?: string;
  specificationHash?: string;
  summary: string;
  reference: string;
  effectiveFrom: string;
  effectiveTo: string;
  status: "DRAFT" | "ACTIVE" | "SUPERSEDED";
};

export type ItemMasterConversionRevision = {
  id: string;
  fromUomCode: string;
  toUomCode: string;
  conversionMode: ItemMasterConversionMode;
  factor: string;
  decimalScale: number;
  roundingMode: string;
  effectiveFrom: string;
  effectiveTo: string;
  status: "DRAFT" | "ACTIVE" | "SUPERSEDED";
};

export type ItemMasterAuditEvent = {
  id: string;
  eventType: string;
  label: string;
  actor: string;
  approver: string;
  reason: string;
  occurredAt: string;
  beforeValue: string;
  afterValue: string;
  evidenceReference: string;
};

export type ItemMasterGovernanceData = {
  itemId: string;
  itemCode: string;
  displayName: string;
  primaryCategory: ItemMasterPrimaryCategory;
  ownershipContext: ItemMasterOwnershipContext;
  baseUomCode: string;
  description: string;
  specificationSummary: string;
  specificationReference: string;
  lifecycleStatus: ItemMasterLifecycleStatus;
  rowVersion: number;
  baseUomLocked: boolean;
  catchWeightAuthorized: boolean;
  successorRelationshipId: string;
  specificationRevisions: ItemMasterRevision[];
  conversionRevisions: ItemMasterConversionRevision[];
  auditHistory: ItemMasterAuditEvent[];
};

export type ItemMasterDraft = {
  displayName: string;
  primaryCategory: ItemMasterPrimaryCategory | "";
  ownershipContext: ItemMasterOwnershipContext | "";
  baseUomCode: string;
  description: string;
  specificationSummary: string;
  specificationReference: string;
  specificationLineageId: string;
  specificationRevisionNo: string;
  specificationCode: string;
  specificationName: string;
  specificationHash: string;
  specificationEffectiveFrom: string;
  specificationEffectiveTo: string;
  conversionFromUomCode: string;
  conversionToUomCode: string;
  conversionMode: ItemMasterConversionMode;
  conversionFactor: string;
  conversionDecimalScale: string;
  conversionRoundingMode: string;
  conversionEffectiveFrom: string;
  conversionEffectiveTo: string;
};

export type ItemMasterFieldError = {
  field: string;
  message: string;
};

export type ItemMasterCreateRequest = {
  idempotency_key: string;
  display_name: string;
  primary_category: ItemMasterPrimaryCategory;
  ownership_context: ItemMasterOwnershipContext;
  base_uom_code: string;
  description?: string;
  specification_summary?: string;
  specification_reference?: string;
};

export type ItemMasterNameUpdateRequest = {
  request_id: string;
  display_name: string;
  reason: string;
  expected_row_version: number;
};

export type ItemMasterCategoryUpdateRequest = {
  request_id: string;
  primary_category: ItemMasterPrimaryCategory;
  reason: string;
  expected_row_version: number;
};

export type ItemMasterLifecycleRequest = {
  request_id: string;
  idempotency_key: string;
  to_status: Exclude<ItemMasterLifecycleStatus, "DRAFT">;
  reason: string;
  business_actor_type: string;
  business_actor_ref: string;
  accountable_approval_role: string;
  delegated_authorization_ref?: string;
  decision_evidence_ref: string;
  effective_at: string;
  expected_row_version: number;
  successor_relationship_id?: string;
  reentry_review_evidence_ref?: string;
};

export const ITEM_MASTER_CATEGORIES: ItemMasterPrimaryCategory[] = ["RAW", "MATERIAL", "FILM", "WIP", "FG"];

export const ITEM_MASTER_LIFECYCLE_ACTIONS: Record<
  ItemMasterLifecycleStatus,
  ItemMasterLifecycleAction[]
> = {
  DRAFT: ["ACTIVATE", "BLOCK", "INACTIVATE"],
  ACTIVE: ["BLOCK", "INACTIVATE", "SUPERSEDE", "RETIRE"],
  BLOCKED: ["ACTIVATE"],
  INACTIVE: ["ACTIVATE"],
  SUPERSEDED: ["RETIRE"],
  RETIRED: []
};
