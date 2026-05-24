import type { StatusTone } from "@/types/dashboard";

export type SettingsWorkspaceTab = "master-data" | "permissions" | "integrations" | "localization";

export type GovernanceRiskLevel = "正常" | "注意" | "高風險";

export type SettingsSummary = {
  label: string;
  value: string;
  hint: string;
  tone: StatusTone;
};

export type MasterDataItem = {
  id: string;
  domain: "品項" | "BOM" | "客戶" | "供應商" | "倉位" | "產線" | "權限" | "語言";
  name: string;
  owner: string;
  status: "完整" | "待補" | "需審核";
  riskLevel: GovernanceRiskLevel;
  riskReason: string;
  affectedWorkspaces: string[];
  lastUpdated: string;
  tone: StatusTone;
};

export type SettingsDashboardData = {
  summary: SettingsSummary[];
  items: MasterDataItem[];
};

export type SettingsDataSource = "api" | "mock";
