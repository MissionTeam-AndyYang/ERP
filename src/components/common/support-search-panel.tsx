import { Search } from "lucide-react";

type SupportSearchPanelProps = {
  ariaLabel: string;
  placeholder: string;
  value: string;
  onChange: (value: string) => void;
};

export function SupportSearchPanel({ ariaLabel, placeholder, value, onChange }: SupportSearchPanelProps) {
  return (
    <section className="rounded-lg border border-border bg-white p-4 shadow-card">
      <label className="flex h-10 max-w-xl items-center gap-2 rounded-input border border-border bg-slate-50 px-3">
        <Search className="h-4 w-4 text-textSecondary" aria-hidden="true" />
        <input
          aria-label={ariaLabel}
          className="w-full bg-transparent text-sm outline-none placeholder:text-textSecondary"
          placeholder={placeholder}
          value={value}
          onChange={(event) => onChange(event.target.value)}
        />
      </label>
    </section>
  );
}
