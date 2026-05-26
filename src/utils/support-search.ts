export type SearchableValue = string | number | null | undefined;

export function normalizeSupportSearch(value: string) {
  return value.trim().toLowerCase();
}

export function includesSupportSearch(value: SearchableValue, query: string) {
  return String(value ?? "").toLowerCase().includes(query);
}

export function matchesSupportSearch(values: SearchableValue[], query: string) {
  if (!query) {
    return true;
  }

  return values.some((value) => includesSupportSearch(value, query));
}
