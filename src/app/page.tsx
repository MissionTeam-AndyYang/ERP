import Link from "next/link";
import {
  ArrowRight,
  ClipboardCheck,
  DollarSign,
  Factory,
  ShieldAlert,
  TimerReset
} from "lucide-react";
import { AlertDistributionChart } from "@/components/charts/alert-distribution-chart";
import { OeeTrendChart } from "@/components/charts/oee-trend-chart";
import { ProductionTrendChart } from "@/components/charts/production-trend-chart";
import { QualityTrendChart } from "@/components/charts/quality-trend-chart";
import { AlertCard } from "@/components/dashboard/alert-card";
import { KpiCard } from "@/components/dashboard/kpi-card";
import { ProductionLineCard } from "@/components/dashboard/production-line-card";
import { StatusBadge } from "@/components/ui/status-badge";
import { AppLayout } from "@/layouts/app-layout";
import {
  alertDistributionData,
  alertItems,
  departmentBlockers,
  kpiItems,
  managerDecisionItems,
  managerFocusItems,
  managerSnapshot,
  moduleShortcuts,
  oeeTrendData,
  preOrderPipeline,
  productionLines,
  productionTrendData,
  qualityTrendData,
  todayTasks
} from "@/mock/dashboard";
import type { StatusTone } from "@/types/dashboard";

const tonePanelStyles: Record<StatusTone, string> = {
  success: "border-success/20 bg-success/5 text-success",
  warning: "border-warning/20 bg-warning/5 text-warning",
  danger: "border-danger/20 bg-danger/5 text-danger",
  info: "border-info/20 bg-info/5 text-info",
  neutral: "border-slate-200 bg-slate-50 text-slate-600"
};

const toneDotStyles: Record<StatusTone, string> = {
  success: "bg-success",
  warning: "bg-warning",
  danger: "bg-danger",
  info: "bg-info",
  neutral: "bg-slate-400"
};

export default function HomePage() {
  return (
    <AppLayout title="管理者 Dashboard">
      <div className="mx-auto max-w-[1440px] space-y-6">
        <section className="grid gap-4 rounded-card bg-primaryDark p-6 text-white shadow-card xl:grid-cols-[1fr_420px]">
          <div>
            <StatusBadge tone="info">Manager View</StatusBadge>
            <h2 className="mt-4 text-2xl font-semibold md:text-3xl">
              今日營運協調與履約風險
            </h2>
            <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-300">
              以管理者每天需要處理的決策為中心，彙整接單承諾、開發報價、排程備料、倉位、品保、生產、物流與毛利訊號。
            </p>
            <div className="mt-5 flex flex-wrap gap-2">
              {moduleShortcuts.map((item) => {
                const Icon = item.icon;
                return (
                  <Link
                    className="inline-flex h-10 items-center gap-2 rounded-button bg-white/10 px-3 text-sm font-medium text-white transition hover:bg-white/20"
                    href={item.href}
                    key={item.href}
                  >
                    <Icon className="h-4 w-4" aria-hidden="true" />
                    {item.label}
                  </Link>
                );
              })}
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3 rounded-card bg-white/10 p-4">
            <div>
              <p className="text-xs text-slate-300">履約風險</p>
              <p className="mt-1 text-3xl font-bold">{managerSnapshot.fulfillmentRisk}</p>
            </div>
            <div>
              <p className="text-xs text-slate-300">交付承諾率</p>
              <p className="mt-1 text-3xl font-bold">{managerSnapshot.deliveryCommitment}</p>
            </div>
            <div>
              <p className="text-xs text-slate-300">預估毛利</p>
              <p className="mt-1 text-3xl font-bold">{managerSnapshot.marginSignal}</p>
            </div>
            <div>
              <p className="text-xs text-slate-300">待收款訊號</p>
              <p className="mt-1 text-3xl font-bold">{managerSnapshot.cashSignal}</p>
            </div>
          </div>
        </section>

        <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {managerFocusItems.map((item) => {
            const Icon = item.icon;
            return (
              <article
                className="rounded-card border border-border bg-white p-5 shadow-card"
                key={item.label}
              >
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <p className="text-sm font-medium text-textSecondary">{item.label}</p>
                    <div className="mt-3 flex items-end gap-2">
                      <strong className="text-4xl font-bold leading-none text-textPrimary">
                        {item.value}
                      </strong>
                      {item.label === "預估毛利" ? (
                        <span className="pb-1 text-sm font-medium text-textSecondary">%</span>
                      ) : null}
                    </div>
                  </div>
                  <div className={`rounded-button border p-3 ${tonePanelStyles[item.tone]}`}>
                    <Icon className="h-5 w-5" aria-hidden="true" />
                  </div>
                </div>
                <p className="mt-4 text-sm leading-6 text-textSecondary">{item.detail}</p>
              </article>
            );
          })}
        </section>

        <section className="grid gap-6 xl:grid-cols-[1.1fr_0.9fr]">
          <article className="rounded-card border border-border bg-white p-5 shadow-card">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div>
                <p className="text-sm font-medium text-textSecondary">Decision Center</p>
                <h2 className="text-xl font-semibold text-textPrimary">主管今日待決策</h2>
              </div>
              <StatusBadge tone="danger">3 件會影響交期</StatusBadge>
            </div>
            <div className="mt-5 space-y-3">
              {managerDecisionItems.map((item) => (
                <div
                  className="rounded-card border border-border bg-slate-50 p-4"
                  key={item.title}
                >
                  <div className="flex flex-wrap items-start justify-between gap-3">
                    <div>
                      <div className="flex items-center gap-2">
                        <span className={`h-2.5 w-2.5 rounded-full ${toneDotStyles[item.tone]}`} />
                        <h3 className="font-semibold text-textPrimary">{item.title}</h3>
                      </div>
                      <p className="mt-2 text-sm leading-6 text-textSecondary">{item.impact}</p>
                    </div>
                    <StatusBadge tone={item.tone}>{item.due}</StatusBadge>
                  </div>
                  <div className="mt-4 grid gap-3 text-sm md:grid-cols-3">
                    <p>
                      <span className="text-textSecondary">負責：</span>
                      <span className="font-medium text-textPrimary">{item.owner}</span>
                    </p>
                    <p className="md:col-span-2">
                      <span className="text-textSecondary">建議動作：</span>
                      <span className="font-medium text-textPrimary">{item.action}</span>
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </article>

          <article className="rounded-card border border-border bg-white p-5 shadow-card">
            <div>
              <p className="text-sm font-medium text-textSecondary">Today Work Queue</p>
              <h2 className="text-xl font-semibold text-textPrimary">今日跨部門待辦</h2>
            </div>
            <div className="mt-5 space-y-3">
              {todayTasks.map((task) => (
                <div className="grid grid-cols-[68px_1fr] gap-3" key={`${task.time}-${task.title}`}>
                  <p className="pt-1 text-sm font-semibold text-textSecondary">{task.time}</p>
                  <div className="rounded-card border border-border bg-white p-3">
                    <div className="flex flex-wrap items-center justify-between gap-2">
                      <p className="text-xs font-medium text-textSecondary">{task.module}</p>
                      <StatusBadge tone={task.tone}>{task.status}</StatusBadge>
                    </div>
                    <p className="mt-2 text-sm font-semibold text-textPrimary">{task.title}</p>
                  </div>
                </div>
              ))}
            </div>
          </article>
        </section>

        <section className="grid gap-6 xl:grid-cols-[1fr_380px]">
          <article className="rounded-card border border-border bg-white p-5 shadow-card">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div>
                <p className="text-sm font-medium text-textSecondary">Department Blockers</p>
                <h2 className="text-xl font-semibold text-textPrimary">跨部門卡點</h2>
              </div>
              <StatusBadge tone="warning">需主管協調</StatusBadge>
            </div>
            <div className="mt-5 grid gap-4 md:grid-cols-2">
              {departmentBlockers.map((item) => (
                <Link
                  className="group rounded-card border border-border bg-slate-50 p-4 transition hover:border-primary/40 hover:bg-white"
                  href={item.href}
                  key={`${item.department}-${item.title}`}
                >
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <p className="text-xs font-medium text-textSecondary">{item.department}</p>
                      <h3 className="mt-1 font-semibold text-textPrimary">{item.title}</h3>
                    </div>
                    <StatusBadge tone={item.tone}>{item.owner}</StatusBadge>
                  </div>
                  <p className="mt-3 text-sm leading-6 text-textSecondary">{item.detail}</p>
                  <div className="mt-4 flex items-center gap-2 text-sm font-medium text-primary">
                    {item.relatedModule}
                    <ArrowRight className="h-4 w-4 transition group-hover:translate-x-1" />
                  </div>
                </Link>
              ))}
            </div>
          </article>

          <article className="rounded-card border border-border bg-white p-5 shadow-card">
            <div>
              <p className="text-sm font-medium text-textSecondary">Pre-order Pipeline</p>
              <h2 className="text-xl font-semibold text-textPrimary">接單前開發與報價</h2>
            </div>
            <div className="mt-5 space-y-3">
              {preOrderPipeline.map((item) => (
                <div className="rounded-card border border-border bg-slate-50 p-4" key={item.stage}>
                  <div className="flex items-center justify-between gap-3">
                    <div>
                      <p className="text-sm font-semibold text-textPrimary">{item.stage}</p>
                      <p className="mt-1 text-xs text-textSecondary">{item.owner}</p>
                    </div>
                    <StatusBadge tone={item.tone}>{item.count} 件</StatusBadge>
                  </div>
                  <p className="mt-3 text-sm leading-6 text-textSecondary">{item.focus}</p>
                </div>
              ))}
            </div>
          </article>
        </section>

        <section className="grid gap-6 xl:grid-cols-[1.35fr_1fr]">
          <ProductionTrendChart data={productionTrendData} />
          <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-1">
            <OeeTrendChart data={oeeTrendData} />
            <AlertDistributionChart data={alertDistributionData} />
          </div>
        </section>

        <section className="grid gap-6 xl:grid-cols-[1fr_380px]">
          <QualityTrendChart data={qualityTrendData} />
          <article className="rounded-card border border-border bg-white p-5 shadow-card">
            <p className="text-sm font-medium text-textSecondary">Manager Insight</p>
            <h3 className="text-lg font-semibold text-textPrimary">今日營運判讀</h3>
            <div className="mt-5 space-y-4">
              <div className="rounded-button bg-danger/10 p-4">
                <div className="flex items-center gap-2 text-danger">
                  <ShieldAlert className="h-4 w-4" aria-hidden="true" />
                  <p className="text-sm font-semibold">履約優先處理</p>
                </div>
                <p className="mt-1 text-sm leading-6 text-textSecondary">
                  SO-240523-018 受急單插單與替代料放行影響，建議先完成接單承諾判定。
                </p>
              </div>
              <div className="rounded-button bg-warning/10 p-4">
                <div className="flex items-center gap-2 text-warning">
                  <TimerReset className="h-4 w-4" aria-hidden="true" />
                  <p className="text-sm font-semibold">倉位需提前調度</p>
                </div>
                <p className="mt-1 text-sm leading-6 text-textSecondary">
                  冷凍庫本週五到貨後剩餘板數偏低，需決定寄倉或提前出貨。
                </p>
              </div>
              <div className="rounded-button bg-success/10 p-4">
                <div className="flex items-center gap-2 text-success">
                  <DollarSign className="h-4 w-4" aria-hidden="true" />
                  <p className="text-sm font-semibold">毛利維持可接單區間</p>
                </div>
                <p className="mt-1 text-sm leading-6 text-textSecondary">
                  本週新報價平均毛利仍高於底線，但雞肉原料合約價格需採購追蹤。
                </p>
              </div>
            </div>
          </article>
        </section>

        <section className="grid gap-6 xl:grid-cols-[1fr_380px]">
          <div className="space-y-4">
            <div className="flex items-center justify-between gap-4">
              <div>
                <p className="text-sm font-medium text-textSecondary">Production Lines</p>
                <h2 className="text-xl font-semibold text-textPrimary">產線即時狀態</h2>
              </div>
              <StatusBadge tone="success">6 條正常運轉</StatusBadge>
            </div>
            <div className="grid gap-4 lg:grid-cols-3">
              {productionLines.map((line) => (
                <ProductionLineCard line={line} key={line.batchNo} />
              ))}
            </div>
          </div>

          <aside className="space-y-4">
            <div>
              <p className="text-sm font-medium text-textSecondary">Alert Center</p>
              <h2 className="text-xl font-semibold text-textPrimary">異常與提醒</h2>
            </div>
            <div className="space-y-3">
              {alertItems.map((item) => (
                <AlertCard item={item} key={item.title} />
              ))}
            </div>
          </aside>
        </section>

        <section className="grid gap-4 lg:grid-cols-3">
          <article className="rounded-card border border-border bg-white p-5 shadow-card">
            <div className="flex items-center gap-3">
              <div className="rounded-button bg-primary/10 p-3 text-primary">
                <Factory className="h-5 w-5" aria-hidden="true" />
              </div>
              <div>
                <h3 className="font-semibold text-textPrimary">產能稼動</h3>
                <p className="text-sm text-textSecondary">今日整體稼動率 84%</p>
              </div>
            </div>
          </article>
          <article className="rounded-card border border-border bg-white p-5 shadow-card">
            <div className="flex items-center gap-3">
              <div className="rounded-button bg-success/10 p-3 text-success">
                <ClipboardCheck className="h-5 w-5" aria-hidden="true" />
              </div>
              <div>
                <h3 className="font-semibold text-textPrimary">出貨達成</h3>
                <p className="text-sm text-textSecondary">本日訂單達成率 91%</p>
              </div>
            </div>
          </article>
          <article className="rounded-card border border-border bg-white p-5 shadow-card">
            <div className="flex items-center gap-3">
              <div className="rounded-button bg-warning/10 p-3 text-warning">
                <TimerReset className="h-5 w-5" aria-hidden="true" />
              </div>
              <div>
                <h3 className="font-semibold text-textPrimary">待處理工單</h3>
                <p className="text-sm text-textSecondary">4 張工單需排程確認</p>
              </div>
            </div>
          </article>
        </section>
      </div>
    </AppLayout>
  );
}
