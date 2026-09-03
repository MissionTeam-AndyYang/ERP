import type { RecipeFormulaDashboardData, RecipeFormulaDetail } from "@/types/recipe";

export const recipeFormulaDashboardMock: RecipeFormulaDashboardData = {
  summary: {
    recipeCount: 2,
    versionCount: 4,
    effectiveVersionCount: 1,
    warningCount: 1
  },
  kpis: [
    { label: "Recipe 定義", value: "2", hint: "受治理的配方定義", tone: "info" },
    { label: "版本總數", value: "4", hint: "含有效、未來與歷史版本", tone: "neutral" },
    { label: "目前有效", value: "1", hint: "可作 read-only 引用", tone: "success" },
    { label: "待確認", value: "1", hint: "存在重量或來源警示", tone: "warning" }
  ],
  recipes: [
    {
      id: "RCP-260901-v2",
      recipeNo: "RCP-260901",
      recipeName: "檸檬飲基礎製程配方",
      productNo: "PRD-LEMON-001",
      productName: "檸檬風味飲",
      currentVersion: 2,
      statusCode: "effective",
      statusLabel: "目前有效",
      tone: "success",
      inputCount: 4,
      warningCount: 0,
      owner: "研發",
      sourceLabel: "R&D 試作確認"
    },
    {
      id: "RCP-260742-v1",
      recipeNo: "RCP-260742",
      recipeName: "燕麥餅乾試作配方",
      productNo: "PRD-OAT-014",
      productName: "燕麥餅乾",
      currentVersion: 1,
      statusCode: "warning",
      statusLabel: "待確認",
      tone: "warning",
      inputCount: 3,
      warningCount: 1,
      owner: "研發",
      sourceLabel: "試作紀錄"
    }
  ],
  total: 2,
  start: 0,
  count: 2
};

export const recipeFormulaDetailMock: Record<string, RecipeFormulaDetail> = {
  "RCP-260901": {
    recipe: recipeFormulaDashboardMock.recipes[0],
    versions: [
      { version: 2, statusCode: "effective", statusLabel: "目前有效", tone: "success", effectiveDate: "2026/09/01" },
      { version: 1, statusCode: "historical", statusLabel: "歷史版本", tone: "neutral", effectiveDate: "2026/07/15" }
    ],
    inputs: [
      {
        lineNo: "10",
        itemNo: "RM-LEMON-001",
        itemName: "檸檬濃縮汁",
        itemCategoryLabel: "原料",
        processStageLabel: "前備",
        quantity: 1,
        weight: 12.5,
        unit: "公斤",
        weightRatio: 12.5,
        inputLossRate: 1.2,
        sourceRef: "TRIAL-260831"
      },
      {
        lineNo: "20",
        itemNo: "RM-SUGAR-002",
        itemName: "砂糖",
        itemCategoryLabel: "原料",
        processStageLabel: "加工",
        quantity: 1,
        weight: 8,
        unit: "公斤",
        weightRatio: 8,
        inputLossRate: 0.5,
        sourceRef: "TRIAL-260831"
      },
      {
        lineNo: "30",
        itemNo: "WIP-SYRUP-001",
        itemName: "糖漿半成品",
        itemCategoryLabel: "半成品",
        processStageLabel: "加工",
        quantity: 1,
        weight: 28,
        unit: "公斤",
        weightRatio: 28,
        inputLossRate: 0.8,
        sourceRef: "RCP-260901/V1"
      },
      {
        lineNo: "40",
        itemNo: "PKG-BOTTLE-001",
        itemName: "瓶器",
        itemCategoryLabel: "包材",
        processStageLabel: "包裝",
        quantity: 120,
        weight: 0,
        unit: "個",
        weightRatio: 0,
        inputLossRate: 0,
        sourceRef: "PKG-SPEC-REF"
      }
    ],
    output: {
      itemNo: "PRD-LEMON-001",
      itemName: "檸檬風味飲",
      outputTypeLabel: "唯一定義產出",
      quantity: 120,
      weight: 100,
      unit: "公斤",
      yieldRate: 98.4
    },
    lineage: [
      { sourceTypeLabel: "Recipe definition", sourceRef: "RCP-260901", evidenceLabel: "研發試作確認", statusLabel: "已引用" },
      { sourceTypeLabel: "BOM reference", sourceRef: "BOM-LEMON-001/V2", evidenceLabel: "產品結構參照", statusLabel: "參照中" }
    ],
    warnings: [],
    productStructureReferences: [
      { typeLabel: "Product Structure", refNo: "PRD-LEMON-001/V3", refName: "檸檬風味飲成品結構", statusLabel: "參照中" }
    ],
    routingReferences: [
      { typeLabel: "Routing context", refNo: "ROUTE-LEMON-001", refName: "前備 / 加工 / 包裝", statusLabel: "參照中" }
    ]
  },
  "RCP-260742": {
    recipe: recipeFormulaDashboardMock.recipes[1],
    versions: [
      { version: 1, statusCode: "warning", statusLabel: "待確認", tone: "warning", effectiveDate: "2026/07/42" }
    ],
    inputs: [
      {
        lineNo: "10",
        itemNo: "RM-OAT-001",
        itemName: "燕麥",
        itemCategoryLabel: "原料",
        processStageLabel: "前備",
        quantity: 1,
        weight: 40,
        unit: "公斤",
        weightRatio: 53.33,
        inputLossRate: 1,
        sourceRef: "TRIAL-260742"
      },
      {
        lineNo: "20",
        itemNo: "RM-BUTTER-001",
        itemName: "奶油",
        itemCategoryLabel: "原料",
        processStageLabel: "加工",
        quantity: 1,
        weight: 20,
        unit: "公斤",
        weightRatio: 26.67,
        inputLossRate: 1.5,
        sourceRef: "TRIAL-260742"
      }
    ],
    output: {
      itemNo: "PRD-OAT-014",
      itemName: "燕麥餅乾",
      outputTypeLabel: "唯一定義產出",
      quantity: 1,
      weight: 75,
      unit: "公斤",
      yieldRate: 96
    },
    lineage: [{ sourceTypeLabel: "Trial record", sourceRef: "TRIAL-260742", evidenceLabel: "試作紀錄", statusLabel: "待確認" }],
    warnings: [{ code: "unresolved_weight_basis", message: "包裝段重量基準尚未確認。", refNo: "PKG-OAT-014" }],
    productStructureReferences: [
      { typeLabel: "Product Structure", refNo: "PRD-OAT-014/V1", refName: "燕麥餅乾產品結構", statusLabel: "待確認" }
    ],
    routingReferences: [{ typeLabel: "Routing context", refNo: "ROUTE-OAT-014", refName: "前備 / 加工", statusLabel: "待確認" }]
  }
};
