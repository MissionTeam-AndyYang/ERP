export type DataSourceMode = "api" | "mock";

type DataSourceToggleProps = {
  value: DataSourceMode;
  onChange: (value: DataSourceMode) => void;
};

export function DataSourceToggle({ value, onChange }: DataSourceToggleProps) {
  return (
    <div className="inline-flex h-10 rounded-button border border-border bg-white p-1" aria-label="資料來源">
      {(["api", "mock"] as const).map((mode) => (
        <button
          className={`rounded-button px-3 text-sm font-medium transition ${
            value === mode ? "bg-primary text-white" : "text-textSecondary hover:bg-slate-100"
          }`}
          key={mode}
          onClick={() => onChange(mode)}
          type="button"
        >
          {mode === "api" ? "API" : "Mock"}
        </button>
      ))}
    </div>
  );
}
