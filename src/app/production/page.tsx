import { ClipboardList, Factory, Layers3 } from "lucide-react";
import { ProductionScheduleBoard } from "@/components/production/production-schedule-board";
import { ProductionSummaryCard } from "@/components/production/production-summary-card";
import { WorkOrderCard } from "@/components/production/work-order-card";
import { StatusBadge } from "@/components/ui/status-badge";
import { AppLayout } from "@/layouts/app-layout";
import {
  productionSchedule,
  productionSummary,
  workOrders,
  workflowStages
} from "@/mock/production";

export default function ProductionPage() {
  return (
    <AppLayout activePath="/production" title="生產中心 Production Module">
      <div className="mx-auto max-w-[1440px] space-y-6">
        <section className="flex flex-col justify-between gap-4 rounded-card bg-primaryDark p-6 text-white shadow-card md:flex-row md:items-center">
          <div>
            <StatusBadge tone="info">Sprint 3 Production</StatusBadge>
            <h2 className="mt-4 text-2xl font-semibold md:text-3xl">生產工單與排程控制台</h2>
            <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-300">
              以工單為核心串接產線、批號、Workflow、進度與排程，讓生管、現場與品保能用同一個畫面協作。
            </p>
          </div>
          <div className="grid grid-cols-3 gap-3 rounded-card bg-white/10 p-4 text-center">
            <div>
              <ClipboardList className="mx-auto h-5 w-5 text-slate-300" aria-hidden="true" />
              <p className="mt-2 text-2xl font-bold">12</p>
              <p className="text-xs text-slate-300">今日工單</p>
            </div>
            <div>
              <Factory className="mx-auto h-5 w-5 text-slate-300" aria-hidden="true" />
              <p className="mt-2 text-2xl font-bold">4</p>
              <p className="text-xs text-slate-300">產線排程</p>
            </div>
            <div>
              <Layers3 className="mx-auto h-5 w-5 text-slate-300" aria-hidden="true" />
              <p className="mt-2 text-2xl font-bold">5</p>
              <p className="text-xs text-slate-300">流程階段</p>
            </div>
          </div>
        </section>

        <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {productionSummary.map((item) => (
            <ProductionSummaryCard item={item} key={item.label} />
          ))}
        </section>

        <ProductionScheduleBoard schedule={productionSchedule} />

        <section className="space-y-4">
          <div className="flex flex-col justify-between gap-3 md:flex-row md:items-center">
            <div>
              <p className="text-sm font-medium text-textSecondary">Work Orders</p>
              <h2 className="text-xl font-semibold text-textPrimary">工單列表與 Workflow</h2>
            </div>
            <div className="flex flex-wrap gap-2">
              {workflowStages.map((stage) => (
                <StatusBadge tone={stage === "完工" ? "neutral" : "info"} key={stage}>
                  {stage}
                </StatusBadge>
              ))}
            </div>
          </div>

          <div className="grid gap-4 xl:grid-cols-2">
            {workOrders.map((order) => (
              <WorkOrderCard order={order} stages={workflowStages} key={order.id} />
            ))}
          </div>
        </section>
      </div>
    </AppLayout>
  );
}
