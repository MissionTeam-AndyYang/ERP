import type { StatusTone } from "@/types/dashboard";

export type BomDataSource = "api" | "mock";

export type BomVersionStateCode = "effective" | "future" | "historical" | "unknown";

export type BomSummary = {
  bomCount: number;
  versionCount: number;
  effectiveVersionCount: number;
  futureVersionCount: number;
  historicalVersionCount: number;
};

export type BomKpiItem = {
  label: string;
  value: string;
  hint: string;
  tone: StatusTone;
};

export type BomDashboardItem = {
  id: string;
  bomNo: string;
  bomName: string;
  version: number;
  date: string;
  dateTimestamp: number;
  unit: string;
  unitCode: number;
  weight: number;
  versionStateCode: BomVersionStateCode;
  versionStateLabel: string;
  tone: StatusTone;
  itemCount: number;
  linkedProductCount: number;
};

export type BomDashboardData = {
  summary: BomSummary;
  kpis: BomKpiItem[];
  items: BomDashboardItem[];
  total: number;
  start: number;
  count: number;
};

export type BomVersionOption = {
  version: number;
  date: string;
  dateTimestamp: number;
  versionStateCode: BomVersionStateCode;
  versionStateLabel: string;
  tone: StatusTone;
};

export type BomMaterialItem = {
  itemNo: string;
  itemName: string;
  unit: string;
  unitCode: number;
  weight: number;
};

export type BomLinkedProduct = {
  productNo: string;
  productVersion: number;
  level: number;
  levelLabel: string;
  itemType: number;
  itemTypeLabel: string;
  itemNo: string;
  count: number;
  unit: string;
  unitCode: number;
  weight: number;
};

export type BomDetail = {
  bom: BomDashboardItem & {
    comment: string;
  };
  versions: BomVersionOption[];
  items: BomMaterialItem[];
  linkedProducts: BomLinkedProduct[];
};
