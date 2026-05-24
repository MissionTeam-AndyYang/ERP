"use client";

import { AlertTriangle, CalendarDays, Filter, IdCard, Search, UsersRound } from "lucide-react";
import { useMemo, useState } from "react";
import { StatusBadge } from "@/components/ui/status-badge";
import { useWorkforceDashboard } from "@/hooks/use-workforce-dashboard";
import { AppLayout } from "@/layouts/app-layout";
import type {
  WorkforceCase,
  WorkforceDashboardData,
  WorkforceRiskLevel,
  WorkforceSummary,
  WorkforceWorkspaceTab
} from "@/types/workforce";

const tabs: { id: WorkforceWorkspaceTab; label: string }[] = [
  { id: "coverage", label: "班表覆蓋" },
  { id: "skill-gap", label: "技能缺口" },
  { id: "overtime", label: "加班/支援" },
  { id: "certifications", label: "證照/複訓" }
];

const tabDescriptions: Record<WorkforceWorkspaceTab, string> = {
  coverage: "檢視今日各產線、倉庫、品保與物流的人員是否足夠。",
  "skill-gap": "追蹤技能是否符合預排工單、冷鏈配送與品質檢驗需求。",
  overtime: "檢視加班、跨線支援與晚班缺口，支援 Planning/Production 重排。",
  certifications: "追蹤證照、訓練與複訓到期，避免影響派工與派車。"
};

function riskTone(risk: WorkforceRiskLevel) {
  if (risk === "高風險") return "danger";
  if (risk === "注意") return "warning";
  return "success";
}

function getVisibleCases(activeTab: WorkforceWorkspaceTab, cases: WorkforceCase[]) {
  if (activeTab === "skill-gap") {
    return cases.filter((item) => item.skillCoverage !== "完整");
  }
  if (activeTab === "overtime") {
    return cases.filter((item) => item.overtimeHours > 0 || item.supportNeeded > 0);
  }
  if (activeTab === "certifications") {
    return cases.filter((item) => item.certificationIssue !== null);
  }
  return cases;
}

function KpiStrip({ summary }: { summary: WorkforceSummary[] }) {
  const icons = [UsersRound, AlertTriangle, IdCard, CalendarDays];

  return (
    <section className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
      {summary.map((item, index) => {
        const Icon = icons[index] ?? UsersRound;
        return (
          <div className="rounded-lg border border-border bg-white p-4 shadow-card" key={item.label}>
            <div className="flex items-start justify-between gap-3">
              <div>
                <p className="text-sm font-medium text-textSecondary">{item.label}</p>
                <p className="mt-2 text-2xl font-semibold text-textPrimary">{item.value}</p>
              </div>
              <span className="grid h-10 w-10 place-items-center rounded-full bg-slate-100 text-textSecondary">
                <Icon className="h-5 w-5" aria-hidden="true" />
              </span>
            </div>
            <p className="mt-3 text-xs leading-5 text-textSecondary">{item.hint}</p>
          </div>
        );
      })}
    </section>
  );
}

function WorkforceTable({
  activeTab,
  cases,
  selectedId,
  onSelect
}: {
  activeTab: WorkforceWorkspaceTab;
  cases: WorkforceCase[];
  selectedId: string;
  onSelect: (item: WorkforceCase) => void;
}) {
  const rows = useMemo(() => getVisibleCases(activeTab, cases), [activeTab, cases]);

  return (
    <div className="overflow-hidden rounded-lg border border-border bg-white shadow-card">
      <div className="overflow-x-auto">
        <table className="min-w-[1080px] w-full border-collapse text-sm">
          <thead className="bg-slate-50 text-left text-xs font-semibold uppercase tracking-wide text-textSecondary">
            <tr>
              <th className="px-4 py-3">區域 / 班別</th>
              <th className="px-4 py-3">關聯計劃</th>
              <th className="px-4 py-3 text-right">人力</th>
              <th className="px-4 py-3">技能</th>
              <th className="px-4 py-3">加班/支援</th>
              <th className="px-4 py-3">證照</th>
              <th className="px-4 py-3">風險</th>
              <th className="px-4 py-3">負責</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {rows.map((item) => {
              const isSelected = item.id === selectedId;
              return (
                <tr
                  className={`cursor-pointer transition ${isSelected ? "bg-info/10" : "hover:bg-slate-50"}`}
                  key={item.id}
                  onClick={() => onSelect(item)}
                >
                  <td className="px-4 py-3">
                    <p className="font-semibold text-textPrimary">{item.lineOrArea}</p>
                    <p className="mt-1 text-xs text-textSecondary">{item.department} · {item.shift}</p>
                  </td>
                  <td className="px-4 py-3">
                    <p className="text-textPrimary">{item.relatedPlan ?? "無"}</p>
                    <p className="mt-1 text-xs text-textSecondary">{item.relatedWorkOrder ?? "無工單"}</p>
                  </td>
                  <td className="px-4 py-3 text-right font-semibold text-textPrimary">
                    {item.assignedStaff} / {item.requiredStaff}
                  </td>
                  <td className="px-4 py-3">
                    <p className="text-textPrimary">{item.skillCoverage}</p>
                    <p className="mt-1 text-xs text-textSecondary">{item.skillRequired}</p>
                  </td>
                  <td className="px-4 py-3">
                    <p className="text-textPrimary">{item.overtimeHours} 小時</p>
                    <p className="mt-1 text-xs text-textSecondary">支援 {item.supportNeeded} 人</p>
                  </td>
                  <td className="px-4 py-3 text-textPrimary">{item.certificationIssue ?? "正常"}</td>
                  <td className="px-4 py-3">
                    <StatusBadge tone={riskTone(item.riskLevel)}>{item.riskLevel}</StatusBadge>
                    <p className="mt-1 line-clamp-2 text-xs text-textSecondary">{item.riskReason}</p>
                  </td>
                  <td className="px-4 py-3 text-textPrimary">{item.owner}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function RiskCards({ cases }: { cases: WorkforceCase[] }) {
  return (
    <div className="grid gap-3 lg:grid-cols-3">
      {cases
        .filter((item) => item.riskLevel !== "正常")
        .map((item) => (
          <div className="rounded-lg border border-border bg-white p-4 shadow-card" key={item.id}>
            <StatusBadge tone={riskTone(item.riskLevel)}>{item.riskLevel}</StatusBadge>
            <h3 className="mt-3 font-semibold text-textPrimary">{item.lineOrArea}</h3>
            <p className="mt-1 text-sm text-textSecondary">{item.riskReason}</p>
            <div className="mt-3 grid grid-cols-2 gap-2 text-sm">
              <div className="rounded-md bg-slate-50 p-3">
                <p className="text-xs text-textSecondary">人力</p>
                <p className="mt-1 font-semibold text-textPrimary">{item.assignedStaff}/{item.requiredStaff}</p>
              </div>
              <div className="rounded-md bg-slate-50 p-3">
                <p className="text-xs text-textSecondary">支援</p>
                <p className="mt-1 font-semibold text-textPrimary">{item.supportNeeded} 人</p>
              </div>
            </div>
          </div>
        ))}
    </div>
  );
}

function DetailPanel({ item }: { item: WorkforceCase }) {
  return (
    <aside className="space-y-4 rounded-lg border border-border bg-white p-4 shadow-card xl:sticky xl:top-24">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-xs font-medium uppercase tracking-wide text-textSecondary">目前人力檢核</p>
          <h2 className="mt-1 text-lg font-semibold text-textPrimary">{item.id}</h2>
          <p className="mt-1 text-sm text-textSecondary">{item.lineOrArea}</p>
        </div>
        <StatusBadge tone={riskTone(item.riskLevel)}>{item.riskLevel}</StatusBadge>
      </div>

      <div className="grid grid-cols-2 gap-3 text-sm">
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">人力</p>
          <p className="mt-1 font-semibold text-textPrimary">{item.assignedStaff} / {item.requiredStaff}</p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">加班</p>
          <p className="mt-1 font-semibold text-textPrimary">{item.overtimeHours} 小時</p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">技能</p>
          <p className="mt-1 font-semibold text-textPrimary">{item.skillCoverage}</p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">支援需求</p>
          <p className="mt-1 font-semibold text-textPrimary">{item.supportNeeded} 人</p>
        </div>
      </div>

      <div className="rounded-md bg-slate-50 p-3 text-sm">
        <p className="text-xs text-textSecondary">風險說明</p>
        <p className="mt-1 leading-6 text-textPrimary">{item.riskReason}</p>
      </div>

      <div className="space-y-2">
        <p className="text-sm font-semibold text-textPrimary">需求拆解</p>
        {item.requirements.map((req) => (
          <div className="rounded-md border border-border px-3 py-2" key={`${req.area}-${req.note}`}>
            <div className="flex items-center justify-between gap-3">
              <p className="font-medium text-textPrimary">{req.area}</p>
              <StatusBadge tone={req.tone}>缺口 {req.gap}</StatusBadge>
            </div>
            <p className="mt-1 text-xs text-textSecondary">
              {req.assigned}/{req.required} · {req.note}
            </p>
          </div>
        ))}
      </div>
    </aside>
  );
}

function MainContent({
  activeTab,
  data,
  selectedCase,
  onSelectCase
}: {
  activeTab: WorkforceWorkspaceTab;
  data: WorkforceDashboardData;
  selectedCase: WorkforceCase;
  onSelectCase: (item: WorkforceCase) => void;
}) {
  if (activeTab === "skill-gap" || activeTab === "overtime") {
    return (
      <div className="space-y-4">
        <RiskCards cases={data.cases} />
        <WorkforceTable activeTab={activeTab} cases={data.cases} selectedId={selectedCase.id} onSelect={onSelectCase} />
      </div>
    );
  }

  return <WorkforceTable activeTab={activeTab} cases={data.cases} selectedId={selectedCase.id} onSelect={onSelectCase} />;
}

export default function WorkforcePage() {
  const { data: workforceData, error, isLoading, source } = useWorkforceDashboard();
  const [activeTab, setActiveTab] = useState<WorkforceWorkspaceTab>("coverage");
  const [selectedCaseId, setSelectedCaseId] = useState<string>(workforceData.cases[0].id);
  const selectedCase = workforceData.cases.find((item) => item.id === selectedCaseId) ?? workforceData.cases[0];

  return (
    <AppLayout activePath="/workforce" title="人力班表 Workforce Workspace">
      <div className="mx-auto max-w-[1480px] space-y-5">
        <section className="rounded-lg border border-border bg-white p-4 shadow-card">
          <div className="flex flex-col gap-4 xl:flex-row xl:items-center xl:justify-between">
            <div>
              <div className="flex flex-wrap items-center gap-2">
                <StatusBadge tone="info">EWDB 20260522</StatusBadge>
                <StatusBadge tone={source === "api" ? "success" : "warning"}>
                  {source === "api" ? "API data" : "Mock fallback"}
                </StatusBadge>
                {isLoading ? <StatusBadge tone="info">Loading API</StatusBadge> : null}
                <StatusBadge tone="neutral">班表 / 技能 / 支援 / 證照</StatusBadge>
              </div>
              <h2 className="mt-3 text-2xl font-semibold text-textPrimary">人力覆蓋與技能缺口總覽</h2>
              <p className="mt-2 max-w-3xl text-sm leading-6 text-textSecondary">
                串接 Planning 與 Production 的排程需求，檢查今日產線、倉庫、品保與物流人員是否足夠，
                並掌握技能、加班、跨線支援與證照複訓風險。
              </p>
            </div>
            <div className="grid gap-2 sm:grid-cols-[minmax(220px,1fr)_auto_auto]">
              <label className="flex h-10 items-center gap-2 rounded-input border border-border bg-slate-50 px-3">
                <Search className="h-4 w-4 text-textSecondary" aria-hidden="true" />
                <input
                  className="w-full bg-transparent text-sm outline-none placeholder:text-textSecondary"
                  placeholder="班別 / 產線 / 技能 / 人員"
                />
              </label>
              <button className="inline-flex h-10 items-center justify-center gap-2 rounded-button border border-border bg-white px-3 text-sm font-medium text-textSecondary">
                <Filter className="h-4 w-4" aria-hidden="true" />
                篩選
              </button>
              <button className="inline-flex h-10 items-center justify-center gap-2 rounded-button bg-primary px-3 text-sm font-medium text-white">
                <CalendarDays className="h-4 w-4" aria-hidden="true" />
                排班
              </button>
            </div>
          </div>
        </section>

        {error ? (
          <p className="rounded-lg border border-warning/20 bg-warning/10 px-4 py-3 text-sm text-warning">
            Workforce API 尚未可用，已使用 mock fallback。{error}
          </p>
        ) : null}

        <KpiStrip summary={workforceData.summary} />

        <section className="grid gap-5 xl:grid-cols-[minmax(0,1fr)_390px]">
          <div className="space-y-4">
            <div className="rounded-lg border border-border bg-white p-3 shadow-card">
              <div className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
                <div>
                  <p className="text-xs font-medium uppercase tracking-wide text-textSecondary">人力視圖</p>
                  <h3 className="mt-1 text-lg font-semibold text-textPrimary">
                    {tabs.find((tab) => tab.id === activeTab)?.label}
                  </h3>
                  <p className="mt-1 text-sm text-textSecondary">{tabDescriptions[activeTab]}</p>
                </div>
                <div className="flex flex-wrap gap-2">
                  {tabs.map((tab) => (
                    <button
                      className={`h-9 rounded-button px-3 text-sm font-medium transition ${
                        activeTab === tab.id ? "bg-primary text-white" : "bg-slate-100 text-textSecondary hover:bg-slate-200"
                      }`}
                      key={tab.id}
                      onClick={() => setActiveTab(tab.id)}
                      type="button"
                    >
                      {tab.label}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            <MainContent
              activeTab={activeTab}
              data={workforceData}
              selectedCase={selectedCase}
              onSelectCase={(item) => setSelectedCaseId(item.id)}
            />
          </div>

          <DetailPanel item={selectedCase} />
        </section>
      </div>
    </AppLayout>
  );
}
