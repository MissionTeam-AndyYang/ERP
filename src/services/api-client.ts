export type ApiClientOptions = {
  baseUrl?: string;
  timeoutMs?: number;
};

export class ApiClientError extends Error {
  status?: number;

  constructor(message: string, status?: number) {
    super(message);
    this.name = "ApiClientError";
    this.status = status;
  }
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

export async function apiGet<T>(
  path: string,
  { baseUrl, timeoutMs = DEFAULT_TIMEOUT_MS }: ApiClientOptions = {}
): Promise<T> {
  const controller = new AbortController();
  const timeout = window.setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch(buildUrl(path, baseUrl), {
      headers: { Accept: "application/json" },
      signal: controller.signal
    });

    if (!response.ok) {
      throw new ApiClientError(`API request failed: ${response.status}`, response.status);
    }

    const payload = (await response.json()) as unknown;
    if (payload && typeof payload === "object" && "data" in payload) {
      return (payload as { data: T }).data;
    }

    return payload as T;
  } finally {
    window.clearTimeout(timeout);
  }
}

export function withFallbackArray<T>(value: unknown, fallback: T[]): T[] {
  return Array.isArray(value) ? (value as T[]) : fallback;
}
