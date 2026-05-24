import type { WorkforceCase, WorkforceDashboardData, WorkforceSummary } from "@/types/workforce";

export const workforceSummary: WorkforceSummary[] = [
  { label: "今日出勤", value: "86", hint: "92% 到勤", tone: "success" },
  { label: "人力缺口", value: "4", hint: "B2 晚班最吃緊", tone: "warning" },
  { label: "技能不符", value: "3", hint: "冷凍/殺菌/冷鏈", tone: "danger" },
  { label: "證照到期", value: "2", hint: "30 天內需複訓", tone: "info" }
];

export const workforceCases: WorkforceCase[] = [
  {
    id: "WF-20260523-A1",
    department: "生產",
    lineOrArea: "A1 調理包產線",
    shift: "日班 08:00-17:00",
    relatedPlan: "PLAN-20260523-018",
    relatedWorkOrder: "WO-20260523-001",
    requiredStaff: 8,
    assignedStaff: 8,
    skillRequired: "調理 / 殺菌 / 報工",
    skillCoverage: "完整",
    riskLevel: "正常",
    riskReason: "A1 日班人員與技能符合今日工單需求。",
    overtimeHours: 0,
    supportNeeded: 0,
    certificationIssue: null,
    owner: "生產一組",
    tone: "success",
    requirements: [
      { area: "產線", required: 8, assigned: 8, gap: 0, note: "A1 人力已滿編", tone: "success" },
      { area: "品保", required: 1, assigned: 1, gap: 0, note: "首件檢驗已安排", tone: "success" }
    ]
  },
  {
    id: "WF-20260523-B2",
    department: "生產",
    lineOrArea: "B2 冷凍蔬菜產線",
    shift: "晚班 17:00-01:00",
    relatedPlan: "PLAN-20260523-022",
    relatedWorkOrder: "WO-建議-20260523-022",
    requiredStaff: 7,
    assignedStaff: 5,
    skillRequired: "冷凍蔬菜 / 換線 / 包裝",
    skillCoverage: "不足",
    riskLevel: "高風險",
    riskReason: "B2 晚班缺 2 人，且冷凍蔬菜經驗不足，會影響重排後工單。",
    overtimeHours: 6,
    supportNeeded: 2,
    certificationIssue: null,
    owner: "生產二組",
    tone: "danger",
    requirements: [
      { area: "產線", required: 7, assigned: 5, gap: 2, note: "需跨線支援 2 人", tone: "danger" },
      { area: "倉庫", required: 2, assigned: 1, gap: 1, note: "冷凍原料備料人力不足", tone: "warning" }
    ]
  },
  {
    id: "WF-20260523-LOG",
    department: "物流",
    lineOrArea: "中區/南區冷鏈配送",
    shift: "日班 09:00-18:00",
    relatedPlan: null,
    relatedWorkOrder: null,
    requiredStaff: 4,
    assignedStaff: 4,
    skillRequired: "冷鏈配送 / 職業大貨車",
    skillCoverage: "注意",
    riskLevel: "注意",
    riskReason: "2 名司機冷鏈訓練證照 30 天內到期，需安排複訓避免後續派車受限。",
    overtimeHours: 2,
    supportNeeded: 0,
    certificationIssue: "冷鏈訓練證照 30 天內到期",
    owner: "物流一組",
    tone: "warning",
    requirements: [
      { area: "物流", required: 4, assigned: 4, gap: 0, note: "今日車次可執行", tone: "success" },
      { area: "品保", required: 1, assigned: 1, gap: 0, note: "溫度紀錄覆核已安排", tone: "info" }
    ]
  }
];

export const workforceDashboardMock: WorkforceDashboardData = {
  summary: workforceSummary,
  cases: workforceCases
};
