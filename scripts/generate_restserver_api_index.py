import ast
import json
import re
import shutil
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
API_DIR = ROOT / "restserver/package/restserver/api"
AUTH_DIR = ROOT / "restserver/package/auth"
TABLE_PY = ROOT / "restserver/package/dbwrapper/table.py"
DB_DOC = ROOT / "docs/spec/database/index.md"
API_OUT_DIR = ROOT / "docs/spec/api"


MODULE_LABELS = {
    "aps": "APS",
    "bankaccount": "銀行帳戶",
    "batchnumber": "批號",
    "batchtrace": "批號追蹤",
    "bom": "BOM",
    "company": "客戶/廠商",
    "contract": "合約",
    "device": "設備",
    "enterprise": "企業",
    "goods": "貨品",
    "heartbeat": "服務心跳",
    "inventory": "庫存",
    "material": "原物料",
    "mix": "混合品項",
    "plstatistics": "產線統計",
    "product": "製成品",
    "productline": "產線",
    "purchase": "採購",
    "quotation": "報價",
    "sale": "銷售",
    "shipwarehouse": "物流倉儲",
    "transitems": "交易品項",
    "user": "使用者",
    "work": "製造作業",
    "workorder": "工單",
}

SEGMENT_LABELS = {
    "login": "登入",
    "logout": "登出",
    "device": "設備",
    "quantity": "製造需求數量",
    "item": "品項",
    "itemprice": "品項價格",
    "process": "製程",
    "tree": "樹狀資料",
    "aps": "APS 資料",
    "record": "紀錄",
    "statistics": "統計",
    "items": "品項清單",
    "months": "月資料",
    "price": "價格",
    "factory": "廠區",
    "station": "站點",
    "equipment": "設備",
    "purchaseorder": "採購單",
    "goodsreceiptnote": "進貨單",
    "payment": "帳款",
    "contract": "合約",
    "arap": "應收應付",
    "productorder": "訂購單",
    "shippingorder": "銷貨單",
    "shiprec": "運輸紀錄",
    "shippayment": "物流帳款",
    "shiparap": "物流應收應付",
    "warehouserec": "倉儲紀錄",
    "warehousepayment": "倉儲帳款",
    "warehousearap": "倉儲應收應付",
    "productdata": "生產數據",
    "expecteddata": "預期資料",
    "assignment": "作業分派",
    "progress": "作業進度",
    "itemcapacity": "品項產能",
    "itemcost": "品項成本",
    "itemloss": "品項損耗",
    "mancapacity": "人力產能",
}

PARAM_LABELS = {
    "start": "分頁起始位置",
    "count": "分頁筆數",
    "no": "編號篩選",
    "id": "資料 ID",
    "type": "類型篩選",
    "category": "類別篩選",
    "subCategory": "子類別篩選",
    "status": "狀態篩選",
    "info": "附加資訊類型",
    "item_no": "料品/品項編號",
    "itemNo": "料品/品項編號",
    "itemCategory": "料品類別",
    "item_ref_no": "交易對象編號",
    "item_ref_displayName": "交易對象顯示名稱",
    "item_ref_name": "交易對象名稱",
    "material_id": "原物料資料 ID",
    "material_no": "原物料編號",
    "supplier_no": "供應商編號",
    "product_no": "製成品編號",
    "order_no": "訂單編號",
    "order": "訂單編號",
    "orderCategory": "訂單類別",
    "purchase_order_no": "採購單號",
    "product_order_no": "訂購單號",
    "work_order_no": "工單號",
    "aps_no": "APS 編號",
    "oneProcess": "主製程",
    "start_time": "查詢開始時間",
    "end_time": "查詢結束時間",
    "start_date": "查詢開始日期",
    "end_date": "查詢結束日期",
    "inventoryType": "庫存異動類型",
    "batchNumber": "批號",
    "batch_number": "批號",
    "commit": "是否提交/確認統計條件",
    "date": "日期",
    "displayName": "顯示名稱",
    "itemStyle": "品項樣式",
    "children": "是否包含子項目",
    "name": "名稱",
    "process": "製程",
    "registerNo": "設備註冊編號",
    "username": "登入帳號",
    "password": "登入密碼",
    "token": "登入 token",
}


def rel(path):
    return str(path.relative_to(ROOT)).replace("\\", "/")


def md(value):
    return str(value or "").replace("|", "\\|").replace("\n", "<br>")


def type_from_schema(raw):
    return {
        "string": "String",
        "integer": "Integer",
        "number": "Number",
        "boolean": "Boolean",
        "array": "Array",
        "object": "Object",
    }.get(str(raw), str(raw).title())


def type_from_ast(node):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool):
            return "Boolean"
        if isinstance(node.value, int):
            return "Integer"
        if isinstance(node.value, float):
            return "Float"
        if isinstance(node.value, str):
            return "String"
        if node.value is None:
            return "Null"
    if isinstance(node, ast.List):
        return "Need Review"
    if isinstance(node, ast.Dict):
        return "Need Review"
    if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name) and node.func.id in {"util_retrieve_now_time", "int"}:
            return "Integer"
        if isinstance(node.func, ast.Name) and node.func.id in {"get_server_id", "str"}:
            return "String"
        if isinstance(node.func, ast.Name) and node.func.id in {"len"}:
            return "Integer"
        return "Need Review"
    if isinstance(node, ast.Name):
        return {
            "str_token": "String",
            "str_message": "String",
            "n_code": "Integer",
            "n_status_code": "Integer",
            "n_total": "Integer",
        }.get(node.id, "Need Review")
    return "Need Review"


def load_db_fields():
    fields = {}
    if not DB_DOC.exists():
        return fields
    table = None
    for line in DB_DOC.read_text(encoding="utf-8").splitlines():
        if line.startswith("## ") and line not in ("## Table of Contents", "## Generation Notes"):
            table = line[3:].strip()
            continue
        if table and line.startswith("| ") and not line.startswith("| 欄位名稱") and not line.startswith("|----------"):
            parts = [part.strip() for part in line.strip("|").split("|")]
            if len(parts) >= 9:
                fields[(table, parts[0])] = {
                    "type": parts[1],
                    "description": parts[5],
                    "enum": parts[6],
                    "status": parts[7],
                }
    return fields


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
    constants = {"URL_PATH": "/api/v1", "URL_PATH_DEVICE": "/", "URL_PATH_V0": "/api/v0"}
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
    return ast.unparse(node) if hasattr(ast, "unparse") else ""


def uri_executor(class_node):
    for stmt in class_node.body:
        if isinstance(stmt, ast.FunctionDef) and stmt.name == "_get_executor":
            for sub in ast.walk(stmt):
                if isinstance(sub, ast.Return):
                    value = sub.value
                    if isinstance(value, ast.Call) and isinstance(value.func, ast.Name):
                        return value.func.id
    return ""


def override_return(class_node, method_name):
    for stmt in class_node.body:
        if isinstance(stmt, ast.FunctionDef) and stmt.name == method_name:
            for sub in stmt.body:
                if isinstance(sub, ast.Return):
                    try:
                        return ast.unparse(sub.value)
                    except Exception:
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


def literal_dict(node):
    try:
        value = ast.literal_eval(node)
        return value if isinstance(value, dict) else None
    except Exception:
        return None


def extract_modules():
    modules = []
    for path in sorted(API_DIR.glob("*_uri.py"), key=lambda p: p.name.lower()):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        constants = constants_from_uri(path)
        uri_map = {}
        overrides = {}
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                executor = uri_executor(node)
                if executor:
                    uri_map[node.name] = executor
                    overrides[node.name] = {
                        "validate_token": override_return(node, "_is_vaildate_token"),
                        "validate_param": override_return(node, "_is_vaildate_param"),
                        "reset_alive": override_return(node, "_is_reset_alive_time"),
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
                            "uri_class": uri_class,
                            "executor": uri_map.get(uri_class, ""),
                            "overrides": overrides.get(uri_class, {}),
                        }
                    )
        modules.append(
            {
                "name": path.stem.replace("_uri", ""),
                "uri_file": rel(path),
                "routes": sorted(routes, key=lambda r: r["path"]),
            }
        )
    return modules


def schema_fields(schema):
    if not isinstance(schema, dict):
        return [], {}
    props = schema.get("properties", {})
    required = set(schema.get("required", []))
    fields = []
    structure = {}
    for name, spec in props.items():
        spec = spec if isinstance(spec, dict) else {}
        field_type = type_from_schema(spec.get("type", "object"))
        is_required = name in required or spec.get("required") is True or spec.get("minLength", 0) > 0
        structure[name] = field_type
        fields.append(
            {
                "path": name,
                "type": field_type,
                "required": "YES" if is_required else "NO",
                "description": PARAM_LABELS.get(name, f"{name} 欄位"),
                "enum": "",
            }
        )
    return fields, structure


def table_attr_name(node):
    if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
        return node.value.id, node.attr
    return None, None


def extract_query_context(stmt, table_map):
    params = {}
    required = set()
    table_fields = {}
    for sub in ast.walk(stmt):
        if is_request_args_get(sub) and sub.args and isinstance(sub.args[0], ast.Constant):
            name = sub.args[0].value
            ptype = "String"
            if len(sub.args) > 1 and isinstance(sub.args[1], ast.Constant):
                if isinstance(sub.args[1].value, int):
                    ptype = "Integer"
                elif isinstance(sub.args[1].value, float):
                    ptype = "Float"
            for keyword in sub.keywords:
                if keyword.arg == "type" and isinstance(keyword.value, ast.Name):
                    ptype = {"int": "Integer", "float": "Float", "str": "String"}.get(keyword.value.id, ptype)
            params[name] = ptype
        if isinstance(sub, ast.UnaryOp) and isinstance(sub.op, ast.Not) and is_request_args_get(sub.operand):
            call = sub.operand
            if call.args and isinstance(call.args[0], ast.Constant):
                required.add(call.args[0].value)
        if isinstance(sub, ast.Compare):
            left_table, left_field = table_attr_name(sub.left)
            if left_table in table_map:
                for comp in sub.comparators:
                    if is_request_args_get(comp) and comp.args and isinstance(comp.args[0], ast.Constant):
                        table_fields[comp.args[0].value] = (table_map[left_table], left_field)
    return params, required, table_fields


def assign_name(target):
    if isinstance(target, ast.Name):
        return target.id
    return ""


def dict_structure_from_ast(dict_node, local_structures=None):
    local_structures = local_structures or {}
    result = {}
    if not isinstance(dict_node, ast.Dict):
        return result
    for key, value in zip(dict_node.keys, dict_node.values):
        if not isinstance(key, ast.Constant) or not isinstance(key.value, str):
            continue
        if isinstance(value, ast.Dict):
            result[key.value] = dict_structure_from_ast(value, local_structures)
        elif isinstance(value, ast.List):
            result[key.value] = []
        elif isinstance(value, ast.Name) and value.id in local_structures:
            result[key.value] = local_structures[value.id]
        else:
            result[key.value] = type_from_ast(value)
    return result


def merge_structure(target, path, value):
    cur = target
    for key in path[:-1]:
        cur = cur.setdefault(key, {})
    cur[path[-1]] = value


def flatten_structure(prefix, obj):
    rows = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            path = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                if value:
                    rows.extend(flatten_structure(path, value))
                else:
                    rows.append((path, "Need Review"))
            elif isinstance(value, list):
                if value and isinstance(value[0], dict):
                    rows.extend(flatten_structure(path + "[]", value[0]))
                else:
                    rows.append((path, "Need Review"))
            else:
                rows.append((path, value))
    else:
        rows.append((prefix, obj))
    return rows


def extract_method_info(class_node, table_map, db_fields, service_tables):
    result = {}
    helper_tables = defaultdict(set)
    helper_names = set()
    for stmt in class_node.body:
        if isinstance(stmt, ast.FunctionDef) and stmt.name.startswith("_"):
            for sub in ast.walk(stmt):
                if isinstance(sub, ast.Name) and sub.id in table_map:
                    helper_tables[stmt.name].add(table_map[sub.id])
    for stmt in class_node.body:
        if not isinstance(stmt, ast.FunctionDef) or stmt.name not in {"get", "post", "put", "delete"}:
            continue
        tables = set()
        params, required_params, table_field_context = extract_query_context(stmt, table_map)
        schemas = []
        local_structures = {}
        payload = {}
        service_calls = []
        steps = []
        returns_tuple = False
        for sub in ast.walk(stmt):
            if isinstance(sub, ast.Name) and sub.id in table_map:
                tables.add(table_map[sub.id])
            if isinstance(sub, ast.Call) and isinstance(sub.func, ast.Attribute):
                if isinstance(sub.func.value, ast.Call) and isinstance(sub.func.value.func, ast.Name):
                    service_calls.append(f"{sub.func.value.func.id}.{sub.func.attr}")
                    tables.update(service_tables.get((sub.func.value.func.id, sub.func.attr), set()))
                if isinstance(sub.func.value, ast.Name) and sub.func.value.id == "self":
                    helper_names.add(sub.func.attr)
                    tables.update(helper_tables.get(sub.func.attr, set()))
            if isinstance(sub, ast.Assign):
                value_dict = literal_dict(sub.value)
                for target in sub.targets:
                    name = assign_name(target)
                    if name in {"dict_schema", "schema"} and value_dict:
                        schemas.append(value_dict)
                    elif name:
                        if isinstance(sub.value, ast.Dict):
                            local_structures[name] = dict_structure_from_ast(sub.value, local_structures)
                        elif isinstance(sub.value, ast.List):
                            local_structures[name] = []
                    if name == "dict_extra_data":
                        if isinstance(sub.value, ast.Dict):
                            payload.update(dict_structure_from_ast(sub.value, local_structures))
                    if (
                        isinstance(target, ast.Subscript)
                        and isinstance(target.value, ast.Name)
                        and target.value.id == "dict_extra_data"
                    ):
                        key = target.slice
                        if isinstance(key, ast.Constant) and isinstance(key.value, str):
                            if isinstance(sub.value, ast.Name) and sub.value.id in local_structures:
                                payload[key.value] = local_structures[sub.value.id]
                            elif isinstance(sub.value, ast.Dict):
                                payload[key.value] = dict_structure_from_ast(sub.value, local_structures)
                            elif isinstance(sub.value, ast.List):
                                payload[key.value] = []
                            else:
                                payload[key.value] = type_from_ast(sub.value)
            if (
                isinstance(sub, ast.Call)
                and isinstance(sub.func, ast.Attribute)
                and sub.func.attr == "append"
                and isinstance(sub.func.value, ast.Name)
                and sub.args
            ):
                list_name = sub.func.value.id
                arg = sub.args[0]
                if isinstance(arg, ast.Name) and arg.id in local_structures:
                    local_structures[list_name] = [local_structures[arg.id]]
                elif isinstance(arg, ast.Dict):
                    local_structures[list_name] = [dict_structure_from_ast(arg, local_structures)]
            if isinstance(sub, ast.Return) and isinstance(sub.value, ast.Tuple):
                returns_tuple = True

        if schemas:
            fields, structure = schema_fields(schemas[0])
        else:
            fields, structure = [], {}

        query_fields = []
        for name, typ in sorted(params.items()):
            description = PARAM_LABELS.get(name)
            table, field = table_field_context.get(name, ("", ""))
            if not description and table and (table, field) in db_fields:
                description = db_fields[(table, field)]["description"]
            if not description:
                description = f"{name} 查詢條件"
            query_fields.append(
                {
                    "name": name,
                    "type": typ,
                    "required": "YES" if name in required_params else "NO",
                    "description": description,
                }
            )

        if fields:
            steps.append("驗證 request body 欄位：" + "、".join(field["path"] for field in fields))
        if query_fields:
            steps.append("讀取查詢條件：" + "、".join(field["name"] for field in query_fields))
        service_actions = []
        for call in sorted(set(service_calls)):
            if call == "CAuth.login":
                service_actions.append("驗證登入帳號密碼並建立 session token")
            elif call == "CAuth.logout":
                service_actions.append("使登入 token 失效")
        steps.extend(service_actions)
        if tables:
            steps.append("查詢資料表並套用條件：" + "、".join(sorted(tables)))
        if payload:
            steps.append("組裝回傳 payload 欄位：" + "、".join(flatten_payload_names(payload)))

        result[stmt.name] = {
            "tables": sorted(tables),
            "query_fields": query_fields,
            "body_fields": fields,
            "body_structure": structure,
            "payload": payload,
            "returns_tuple": returns_tuple,
            "steps": steps,
        }
    return result


def flatten_payload_names(payload):
    names = []
    for path, _typ in flatten_structure("payload", payload):
        names.append(path)
    return names or ["payload"]


def service_table_usage(table_map):
    usage = defaultdict(set)
    for path in AUTH_DIR.glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for cls in tree.body:
            if not isinstance(cls, ast.ClassDef):
                continue
            for method in cls.body:
                if not isinstance(method, ast.FunctionDef):
                    continue
                tables = set()
                for sub in ast.walk(method):
                    if isinstance(sub, ast.Name) and sub.id in table_map:
                        tables.add(table_map[sub.id])
                if tables:
                    usage[(cls.name, method.name)] = tables
    return usage


def executor_info(table_map, db_fields):
    services = service_table_usage(table_map)
    info = {}
    for path in sorted(API_DIR.glob("*.py")):
        if path.name.endswith("_uri.py") or path.name in {"apibase.py", "common.py", "util.py", "__init__.py"}:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                methods = extract_method_info(node, table_map, db_fields, services)
                if methods:
                    info[node.name] = {"file": rel(path), "methods": methods}
    return info


def path_segments(path):
    return [segment for segment in path.strip("/").split("/") if segment and segment not in {"api", "v1"}]


def description(module, route, method):
    segments = path_segments(route["path"])
    labels = [SEGMENT_LABELS.get(seg, MODULE_LABELS.get(seg, seg)) for seg in segments]
    if not labels:
        labels = [MODULE_LABELS.get(module, module)]
    subject = " / ".join(labels)
    if method == "GET":
        return f"查詢{subject}"
    if method == "POST":
        if "登入" in subject:
            return f"{subject}"
        return f"新增{subject}"
    if method == "PUT":
        return f"更新{subject}"
    if method == "DELETE":
        if "登出" in subject:
            return f"{subject}"
        return f"刪除{subject}"
    return f"{subject} API"


def header_rows(route, method):
    rows = []
    if method in {"POST", "PUT"}:
        rows.append(("Content-Type", "application/json"))
    token_rule = route["overrides"].get("validate_token", "")
    disabled = token_rule == "False" or (method == "POST" and "False if self._is_post_method()" in token_rule)
    rows.append(("x-auth-token", "Not required" if disabled else "存取金鑰"))
    return rows


def response_structure(payload):
    return {"code": "Integer", "message": "String", "payload": normalize_response_value(payload or {})}


def normalize_response_value(value):
    if isinstance(value, dict):
        if not value:
            return "Need Review"
        return {key: normalize_response_value(child) for key, child in value.items()}
    if isinstance(value, list):
        if not value:
            return "Need Review"
        return [normalize_response_value(value[0])]
    if value in {"Object", "Array", "List", "Dict"}:
        return "Need Review"
    return value


def response_rows(payload):
    rows = [
        ("code", "Integer", "API 回傳代碼", ""),
        ("message", "String", "API 回傳訊息", ""),
    ]
    if payload:
        for path, typ in flatten_structure("payload", payload):
            rows.append((path, typ if isinstance(typ, str) else "Object", response_desc(path), ""))
    else:
        rows.append(("payload", "Need Review", "程式回傳空 payload 物件，無子欄位可展開", ""))
    return rows


def response_desc(path):
    last = path.split(".")[-1]
    mapping = {
        "total": "符合條件的總筆數",
        "count": "本次回傳筆數",
        "results": "查詢結果清單",
        "token": "登入 token",
        "user": "使用者資訊",
        "employee": "員工資訊",
        "role": "角色",
        "serverTimestamp": "伺服器時間戳記",
        "serverId": "伺服器識別",
        "stock": "批號庫存資訊",
        "nonWork": "非生產來源追蹤資料",
        "work": "生產來源追蹤資料",
    }
    return mapping.get(last, PARAM_LABELS.get(last, f"{last} 回傳欄位"))


def table_purpose(module_name, route_path, table):
    subject = MODULE_LABELS.get(module_name, module_name)
    if module_name == "user":
        if table == "member":
            return "驗證登入帳號"
        if table == "session":
            return "建立或失效登入 Session"
        if table == "employee":
            return "取得登入人員資料與部門權限"
        if table == "device":
            return "確認設備註冊編號與設備角色"
        if table == "user_group":
            return "取得使用者群組與角色"
    if "batchtrace" in route_path:
        return "追蹤批號來源、庫存、生產與出入庫關聯"
    if module_name in {"inventory", "shipwarehouse"}:
        return f"提供{subject}查詢、統計或紀錄資料"
    if module_name in {"sale", "purchase", "contract", "quotation"}:
        return f"提供{subject}單據、合約、帳款或統計資料"
    if module_name in {"work", "workorder", "aps", "plstatistics", "productline"}:
        return f"提供{subject}排程、生產或產能資料"
    if module_name in {"material", "product", "goods", "transitems", "mix", "bom"}:
        return f"提供{subject}主檔、配方或價格資料"
    return f"提供{subject}相關資料"


def write_index(modules):
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
    (API_OUT_DIR / "index.md").write_text("\n".join(lines), encoding="utf-8")


def anchor(method, path):
    text = path.strip("/").replace("/", "-").replace("_", "-") or "root"
    return f"{method.lower()}-{text}"


def status_for(method_info, desc):
    reasons = []
    if not desc:
        reasons.append("API purpose cannot be derived from route/class/function context.")
    if not method_info:
        reasons.append("Executor method is not present in code.")
    elif not method_info["returns_tuple"]:
        reasons.append("Executor return tuple cannot be confirmed from code.")
    if reasons:
        return "Need Review", " ".join(reasons)
    return "OK", "OK"


def module_doc(module, executors):
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
    summary = []
    if not module["routes"]:
        lines.append("| None | None | No active route in this module | Need Review | Module file has no route decorator. |")
    for route in module["routes"]:
        ex = executors.get(route["executor"], {})
        for method in route["methods"]:
            method_info = ex.get("methods", {}).get(method.lower(), {})
            desc = description(module["name"], route, method)
            status, note = status_for(method_info, desc)
            a = anchor(method, route["path"])
            summary.append((route, method, method_info, desc, status, note, a))
            lines.append(f"| [{md(route['path'])}](#{a}) | {method} | {md(desc)} | {status} | {md(note)} |")

    for route, method, method_info, desc, _status, _note, a in summary:
        payload = method_info.get("payload", {})
        lines.extend(
            [
                "",
                f"## {method} {route['path']}",
                "",
                f'<a id="{a}"></a>',
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
        )
        for name, value in header_rows(route, method):
            lines.append(f"| {name} | {md(value)} |")

        lines.extend(["", "### Query Parameters", ""])
        if method_info.get("query_fields"):
            lines.extend(["| Parameter | Type | Required | Description |", "|----------|----------|------|-----|"])
            for field in method_info["query_fields"]:
                lines.append(f"| {field['name']} | {field['type']} | {field['required']} | {md(field['description'])} |")
        else:
            lines.append("None")

        lines.extend(["", "### Request Body", ""])
        if method in {"POST", "PUT"}:
            structure = method_info.get("body_structure", {})
            if structure:
                lines.append("```json")
                lines.append(json.dumps(structure, ensure_ascii=False, indent=2))
                lines.append("```")
                lines.extend(["", "| Field Path | Type | Required | Description | Enum |", "|----------|----------|------|-----|---|"])
                for field in method_info["body_fields"]:
                    lines.append(
                        f"| {field['path']} | {field['type']} | {field['required']} | {md(field['description'])} | {md(field['enum'])} |"
                    )
            else:
                lines.append("Need Review: request body is read in code, but no explicit schema or field check was found.")
        else:
            lines.append("None")

        lines.extend(
            [
                "",
                "### Success Response Data",
                "",
                "```json",
                json.dumps(response_structure(payload), ensure_ascii=False, indent=2),
                "```",
                "",
                "| Field Path | Type | Description | Enum |",
                "|----------|----------|------|---|",
            ]
        )
        for path, typ, desc2, enum in response_rows(payload):
            lines.append(f"| {path} | {typ} | {md(desc2)} | {md(enum)} |")

        lines.extend(
            [
                "",
                "### Failed Response Data",
                "",
                "| Field Path | Type | Description | Enum |",
                "|----------|----------|------|---|",
                "| code | Integer | API 錯誤代碼 |  |",
                "| message | String | API 錯誤訊息 |  |",
                "| payload | Need Review | 錯誤 payload 目前多為空物件，無子欄位可展開 |  |",
                "",
                "### Processing Flow",
                "",
            ]
        )
        steps = method_info.get("steps", [])
        if steps:
            for idx, step in enumerate(steps, 1):
                lines.append(f"{idx}. {md(step)}")
        else:
            lines.append("Need Review: executor method body could not be traced to concrete business logic.")

        lines.extend(["", "### Database Tables Used", ""])
        tables = method_info.get("tables", [])
        if tables:
            lines.extend(["| Table | Purpose |", "|----------|------|"])
            for table in tables:
                lines.append(f"| {table} | {md(table_purpose(module['name'], route['path'], table))} |")
        else:
            lines.append("None")

    (API_OUT_DIR / f"{module['name']}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def clean_output_dir():
    if API_OUT_DIR.exists():
        shutil.rmtree(API_OUT_DIR)
    API_OUT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    table_map = load_table_map()
    db_fields = load_db_fields()
    modules = extract_modules()
    executors = executor_info(table_map, db_fields)
    clean_output_dir()
    write_index(modules)
    for module in modules:
        module_doc(module, executors)
    route_count = sum(len(module["routes"]) for module in modules)
    method_count = sum(len(route["methods"]) for module in modules for route in module["routes"])
    print(f"modules={len(modules)} routes={route_count} methods={method_count} output={rel(API_OUT_DIR)}")


if __name__ == "__main__":
    main()
