"use client";

import Link from "next/link";
import { ArrowUpRight, CircleHelp, PencilLine } from "lucide-react";
import { StatusBadge } from "@/components/ui/status-badge";
import { fm01ErrorText, fm01Text } from "@/i18n/fm01-copy";
import {
  fm01ResourceLabels,
  type Fm01Hierarchy,
  type Fm01Record,
  type Fm01Resource
} from "@/types/fm01-organization-location";
import { Fm01ApiError } from "@/services/fm01-organization-location-api";

type RelationRow = { label: string; value: string };

export function getFm01RelationRows(record: Fm01Record, hierarchy?: Fm01Hierarchy): RelationRow[] {
  const lookup = (resource: Fm01Resource, id: number | null | undefined) => {
    if (id == null) return "未提供";
    const related = hierarchy?.[resource].find((item) => item.id === id);
    return related ? `${related.ref || `ID ${id}`} · ${related.displayName || "名稱未提供"}` : `ID ${id}`;
  };

  switch (record.resource) {
    case "legal-entities":
      return [];
    case "companies":
      return [{ label: "所屬法人", value: lookup("legal-entities", record.relations.legal_entity_id) }];
    case "sites":
      return [{ label: "所屬公司", value: lookup("companies", record.relations.company_id) }];
    case "plants":
      return [{ label: "所屬廠區", value: lookup("sites", record.relations.site_id) }];
    case "warehouses": {
      const plantId = record.relations.plant_id;
      const plant = plantId == null ? undefined : hierarchy?.plants.find((item) => item.id === plantId);
      const sameSite = plant && record.relations.site_id != null && plant.relations.site_id === record.relations.site_id;
      return [
        { label: "所屬廠區", value: lookup("sites", record.relations.site_id) },
        {
          label: fm01Text("detail.plantAssociation"),
          value: plantId == null
            ? "未提供"
            : sameSite
              ? `${plant.ref || `ID ${plantId}`} · ${plant.displayName || "名稱未提供"}`
              : `ID ${plantId}（無法確認同廠區）`
        }
      ];
    }
    case "locations":
      return [
        { label: "所屬倉庫", value: lookup("warehouses", record.relations.warehouse_id) },
        { label: fm01Text("detail.parentLocation"), value: record.relations.parent_location_id == null ? "未提供" : `ID ${record.relations.parent_location_id}` }
      ];
  }
}

function WorkflowLink({ record, operation }: { record: Fm01Record; operation: "deactivate" | "reactivate" }) {
  const label = operation === "deactivate" ? "檢視停用流程設計" : "檢視重新啟用流程設計";
  const href = `/settings/organization-location/workflow?resource=${record.resource}&id=${record.id}&operation=${operation}`;
  return (
    <Link
      href={href}
      className="inline-flex min-h-11 items-center justify-center gap-2 rounded-button border border-border bg-white px-3 text-sm font-medium text-textPrimary hover:bg-slate-50 focus-visible:outline focus-visible:outline-2 focus-visible:outline-primary"
    >
      {label}
      <ArrowUpRight className="h-4 w-4" aria-hidden="true" />
    </Link>
  );
}

export type DetailPanelProps = {
  record: Fm01Record | null;
  hierarchy?: Fm01Hierarchy;
  isLoading: boolean;
  error?: Fm01ApiError;
  onRetry: () => void;
  onEdit: () => void;
};

export function DetailPanel({ record, hierarchy, isLoading, error, onRetry, onEdit }: DetailPanelProps) {
  if (isLoading) {
    return (
      <section className="rounded-card border border-border bg-white p-5 shadow-card" aria-busy="true">
        <div className="h-5 w-32 animate-pulse rounded bg-slate-200" />
        <div className="mt-5 space-y-3">
          <div className="h-4 animate-pulse rounded bg-slate-100" />
          <div className="h-4 w-3/4 animate-pulse rounded bg-slate-100" />
          <div className="h-4 w-1/2 animate-pulse rounded bg-slate-100" />
        </div>
        <span className="sr-only">{fm01Text("page.loading")}</span>
      </section>
    );
  }

  if (error) {
    return (
      <section className="rounded-card border border-danger/30 bg-white p-5 shadow-card" aria-live="polite">
        <h2 className="text-base font-semibold text-textPrimary">{fm01Text("detail.unavailable")}</h2>
        <p role="alert" className="mt-2 text-sm text-textSecondary">{fm01ErrorText(error.code, error.status)}</p>
        <button
          type="button"
          onClick={onRetry}
          className="mt-4 inline-flex min-h-11 items-center rounded-button bg-primary px-4 text-sm font-semibold text-white focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary"
        >
          {fm01Text("page.retry")}
        </button>
      </section>
    );
  }

  if (!record) {
    return (
      <section className="flex min-h-56 flex-col items-center justify-center rounded-card border border-border bg-white p-6 text-center shadow-card">
        <CircleHelp className="h-6 w-6 text-textSecondary" aria-hidden="true" />
        <h2 className="mt-3 text-base font-semibold text-textPrimary">{fm01Text("detail.title")}</h2>
        <p className="mt-1 text-sm text-textSecondary">{fm01Text("page.selectPrompt")}</p>
      </section>
    );
  }

  const relations = getFm01RelationRows(record, hierarchy);

  return (
    <section className="rounded-card border border-border bg-white shadow-card" aria-labelledby="fm01-detail-title">
      <div className="flex flex-wrap items-start justify-between gap-3 border-b border-border px-5 py-4">
        <div className="min-w-0">
          <p className="text-xs font-medium text-textSecondary">{fm01Text("detail.title")}</p>
          <h2 id="fm01-detail-title" className="mt-1 break-words text-lg font-semibold text-textPrimary">
            {record.displayName || "（名稱未提供）"}
          </h2>
          <p className="mt-1 text-sm text-textSecondary">{fm01ResourceLabels[record.resource]} · {record.ref || "（代碼未提供）"}</p>
        </div>
        <StatusBadge tone="neutral">{fm01Text("detail.statusUnavailable")}</StatusBadge>
      </div>

      <div className="space-y-5 p-5">
        <dl className="grid grid-cols-1 gap-x-5 gap-y-4 sm:grid-cols-2">
          <div>
            <dt className="text-xs font-medium text-textSecondary">{fm01Text("detail.entityType")}</dt>
            <dd className="mt-1 text-sm text-textPrimary">{fm01ResourceLabels[record.resource]}</dd>
          </div>
          <div>
            <dt className="text-xs font-medium text-textSecondary">{fm01Text("detail.identifier")}</dt>
            <dd className="mt-1 break-all text-sm text-textPrimary">{record.id}</dd>
          </div>
          <div>
            <dt className="text-xs font-medium text-textSecondary">{fm01Text("detail.reference")}</dt>
            <dd className="mt-1 break-all text-sm text-textPrimary">{record.ref || "未提供"}</dd>
          </div>
          <div>
            <dt className="text-xs font-medium text-textSecondary">{fm01Text("detail.displayName")}</dt>
            <dd className="mt-1 break-words text-sm text-textPrimary">{record.displayName || "未提供"}</dd>
          </div>
        </dl>

        {relations.length > 0 && (
          <div>
            <h3 className="text-sm font-semibold text-textPrimary">{fm01Text("detail.relationships")}</h3>
            <dl className="mt-3 divide-y divide-border rounded-card border border-border">
              {relations.map((relation) => (
                <div key={relation.label} className="grid grid-cols-1 gap-1 px-3 py-3 sm:grid-cols-[minmax(120px,0.45fr)_1fr] sm:gap-4">
                  <dt className="text-xs font-medium text-textSecondary">{relation.label}</dt>
                  <dd className="break-words text-sm text-textPrimary">{relation.value}</dd>
                </div>
              ))}
            </dl>
          </div>
        )}

        {record.resource === "warehouses" && (
          <p className="text-xs leading-5 text-textSecondary">目前只讀取到關聯值，尚未驗證關聯廠別是否位於同一廠區。</p>
        )}
        {record.resource === "locations" && (
          <p className="text-xs leading-5 text-textSecondary">庫位依所屬倉庫呈現，不展開庫位巢狀階層。</p>
        )}

        <div className="flex flex-wrap gap-2 border-t border-border pt-4">
          <button
            type="button"
            onClick={onEdit}
            className="inline-flex min-h-11 items-center justify-center gap-2 rounded-button bg-primary px-4 text-sm font-semibold text-white hover:bg-blue-700 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary"
          >
            <PencilLine className="h-4 w-4" aria-hidden="true" />
            {fm01Text("detail.edit")}
          </button>
          <WorkflowLink record={record} operation="deactivate" />
          <WorkflowLink record={record} operation="reactivate" />
        </div>
        <p className="text-xs leading-5 text-textSecondary">目前資料未包含狀態與操作授權；流程頁僅供檢視，不會執行變更。</p>
      </div>
    </section>
  );
}
