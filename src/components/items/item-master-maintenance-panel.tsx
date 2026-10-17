"use client";

import {
  AlertTriangle,
  CheckCircle2,
  FilePlus2,
  Loader2,
  LockKeyhole,
  Save,
  ShieldCheck,
  X
} from "lucide-react";
import { useEffect, useMemo, useState, type FormEvent } from "react";
import type { DataSourceMode } from "@/components/common/data-source-toggle";
import { StatusBadge } from "@/components/ui/status-badge";
import {
  createConversionRevision,
  createItemMaster,
  createSpecificationRevision,
  getItemMasterGovernance,
  submitItemLifecycleAction,
  updateItemCategory,
  updateItemName
} from "@/services/item-master-governance-api";
import type {
  ItemMasterDraft,
  ItemMasterGovernanceData,
  ItemMasterLifecycleAction,
  ItemMasterLifecycleStatus,
  ItemMasterPrimaryCategory,
  ItemMasterOwnershipContext
} from "@/types/item-master-governance";
import { ITEM_MASTER_CATEGORIES, ITEM_MASTER_LIFECYCLE_ACTIONS } from "@/types/item-master-governance";

export type ItemMasterMaintenanceTarget = {
  itemId: string;
  itemCode: string;
  displayName: string;
  primaryCategory?: ItemMasterPrimaryCategory;
  ownershipContext?: ItemMasterOwnershipContext;
  baseUomCode?: string;
};

type ItemMasterMaintenancePanelProps = {
  open: boolean;
  dataSourceMode: DataSourceMode;
  target?: ItemMasterMaintenanceTarget;
  onClose: () => void;
  onSaved: () => void;
};

type DraftValidationOptions = {
  isEdit?: boolean;
  originalBaseUomCode?: string;
  baseUomLocked?: boolean;
  catchWeightAuthorized?: boolean;
};

const EMPTY_DRAFT: ItemMasterDraft = {
  displayName: "",
  primaryCategory: "",
  ownershipContext: "",
  baseUomCode: "",
  description: "",
  specificationSummary: "",
  specificationReference: "",
  specificationLineageId: "",
  specificationRevisionNo: "1",
  specificationCode: "",
  specificationName: "",
  specificationHash: "",
  specificationEffectiveFrom: "",
  specificationEffectiveTo: "",
  conversionFromUomCode: "",
  conversionToUomCode: "",
  conversionMode: "FIXED",
  conversionFactor: "",
  conversionDecimalScale: "2",
  conversionRoundingMode: "HALF_UP",
  conversionEffectiveFrom: "",
  conversionEffectiveTo: ""
};

const categoryLabels: Record<ItemMasterPrimaryCategory, string> = {
  RAW: "原料",
  MATERIAL: "材料",
  FILM: "膜材",
  WIP: "半成品",
  FG: "成品"
};

const lifecycleLabels: Record<ItemMasterLifecycleStatus, string> = {
  DRAFT: "草稿",
  ACTIVE: "啟用",
  BLOCKED: "封鎖",
  INACTIVE: "停用",
  SUPERSEDED: "已被取代",
  RETIRED: "退役"
};

const lifecycleActionLabels: Record<ItemMasterLifecycleAction, string> = {
  ACTIVATE: "啟用",
  BLOCK: "封鎖",
  INACTIVATE: "停用",
  SUPERSEDE: "建立取代關係",
  RETIRE: "退役"
};

function createIdempotencyKey() {
  return typeof crypto !== "undefined" && "randomUUID" in crypto
    ? crypto.randomUUID()
    : `fm02-${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

function draftFromGovernance(
  data?: Partial<ItemMasterGovernanceData>,
  target?: ItemMasterMaintenanceTarget
): ItemMasterDraft {
  return {
    ...EMPTY_DRAFT,
    displayName: data?.displayName ?? target?.displayName ?? "",
    primaryCategory: data?.primaryCategory ?? target?.primaryCategory ?? "",
    ownershipContext: data?.ownershipContext ?? target?.ownershipContext ?? "",
    baseUomCode: data?.baseUomCode ?? target?.baseUomCode ?? "",
    description: data?.description ?? "",
    specificationSummary: data?.specificationSummary ?? "",
    specificationReference: data?.specificationReference ?? "",
    specificationLineageId: data?.specificationRevisions?.[0]?.specificationLineageId ?? "",
    specificationRevisionNo: data?.specificationRevisions?.[0]?.revisionNo
      ? String(data.specificationRevisions[0].revisionNo)
      : "1",
    specificationCode: data?.specificationRevisions?.[0]?.specificationCode ?? "",
    specificationName: data?.specificationRevisions?.[0]?.specificationName ?? "",
    specificationHash: data?.specificationRevisions?.[0]?.specificationHash ?? "",
    specificationEffectiveFrom: data?.specificationRevisions?.[0]?.effectiveFrom ?? "",
    specificationEffectiveTo: data?.specificationRevisions?.[0]?.effectiveTo ?? "",
    conversionFromUomCode: data?.conversionRevisions?.[0]?.fromUomCode ?? "",
    conversionToUomCode: data?.conversionRevisions?.[0]?.toUomCode ?? "",
    conversionMode: data?.conversionRevisions?.[0]?.conversionMode ?? "FIXED",
    conversionFactor: data?.conversionRevisions?.[0]?.factor ?? "",
    conversionDecimalScale: data?.conversionRevisions?.[0]?.decimalScale !== undefined
      ? String(data.conversionRevisions[0].decimalScale)
      : "2",
    conversionRoundingMode: data?.conversionRevisions?.[0]?.roundingMode ?? "HALF_UP",
    conversionEffectiveFrom: data?.conversionRevisions?.[0]?.effectiveFrom ?? "",
    conversionEffectiveTo: data?.conversionRevisions?.[0]?.effectiveTo ?? ""
  };
}

function hasAnyValue(...values: string[]) {
  return values.some((value) => value.trim().length > 0);
}

export function validateItemMasterDraft(
  draft: ItemMasterDraft,
  options: DraftValidationOptions = {}
) {
  const errors: Record<string, string> = {};

  if (!draft.displayName.trim()) errors.displayName = "請輸入品項名稱。";
  if (!draft.primaryCategory) errors.primaryCategory = "請選擇主分類。";
  if (!draft.ownershipContext) errors.ownershipContext = "請選擇所有權情境。";
  if (!/^[A-Z0-9]{1,3}$/.test(draft.baseUomCode.trim())) {
    errors.baseUomCode = "基準單位需為 1-3 碼大寫英數字。";
  }
  if (
    options.isEdit &&
    options.baseUomLocked &&
    options.originalBaseUomCode &&
    draft.baseUomCode.trim() !== options.originalBaseUomCode
  ) {
    errors.baseUomCode = "正式使用後基準單位已鎖定，不能直接修改。";
  }

  const hasSpecificationPeriod = hasAnyValue(
    draft.specificationSummary,
    draft.specificationReference,
    draft.specificationLineageId,
    draft.specificationRevisionNo,
    draft.specificationCode,
    draft.specificationName,
    draft.specificationHash,
    draft.specificationEffectiveFrom,
    draft.specificationEffectiveTo
  );
  if (hasSpecificationPeriod && !draft.specificationEffectiveFrom) {
    errors.specificationEffectiveFrom = "規格 revision 需要生效起日。";
  }
  if (hasSpecificationPeriod && !draft.specificationSummary.trim()) {
    errors.specificationSummary = "規格 revision 需要規格摘要。";
  }
  if (hasSpecificationPeriod && !draft.specificationLineageId.trim()) {
    errors.specificationLineageId = "規格 revision 需要 lineage ID。";
  }
  if (hasSpecificationPeriod && (!Number.isInteger(Number(draft.specificationRevisionNo)) || Number(draft.specificationRevisionNo) < 1)) {
    errors.specificationRevisionNo = "revision number 必須是正整數。";
  }
  if (hasSpecificationPeriod && !draft.specificationCode.trim()) {
    errors.specificationCode = "規格 revision 需要 specification code。";
  }
  if (hasSpecificationPeriod && !draft.specificationName.trim()) {
    errors.specificationName = "規格 revision 需要 specification name。";
  }
  if (hasSpecificationPeriod && !/^[A-Fa-f0-9]{64}$/.test(draft.specificationHash.trim())) {
    errors.specificationHash = "規格 hash 必須是 64 碼十六進位值。";
  }
  if (
    draft.specificationEffectiveFrom &&
    draft.specificationEffectiveTo &&
    draft.specificationEffectiveTo < draft.specificationEffectiveFrom
  ) {
    errors.specificationEffectiveTo = "規格生效迄日不可早於起日。";
  }

  const hasConversion = hasAnyValue(
    draft.conversionFromUomCode,
    draft.conversionToUomCode,
    draft.conversionFactor,
    draft.conversionEffectiveFrom,
    draft.conversionEffectiveTo
  );
  if (hasConversion) {
    if (!draft.conversionFromUomCode.trim()) errors.conversionFromUomCode = "請輸入來源單位。";
    if (!draft.conversionToUomCode.trim()) errors.conversionToUomCode = "請輸入目的單位。";
    if (draft.conversionFromUomCode.trim() === draft.conversionToUomCode.trim()) {
      errors.conversionToUomCode = "來源與目的單位不可相同。";
    }
    if (!draft.conversionEffectiveFrom) errors.conversionEffectiveFrom = "換算 revision 需要生效起日。";
    if (
      draft.conversionEffectiveFrom &&
      draft.conversionEffectiveTo &&
      draft.conversionEffectiveTo < draft.conversionEffectiveFrom
    ) {
      errors.conversionEffectiveTo = "換算生效迄日不可早於起日。";
    }
    if (draft.conversionMode === "FIXED") {
      const factor = Number(draft.conversionFactor);
      if (!Number.isFinite(factor) || factor <= 0) errors.conversionFactor = "固定換算因子需為大於 0 的數字。";
    } else if (!options.catchWeightAuthorized) {
      errors.conversionMode = "目前品項未取得重量換算授權，不能建立 CATCH_WEIGHT revision。";
    }
  }

  return errors;
}

function inputClass(hasError?: boolean) {
  return `mt-1 h-10 w-full rounded-input border px-3 text-sm text-textPrimary outline-none ${
    hasError ? "border-danger ring-1 ring-danger/20" : "border-border"
  }`;
}

function FieldError({ message }: { message?: string }) {
  return message ? <p className="mt-1 text-xs text-danger">{message}</p> : null;
}

function formatDateTime(value: string) {
  if (!value) return "未提供";
  return value.replace("T", " ");
}

export function ItemMasterMaintenancePanel({
  open,
  dataSourceMode,
  target,
  onClose,
  onSaved
}: ItemMasterMaintenancePanelProps) {
  const isEdit = Boolean(target);
  const [governance, setGovernance] = useState<ItemMasterGovernanceData>();
  const [draft, setDraft] = useState<ItemMasterDraft>(EMPTY_DRAFT);
  const [isLoading, setIsLoading] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string>();
  const [notice, setNotice] = useState<string>();
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});
  const [changeReason, setChangeReason] = useState("");
  const [lifecycleAction, setLifecycleAction] = useState<ItemMasterLifecycleAction>();
  const [lifecycleReason, setLifecycleReason] = useState("");
  const [lifecycleEffectiveAt, setLifecycleEffectiveAt] = useState("");
  const [lifecycleEvidence, setLifecycleEvidence] = useState("");
  const [businessActorType, setBusinessActorType] = useState("BUSINESS");
  const [businessActorRef, setBusinessActorRef] = useState("");
  const [accountableApprovalRole, setAccountableApprovalRole] = useState("");
  const [delegatedAuthorizationRef, setDelegatedAuthorizationRef] = useState("");
  const [reentryReviewEvidenceRef, setReentryReviewEvidenceRef] = useState("");
  const [successorRelationshipId, setSuccessorRelationshipId] = useState("");

  useEffect(() => {
    if (!open) return;
    let cancelled = false;
    setError(undefined);
    setNotice(undefined);
    setFieldErrors({});
    setChangeReason("");
    setLifecycleAction(undefined);
    setBusinessActorType("BUSINESS");
    setBusinessActorRef("");
    setAccountableApprovalRole("");
    setDelegatedAuthorizationRef("");
    setReentryReviewEvidenceRef("");
    setSuccessorRelationshipId("");
    setDraft(draftFromGovernance(undefined, target));
    if (!target) {
      setGovernance(undefined);
      return () => { cancelled = true; };
    }

    setIsLoading(true);
    getItemMasterGovernance(target.itemId, dataSourceMode).then((result) => {
      if (cancelled) return;
      setIsLoading(false);
      if (result.error) {
        setError(result.error);
        setGovernance(undefined);
        return;
      }
      setGovernance(result.data);
      setDraft(draftFromGovernance(result.data, target));
    });
    return () => { cancelled = true; };
  }, [dataSourceMode, open, target]);

  const lifecycleActions = useMemo(
    () => (governance ? ITEM_MASTER_LIFECYCLE_ACTIONS[governance.lifecycleStatus] : []),
    [governance]
  );
  const lockedBaseUom = Boolean(governance?.baseUomLocked);

  if (!open) return null;

  const updateDraft = <K extends keyof ItemMasterDraft>(field: K, value: ItemMasterDraft[K]) => {
    setDraft((current) => ({ ...current, [field]: value }));
    setFieldErrors((current) => {
      const next = { ...current };
      delete next[field];
      return next;
    });
  };

  const showResult = (result: { data?: ItemMasterGovernanceData; error?: string; status?: number; fieldErrors?: Record<string, string> }) => {
    if (result.error) {
      const errorMessage = result.status === 401
        ? "登入驗證已失效，請重新登入後再試。"
        : result.status === 403
          ? "目前使用者沒有執行此操作的權限。"
          : result.status === 409
            ? "資料衝突，可能是版本過期、有效期間重疊或生命週期轉移不允許；請重新載入後再試。"
            : result.error;
      setError(errorMessage);
      setFieldErrors(result.fieldErrors ?? {});
      setNotice(undefined);
      return false;
    }
    if (result.data) setGovernance(result.data);
    setError(undefined);
    setFieldErrors({});
    setNotice("已送出後端處理，畫面將依回傳資料更新。");
    return true;
  };

  const submitCreateForm = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (isEdit) return;
    const errors = validateItemMasterDraft(draft, {
      catchWeightAuthorized: governance?.catchWeightAuthorized
    });
    setFieldErrors(errors);
    setError(undefined);
    setNotice(undefined);
    if (Object.keys(errors).length) return;

    setIsSubmitting(true);
    const result = await createItemMaster({
      idempotency_key: createIdempotencyKey(),
      display_name: draft.displayName.trim(),
      primary_category: draft.primaryCategory as ItemMasterPrimaryCategory,
      ownership_context: draft.ownershipContext as ItemMasterOwnershipContext,
      base_uom_code: draft.baseUomCode.trim(),
      description: draft.description.trim(),
      specification_summary: draft.specificationSummary.trim() || undefined,
      specification_reference: draft.specificationReference.trim() || undefined
    }, dataSourceMode);
    setIsSubmitting(false);
    if (showResult(result)) onSaved();
  };

  const validateAuditedCorrection = (field: "displayName" | "primaryCategory") => {
    const errors: Record<string, string> = {};
    if (field === "displayName" && !draft.displayName.trim()) errors.displayName = "請輸入品項名稱。";
    if (field === "primaryCategory" && !draft.primaryCategory) errors.primaryCategory = "請選擇主分類。";
    if (!changeReason.trim()) errors.changeReason = "名稱或分類變更需要填寫原因。";
    setFieldErrors(errors);
    return errors;
  };

  const submitNameChange = async () => {
    if (!target || Object.keys(validateAuditedCorrection("displayName")).length) return;
    setIsSubmitting(true);
    const result = await updateItemName(target.itemId, {
      request_id: createIdempotencyKey(),
      display_name: draft.displayName.trim(),
      reason: changeReason.trim(),
      expected_row_version: governance?.rowVersion ?? 0
    }, dataSourceMode);
    setIsSubmitting(false);
    if (showResult(result)) onSaved();
  };

  const submitCategoryChange = async () => {
    if (!target || Object.keys(validateAuditedCorrection("primaryCategory")).length) return;
    setIsSubmitting(true);
    const result = await updateItemCategory(target.itemId, {
      request_id: createIdempotencyKey(),
      primary_category: draft.primaryCategory as ItemMasterPrimaryCategory,
      reason: changeReason.trim(),
      expected_row_version: governance?.rowVersion ?? 0
    }, dataSourceMode);
    setIsSubmitting(false);
    if (showResult(result)) onSaved();
  };

  const submitSpecificationRevision = async () => {
    if (!target) return;
    const errors = validateItemMasterDraft(draft, { catchWeightAuthorized: governance?.catchWeightAuthorized });
    const revisionErrors = Object.fromEntries(
      Object.entries(errors).filter(([key]) => key.startsWith("specification"))
    );
    if (!draft.specificationSummary.trim()) revisionErrors.specificationSummary = "規格 revision 需要規格摘要。";
    if (!draft.specificationEffectiveFrom) revisionErrors.specificationEffectiveFrom = "規格 revision 需要生效起日。";
    setFieldErrors(revisionErrors);
    if (Object.keys(revisionErrors).length) return;
    setIsSubmitting(true);
    const result = await createSpecificationRevision(target.itemId, {
      specification_lineage_id: draft.specificationLineageId.trim(),
      revision_no: Number(draft.specificationRevisionNo),
      specification_code: draft.specificationCode.trim(),
      specification_name: draft.specificationName.trim(),
      specification_hash: draft.specificationHash.trim().toUpperCase(),
      specification_summary: draft.specificationSummary.trim(),
      specification_reference: draft.specificationReference.trim() || undefined,
      revision_status: "DRAFT",
      effective_from: draft.specificationEffectiveFrom,
      effective_to: draft.specificationEffectiveTo || undefined,
      expected_row_version: governance?.rowVersion ?? 0
    }, dataSourceMode);
    setIsSubmitting(false);
    showResult(result);
  };

  const submitConversionRevision = async () => {
    if (!target) return;
    const errors = validateItemMasterDraft(draft, {
      catchWeightAuthorized: governance?.catchWeightAuthorized
    });
    const revisionErrors = Object.fromEntries(
      Object.entries(errors).filter(([key]) => key.startsWith("conversion"))
    );
    if (!draft.conversionFromUomCode.trim()) revisionErrors.conversionFromUomCode = "請輸入來源單位。";
    if (!draft.conversionToUomCode.trim()) revisionErrors.conversionToUomCode = "請輸入目的單位。";
    if (!draft.conversionEffectiveFrom) revisionErrors.conversionEffectiveFrom = "換算 revision 需要生效起日。";
    setFieldErrors(revisionErrors);
    if (Object.keys(revisionErrors).length) return;
    setIsSubmitting(true);
    const result = await createConversionRevision(target.itemId, {
      idempotency_key: createIdempotencyKey(),
      from_uom_code: draft.conversionFromUomCode.trim(),
      to_uom_code: draft.conversionToUomCode.trim(),
      conversion_mode: draft.conversionMode,
      factor: draft.conversionMode === "FIXED" ? draft.conversionFactor : undefined,
      decimal_scale: Number(draft.conversionDecimalScale),
      rounding_mode: draft.conversionRoundingMode.trim(),
      effective_from: draft.conversionEffectiveFrom,
      effective_to: draft.conversionEffectiveTo || undefined,
      expected_row_version: governance?.rowVersion ?? 0
    }, dataSourceMode);
    setIsSubmitting(false);
    showResult(result);
  };

  const submitLifecycle = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!target || !lifecycleAction) return;
    const lifecycleErrors: Record<string, string> = {};
    if (!lifecycleReason.trim()) lifecycleErrors.lifecycleReason = "生命週期動作需要原因。";
    if (!lifecycleEffectiveAt) lifecycleErrors.lifecycleEffectiveAt = "請填寫生效時間。";
    if (!lifecycleEvidence.trim()) lifecycleErrors.lifecycleEvidence = "生命週期動作需要決策證據參照。";
    if (!businessActorRef.trim()) lifecycleErrors.businessActorRef = "請填寫業務執行者參照。";
    if (!accountableApprovalRole.trim()) lifecycleErrors.accountableApprovalRole = "請填寫負責核准角色。";
    if (lifecycleAction === "ACTIVATE" && !delegatedAuthorizationRef.trim()) lifecycleErrors.delegatedAuthorizationRef = "啟用需要業務授權參照。";
    if ((governance?.lifecycleStatus === "BLOCKED" || governance?.lifecycleStatus === "INACTIVE") && lifecycleAction === "ACTIVATE" && !reentryReviewEvidenceRef.trim()) lifecycleErrors.reentryReviewEvidenceRef = "重新啟用需要 review evidence。";
    if (lifecycleAction === "SUPERSEDE" && !successorRelationshipId.trim()) lifecycleErrors.successorRelationshipId = "建立取代關係時需要 successor relationship ID。";
    setFieldErrors(lifecycleErrors);
    if (Object.keys(lifecycleErrors).length) return;
    setIsSubmitting(true);
    const result = await submitItemLifecycleAction(target.itemId, {
      request_id: createIdempotencyKey(),
      idempotency_key: createIdempotencyKey(),
      to_status: {
        ACTIVATE: "ACTIVE",
        BLOCK: "BLOCKED",
        INACTIVATE: "INACTIVE",
        SUPERSEDE: "SUPERSEDED",
        RETIRE: "RETIRED"
      }[lifecycleAction],
      reason: lifecycleReason.trim(),
      business_actor_type: businessActorType,
      business_actor_ref: businessActorRef.trim(),
      accountable_approval_role: accountableApprovalRole.trim(),
      delegated_authorization_ref: delegatedAuthorizationRef.trim() || undefined,
      decision_evidence_ref: lifecycleEvidence.trim(),
      effective_at: lifecycleEffectiveAt,
      expected_row_version: governance?.rowVersion ?? 0,
      successor_relationship_id: lifecycleAction === "SUPERSEDE" ? successorRelationshipId.trim() : undefined,
      reentry_review_evidence_ref: reentryReviewEvidenceRef.trim() || undefined
    }, dataSourceMode);
    setIsSubmitting(false);
    if (showResult(result)) {
      setLifecycleAction(undefined);
      setLifecycleReason("");
      setLifecycleEffectiveAt("");
      setLifecycleEvidence("");
      setBusinessActorRef("");
      setAccountableApprovalRole("");
      setDelegatedAuthorizationRef("");
      setReentryReviewEvidenceRef("");
      setSuccessorRelationshipId("");
    }
  };

  return (
    <section className="rounded-lg border border-primary/20 bg-white p-4 shadow-sm" aria-label="料品主檔維護面板">
      <div className="flex items-start justify-between gap-3 border-b border-border pb-4">
        <div>
          <div className="flex flex-wrap items-center gap-2">
            <p className="text-xs font-medium text-textSecondary">料品主檔治理</p>
            <StatusBadge tone={dataSourceMode === "api" ? "info" : "neutral"}>
              {dataSourceMode === "api" ? "後端資料" : "示範資料"}
            </StatusBadge>
            {governance ? <StatusBadge tone="neutral">{lifecycleLabels[governance.lifecycleStatus]}</StatusBadge> : null}
          </div>
          <h3 className="mt-1 text-lg font-semibold text-textPrimary">{isEdit ? "維護料品主檔" : "新增料品"}</h3>
          <p className="mt-1 text-sm text-textSecondary">
            {isEdit ? `${target?.itemCode || target?.itemId} · ${target?.displayName || "未命名料品"}` : "建立後由後端產生料號、版本與稽核紀錄。"}
          </p>
        </div>
        <button aria-label="關閉料品主檔維護" className="rounded-button p-2 text-textSecondary hover:bg-slate-100" onClick={onClose} type="button">
          <X className="h-5 w-5" />
        </button>
      </div>

      {isLoading ? (
        <div className="flex items-center gap-2 py-5 text-sm text-textSecondary"><Loader2 className="h-4 w-4 animate-spin text-primary" />載入主檔治理資料</div>
      ) : null}
      {error ? <div className="mt-4 flex gap-2 rounded-md border border-danger/20 bg-danger/10 px-3 py-2 text-sm text-danger" role="alert"><AlertTriangle className="h-4 w-4 shrink-0" />{error}</div> : null}
      {notice ? <div className="mt-4 flex gap-2 rounded-md border border-success/20 bg-success/10 px-3 py-2 text-sm text-success" role="status"><CheckCircle2 className="h-4 w-4 shrink-0" />{notice}</div> : null}
      {dataSourceMode === "mock" ? <p className="mt-4 rounded-md border border-warning/20 bg-warning/10 px-3 py-2 text-xs text-textSecondary">示範資料模式只提供欄位與驗證預覽，不會寫入後端。</p> : null}

      {!isLoading ? (
        <div className="mt-5 space-y-5">
          <form className="space-y-4" onSubmit={submitCreateForm}>
            <div className="grid gap-4 lg:grid-cols-2">
              <label className="text-xs text-textSecondary">品項名稱 *<input aria-label="品項名稱" className={inputClass(Boolean(fieldErrors.displayName))} onChange={(event) => updateDraft("displayName", event.target.value)} value={draft.displayName} /><FieldError message={fieldErrors.displayName} /></label>
              <label className="text-xs text-textSecondary">主分類 *<select aria-label="主分類" className={inputClass(Boolean(fieldErrors.primaryCategory))} onChange={(event) => updateDraft("primaryCategory", event.target.value as ItemMasterDraft["primaryCategory"])} value={draft.primaryCategory}><option value="">請選擇</option>{ITEM_MASTER_CATEGORIES.map((category) => <option key={category} value={category}>{categoryLabels[category]} ({category})</option>)}</select><FieldError message={fieldErrors.primaryCategory} /></label>
              <label className="text-xs text-textSecondary">所有權情境 *<select aria-label="所有權情境" className={inputClass(Boolean(fieldErrors.ownershipContext))} disabled={isEdit} onChange={(event) => updateDraft("ownershipContext", event.target.value as ItemMasterDraft["ownershipContext"])} value={draft.ownershipContext}><option value="">請選擇</option><option value="COMPANY_PURCHASED">公司採購</option><option value="CUSTOMER_SUPPLIED">客供</option><option value="BOTH">公司採購／客供</option></select><FieldError message={fieldErrors.ownershipContext} /></label>
              <label className="text-xs text-textSecondary">基準單位 *{lockedBaseUom ? <span className="ml-1 inline-flex items-center gap-1 text-warning"><LockKeyhole className="h-3 w-3" />已鎖定</span> : null}<input aria-label="基準單位" className={inputClass(Boolean(fieldErrors.baseUomCode))} disabled={isEdit || lockedBaseUom} onChange={(event) => updateDraft("baseUomCode", event.target.value.toUpperCase())} value={draft.baseUomCode} /><FieldError message={fieldErrors.baseUomCode} /></label>
              <label className="text-xs text-textSecondary lg:col-span-2">說明<textarea aria-label="品項說明" className="mt-1 min-h-20 w-full rounded-input border border-border px-3 py-2 text-sm text-textPrimary outline-none" disabled={isEdit} onChange={(event) => updateDraft("description", event.target.value)} value={draft.description} /></label>
            </div>

            <div className="flex items-center gap-2 border-t border-border pt-4"><ShieldCheck className="h-4 w-4 text-primary" /><h4 className="text-sm font-semibold text-textPrimary">伺服器管理欄位</h4></div>
            <div className="grid gap-3 rounded-md bg-slate-50 p-3 text-sm sm:grid-cols-2 lg:grid-cols-4">
              <div><p className="text-xs text-textSecondary">料號</p><p className="mt-1 font-medium text-textPrimary">{governance?.itemCode || target?.itemCode || "建立後產生"}</p></div>
              <div><p className="text-xs text-textSecondary">Item ID</p><p className="mt-1 font-medium text-textPrimary">{governance?.itemId || target?.itemId || "建立後產生"}</p></div>
              <div><p className="text-xs text-textSecondary">Row version</p><p className="mt-1 font-medium text-textPrimary">{governance?.rowVersion ?? "建立後產生"}</p></div>
              <div><p className="text-xs text-textSecondary">重量換算授權</p><p className="mt-1 font-medium text-textPrimary">{governance?.catchWeightAuthorized ? "已授權" : "未授權"}</p></div>
            </div>
            {!isEdit ? <button className="inline-flex h-10 items-center gap-2 rounded-button bg-primary px-4 text-sm font-medium text-white disabled:cursor-not-allowed disabled:opacity-60" disabled={isSubmitting} type="submit"><Save className="h-4 w-4" />{isSubmitting ? "送出中" : "建立料品"}</button> : null}
          </form>

          {isEdit ? (
            <section className="rounded-md border border-primary/20 bg-slate-50 p-3">
              <div className="flex items-center gap-2"><ShieldCheck className="h-4 w-4 text-primary" /><h4 className="text-sm font-semibold text-textPrimary">受控主檔修正</h4></div>
              <p className="mt-1 text-xs leading-5 text-textSecondary">名稱與主分類是分開的 audited action；所有權情境、基準單位與說明在本畫面維持伺服器唯讀。</p>
              <label className="mt-3 block text-xs text-textSecondary">變更原因 *<textarea aria-label="主檔變更原因" className="mt-1 min-h-20 w-full rounded-input border border-border bg-white px-3 py-2 text-sm text-textPrimary" onChange={(event) => setChangeReason(event.target.value)} value={changeReason} /><FieldError message={fieldErrors.changeReason} /></label>
              <div className="mt-3 flex flex-wrap gap-2">
                <button className="inline-flex h-9 items-center gap-2 rounded-button bg-primary px-3 text-xs font-medium text-white disabled:opacity-60" disabled={isSubmitting} onClick={submitNameChange} type="button"><Save className="h-4 w-4" />送出名稱修正</button>
                <button className="inline-flex h-9 items-center gap-2 rounded-button border border-border bg-white px-3 text-xs font-medium text-textSecondary disabled:opacity-60" disabled={isSubmitting} onClick={submitCategoryChange} type="button"><Save className="h-4 w-4" />送出分類修正</button>
              </div>
            </section>
          ) : null}

          {isEdit ? (
            <>
              <section className="border-t border-border pt-4">
                <div className="flex items-center gap-2"><FilePlus2 className="h-4 w-4 text-primary" /><h4 className="text-sm font-semibold text-textPrimary">規格 revision</h4></div>
                <div className="mt-3 grid gap-3 lg:grid-cols-2">
                  <label className="text-xs text-textSecondary">Specification lineage ID *<input aria-label="規格 lineage ID" className={inputClass(Boolean(fieldErrors.specificationLineageId))} onChange={(event) => updateDraft("specificationLineageId", event.target.value)} value={draft.specificationLineageId} /><FieldError message={fieldErrors.specificationLineageId} /></label>
                  <label className="text-xs text-textSecondary">Revision number *<input aria-label="規格 revision number" className={inputClass(Boolean(fieldErrors.specificationRevisionNo))} inputMode="numeric" onChange={(event) => updateDraft("specificationRevisionNo", event.target.value)} value={draft.specificationRevisionNo} /><FieldError message={fieldErrors.specificationRevisionNo} /></label>
                  <label className="text-xs text-textSecondary">Specification code *<input aria-label="規格 code" className={inputClass(Boolean(fieldErrors.specificationCode))} onChange={(event) => updateDraft("specificationCode", event.target.value)} value={draft.specificationCode} /><FieldError message={fieldErrors.specificationCode} /></label>
                  <label className="text-xs text-textSecondary">Specification name *<input aria-label="規格 name" className={inputClass(Boolean(fieldErrors.specificationName))} onChange={(event) => updateDraft("specificationName", event.target.value)} value={draft.specificationName} /><FieldError message={fieldErrors.specificationName} /></label>
                  <label className="text-xs text-textSecondary">Specification hash *<input aria-label="規格 hash" className={inputClass(Boolean(fieldErrors.specificationHash))} onChange={(event) => updateDraft("specificationHash", event.target.value)} value={draft.specificationHash} /><FieldError message={fieldErrors.specificationHash} /></label>
                  <label className="text-xs text-textSecondary">規格摘要 *<input aria-label="規格摘要" className={inputClass(Boolean(fieldErrors.specificationSummary))} onChange={(event) => updateDraft("specificationSummary", event.target.value)} value={draft.specificationSummary} /><FieldError message={fieldErrors.specificationSummary} /></label>
                  <label className="text-xs text-textSecondary">規格參照<input aria-label="規格參照" className={inputClass(Boolean(fieldErrors.specificationReference))} onChange={(event) => updateDraft("specificationReference", event.target.value)} value={draft.specificationReference} /></label>
                  <label className="text-xs text-textSecondary">生效起日<input aria-label="規格生效起日" className={inputClass(Boolean(fieldErrors.specificationEffectiveFrom))} onChange={(event) => updateDraft("specificationEffectiveFrom", event.target.value)} type="datetime-local" value={draft.specificationEffectiveFrom} /><FieldError message={fieldErrors.specificationEffectiveFrom} /></label>
                  <label className="text-xs text-textSecondary">生效迄日<input aria-label="規格生效迄日" className={inputClass(Boolean(fieldErrors.specificationEffectiveTo))} onChange={(event) => updateDraft("specificationEffectiveTo", event.target.value)} type="datetime-local" value={draft.specificationEffectiveTo} /><FieldError message={fieldErrors.specificationEffectiveTo} /></label>
                </div>
                <button className="mt-3 inline-flex h-9 items-center gap-2 rounded-button border border-border bg-white px-3 text-xs font-medium text-textSecondary disabled:opacity-60" disabled={isSubmitting} onClick={submitSpecificationRevision} type="button"><FilePlus2 className="h-4 w-4" />新增規格 revision</button>
                {governance?.specificationRevisions.length ? <div className="mt-3 space-y-2">{governance.specificationRevisions.map((revision) => <div className="rounded-md border border-border p-3 text-sm" key={revision.id}><div className="flex justify-between gap-2"><p className="font-medium text-textPrimary">R{revision.revisionNo} · {revision.summary || "未提供摘要"}</p><StatusBadge tone={revision.status === "ACTIVE" ? "success" : "neutral"}>{revision.status}</StatusBadge></div><p className="mt-1 text-xs text-textSecondary">{formatDateTime(revision.effectiveFrom)} - {formatDateTime(revision.effectiveTo)}</p></div>)}</div> : <p className="mt-3 text-xs text-textSecondary">目前沒有規格 revision。</p>}
              </section>

              <section className="border-t border-border pt-4">
                <div className="flex items-center gap-2"><FilePlus2 className="h-4 w-4 text-primary" /><h4 className="text-sm font-semibold text-textPrimary">UOM conversion revision</h4></div>
                <div className="mt-3 grid gap-3 lg:grid-cols-2">
                  <label className="text-xs text-textSecondary">來源單位<input aria-label="換算來源單位" className={inputClass(Boolean(fieldErrors.conversionFromUomCode))} onChange={(event) => updateDraft("conversionFromUomCode", event.target.value.toUpperCase())} value={draft.conversionFromUomCode} /><FieldError message={fieldErrors.conversionFromUomCode} /></label>
                  <label className="text-xs text-textSecondary">目的單位<input aria-label="換算目的單位" className={inputClass(Boolean(fieldErrors.conversionToUomCode))} onChange={(event) => updateDraft("conversionToUomCode", event.target.value.toUpperCase())} value={draft.conversionToUomCode} /><FieldError message={fieldErrors.conversionToUomCode} /></label>
                  <label className="text-xs text-textSecondary">換算模式<select aria-label="換算模式" className={inputClass(Boolean(fieldErrors.conversionMode))} onChange={(event) => updateDraft("conversionMode", event.target.value as ItemMasterDraft["conversionMode"])} value={draft.conversionMode}><option value="FIXED">固定換算</option><option value="CATCH_WEIGHT">重量換算</option></select><FieldError message={fieldErrors.conversionMode} /></label>
                  <label className="text-xs text-textSecondary">固定換算因子<input aria-label="固定換算因子" className={inputClass(Boolean(fieldErrors.conversionFactor))} disabled={draft.conversionMode === "CATCH_WEIGHT"} onChange={(event) => updateDraft("conversionFactor", event.target.value)} value={draft.conversionFactor} /><FieldError message={fieldErrors.conversionFactor} /></label>
                  <label className="text-xs text-textSecondary">小數位<input aria-label="換算小數位" className={inputClass()} inputMode="numeric" onChange={(event) => updateDraft("conversionDecimalScale", event.target.value)} value={draft.conversionDecimalScale} /></label>
                  <label className="text-xs text-textSecondary">進位模式<input aria-label="換算進位模式" className={inputClass()} onChange={(event) => updateDraft("conversionRoundingMode", event.target.value)} value={draft.conversionRoundingMode} /></label>
                  <label className="text-xs text-textSecondary">生效起日<input aria-label="換算生效起日" className={inputClass(Boolean(fieldErrors.conversionEffectiveFrom))} onChange={(event) => updateDraft("conversionEffectiveFrom", event.target.value)} type="datetime-local" value={draft.conversionEffectiveFrom} /><FieldError message={fieldErrors.conversionEffectiveFrom} /></label>
                  <label className="text-xs text-textSecondary">生效迄日<input aria-label="換算生效迄日" className={inputClass(Boolean(fieldErrors.conversionEffectiveTo))} onChange={(event) => updateDraft("conversionEffectiveTo", event.target.value)} type="datetime-local" value={draft.conversionEffectiveTo} /><FieldError message={fieldErrors.conversionEffectiveTo} /></label>
                </div>
                <button className="mt-3 inline-flex h-9 items-center gap-2 rounded-button border border-border bg-white px-3 text-xs font-medium text-textSecondary disabled:cursor-not-allowed disabled:opacity-60" disabled={isSubmitting || dataSourceMode === "api"} onClick={submitConversionRevision} type="button"><FilePlus2 className="h-4 w-4" />新增 UOM conversion revision</button>
                {dataSourceMode === "api" ? <p className="mt-2 text-xs text-warning">目前 backend contract 尚未提供 UOM conversion endpoint，API 模式不會送出此操作。</p> : null}
                {governance?.conversionRevisions.length ? <div className="mt-3 space-y-2">{governance.conversionRevisions.map((revision) => <div className="rounded-md border border-border p-3 text-sm" key={revision.id}><div className="flex justify-between gap-2"><p className="font-medium text-textPrimary">{revision.fromUomCode} → {revision.toUomCode} · {revision.factor || revision.conversionMode}</p><StatusBadge tone={revision.status === "ACTIVE" ? "success" : "neutral"}>{revision.status}</StatusBadge></div><p className="mt-1 text-xs text-textSecondary">{formatDateTime(revision.effectiveFrom)} - {formatDateTime(revision.effectiveTo)} · {revision.roundingMode || "未提供進位模式"}</p></div>)}</div> : <p className="mt-3 text-xs text-textSecondary">目前沒有 UOM conversion revision。</p>}
              </section>

              <section className="border-t border-border pt-4">
                <div className="flex items-center gap-2"><ShieldCheck className="h-4 w-4 text-primary" /><h4 className="text-sm font-semibold text-textPrimary">生命週期與稽核</h4></div>
                <div className="mt-3 rounded-md bg-slate-50 p-3 text-sm"><div className="grid gap-2 sm:grid-cols-3"><div><p className="text-xs text-textSecondary">目前狀態</p><p className="mt-1 font-medium text-textPrimary">{governance ? lifecycleLabels[governance.lifecycleStatus] : "未提供"}</p></div><div><p className="text-xs text-textSecondary">基準單位鎖定</p><p className="mt-1 font-medium text-textPrimary">{lockedBaseUom ? "是" : "否"}</p></div><div><p className="text-xs text-textSecondary">資料版本</p><p className="mt-1 font-medium text-textPrimary">{governance?.rowVersion ?? "未提供"}</p></div></div></div>
                {lifecycleActions.length ? <div className="mt-3 flex flex-wrap gap-2">{lifecycleActions.map((action) => <button className={`inline-flex h-9 items-center gap-2 rounded-button border px-3 text-xs font-medium ${lifecycleAction === action ? "border-primary bg-primary/10 text-primary" : "border-border bg-white text-textSecondary"}`} key={action} onClick={() => setLifecycleAction(action)} type="button"><ShieldCheck className="h-3.5 w-3.5" />{lifecycleActionLabels[action]}</button>)}</div> : <p className="mt-3 text-xs text-textSecondary">目前狀態沒有可執行的生命週期動作。</p>}
                {lifecycleAction ? <form className="mt-3 grid gap-3 rounded-md border border-primary/20 p-3 lg:grid-cols-2" onSubmit={submitLifecycle}><div className="rounded-md bg-primary/5 px-3 py-2 text-xs text-textSecondary lg:col-span-2">狀態變更：{governance ? lifecycleLabels[governance.lifecycleStatus] : "未提供"} → {lifecycleActionLabels[lifecycleAction]}</div><label className="text-xs text-textSecondary">動作原因 *<textarea aria-label="生命週期動作原因" className="mt-1 min-h-20 w-full rounded-input border border-border px-3 py-2 text-sm text-textPrimary" onChange={(event) => setLifecycleReason(event.target.value)} value={lifecycleReason} /><FieldError message={fieldErrors.lifecycleReason} /></label><label className="text-xs text-textSecondary">業務執行者類型 *<select aria-label="業務執行者類型" className={inputClass()} onChange={(event) => setBusinessActorType(event.target.value)} value={businessActorType}><option value="BUSINESS">業務人員</option><option value="OWNER">Owner</option><option value="APPROVER">核准人員</option></select></label><label className="text-xs text-textSecondary">業務執行者參照 *<input aria-label="業務執行者參照" className={inputClass(Boolean(fieldErrors.businessActorRef))} onChange={(event) => setBusinessActorRef(event.target.value)} value={businessActorRef} /><FieldError message={fieldErrors.businessActorRef} /></label><label className="text-xs text-textSecondary">負責核准角色 *<input aria-label="負責核准角色" className={inputClass(Boolean(fieldErrors.accountableApprovalRole))} onChange={(event) => setAccountableApprovalRole(event.target.value)} value={accountableApprovalRole} /><FieldError message={fieldErrors.accountableApprovalRole} /></label><label className="text-xs text-textSecondary">生效時間 *<input aria-label="生命週期生效時間" className={inputClass(Boolean(fieldErrors.lifecycleEffectiveAt))} onChange={(event) => setLifecycleEffectiveAt(event.target.value)} type="datetime-local" value={lifecycleEffectiveAt} /><FieldError message={fieldErrors.lifecycleEffectiveAt} /></label><label className="text-xs text-textSecondary">證據參照 *<input aria-label="生命週期證據參照" className={inputClass(Boolean(fieldErrors.lifecycleEvidence))} onChange={(event) => setLifecycleEvidence(event.target.value)} value={lifecycleEvidence} /><FieldError message={fieldErrors.lifecycleEvidence} /></label><label className="text-xs text-textSecondary">業務授權參照{lifecycleAction === "ACTIVATE" ? " *" : ""}<input aria-label="業務授權參照" className={inputClass(Boolean(fieldErrors.delegatedAuthorizationRef))} onChange={(event) => setDelegatedAuthorizationRef(event.target.value)} value={delegatedAuthorizationRef} /><FieldError message={fieldErrors.delegatedAuthorizationRef} /></label>{(governance?.lifecycleStatus === "BLOCKED" || governance?.lifecycleStatus === "INACTIVE") && lifecycleAction === "ACTIVATE" ? <label className="text-xs text-textSecondary">重新啟用 review evidence *<input aria-label="重新啟用 review evidence" className={inputClass(Boolean(fieldErrors.reentryReviewEvidenceRef))} onChange={(event) => setReentryReviewEvidenceRef(event.target.value)} value={reentryReviewEvidenceRef} /><FieldError message={fieldErrors.reentryReviewEvidenceRef} /></label> : null}{lifecycleAction === "SUPERSEDE" ? <label className="text-xs text-textSecondary">Successor relationship ID *<input aria-label="取代關係參照" className={inputClass(Boolean(fieldErrors.successorRelationshipId))} onChange={(event) => setSuccessorRelationshipId(event.target.value)} value={successorRelationshipId} /><FieldError message={fieldErrors.successorRelationshipId} /></label> : null}<div className="flex items-end gap-2"><button className="inline-flex h-10 items-center gap-2 rounded-button bg-primary px-3 text-sm font-medium text-white disabled:opacity-60" disabled={isSubmitting} type="submit"><ShieldCheck className="h-4 w-4" />確認{lifecycleActionLabels[lifecycleAction]}</button><button className="h-10 rounded-button border border-border px-3 text-sm text-textSecondary" onClick={() => setLifecycleAction(undefined)} type="button">取消</button></div></form> : null}
                <div className="mt-4 space-y-2">{governance?.auditHistory.length ? governance.auditHistory.map((event) => <div className="rounded-md border border-border p-3 text-xs" key={event.id}><div className="flex justify-between gap-2"><p className="font-medium text-textPrimary">{event.label || event.eventType || "稽核事件"}</p><p className="text-textSecondary">{formatDateTime(event.occurredAt)}</p></div><p className="mt-1 text-textSecondary">執行者：{event.actor || "未提供"} · 核准者：{event.approver || "未提供"}</p>{event.reason ? <p className="mt-1 text-textSecondary">原因：{event.reason}</p> : null}</div>) : <p className="text-xs text-textSecondary">目前沒有稽核紀錄。</p>}</div>
              </section>
            </>
          ) : null}
        </div>
      ) : null}
    </section>
  );
}
