"use client";

import { AlertTriangle, CheckCircle2, CircleHelp, LockKeyhole, Plus, X } from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import { StatusBadge } from "@/components/ui/status-badge";
import { getItemC2Reference, FM02_C2_UI_SCOPE_DECISION, validateC2ConversionDraft, validateC2CustomerQualificationDraft } from "@/services/fm02-c2-api";
import type { DataSourceMode } from "@/components/common/data-source-toggle";
import type {
  C2ConversionDraft,
  C2CustomerQualificationDraft,
  C2ItemReferenceData,
  C2ValidationError
} from "@/types/fm02-c2";

type C2ReferencePanelProps = {
  itemId: string;
  dataSourceMode: DataSourceMode;
};

type FormMode = "conversion" | "qualification" | undefined;

const initialConversionDraft = (data?: C2ItemReferenceData): C2ConversionDraft => ({
  fromItemUomId: data?.itemUoms[0]?.id ?? "",
  toItemUomId: data?.itemUoms[1]?.id ?? "",
  conversionType: "FIXED",
  conversionFactor: "",
  effectiveFrom: "2026-10-16T00:00",
  sourceReference: "frontend-mock"
});

const initialQualificationDraft: C2CustomerQualificationDraft = {
  customerRef: "",
  approvalScope: "ANY_GENERAL_QUALIFIED_SUPPLIER",
  supplierQualificationId: "",
  supplyMethod: "PURCHASED",
  effectiveFrom: "2026-10-16T00:00",
  sourceReference: "frontend-mock"
};

function formatStatus(status: string) {
  return status === "ACTIVE" ? "啟用" : status === "DRAFT" ? "草稿" : status;
}

function formatUomLabel(data: C2ItemReferenceData, id: string) {
  return data.itemUoms.find((uom) => uom.id === id)?.label ?? id;
}

function FormErrors({ errors }: { errors: C2ValidationError[] }) {
  if (!errors.length) return null;
  return (
    <div className="rounded-md border border-danger/20 bg-danger/10 px-3 py-2 text-sm text-danger" role="alert">
      <p className="font-semibold">示範驗證未通過</p>
      <ul className="mt-1 list-disc pl-5">
        {errors.map((error) => <li key={`${error.field}-${error.message}`}>{error.field}: {error.message}</li>)}
      </ul>
    </div>
  );
}

export function C2ReferencePanel({ itemId, dataSourceMode }: C2ReferencePanelProps) {
  const [data, setData] = useState<C2ItemReferenceData>();
  const [error, setError] = useState<string>();
  const [isLoading, setIsLoading] = useState(true);
  const [formMode, setFormMode] = useState<FormMode>();
  const [conversionDraft, setConversionDraft] = useState<C2ConversionDraft>(initialConversionDraft());
  const [qualificationDraft, setQualificationDraft] = useState<C2CustomerQualificationDraft>(initialQualificationDraft);
  const [formErrors, setFormErrors] = useState<C2ValidationError[]>([]);
  const [formMessage, setFormMessage] = useState<string>();

  useEffect(() => {
    let cancelled = false;
    setIsLoading(true);
    setData(undefined);
    setError(undefined);
    setFormMode(undefined);
    getItemC2Reference(itemId, dataSourceMode).then((result) => {
      if (cancelled) return;
      setData(result.data);
      setError(result.error);
      setIsLoading(false);
      if (result.data) setConversionDraft(initialConversionDraft(result.data));
    });
    return () => { cancelled = true; };
  }, [dataSourceMode, itemId]);

  const uomIds = useMemo(() => data?.itemUoms.map((uom) => uom.id) ?? [], [data]);

  const openForm = (mode: FormMode) => {
    setFormMode(mode);
    setFormErrors([]);
    setFormMessage(undefined);
  };

  const closeForm = () => {
    setFormMode(undefined);
    setFormErrors([]);
    setFormMessage(undefined);
  };

  const submitConversion = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const errors = validateC2ConversionDraft(conversionDraft, uomIds);
    setFormErrors(errors);
    setFormMessage(errors.length ? undefined : "示範驗證通過；依目前 Product/Frontend 決策狀態，未送出或持久化資料。");
  };

  const submitQualification = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const errors = validateC2CustomerQualificationDraft(qualificationDraft);
    setFormErrors(errors);
    setFormMessage(errors.length ? undefined : "示範驗證通過；依目前 Product/Frontend 決策狀態，未送出或持久化資料。");
  };

  return (
    <section className="rounded-lg border border-primary/20 bg-slate-50 p-4" aria-label="FM02 C2 參考契約">
      <div className="flex items-start justify-between gap-3">
        <div>
          <div className="flex items-center gap-2">
            <p className="text-sm font-semibold text-textPrimary">C2 Item 參考契約</p>
            <StatusBadge tone={dataSourceMode === "mock" ? "info" : "warning"}>
              {dataSourceMode === "mock" ? "示範資料" : "API blocked"}
            </StatusBadge>
          </div>
          <p className="mt-1 text-xs leading-5 text-textSecondary">只展示 item-scoped UOM、conversion 與 customer qualification；不涵蓋 Product/SKU、全域換算或 live DB。</p>
        </div>
        <LockKeyhole className="h-5 w-5 shrink-0 text-textSecondary" aria-label="mock-only" />
      </div>

      <div className="mt-3 rounded-md border border-warning/20 bg-warning/10 px-3 py-2 text-xs leading-5 text-textSecondary">
        <p className="font-semibold text-textPrimary">Product decision record</p>
        <p>{FM02_C2_UI_SCOPE_DECISION}</p>
      </div>

      {isLoading ? <p className="mt-4 text-sm text-textSecondary">C2 參考資料載入中…</p> : null}
      {!isLoading && error ? (
        <div className="mt-4 flex gap-2 rounded-md border border-warning/20 bg-warning/10 px-3 py-2 text-sm text-textSecondary" role="status">
          <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0 text-warning" />
          <p>{error}</p>
        </div>
      ) : null}

      {data ? (
        <div className="mt-4 space-y-4">
          <div>
            <div className="mb-2 flex items-center justify-between gap-2">
              <p className="text-xs font-semibold text-textSecondary">Item UOM</p>
              <StatusBadge tone="neutral">{data.itemUoms.length} 筆</StatusBadge>
            </div>
            <div className="grid gap-2 sm:grid-cols-2">
              {data.itemUoms.map((uom) => (
                <div className="rounded-md border border-border bg-white p-3" key={uom.id}>
                  <div className="flex items-center justify-between gap-2">
                    <p className="font-medium text-textPrimary">{uom.label}</p>
                    <StatusBadge tone="neutral">{uom.role === "STOCK" ? "庫存" : "生產"}</StatusBadge>
                  </div>
                  <p className="mt-1 text-xs text-textSecondary">{uom.code} · {uom.id}</p>
                </div>
              ))}
            </div>
          </div>

          <div>
            <div className="mb-2 flex items-center justify-between gap-2">
              <p className="text-xs font-semibold text-textSecondary">Item-specific conversion</p>
              <button className="inline-flex h-8 items-center gap-1 rounded-button border border-border bg-white px-2 text-xs font-medium text-textSecondary" onClick={() => openForm("conversion")} type="button">
                <Plus className="h-3.5 w-3.5" /> 新增示範
              </button>
            </div>
            {data.conversionRules.length ? data.conversionRules.map((rule) => (
              <div className="rounded-md border border-border bg-white p-3" key={rule.id}>
                <div className="flex items-center justify-between gap-2">
                  <p className="font-medium text-textPrimary">{formatUomLabel(data, rule.fromItemUomId)} → {formatUomLabel(data, rule.toItemUomId)}</p>
                  <StatusBadge tone={rule.lifecycleStatus === "ACTIVE" ? "success" : "neutral"}>{formatStatus(rule.lifecycleStatus)}</StatusBadge>
                </div>
                <p className="mt-1 text-xs text-textSecondary">{rule.conversionType} · factor {rule.conversionFactor ?? "—"} · {rule.effectiveFrom}</p>
              </div>
            )) : (
              <div className="rounded-md border border-dashed border-border bg-white px-3 py-3 text-sm text-textSecondary">沒有可解析的 Item-specific conversion rule；不使用全域換算 fallback。</div>
            )}
          </div>

          <div>
            <div className="mb-2 flex items-center justify-between gap-2">
              <p className="text-xs font-semibold text-textSecondary">Customer qualification</p>
              <button className="inline-flex h-8 items-center gap-1 rounded-button border border-border bg-white px-2 text-xs font-medium text-textSecondary" onClick={() => openForm("qualification")} type="button">
                <Plus className="h-3.5 w-3.5" /> 新增示範
              </button>
            </div>
            {data.customerQualifications.length ? data.customerQualifications.map((qualification) => (
              <div className="rounded-md border border-border bg-white p-3" key={qualification.id}>
                <div className="flex items-center justify-between gap-2">
                  <p className="font-medium text-textPrimary">{qualification.customerRef}</p>
                  <StatusBadge tone={qualification.qualificationStatus === "ACTIVE" ? "success" : "neutral"}>{formatStatus(qualification.qualificationStatus)}</StatusBadge>
                </div>
                <p className="mt-1 text-xs text-textSecondary">{qualification.approvalScope} · {qualification.supplyMethod} · {qualification.effectiveFrom}</p>
              </div>
            )) : (
              <div className="rounded-md border border-dashed border-border bg-white px-3 py-3 text-sm text-textSecondary">目前沒有 customer qualification 示範資料。</div>
            )}
          </div>

          <div className="grid gap-2 sm:grid-cols-2">
            <div className="rounded-md border border-dashed border-border bg-white p-3 text-xs text-textSecondary">
              <div className="flex items-center gap-2 font-semibold text-textPrimary"><CircleHelp className="h-4 w-4 text-info" /> Package / customer structures</div>
              <p className="mt-1">UI 欄位與責任邊界尚未由 Product 接受；暫不呈現可寫入畫面。</p>
            </div>
            <div className="rounded-md border border-dashed border-border bg-white p-3 text-xs text-textSecondary">
              <div className="flex items-center gap-2 font-semibold text-textPrimary"><CircleHelp className="h-4 w-4 text-info" /> Legacy mapping</div>
              <p className="mt-1">僅可在 zero-row admission gate 後處理；本畫面不猜測或回填 legacy mapping。</p>
            </div>
          </div>

          {formMode ? (
            <div className="rounded-md border border-primary/20 bg-white p-3">
              <div className="flex items-center justify-between gap-2">
                <p className="text-sm font-semibold text-textPrimary">{formMode === "conversion" ? "新增 Item-specific conversion（示範）" : "新增 customer qualification（示範）"}</p>
                <button aria-label="關閉表單" className="text-textSecondary" onClick={closeForm} type="button"><X className="h-4 w-4" /></button>
              </div>
              {formMode === "conversion" ? (
                <form className="mt-3 space-y-3" onSubmit={submitConversion}>
                  <div className="grid gap-3 sm:grid-cols-2">
                    <label className="text-xs text-textSecondary">來源 Item UOM<select className="mt-1 h-10 w-full rounded-input border border-border bg-white px-2 text-sm text-textPrimary" onChange={(event) => setConversionDraft({ ...conversionDraft, fromItemUomId: event.target.value })} value={conversionDraft.fromItemUomId}>{data.itemUoms.map((uom) => <option key={uom.id} value={uom.id}>{uom.label} ({uom.code})</option>)}</select></label>
                    <label className="text-xs text-textSecondary">目的 Item UOM<select className="mt-1 h-10 w-full rounded-input border border-border bg-white px-2 text-sm text-textPrimary" onChange={(event) => setConversionDraft({ ...conversionDraft, toItemUomId: event.target.value })} value={conversionDraft.toItemUomId}>{data.itemUoms.map((uom) => <option key={uom.id} value={uom.id}>{uom.label} ({uom.code})</option>)}</select></label>
                  </div>
                  <div className="grid gap-3 sm:grid-cols-2">
                    <label className="text-xs text-textSecondary">轉換類型<select className="mt-1 h-10 w-full rounded-input border border-border bg-white px-2 text-sm text-textPrimary" onChange={(event) => setConversionDraft({ ...conversionDraft, conversionType: event.target.value as C2ConversionDraft["conversionType"], conversionFactor: event.target.value === "CATCH_WEIGHT" ? "" : conversionDraft.conversionFactor })} value={conversionDraft.conversionType}><option value="FIXED">FIXED</option><option value="CATCH_WEIGHT">CATCH_WEIGHT</option></select></label>
                    <label className="text-xs text-textSecondary">Conversion factor（FIXED）<input className="mt-1 h-10 w-full rounded-input border border-border px-2 text-sm text-textPrimary" disabled={conversionDraft.conversionType === "CATCH_WEIGHT"} onChange={(event) => setConversionDraft({ ...conversionDraft, conversionFactor: event.target.value })} value={conversionDraft.conversionFactor} /></label>
                  </div>
                  <div className="grid gap-3 sm:grid-cols-2">
                    <label className="text-xs text-textSecondary">生效時間<input className="mt-1 h-10 w-full rounded-input border border-border px-2 text-sm text-textPrimary" onChange={(event) => setConversionDraft({ ...conversionDraft, effectiveFrom: event.target.value })} type="datetime-local" value={conversionDraft.effectiveFrom} /></label>
                    <label className="text-xs text-textSecondary">來源參照<input className="mt-1 h-10 w-full rounded-input border border-border px-2 text-sm text-textPrimary" onChange={(event) => setConversionDraft({ ...conversionDraft, sourceReference: event.target.value })} value={conversionDraft.sourceReference} /></label>
                  </div>
                  <button className="h-10 rounded-button bg-primary px-3 text-sm font-medium text-white" type="submit">執行示範驗證</button>
                </form>
              ) : (
                <form className="mt-3 space-y-3" onSubmit={submitQualification}>
                  <div className="grid gap-3 sm:grid-cols-2">
                    <label className="text-xs text-textSecondary">Customer reference<input className="mt-1 h-10 w-full rounded-input border border-border px-2 text-sm text-textPrimary" onChange={(event) => setQualificationDraft({ ...qualificationDraft, customerRef: event.target.value })} value={qualificationDraft.customerRef} /></label>
                    <label className="text-xs text-textSecondary">Approval scope<select className="mt-1 h-10 w-full rounded-input border border-border bg-white px-2 text-sm text-textPrimary" onChange={(event) => setQualificationDraft({ ...qualificationDraft, approvalScope: event.target.value as C2CustomerQualificationDraft["approvalScope"], supplierQualificationId: event.target.value === "ANY_GENERAL_QUALIFIED_SUPPLIER" ? "" : qualificationDraft.supplierQualificationId })} value={qualificationDraft.approvalScope}><option value="ANY_GENERAL_QUALIFIED_SUPPLIER">ANY_GENERAL_QUALIFIED_SUPPLIER</option><option value="SPECIFIC_SUPPLIER">SPECIFIC_SUPPLIER</option></select></label>
                  </div>
                  <div className="grid gap-3 sm:grid-cols-2">
                    <label className="text-xs text-textSecondary">Supplier qualification（指定供應商時必填）<input className="mt-1 h-10 w-full rounded-input border border-border px-2 text-sm text-textPrimary" disabled={qualificationDraft.approvalScope === "ANY_GENERAL_QUALIFIED_SUPPLIER"} onChange={(event) => setQualificationDraft({ ...qualificationDraft, supplierQualificationId: event.target.value })} value={qualificationDraft.supplierQualificationId} /></label>
                    <label className="text-xs text-textSecondary">供應方式<input className="mt-1 h-10 w-full rounded-input border border-border px-2 text-sm text-textPrimary" onChange={(event) => setQualificationDraft({ ...qualificationDraft, supplyMethod: event.target.value })} value={qualificationDraft.supplyMethod} /></label>
                  </div>
                  <div className="grid gap-3 sm:grid-cols-2">
                    <label className="text-xs text-textSecondary">生效時間<input className="mt-1 h-10 w-full rounded-input border border-border px-2 text-sm text-textPrimary" onChange={(event) => setQualificationDraft({ ...qualificationDraft, effectiveFrom: event.target.value })} type="datetime-local" value={qualificationDraft.effectiveFrom} /></label>
                    <label className="text-xs text-textSecondary">來源參照<input className="mt-1 h-10 w-full rounded-input border border-border px-2 text-sm text-textPrimary" onChange={(event) => setQualificationDraft({ ...qualificationDraft, sourceReference: event.target.value })} value={qualificationDraft.sourceReference} /></label>
                  </div>
                  <button className="h-10 rounded-button bg-primary px-3 text-sm font-medium text-white" type="submit">執行示範驗證</button>
                </form>
              )}
              <FormErrors errors={formErrors} />
              {formMessage ? <p className="mt-3 flex items-start gap-2 rounded-md border border-success/20 bg-success/10 px-3 py-2 text-sm text-success"><CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0" />{formMessage}</p> : null}
            </div>
          ) : null}
        </div>
      ) : null}
    </section>
  );
}
