export type ApiClientOptions = {
  baseUrl?: string;
  timeoutMs?: number;
  headers?: Record<string, string>;
};

export class ApiClientError extends Error {
  status?: number;
  fieldErrors?: Record<string, string>;

  constructor(message: string, status?: number, fieldErrors?: Record<string, string>) {
    super(message);
    this.name = "ApiClientError";
    this.status = status;
    this.fieldErrors = fieldErrors;
  }
}

function normalizeFieldErrors(value: unknown): Record<string, string> | undefined {
  if (Array.isArray(value)) {
    const fields = value.reduce<Record<string, string>>((result, entry) => {
      if (entry && typeof entry === "object") {
        const field = "field" in entry ? (entry.field as unknown) : undefined;
        const message = "message" in entry ? (entry.message as unknown) : undefined;
        if (typeof field === "string" && typeof message === "string") result[field] = message;
      }
      return result;
    }, {});
    return Object.keys(fields).length ? fields : undefined;
  }
  if (value && typeof value === "object") {
    const fields = Object.entries(value).reduce<Record<string, string>>((result, [field, message]) => {
      if (typeof message === "string") result[field] = message;
      return result;
    }, {});
    return Object.keys(fields).length ? fields : undefined;
  }
  return undefined;
}

const DEFAULT_TIMEOUT_MS = 8000;

function getApiBaseUrl(baseUrl?: string) {
  return (baseUrl ?? process.env.NEXT_PUBLIC_API_BASE_URL ?? "").replace(/\/$/, "");
}

function buildUrl(path: string, baseUrl?: string) {
  const normalizedPath = path.startsWith("/") ? path : `/${path}`;
  const normalizedBaseUrl = getApiBaseUrl(baseUrl);
  return normalizedBaseUrl ? `${normalizedBaseUrl}${normalizedPath}` : normalizedPath;
}

function buildHeaders(headers?: Record<string, string>) {
  const token = process.env.NEXT_PUBLIC_API_TOKEN;
  const timezone = process.env.NEXT_PUBLIC_API_TIMEZONE ?? "Asia/Taipei";
  return {
    Accept: "application/json",
    "x-timezone": timezone,
    ...(token ? { "x-auth-token": token } : {}),
    ...(headers ?? {})
  };
}

export async function apiGet<T>(
  path: string,
  { baseUrl, timeoutMs = DEFAULT_TIMEOUT_MS, headers }: ApiClientOptions = {}
): Promise<T> {
  const controller = new AbortController();
  const timeout = window.setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch(buildUrl(path, baseUrl), {
      headers: buildHeaders(headers),
      signal: controller.signal
    });

    if (!response.ok) {
      let detail = `API request failed: ${response.status}`;
      let fieldErrors: Record<string, string> | undefined;
      try {
        const errorPayload = (await response.json()) as {
          message?: string;
          error?: string;
          detail?: string;
          field_errors?: unknown;
          errors?: unknown;
        };
        detail = errorPayload.message ?? errorPayload.error ?? errorPayload.detail ?? detail;
        fieldErrors = normalizeFieldErrors(errorPayload.field_errors ?? errorPayload.errors);
      } catch {
        // Preserve the HTTP status when the server does not return JSON.
      }
      throw new ApiClientError(detail, response.status, fieldErrors);
    }

    const payload = (await response.json()) as unknown;
    if (payload && typeof payload === "object" && "data" in payload) {
      return (payload as { data: T }).data;
    }
    if (payload && typeof payload === "object" && "payload" in payload) {
      return (payload as { payload: T }).payload;
    }

    return payload as T;
  } finally {
    window.clearTimeout(timeout);
  }
}

async function apiRequest<T>(
  method: "PATCH" | "POST",
  path: string,
  body: unknown,
  { baseUrl, timeoutMs = DEFAULT_TIMEOUT_MS, headers }: ApiClientOptions = {}
): Promise<T> {
  const controller = new AbortController();
  const timeout = window.setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch(buildUrl(path, baseUrl), {
      method,
      headers: {
        ...buildHeaders(headers),
        "Content-Type": "application/json"
      },
      body: JSON.stringify(body),
      signal: controller.signal
    });

    if (!response.ok) {
      let detail = `API request failed: ${response.status}`;
      let fieldErrors: Record<string, string> | undefined;
      try {
        const errorPayload = (await response.json()) as {
          message?: string;
          error?: string;
          detail?: string;
          field_errors?: unknown;
          errors?: unknown;
        };
        detail = errorPayload.message ?? errorPayload.error ?? errorPayload.detail ?? detail;
        fieldErrors = normalizeFieldErrors(errorPayload.field_errors ?? errorPayload.errors);
      } catch {
        // Preserve the HTTP status when the server does not return JSON.
      }
      throw new ApiClientError(detail, response.status, fieldErrors);
    }

    const payload = (await response.json()) as unknown;
    if (payload && typeof payload === "object" && "data" in payload) {
      return (payload as { data: T }).data;
    }
    if (payload && typeof payload === "object" && "payload" in payload) {
      return (payload as { payload: T }).payload;
    }
    return payload as T;
  } finally {
    window.clearTimeout(timeout);
  }
}

export function apiPost<T>(path: string, body: unknown, options?: ApiClientOptions) {
  return apiRequest<T>("POST", path, body, options);
}

export function apiPatch<T>(path: string, body: unknown, options?: ApiClientOptions) {
  return apiRequest<T>("PATCH", path, body, options);
}

export function withFallbackArray<T>(value: unknown, fallback: T[]): T[] {
  return Array.isArray(value) ? (value as T[]) : fallback;
}
