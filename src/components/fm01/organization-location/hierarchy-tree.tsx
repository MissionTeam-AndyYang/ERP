"use client";

import { ChevronDown, ChevronRight, Landmark, MapPin, Network, Warehouse } from "lucide-react";
import {
  fm01ResourceLabels,
  type Fm01Hierarchy,
  type Fm01Record,
  type Fm01Resource,
  type Fm01Selection
} from "@/types/fm01-organization-location";
import { fm01Text } from "@/i18n/fm01-copy";

export type Fm01HierarchyNode = {
  record: Fm01Record;
  children: Fm01HierarchyNode[];
};

export function buildFm01Hierarchy(data: Fm01Hierarchy): Fm01HierarchyNode[] {
  const byRelation = (items: Fm01Record[], key: string, id: number) =>
    items.filter((item) => item.relations[key as keyof Fm01Record["relations"]] === id);

  return data["legal-entities"].map((legalEntity) => ({
    record: legalEntity,
    children: byRelation(data.companies, "legal_entity_id", legalEntity.id).map((company) => ({
      record: company,
      children: byRelation(data.sites, "company_id", company.id).map((site) => ({
        record: site,
        children: [
          ...byRelation(data.plants, "site_id", site.id),
          ...byRelation(data.warehouses, "site_id", site.id)
        ].map((node) => ({
          record: node,
          children: node.resource === "warehouses"
            ? byRelation(data.locations, "warehouse_id", node.id).map((location) => ({ record: location, children: [] }))
            : []
        }))
      }))
    }))
  }));
}

export function filterFm01Hierarchy(
  nodes: Fm01HierarchyNode[],
  query: string,
  resource: Fm01Resource | "all"
): Fm01HierarchyNode[] {
  const normalized = query.trim().toLocaleLowerCase();

  return nodes.flatMap((node) => {
    const children = filterFm01Hierarchy(node.children, query, resource);
    const textMatch = !normalized || `${node.record.ref} ${node.record.displayName}`.toLocaleLowerCase().includes(normalized);
    const resourceMatch = resource === "all" || node.record.resource === resource;
    if ((textMatch && resourceMatch) || children.length > 0) {
      return [{ ...node, children }];
    }
    return [];
  });
}

function nodeIcon(resource: Fm01Resource) {
  if (resource === "legal-entities") return Landmark;
  if (resource === "warehouses" || resource === "locations") return resource === "warehouses" ? Warehouse : MapPin;
  return Network;
}

type TreeNodeProps = {
  node: Fm01HierarchyNode;
  level: number;
  query: string;
  selected?: Fm01Selection;
  expanded: Set<string>;
  onToggle: (key: string) => void;
  onSelect: (record: Fm01Record) => void;
};

function TreeNode({ node, level, query, selected, expanded, onToggle, onSelect }: TreeNodeProps) {
  const { record, children } = node;
  const key = `${record.resource}:${record.id}`;
  const canExpand = ["legal-entities", "companies", "sites", "warehouses"].includes(record.resource);
  const isExpanded = query.trim().length > 0 || expanded.has(key);
  const isSelected = selected?.resource === record.resource && selected.id === record.id;
  const Icon = nodeIcon(record.resource);
  const childListId = `fm01-children-${record.resource}-${record.id}`;

  return (
    <li className="list-none">
      <div
        className={`flex min-h-12 items-center gap-2 border-b border-border/70 py-1 pr-2 ${
          isSelected ? "bg-blue-50" : "hover:bg-slate-50"
        }`}
        style={{ paddingLeft: `${level * 18 + 8}px` }}
      >
        {canExpand ? (
          <button
            type="button"
            className="grid h-9 w-9 shrink-0 place-items-center rounded-button text-textSecondary hover:bg-slate-100 focus-visible:outline focus-visible:outline-2 focus-visible:outline-primary"
            aria-label={`${isExpanded ? "收合" : "展開"}${fm01ResourceLabels[record.resource]}：${record.displayName}`}
            aria-expanded={isExpanded}
            aria-controls={childListId}
            onClick={() => onToggle(key)}
            disabled={query.trim().length > 0}
          >
            {isExpanded ? <ChevronDown className="h-4 w-4" aria-hidden="true" /> : <ChevronRight className="h-4 w-4" aria-hidden="true" />}
          </button>
        ) : (
          <span className="h-9 w-9 shrink-0" aria-hidden="true" />
        )}
        <button
          type="button"
          className="flex min-w-0 flex-1 items-center gap-3 rounded-button py-1 text-left focus-visible:outline focus-visible:outline-2 focus-visible:outline-primary"
          aria-current={isSelected ? "true" : undefined}
          onClick={() => onSelect(record)}
        >
          <Icon className="h-4 w-4 shrink-0 text-textSecondary" aria-hidden="true" />
          <span className="min-w-0 flex-1">
            <span className="block truncate text-sm font-medium text-textPrimary">
              {record.displayName || "（名稱未提供）"}
            </span>
            <span className="block truncate text-xs text-textSecondary">
              {fm01ResourceLabels[record.resource]} · {record.ref || "（代碼未提供）"}
            </span>
          </span>
        </button>
      </div>
      {canExpand && (
        <ul id={childListId} hidden={!isExpanded} className="m-0 p-0" aria-label={`${record.displayName} 下層資料`}>
          {children.length === 0 ? (
            <li className="list-none py-2 text-xs text-textSecondary" style={{ paddingLeft: `${(level + 1) * 18 + 52}px` }}>{query.trim() ? fm01Text("page.emptySearch") : fm01Text("page.emptyChildren")}</li>
          ) : children.map((child) => (
            <TreeNode
              key={`${child.record.resource}:${child.record.id}`}
              node={child}
              level={level + 1}
              query={query}
              selected={selected}
              expanded={expanded}
              onToggle={onToggle}
              onSelect={onSelect}
            />
          ))}
        </ul>
      )}
    </li>
  );
}

type HierarchyTreeProps = {
  nodes: Fm01HierarchyNode[];
  query: string;
  selected?: Fm01Selection;
  expanded: Set<string>;
  onToggle: (key: string) => void;
  onSelect: (record: Fm01Record) => void;
};

export function HierarchyTree({ nodes, query, selected, expanded, onToggle, onSelect }: HierarchyTreeProps) {
  if (nodes.length === 0) return null;

  return (
    <ul className="m-0 p-0" aria-label="法人、公司、廠區、廠別、倉庫與庫位階層">
      {nodes.map((node) => (
        <TreeNode
          key={`${node.record.resource}:${node.record.id}`}
          node={node}
          level={0}
          query={query}
          selected={selected}
          expanded={expanded}
          onToggle={onToggle}
          onSelect={onSelect}
        />
      ))}
    </ul>
  );
}
