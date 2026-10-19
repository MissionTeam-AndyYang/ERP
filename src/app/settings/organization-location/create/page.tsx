"use client";

import Link from "next/link";
import { ArrowLeft, CircleAlert } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { AppLayout } from "@/layouts/app-layout";
import { fm01ErrorText, fm01Text } from "@/i18n/fm01-copy";
import { getFm01Hierarchy, Fm01ApiError } from "@/services/fm01-organization-location-api";
import {
  fm01ParentFor,
  fm01ResourceLabels,
  fm01Resources,
  type Fm01Hierarchy,
  type Fm01Resource
} from "@/types/fm01-organization-location";

type FieldErrors = Partial<Record<"ref" | "displayName" | "parent", string>>;

export default function OrganizationLocationCreatePage() {
  const [resource, setResource] = useState<Fm01Resource>("legal-entities");
  const [ref, setRef] = useState("");
  const [displayName, setDisplayName] = useState("");
  const [parentId, setParentId] = useState("");
  const [parentQuery, setParentQuery] = useState("");
  const [hierarchy, setHierarchy] = useState<Fm01Hierarchy | null>(null);
  const [reload, setReload] = useState(0);
  const [isLoading, setIsLoading] = useState(true);
  const [loadError, setLoadError] = useState<Fm01ApiError>();
  const [fieldErrors, setFieldErrors] = useState<FieldErrors>({});
  const [showSummary, setShowSummary] = useState(false);
  const refRef = useRef<HTMLInputElement>(null);
  const nameRef = useRef<HTMLInputElement>(null);
  const parentRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    let active = true;
    setIsLoading(true);
    getFm01Hierarchy()
      .then((data) => { if (active) { setHierarchy(data); setLoadError(undefined); } })
      .catch((error: unknown) => {
        if (active) setLoadError(error instanceof Fm01ApiError ? error : new Fm01ApiError("REQUEST_FAILED", undefined));
      })
      .finally(() => { if (active) setIsLoading(false); });
    return () => { active = false; };
  }, [reload]);

  const parentResource = fm01ParentFor[resource];
  const parentOptions = parentResource ? hierarchy?.[parentResource] ?? [] : [];
  const loadMessage = loadError ? fm01ErrorText(loadError.code, loadError.status, loadError.correlationId) : "";

  function validate() {
    const errors: FieldErrors = {};
    if (!ref.trim()) errors.ref = fm01Text("create.required");
    if (!displayName.trim()) errors.displayName = fm01Text("create.required");
    if (parentResource && !parentId) errors.parent = fm01Text("create.required");
    if (parentResource && parentOptions.length === 0 && !loadError) errors.parent = fm01Text("create.parentLoadError");
    setFieldErrors(errors);
    setShowSummary(Object.keys(errors).length > 0);

    const firstInvalid = errors.ref ? refRef.current : errors.displayName ? nameRef.current : errors.parent ? parentRef.current : null;
    firstInvalid?.focus();
  }

  return (
    <AppLayout activePath="/settings" title={fm01Text("create.title")} site={fm01Text("settings.title")}>
      <div className="mx-auto max-w-4xl space-y-5">
        <nav aria-label="頁面路徑" className="flex items-center gap-2 text-sm text-textSecondary">
          <Link href="/settings/organization-location" className="inline-flex min-h-9 items-center gap-2 rounded-button hover:text-primary focus-visible:outline focus-visible:outline-2 focus-visible:outline-primary">
            <ArrowLeft className="h-4 w-4" aria-hidden="true" />{fm01Text("create.cancel")}
          </Link>
          <span aria-hidden="true">/</span>
          <span aria-current="page">{fm01Text("create.title")}</span>
        </nav>

        <header>
          <h2 className="text-xl font-semibold text-textPrimary">{fm01Text("create.title")}</h2>
          <p className="mt-1 text-sm text-textSecondary">{fm01Text("create.description")}</p>
        </header>

        <section className="rounded-card border border-border bg-white p-5 shadow-card md:p-6">
          {showSummary && (
            <div className="mb-5 rounded-card border border-danger/30 bg-red-50 p-4" role="alert" aria-labelledby="fm01-create-summary">
              <h3 id="fm01-create-summary" className="text-sm font-semibold text-textPrimary">{fm01Text("create.validationTitle")}</h3>
              <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-danger">
                {fieldErrors.ref && <li>{fm01Text("create.reference")}: {fieldErrors.ref}</li>}
                {fieldErrors.displayName && <li>{fm01Text("create.name")}: {fieldErrors.displayName}</li>}
                {fieldErrors.parent && <li>{fm01Text("create.parent")}: {fieldErrors.parent}</li>}
              </ul>
            </div>
          )}

          <div className="grid grid-cols-1 gap-x-6 gap-y-5 md:grid-cols-2">
            <div>
              <label htmlFor="fm01-create-resource" className="block text-sm font-medium text-textPrimary">{fm01Text("create.entityType")}</label>
              <select
                id="fm01-create-resource"
                value={resource}
                onChange={(event) => { setResource(event.target.value as Fm01Resource); setParentId(""); setParentQuery(""); setFieldErrors({}); setShowSummary(false); }}
                className="mt-2 h-11 w-full rounded-input border border-border bg-white px-3 text-sm text-textPrimary outline-none focus:border-primary focus:ring-2 focus:ring-primary/20"
              >
                {fm01Resources.map((item) => <option key={item} value={item}>{fm01ResourceLabels[item]}</option>)}
              </select>
            </div>

            <div>
              <label htmlFor="fm01-create-ref" className="block text-sm font-medium text-textPrimary">{fm01Text("create.reference")} <span aria-hidden="true" className="text-danger">*</span></label>
              <input
                ref={refRef}
                id="fm01-create-ref"
                value={ref}
                onChange={(event) => { setRef(event.target.value); setFieldErrors((current) => ({ ...current, ref: undefined })); }}
                aria-invalid={Boolean(fieldErrors.ref)}
                aria-describedby={fieldErrors.ref ? "fm01-create-ref-error" : "fm01-create-ref-help"}
                className="mt-2 h-11 w-full rounded-input border border-border px-3 text-sm text-textPrimary outline-none focus:border-primary focus:ring-2 focus:ring-primary/20"
              />
              {fieldErrors.ref ? <p id="fm01-create-ref-error" className="mt-1 text-sm text-danger">{fieldErrors.ref}</p> : <p id="fm01-create-ref-help" className="mt-1 text-xs text-textSecondary">重複性需由正式建立流程確認。</p>}
            </div>

            <div className="md:col-span-2">
              <label htmlFor="fm01-create-name" className="block text-sm font-medium text-textPrimary">{fm01Text("create.name")} <span aria-hidden="true" className="text-danger">*</span></label>
              <input
                ref={nameRef}
                id="fm01-create-name"
                value={displayName}
                onChange={(event) => { setDisplayName(event.target.value); setFieldErrors((current) => ({ ...current, displayName: undefined })); }}
                aria-invalid={Boolean(fieldErrors.displayName)}
                aria-describedby={fieldErrors.displayName ? "fm01-create-name-error" : undefined}
                className="mt-2 h-11 w-full rounded-input border border-border px-3 text-sm text-textPrimary outline-none focus:border-primary focus:ring-2 focus:ring-primary/20"
              />
              {fieldErrors.displayName && <p id="fm01-create-name-error" className="mt-1 text-sm text-danger">{fieldErrors.displayName}</p>}
            </div>

            {parentResource && (
              <div className="md:col-span-2">
                <label htmlFor="fm01-create-parent" className="block text-sm font-medium text-textPrimary">{fm01Text("create.parent")} <span aria-hidden="true" className="text-danger">*</span></label>
                <input
                  ref={parentRef}
                  id="fm01-create-parent"
                  list="fm01-create-parent-options"
                  value={parentQuery}
                  onChange={(event) => {
                    const value = event.target.value;
                    const selected = parentOptions.find((item) => `${item.ref} · ${item.displayName}` === value);
                    setParentQuery(value);
                    setParentId(selected ? String(selected.id) : "");
                    setFieldErrors((current) => ({ ...current, parent: undefined }));
                  }}
                  disabled={isLoading || Boolean(loadError) || parentOptions.length === 0}
                  aria-invalid={Boolean(fieldErrors.parent)}
                  aria-describedby={fieldErrors.parent ? "fm01-create-parent-error" : "fm01-create-parent-help"}
                  aria-required="true"
                  placeholder={isLoading ? fm01Text("page.loading") : fm01Text("create.parentChoose")}
                  className="mt-2 h-11 w-full rounded-input border border-border bg-white px-3 text-sm text-textPrimary outline-none focus:border-primary focus:ring-2 focus:ring-primary/20 disabled:cursor-not-allowed disabled:bg-slate-100"
                />
                <datalist id="fm01-create-parent-options">
                  {parentOptions.map((item) => <option key={item.id} value={`${item.ref} · ${item.displayName}`} />)}
                </datalist>
                {fieldErrors.parent ? <p id="fm01-create-parent-error" className="mt-1 text-sm text-danger">{fieldErrors.parent}</p> : <p id="fm01-create-parent-help" className="mt-1 text-xs text-textSecondary">從清單選取上層；目前無法確認該資料是否啟用或可供新建使用。</p>}
              </div>
            )}

            {resource === "warehouses" && (
              <div className="md:col-span-2">
                <label htmlFor="fm01-create-plant" className="block text-sm font-medium text-textPrimary">{fm01Text("create.plant")}</label>
                <select id="fm01-create-plant" disabled className="mt-2 h-11 w-full cursor-not-allowed rounded-input border border-border bg-slate-100 px-3 text-sm text-textSecondary">
                  <option>未提供可驗證的同廠區選項</option>
                </select>
                <p className="mt-1 text-xs text-textSecondary">{fm01Text("create.plantUnavailable")}</p>
              </div>
            )}
          </div>

          {loadError && (
            <div className="mt-5 flex gap-3 rounded-card border border-danger/30 bg-red-50 p-4" role="alert">
              <CircleAlert className="mt-0.5 h-4 w-4 shrink-0 text-danger" aria-hidden="true" />
              <div><p className="text-sm font-medium text-textPrimary">{fm01Text("create.parentLoadError")}</p><p className="mt-1 text-sm text-textSecondary">{loadMessage}</p><button type="button" onClick={() => setReload((value) => value + 1)} className="mt-2 min-h-9 text-sm font-medium text-primary focus-visible:outline focus-visible:outline-2 focus-visible:outline-primary">{fm01Text("page.retry")}</button></div>
            </div>
          )}

          <div className="mt-6 rounded-card border border-warning/40 bg-amber-50 p-4" role="status">
            <p className="text-sm font-medium text-textPrimary">{fm01Text("create.submitDisabled")}</p>
            <p className="mt-1 text-xs leading-5 text-textSecondary">輸入內容只保留於目前畫面，不會送往伺服器或建立任何資料紀錄。</p>
          </div>

          <div className="mt-6 flex flex-wrap justify-end gap-2 border-t border-border pt-4">
            <Link href="/settings/organization-location" className="inline-flex min-h-11 items-center justify-center rounded-button border border-border px-4 text-sm font-medium text-textPrimary hover:bg-slate-50 focus-visible:outline focus-visible:outline-2 focus-visible:outline-primary">{fm01Text("edit.cancel")}</Link>
            <button type="button" onClick={validate} className="min-h-11 rounded-button border border-border px-4 text-sm font-medium text-textPrimary hover:bg-slate-50 focus-visible:outline focus-visible:outline-2 focus-visible:outline-primary">{fm01Text("create.check")}</button>
            <button type="button" disabled aria-describedby="fm01-create-disabled" className="min-h-11 cursor-not-allowed rounded-button bg-slate-200 px-4 text-sm font-semibold text-slate-500">{fm01Text("create.submit")}</button>
            <span id="fm01-create-disabled" className="sr-only">{fm01Text("create.submitDisabled")}</span>
          </div>
        </section>
      </div>
    </AppLayout>
  );
}
