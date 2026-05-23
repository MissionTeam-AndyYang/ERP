import type { MasterDataItem, SettingsSummary } from "@/types/settings";

export const settingsSummary: SettingsSummary[] = [
  { label: "主檔項目", value: "8", hint: "第一版核心治理範圍", tone: "info" },
  { label: "待補主檔", value: "5", hint: "BOM、倉位、語言", tone: "warning" },
  { label: "權限待審", value: "3", hint: "品保/財務/採購", tone: "danger" },
  { label: "多語支援", value: "4", hint: "繁中、英、日、越", tone: "success" }
];

export const masterDataItems: MasterDataItem[] = [
  {
    id: "MD-ITEM-001",
    domain: "品項",
    name: "食品品項與分類",
    owner: "研發/品管",
    status: "待補",
    riskLevel: "注意",
    riskReason: "部分品項尚未補齊保存期限、溫層與安全庫存規則。",
    affectedWorkspaces: ["Warehouse", "Planning", "Quality", "Finance"],
    lastUpdated: "2026-05-23",
    tone: "warning"
  },
  {
    id: "MD-BOM-002",
    domain: "BOM",
    name: "BOM 與替代料規則",
    owner: "研發/生管",
    status: "需審核",
    riskLevel: "高風險",
    riskReason: "缺料時是否允許替代料尚未定義，會影響 Planning/APS 請購與工單建議。",
    affectedWorkspaces: ["Orders", "Planning", "Purchasing", "Production"],
    lastUpdated: "2026-05-23",
    tone: "danger"
  },
  {
    id: "MD-WH-003",
    domain: "倉位",
    name: "倉庫、倉位與板位容量",
    owner: "倉儲",
    status: "待補",
    riskLevel: "注意",
    riskReason: "寄倉與板位容量規則需補齊，才能支援倉位使用率與可用板數。",
    affectedWorkspaces: ["Warehouse", "Logistics", "Planning"],
    lastUpdated: "2026-05-23",
    tone: "warning"
  },
  {
    id: "MD-LINE-004",
    domain: "產線",
    name: "產線、製程與標準產能",
    owner: "生產",
    status: "完整",
    riskLevel: "正常",
    riskReason: "第一版已可支援產能與人員檢核。",
    affectedWorkspaces: ["Planning", "Production", "Workforce"],
    lastUpdated: "2026-05-23",
    tone: "success"
  },
  {
    id: "MD-AUTH-005",
    domain: "權限",
    name: "角色權限與簽核範圍",
    owner: "系統管理",
    status: "需審核",
    riskLevel: "注意",
    riskReason: "高風險訂單、品質放行、採購請購與請款權限需後續確認。",
    affectedWorkspaces: ["Orders", "Quality", "Purchasing", "Finance"],
    lastUpdated: "2026-05-23",
    tone: "warning"
  },
  {
    id: "MD-I18N-006",
    domain: "語言",
    name: "多國語言與現場用詞",
    owner: "系統管理",
    status: "待補",
    riskLevel: "注意",
    riskReason: "目前已有語言切換基礎，但各頁業務文案尚未完整字典化。",
    affectedWorkspaces: ["All"],
    lastUpdated: "2026-05-23",
    tone: "info"
  }
];

