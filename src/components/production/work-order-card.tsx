import { Clock, Package, UserRound } from "lucide-react";
import { StatusBadge } from "@/components/ui/status-badge";
import { WorkflowStepper } from "@/components/production/workflow-stepper";
import type { WorkOrder, WorkOrderStage } from "@/types/production";

type WorkOrderCardProps = {
  order: WorkOrder;
  stages: WorkOrderStage[];
};

export function WorkOrderCard({ order, stages }: WorkOrderCardProps) {
  return (
    <article className="rounded-card border border-border bg-white p-5 shadow-card">
      <div className="flex items-start justify-between gap-4">
        <div className="min-w-0">
          <p className="text-sm font-semibold text-primary">{order.id}</p>
          <h3 className="mt-1 truncate text-lg font-semibold text-textPrimary">{order.product}</h3>
          <p className="mt-1 text-xs text-textSecondary">批號 {order.batchNo}</p>
        </div>
        <StatusBadge tone={order.tone}>{order.stage}</StatusBadge>
      </div>

      <div className="mt-5">
        <WorkflowStepper stages={stages} currentStage={order.stage} />
      </div>

      <div className="mt-5">
        <div className="mb-2 flex justify-between text-sm">
          <span className="font-medium text-textPrimary">工單進度</span>
          <span className="text-textSecondary">{order.progress}%</span>
        </div>
        <div className="h-2 overflow-hidden rounded-full bg-slate-100">
          <div className="h-full rounded-full bg-primary" style={{ width: `${order.progress}%` }} />
        </div>
      </div>

      <div className="mt-5 grid gap-3 text-sm sm:grid-cols-3">
        <div className="rounded-button bg-slate-50 p-3">
          <div className="flex items-center gap-2 text-textSecondary">
            <Package className="h-4 w-4" aria-hidden="true" />
            <span>產量</span>
          </div>
          <p className="mt-1 font-semibold text-textPrimary">
            {order.completedQty.toLocaleString()} / {order.plannedQty.toLocaleString()}
          </p>
        </div>
        <div className="rounded-button bg-slate-50 p-3">
          <div className="flex items-center gap-2 text-textSecondary">
            <Clock className="h-4 w-4" aria-hidden="true" />
            <span>預計</span>
          </div>
          <p className="mt-1 font-semibold text-textPrimary">{order.eta}</p>
        </div>
        <div className="rounded-button bg-slate-50 p-3">
          <div className="flex items-center gap-2 text-textSecondary">
            <UserRound className="h-4 w-4" aria-hidden="true" />
            <span>負責</span>
          </div>
          <p className="mt-1 font-semibold text-textPrimary">{order.owner}</p>
        </div>
      </div>

      <div className="mt-4 flex items-center justify-between border-t border-border pt-4 text-sm">
        <span className="text-textSecondary">{order.line}</span>
        <span className="font-medium text-textPrimary">優先度：{order.priority}</span>
      </div>
    </article>
  );
}
