import ast
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
API_DIR = ROOT / "restserver/package/restserver/api"
TABLE_PY = ROOT / "restserver/package/dbwrapper/table.py"
OUT = ROOT / "docs/spec/api/index.md"


def load_table_map():
    table_class_to_name = {}
    tree = ast.parse(TABLE_PY.read_text(encoding="utf-8"))
    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue
        table_name = None
        for stmt in node.body:
            if not isinstance(stmt, ast.Assign):
                continue
            for target in stmt.targets:
                if isinstance(target, ast.Name) and target.id == "__tablename__":
                    if isinstance(stmt.value, ast.Constant):
                        table_name = stmt.value.value
        if table_name:
            table_class_to_name[node.name] = table_name
    return table_class_to_name


def constants_from_file(path):
    constants = {
        "URL_PATH": "/api/v1",
        "URL_PATH_V0": "/api/v0",
        "URL_PATH_DEVICE": "/",
    }
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in tree.body:
        if (
            isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
            and isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, str)
        ):
            constants[node.targets[0].id] = node.value.value
    return constants


def eval_expr(node, constants):
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Name):
        return constants.get(node.id, "{" + node.id + "}")
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        return str(eval_expr(node.left, constants)) + str(eval_expr(node.right, constants))
    if isinstance(node, (ast.List, ast.Tuple)):
        return [eval_expr(item, constants) for item in node.elts]
    return ast.unparse(node) if hasattr(ast, "unparse") else "?"


def get_executor(class_node):
    for stmt in class_node.body:
        if isinstance(stmt, ast.FunctionDef) and stmt.name == "_get_executor":
            for sub in ast.walk(stmt):
                if isinstance(sub, ast.Return):
                    value = sub.value
                    if isinstance(value, ast.Call) and isinstance(value.func, ast.Name):
                        return value.func.id
                    if isinstance(value, ast.Name):
                        return value.id
    return ""


def method_override(class_node, name):
    for stmt in class_node.body:
        if isinstance(stmt, ast.FunctionDef) and stmt.name == name:
            try:
                first = stmt.body[0]
                if isinstance(first, ast.Return):
                    return ast.unparse(first.value)
                return ast.unparse(first)
            except Exception:
                return "overridden"
    return ""


def instantiated_uri(function_node):
    for sub in ast.walk(function_node):
        if isinstance(sub, ast.Call) and isinstance(sub.func, ast.Name) and sub.func.id.endswith("URI"):
            return sub.func.id
    return ""


def extract_routes():
    routes = []
    uri_executor = {}
    uri_overrides = {}
    for path in sorted(API_DIR.glob("*_uri.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        constants = constants_from_file(path)
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                executor = get_executor(node)
                if executor:
                    uri_executor[node.name] = executor
                    uri_overrides[node.name] = {
                        "validate_token": method_override(node, "_is_vaildate_token"),
                        "validate_param": method_override(node, "_is_vaildate_param"),
                        "custom_response": method_override(node, "_is_customized_reponse"),
                    }
        for node in tree.body:
            if not isinstance(node, ast.FunctionDef):
                continue
            for decorator in node.decorator_list:
                if (
                    isinstance(decorator, ast.Call)
                    and isinstance(decorator.func, ast.Attribute)
                    and decorator.func.attr == "route"
                ):
                    route_path = eval_expr(decorator.args[0], constants) if decorator.args else ""
                    methods = []
                    for keyword in decorator.keywords:
                        if keyword.arg == "methods":
                            methods = eval_expr(keyword.value, constants)
                    uri_class = instantiated_uri(node)
                    routes.append(
                        {
                            "blueprint": path.stem.replace("_uri", ""),
                            "uri_file": str(path.relative_to(ROOT)).replace("\\", "/"),
                            "handler": node.name,
                            "path": route_path,
                            "methods": methods or ["GET"],
                            "uri_class": uri_class,
                            "executor": uri_executor.get(uri_class, ""),
                            "overrides": uri_overrides.get(uri_class, {}),
                        }
                    )
    return routes


def extract_executors(table_class_to_name):
    executor_info = {}
    for path in sorted(API_DIR.glob("*.py")):
        if path.name.endswith("_uri.py") or path.name in {"apibase.py", "common.py", "util.py", "__init__.py"}:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in tree.body:
            if not isinstance(node, ast.ClassDef):
                continue
            methods = [
                stmt.name
                for stmt in node.body
                if isinstance(stmt, ast.FunctionDef) and stmt.name in {"get", "post", "put", "delete"}
            ]
            refs = set()
            params = set()
            for sub in ast.walk(node):
                if isinstance(sub, ast.Name) and sub.id in table_class_to_name:
                    refs.add(table_class_to_name[sub.id])
                if isinstance(sub, ast.Call) and isinstance(sub.func, ast.Attribute) and sub.func.attr == "get":
                    if sub.args and isinstance(sub.args[0], ast.Constant) and isinstance(sub.args[0].value, str):
                        params.add(sub.args[0].value)
            if methods or refs:
                executor_info[node.name] = {
                    "file": str(path.relative_to(ROOT)).replace("\\", "/"),
                    "methods": methods,
                    "tables": sorted(refs),
                    "param_names": sorted(params),
                }
    return executor_info


def md_cell(value):
    return str(value or "").replace("|", "\\|").replace("\n", "<br>")


def main():
    table_map = load_table_map()
    routes = extract_routes()
    executors = extract_executors(table_map)
    for route in routes:
        executor = executors.get(route["executor"], {})
        route["executor_file"] = executor.get("file", "")
        route["executor_methods"] = executor.get("methods", [])
        route["tables"] = executor.get("tables", [])
        route["params"] = executor.get("param_names", [])

    routes = sorted(routes, key=lambda item: (item["path"], ",".join(item["methods"])))
    by_blueprint = defaultdict(list)
    for route in routes:
        by_blueprint[route["blueprint"]].append(route)

    lines = [
        "# ERP 2.0 Restserver API Development Index",
        "",
        "> Baseline code: `restserver/package/restserver` on `main`  ",
        "> Database baseline: `docs/database/EWDB_20260526.sql`  ",
        "> Database field reference: `docs/spec/database/index.md`  ",
        "> Runtime baseline: `docs/backend/runtime-verification/RESTSERVER_RUNTIME_EWDB_20260526_20260527.json`  ",
        "> Generated: 2026-05-28",
        "",
        "## Purpose",
        "",
        "This document is the shared API development reference for Codex and the backend engineer. It documents what is confirmed from the current `restserver` source code and explicitly marks items that still require engineer confirmation before frontend/API contract integration.",
        "",
        "## Baseline Status",
        "",
        "| Item | Confirmed Value | Status |",
        "| --- | --- | --- |",
        "| Framework | Flask application factory | Confirmed from `app.py` |",
        "| API prefix | `/api/v1` | Confirmed from `api/common.py` |",
        "| Registered blueprints | 26 | Confirmed by runtime verification |",
        "| Flask URL rules | 70 | Confirmed by runtime verification; includes Flask/app-level rules |",
        "| Documented active API routes | 69 | Confirmed from active `@blueprint.route(...)` decorators in `*_uri.py` |",
        "| ORM tables | 79 | Confirmed by runtime verification |",
        "| DB tables | 79 | Confirmed by runtime verification |",
        "| Response envelope | `{ code, message, payload }` | Confirmed from `CAPIBase.run()` |",
        "| Baseline code review | Pass for runtime/schema/app registration scope | Confirmed from runtime review |",
        "",
        "## Coding Style Confirmed From Restserver",
        "",
        "| Concern | Current Pattern | Status |",
        "| --- | --- | --- |",
        "| App composition | `create_app()` imports and registers Blueprint objects | Confirmed |",
        "| Route files | `restserver/package/restserver/api/*_uri.py` define Flask routes | Confirmed |",
        "| Business executors | Paired `restserver/package/restserver/api/*.py` files contain executor classes | Confirmed |",
        "| Shared runner | URI classes subclass `CAPIBase` and call `.run()` | Confirmed |",
        "| Executor return contract | `(http_status, code, message, payload_dict)` | Confirmed |",
        "| GET inputs | `request.args.get(...)` | Confirmed |",
        "| POST/PUT inputs | JSON body via `request.get_json()`; content type must be `application/json` or `multipart/form-data` | Confirmed |",
        "| DELETE inputs | mixed by endpoint; some use query params and some use JSON/body conventions | Need Engineer Confirmation |",
        "| Auth token behavior | `X_AUTH_TOKEN` required by `CAPIBase` unless URI overrides validation; behavior also depends on `TOKEN_ENABLED` | Need Engineer Confirmation |",
        "| Timezone header | `X_TIMEZONE` is passed into executor methods as `str_timezone` | Confirmed |",
        "",
        "## Standard Response Contract",
        "",
        "All non-customized `CAPIBase` responses are wrapped as:",
        "",
        "```json",
        "{",
        '  "code": 0,',
        '  "message": "success",',
        '  "payload": {}',
        "}",
        "```",
        "",
        "Need Engineer Confirmation:",
        "",
        "- Confirm whether all frontend-facing APIs should always use this envelope, including future dashboard aggregation APIs.",
        "- Confirm canonical success/error `code` values from `package.common.common.EErrorCode` that frontend should handle.",
        "- Confirm whether `message` should remain English strings or move toward i18n-ready message codes.",
        "",
        "## Request Convention",
        "",
        "| Method | Current Source Pattern | Frontend Contract Guidance | Status |",
        "| --- | --- | --- | --- |",
        "| GET | Query string through `request.args` | Use query params; unwrap `{ payload }` | Confirmed |",
        "| POST | JSON body through `request.get_json()` | Send `Content-Type: application/json` | Confirmed |",
        '| PUT | JSON body through `request.get_json()` in many executors; `CAPIBase` logs `request.form.get("param")` | Confirm exact per endpoint before write integration | Need Engineer Confirmation |',
        "| DELETE | Route supports DELETE where declared, but body/query convention varies | Confirm exact per endpoint before write integration | Need Engineer Confirmation |",
        "",
        "## Route Inventory",
        "",
        "The table below is generated from active Flask decorators in `*_uri.py`. `Tables Referenced` is inferred from executor source code references to `CTable*` ORM classes; it is a source-code hint, not a complete SQL trace.",
        "",
        "Note: `auth` is registered as a blueprint in `app.py` but currently has no active route decorators. Runtime route count is 70 while the documented API decorator count is 69; the remaining URL rule is app/framework-level and should be confirmed if the engineer expects another API endpoint.",
        "",
        "| Path | Methods | Blueprint | URI Class | Executor | Executor Methods | Tables Referenced | Query/Body Parameter Hints | Status | Review Note |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]

    for route in routes:
        methods = ", ".join(route["methods"])
        executor_methods = ", ".join(route["executor_methods"])
        tables = ", ".join(route["tables"])
        params = ", ".join(route["params"][:18])
        if len(route["params"]) > 18:
            params += " ..."
        status = "Confirmed"
        note = "Route and executor mapping confirmed from source."
        if not route["executor"]:
            status = "Need Engineer Confirmation"
            note = "Route handler did not map cleanly to a CAPIBase URI executor in static analysis."
        elif not route["tables"] and route["blueprint"] not in {"heartbeat", "user", "auth", "device"}:
            status = "Need Engineer Confirmation"
            note = "No ORM table reference inferred; confirm payload source and business behavior."
        if any(method in {"POST", "PUT", "DELETE"} for method in route["methods"]):
            if status == "Confirmed":
                status = "Need Engineer Confirmation"
                note = "Route exists, but write request body/set dataset requires endpoint-level confirmation before frontend mutation integration."
        values = [
            route["path"],
            methods,
            route["blueprint"],
            route["uri_class"],
            route["executor"],
            executor_methods,
            tables,
            params,
            status,
            note,
        ]
        lines.append("| " + " | ".join(md_cell(value) for value in values) + " |")

    lines += [
        "",
        "## Blueprint Summary",
        "",
        "| Blueprint | Route Count | Main Paths | Primary Tables Inferred | Confirmation Status |",
        "| --- | ---: | --- | --- | --- |",
    ]
    for blueprint in sorted(by_blueprint):
        routes_for_blueprint = by_blueprint[blueprint]
        paths = ", ".join(route["path"] for route in routes_for_blueprint[:6])
        if len(routes_for_blueprint) > 6:
            paths += " ..."
        tables = sorted({table for route in routes_for_blueprint for table in route["tables"]})
        status = "Confirmed" if tables or blueprint in {"heartbeat", "user", "auth", "device"} else "Need Engineer Confirmation"
        lines.append(
            "| "
            + " | ".join(
                [
                    md_cell(blueprint),
                    str(len(routes_for_blueprint)),
                    md_cell(paths),
                    md_cell(", ".join(tables)),
                    status,
                ]
            )
            + " |"
        )

    lines += [
        "",
        "## Get/Set Dataset Documentation Status",
        "",
        "| Dataset Layer | Current Understanding | Status | Next Action |",
        "| --- | --- | --- | --- |",
        "| DB field meaning | Centralized in `docs/spec/database/index.md` | Partially confirmed | Engineer should resolve `Need Review` DB fields. |",
        "| Existing GET payloads | Payload keys are implemented inside executor `get()` methods and wrapped under `{ payload }` | Partially inferred | Need runtime samples or engineer confirmation for each endpoint used by frontend. |",
        "| Existing POST/PUT/DELETE bodies | Often map closely to ORM/table fields, but exact required/optional fields are not documented in source comments | Need Engineer Confirmation | Confirm per endpoint before frontend write integration. |",
        "| Future dashboard GET datasets | Defined separately in frontend/API specs and should be implemented as read-only aggregation APIs | Planned | Start with Warehouse dashboard API. |",
        "| Error dataset | `code` and `message` are common; detailed validation errors are not standardized | Need Engineer Confirmation | Define frontend-safe error handling contract. |",
        "",
        "## Engineer Confirmation Items",
        "",
        "Use this section as the working checklist with the backend engineer.",
        "",
        "| Priority | Item | Why It Matters | Suggested Owner | Status |",
        "| --- | --- | --- | --- | --- |",
        "| P0 | Confirm canonical auth behavior for local/dev/prod: `TOKEN_ENABLED`, `X_AUTH_TOKEN`, login/logout flow | Frontend API client and runtime tests need a stable auth rule | Engineer | Need Confirmation |",
        "| P0 | Confirm exact request body convention for PUT and DELETE endpoints | Avoid frontend write integration mismatches | Engineer | Need Confirmation |",
        "| P0 | Confirm `EErrorCode` values and frontend handling rules | Needed for shared error UI and tests | Engineer + Codex | Need Confirmation |",
        "| P1 | Provide runtime sample responses for core read endpoints: warehouse, inventory, sale, purchase, workorder, batchtrace | Converts route inventory into precise API contract | Engineer | Need Confirmation |",
        "| P1 | Confirm whether future V1 dashboard APIs should be new aggregation endpoints or composed from existing CRUD endpoints | Determines backend/frontend integration strategy | Engineer + Codex | Need Confirmation |",
        "| P1 | Confirm date/time unit convention for `creationTime`, `start_time`, `end_time`, `date`, `month` | Prevents dashboard calculation errors | Engineer + User | Need Confirmation |",
        "| P1 | Confirm enum/status values that are only visible as integers in API payloads | Needed for multilingual labels and visual status tones | Engineer + User | Need Confirmation |",
        "| P2 | Add endpoint-level examples after runtime samples are available | Improves handoff and lowers future regression risk | Codex | Planned |",
        "",
        "## Recommended Backend Development Flow",
        "",
        "1. Keep existing CRUD route behavior stable unless a breaking change is explicitly agreed.",
        "2. Add V1 read-only dashboard aggregation endpoints incrementally, beginning with Warehouse.",
        "3. For each new endpoint, document the dataset before or alongside implementation.",
        "4. Run runtime verification and store output under `docs/backend/runtime-verification/`.",
        "5. Update this API index and the module-specific API spec when route behavior changes.",
        "",
        "## Done Criteria For API Documentation",
        "",
        "- Route exists in source and appears in this index.",
        "- Request query/body fields are documented.",
        "- Response `payload` fields are documented.",
        "- Source DB tables and major fields are linked to `docs/spec/database/index.md`.",
        "- Runtime sample exists for frontend-facing endpoints.",
        "- Any ambiguous item is marked `Need Engineer Confirmation` rather than silently assumed.",
    ]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")
    print(f"routes={len(routes)} blueprints={len(by_blueprint)} table_classes={len(table_map)}")


if __name__ == "__main__":
    main()
