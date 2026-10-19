"use client";

import { useEffect, useRef, useState } from "react";
import { X } from "lucide-react";
import { fm01Text } from "@/i18n/fm01-copy";
import { getFm01RelationRows } from "@/components/fm01/organization-location/detail-panel";
import { fm01ResourceLabels, type Fm01Hierarchy, type Fm01Record } from "@/types/fm01-organization-location";

type EditDrawerProps = {
  record: Fm01Record | null;
  hierarchy?: Fm01Hierarchy;
  onClose: () => void;
};

export function EditDrawer({ record, hierarchy, onClose }: EditDrawerProps) {
  const [draft, setDraft] = useState("");
  const [validationMessage, setValidationMessage] = useState("");
  const panelRef = useRef<HTMLElement>(null);

  useEffect(() => {
    setDraft(record?.displayName ?? "");
    setValidationMessage("");
  }, [record]);

  useEffect(() => {
    if (!record) return;
    const previousFocus = document.activeElement instanceof HTMLElement ? document.activeElement : null;
    const panel = panelRef.current;
    const firstInput = panel?.querySelector<HTMLElement>("input, button:not([disabled])");
    firstInput?.focus();

    function handleKeyDown(event: KeyboardEvent) {
      if (event.key === "Escape") {
        event.preventDefault();
        onClose();
        return;
      }
      if (event.key !== "Tab" || !panel) return;
      const controls = Array.from(panel.querySelectorAll<HTMLElement>('button:not([disabled]), input:not([disabled]), a[href]'));
      if (controls.length === 0) return;
      const first = controls[0];
      const last = controls[controls.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    }

    document.addEventListener("keydown", handleKeyDown);
    return () => {
      document.removeEventListener("keydown", handleKeyDown);
      previousFocus?.focus();
    };
  }, [record, onClose]);

  if (!record) return null;
  const relations = getFm01RelationRows(record, hierarchy);

  function validateDraft() {
    setValidationMessage(draft.trim() ? "" : fm01Text("edit.invalid"));
  }

  return (
      <div className="fixed inset-0 z-30 flex justify-end">
      <button type="button" aria-label={fm01Text("edit.cancel")} onClick={onClose} className="absolute inset-0 z-0 cursor-default bg-slate-950/40" />
      <aside
        ref={panelRef}
        role="dialog"
        aria-modal="true"
        aria-labelledby="fm01-edit-title"
        className="relative z-10 flex h-full w-full max-w-xl flex-col overflow-y-auto border-l border-border bg-white shadow-card"
      >
        <div className="flex items-start justify-between gap-4 border-b border-border px-5 py-4">
          <div>
            <p className="text-xs font-medium text-textSecondary">{record.ref}</p>
            <h2 id="fm01-edit-title" className="mt-1 text-lg font-semibold text-textPrimary">{fm01Text("edit.title")}</h2>
          </div>
          <button
            type="button"
            onClick={onClose}
            aria-label={fm01Text("error.dismiss")}
            className="grid h-11 w-11 shrink-0 place-items-center rounded-button border border-border text-textSecondary hover:bg-slate-50 focus-visible:outline focus-visible:outline-2 focus-visible:outline-primary"
          >
            <X className="h-5 w-5" aria-hidden="true" />
          </button>
        </div>

        <div className="flex-1 space-y-6 p-5">
          <p className="text-sm leading-6 text-textSecondary">{fm01Text("edit.description")}</p>
          <dl className="grid grid-cols-1 gap-4 rounded-card border border-border bg-slate-50 p-4 sm:grid-cols-2">
            <div><dt className="text-xs text-textSecondary">資料類型</dt><dd className="mt-1 text-sm text-textPrimary">{fm01ResourceLabels[record.resource]}</dd></div>
            <div><dt className="text-xs text-textSecondary">系統編號</dt><dd className="mt-1 text-sm text-textPrimary">{record.id}</dd></div>
            <div className="sm:col-span-2"><dt className="text-xs text-textSecondary">參照代碼（唯讀）</dt><dd className="mt-1 break-all text-sm text-textPrimary">{record.ref}</dd></div>
            {relations.map((relation) => <div key={relation.label} className="sm:col-span-2"><dt className="text-xs text-textSecondary">{relation.label}（唯讀）</dt><dd className="mt-1 break-words text-sm text-textPrimary">{relation.value}</dd></div>)}
          </dl>

          <div>
            <label htmlFor="fm01-display-name" className="block text-sm font-medium text-textPrimary">{fm01Text("detail.displayName")} <span aria-hidden="true" className="text-danger">*</span></label>
            <input
              id="fm01-display-name"
              value={draft}
              onChange={(event) => { setDraft(event.target.value); setValidationMessage(""); }}
              aria-invalid={Boolean(validationMessage)}
              aria-describedby={validationMessage ? "fm01-edit-error" : "fm01-edit-help"}
              className="mt-2 h-11 w-full rounded-input border border-border bg-white px-3 text-sm text-textPrimary outline-none focus:border-primary focus:ring-2 focus:ring-primary/20"
            />
            {validationMessage ? (
              <p id="fm01-edit-error" className="mt-2 text-sm text-danger" role="alert">{validationMessage}</p>
            ) : (
              <p id="fm01-edit-help" className="mt-2 text-xs leading-5 text-textSecondary">只在本機保留草稿，不會變更後端資料。</p>
            )}
            <button type="button" onClick={validateDraft} className="mt-3 min-h-11 rounded-button border border-border px-3 text-sm font-medium text-textPrimary hover:bg-slate-50 focus-visible:outline focus-visible:outline-2 focus-visible:outline-primary">{fm01Text("create.check")}</button>
          </div>

          <div className="rounded-card border border-warning/40 bg-amber-50 p-4" role="status">
            <p className="text-sm font-medium text-textPrimary">{fm01Text("edit.disabled")}</p>
            <p className="mt-1 text-xs leading-5 text-textSecondary">更新必須先具備版本檢查、獨立核准與稽核紀錄，目前尚未具備。</p>
          </div>
        </div>

        <div className="flex justify-end gap-2 border-t border-border p-4">
          <button type="button" onClick={onClose} className="min-h-11 rounded-button border border-border px-4 text-sm font-medium text-textPrimary hover:bg-slate-50 focus-visible:outline focus-visible:outline-2 focus-visible:outline-primary">{fm01Text("edit.cancel")}</button>
          <button type="button" disabled aria-describedby="fm01-edit-disabled" className="min-h-11 cursor-not-allowed rounded-button bg-slate-200 px-4 text-sm font-semibold text-slate-500">{fm01Text("edit.save")}</button>
          <span id="fm01-edit-disabled" className="sr-only">{fm01Text("edit.disabled")}</span>
        </div>
      </aside>
    </div>
  );
}
