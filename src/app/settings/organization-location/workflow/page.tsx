"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { ArrowLeft, CircleAlert, LockKeyhole } from "lucide-react";
import { AppLayout } from "@/layouts/app-layout";
import { fm01ErrorText, fm01Text } from "@/i18n/fm01-copy";
import { getFm01Record, Fm01ApiError } from "@/services/fm01-organization-location-api";
import {
  fm01ResourceLabels,
  fm01Resources,
  type Fm01Record,
  type Fm01Resource
} from "@/types/fm01-organization-location";

type WorkflowOperation = "deactivate" | "reactivate";
type WorkflowTab = "overview" | "approval" | "audit";

function validResource(value: string | null): value is Fm01Resource {
  return value !== null && fm01Resources.includes(value as Fm01Resource);
}

export default function OrganizationLocationWorkflowPage() {
  const [record, setRecord] = useState<Fm01Record | null>(null);
  const [operation, setOperation] = useState<WorkflowOperation>("deactivate");
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<Fm01ApiError>();
  const [tab, setTab] = useState<WorkflowTab>("overview");
  const [reason, setReason] = useState("");
  const [evidence, setEvidence] = useState("");

  useEffect(() => {
    let active = true;
    const params = new URLSearchParams(window.location.search);
    const resource = params.get("resource");
    const idValue = Number(params.get("id"));
    const requestedOperation = params.get("operation");

    if (!validResource(resource) || !Number.isInteger(idValue) || idValue < 1 || !["deactivate", "reactivate"].includes(requestedOperation ?? "")) {
      setError(new Fm01ApiError("INVALID_ROUTE", undefined));
      setIsLoading(false);
      return () => { active = false; };
    }

    setOperation(requestedOperation as WorkflowOperation);
    getFm01Record(resource, idValue)
      .then((data) => { if (active) setRecord(data); })
      .catch((caught: unknown) => {
        if (active) setError(caught instanceof Fm01ApiError ? caught : new Fm01ApiError("REQUEST_FAILED", undefined));
      })
      .finally(() => { if (active) setIsLoading(false); });

    return () => { active = false; };
  }, []);

  const operationLabel = operation === "deactivate" ? fm01Text("workflow.deactivate") : fm01Text("workflow.reactivate");

  return (
    <AppLayout activePath="/settings" title={fm01Text("workflow.title")} site={fm01Text("settings.title")}>
      <div className="mx-auto max-w-4xl space-y-5">
        <nav aria-label="頁面路徑" className="flex items-center gap-2 text-sm text-textSecondary">
          <Link href="/settings/organization-location" className="inline-flex min-h-9 items-center gap-2 rounded-button hover:text-primary focus-visible:outline focus-visible:outline-2 focus-visible:outline-primary">
            <ArrowLeft className="h-4 w-4" aria-hidden="true" />{fm01Text("page.title")}
          </Link>
          <span aria-hidden="true">/</span>
          <span aria-current="page">{fm01Text("workflow.title")}</span>
        </nav>

        <header>
          <h2 className="text-xl font-semibold text-textPrimary">{fm01Text("workflow.title")}</h2>
          <p className="mt-1 text-sm leading-6 text-textSecondary">{fm01Text("workflow.description")}</p>
        </header>

        {isLoading && (
          <section className="rounded-card border border-border bg-white p-5 shadow-card" aria-busy="true">
            <div className="h-5 w-48 animate-pulse rounded bg-slate-200" />
            <div className="mt-4 h-4 w-2/3 animate-pulse rounded bg-slate-100" />
            <span className="sr-only">{fm01Text("page.loading")}</span>
          </section>
        )}

        {error && (
          <section className="rounded-card border border-danger/30 bg-red-50 p-4" role="alert">
            <div className="flex gap-3">
              <CircleAlert className="mt-0.5 h-5 w-5 shrink-0 text-danger" aria-hidden="true" />
              <div><h3 className="text-sm font-semibold text-textPrimary">{fm01Text("page.errorTitle")}</h3><p className="mt-1 text-sm text-textSecondary">{fm01ErrorText(error.code, error.status, error.correlationId)}</p></div>
            </div>
          </section>
        )}

        {!isLoading && !error && record && (
          <>
            <section className="rounded-card border border-border bg-white shadow-card" aria-labelledby="fm01-workflow-target">
              <div className="border-b border-border px-5 py-4">
                <p className="text-xs font-medium text-textSecondary">{operationLabel}</p>
                <h3 id="fm01-workflow-target" className="mt-1 break-words text-lg font-semibold text-textPrimary">{record.displayName || "（名稱未提供）"}</h3>
                <p className="mt-1 text-sm text-textSecondary">{fm01ResourceLabels[record.resource]} · {record.ref || `ID ${record.id}`}</p>
              </div>

              <div className="border-b border-border px-4 py-3">
                <div role="tablist" aria-label="受控流程內容" className="flex flex-wrap gap-2">
                  {(["overview", "approval", "audit"] as const).map((item) => {
                    const label = item === "overview" ? "流程概要" : item === "approval" ? fm01Text("workflow.approval") : fm01Text("workflow.audit");
                    return <button key={item} type="button" role="tab" aria-selected={tab === item} onClick={() => setTab(item)} className={`min-h-10 rounded-button px-3 text-sm font-medium focus-visible:outline focus-visible:outline-2 focus-visible:outline-primary ${tab === item ? "bg-primary text-white" : "text-textSecondary hover:bg-slate-50"}`}>{label}</button>;
                  })}
                </div>
              </div>

              <div className="space-y-5 p-5">
                {tab === "overview" && (
                  <>
                    <div className="rounded-card border border-warning/40 bg-amber-50 p-4" role="status">
                      <div className="flex gap-3">
                        <LockKeyhole className="mt-0.5 h-5 w-5 shrink-0 text-amber-700" aria-hidden="true" />
                        <div><h4 className="text-sm font-semibold text-textPrimary">{fm01Text("workflow.allDisabled")}</h4><p className="mt-1 text-xs leading-5 text-textSecondary">目前為唯讀流程介面；本頁不會建立申請，也不會改變啟用狀態。</p></div>
                      </div>
                    </div>

                    <div>
                      <h4 className="text-sm font-semibold text-textPrimary">{fm01Text("workflow.steps")}</h4>
                      <ol className="mt-3 grid grid-cols-1 gap-3 sm:grid-cols-2">
                        {[fm01Text("workflow.stepReview"), fm01Text("workflow.stepChecks"), fm01Text("workflow.stepApproval"), fm01Text("workflow.stepExecution")].map((step, index) => (
                          <li key={step} className="flex min-h-16 items-center gap-3 rounded-card border border-border p-3">
                            <span className="grid h-8 w-8 shrink-0 place-items-center rounded-full bg-slate-100 text-sm font-semibold text-textSecondary">{index + 1}</span>
                            <span className="min-w-0"><span className="block text-sm font-medium text-textPrimary">{step}</span><span className="mt-0.5 block text-xs text-textSecondary">{fm01Text("workflow.notStarted")}</span></span>
                          </li>
                        ))}
                      </ol>
                    </div>

                    <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
                      <div>
                        <label htmlFor="fm01-workflow-reason" className="block text-sm font-medium text-textPrimary">{fm01Text("workflow.reason")}</label>
                        <textarea id="fm01-workflow-reason" value={reason} onChange={(event) => setReason(event.target.value)} rows={3} className="mt-2 w-full rounded-input border border-border bg-white p-3 text-sm text-textPrimary outline-none focus:border-primary focus:ring-2 focus:ring-primary/20" aria-describedby="fm01-workflow-local-draft" />
                      </div>
                      <div>
                        <label htmlFor="fm01-workflow-evidence" className="block text-sm font-medium text-textPrimary">{fm01Text("workflow.evidence")}</label>
                        <input id="fm01-workflow-evidence" value={evidence} onChange={(event) => setEvidence(event.target.value)} className="mt-2 h-11 w-full rounded-input border border-border px-3 text-sm text-textPrimary outline-none focus:border-primary focus:ring-2 focus:ring-primary/20" aria-describedby="fm01-workflow-local-draft" />
                      </div>
                    </div>
                    <p id="fm01-workflow-local-draft" className="text-xs text-textSecondary">原因與佐證僅為本機草稿，離開頁面即不保留；不會送出或建立紀錄。</p>
                  </>
                )}

                {tab === "approval" && <div className="rounded-card border border-border bg-slate-50 p-5"><h4 className="text-sm font-semibold text-textPrimary">{fm01Text("workflow.approval")}</h4><p className="mt-2 text-sm text-textSecondary">{fm01Text("workflow.approvalUnavailable")}</p></div>}
                {tab === "audit" && <div className="rounded-card border border-border bg-slate-50 p-5"><h4 className="text-sm font-semibold text-textPrimary">{fm01Text("workflow.audit")}</h4><p className="mt-2 text-sm text-textSecondary">{fm01Text("workflow.auditUnavailable")}</p></div>}
              </div>

              <div className="flex flex-wrap justify-end gap-2 border-t border-border p-4">
                <Link href="/settings/organization-location" className="inline-flex min-h-11 items-center justify-center rounded-button border border-border px-4 text-sm font-medium text-textPrimary hover:bg-slate-50 focus-visible:outline focus-visible:outline-2 focus-visible:outline-primary">{fm01Text("create.cancel")}</Link>
                <button type="button" disabled aria-describedby="fm01-workflow-disabled" className="min-h-11 cursor-not-allowed rounded-button bg-slate-200 px-4 text-sm font-semibold text-slate-500">{fm01Text("workflow.submit")}</button>
                <button type="button" disabled aria-describedby="fm01-workflow-disabled" className="min-h-11 cursor-not-allowed rounded-button border border-border px-4 text-sm font-medium text-slate-500">{fm01Text("workflow.approve")}</button>
                <button type="button" disabled aria-describedby="fm01-workflow-disabled" className="min-h-11 cursor-not-allowed rounded-button border border-border px-4 text-sm font-medium text-slate-500">{fm01Text("workflow.reject")}</button>
                <span id="fm01-workflow-disabled" className="sr-only">{fm01Text("workflow.allDisabled")}</span>
              </div>
            </section>

          <p className="text-xs leading-5 text-textSecondary">目前資料包含識別、名稱及關係；尚無狀態、版本、授權、核准、稽核或執行結果。</p>
          </>
        )}
      </div>
    </AppLayout>
  );
}
