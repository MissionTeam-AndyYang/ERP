export type Fm01Resource =
  | "legal-entities"
  | "companies"
  | "sites"
  | "plants"
  | "warehouses"
  | "locations";

export type Fm01RelationKey =
  | "legal_entity_id"
  | "company_id"
  | "site_id"
  | "plant_id"
  | "warehouse_id"
  | "parent_location_id";

export type Fm01Record = {
  resource: Fm01Resource;
  id: number;
  ref: string;
  displayName: string;
  relations: Partial<Record<Fm01RelationKey, number | null>>;
};

export type Fm01Hierarchy = Record<Fm01Resource, Fm01Record[]>;

export type Fm01Collection = {
  records: Fm01Record[];
  total: number;
};

export type Fm01Selection = {
  resource: Fm01Resource;
  id: number;
};

export const fm01Resources: Fm01Resource[] = [
  "legal-entities",
  "companies",
  "sites",
  "plants",
  "warehouses",
  "locations"
];

export const fm01ResourceLabels: Record<Fm01Resource, string> = {
  "legal-entities": "法人",
  companies: "公司",
  sites: "廠區",
  plants: "廠別",
  warehouses: "倉庫",
  locations: "庫位"
};

export const fm01ResourceReferences: Record<Fm01Resource, { id: string; ref: string }> = {
  "legal-entities": { id: "legal_entity_id", ref: "legal_entity_ref" },
  companies: { id: "company_id", ref: "company_ref" },
  sites: { id: "site_id", ref: "site_ref" },
  plants: { id: "plant_id", ref: "plant_ref" },
  warehouses: { id: "warehouse_id", ref: "warehouse_ref" },
  locations: { id: "location_id", ref: "location_ref" }
};

export const fm01HierarchyKeys: Record<Fm01Resource, keyof Fm01Hierarchy> = {
  "legal-entities": "legal_entities",
  companies: "companies",
  sites: "sites",
  plants: "plants",
  warehouses: "warehouses",
  locations: "locations"
};

export const fm01ParentFor: Partial<Record<Fm01Resource, Fm01Resource>> = {
  companies: "legal-entities",
  sites: "companies",
  plants: "sites",
  warehouses: "sites",
  locations: "warehouses"
};
