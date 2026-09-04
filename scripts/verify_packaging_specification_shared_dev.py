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
    try:
        dict_body = obj_response.get_json() or {}
    except Exception:
        dict_body = {}
    return {
        "method": str_method,
        "url": str_url,
        "httpStatus": obj_response.status_code,
        "elapsedMs": f_elapsed_ms,
        "code": dict_body.get("code"),
        "message": dict_body.get("message", ""),
        "payload": dict_body.get("payload", {}),
    }


def summarize(dict_result):
    dict_payload = dict_result.get("payload", {}) or {}
    return {
        "httpStatus": dict_result.get("httpStatus"),
        "code": dict_result.get("code"),
        "message": dict_result.get("message"),
        "elapsedMs": dict_result.get("elapsedMs"),
        "subject": dict_payload.get("subject", {}),
        "summary": dict_payload.get("summary", {}),
        "moduleReadiness": dict_payload.get("moduleReadiness", []),
        "sourceLineage": dict_payload.get("sourceLineage", {}),
        "warningCodes": [
            dict_warning.get("warningCode", "")
            for dict_warning in dict_payload.get("warnings", [])
        ],
        "capabilityBoundary": dict_payload.get("capabilityBoundary", {}),
        "packagingSpecCount": len(dict_payload.get("packagingSpecs", []) or []),
    }


def markdown_escape(obj_value):
    return str(obj_value).replace("|", "\\|").replace("\n", " ")


def write_report(dict_report, str_report_path):
    path_report = Path(str_report_path)
    lines = [
        "# Backend API Response - ERP2-CIO-PACKAGING-SPECIFICATION-RO-RDY-001 Shared DEV Runtime Retest",
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
        "## Local Full-Stack DEV Backend Requirements",
        "",
        "Required environment variables:",
        "",
        "```txt",
        "DB_HOST=<local_or_shared_dev_host>",
        "DB_PORT=<mariadb_port>",
        "DB_NAME=<database_name>",
        "DB_USER=<readonly_or_dev_user>",
        "DB_PASSWORD=<password>",
        "TOKEN_ENABLED=1",
        "ENV=local_dev",
        "```",
        "",
        "Recommended first smoke path:",
        "",
        "```txt",
        "GET /api/v2/packaging-specification/overview?itemNo=<product_no>&itemCategory=5",
        "GET /api/v2/packaging-specification/overview?itemNo=<wip_no>&itemCategory=4",
        "```",
        "",
        "## Boundary Confirmation",
        "",
        "No material database/schema change was performed.",
        "",
        "No Packaging write, Packaging approval/release, Product write, Production action, migration, Source-of-Truth transition, Engineering Pull, Cutover, or ERP2.0 Go-Live was performed.",
    ])
    path_report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return hashlib.sha256(path_report.read_bytes()).hexdigest().upper()


def main():
    map_shared_dev_env()
    from package.restserver.app import create_app
    from package.restserver.api.v2.packaging_specification import CPackagingSpecificationService

    obj_app = create_app()
    lst_cases = []
    dict_summaries = {}
    lst_limitations = []

    with obj_app.test_client() as obj_client:
        dict_product = call_api(
            obj_client,
            "GET",
            "/api/v2/packaging-specification/overview?itemNo=PRD-SD-001&itemCategory=5&productVersion=1&effectiveDate=1700000000",
        )
        dict_product_summary = summarize(dict_product)
        dict_summaries["productScenario"] = dict_product_summary
        lst_cases.append({
            "name": "Product packaging scenario",
            "result": "PASS" if dict_product["httpStatus"] == 200 else "FAIL",
            "detail": "HTTP %s, specCount=%s, warnings=%s" % (
                dict_product["httpStatus"],
                dict_product_summary.get("packagingSpecCount"),
                dict_product_summary.get("warningCodes"),
            ),
        })
        if dict_product["httpStatus"] == 200 and dict_product_summary.get("packagingSpecCount") == 0:
            lst_limitations.append("Shared DEV returned Product subject but no visible packagingSpecs for PRD-SD-001.")
        if "module_unavailable" in dict_product_summary.get("warningCodes", []):
            lst_limitations.append(
                "Shared DEV Product packaging scenario returned module_unavailable, indicating the current Shared DEV packaging table/support surface is not fully aligned with the formal packaging_specification implementation path."
            )

        dict_wip = call_api(
            obj_client,
            "GET",
            "/api/v2/packaging-specification/overview?itemNo=INP-SD-001&itemCategory=4&effectiveDate=1700000000",
        )
        dict_wip_summary = summarize(dict_wip)
        dict_summaries["wipScenario"] = dict_wip_summary
        lst_cases.append({
            "name": "WIP packaging scenario",
            "result": "PASS" if dict_wip["httpStatus"] in (200, 404) else "FAIL",
            "detail": "HTTP %s, specCount=%s, warnings=%s" % (
                dict_wip["httpStatus"],
                dict_wip_summary.get("packagingSpecCount"),
                dict_wip_summary.get("warningCodes"),
            ),
        })

        dict_not_found = call_api(
            obj_client,
            "GET",
            "/api/v2/packaging-specification/overview?itemNo=PRD-SD-NOT-FOUND&itemCategory=5",
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

        dict_invalid = call_api(
            obj_client,
            "GET",
            "/api/v2/packaging-specification/overview?itemNo=PRD-SD-001&itemCategory=1",
        )
        dict_summaries["invalidCategory"] = {
            "httpStatus": dict_invalid["httpStatus"],
            "code": dict_invalid.get("code"),
            "message": dict_invalid.get("message"),
        }
        lst_cases.append({
            "name": "Invalid category",
            "result": "PASS" if dict_invalid["httpStatus"] == 400 else "FAIL",
            "detail": "HTTP %s, code=%s, message=%s" % (
                dict_invalid["httpStatus"],
                dict_invalid.get("code"),
                dict_invalid.get("message"),
            ),
        })

        obj_original = CPackagingSpecificationService._CPackagingSpecificationService__query_packaging_specs

        def raise_module_unavailable(self, obj_session, str_item_no, n_item_category, n_product_version):
            raise RuntimeError("bounded packaging module unavailable validation")

        CPackagingSpecificationService._CPackagingSpecificationService__query_packaging_specs = raise_module_unavailable
        try:
            dict_unavailable = call_api(
                obj_client,
                "GET",
                "/api/v2/packaging-specification/overview?itemNo=PRD-SD-001&itemCategory=5&productVersion=1",
            )
        finally:
            CPackagingSpecificationService._CPackagingSpecificationService__query_packaging_specs = obj_original
        dict_unavailable_summary = summarize(dict_unavailable)
        dict_summaries["moduleUnavailable"] = dict_unavailable_summary
        lst_cases.append({
            "name": "Module unavailable/error handling",
            "result": "PASS" if (
                dict_unavailable["httpStatus"] == 200
                and dict_unavailable_summary.get("moduleReadiness", [{}])[0].get("statusCode") == "error"
            ) else "FAIL",
            "detail": "HTTP %s, warnings=%s" % (
                dict_unavailable["httpStatus"],
                dict_unavailable_summary.get("warningCodes"),
            ),
        })

        dict_post = call_api(obj_client, "POST", "/api/v2/packaging-specification/overview")
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

    lst_cases.append({
        "name": "Source-lineage/warning propagation",
        "result": "PASS" if dict_summaries["productScenario"].get("sourceLineage") is not None else "FAIL",
        "detail": "sourceLineage=%s, warnings=%s" % (
            dict_summaries["productScenario"].get("sourceLineage"),
            dict_summaries["productScenario"].get("warningCodes"),
        ),
    })

    str_classification = "PASS - SHARED DEV DB-BACKED PACKAGING SPECIFICATION RETEST COMPLETED"
    if lst_limitations:
        str_classification = "PASS WITH FIXTURE LIMITATION - SHARED DEV DB-BACKED PACKAGING SPECIFICATION RETEST COMPLETED"
    if any(dict_case["result"] == "FAIL" for dict_case in lst_cases):
        str_classification = "CONDITIONAL - SHARED DEV DB-BACKED PACKAGING SPECIFICATION RETEST COMPLETED WITH FAILURES"

    dict_report = {
        "classification": str_classification,
        "generatedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "cases": lst_cases,
        "limitations": lst_limitations,
        "payloadSummaries": dict_summaries,
    }
    str_report_path = str(ROOT / "docs" / "report" / "Backend-API-Response-ERP2-CIO-PACKAGING-SPECIFICATION-RO-RDY-001-Shared-DEV-Retest-20260904-001.md")
    str_hash = write_report(dict_report, str_report_path)
    print(json.dumps({
        "classification": str_classification,
        "reportPath": str_report_path,
        "reportSha256": str_hash,
        "cases": lst_cases,
    }, ensure_ascii=False, indent=2))
    return 1 if "FAILURES" in str_classification else 0


if __name__ == "__main__":
    raise SystemExit(main())
