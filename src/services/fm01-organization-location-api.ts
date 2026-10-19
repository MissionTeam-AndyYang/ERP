import {
  fm01HierarchyKeys,
  fm01ResourceReferences,
  fm01Resources,
  type Fm01Collection,
  type Fm01Hierarchy,
  type Fm01Record,
  type Fm01RelationKey,
  type Fm01Resource
} from "@/types/fm01-organization-location";

const relationKeys: Partial<Record<Fm01Resource, Fm01RelationKey[]>> = {
  companies: ["legal_entity_id"],
  sites: ["company_id"],
  plants: ["site_id"],
  warehouses: ["site_id", "plant_id"],
  locations: ["warehouse_id", "parent_location_id"]
};

export class Fm01ApiError extends Error {
  constructor(
    readonly code: string,
    readonly status: number | undefined,
    readonly correlationId?: string,
    message = "FM-01 request failed"
  ) {
    super(message);
    this.name = "Fm01ApiError";
  }
}

function apiBaseUrl() {
  const configured = process.env.NEXT_PUBLIC_API_BASE_URL?.trim().replace(/\/$/, "");
  if (!configured) {
    throw new Fm01ApiError("API_BASE_URL_MISSING", undefined);
  }
  return configured;
}

function assertObject(value: unknown): Record<string, unknown> {
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    throw new Fm01ApiError("INVALID_RESPONSE", undefined);
  }
  return value as Record<string, unknown>;
}

function parseRecord(resource: Fm01Resource, value: unknown): Fm01Record {
  const row = assertObject(value);
  const keys = fm01ResourceReferences[resource];
  const id = row[keys.id];
  const ref = row[keys.ref];
  const name = row.display_name;

  if (typeof id !== "number" || !Number.isInteger(id) || id < 1) {
    throw new Fm01ApiError("INVALID_RESPONSE", undefined);
  }
  if (typeof ref !== "string" || typeof name !== "string") {
    throw new Fm01ApiError("INVALID_RESPONSE", undefined);
  }

  const relations: Fm01Record["relations"] = {};
  for (const key of relationKeys[resource] ?? []) {
    const relation = row[key];
    if (relation !== null && relation !== undefined && (typeof relation !== "number" || !Number.isInteger(relation))) {
      throw new Fm01ApiError("INVALID_RESPONSE", undefined);
    }
    relations[key] = (relation as number | null | undefined) ?? null;
  }

  return { resource, id, ref, displayName: name, relations };
}

async function requestJson(path: string, params?: Record<string, string>) {
  const query = params ? `?${new URLSearchParams(params).toString()}` : "";
  let response: Response;

  try {
    response = await fetch(`${apiBaseUrl()}${path}${query}`, {
      method: "GET",
      headers: { Accept: "application/json" },
      cache: "no-store"
    });
  } catch (error) {
    if (error instanceof Fm01ApiError) throw error;
    throw new Fm01ApiError("NETWORK_UNAVAILABLE", undefined);
  }

  let payload: unknown;
  try {
    payload = await response.json();
  } catch {
    throw new Fm01ApiError("INVALID_RESPONSE", response.status);
  }

  if (!response.ok) {
    const root = payload && typeof payload === "object" ? (payload as Record<string, unknown>) : {};
    const detail = root.error && typeof root.error === "object"
      ? (root.error as Record<string, unknown>)
      : root;
    const code = typeof detail.code === "string" ? detail.code : "REQUEST_FAILED";
    const details = detail.details && typeof detail.details === "object"
      ? (detail.details as Record<string, unknown>)
      : {};
    const correlationId = typeof details.correlation_id === "string" ? details.correlation_id : undefined;
    throw new Fm01ApiError(code, response.status, correlationId);
  }

  return assertObject(payload);
}

function parseHierarchy(value: unknown): Fm01Hierarchy {
  const data = assertObject(value);
  const hierarchy = {} as Fm01Hierarchy;

  for (const resource of fm01Resources) {
    const rows = data[fm01HierarchyKeys[resource]];
    if (!Array.isArray(rows)) {
      throw new Fm01ApiError("INVALID_RESPONSE", undefined);
    }
    hierarchy[resource] = rows.map((row) => parseRecord(resource, row));
  }

  return hierarchy;
}

export async function getFm01Hierarchy(): Promise<Fm01Hierarchy> {
  const envelope = await requestJson("/api/v1/fm01/hierarchy");
  return parseHierarchy(envelope.data);
}

export async function getFm01Collection(
  resource: Fm01Resource,
  offset = 1,
  limit = 25
): Promise<Fm01Collection> {
  const envelope = await requestJson(`/api/v1/fm01/${resource}`, {
    limit: String(limit),
    offset: String(offset)
  });
  const rows = envelope.data;
  const meta = assertObject(envelope.meta);
  if (!Array.isArray(rows) || typeof meta.total !== "number" || !Number.isInteger(meta.total) || meta.total < 0) {
    throw new Fm01ApiError("INVALID_RESPONSE", undefined);
  }
  return { records: rows.map((row) => parseRecord(resource, row)), total: meta.total };
}

export async function getFm01Record(resource: Fm01Resource, id: number): Promise<Fm01Record> {
  const envelope = await requestJson(`/api/v1/fm01/${resource}`, {
    id: String(id),
    limit: "1",
    offset: "1"
  });
  if (!Array.isArray(envelope.data)) {
    throw new Fm01ApiError("INVALID_RESPONSE", undefined);
  }
  const [record] = envelope.data;
  if (!record) {
    throw new Fm01ApiError("NOT_FOUND", 404);
  }
  return parseRecord(resource, record);
}
