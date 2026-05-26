type SupportEmptyStateProps = {
  title: string;
  description: string;
};

export function SupportEmptyState({ title, description }: SupportEmptyStateProps) {
  return (
    <div className="rounded-lg border border-dashed border-border bg-slate-50 px-4 py-10 text-center">
      <p className="font-semibold text-textPrimary">{title}</p>
      <p className="mt-2 text-sm text-textSecondary">{description}</p>
    </div>
  );
}
