import ast
import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
API_DIR = ROOT / "restserver/package/restserver/api"
TABLE_PY = ROOT / "restserver/package/dbwrapper/table.py"
API_OUT_DIR = ROOT / "docs/spec/api"
API_INDEX = API_OUT_DIR / "index.md"


COMMON_HEADERS = [
    ("code", "Integer", "API result code", ""),
    ("message", "String", "API result message", ""),
    ("payload", "Object", "Response payload object", ""),
]


def rel(path):
    return str(path.relative_to(ROOT)).replace("\\", "/")


def md(value):
    return str(value or "").replace("|", "\\|").replace("\n", "<br>")


def load_table_map():
    tree = ast.parse(TABLE_PY.read_text(encoding="utf-8"))
    table_map = {}
    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue
        for stmt in node.body:
            if not isinstance(stmt, ast.Assign):
                continue
            for target in stmt.targets:
                if isinstance(target, ast.Name) and target.id == "__tablename__":
                    if isinstance(stmt.value, ast.Constant):
                        table_map[node.name] = stmt.value.value
    return table_map


def constants_from_uri(path):
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
    return ast.unparse(node) if hasattr(ast, "unparse") else "Need Review"


def class_docstrings(tree):
    docs = {}
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            docs[node.name] = ast.get_docstring(node) or ""
    return docs


def function_docstrings(tree):
    docs = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            docs[node.name] = ast.get_docstring(node) or ""
    return docs


def uri_executor(class_node):
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


def method_override_text(class_node, method_name):
    for stmt in class_node.body:
        if isinstance(stmt, ast.FunctionDef) and stmt.name == method_name:
            for sub in stmt.body:
                if isinstance(sub, ast.Return):
                    try:
                        return ast.unparse(sub.value)
                    except Exception:
                        return "overridden"
            return "overridden"
    return ""


def instantiated_uri(function_node):
    for sub in ast.walk(function_node):
        if isinstance(sub, ast.Call) and isinstance(sub.func, ast.Name) and sub.func.id.endswith("URI"):
            return sub.func.id
    return ""


def is_request_args_get(call_node):
    if not isinstance(call_node, ast.Call):
        return False
    if not isinstance(call_node.func, ast.Attribute) or call_node.func.attr != "get":
        return False
    value = call_node.func.value
    return (
        isinstance(value, ast.Attribute)
        and value.attr == "args"
        and isinstance(value.value, ast.Name)
        and value.value.id == "request"
    )


def extract_uri_modules():
    modules = []
    for path in sorted(API_DIR.glob("*_uri.py"), key=lambda p: p.name.lower()):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        constants = constants_from_uri(path)
        uri_to_executor = {}
        uri_overrides = {}
        c_docs = class_docstrings(tree)
        f_docs = function_docstrings(tree)

        for node in tree.body:
            if not isinstance(node, ast.ClassDef):
                continue
            executor = uri_executor(node)
            if executor:
                uri_to_executor[node.name] = executor
                uri_overrides[node.name] = {
                    "validate_token": method_override_text(node, "_is_vaildate_token"),
                    "validate_param": method_override_text(node, "_is_vaildate_param"),
                    "reset_alive_time": method_override_text(node, "_is_reset_alive_time"),
                    "custom_response": method_override_text(node, "_is_customized_reponse"),
                    "docstring": c_docs.get(node.name, ""),
                }

        routes = []
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
                            "path": route_path,
                            "methods": methods or ["GET"],
                            "handler": node.name,
                            "handler_docstring": f_docs.get(node.name, ""),
                            "uri_class": uri_class,
                            "executor": uri_to_executor.get(uri_class, ""),
                            "overrides": uri_overrides.get(uri_class, {}),
                            "uri_file": rel(path),
                        }
                    )
        modules.append(
            {
                "name": path.stem.replace("_uri", ""),
                "uri_file": rel(path),
                "module_file": API_OUT_DIR / (path.stem.replace("_uri", "") + ".md"),
                "routes": routes,
            }
        )
    return modules


def literal_dict(node):
    try:
        value = ast.literal_eval(node)
        return value if isinstance(value, dict) else None
    except Exception:
        return None


def schema_to_fields(schema):
    if not schema:
        return [], {}
    props = schema.get("properties", {}) if isinstance(schema, dict) else {}
    required = set(schema.get("required", [])) if isinstance(schema, dict) else set()
    fields = []
    structure = {}
    for name, spec in props.items():
        typ = "Object"
        if isinstance(spec, dict):
            raw_type = spec.get("type", "Object")
            typ = {
                "string": "String",
                "integer": "Integer",
                "number": "Number",
                "boolean": "Boolean",
                "array": "Array",
                "object": "Object",
            }.get(raw_type, str(raw_type))
        structure[name] = typ
        fields.append(
            {
                "path": name,
                "type": typ,
                "required": "YES" if name in required else "Need Review",
                "description": "Derived from JSON schema field name; semantic description requires review.",
                "enum": "",
            }
        )
    return fields, structure


def collect_method_info(class_node, table_map):
    methods = {}
    for stmt in class_node.body:
        if not isinstance(stmt, ast.FunctionDef) or stmt.name not in {"get", "post", "put", "delete"}:
            continue
        tables = set()
        params = {}
        required_params = set()
        schemas = []
        payload_fields = set()
        returns_tuple = False

        for sub in ast.walk(stmt):
            if isinstance(sub, ast.Name) and sub.id in table_map:
                tables.add(table_map[sub.id])
            if is_request_args_get(sub):
                if sub.args and isinstance(sub.args[0], ast.Constant) and isinstance(sub.args[0].value, str):
                    name = sub.args[0].value
                    typ = "String"
                    if len(sub.args) > 1 and isinstance(sub.args[1], ast.Constant):
                        if isinstance(sub.args[1].value, int):
                            typ = "Integer"
                        elif isinstance(sub.args[1].value, float):
                            typ = "Float"
                    for keyword in sub.keywords:
                        if keyword.arg == "type" and isinstance(keyword.value, ast.Name):
                            if keyword.value.id == "int":
                                typ = "Integer"
                            elif keyword.value.id == "float":
                                typ = "Float"
                    params.setdefault(name, typ)
            if isinstance(sub, ast.UnaryOp) and isinstance(sub.op, ast.Not):
                call = sub.operand
                if is_request_args_get(call):
                    if call.args and isinstance(call.args[0], ast.Constant) and isinstance(call.args[0].value, str):
                        required_params.add(call.args[0].value)
            if isinstance(sub, ast.Assign):
                for target in sub.targets:
                    if isinstance(target, ast.Name) and target.id in {"dict_schema", "schema"}:
                        schema = literal_dict(sub.value)
                        if schema:
                            schemas.append(schema)
                    if isinstance(target, ast.Name) and target.id == "dict_extra_data":
                        if isinstance(sub.value, ast.Dict):
                            for key in sub.value.keys:
                                if isinstance(key, ast.Constant) and isinstance(key.value, str):
                                    payload_fields.add(key.value)
                        else:
                            payload = literal_dict(sub.value)
                            if payload:
                                payload_fields.update(payload.keys())
                    if (
                        isinstance(target, ast.Subscript)
                        and isinstance(target.value, ast.Name)
                        and target.value.id == "dict_extra_data"
                    ):
                        slice_node = target.slice
                        if isinstance(slice_node, ast.Constant) and isinstance(slice_node.value, str):
                            payload_fields.add(slice_node.value)
            if isinstance(sub, ast.Return) and isinstance(sub.value, ast.Tuple):
                returns_tuple = True

        query_fields = [
            {
                "name": name,
                "type": typ,
                "required": "YES" if name in required_params else "Need Review",
                "description": "Derived from request.args.get usage; semantic description requires review.",
            }
            for name, typ in sorted(params.items())
        ]
        body_schema = schemas[0] if schemas else None
        body_fields, body_structure = schema_to_fields(body_schema)
        methods[stmt.name] = {
            "docstring": ast.get_docstring(stmt) or "",
            "tables": sorted(tables),
            "query_fields": query_fields,
            "body_fields": body_fields,
            "body_structure": body_structure,
            "payload_fields": sorted(payload_fields),
            "returns_tuple": returns_tuple,
        }
    return methods


def extract_executor_info(table_map):
    info = {}
    for path in sorted(API_DIR.glob("*.py")):
        if path.name.endswith("_uri.py") or path.name in {"apibase.py", "common.py", "util.py", "__init__.py"}:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                methods = collect_method_info(node, table_map)
                if methods:
                    info[node.name] = {
                        "file": rel(path),
                        "docstring": ast.get_docstring(node) or "",
                        "methods": methods,
                    }
    return info


def route_description(route, method, executor_info):
    if route.get("handler_docstring"):
        return route["handler_docstring"]
    if route.get("overrides", {}).get("docstring"):
        return route["overrides"]["docstring"]
    if executor_info.get("docstring"):
        return executor_info["docstring"]
    method_info = executor_info.get("methods", {}).get(method.lower(), {})
    if method_info.get("docstring"):
        return method_info["docstring"]
    return "Need Review"


def route_status(route, method, executor_info, description):
    method_info = executor_info.get("methods", {}).get(method.lower(), {})
    reasons = []
    if description == "Need Review":
        reasons.append("description cannot be determined from docstring or explicit schema semantics")
    if not route["path"] or method not in route["methods"]:
        reasons.append("route/method not fully resolved")
    if method in {"POST", "PUT"} and not method_info.get("body_fields"):
        reasons.append("request body schema not explicitly parsed")
    if method_info and not method_info.get("returns_tuple"):
        reasons.append("executor return tuple not confirmed")
    if not method_info:
        reasons.append("executor method not found")
    payload = method_info.get("payload_fields", [])
    if method == "GET" and route["executor"] != "CHeartbeat" and not payload:
        reasons.append("success payload is dynamic or not statically explicit")
    if reasons:
        return "Need Review", "; ".join(reasons)
    return "OK", "OK"


def json_block(structure):
    return "```json\n" + json.dumps(structure, ensure_ascii=False, indent=2) + "\n```"


def write_api_index(modules):
    lines = [
        "# ERP 2.0 REST API Index",
        "",
        "> Navigation only. Detailed request/response specifications are stored in each API module file.",
        "",
        "## API Groups",
        "",
    ]
    for module in modules:
        lines.append(f"- [{module['name']}](./{module['name']}.md)")
    lines.append("")
    API_INDEX.write_text("\n".join(lines), encoding="utf-8")


def header_rows(route, method):
    rows = []
    if method in {"POST", "PUT"}:
        rows.append(("Content-Type", "application/json or multipart/form-data, enforced by CAPIBase"))
    token_rule = route.get("overrides", {}).get("validate_token", "")
    if token_rule == "False" or (method == "POST" and "False if self._is_post_method()" in token_rule):
        rows.append(("X_AUTH_TOKEN", "Not required by URI override for this method"))
    else:
        rows.append(("X_AUTH_TOKEN", "Required by CAPIBase unless URI override disables token validation"))
    if rows:
        return rows
    return [("None", "No request header requirement identified from code")]


def write_module_doc(module, executor_info):
    lines = [
        f"# {module['name']} API Group",
        "",
        f"> Source: `{module['uri_file']}`",
        "",
        "## API Summary",
        "",
        "| URL | Method | Description | Status | Review Note |",
        "|----------|----------|----------------|------|------|",
    ]

    if not module["routes"]:
        lines.append("| None | None | No active route decorator found in this module | Need Review | Blueprint may be registered without active API routes. |")
    summary_rows = []
    specs = []
    for route in module["routes"]:
        ex_info = executor_info.get(route["executor"], {})
        for method in route["methods"]:
            desc = route_description(route, method, ex_info)
            status, note = route_status(route, method, ex_info, desc)
            anchor = f"{method.lower()}-{route['path'].strip('/').replace('/', '-').replace('_', '-') or 'root'}"
            summary_rows.append((route["path"], method, desc, status, note, anchor, route, ex_info))
            lines.append(f"| [{md(route['path'])}](#{anchor}) | {method} | {md(desc)} | {status} | {md(note)} |")

    for path, method, desc, status, note, anchor, route, ex_info in summary_rows:
        method_info = ex_info.get("methods", {}).get(method.lower(), {})
        specs += [
            "",
            f"## {method} {route['path']}",
            "",
            f'<a id="{anchor}"></a>',
            "",
            "### Basic Information",
            "",
            "| URL | Method | Description |",
            "|----------|----------|----------------|",
            f"| {md(route['path'])} | {method} | {md(desc)} |",
            "",
            "### Request Header",
            "",
            "| Header | Description |",
            "|----------|----------|",
        ]
        for name, description in header_rows(route, method):
            specs.append(f"| {name} | {md(description)} |")

        specs += ["", "### Query Parameters", ""]
        query_fields = method_info.get("query_fields", [])
        if query_fields:
            specs += ["| Parameter | Type | Required | Description |", "|----------|----------|------|-----|"]
            for item in query_fields:
                specs.append(f"| {md(item['name'])} | {item['type']} | {item['required']} | {md(item['description'])} |")
        else:
            specs.append("None")

        specs += ["", "### Request Body", ""]
        body_structure = method_info.get("body_structure", {})
        body_fields = method_info.get("body_fields", [])
        if method in {"POST", "PUT"}:
            if body_structure:
                specs.append(json_block(body_structure))
                specs += ["", "| Field Path | Type | Required | Description | Enum |", "|----------|----------|------|-----|---|"]
                for field in body_fields:
                    specs.append(
                        f"| {md(field['path'])} | {field['type']} | {field['required']} | {md(field['description'])} | {md(field['enum'])} |"
                    )
            else:
                specs.append("Need Review")
        else:
            specs.append("None")

        specs += [
            "",
            "### Success Response Data",
            "",
            json_block({"code": "Integer", "message": "String", "payload": "Object"}),
            "",
            "| Field Path | Type | Description | Enum |",
            "|----------|----------|------|---|",
        ]
        for field, typ, description, enum in COMMON_HEADERS:
            specs.append(f"| {field} | {typ} | {description} | {enum} |")
        for field in method_info.get("payload_fields", []):
            specs.append(f"| payload.{md(field)} | Need Review | Derived from dict_extra_data key; exact type requires runtime/code review. |  |")
        if not method_info.get("payload_fields"):
            specs.append("| payload | Object | Payload structure is empty or dynamic in code; confirm with runtime sample if frontend uses it. |  |")

        specs += [
            "",
            "### Failed Response Data",
            "",
            "| Field Path | Type | Description | Enum |",
            "|----------|----------|------|---|",
            "| code | Integer | Error code returned by CAPIBase or executor |  |",
            "| message | String | Error message returned by CAPIBase or executor |  |",
            "| payload | Object | Error payload; usually empty unless executor returns extra data |  |",
            "",
            "### Processing Flow",
            "",
            "```",
            "1. Flask route handler instantiates the URI class.",
            "2. URI class delegates request handling to CAPIBase.run().",
            "3. CAPIBase performs content-type, body, token, and alive-time checks according to URI overrides.",
            f"4. CAPIBase calls executor `{route['executor']}.{method.lower()}(str_timezone, str_id)` when supported.",
            "5. Executor returns `(http_status, code, message, payload_dict)`.",
            "6. CAPIBase wraps the result as JSON unless the URI uses a customized response.",
            "```",
            "",
            "### Database Tables Used",
            "",
        ]
        tables = method_info.get("tables", [])
        if tables:
            specs += ["| Table | Purpose |", "|----------|------|"]
            for table in tables:
                specs.append(f"| {table} | Referenced by executor source through ORM model. See `docs/spec/database/index.md#{table}`. |")
        else:
            specs.append("None")

    lines += specs
    module["module_file"].write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    API_OUT_DIR.mkdir(parents=True, exist_ok=True)
    table_map = load_table_map()
    modules = extract_uri_modules()
    executors = extract_executor_info(table_map)
    write_api_index(modules)
    for module in modules:
        write_module_doc(module, executors)
    route_count = sum(len(module["routes"]) for module in modules)
    print(f"modules={len(modules)} routes={route_count} output={rel(API_OUT_DIR)}")


if __name__ == "__main__":
    main()
