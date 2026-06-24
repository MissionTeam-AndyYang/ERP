"use client";

import {
  AlertTriangle,
  Boxes,
  ClipboardList,
  Filter,
  PackageSearch,
  Search,
  TrendingUp,
  Warehouse
} from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import { StatusBadge } from "@/components/ui/status-badge";
import { useWarehouseDashboard } from "@/hooks/use-warehouse-dashboard";
import { AppLayout } from "@/layouts/app-layout";
import type {
  WarehouseCapacity,
  WarehouseCategorySummary,
  WarehouseDashboardData,
  WarehouseKpi,
  WarehouseRecord,
  WarehouseRisk,
  WarehouseTask,
  WarehouseWorkspaceTab
} from "@/types/warehouse";

const tabs: { id: WarehouseWorkspaceTab; label: string }[] = [
  { id: "value-space", label: "價值與倉位" },
  { id: "risk", label: "風險警示" },
  { id: "tasks", label: "待處理入出庫" },
  { id: "details", label: "庫存明細" }
];

const tabDescriptions: Record<WarehouseWorkspaceTab, string> = {
  "value-space": "依庫存類別掌握資金水位、佔用板數與各倉可用空間。",
  risk: "集中查看迴轉超過一個月、少於 1/3 效期與低於安全水位的庫存。",
  tasks: "追蹤今天尚未完成的入庫、出庫、移倉與確認事項。",
  details: "以批號、品項、倉位、來源與 workflow 檢視庫存明細。"
};

function formatNumber(value: number) {
  return new Intl.NumberFormat("zh-TW").format(value);
}

function formatMoney(value: number) {
  return `$${new Intl.NumberFormat("zh-TW").format(value)}`;
}

function getVisibleRows(activeTab: WarehouseWorkspaceTab, data: WarehouseDashboardData) {
  if (activeTab === "risk") {
    const riskBatches = new Set(data.risks.map((risk) => risk.batchNo));
    return data.records.filter((record) => riskBatches.has(record.batchNo));
  }

  if (activeTab === "tasks") {
    const taskBatches = new Set(data.tasks.map((task) => task.batchNo));
    return data.records.filter((record) => taskBatches.has(record.batchNo));
  }

  return data.records;
}

function normalizeSearch(value: string) {
  return value.trim().toLocaleLowerCase();
}

function includesSearch(value: string | number, search: string) {
  return String(value).toLocaleLowerCase().includes(search);
}

function recordMatchesSearch(record: WarehouseRecord, search: string) {
  if (!search) {
    return true;
  }

  return [
    record.itemNo,
    record.itemName,
    record.category,
    record.warehouseNo,
    record.warehouseName,
    record.batchNo,
    record.sourceLabel,
    record.sourceNo,
    record.status
  ].some((value) => includesSearch(value, search));
}

function riskMatchesSearch(risk: WarehouseRisk, search: string) {
  if (!search) {
    return true;
  }

  return [
    risk.type,
    risk.itemName,
    risk.category,
    risk.batchNo,
    risk.warehouseName,
    risk.metric,
    risk.recommendation
  ].some((value) => includesSearch(value, search));
}

function taskMatchesSearch(task: WarehouseTask, search: string) {
  if (!search) {
    return true;
  }

  return [
    task.id,
    task.type,
    task.itemName,
    task.batchNo,
    task.sourceNo,
    task.owner,
    task.dueTime,
    task.status
  ].some((value) => includesSearch(value, search));
}

function KpiStrip({ kpis }: { kpis: WarehouseKpi[] }) {
  const icons = [TrendingUp, Warehouse, AlertTriangle, ClipboardList];

  return (
    <section className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
      {kpis.map((item, index) => {
        const Icon = icons[index] ?? Boxes;
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

function ValueAndSpaceView({
  capacities,
  categorySummaries
}: {
  capacities: WarehouseCapacity[];
  categorySummaries: WarehouseCategorySummary[];
}) {
  const totalValue = categorySummaries.reduce((sum, item) => sum + item.amount, 0);
  const totalPallets = categorySummaries.reduce((sum, item) => sum + item.palletCount, 0);

  return (
    <div className="grid min-w-0 gap-4 xl:grid-cols-[minmax(0,1fr)_420px]">
      <div className="min-w-0 rounded-lg border border-border bg-white p-4 shadow-card">
        <div className="flex flex-col gap-1 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <p className="text-sm font-medium text-textSecondary">庫存價值與板數</p>
            <h3 className="mt-1 text-lg font-semibold text-textPrimary">依類別統計資金與空間佔用</h3>
          </div>
          <p className="text-sm text-textSecondary">
            總價值 {formatMoney(totalValue)} · 佔用 {formatNumber(totalPallets)} 板
          </p>
        </div>

        <div className="mt-4 overflow-x-auto">
          <table className="min-w-[720px] w-full border-collapse text-sm">
            <thead className="bg-slate-50 text-left text-xs font-semibold uppercase tracking-wide text-textSecondary">
              <tr>
                <th className="px-4 py-3">類別</th>
                <th className="px-4 py-3 text-right">庫存價值</th>
                <th className="px-4 py-3">價值佔比</th>
                <th className="px-4 py-3 text-right">佔用板數</th>
                <th className="px-4 py-3 text-right">預留價值</th>
                <th className="px-4 py-3 text-right">可用價值</th>
                <th className="px-4 py-3 text-right">7日趨勢</th>
                <th className="px-4 py-3 text-right">品項數</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border">
              {categorySummaries.map((item) => (
                <tr key={item.category}>
                  <td className="px-4 py-3">
                    <StatusBadge tone={item.tone}>{item.category}</StatusBadge>
                  </td>
                  <td className="px-4 py-3 text-right font-semibold text-textPrimary">
                    {formatMoney(item.amount)}
                  </td>
                  <td className="px-4 py-3">
                    <div className="flex items-center gap-2">
                      <div className="h-2 w-24 overflow-hidden rounded-full bg-slate-100">
                        <div className="h-full rounded-full bg-primary" style={{ width: `${item.amountRatio}%` }} />
                      </div>
                      <span className="text-xs text-textSecondary">{item.amountRatio}%</span>
                    </div>
                  </td>
                  <td className="px-4 py-3 text-right text-textPrimary">{formatNumber(item.palletCount)} 板</td>
                  <td className="px-4 py-3 text-right text-textPrimary">{formatMoney(item.reservedAmount)}</td>
                  <td className="px-4 py-3 text-right font-semibold text-textPrimary">
                    {formatMoney(item.availableAmount)}
                  </td>
                  <td
                    className={`px-4 py-3 text-right font-medium ${
                      item.trend7Days >= 0 ? "text-warning" : "text-success"
                    }`}
                  >
                    {item.trend7Days >= 0 ? "+" : ""}
                    {item.trend7Days}%
                  </td>
                  <td className="px-4 py-3 text-right text-textPrimary">{formatNumber(item.itemCount)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="space-y-3">
        {capacities.map((warehouseItem) => {
          const usedRatio = Math.round((warehouseItem.usedPallets / warehouseItem.totalPallets) * 100);
          return (
            <div className="rounded-lg border border-border bg-white p-4 shadow-card" key={warehouseItem.id}>
              <div className="flex items-start justify-between gap-3">
                <div>
                  <p className="font-semibold text-textPrimary">{warehouseItem.warehouseName}</p>
                  <p className="mt-1 text-xs text-textSecondary">{warehouseItem.warehouseType}</p>
                </div>
                <StatusBadge tone={warehouseItem.tone}>{usedRatio}% 使用</StatusBadge>
              </div>
              <div className="mt-3 h-2 overflow-hidden rounded-full bg-slate-100">
                <div className="h-full rounded-full bg-primary" style={{ width: `${usedRatio}%` }} />
              </div>
              <div className="mt-3 grid grid-cols-3 gap-2 text-sm">
                <div>
                  <p className="text-xs text-textSecondary">已用</p>
                  <p className="font-semibold text-textPrimary">{warehouseItem.usedPallets} 板</p>
                </div>
                <div>
                  <p className="text-xs text-textSecondary">預留</p>
                  <p className="font-semibold text-textPrimary">{warehouseItem.reservedPallets} 板</p>
                </div>
                <div>
                  <p className="text-xs text-textSecondary">可用</p>
                  <p className="font-semibold text-textPrimary">{warehouseItem.availablePallets} 板</p>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function EmptyState({ message }: { message: string }) {
  return (
    <div className="rounded-lg border border-dashed border-border bg-white px-4 py-8 text-center text-sm text-textSecondary">
      {message}
    </div>
  );
}

function RiskView({ risks, searchQuery }: { risks: WarehouseRisk[]; searchQuery: string }) {
  const visibleRisks = risks.filter((risk) => riskMatchesSearch(risk, searchQuery));

  if (!visibleRisks.length) {
    return <EmptyState message="目前查無符合條件的風險警示。" />;
  }

  return (
    <div className="grid gap-3 lg:grid-cols-3">
      {visibleRisks.map((risk) => (
        <div className="rounded-lg border border-border bg-white p-4 shadow-card" key={risk.id}>
          <div className="flex items-start justify-between gap-3">
            <div>
              <StatusBadge tone={risk.tone}>{risk.type}</StatusBadge>
              <h3 className="mt-3 font-semibold text-textPrimary">{risk.itemName}</h3>
              <p className="mt-1 text-xs text-textSecondary">
                {risk.category} · {risk.batchNo}
              </p>
            </div>
            <AlertTriangle className="h-5 w-5 text-textSecondary" aria-hidden="true" />
          </div>
          <div className="mt-4 rounded-md bg-slate-50 p-3">
            <p className="text-xs text-textSecondary">目前指標</p>
            <p className="mt-1 font-semibold text-textPrimary">{risk.metric}</p>
          </div>
          <p className="mt-3 text-sm leading-6 text-textSecondary">{risk.recommendation}</p>
          <p className="mt-3 text-xs text-textSecondary">{risk.warehouseName}</p>
        </div>
      ))}
    </div>
  );
}

function TaskView({ tasks, searchQuery }: { tasks: WarehouseTask[]; searchQuery: string }) {
  const visibleTasks = tasks.filter((task) => taskMatchesSearch(task, searchQuery));

  if (!visibleTasks.length) {
    return <EmptyState message="目前查無符合條件的待處理入出庫任務。" />;
  }

  return (
    <div className="overflow-hidden rounded-lg border border-border bg-white shadow-card">
      <div className="overflow-x-auto">
        <table className="min-w-[900px] w-full border-collapse text-sm">
          <thead className="bg-slate-50 text-left text-xs font-semibold uppercase tracking-wide text-textSecondary">
            <tr>
              <th className="px-4 py-3">類型</th>
              <th className="px-4 py-3">品項 / 批號</th>
              <th className="px-4 py-3">來源單號</th>
              <th className="px-4 py-3 text-right">任務數量</th>
              <th className="px-4 py-3 text-right">板數</th>
              <th className="px-4 py-3">負責</th>
              <th className="px-4 py-3">時間</th>
              <th className="px-4 py-3">狀態</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {visibleTasks.map((task) => (
              <tr key={task.id}>
                <td className="px-4 py-3">
                  <StatusBadge tone={task.tone}>{task.type}</StatusBadge>
                </td>
                <td className="px-4 py-3">
                  <p className="font-semibold text-textPrimary">{task.itemName}</p>
                  <p className="mt-1 text-xs text-textSecondary">{task.batchNo}</p>
                </td>
                <td className="px-4 py-3 text-textPrimary">{task.sourceNo}</td>
                <td className="px-4 py-3 text-right font-semibold text-textPrimary">
                  {formatNumber(task.quantity)} {task.unit}
                </td>
                <td className="px-4 py-3 text-right text-textPrimary">{task.palletCount} 板</td>
                <td className="px-4 py-3 text-textPrimary">{task.owner}</td>
                <td className="px-4 py-3 text-textPrimary">{task.dueTime}</td>
                <td className="px-4 py-3 text-textPrimary">{task.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function WarehouseTable({
  activeTab,
  data,
  selectedId,
  searchQuery,
  onSelect
}: {
  activeTab: WarehouseWorkspaceTab;
  data: WarehouseDashboardData;
  selectedId: string;
  searchQuery: string;
  onSelect: (record: WarehouseRecord) => void;
}) {
  const rows = useMemo(
    () => getVisibleRows(activeTab, data).filter((record) => recordMatchesSearch(record, searchQuery)),
    [activeTab, data, searchQuery]
  );

  if (!rows.length) {
    return <EmptyState message="目前查無符合條件的庫存明細。" />;
  }

  return (
    <div className="overflow-hidden rounded-lg border border-border bg-white shadow-card">
      <div className="overflow-x-auto">
        <table className="min-w-[1040px] w-full border-collapse text-sm">
          <thead className="bg-slate-50 text-left text-xs font-semibold uppercase tracking-wide text-textSecondary">
            <tr>
              <th className="px-4 py-3">品項</th>
              <th className="px-4 py-3">批號</th>
              <th className="px-4 py-3">倉庫</th>
              <th className="px-4 py-3">來源</th>
              <th className="px-4 py-3 text-right">數量</th>
              <th className="px-4 py-3 text-right">價值</th>
              <th className="px-4 py-3 text-right">板數</th>
              <th className="px-4 py-3">迴轉 / 效期</th>
              <th className="px-4 py-3">狀態</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {rows.map((record) => {
              const isSelected = record.id === selectedId;
              return (
                <tr
                  className={`cursor-pointer transition ${
                    isSelected ? "bg-info/10" : "hover:bg-slate-50"
                  }`}
                  key={record.id}
                  onClick={() => onSelect(record)}
                >
                  <td className="px-4 py-3">
                    <p className="font-semibold text-textPrimary">{record.itemName}</p>
                    <p className="mt-1 text-xs text-textSecondary">
                      {record.itemNo} · {record.category}
                    </p>
                  </td>
                  <td className="px-4 py-3 font-medium text-textPrimary">{record.batchNo}</td>
                  <td className="px-4 py-3">
                    <p className="text-textPrimary">{record.warehouseName}</p>
                    <p className="mt-1 text-xs text-textSecondary">{record.warehouseNo}</p>
                  </td>
                  <td className="px-4 py-3">
                    <p className="text-textPrimary">{record.sourceLabel}</p>
                    <p className="mt-1 text-xs text-textSecondary">{record.sourceNo}</p>
                  </td>
                  <td className="px-4 py-3 text-right font-semibold text-textPrimary">
                    {formatNumber(record.quantity)} / {formatNumber(record.reservedQuantity)} /{" "}
                    {formatNumber(record.availableQuantity)} {record.unit}
                  </td>
                  <td className="px-4 py-3 text-right text-textPrimary">{formatMoney(record.amount)}</td>
                  <td className="px-4 py-3 text-right text-textPrimary">{record.palletCount} 板</td>
                  <td className="px-4 py-3">
                    <p className="text-textPrimary">迴轉 {record.turnoverDays} 天</p>
                    <p className="mt-1 text-xs text-textSecondary">
                      剩餘 {record.daysLeft} 天 / 效期 {record.shelfLifeDays} 天
                    </p>
                  </td>
                  <td className="px-4 py-3">
                    <StatusBadge tone={record.tone}>{record.status}</StatusBadge>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function DetailPanel({ record }: { record: WarehouseRecord }) {
  return (
    <aside className="space-y-4 rounded-lg border border-border bg-white p-4 shadow-card xl:sticky xl:top-24">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-xs font-medium uppercase tracking-wide text-textSecondary">目前批號</p>
          <h2 className="mt-1 text-lg font-semibold text-textPrimary">{record.batchNo}</h2>
          <p className="mt-1 text-sm text-textSecondary">{record.itemName}</p>
        </div>
        <StatusBadge tone={record.tone}>{record.status}</StatusBadge>
      </div>

      <div className="grid grid-cols-2 gap-3 text-sm">
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">現有 / 預留 / 可用</p>
          <p className="mt-1 font-semibold text-textPrimary">
            {formatNumber(record.quantity)} / {formatNumber(record.reservedQuantity)} /{" "}
            {formatNumber(record.availableQuantity)} {record.unit}
          </p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">價值 / 預留 / 可用</p>
          <p className="mt-1 font-semibold text-textPrimary">{formatMoney(record.amount)}</p>
          <p className="mt-1 text-xs text-textSecondary">
            {formatMoney(record.reservedAmount)} / {formatMoney(record.availableAmount)}
          </p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">佔用板數</p>
          <p className="mt-1 font-semibold text-textPrimary">{record.palletCount} 板</p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">安全水位</p>
          <p className="mt-1 font-semibold text-textPrimary">
            {formatNumber(record.safetyStock)} {record.unit}
          </p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">迴轉週期</p>
          <p className="mt-1 font-semibold text-textPrimary">{record.turnoverDays} 天</p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">效期剩餘</p>
          <p className="mt-1 font-semibold text-textPrimary">{record.daysLeft} 天</p>
        </div>
      </div>

      <div className="space-y-2">
        <p className="text-sm font-semibold text-textPrimary">流程狀態</p>
        {record.workflow.map((step, index) => (
          <div className="flex gap-3" key={`${step.label}-${step.ref}`}>
            <div className="flex flex-col items-center">
              <span
                className={`grid h-6 w-6 place-items-center rounded-full text-xs font-bold ${
                  step.tone === "success"
                    ? "bg-success text-white"
                    : step.tone === "danger"
                      ? "bg-danger text-white"
                      : step.tone === "warning"
                        ? "bg-warning text-white"
                        : "bg-info text-white"
                }`}
              >
                {index + 1}
              </span>
              {index < record.workflow.length - 1 ? <span className="h-8 w-px bg-border" /> : null}
            </div>
            <div className="min-w-0 pb-2">
              <div className="flex flex-wrap items-center gap-2">
                <p className="font-medium text-textPrimary">{step.label}</p>
                <StatusBadge tone={step.tone}>{step.status}</StatusBadge>
              </div>
              <p className="mt-1 truncate text-xs text-textSecondary">{step.ref}</p>
            </div>
          </div>
        ))}
      </div>

      <div className="space-y-2">
        <p className="text-sm font-semibold text-textPrimary">關聯單據</p>
        {record.relatedDocuments.map((doc) => (
          <div
            className="flex items-center justify-between gap-3 rounded-md border border-border px-3 py-2"
            key={`${doc.type}-${doc.no}`}
          >
            <div className="min-w-0">
              <p className="text-sm font-medium text-textPrimary">{doc.type}</p>
              <p className="truncate text-xs text-textSecondary">{doc.no}</p>
            </div>
            <StatusBadge tone={doc.tone}>{doc.status}</StatusBadge>
          </div>
        ))}
      </div>
    </aside>
  );
}

function MainContent({
  activeTab,
  data,
  selectedRecord,
  searchQuery,
  onSelectRecord
}: {
  activeTab: WarehouseWorkspaceTab;
  data: WarehouseDashboardData;
  selectedRecord?: WarehouseRecord;
  searchQuery: string;
  onSelectRecord: (record: WarehouseRecord) => void;
}) {
  if (activeTab === "value-space") {
    return (
      <ValueAndSpaceView
        capacities={data.capacities}
        categorySummaries={data.categorySummaries}
      />
    );
  }

  if (activeTab === "risk") {
    return (
      <div className="space-y-4">
        <RiskView risks={data.risks} searchQuery={searchQuery} />
        <WarehouseTable
          activeTab={activeTab}
          data={data}
          selectedId={selectedRecord?.id ?? ""}
          searchQuery={searchQuery}
          onSelect={onSelectRecord}
        />
      </div>
    );
  }

  if (activeTab === "tasks") {
    return (
      <div className="space-y-4">
        <TaskView tasks={data.tasks} searchQuery={searchQuery} />
        <WarehouseTable
          activeTab={activeTab}
          data={data}
          selectedId={selectedRecord?.id ?? ""}
          searchQuery={searchQuery}
          onSelect={onSelectRecord}
        />
      </div>
    );
  }

  return (
    <WarehouseTable
      activeTab={activeTab}
      data={data}
      selectedId={selectedRecord?.id ?? ""}
      searchQuery={searchQuery}
      onSelect={onSelectRecord}
    />
  );
}

export default function WarehousePage() {
  const { data: warehouseData, error, isLoading, isInventoryLoading, source, loadInventory, loadTasks } =
    useWarehouseDashboard();
  const [activeTab, setActiveTab] = useState<WarehouseWorkspaceTab>("value-space");
  const [selectedRecordId, setSelectedRecordId] = useState<string>(warehouseData.records[0]?.id ?? "");
  const [searchValue, setSearchValue] = useState("");
  const searchQuery = normalizeSearch(searchValue);
  const selectedRecord =
    warehouseData.records.find((record) => record.id === selectedRecordId) ?? warehouseData.records[0];

  useEffect(() => {
    if (!isLoading && (activeTab === "value-space" || activeTab === "risk" || activeTab === "details")) {
      void loadInventory();
    }
    if (!isLoading && activeTab === "tasks") {
      void loadTasks();
      void loadInventory();
    }
  }, [activeTab, isLoading, loadInventory, loadTasks]);

  return (
    <AppLayout activePath="/warehouse" titleKey="warehouse.layoutTitle">
      <div className="mx-auto max-w-[1480px] space-y-5">
        <section className="rounded-lg border border-border bg-white p-4 shadow-card">
          <div className="flex flex-col gap-4 xl:flex-row xl:items-center xl:justify-between">
            <div>
              <div className="flex flex-wrap items-center gap-2">
                <StatusBadge tone="info">EWDB 20260522</StatusBadge>
                <StatusBadge tone="neutral">價值 / 倉位 / 風險 / 入出庫</StatusBadge>
                <StatusBadge tone={source === "api" ? "success" : "warning"}>
                  {source === "api" ? "API data" : "Mock fallback"}
                </StatusBadge>
                {isLoading ? <StatusBadge tone="info">Loading API</StatusBadge> : null}
              </div>
              <h2 className="mt-3 text-2xl font-semibold text-textPrimary">倉庫經營總覽</h2>
              <p className="mt-2 max-w-3xl text-sm leading-6 text-textSecondary">
                以庫存價值、佔用板數、倉庫可用空間、迴轉週期、效期與安全水位為核心，
                協助管理者掌握資金分佈、寄倉規劃與今日入出庫待處理事項。
              </p>
            </div>
            <div className="grid gap-2 sm:grid-cols-[minmax(220px,1fr)_auto_auto]">
              <label className="flex h-10 items-center gap-2 rounded-input border border-border bg-slate-50 px-3">
                <Search className="h-4 w-4 text-textSecondary" aria-hidden="true" />
                <input
                  className="w-full bg-transparent text-sm outline-none placeholder:text-textSecondary"
                  aria-label="搜尋批號、品項、倉庫或來源單號"
                  value={searchValue}
                  onChange={(event) => setSearchValue(event.target.value)}
                  placeholder="批號 / 品項 / 倉庫 / 來源單號"
                />
              </label>
              <button
                className="inline-flex h-10 items-center justify-center gap-2 rounded-button border border-border bg-white px-3 text-sm font-medium text-textSecondary"
                title="V1 先保留為進階篩選入口，待 API 條件欄位確認後啟用。"
                type="button"
              >
                <Filter className="h-4 w-4" aria-hidden="true" />
                篩選
              </button>
              <button
                className="inline-flex h-10 items-center justify-center gap-2 rounded-button bg-primary px-3 text-sm font-medium text-white"
                onClick={() => setActiveTab("details")}
                title="切換到庫存明細，檢視目前選取批號的流程與關聯單據。"
                type="button"
              >
                <PackageSearch className="h-4 w-4" aria-hidden="true" />
                追溯
              </button>
            </div>
          </div>
        </section>

        {error ? (
          <p className="rounded-lg border border-warning/20 bg-warning/10 px-4 py-3 text-sm text-warning">
            Warehouse API 尚未可用，已使用 mock fallback。{error}
          </p>
        ) : null}

        <KpiStrip kpis={warehouseData.kpis} />

        <section className="grid gap-5 xl:grid-cols-[minmax(0,1fr)_390px]">
          <div className="min-w-0 space-y-4">
            <div className="rounded-lg border border-border bg-white p-3 shadow-card">
              <div className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
                <div>
                  <p className="text-xs font-medium uppercase tracking-wide text-textSecondary">倉庫視圖</p>
                  <h3 className="mt-1 text-lg font-semibold text-textPrimary">
                    {tabs.find((tab) => tab.id === activeTab)?.label}
                  </h3>
                  <p className="mt-1 text-sm text-textSecondary">{tabDescriptions[activeTab]}</p>
                </div>
                <div className="flex flex-wrap gap-2">
                  {tabs.map((tab) => (
                    <button
                      className={`h-9 rounded-button px-3 text-sm font-medium transition ${
                        activeTab === tab.id
                          ? "bg-primary text-white"
                          : "bg-slate-100 text-textSecondary hover:bg-slate-200"
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
              data={warehouseData}
              selectedRecord={selectedRecord}
              searchQuery={searchQuery}
              onSelectRecord={(record) => setSelectedRecordId(record.id)}
            />
          </div>

          {selectedRecord ? (
            <DetailPanel record={selectedRecord} />
          ) : (
            <EmptyState
              message={
                isLoading || isInventoryLoading
                  ? "正在載入庫存明細。"
                  : "目前沒有可顯示的庫存批號，請確認 inventory API 是否仍有 currentQuantity 大於 0 的資料。"
              }
            />
          )}
        </section>
      </div>
    </AppLayout>
  );
}
