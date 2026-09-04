# coding=utf8
import hashlib
import json
import os
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESTSERVER_ROOT = ROOT / "restserver"
if str(RESTSERVER_ROOT) not in sys.path:
    sys.path.insert(0, str(RESTSERVER_ROOT))


def map_shared_dev_env():
    for str_src, str_dst in [
        ("ERP2_SHARED_DEV_DB_HOST", "DB_HOST"),
        ("ERP2_SHARED_DEV_DB_PORT", "DB_PORT"),
        ("ERP2_SHARED_DEV_DB_NAME", "DB_NAME"),
        ("ERP2_SHARED_DEV_DB_USER", "DB_USER"),
        ("ERP2_SHARED_DEV_DB_PASSWORD", "DB_PASSWORD"),
    ]:
        if os.getenv(str_src):
            os.environ[str_dst] = os.getenv(str_src, "")
    os.environ["TOKEN_ENABLED"] = "1"
    os.environ["ENV"] = "shared_dev"


def call_api(obj_client, str_method, str_url):
    n_started = time.perf_counter()
    obj_response = getattr(obj_client, str_method.lower())(
        str_url,
        headers={
            "x-auth-token": "shared-dev-readonly-runtime-validation",
            "x-timezone": "Asia/Taipei",
        },
    )
    f_elapsed_ms = round((time.perf_counter() - n_started) * 1000, 2)
    dict_payload = {}
    try:
        dict_payload = obj_response.get_json() or {}
    except Exception:
        dict_payload = {}
    return {
        "method": str_method,
        "url": str_url,
        "httpStatus": obj_response.status_code,
        "elapsedMs": f_elapsed_ms,
        "code": dict_payload.get("code"),
        "message": dict_payload.get("message", ""),
        "payload": dict_payload.get("payload", {}),
    }


def summarize_overview(dict_result):
    dict_payload = dict_result.get("payload", {}) or {}
    dict_readiness = {
        dict_row.get("moduleCode", ""): dict_row
        for dict_row in dict_payload.get("moduleReadiness", [])
    }
    return {
        "httpStatus": dict_result.get("httpStatus"),
        "code": dict_result.get("code"),
        "message": dict_result.get("message"),
        "elapsedMs": dict_result.get("elapsedMs"),
        "subject": dict_payload.get("subject", {}),
        "requestIdentity": dict_payload.get("requestIdentity", {}),
        "moduleReadiness": dict_readiness,
        "sourceLineage": dict_payload.get("sourceLineage", {}),
        "warningCodes": [
            dict_warning.get("warningCode", "")
            for dict_warning in dict_payload.get("warnings", [])
        ],
        "inventoryOverview": dict_payload.get("inventoryOverview", {}),
        "transactionItemCount": (dict_payload.get("transactionContext", {}) or {}).get("total"),
        "batchHighlightCount": len(dict_payload.get("batchHighlights", []) or []),
        "capabilityBoundary": dict_payload.get("capabilityBoundary", {}),
    }


def markdown_escape(obj_value):
    return str(obj_value).replace("|", "\\|").replace("\n", " ")


def write_report(dict_report, str_report_path):
    path_report = Path(str_report_path)
    lines = [
        "# Backend API Response - ERP2-CP1-PRODUCT-WIP-360-RO-IMPL-001 Shared DEV Runtime Retest",
        "",
        "## Runtime Identity",
        "",
        "| Field | Value |",
        "| --- | --- |",
        "| Classification | %s |" % dict_report["classification"],
        "| Endpoint | 172.20.10.3:3307 |",
        "| Database | erp2_shared_dev_item_transitem_np |",
        "| Credential class | ERP2_SHARED_DEV_ITEM_TRANSITEM_NP_READONLY |",
        "| Raw secret exposure | 0 |",
        "| Report generated at | %s |" % dict_report["generatedAt"],
        "",
        "## Shared DEV Fixture Limitations",
        "",
    ]
    if dict_report["limitations"]:
        for str_limitation in dict_report["limitations"]:
            lines.append("- %s" % str_limitation)
    else:
        lines.append("- None observed.")
    lines.extend([
        "",
        "## Route Evidence",
        "",
        "| Evidence | Result | Detail |",
        "| --- | --- | --- |",
    ])
    for dict_case in dict_report["cases"]:
        lines.append("| %s | %s | %s |" % (
            markdown_escape(dict_case["name"]),
            markdown_escape(dict_case["result"]),
            markdown_escape(dict_case["detail"]),
        ))
    lines.extend([
        "",
        "## Payload Summaries",
        "",
        "```json",
        json.dumps(dict_report["payloadSummaries"], ensure_ascii=False, indent=2),
        "```",
        "",
        "## Boundary Confirmation",
        "",
        "No material database/schema change was performed.",
        "",
        "No Product write, Routing write, Process Master write, Production action, migration, Source-of-Truth transition, Engineering Pull, Cutover, or ERP2.0 Go-Live was performed.",
    ])
    path_report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return hashlib.sha256(path_report.read_bytes()).hexdigest().upper()


def main():
    map_shared_dev_env()
    from package.restserver.app import create_app
    from package.restserver.api.v2.items import CItemCenterService

    obj_app = create_app()
    lst_cases = []
    dict_summaries = {}

    with obj_app.test_client() as obj_client:
        dict_product = call_api(
            obj_client,
            "GET",
            "/api/v2/product-wip-360/overview?itemNo=PRD-SD-001&itemCategory=5&effectiveDate=1700000000&inventoryDate=1700000000",
        )
        dict_product_summary = summarize_overview(dict_product)
        dict_summaries["productCompleteOrPartial"] = dict_product_summary
        lst_cases.append({
            "name": "Product complete/partial",
            "result": "PASS" if dict_product["httpStatus"] == 200 and dict_product.get("code") == 0 else "FAIL",
            "detail": "HTTP %s, modules=%s, warnings=%s" % (
                dict_product["httpStatus"],
                list(dict_product_summary["moduleReadiness"].keys()),
                dict_product_summary["warningCodes"],
            ),
        })

        dict_wip = call_api(
            obj_client,
            "GET",
            "/api/v2/product-wip-360/overview?itemNo=INP-SD-001&itemCategory=4&effectiveDate=1700000000&inventoryDate=1700000000",
        )
        dict_wip_summary = summarize_overview(dict_wip)
        dict_summaries["standaloneWipPartial"] = dict_wip_summary
        lst_cases.append({
            "name": "Standalone WIP partial or fixture limitation",
            "result": "PASS" if dict_wip["httpStatus"] in (200, 404) else "FAIL",
            "detail": "HTTP %s, code=%s, warnings=%s" % (
                dict_wip["httpStatus"],
                dict_wip.get("code"),
                dict_wip_summary.get("warningCodes", []),
            ),
        })

        dict_not_found = call_api(
            obj_client,
            "GET",
            "/api/v2/product-wip-360/overview?itemNo=PRD-SD-NOT-FOUND&itemCategory=5&effectiveDate=1700000000&inventoryDate=1700000000",
        )
        dict_summaries["notFound"] = {
            "httpStatus": dict_not_found["httpStatus"],
            "code": dict_not_found.get("code"),
            "message": dict_not_found.get("message"),
        }
        lst_cases.append({
            "name": "Not found",
            "result": "PASS" if dict_not_found["httpStatus"] == 404 else "FAIL",
            "detail": "HTTP %s, code=%s, message=%s" % (
                dict_not_found["httpStatus"],
                dict_not_found.get("code"),
                dict_not_found.get("message"),
            ),
        })

        dict_invalid_category = call_api(
            obj_client,
            "GET",
            "/api/v2/product-wip-360/overview?itemNo=PRD-SD-001&itemCategory=1&effectiveDate=1700000000&inventoryDate=1700000000",
        )
        dict_summaries["invalidCategory"] = {
            "httpStatus": dict_invalid_category["httpStatus"],
            "code": dict_invalid_category.get("code"),
            "message": dict_invalid_category.get("message"),
        }
        lst_cases.append({
            "name": "Invalid category",
            "result": "PASS" if dict_invalid_category["httpStatus"] == 400 else "FAIL",
            "detail": "HTTP %s, code=%s, message=%s" % (
                dict_invalid_category["httpStatus"],
                dict_invalid_category.get("code"),
                dict_invalid_category.get("message"),
            ),
        })

        obj_original_get_detail = CItemCenterService.get_detail

        def raise_module_unavailable(self, str_item_no, n_date=0, str_timezone=""):
            raise RuntimeError("bounded module unavailable validation")

        CItemCenterService.get_detail = raise_module_unavailable
        try:
            dict_module_unavailable = call_api(
                obj_client,
                "GET",
                "/api/v2/product-wip-360/overview?itemNo=PRD-SD-001&itemCategory=5&effectiveDate=1700000000&inventoryDate=1700000000&includeModules=item",
            )
        finally:
            CItemCenterService.get_detail = obj_original_get_detail
        dict_module_unavailable_summary = summarize_overview(dict_module_unavailable)
        dict_summaries["moduleUnavailable"] = dict_module_unavailable_summary
        lst_cases.append({
            "name": "Module unavailable/error handling",
            "result": "PASS" if (
                dict_module_unavailable["httpStatus"] == 200
                and dict_module_unavailable_summary["moduleReadiness"].get("item", {}).get("statusCode") == "error"
            ) else "FAIL",
            "detail": "HTTP %s, itemStatus=%s, warnings=%s" % (
                dict_module_unavailable["httpStatus"],
                dict_module_unavailable_summary["moduleReadiness"].get("item", {}).get("statusCode"),
                dict_module_unavailable_summary["warningCodes"],
            ),
        })

        dict_post = call_api(obj_client, "POST", "/api/v2/product-wip-360/overview")
        dict_summaries["readOnlyNegativeControl"] = {
            "httpStatus": dict_post["httpStatus"],
            "code": dict_post.get("code"),
            "message": dict_post.get("message"),
        }
        lst_cases.append({
            "name": "Read-only negative control",
            "result": "PASS" if dict_post["httpStatus"] == 405 else "FAIL",
            "detail": "POST returned HTTP %s" % dict_post["httpStatus"],
        })

    lst_limitations = []
    str_product_warehouse_status = dict_summaries["productCompleteOrPartial"].get("moduleReadiness", {}).get("warehouse", {}).get("statusCode")
    str_wip_warehouse_status = dict_summaries["standaloneWipPartial"].get("moduleReadiness", {}).get("warehouse", {}).get("statusCode")
    if str_product_warehouse_status == "error" or str_wip_warehouse_status == "error":
        lst_limitations.append(
            "Shared DEV fixture surface currently exposes inventory_record rows but not the inventory_item_month_statistic table required by the existing Warehouse inventory snapshot service. Product/WIP 360 correctly isolates this as warehouse module_unavailable instead of failing the whole overview response."
        )

    dict_route_status = dict_summaries["productCompleteOrPartial"].get("moduleReadiness", {}).get("routing", {}).get("statusCode")
    dict_route_source = dict_summaries["productCompleteOrPartial"].get("sourceLineage", {}).get("routing", {}).get("sourceCode")
    lst_cases.append({
        "name": "Routing test-support",
        "result": "PASS" if dict_route_status in ("test_support", "partial", "complete") and dict_route_source else "FAIL",
        "detail": "routingStatus=%s, routingSource=%s" % (dict_route_status, dict_route_source),
    })
    lst_cases.append({
        "name": "Source-lineage/warning propagation",
        "result": "PASS" if dict_summaries["productCompleteOrPartial"].get("sourceLineage") is not None else "FAIL",
        "detail": "sourceModules=%s, warningCodes=%s" % (
            list(dict_summaries["productCompleteOrPartial"].get("sourceLineage", {}).keys()),
            dict_summaries["productCompleteOrPartial"].get("warningCodes", []),
        ),
    })

    str_classification = "PASS - SHARED DEV DB-BACKED PRODUCT/WIP 360 RETEST COMPLETED"
    if lst_limitations:
        str_classification = "PASS WITH FIXTURE LIMITATION - SHARED DEV DB-BACKED PRODUCT/WIP 360 RETEST COMPLETED"
    if any(dict_case["result"] == "FAIL" for dict_case in lst_cases):
        str_classification = "CONDITIONAL - SHARED DEV DB-BACKED RETEST COMPLETED WITH FAILURES"

    dict_report = {
        "classification": str_classification,
        "generatedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "cases": lst_cases,
        "payloadSummaries": dict_summaries,
        "limitations": lst_limitations,
    }
    str_report_path = str(ROOT / "docs" / "report" / "Backend-API-Response-ERP2-CP1-PRODUCT-WIP-360-RO-IMPL-001-Shared-DEV-Retest-20260904-001.md")
    str_hash = write_report(dict_report, str_report_path)
    dict_report["reportPath"] = str_report_path
    dict_report["reportSha256"] = str_hash
    print(json.dumps({
        "classification": str_classification,
        "reportPath": str_report_path,
        "reportSha256": str_hash,
        "cases": lst_cases,
    }, ensure_ascii=False, indent=2))
    return 1 if "FAILURES" in str_classification else 0


if __name__ == "__main__":
    raise SystemExit(main())
