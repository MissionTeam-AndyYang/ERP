#!/usr/bin/env python3
"""Verify ERP V1 API response contracts.

This script checks whether a running restserver exposes the expected V1
aggregation/detail API response structure defined by docs/frontend/api.
It intentionally validates response shape only; it does not validate DB values.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class EndpointContract:
    name: str
    path: str
    required_datasets: tuple[str, ...]


MODULE_CONTRACTS: dict[str, EndpointContract] = {
    "warehouse": EndpointContract(
        name="Warehouse dashboard",
        path="/api/v1/warehouse/dashboard",
        required_datasets=(
            "kpis",
            "categorySummaries",
            "capacities",
            "records",
            "risks",
            "tasks",
        ),
    ),
    "orders": EndpointContract(
        name="Orders dashboard",
        path="/api/v1/orders/dashboard",
        required_datasets=(
            "summary",
            "orders",
        ),
    ),
    "planning": EndpointContract(
        name="Planning / APS dashboard",
        path="/api/v1/planning/dashboard",
        required_datasets=(
            "summary",
            "cases",
        ),
    ),
    "purchasing": EndpointContract(
        name="Purchasing dashboard",
        path="/api/v1/purchasing/dashboard",
        required_datasets=(
            "summary",
            "items",
        ),
    ),
    "quality": EndpointContract(
        name="Quality dashboard",
        path="/api/v1/quality/dashboard",
        required_datasets=(
            "summary",
            "inspections",
        ),
    ),
    "production": EndpointContract(
        name="Production dashboard",
        path="/api/v1/production/dashboard",
        required_datasets=(
            "summary",
            "orders",
            "weekSchedule",
            "alerts",
        ),
    ),
    "traceability": EndpointContract(
        name="Traceability dashboard",
        path="/api/v1/traceability/dashboard",
        required_datasets=(
            "summary",
            "records",
        ),
    ),
    "logistics": EndpointContract(
        name="Logistics dashboard",
        path="/api/v1/logistics/dashboard",
        required_datasets=(
            "summary",
            "shipments",
        ),
    ),
    "finance": EndpointContract(
        name="Finance dashboard",
        path="/api/v1/finance/dashboard",
        required_datasets=(
            "summary",
            "cases",
        ),
    ),
    "rd": EndpointContract(
        name="R&D / Costing dashboard",
        path="/api/v1/rd/dashboard",
        required_datasets=(
            "summary",
            "projects",
        ),
    ),
    "workforce": EndpointContract(
        name="Workforce dashboard",
        path="/api/v1/workforce/dashboard",
        required_datasets=(
            "summary",
            "cases",
        ),
    ),
    "dashboard": EndpointContract(
        name="Manager dashboard",
        path="/api/v1/dashboard/manager",
        required_datasets=(
            "managerSnapshot",
            "managerFocusItems",
            "managerDecisionItems",
            "departmentBlockers",
            "todayTasks",
            "preOrderPipeline",
            "productionLines",
            "alertItems",
            "productionTrendData",
            "oeeTrendData",
            "qualityTrendData",
            "alertDistributionData",
            "moduleShortcuts",
        ),
    ),
    "settings": EndpointContract(
        name="Settings / Master Data dashboard",
        path="/api/v1/settings/dashboard",
        required_datasets=(
            "summary",
            "items",
        ),
    ),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify ERP V1 API contracts.")
    parser.add_argument("--base-url", default="http://127.0.0.1:5000")
    parser.add_argument(
        "--module",
        action="append",
        choices=sorted(MODULE_CONTRACTS),
        help="Module to verify. Repeat for multiple modules. Omit to verify all.",
    )
    parser.add_argument("--timeout", type=float, default=8.0)
    parser.add_argument("--output", help="Optional markdown report path.")
    return parser.parse_args()


def normalize_base_url(base_url: str) -> str:
    return base_url.rstrip("/")


def fetch_json(url: str, timeout: float) -> tuple[int | None, Any | None, str | None]:
    request = Request(url, headers={"Accept": "application/json"})
    try:
        with urlopen(request, timeout=timeout) as response:
            status = response.getcode()
            body = response.read().decode("utf-8", errors="replace")
    except HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        return error.code, None, body[:500]
    except URLError as error:
        return None, None, str(error.reason)
    except TimeoutError as error:
        return None, None, str(error)

    try:
        return status, json.loads(body), None
    except json.JSONDecodeError:
        return status, None, body[:500]


def unwrap_data(payload: Any) -> Any:
    if isinstance(payload, dict) and "data" in payload:
        return payload["data"]
    if isinstance(payload, dict) and "payload" in payload:
        return payload["payload"]
    return payload


def validate_contract(contract: EndpointContract, payload: Any) -> list[str]:
    errors: list[str] = []
    data = unwrap_data(payload)
    if not isinstance(data, dict):
        return ["response data must be a JSON object"]

    for dataset in contract.required_datasets:
        if dataset not in data:
            errors.append(f"missing dataset: {dataset}")
    return errors


def verify_module(base_url: str, module: str, timeout: float) -> dict[str, Any]:
    contract = MODULE_CONTRACTS[module]
    url = f"{base_url}{contract.path}"
    start = time.perf_counter()
    status, payload, error = fetch_json(url, timeout)
    elapsed_ms = round((time.perf_counter() - start) * 1000)

    result: dict[str, Any] = {
        "module": module,
        "name": contract.name,
        "url": url,
        "status": status,
        "elapsedMs": elapsed_ms,
        "passed": False,
        "errors": [],
    }

    if status is None:
        result["errors"].append(f"request failed: {error}")
        return result
    if status < 200 or status >= 300:
        result["errors"].append(f"unexpected HTTP status: {status}")
        if error:
            result["errors"].append(f"body: {error}")
        return result
    if payload is None:
        result["errors"].append("response is not valid JSON")
        if error:
            result["errors"].append(f"body: {error}")
        return result

    result["errors"].extend(validate_contract(contract, payload))
    result["passed"] = not result["errors"]
    return result


def write_markdown_report(path: str, base_url: str, results: list[dict[str, Any]]) -> None:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = [
        "# ERP V1 API Contract Verification",
        "",
        f"Generated: {now}",
        f"Base URL: `{base_url}`",
        "",
        "## Summary",
        "",
        "| Module | Status | HTTP | Elapsed | Errors |",
        "| --- | --- | --- | --- | --- |",
    ]
    for result in results:
        status = "PASS" if result["passed"] else "FAIL"
        http = result["status"] if result["status"] is not None else "-"
        errors = "<br>".join(result["errors"]) if result["errors"] else "-"
        lines.append(
            f"| {result['module']} | {status} | {http} | {result['elapsedMs']} ms | {errors} |"
        )

    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- This report validates response shape only.",
            "- Failed endpoints may be expected before backend implementation is complete.",
            "- Review this file before committing to ensure no secrets were returned in error bodies.",
            "",
        ]
    )
    with open(path, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))


def main() -> int:
    args = parse_args()
    base_url = normalize_base_url(args.base_url)
    modules = args.module or sorted(MODULE_CONTRACTS)

    results = [verify_module(base_url, module, args.timeout) for module in modules]

    for result in results:
        status = "PASS" if result["passed"] else "FAIL"
        print(f"{status} {result['module']} {result['url']} ({result['elapsedMs']} ms)")
        for error in result["errors"]:
            print(f"  - {error}")

    if args.output:
        write_markdown_report(args.output, base_url, results)
        print(f"\nReport written: {args.output}")

    return 0 if all(result["passed"] for result in results) else 1


if __name__ == "__main__":
    sys.exit(main())
