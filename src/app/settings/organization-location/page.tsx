"use client";

import Link from "next/link";
import { useCallback, useEffect, useMemo, useState } from "react";
import { ChevronLeft, ChevronRight, Plus, RefreshCw, Search } from "lucide-react";
import { AppLayout } from "@/layouts/app-layout";
import { DetailPanel } from "@/components/fm01/organization-location/detail-panel";
import { EditDrawer } from "@/components/fm01/organization-location/edit-drawer";
import {
  buildFm01Hierarchy,
  filterFm01Hierarchy,
  HierarchyTree,
  type Fm01HierarchyNode
} from "@/components/fm01/organization-location/hierarchy-tree";
import { fm01ErrorText, fm01Text } from "@/i18n/fm01-copy";
import { getFm01Collection, getFm01Hierarchy, getFm01Record, Fm01ApiError } from "@/services/fm01-organization-location-api";
import {
  fm01ResourceLabels,
  fm01Resources,
  type Fm01Collection,
  type Fm01Hierarchy,
  type Fm01Record,
  type Fm01Resource,
  type Fm01Selection
} from "@/types/fm01-organization-location";

type ViewMode = "hierarchy" | "list";
const PAGE_SIZE = 25;

function collectVisibleIds(nodes: Fm01HierarchyNode[], found = new Set<string>()) {
  for (const node of nodes) {
    found.add(`${node.record.resource}:${node.record.id}`);
    collectVisibleIds(node.children, found);
  }
  return found;
}

function flattenTree(nodes: Fm01HierarchyNode[]): Fm01Record[] {
  return nodes.flatMap((node) => [node.record, ...flattenTree(node.children)]);
}

function LoadingPanel() {
  return (
    <div className="space-y-3 p-4" aria-busy="true">
      {[0, 1, 2, 3, 4].map((row) => <div key={row} className="h-11 animate-pulse rounded-button bg-slate-100" />)}
      <span className="sr-only">{fm01Text("page.loading")}</span>
    </div>
  );
}

function ErrorPanel({ error, onRetry }: { error: Fm01ApiError; onRetry: () => void }) {
  return (
    <div className="m-4 rounded-card border border-danger/30 bg-red-50 p-4" role="alert">
      <p className="text-sm font-medium text-textPrimary">{fm01Text("page.errorTitle")}</p>
      <p className="mt-1 text-sm text-textSecondary">{fm01ErrorText(error.code, error.status, error.correlationId)}</p>
      <button type="button" onClick={onRetry} className="mt-3 min-h-11 rounded-button bg-primary px-4 text-sm font-semibold text-white hover:bg-blue-700 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary">
        {fm01Text("page.retry")}
      </button>
    </div>
  );
}

export default function OrganizationLocationPage() {
  const [mode, setMode] = useState<ViewMode>("hierarchy");
  const [search, setSearch] = useState("");
  const [resourceFilter, setResourceFilter] = useState<Fm01Resource | "all">("all");
  const [hierarchy, setHierarchy] = useState<Fm01Hierarchy | null>(null);
  const [hierarchyLoading, setHierarchyLoading] = useState(true);
  const [hierarchyError, setHierarchyError] = useState<Fm01ApiError>();
  const [hierarchyReload, setHierarchyReload] = useState(0);
  const [expanded, setExpanded] = useState<Set<string>>(() => new Set());
  const [selection, setSelection] = useState<Fm01Selection | null>(null);
  const [detail, setDetail] = useState<Fm01Record | null>(null);
  const [detailLoading, setDetailLoading] = useState(false);
  const [detailError, setDetailError] = useState<Fm01ApiError>();
  const [detailReload, setDetailReload] = useState(0);
  const [editRecord, setEditRecord] = useState<Fm01Record | null>(null);
  const [listResource, setListResource] = useState<Fm01Resource>("legal-entities");
  const [listPage, setListPage] = useState(1);
  const [listData, setListData] = useState<Fm01Collection | null>(null);
  const [listLoading, setListLoading] = useState(false);
  const [listError, setListError] = useState<Fm01ApiError>();
  const [listReload, setListReload] = useState(0);

  useEffect(() => {
    let active = true;
    setHierarchyLoading(true);
    setHierarchyError(undefined);
    setHierarchy(null);
    getFm01Hierarchy()
      .then((data) => { if (active) setHierarchy(data); })
      .catch((error: unknown) => {
        if (active) setHierarchyError(error instanceof Fm01ApiError ? error : new Fm01ApiError("REQUEST_FAILED", undefined));
      })
      .finally(() => { if (active) setHierarchyLoading(false); });
    return () => { active = false; };
  }, [hierarchyReload]);

  useEffect(() => {
    if (!selection) {
      setDetail(null);
      setDetailError(undefined);
      setDetailLoading(false);
      return;
    }
    let active = true;
    setDetail(null);
    setDetailError(undefined);
    setDetailLoading(true);
    getFm01Record(selection.resource, selection.id)
      .then((record) => { if (active) setDetail(record); })
      .catch((error: unknown) => {
        if (active) setDetailError(error instanceof Fm01ApiError ? error : new Fm01ApiError("REQUEST_FAILED", undefined));
      })
      .finally(() => { if (active) setDetailLoading(false); });
    return () => { active = false; };
  }, [selection, detailReload]);

  useEffect(() => {
    if (mode !== "list") return;
    let active = true;
    setListLoading(true);
    setListData(null);
    setListError(undefined);
    const offset = (listPage - 1) * PAGE_SIZE + 1;
    getFm01Collection(listResource, offset, PAGE_SIZE)
      .then((data) => { if (active) setListData(data); })
      .catch((error: unknown) => {
        if (active) setListError(error instanceof Fm01ApiError ? error : new Fm01ApiError("REQUEST_FAILED", undefined));
      })
      .finally(() => { if (active) setListLoading(false); });
    return () => { active = false; };
  }, [mode, listResource, listPage, listReload]);

  const treeNodes = useMemo(() => hierarchy ? buildFm01Hierarchy(hierarchy) : [], [hierarchy]);
  const filteredTree = useMemo(
    () => filterFm01Hierarchy(treeNodes, search, resourceFilter),
    [treeNodes, search, resourceFilter]
  );
  const visibleIds = useMemo(() => collectVisibleIds(treeNodes), [treeNodes]);
  const unattachedRecords = useMemo(() => {
    if (!hierarchy) return [];
    return fm01Resources.flatMap((resource) => hierarchy[resource]).filter((record) => !visibleIds.has(`${record.resource}:${record.id}`));
  }, [hierarchy, visibleIds]);
  const filteredUnattachedRecords = useMemo(() => {
    const normalized = search.trim().toLocaleLowerCase();
    return unattachedRecords.filter((record) =>
      (resourceFilter === "all" || resourceFilter === record.resource) &&
      (!normalized || `${record.ref} ${record.displayName}`.toLocaleLowerCase().includes(normalized))
    );
  }, [unattachedRecords, resourceFilter, search]);
  const listRows = useMemo(() => {
    const rows = listData?.records ?? [];
    const normalized = search.trim().toLocaleLowerCase();
    return normalized
      ? rows.filter((record) => `${record.ref} ${record.displayName}`.toLocaleLowerCase().includes(normalized))
      : rows;
  }, [listData, search]);
  const pageCount = Math.max(1, Math.ceil((listData?.total ?? 0) / PAGE_SIZE));

  const closeDrawer = useCallback(() => setEditRecord(null), []);
  const chooseRecord = useCallback((record: Fm01Record) => {
    setSelection({ resource: record.resource, id: record.id });
  }, []);

  function retryHierarchy() {
    setSelection(null);
    setDetail(null);
    setDetailError(undefined);
    setEditRecord(null);
    setHierarchyReload((value) => value + 1);
  }
  function retryList() { setListReload((value) => value + 1); }
  function retryDetail() { setDetailReload((value) => value + 1); }

  return (
    <AppLayout activePath="/settings" title={fm01Text("page.title")} site={fm01Text("settings.title")}>
      <div className="mx-auto max-w-[1600px] space-y-5">
        <header className="flex flex-col gap-4 border-b border-border pb-4 lg:flex-row lg:items-end lg:justify-between">
          <div className="min-w-0">
            <p className="text-xs font-medium text-textSecondary">{fm01Text("settings.title")} <span aria-hidden="true">/</span> {fm01Text("page.title")}</p>
            <h2 className="mt-1 text-xl font-semibold text-textPrimary">{fm01Text("page.title")}</h2>
            <p className="mt-1 max-w-3xl text-sm leading-6 text-textSecondary">{fm01Text("page.description")}</p>
          </div>
          <div className="flex flex-wrap items-center gap-2">
            <span className="inline-flex min-h-9 items-center rounded-button border border-border bg-white px-3 text-xs font-medium text-textSecondary">{fm01Text("page.apiSource")}</span>
            <button type="button" onClick={retryHierarchy} disabled={hierarchyLoading} className="inline-flex min-h-11 items-center justify-center gap-2 rounded-button border border-border bg-white px-3 text-sm font-medium text-textPrimary hover:bg-slate-50 focus-visible:outline focus-visible:outline-2 focus-visible:outline-primary disabled:cursor-not-allowed disabled:opacity-60">
              <RefreshCw className="h-4 w-4" aria-hidden="true" />{fm01Text("page.refresh")}
            </button>
            <Link href="/settings/organization-location/create" className="inline-flex min-h-11 items-center justify-center gap-2 rounded-button bg-primary px-4 text-sm font-semibold text-white hover:bg-blue-700 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary">
              <Plus className="h-4 w-4" aria-hidden="true" />{fm01Text("page.add")}
            </Link>
          </div>
        </header>

        <div className="flex flex-col gap-3 xl:flex-row xl:items-center xl:justify-between">
          <div className="inline-flex w-fit items-center rounded-button border border-border bg-white p-1" role="tablist" aria-label="組織與地點檢視方式">
            <button type="button" role="tab" aria-selected={mode === "hierarchy"} onClick={() => setMode("hierarchy")} className={`min-h-10 rounded-button px-4 text-sm font-medium focus-visible:outline focus-visible:outline-2 focus-visible:outline-primary ${mode === "hierarchy" ? "bg-primary text-white" : "text-textSecondary hover:bg-slate-50"}`}>{fm01Text("page.hierarchy")}</button>
            <button type="button" role="tab" aria-selected={mode === "list"} onClick={() => setMode("list")} className={`min-h-10 rounded-button px-4 text-sm font-medium focus-visible:outline focus-visible:outline-2 focus-visible:outline-primary ${mode === "list" ? "bg-primary text-white" : "text-textSecondary hover:bg-slate-50"}`}>{fm01Text("page.list")}</button>
          </div>

          <div className="grid grid-cols-1 gap-2 sm:grid-cols-[minmax(240px,1fr)_220px] xl:w-[620px]">
            <label className="flex h-11 min-w-0 items-center gap-2 rounded-input border border-border bg-white px-3 focus-within:border-primary focus-within:ring-2 focus-within:ring-primary/20">
              <Search className="h-4 w-4 shrink-0 text-textSecondary" aria-hidden="true" />
              <span className="sr-only">{fm01Text("page.search")}</span>
              <input value={search} onChange={(event) => setSearch(event.target.value)} placeholder={fm01Text("page.search")} className="min-w-0 flex-1 bg-transparent text-sm text-textPrimary outline-none placeholder:text-textSecondary" />
              {search && <button type="button" onClick={() => setSearch("")} className="min-h-8 rounded px-2 text-xs font-medium text-primary focus-visible:outline focus-visible:outline-2 focus-visible:outline-primary">{fm01Text("page.clear")}</button>}
            </label>
            <label>
              <span className="sr-only">{fm01Text("page.entityFilter")}</span>
              <select
                value={mode === "hierarchy" ? resourceFilter : listResource}
                onChange={(event) => {
                  if (mode === "hierarchy") setResourceFilter(event.target.value as Fm01Resource | "all");
                  else { setListResource(event.target.value as Fm01Resource); setListPage(1); setSelection(null); }
                }}
                className="h-11 w-full rounded-input border border-border bg-white px-3 text-sm text-textPrimary outline-none focus:border-primary focus:ring-2 focus:ring-primary/20"
              >
                {mode === "hierarchy" && <option value="all">全部類型</option>}
                {fm01Resources.map((resource) => <option key={resource} value={resource}>{fm01ResourceLabels[resource]}</option>)}
              </select>
            </label>
          </div>
        </div>

        {mode === "list" && <p className="-mt-1 text-xs text-textSecondary">{fm01Text("page.searchScope")}</p>}

        <div className="grid grid-cols-1 items-start gap-4 xl:grid-cols-[minmax(320px,0.9fr)_minmax(420px,1.1fr)]">
          <section className="min-w-0 rounded-card border border-border bg-white shadow-card" aria-labelledby="fm01-records-title">
            <div className="flex flex-wrap items-center justify-between gap-3 border-b border-border px-4 py-3">
              <h2 id="fm01-records-title" className="text-sm font-semibold text-textPrimary">{mode === "hierarchy" ? fm01Text("page.hierarchy") : fm01Text("page.list")}</h2>
            </div>

            {mode === "hierarchy" && (
              hierarchyLoading ? <LoadingPanel /> : hierarchyError ? <ErrorPanel error={hierarchyError} onRetry={retryHierarchy} /> : hierarchy ? (
                <div className="p-2">
                  {flattenTree(filteredTree).length === 0 && filteredUnattachedRecords.length === 0 ? (
                    <div className="p-6 text-center text-sm text-textSecondary">{search || resourceFilter !== "all" ? fm01Text("page.emptySearch") : fm01Text("page.empty")}</div>
                  ) : (
                    <>
                      {filteredTree.length > 0 && <HierarchyTree nodes={filteredTree} query={search} selected={selection ?? undefined} expanded={expanded} onToggle={(key) => setExpanded((current) => { const next = new Set(current); next.has(key) ? next.delete(key) : next.add(key); return next; })} onSelect={chooseRecord} />}
                      {unattachedRecords.length > 0 && (
                        <section className="mt-4 rounded-card border border-warning/40 bg-amber-50 p-3" aria-labelledby="fm01-unattached-title">
                          <h3 id="fm01-unattached-title" className="text-sm font-semibold text-textPrimary">未能對應上層的資料</h3>
                          <p className="mt-1 text-xs leading-5 text-textSecondary">這些資料未能依已知父層關係放入階層；仍可選取查看。</p>
                          <ul className="mt-2 divide-y divide-amber-200">
                            {filteredUnattachedRecords.map((record) => (
                                <li key={`${record.resource}:${record.id}`}>
                                  <button type="button" onClick={() => chooseRecord(record)} className="flex min-h-11 w-full items-center justify-between gap-3 py-2 text-left focus-visible:outline focus-visible:outline-2 focus-visible:outline-primary">
                                    <span className="min-w-0"><span className="block truncate text-sm font-medium text-textPrimary">{record.displayName || "（名稱未提供）"}</span><span className="block truncate text-xs text-textSecondary">{fm01ResourceLabels[record.resource]} · {record.ref || `ID ${record.id}`}</span></span>
                                    <span className="shrink-0 text-xs text-primary">查看</span>
                                  </button>
                                </li>
                              ))}
                          </ul>
                        </section>
                      )}
                    </>
                  )}
                </div>
              ) : null
            )}

            {mode === "list" && (
              listLoading ? <LoadingPanel /> : listError ? <ErrorPanel error={listError} onRetry={retryList} /> : listData ? (
                listRows.length === 0 ? (
                  <div className="p-6 text-center text-sm text-textSecondary">{listData.total === 0 ? fm01Text("page.empty") : fm01Text("page.emptySearch")}</div>
                ) : (
                  <>
                    <div className="max-w-full overflow-x-auto">
                      <table className="min-w-[560px] w-full border-collapse text-sm">
                        <caption className="sr-only">{fm01ResourceLabels[listResource]}，{fm01Text("page.rows").replace("{count}", String(listData.total))}</caption>
                        <thead><tr className="border-b border-border bg-slate-50 text-left text-xs text-textSecondary"><th scope="col" className="px-4 py-3 font-medium">參照代碼</th><th scope="col" className="px-4 py-3 font-medium">顯示名稱</th><th scope="col" className="px-4 py-3 text-right font-medium">操作</th></tr></thead>
                        <tbody className="divide-y divide-border">
                          {listRows.map((record) => (
                            <tr key={record.id} className={selection?.resource === record.resource && selection.id === record.id ? "bg-blue-50" : "hover:bg-slate-50"}>
                              <td className="break-all px-4 py-3 text-textPrimary">{record.ref || `ID ${record.id}`}</td>
                              <td className="break-words px-4 py-3 text-textPrimary">{record.displayName || "（名稱未提供）"}</td>
                              <td className="px-4 py-3 text-right"><button type="button" onClick={() => chooseRecord(record)} aria-label={`查看 ${record.ref || record.id}`} className="min-h-10 rounded-button px-3 font-medium text-primary hover:bg-blue-50 focus-visible:outline focus-visible:outline-2 focus-visible:outline-primary">查看</button></td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                    <div className="flex flex-wrap items-center justify-between gap-3 border-t border-border px-4 py-3">
                      <p className="text-xs text-textSecondary">{fm01Text("page.rows").replace("{count}", String(listData.total))}</p>
                      <div className="flex items-center gap-2">
                        <button type="button" onClick={() => setListPage((value) => Math.max(1, value - 1))} disabled={listPage <= 1} aria-label={fm01Text("page.previous")} className="grid h-10 w-10 place-items-center rounded-button border border-border text-textPrimary hover:bg-slate-50 focus-visible:outline focus-visible:outline-2 focus-visible:outline-primary disabled:cursor-not-allowed disabled:opacity-40"><ChevronLeft className="h-4 w-4" aria-hidden="true" /></button>
                        <span aria-live="polite" className="min-w-24 text-center text-xs text-textSecondary">{fm01Text("page.pageCount").replace("{page}", String(listPage)).replace("{pages}", String(pageCount))}</span>
                        <button type="button" onClick={() => setListPage((value) => Math.min(pageCount, value + 1))} disabled={listPage >= pageCount} aria-label={fm01Text("page.next")} className="grid h-10 w-10 place-items-center rounded-button border border-border text-textPrimary hover:bg-slate-50 focus-visible:outline focus-visible:outline-2 focus-visible:outline-primary disabled:cursor-not-allowed disabled:opacity-40"><ChevronRight className="h-4 w-4" aria-hidden="true" /></button>
                      </div>
                    </div>
                  </>
                )
              ) : null
            )}
          </section>

          <DetailPanel
            record={detail}
            hierarchy={hierarchy ?? undefined}
            isLoading={detailLoading}
            error={detailError}
            onRetry={retryDetail}
            onEdit={() => setEditRecord(detail)}
          />
        </div>
      </div>

      <EditDrawer record={editRecord} hierarchy={hierarchy ?? undefined} onClose={closeDrawer} />
    </AppLayout>
  );
}
