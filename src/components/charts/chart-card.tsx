type ChartCardProps = {
  title: string;
  subtitle: string;
  children: React.ReactNode;
};

export function ChartCard({ title, subtitle, children }: ChartCardProps) {
  return (
    <article className="rounded-card border border-border bg-white p-5 shadow-card">
      <div className="mb-4">
        <p className="text-sm font-medium text-textSecondary">{subtitle}</p>
        <h3 className="text-lg font-semibold text-textPrimary">{title}</h3>
      </div>
      {children}
    </article>
  );
}
