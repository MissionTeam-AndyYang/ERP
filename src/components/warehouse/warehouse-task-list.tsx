import { ClipboardCheck } from "lucide-react";
import { StatusBadge } from "@/components/ui/status-badge";
import type { WarehouseTask } from "@/types/warehouse";

type WarehouseTaskListProps = {
  tasks: WarehouseTask[];
};

export function WarehouseTaskList({ tasks }: WarehouseTaskListProps) {
  return (
    <article className="rounded-card border border-border bg-white p-5 shadow-card">
      <div className="flex items-center justify-between gap-4">
        <div>
          <p className="text-sm font-medium text-textSecondary">Inbound / Outbound</p>
          <h2 className="text-xl font-semibold text-textPrimary">入庫 / 出庫任務</h2>
        </div>
        <div className="rounded-button bg-primary/10 p-3 text-primary">
          <ClipboardCheck className="h-5 w-5" aria-hidden="true" />
        </div>
      </div>

      <div className="mt-5 space-y-3">
        {tasks.map((task) => (
          <div className="rounded-card border border-border p-4" key={task.id}>
            <div className="flex items-start justify-between gap-3">
              <div className="min-w-0">
                <p className="text-sm font-semibold text-primary">{task.id}</p>
                <h3 className="mt-1 truncate text-base font-semibold text-textPrimary">{task.itemName}</h3>
                <p className="mt-1 text-xs text-textSecondary">{task.batchNo}</p>
              </div>
              <StatusBadge tone={task.tone}>{task.type}</StatusBadge>
            </div>
            <div className="mt-4 grid grid-cols-3 gap-3 rounded-button bg-slate-50 p-3 text-sm">
              <div>
                <p className="text-xs text-textSecondary">數量</p>
                <p className="mt-1 font-semibold text-textPrimary">
                  {task.quantity.toLocaleString()} {task.unit}
                </p>
              </div>
              <div>
                <p className="text-xs text-textSecondary">負責</p>
                <p className="mt-1 font-semibold text-textPrimary">{task.owner}</p>
              </div>
              <div>
                <p className="text-xs text-textSecondary">期限</p>
                <p className="mt-1 font-semibold text-textPrimary">{task.dueTime}</p>
              </div>
            </div>
            <div className="mt-3 flex justify-end">
              <StatusBadge tone={task.tone}>{task.status}</StatusBadge>
            </div>
          </div>
        ))}
      </div>
    </article>
  );
}
