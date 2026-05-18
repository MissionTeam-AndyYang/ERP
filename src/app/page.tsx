import { TimerReset, TrendingUp } from "lucide-react";
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
  kpiItems,
  lineSummary,
  oeeTrendData,
  productionLines,
  productionTrendData,
  qualityTrendData
} from "@/mock/dashboard";

export default function HomePage() {
  const SummaryIcon = lineSummary.icon;

  return (
    <AppLayout>
      <div className="mx-auto max-w-[1440px] space-y-6">
        <section className="flex flex-col justify-between gap-4 rounded-card bg-primaryDark p-6 text-white shadow-card md:flex-row md:items-center">
          <div>
            <StatusBadge tone="info">Sprint 2 Dashboard</StatusBadge>
            <h2 className="mt-4 text-2xl font-semibold md:text-3xl">
              今日工廠營運總覽
            </h2>
            <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-300">
              即時掌握產量、良率、OEE、產線狀態、趨勢圖表與異常分類，作為生產早會與現場調度的共用畫面。
            </p>
          </div>
          <div className="grid grid-cols-3 gap-3 rounded-card bg-white/10 p-4 text-center">
            <div>
              <p className="text-2xl font-bold">{lineSummary.active}</p>
              <p className="text-xs text-slate-300">生產中</p>
            </div>
            <div>
              <p className="text-2xl font-bold">{lineSummary.idle}</p>
              <p className="text-xs text-slate-300">待料</p>
            </div>
            <div>
              <p className="text-2xl font-bold">{lineSummary.cleaning}</p>
              <p className="text-xs text-slate-300">清洗中</p>
            </div>
          </div>
        </section>

        <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {kpiItems.map((item) => (
            <KpiCard item={item} key={item.title} />
          ))}
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
            <p className="text-sm font-medium text-textSecondary">Sprint 2 Insight</p>
            <h3 className="text-lg font-semibold text-textPrimary">今日營運判讀</h3>
            <div className="mt-5 space-y-4">
              <div className="rounded-button bg-success/10 p-4">
                <p className="text-sm font-semibold text-success">產量領先計畫</p>
                <p className="mt-1 text-sm leading-6 text-textSecondary">
                  14:00 實際累積產量高於計畫 540 盒，A1 產線表現穩定。
                </p>
              </div>
              <div className="rounded-button bg-warning/10 p-4">
                <p className="text-sm font-semibold text-warning">缺料風險需追蹤</p>
                <p className="mt-1 text-sm leading-6 text-textSecondary">
                  B2 產線待料會影響下午產能，建議倉儲先處理玉米粒補料。
                </p>
              </div>
              <div className="rounded-button bg-info/10 p-4">
                <p className="text-sm font-semibold text-info">OEE 已接近目標</p>
                <p className="mt-1 text-sm leading-6 text-textSecondary">
                  目前 OEE 來到 89%，可作為晚班排程基準。
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
                <SummaryIcon className="h-5 w-5" aria-hidden="true" />
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
                <TrendingUp className="h-5 w-5" aria-hidden="true" />
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
