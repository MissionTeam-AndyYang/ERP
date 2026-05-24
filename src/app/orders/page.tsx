"use client";

import {
  AlertTriangle,
  CalendarClock,
  CheckCircle2,
  ClipboardList,
  DollarSign,
  Filter,
  Search,
  Truck
} from "lucide-react";
import { useMemo, useState } from "react";
import { StatusBadge } from "@/components/ui/status-badge";
import { useOrdersDashboard } from "@/hooks/use-orders-dashboard";
import { AppLayout } from "@/layouts/app-layout";
import type {
  OrderRiskLevel,
  OrdersDashboardData,
  OrderStatusSummary,
  OrderWorkspaceTab,
  SalesOrder
} from "@/types/orders";

const tabs: { id: OrderWorkspaceTab; label: string }[] = [
  { id: "overview", label: "訂單總覽" },
  { id: "commitment", label: "接單承諾" },
  { id: "delivery-risk", label: "交期風險" },
  { id: "fulfillment", label: "履約進度" },
  { id: "margin-payment", label: "毛利與收款" }
];

const tabDescriptions: Record<OrderWorkspaceTab, string> = {
  overview: "以履約風險管理視角查看進行中訂單、交期、生產可行性與目前階段。",
  commitment: "以 ATP/CTP 檢核接單後是否可承諾交期，包含庫存、物料、產能、人員與品質/出貨限制。",
  "delivery-risk": "優先檢視交期與生產是否做得出來，包含缺料、產能、品檢與出貨阻擋。",
  fulfillment: "查看每張訂單從備料、生產、品檢、出貨到收款的履約 workflow。",
  "margin-payment": "第二順位追蹤預估/實際毛利，第三順位查看收款狀態。"
};

function formatNumber(value: number) {
  return new Intl.NumberFormat("zh-TW").format(value);
}

function formatMoney(value: number) {
  return `$${new Intl.NumberFormat("zh-TW").format(value)}`;
}

function riskTone(risk: OrderRiskLevel) {
  if (risk === "高風險") {
    return "danger";
  }

  if (risk === "注意") {
    return "warning";
  }

  return "success";
}

function commitmentTone(decision: SalesOrder["commitmentDecision"]) {
  if (decision === "不可承諾") {
    return "danger";
  }

  if (decision === "需協調") {
    return "warning";
  }

  return "success";
}

function getVisibleOrders(activeTab: OrderWorkspaceTab, orders: SalesOrder[]) {
  if (activeTab === "commitment") {
    return [...orders].sort((a, b) => {
      const rank = { "不可承諾": 0, "需協調": 1, "可承諾": 2 };
      return rank[a.commitmentDecision] - rank[b.commitmentDecision];
    });
  }

  if (activeTab === "delivery-risk") {
    return orders.filter((order) => order.deliveryRisk !== "正常");
  }

  if (activeTab === "margin-payment") {
    return [...orders].sort((a, b) => a.estimatedMarginRate - b.estimatedMarginRate);
  }

  return orders;
}

function KpiStrip({ summary }: { summary: OrderStatusSummary[] }) {
  const icons = [ClipboardList, CalendarClock, AlertTriangle, DollarSign];

  return (
    <section className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
      {summary.map((item, index) => {
        const Icon = icons[index] ?? ClipboardList;
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

function OrdersTable({
  activeTab,
  orders,
  selectedId,
  onSelect
}: {
  activeTab: OrderWorkspaceTab;
  orders: SalesOrder[];
  selectedId: string;
  onSelect: (order: SalesOrder) => void;
}) {
  const rows = useMemo(() => getVisibleOrders(activeTab, orders), [activeTab, orders]);

  return (
    <div className="overflow-hidden rounded-lg border border-border bg-white shadow-card">
      <div className="overflow-x-auto">
        <table className="min-w-[1180px] w-full border-collapse text-sm">
          <thead className="bg-slate-50 text-left text-xs font-semibold uppercase tracking-wide text-textSecondary">
            <tr>
              <th className="px-4 py-3">訂單 / 客戶</th>
              <th className="px-4 py-3">產品</th>
              <th className="px-4 py-3 text-right">數量</th>
              <th className="px-4 py-3 text-right">訂單金額</th>
              <th className="px-4 py-3">交期</th>
              <th className="px-4 py-3">接單承諾</th>
              <th className="px-4 py-3">生產可行性</th>
              <th className="px-4 py-3">履約狀態</th>
              <th className="px-4 py-3">毛利</th>
              <th className="px-4 py-3">收款</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {rows.map((order) => {
              const isSelected = order.id === selectedId;
              return (
                <tr
                  className={`cursor-pointer transition ${
                    isSelected ? "bg-info/10" : "hover:bg-slate-50"
                  }`}
                  key={order.id}
                  onClick={() => onSelect(order)}
                >
                  <td className="px-4 py-3">
                    <p className="font-semibold text-textPrimary">{order.id}</p>
                    <p className="mt-1 text-xs text-textSecondary">
                      {order.customer} · {order.channel}
                    </p>
                  </td>
                  <td className="px-4 py-3">
                    <p className="font-medium text-textPrimary">{order.product}</p>
                    <p className="mt-1 text-xs text-textSecondary">{order.itemNo}</p>
                  </td>
                  <td className="px-4 py-3 text-right font-semibold text-textPrimary">
                    {formatNumber(order.quantity)} {order.unit}
                  </td>
                  <td className="px-4 py-3 text-right text-textPrimary">{formatMoney(order.orderAmount)}</td>
                  <td className="px-4 py-3">
                    <StatusBadge tone={riskTone(order.deliveryRisk)}>{order.deliveryRisk}</StatusBadge>
                    <p className="mt-1 text-xs text-textSecondary">{order.dueDate}</p>
                  </td>
                  <td className="px-4 py-3">
                    <StatusBadge tone={commitmentTone(order.commitmentDecision)}>
                      {order.commitmentDecision}
                    </StatusBadge>
                    <p className="mt-1 text-xs text-textSecondary">可承諾 {order.committedDate}</p>
                  </td>
                  <td className="px-4 py-3">
                    <p className="font-medium text-textPrimary">{order.productionFeasibility}</p>
                    <p className="mt-1 line-clamp-2 text-xs text-textSecondary">{order.riskReason}</p>
                  </td>
                  <td className="px-4 py-3">
                    <StatusBadge tone={order.tone}>{order.stage}</StatusBadge>
                    <p className="mt-1 text-xs text-textSecondary">{order.productionStatus}</p>
                  </td>
                  <td className="px-4 py-3">
                    <p className="text-textPrimary">預估 {order.estimatedMarginRate}%</p>
                    <p className="mt-1 text-xs text-textSecondary">
                      實際 {order.actualMarginRate === null ? "未結算" : `${order.actualMarginRate}%`}
                    </p>
                  </td>
                  <td className="px-4 py-3 text-textPrimary">{order.paymentStatus}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function CommitmentCards({ orders }: { orders: SalesOrder[] }) {
  return (
    <div className="grid gap-3 lg:grid-cols-3">
      {orders.map((order) => (
        <div className="rounded-lg border border-border bg-white p-4 shadow-card" key={order.id}>
          <div className="flex items-start justify-between gap-3">
            <div>
              <StatusBadge tone={commitmentTone(order.commitmentDecision)}>
                {order.commitmentDecision}
              </StatusBadge>
              <h3 className="mt-3 font-semibold text-textPrimary">{order.id}</h3>
              <p className="mt-1 text-sm text-textSecondary">{order.product}</p>
            </div>
            <CheckCircle2 className="h-5 w-5 text-textSecondary" aria-hidden="true" />
          </div>
          <div className="mt-3 grid grid-cols-2 gap-2 text-sm">
            <div className="rounded-md bg-slate-50 p-3">
              <p className="text-xs text-textSecondary">客戶要求</p>
              <p className="mt-1 font-semibold text-textPrimary">{order.dueDate}</p>
            </div>
            <div className="rounded-md bg-slate-50 p-3">
              <p className="text-xs text-textSecondary">可承諾日</p>
              <p className="mt-1 font-semibold text-textPrimary">{order.committedDate}</p>
            </div>
          </div>
          <div className="mt-3 space-y-2">
            {order.commitmentChecks.slice(0, 3).map((check) => (
              <div className="flex items-start justify-between gap-3 text-sm" key={`${order.id}-${check.area}`}>
                <div>
                  <p className="font-medium text-textPrimary">{check.area}</p>
                  <p className="mt-1 line-clamp-2 text-xs text-textSecondary">{check.note}</p>
                </div>
                <StatusBadge tone={check.tone}>{check.status}</StatusBadge>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}

function RiskCards({ orders }: { orders: SalesOrder[] }) {
  return (
    <div className="grid gap-3 lg:grid-cols-3">
      {orders
        .filter((order) => order.deliveryRisk !== "正常")
        .map((order) => (
          <div className="rounded-lg border border-border bg-white p-4 shadow-card" key={order.id}>
            <div className="flex items-start justify-between gap-3">
              <div>
                <StatusBadge tone={riskTone(order.deliveryRisk)}>{order.deliveryRisk}</StatusBadge>
                <h3 className="mt-3 font-semibold text-textPrimary">{order.id}</h3>
                <p className="mt-1 text-sm text-textSecondary">{order.product}</p>
              </div>
              <CalendarClock className="h-5 w-5 text-textSecondary" aria-hidden="true" />
            </div>
            <p className="mt-3 text-sm leading-6 text-textSecondary">{order.riskReason}</p>
            <div className="mt-3 grid grid-cols-2 gap-2 text-sm">
              <div className="rounded-md bg-slate-50 p-3">
                <p className="text-xs text-textSecondary">交期</p>
                <p className="mt-1 font-semibold text-textPrimary">{order.dueDate}</p>
              </div>
              <div className="rounded-md bg-slate-50 p-3">
                <p className="text-xs text-textSecondary">生產</p>
                <p className="mt-1 font-semibold text-textPrimary">{order.productionFeasibility}</p>
              </div>
            </div>
          </div>
        ))}
    </div>
  );
}

function DetailPanel({ order }: { order: SalesOrder }) {
  return (
    <aside className="space-y-4 rounded-lg border border-border bg-white p-4 shadow-card xl:sticky xl:top-24">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-xs font-medium uppercase tracking-wide text-textSecondary">目前訂單</p>
          <h2 className="mt-1 text-lg font-semibold text-textPrimary">{order.id}</h2>
          <p className="mt-1 text-sm text-textSecondary">{order.customer}</p>
        </div>
        <StatusBadge tone={riskTone(order.deliveryRisk)}>{order.deliveryRisk}</StatusBadge>
      </div>

      <div className="grid grid-cols-2 gap-3 text-sm">
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">交期</p>
          <p className="mt-1 font-semibold text-textPrimary">{order.dueDate}</p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">生產可行性</p>
          <p className="mt-1 font-semibold text-textPrimary">{order.productionFeasibility}</p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">接單承諾</p>
          <p className="mt-1 font-semibold text-textPrimary">{order.commitmentDecision}</p>
          <p className="mt-1 text-xs text-textSecondary">可承諾 {order.committedDate}</p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">訂單金額</p>
          <p className="mt-1 font-semibold text-textPrimary">{formatMoney(order.orderAmount)}</p>
        </div>
        <div className="rounded-md bg-slate-50 p-3">
          <p className="text-xs text-textSecondary">毛利率</p>
          <p className="mt-1 font-semibold text-textPrimary">{order.estimatedMarginRate}% 預估</p>
          <p className="mt-1 text-xs text-textSecondary">
            實際 {order.actualMarginRate === null ? "未結算" : `${order.actualMarginRate}%`}
          </p>
        </div>
      </div>

      <div className="space-y-2">
        <p className="text-sm font-semibold text-textPrimary">接單承諾檢核</p>
        {order.commitmentChecks.map((item) => (
          <div className="rounded-md border border-border px-3 py-2" key={`${item.area}-${item.status}`}>
            <div className="flex items-center justify-between gap-3">
              <p className="font-medium text-textPrimary">{item.area}</p>
              <StatusBadge tone={item.tone}>{item.status}</StatusBadge>
            </div>
            <p className="mt-1 text-xs text-textSecondary">{item.note}</p>
          </div>
        ))}
      </div>

      <div className="space-y-2">
        <p className="text-sm font-semibold text-textPrimary">履約依賴</p>
        {order.dependencies.map((item) => (
          <div className="rounded-md border border-border px-3 py-2" key={`${item.area}-${item.status}`}>
            <div className="flex items-center justify-between gap-3">
              <p className="font-medium text-textPrimary">{item.area}</p>
              <StatusBadge tone={item.tone}>{item.status}</StatusBadge>
            </div>
            <p className="mt-1 text-xs text-textSecondary">{item.note}</p>
          </div>
        ))}
      </div>

      <div className="space-y-2">
        <p className="text-sm font-semibold text-textPrimary">履約流程</p>
        {order.workflow.map((step, index) => (
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
              {index < order.workflow.length - 1 ? <span className="h-7 w-px bg-border" /> : null}
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
  selectedOrder,
  onSelectOrder
}: {
  activeTab: OrderWorkspaceTab;
  data: OrdersDashboardData;
  selectedOrder: SalesOrder;
  onSelectOrder: (order: SalesOrder) => void;
}) {
  if (activeTab === "commitment") {
    return (
      <div className="space-y-4">
        <CommitmentCards orders={data.orders} />
        <OrdersTable
          activeTab={activeTab}
          orders={data.orders}
          selectedId={selectedOrder.id}
          onSelect={onSelectOrder}
        />
      </div>
    );
  }

  if (activeTab === "delivery-risk") {
    return (
      <div className="space-y-4">
        <RiskCards orders={data.orders} />
        <OrdersTable
          activeTab={activeTab}
          orders={data.orders}
          selectedId={selectedOrder.id}
          onSelect={onSelectOrder}
        />
      </div>
    );
  }

  return (
    <OrdersTable
      activeTab={activeTab}
      orders={data.orders}
      selectedId={selectedOrder.id}
      onSelect={onSelectOrder}
    />
  );
}

export default function OrdersPage() {
  const { data: ordersData, error, isLoading, source } = useOrdersDashboard();
  const [activeTab, setActiveTab] = useState<OrderWorkspaceTab>("overview");
  const [selectedOrderId, setSelectedOrderId] = useState<string>(ordersData.orders[0].id);
  const selectedOrder =
    ordersData.orders.find((order) => order.id === selectedOrderId) ?? ordersData.orders[0];

  return (
    <AppLayout activePath="/orders" title="訂單履約 Orders Workspace">
      <div className="mx-auto max-w-[1480px] space-y-5">
        <section className="rounded-lg border border-border bg-white p-4 shadow-card">
          <div className="flex flex-col gap-4 xl:flex-row xl:items-center xl:justify-between">
            <div>
              <div className="flex flex-wrap items-center gap-2">
                <StatusBadge tone="info">EWDB 20260522</StatusBadge>
                <StatusBadge tone="neutral">接單承諾 / 交期 / 生產可行性 / 毛利 / 收款</StatusBadge>
                <StatusBadge tone={source === "api" ? "success" : "warning"}>
                  {source === "api" ? "API data" : "Mock fallback"}
                </StatusBadge>
                {isLoading ? <StatusBadge tone="info">Loading API</StatusBadge> : null}
              </div>
              <h2 className="mt-3 text-2xl font-semibold text-textPrimary">訂單承諾與履約風險總覽</h2>
              <p className="mt-2 max-w-3xl text-sm leading-6 text-textSecondary">
                先以 ATP/CTP 判斷接單後是否可承諾交期，再以交期與生產是否做得出來為第一順位，
                串接庫存、備料、生產、品檢與出貨狀態；
                毛利為第二順位，收款為第三順位，先支援管理者掌握履約風險。
              </p>
            </div>
            <div className="grid gap-2 sm:grid-cols-[minmax(220px,1fr)_auto_auto]">
              <label className="flex h-10 items-center gap-2 rounded-input border border-border bg-slate-50 px-3">
                <Search className="h-4 w-4 text-textSecondary" aria-hidden="true" />
                <input
                  className="w-full bg-transparent text-sm outline-none placeholder:text-textSecondary"
                  placeholder="訂單 / 客戶 / 產品 / 交期"
                />
              </label>
              <button className="inline-flex h-10 items-center justify-center gap-2 rounded-button border border-border bg-white px-3 text-sm font-medium text-textSecondary">
                <Filter className="h-4 w-4" aria-hidden="true" />
                篩選
              </button>
              <button className="inline-flex h-10 items-center justify-center gap-2 rounded-button bg-primary px-3 text-sm font-medium text-white">
                <Truck className="h-4 w-4" aria-hidden="true" />
                履約
              </button>
            </div>
          </div>
        </section>

        {error ? (
          <p className="rounded-lg border border-warning/20 bg-warning/10 px-4 py-3 text-sm text-warning">
            Orders API 尚未可用，已使用 mock fallback。{error}
          </p>
        ) : null}

        <KpiStrip summary={ordersData.summary} />

        <section className="grid gap-5 xl:grid-cols-[minmax(0,1fr)_390px]">
          <div className="space-y-4">
            <div className="rounded-lg border border-border bg-white p-3 shadow-card">
              <div className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
                <div>
                  <p className="text-xs font-medium uppercase tracking-wide text-textSecondary">訂單視圖</p>
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
              data={ordersData}
              selectedOrder={selectedOrder}
              onSelectOrder={(order) => setSelectedOrderId(order.id)}
            />
          </div>

          <DetailPanel order={selectedOrder} />
        </section>
      </div>
    </AppLayout>
  );
}
