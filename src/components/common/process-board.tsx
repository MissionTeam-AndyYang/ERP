import { StatusBadge } from "@/components/ui/status-badge";
import type { StatusTone } from "@/types/dashboard";

type ProcessColumn = {
  title: string;
  items: {
    id: string;
    title: string;
    detail: string;
    tone: StatusTone;
  }[];
};

type ProcessBoardProps = {
  eyebrow: string;
  title: string;
  columns: ProcessColumn[];
};

export function ProcessBoard({ eyebrow, title, columns }: ProcessBoardProps) {
  return (
    <article className="rounded-card border border-border bg-white p-5 shadow-card">
      <div>
        <p className="text-sm font-medium text-textSecondary">{eyebrow}</p>
        <h2 className="text-xl font-semibold text-textPrimary">{title}</h2>
      </div>
      <div className="mt-5 grid gap-4 xl:grid-cols-4">
        {columns.map((column) => (
          <section className="rounded-card border border-border bg-slate-50 p-4" key={column.title}>
            <div className="mb-4 flex items-center justify-between">
              <h3 className="font-semibold text-textPrimary">{column.title}</h3>
              <span className="text-xs text-textSecondary">{column.items.length} 筆</span>
            </div>
            <div className="space-y-3">
              {column.items.map((item) => (
                <div className="rounded-button bg-white p-3 shadow-card" key={item.id}>
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <p className="text-xs font-medium text-textSecondary">{item.id}</p>
                      <p className="mt-1 text-sm font-semibold text-textPrimary">{item.title}</p>
                      <p className="mt-1 text-xs leading-5 text-textSecondary">{item.detail}</p>
                    </div>
                    <StatusBadge tone={item.tone}>{column.title}</StatusBadge>
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
