"use client";

import {
  AlertTriangle,
  ClipboardCheck,
  Filter,
  Search,
  ThermometerSnowflake,
  Truck
} from "lucide-react";
import { useMemo, useState } from "react";
import { StatusBadge } from "@/components/ui/status-badge";
import { useLogisticsDashboard } from "@/hooks/use-logistics-dashboard";
import { AppLayout } from "@/layouts/app-layout";
import type {
  DeliveryRiskLevel,
  LogisticsDashboardData,
  LogisticsSummary,
  LogisticsWorkspaceTab,
  Shipment
} from "@/types/logistics";

const tabs: { id: LogisticsWorkspaceTab; label: string }[] = [
  { id: "shipments", label: "今日出貨" },
  { id: "dispatch-risk", label: "派車風險" },
  { id: "cold-chain", label: "冷鏈溫層" },
  { id: "documents", label: "文件/簽收" }
];

const tabDescriptions: Record<LogisticsWorkspaceTab, string> = {
  shipments: "查看今日出貨單、客戶要求到貨時間、倉庫出庫、品檢放行與目前配送階段。",
  "dispatch-risk": "集中檢視會影響交期的出貨阻擋，包含品檢、庫存、派車與文件問題。",
  "cold-chain": "追蹤車輛、溫層要求、目前溫度與冷鏈異常。",
  documents: "檢查出貨單、品檢放行、溫度紀錄與電子簽收是否完整。"
};

function formatNumber(value: number) {
  return new Intl.NumberFormat("zh-TW").format(value);
}

function normalizeSearch(value: string) {
  return value.trim().toLowerCase();
}

function includesSearch(value: string | number | null, query: string) {
  return String(value ?? "").toLowerCase().includes(query);
}

function shipmentMatchesSearch(item: Shipment, query: string) {
  if (!query) {
    return true;
  }

  return [
    item.id,
    item.salesOrder,
    item.customer,
    item.channel,
    item.destination,
    item.route,
    item.product,
    item.batchNo,
    item.vehicleNo,
    item.driver,
    item.owner,
    item.stage,
    item.deliveryRisk,
    item.riskReason,
    item.warehouseStatus,
    item.qualityReleaseStatus
  ].some((value) => includesSearch(value, query));
}

function riskTone(risk: DeliveryRiskLevel) {
  if (risk === "高風險") {
    return "danger";
  }

  if (risk === "注意") {
    return "warning";
  }

  return "success";
}

function getVisibleShipments(activeTab: LogisticsWorkspaceTab, shipments: Shipment[]) {
  if (activeTab === "dispatch-risk") {
    return shipments.filter((item) => item.deliveryRisk !== "正常");
  }

  if (activeTab === "cold-chain") {
    return shipments.filter((item) => item.temperatureStatus !== "正常");
  }

  if (activeTab === "documents") {
    return shipments.filter((item) => !item.documentsReady || item.proofOfDeliveryStatus !== "已簽收");
  }

  return shipments;
}

function EmptyState({ title, description }: { title: string; description: string }) {
  return (
    <div className="rounded-lg border border-dashed border-border bg-slate-50 px-4 py-10 text-center">
      <p className="font-semibold text-textPrimary">{title}</p>
      <p className="mt-2 text-sm text-textSecondary">{description}</p>
    </div>
  );
}

function KpiStrip({ summary }: { summary: LogisticsSummary[] }) {
  const icons = [Truck, AlertTriangle, ThermometerSnowflake, ClipboardCheck];

  return (
    <section className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
      {summary.map((item, index) => {
        const Icon = icons[index] ?? Truck;
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

function ShipmentsTable({
  activeTab,
  shipments,
  searchQuery,
  selectedId,
  onSelect
}: {
  activeTab: LogisticsWorkspaceTab;
  shipments: Shipment[];
  searchQuery: string;
  selectedId: string;
  onSelect: (item: Shipment) => void;
}) {
  const rows = useMemo(
    () => getVisibleShipments(activeTab, shipments).filter((item) => shipmentMatchesSearch(item, searchQuery)),
    [activeTab, shipments, searchQuery]
  );

  return (
    <div className="overflow-hidden rounded-lg border border-border bg-white shadow-card">
      {rows.length > 0 ? (
        <div className="overflow-x-auto">
          <table className="min-w-[1160px] w-full border-collapse text-sm">
            <thead className="bg-slate-50 text-left text-xs font-semibold uppercase tracking-wide text-textSecondary">
              <tr>
                <th className="px-4 py-3">出貨 / 訂單</th>
                <th className="px-4 py-3">客戶 / 路線</th>
                <th className="px-4 py-3">產品批號</th>
                <th className="px-4 py-3 text-right">數量</th>
                <th className="px-4 py-3">到貨/出車</th>
                <th className="px-4 py-3">風險</th>
                <th className="px-4 py-3">倉庫/品檢</th>
                <th className="px-4 py-3">車輛/溫層</th>
                <th className="px-4 py-3">狀態</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border">
              {rows.map((item) => {
                const isSelected = item.id === selectedId;
                return (
                  <tr
                    className={`cursor-pointer transition ${
                      isSelected ? "bg-info/10" : "hover:bg-slate-50"
                    }`}
                    key={item.id}
                    onClick={() => onSelect(item)}
                  >
                    <td className="px-4 py-3">
                      <p className="font-semibold text-textPrimary">{item.id}</p>
                      <p className="mt-1 text-xs text-textSecondary">{item.salesOrder}</p>
                    </td>
                    <td className="px-4 py-3">
                      <p className="font-medium text-textPrimary">{item.customer}</p>
                      <p className="mt-1 text-xs text-textSecondary">{item.route} · {item.destination}</p>
                    </td>
                    <td className="px-4 py-3">
                      <p className="text-textPrimary">{item.product}</p>
                      <p className="mt-1 text-xs text-textSecondary">{item.batchNo}</p>
                    </td>
                    <td className="px-4 py-3 text-right font-semibold text-textPrimary">
                      {formatNumber(item.quantity)} {item.unit}
                    </td>
                    <td className="px-4 py-3">
                      <p className="text-textPrimary">{item.requestedArrivalTime}</p>
                      <p className="mt-1 text-xs text-textSecondary">出車 {item.plannedDepartureTime}</p>
                    </td>
                    <td className="px-4 py-3">
                      <StatusBadge tone={riskTone(item.deliveryRisk)}>{item.deliveryRisk}</StatusBadge>
                      <p className="mt-1 line-clamp-2 text-xs text-textSecondary">{item.riskReason}</p>
                    </td>
                    <td className="px-4 py-3">
                      <p className="text-textPrimary">{item.warehouseStatus}</p>
                      <p className="mt-1 text-xs text-textSecondary">品檢 {item.qualityReleaseStatus}</p>
                    </td>
                    <td className="px-4 py-3">
                      <p className="text-textPrimary">{item.vehicleNo ?? "待派車"}</p>
                      <p className="mt-1 text-xs text-textSecondary">
                        {item.temperatureRequirement} / {item.currentTemperature ?? "未回傳"}
                      </p>
                    </td>
                    <td className="px-4 py-3">
                      <StatusBadge tone={item.tone}>{item.stage}</StatusBadge>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="p-4">
          <EmptyState title="沒有符合條件的出貨單" description="請調整搜尋關鍵字，或切回其他物流視圖檢查。" />
        </div>
      )}
    </div>
  );
}

function RiskCards({ shipments, searchQuery }: { shipments: Shipment[]; searchQuery: string }) {
  const rows = shipments.filter(
    (item) => item.deliveryRisk !== "正常" && shipmentMatchesSearch(item, searchQuery)
  );

  if (rows.length === 0) {
    return <EmptyState title="沒有符合條件的派車風險" description="目前搜尋條件下沒有需要優先處理的出貨阻擋。" />;
  }

  return (
    <div className="grid gap-3 lg:grid-cols-3">
      {rows.map((item) => (
        <div className="rounded-lg border border-border bg-white p-4 shadow-card" key={item.id}>
          <div className="flex items-start justify-between gap-3">
            <div>
              <StatusBadge tone={riskTone(item.deliveryRisk)}>{item.deliveryRisk}</StatusBadge>
              <h3 className="mt-3 font-semibold text-textPrimary">{item.id}</h3>
              <p className="mt-1 text-sm text-textSecondary">{item.customer}</p>
            </div>
            <AlertTriangle className="h-5 w-5 text-textSecondary" aria-hidden="true" />
          </div>
          <p className="mt-3 text-sm leading-6 text-textSecondary">{item.riskReason}</p>
          <div className="mt-3 grid grid-cols-2 gap-2 text-sm">
            <div className="rounded-md bg-slate-50 p-3">
              <p className="text-xs text-textSecondary">倉庫</p>
              <p className="mt-1 font-semibold text-textPrimary">{item.warehouseStatus}</p>
            </div>
            <div className="rounded-md bg-slate-50 p-3">
              <p className="text-xs text-textSecondary">品檢</p>
              <p className="mt-1 font-semibold text-textPrimary">{item.qualityReleaseStatus}</p>
            </div>
          </div>
          </div>
      ))}
    </div>
  );
}

function DetailPanel({ item }: { item: Shipment }) {
  return (
    <aside className="space-y-4 rounded-lg border border-border bg-white p-4 shadow-card xl:sticky xl:top-24">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-xs font-medium uppercase tracking-wide text-textSecondary">目前出貨</p>
          <h2 className="mt-1 text-lg font-semibold text-textPrimary">{item.id}</h2>
          <p className="mt-1 text-sm text-textSecondary">{item.customer}</p>
          <p className="mt-1 text-xs text-textSecondary">{item.batchNo}</p>
        </div>
        <StatusBadge tone={riskTone(item.deliveryRisk)}>{item.deliveryRisk}</StatusBadge>
      </div>

      <div className="grid grid-cols-2 gap-3 text-sm">
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">要求到貨</p>
          <p className="mt-1 font-semibold text-textPrimary">{item.requestedArrivalTime}</p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">預計出車</p>
          <p className="mt-1 font-semibold text-textPrimary">{item.plannedDepartureTime}</p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">車輛/司機</p>
          <p className="mt-1 font-semibold text-textPrimary">{item.vehicleNo ?? "待派車"}</p>
          <p className="mt-1 text-xs text-textSecondary">{item.driver ?? "待安排"}</p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">溫層</p>
          <p className="mt-1 font-semibold text-textPrimary">{item.temperatureRequirement}</p>
          <p className="mt-1 text-xs text-textSecondary">目前 {item.currentTemperature ?? "未回傳"}</p>
        </div>
      </div>

      <div className="rounded-md bg-slate-50 p-3 text-sm">
        <p className="text-xs text-textSecondary">風險說明</p>
        <p className="mt-1 leading-6 text-textPrimary">{item.riskReason}</p>
      </div>

      <div className="space-y-2">
        <p className="text-sm font-semibold text-textPrimary">文件與簽收</p>
        {item.documents.map((doc) => (
          <div className="rounded-md border border-border px-3 py-2" key={`${doc.type}-${doc.no}`}>
            <div className="flex items-center justify-between gap-3">
              <p className="font-medium text-textPrimary">{doc.type}</p>
              <StatusBadge tone={doc.tone}>{doc.status}</StatusBadge>
            </div>
            <p className="mt-1 text-xs text-textSecondary">{doc.no} · {doc.owner}</p>
          </div>
        ))}
        <div className="rounded-md border border-border px-3 py-2">
          <div className="flex items-center justify-between gap-3">
            <p className="font-medium text-textPrimary">簽收</p>
            <StatusBadge tone={item.proofOfDeliveryStatus === "已簽收" ? "success" : "info"}>
              {item.proofOfDeliveryStatus}
            </StatusBadge>
          </div>
          <p className="mt-1 text-xs text-textSecondary">POD / 電子簽收回傳</p>
        </div>
      </div>

      <div className="space-y-2">
        <p className="text-sm font-semibold text-textPrimary">出貨流程</p>
        {item.workflow.map((step, index) => (
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
              {index < item.workflow.length - 1 ? <span className="h-7 w-px bg-border" /> : null}
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
    </aside>
  );
}

function MainContent({
  activeTab,
  data,
  searchQuery,
  selectedShipment,
  onSelectShipment
}: {
  activeTab: LogisticsWorkspaceTab;
  data: LogisticsDashboardData;
  searchQuery: string;
  selectedShipment: Shipment;
  onSelectShipment: (item: Shipment) => void;
}) {
  if (activeTab === "dispatch-risk") {
    return (
      <div className="space-y-4">
        <RiskCards shipments={data.shipments} searchQuery={searchQuery} />
        <ShipmentsTable
          activeTab={activeTab}
          shipments={data.shipments}
          searchQuery={searchQuery}
          selectedId={selectedShipment.id}
          onSelect={onSelectShipment}
        />
      </div>
    );
  }

  return (
    <ShipmentsTable
      activeTab={activeTab}
      shipments={data.shipments}
      searchQuery={searchQuery}
      selectedId={selectedShipment.id}
      onSelect={onSelectShipment}
    />
  );
}

export default function LogisticsPage() {
  const { data: logisticsData, error, isLoading, source } = useLogisticsDashboard();
  const [activeTab, setActiveTab] = useState<LogisticsWorkspaceTab>("shipments");
  const [selectedShipmentId, setSelectedShipmentId] = useState<string>(logisticsData.shipments[0].id);
  const [searchValue, setSearchValue] = useState("");
  const searchQuery = normalizeSearch(searchValue);
  const visibleShipments = useMemo(
    () => getVisibleShipments(activeTab, logisticsData.shipments).filter((item) => shipmentMatchesSearch(item, searchQuery)),
    [activeTab, logisticsData.shipments, searchQuery]
  );
  const selectedCandidate =
    logisticsData.shipments.find((item) => item.id === selectedShipmentId) ?? logisticsData.shipments[0];
  const selectedShipment =
    visibleShipments.find((item) => item.id === selectedCandidate.id) ?? visibleShipments[0] ?? selectedCandidate;

  return (
    <AppLayout activePath="/logistics" title="物流出貨 Logistics Workspace">
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
                <StatusBadge tone="neutral">出庫 / 派車 / 冷鏈 / 簽收</StatusBadge>
              </div>
              <h2 className="mt-3 text-2xl font-semibold text-textPrimary">出貨派車與冷鏈交付總覽</h2>
              <p className="mt-2 max-w-3xl text-sm leading-6 text-textSecondary">
                串接訂單履約、品檢放行與倉庫出庫，集中掌握今日出貨是否準時、車次是否已排、
                冷鏈溫層是否正常，以及出貨文件與簽收是否完整。
              </p>
            </div>
            <div className="grid gap-2 sm:grid-cols-[minmax(220px,1fr)_auto_auto]">
              <label className="flex h-10 items-center gap-2 rounded-input border border-border bg-slate-50 px-3">
                <Search className="h-4 w-4 text-textSecondary" aria-hidden="true" />
                <input
                  aria-label="搜尋出貨單、訂單、客戶或車輛"
                  className="w-full bg-transparent text-sm outline-none placeholder:text-textSecondary"
                  placeholder="出貨單 / 訂單 / 客戶 / 車輛"
                  value={searchValue}
                  onChange={(event) => setSearchValue(event.target.value)}
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
                title="切換到派車風險視圖，檢視出貨阻擋、派車與文件問題。"
                type="button"
                onClick={() => setActiveTab("dispatch-risk")}
              >
                <Truck className="h-4 w-4" aria-hidden="true" />
                派車
              </button>
            </div>
          </div>
        </section>

        {error ? (
          <p className="rounded-lg border border-warning/20 bg-warning/10 px-4 py-3 text-sm text-warning">
            Logistics API 尚未可用，已使用 mock fallback。{error}
          </p>
        ) : null}

        <KpiStrip summary={logisticsData.summary} />

        <section className="grid gap-5 xl:grid-cols-[minmax(0,1fr)_390px]">
          <div className="min-w-0 space-y-4">
            <div className="rounded-lg border border-border bg-white p-3 shadow-card">
              <div className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
                <div>
                  <p className="text-xs font-medium uppercase tracking-wide text-textSecondary">物流視圖</p>
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
              data={logisticsData}
              searchQuery={searchQuery}
              selectedShipment={selectedShipment}
              onSelectShipment={(item) => setSelectedShipmentId(item.id)}
            />
          </div>

          <DetailPanel item={selectedShipment} />
        </section>
      </div>
    </AppLayout>
  );
}
