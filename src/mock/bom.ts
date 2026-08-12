import type { BomDashboardData, BomDetail } from "@/types/bom";

export const bomDashboardMock: BomDashboardData = {
  summary: {
    bomCount: 146,
    versionCount: 176,
    effectiveVersionCount: 118,
    futureVersionCount: 8,
    historicalVersionCount: 50
  },
  kpis: [
    { label: "BOM 數量", value: "146", hint: "不重複商品配方", tone: "info" },
    { label: "版本總數", value: "176", hint: "含有效、未來與歷史版本", tone: "info" },
    { label: "目前有效", value: "118", hint: "可供生產引用", tone: "success" },
    { label: "未來生效", value: "8", hint: "需留意切換日", tone: "warning" },
    { label: "歷史版本", value: "50", hint: "保留追溯，不再作為預設版本", tone: "neutral" }
  ],
  items: [
    {
      id: "BOM-260801-v3",
      bomNo: "BOM-260801",
      bomName: "香草餅乾",
      version: 3,
      date: "2026/08/01",
      dateTimestamp: 1785513600,
      unit: "公斤",
      unitCode: 2,
      weight: 150,
      versionStateCode: "effective",
      versionStateLabel: "目前有效",
      tone: "success",
      itemCount: 18,
      linkedProductCount: 3
    },
    {
      id: "BOM-260734-v2",
      bomNo: "BOM-260734",
      bomName: "可可粉體",
      version: 2,
      date: "2026/09/01",
      dateTimestamp: 1788192000,
      unit: "公斤",
      unitCode: 2,
      weight: 120,
      versionStateCode: "future",
      versionStateLabel: "未來生效",
      tone: "info",
      itemCount: 11,
      linkedProductCount: 1
    },
    {
      id: "BOM-260501-v1",
      bomNo: "BOM-260501",
      bomName: "乳粉基礎",
      version: 1,
      date: "2026/05/01",
      dateTimestamp: 1777564800,
      unit: "公斤",
      unitCode: 2,
      weight: 80,
      versionStateCode: "historical",
      versionStateLabel: "歷史版本",
      tone: "neutral",
      itemCount: 9,
      linkedProductCount: 0
    }
  ],
  total: 3,
  start: 0,
  count: 3
};

export const bomDetailMock: Record<string, BomDetail> = {
  "BOM-260801": {
    bom: {
      ...bomDashboardMock.items[0],
      comment: "標準量產配方；本頁不含成本、報價或合約資料。"
    },
    versions: [
      {
        version: 3,
        date: "2026/08/01",
        dateTimestamp: 1785513600,
        versionStateCode: "effective",
        versionStateLabel: "目前有效",
        tone: "success"
      },
      {
        version: 2,
        date: "2026/06/01",
        dateTimestamp: 1780243200,
        versionStateCode: "historical",
        versionStateLabel: "歷史版本",
        tone: "neutral"
      }
    ],
    items: [
      { itemNo: "RM-0018", itemName: "小麥粉", unit: "公斤", unitCode: 2, weight: 120 },
      { itemNo: "RM-0042", itemName: "砂糖", unit: "公斤", unitCode: 2, weight: 22.5 },
      { itemNo: "RM-0087", itemName: "奶油粉", unit: "公斤", unitCode: 2, weight: 8 }
    ],
    linkedProducts: [
      {
        productNo: "P-00018",
        productVersion: 5,
        level: 2,
        levelLabel: "箱規",
        itemType: 3,
        itemTypeLabel: "製成品",
        itemNo: "FG-COOKIE-018",
        count: 12,
        unit: "公斤",
        unitCode: 2,
        weight: 150
      },
      {
        productNo: "P-00021",
        productVersion: 2,
        level: 1,
        levelLabel: "組規",
        itemType: 2,
        itemTypeLabel: "在製品",
        itemNo: "WIP-COOKIE-021",
        count: 6,
        unit: "公斤",
        unitCode: 2,
        weight: 75
      }
    ]
  }
};
