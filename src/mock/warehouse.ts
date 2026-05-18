import type {
  ExpiryBatch,
  InventoryItem,
  WarehouseKpi,
  WarehouseTask
} from "@/types/warehouse";

export const warehouseKpis: WarehouseKpi[] = [
  {
    label: "總庫存品項",
    value: "428",
    hint: "32 個庫位",
    tone: "info"
  },
  {
    label: "低於安全庫存",
    value: "14",
    hint: "5 項急補",
    tone: "warning"
  },
  {
    label: "即期批號",
    value: "9",
    hint: "7 日內到期",
    tone: "danger"
  },
  {
    label: "待入出庫",
    value: "23",
    hint: "今日任務",
    tone: "success"
  }
];

export const inventoryItems: InventoryItem[] = [
  {
    sku: "RM-CORN-001",
    name: "冷凍玉米粒",
    category: "原料",
    warehouse: "冷凍原料庫",
    location: "FZ-A03-02",
    quantity: 180,
    unit: "kg",
    safetyStock: 420,
    status: "低於安全庫存",
    tone: "warning"
  },
  {
    sku: "RM-CHICKEN-022",
    name: "雞胸肉原料",
    category: "原料",
    warehouse: "冷藏原料庫",
    location: "CH-B01-05",
    quantity: 1280,
    unit: "kg",
    safetyStock: 900,
    status: "庫存正常",
    tone: "success"
  },
  {
    sku: "FG-CURRY-101",
    name: "咖哩雞肉調理包",
    category: "成品",
    warehouse: "成品冷凍庫",
    location: "FG-C02-08",
    quantity: 8420,
    unit: "盒",
    safetyStock: 5000,
    status: "可出貨",
    tone: "success"
  },
  {
    sku: "PK-BAG-010",
    name: "耐熱殺菌袋",
    category: "包材",
    warehouse: "包材庫",
    location: "PK-D04-01",
    quantity: 3200,
    unit: "只",
    safetyStock: 6000,
    status: "需採購",
    tone: "danger"
  }
];

export const expiryBatches: ExpiryBatch[] = [
  {
    batchNo: "RM240506-CORN",
    itemName: "冷凍玉米粒",
    category: "原料",
    quantity: 180,
    unit: "kg",
    expiryDate: "2026-05-17",
    daysLeft: 5,
    location: "FZ-A03-02",
    tone: "danger"
  },
  {
    batchNo: "FG240508-SOUP",
    itemName: "鮮蔬玉米濃湯",
    category: "成品",
    quantity: 920,
    unit: "盒",
    expiryDate: "2026-05-21",
    daysLeft: 9,
    location: "FG-C01-03",
    tone: "warning"
  },
  {
    batchNo: "RM240510-CHK",
    itemName: "雞胸肉原料",
    category: "原料",
    quantity: 460,
    unit: "kg",
    expiryDate: "2026-05-25",
    daysLeft: 13,
    location: "CH-B01-05",
    tone: "info"
  }
];

export const warehouseTasks: WarehouseTask[] = [
  {
    id: "WH-IN-240512-018",
    type: "入庫",
    itemName: "雞胸肉原料",
    batchNo: "RM240512-CHK",
    quantity: 600,
    unit: "kg",
    owner: "李倉管",
    dueTime: "10:40",
    status: "待驗收",
    tone: "info"
  },
  {
    id: "WH-OUT-240512-022",
    type: "出庫",
    itemName: "冷凍玉米粒",
    batchNo: "RM240506-CORN",
    quantity: 240,
    unit: "kg",
    owner: "周倉管",
    dueTime: "11:20",
    status: "待揀料",
    tone: "warning"
  },
  {
    id: "WH-MV-240512-006",
    type: "移倉",
    itemName: "咖哩雞肉調理包",
    batchNo: "FG240512-CURRY",
    quantity: 1200,
    unit: "盒",
    owner: "許組長",
    dueTime: "13:30",
    status: "執行中",
    tone: "success"
  },
  {
    id: "WH-CK-240512-004",
    type: "盤點",
    itemName: "耐熱殺菌袋",
    batchNo: "PK240501-BAG",
    quantity: 3200,
    unit: "只",
    owner: "陳倉管",
    dueTime: "15:00",
    status: "待盤點",
    tone: "danger"
  }
];
