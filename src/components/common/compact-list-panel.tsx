import { StatusBadge } from "@/components/ui/status-badge";
import type { StatusTone } from "@/types/dashboard";

type CompactListItem = {
  id: string;
  title: string;
  detail: string;
  meta: string;
  status: string;
  tone: StatusTone;
};

type CompactListPanelProps = {
  eyebrow: string;
  title: string;
  items: CompactListItem[];
};

export function CompactListPanel({ eyebrow, title, items }: CompactListPanelProps) {
  return (
    <article className="rounded-card border border-border bg-white p-5 shadow-card">
      <div>
        <p className="text-sm font-medium text-textSecondary">{eyebrow}</p>
        <h2 className="text-xl font-semibold text-textPrimary">{title}</h2>
      </div>
      <div className="mt-5 space-y-3">
        {items.map((item) => (
          <div className="rounded-card border border-border p-4" key={item.id}>
            <div className="flex items-start justify-between gap-3">
              <div className="min-w-0">
                <p className="text-sm font-semibold text-primary">{item.id}</p>
                <h3 className="mt-1 truncate text-base font-semibold text-textPrimary">{item.title}</h3>
                <p className="mt-1 text-sm leading-6 text-textSecondary">{item.detail}</p>
                <p className="mt-2 text-xs text-textSecondary">{item.meta}</p>
              </div>
              <StatusBadge tone={item.tone}>{item.status}</StatusBadge>
            </div>
          </div>
        ))}
      </div>
    </article>
  );
}
