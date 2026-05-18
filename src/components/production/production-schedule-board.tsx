import { StatusBadge } from "@/components/ui/status-badge";
import type { ProductionScheduleItem } from "@/types/production";

type ProductionScheduleBoardProps = {
  schedule: ProductionScheduleItem[];
};

export function ProductionScheduleBoard({ schedule }: ProductionScheduleBoardProps) {
  return (
    <article className="rounded-card border border-border bg-white p-5 shadow-card">
      <div className="flex items-center justify-between gap-4">
        <div>
          <p className="text-sm font-medium text-textSecondary">Line Schedule</p>
          <h2 className="text-xl font-semibold text-textPrimary">產線排程看板</h2>
        </div>
        <StatusBadge tone="info">今日班表</StatusBadge>
      </div>

      <div className="mt-5 grid gap-4 xl:grid-cols-4">
        {schedule.map((line) => (
          <section className="rounded-card border border-border bg-slate-50 p-4" key={line.line}>
            <div className="mb-4 flex items-center justify-between">
              <h3 className="font-semibold text-textPrimary">{line.line} 產線</h3>
              <span className="text-xs text-textSecondary">{line.slots.length} 筆</span>
            </div>
            <div className="space-y-3">
              {line.slots.map((slot) => (
                <div className="rounded-button bg-white p-3 shadow-card" key={`${line.line}-${slot.time}`}>
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <p className="text-xs font-medium text-textSecondary">{slot.time}</p>
                      <p className="mt-1 text-sm font-semibold text-textPrimary">{slot.product}</p>
                      <p className="mt-1 text-xs text-textSecondary">{slot.workOrderId}</p>
                    </div>
                    <StatusBadge tone={slot.tone}>{slot.stage}</StatusBadge>
                  </div>
                </div>
              ))}
            </div>
          </section>
        ))}
      </div>
    </article>
  );
}
