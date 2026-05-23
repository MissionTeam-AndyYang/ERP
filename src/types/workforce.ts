import type { StatusTone } from "@/types/dashboard";

export type WorkforceWorkspaceTab = "coverage" | "skill-gap" | "overtime" | "certifications";

export type WorkforceRiskLevel = "正常" | "注意" | "高風險";

export type WorkforceSummary = {
  label: string;
  value: string;
  hint: string;
  tone: StatusTone;
};

export type WorkforceRequirement = {
  area: "產線" | "倉庫" | "品保" | "物流";
  required: number;
  assigned: number;
  gap: number;
  note: string;
  tone: StatusTone;
};

export type WorkforceCase = {
  id: string;
  department: "生產" | "倉庫" | "品保" | "物流";
  lineOrArea: string;
  shift: string;
  relatedPlan: string | null;
  relatedWorkOrder: string | null;
  requiredStaff: number;
  assignedStaff: number;
  skillRequired: string;
  skillCoverage: string;
  riskLevel: WorkforceRiskLevel;
  riskReason: string;
  overtimeHours: number;
  supportNeeded: number;
  certificationIssue: string | null;
  owner: string;
  tone: StatusTone;
  requirements: WorkforceRequirement[];
};

