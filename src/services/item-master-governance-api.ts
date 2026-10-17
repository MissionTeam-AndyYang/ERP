import type { DataSourceMode } from "@/components/common/data-source-toggle";
import { apiGet, apiPatch, apiPost, ApiClientError } from "@/services/api-client";
import type {
  ItemMasterCategoryUpdateRequest,
  ItemMasterCreateRequest,
  ItemMasterGovernanceData,
  ItemMasterLifecycleRequest,
  ItemMasterNameUpdateRequest,
  ItemMasterPrimaryCategory,
  ItemMasterOwnershipContext
} from "@/types/item-master-governance";

type ApiGovernancePayload = {
  item?: Record<string, unknown>;
  [key: string]: unknown;
};

export type ItemMasterGovernanceResult = {
  data?: ItemMasterGovernanceData;
  source: DataSourceMode;
  error?: string;
  status?: number;
  fieldErrors?: Record<string, string>;
};

const asString = (value: unknown, fallback = "") => (typeof value === "string" ? value : fallback);
const asNumber = (value: unknown, fallback = 0) => (typeof value === "number" && Number.isFinite(value) ? value : fallback);
const asBoolean = (value: unknown, fallback = false) => (typeof value === "boolean" ? value : fallback);

function normalizeCategory(value: unknown): ItemMasterPrimaryCategory {
  return ["RAW", "MATERIAL", "FILM", "WIP", "FG"].includes(String(value))
    ? (String(value) as ItemMasterPrimaryCategory)
    : "RAW";
}

function normalizeOwnershipContext(value: unknown): ItemMasterOwnershipContext {
  return ["COMPANY_PURCHASED", "CUSTOMER_SUPPLIED", "BOTH"].includes(String(value))
    ? (String(value) as ItemMasterOwnershipContext)
    : "COMPANY_PURCHASED";
}

function mockGovernance(itemId: string): ItemMasterGovernanceData {
  return {
    itemId,
    itemCode: itemId,
    displayName: "",
    primaryCategory: "RAW",
    ownershipContext: "COMPANY_PURCHASED",
    baseUomCode: "",
    description: "",
    specificationSummary: "",
    specificationReference: "",
    lifecycleStatus: "DRAFT",
    rowVersion: 0,
    baseUomLocked: false,
    catchWeightAuthorized: false,
    successorItemId: "",
    specificationRevisions: [],
    conversionRevisions: [],
    auditHistory: []
  };
}

function mapGovernancePayload(payload: ApiGovernancePayload, fallbackItemId: string): ItemMasterGovernanceData {
  const item = payload.item ?? payload;
  const specifications = Array.isArray(payload.specificationRevisions)
    ? payload.specificationRevisions
    : Array.isArray(item.specificationRevisions)
      ? item.specificationRevisions
      : [];
  const conversions = Array.isArray(payload.conversionRevisions)
    ? payload.conversionRevisions
    : Array.isArray(item.conversionRevisions)
      ? item.conversionRevisions
      : [];
  const auditHistory = Array.isArray(payload.auditHistory)
    ? payload.auditHistory
    : Array.isArray(item.auditHistory)
      ? item.auditHistory
      : [];

  return {
    itemId: asString(item.itemId ?? item.item_id, fallbackItemId),
    itemCode: asString(item.itemCode ?? item.item_code, fallbackItemId),
    displayName: asString(item.displayName ?? item.display_name),
    primaryCategory: normalizeCategory(item.primaryCategory ?? item.primary_category),
    ownershipContext: normalizeOwnershipContext(item.ownershipContext ?? item.ownership_context),
    baseUomCode: asString(item.baseUomCode ?? item.base_uom_code),
    description: asString(item.description),
    specificationSummary: asString(item.specificationSummary ?? item.specification_summary),
    specificationReference: asString(item.specificationReference ?? item.specification_reference),
    lifecycleStatus: normalizeLifecycleStatus(item.lifecycleStatus ?? item.lifecycle_status),
    rowVersion: asNumber(item.rowVersion ?? item.row_version),
    baseUomLocked: asBoolean(item.baseUomLocked ?? item.base_uom_locked),
    catchWeightAuthorized: asBoolean(item.catchWeightAuthorized ?? item.catch_weight_authorized),
    successorItemId: asString(item.successorItemId ?? item.successor_item_id),
    specificationRevisions: specifications.map(mapSpecificationRevision),
    conversionRevisions: conversions.map(mapConversionRevision),
    auditHistory: auditHistory.map(mapAuditEvent)
  };
}

function normalizeLifecycleStatus(value: unknown): ItemMasterGovernanceData["lifecycleStatus"] {
  return ["DRAFT", "ACTIVE", "BLOCKED", "INACTIVE", "SUPERSEDED", "RETIRED"].includes(String(value))
    ? (String(value) as ItemMasterGovernanceData["lifecycleStatus"])
    : "DRAFT";
}

function mapSpecificationRevision(value: unknown, index: number) {
  const row = (value ?? {}) as Record<string, unknown>;
  return {
    id: asString(row.id ?? row.specification_id, `spec-${index}`),
    revisionNo: asNumber(row.revisionNo ?? row.revision_no, index + 1),
    summary: asString(row.summary ?? row.specification_summary),
    reference: asString(row.reference ?? row.specification_reference),
    effectiveFrom: asString(row.effectiveFrom ?? row.effective_from),
    effectiveTo: asString(row.effectiveTo ?? row.effective_to),
    status: normalizeRevisionStatus(row.status ?? row.revision_status)
  };
}

function mapConversionRevision(value: unknown, index: number) {
  const row = (value ?? {}) as Record<string, unknown>;
  const mode = String(row.conversionMode ?? row.conversion_mode) === "CATCH_WEIGHT" ? "CATCH_WEIGHT" : "FIXED";
  return {
    id: asString(row.id ?? row.conversion_id, `conversion-${index}`),
    fromUomCode: asString(row.fromUomCode ?? row.from_uom_code),
    toUomCode: asString(row.toUomCode ?? row.to_uom_code),
    conversionMode: mode as "FIXED" | "CATCH_WEIGHT",
    factor: asString(row.factor ?? row.factor_numerator),
    decimalScale: asNumber(row.decimalScale ?? row.decimal_scale),
    roundingMode: asString(row.roundingMode ?? row.rounding_mode),
    effectiveFrom: asString(row.effectiveFrom ?? row.effective_from),
    effectiveTo: asString(row.effectiveTo ?? row.effective_to),
    status: normalizeRevisionStatus(row.status)
  };
}

function normalizeRevisionStatus(value: unknown): "DRAFT" | "ACTIVE" | "SUPERSEDED" {
  return value === "ACTIVE" || value === "SUPERSEDED" ? value : "DRAFT";
}

function mapAuditEvent(value: unknown, index: number) {
  const row = (value ?? {}) as Record<string, unknown>;
  return {
    id: asString(row.id ?? row.event_id, `audit-${index}`),
    eventType: asString(row.eventType ?? row.event_type),
    label: asString(row.label ?? row.event_label),
    actor: asString(row.actor ?? row.business_actor_ref),
    approver: asString(row.approver ?? row.approver_ref),
    reason: asString(row.reason),
    occurredAt: asString(row.occurredAt ?? row.occurred_at),
    beforeValue: asString(row.beforeValue ?? row.before_value),
    afterValue: asString(row.afterValue ?? row.after_value),
    evidenceReference: asString(row.evidenceReference ?? row.evidence_reference)
  };
}

function mutationError(error: unknown): ItemMasterGovernanceResult {
  return {
    source: "api",
    error: error instanceof ApiClientError || error instanceof Error ? error.message : "Item Master API 操作失敗",
    status: error instanceof ApiClientError ? error.status : undefined,
    fieldErrors: error instanceof ApiClientError ? error.fieldErrors : undefined
  };
}

export async function getItemMasterGovernance(
  itemId: string,
  dataSourceMode: DataSourceMode
): Promise<ItemMasterGovernanceResult> {
  if (dataSourceMode === "mock") {
    return { source: "mock", data: mockGovernance(itemId) };
  }

  try {
    const payload = await apiGet<ApiGovernancePayload>(`/api/v1/items/${encodeURIComponent(itemId)}`);
    return { source: "api", data: mapGovernancePayload(payload, itemId) };
  } catch (error) {
    return mutationError(error);
  }
}

export async function createItemMaster(
  request: ItemMasterCreateRequest,
  dataSourceMode: DataSourceMode
): Promise<ItemMasterGovernanceResult> {
  if (dataSourceMode === "mock") {
    return { source: "mock", error: "示範資料模式不會寫入後端資料。" };
  }

  try {
    const payload = await apiPost<ApiGovernancePayload>("/api/v1/items", request);
    return { source: "api", data: mapGovernancePayload(payload, "") };
  } catch (error) {
    return mutationError(error);
  }
}

export async function updateItemName(
  itemId: string,
  request: ItemMasterNameUpdateRequest,
  dataSourceMode: DataSourceMode
): Promise<ItemMasterGovernanceResult> {
  return mutateItem(`/api/v1/items/${encodeURIComponent(itemId)}/name`, request, dataSourceMode, itemId);
}

export async function updateItemCategory(
  itemId: string,
  request: ItemMasterCategoryUpdateRequest,
  dataSourceMode: DataSourceMode
): Promise<ItemMasterGovernanceResult> {
  return mutateItem(`/api/v1/items/${encodeURIComponent(itemId)}/category`, request, dataSourceMode, itemId);
}

export async function createSpecificationRevision(
  itemId: string,
  request: Record<string, unknown>,
  dataSourceMode: DataSourceMode
): Promise<ItemMasterGovernanceResult> {
  return mutateItem(`/api/v1/items/${encodeURIComponent(itemId)}/specifications`, request, dataSourceMode, itemId, "POST");
}

export async function createConversionRevision(
  itemId: string,
  request: Record<string, unknown>,
  dataSourceMode: DataSourceMode
): Promise<ItemMasterGovernanceResult> {
  return mutateItem(`/api/v1/items/${encodeURIComponent(itemId)}/uom-conversions`, request, dataSourceMode, itemId, "POST");
}

export async function submitItemLifecycleAction(
  itemId: string,
  request: ItemMasterLifecycleRequest,
  dataSourceMode: DataSourceMode
): Promise<ItemMasterGovernanceResult> {
  return mutateItem(`/api/v1/items/${encodeURIComponent(itemId)}/lifecycle-actions`, request, dataSourceMode, itemId, "POST");
}

async function mutateItem(
  path: string,
  request: unknown,
  dataSourceMode: DataSourceMode,
  fallbackItemId: string,
  method: "PATCH" | "POST" = "PATCH"
): Promise<ItemMasterGovernanceResult> {
  if (dataSourceMode === "mock") {
    return { source: "mock", error: "示範資料模式不會寫入後端資料。" };
  }

  try {
    const payload = method === "POST"
      ? await apiPost<ApiGovernancePayload>(path, request)
      : await apiPatch<ApiGovernancePayload>(path, request);
    return { source: "api", data: mapGovernancePayload(payload, fallbackItemId) };
  } catch (error) {
    return mutationError(error);
  }
}
