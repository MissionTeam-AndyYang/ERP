import ast
import json
import re
import shutil
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
API_DIR = ROOT / "restserver/package/restserver/api"
AUTH_DIR = ROOT / "restserver/package/auth"
ITEMS_DIR = ROOT / "restserver/package/items"
CONTRACT_DIR = ROOT / "restserver/package/contract"
ARAP_DIR = ROOT / "restserver/package/arap"
STATISTIC_DIR = ROOT / "restserver/package/statistic"
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
    "item": "設備料品作業",
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
    "data": "資料",
    "group": "棧板群組",
    "purchase": "採購",
    "manufacture": "製造",
    "sales": "銷售",
    "other": "其他",
    "info": "批號資訊",
    "groupInfo": "棧板群組資訊",
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
    "dateTimestampUTC": "UTC 日期時間戳記",
    "shift": "班別",
    "refProcess": "參照製程",
    "batchNo": "批號",
    "groupNo": "棧板群組編號",
    "devAction": "設備動作",
    "refNo": "來源單號",
    "refNoSec": "來源子單號",
    "itemBatchNo": "料品批號清單",
    "serialNos": "流水號清單",
    "devDateTimestamp": "設備作業時間戳記",
    "serialNo": "流水號",
    "value": "數量或重量",
    "isValid": "是否有效",
    "action": "設備作業方向",
    "refDateTimestamp": "來源單據日期時間戳記",
    "itemName": "料品名稱",
    "itemVendor": "料品供應商或交易對象",
    "itemType": "料品類型",
    "itemAmount": "料品作業數量",
    "itemAmountUnit": "料品作業單位",
    "itemComment": "料品備註",
    "itemPageType": "設備作業頁面類型",
    "itemMaxWeight": "允收最大重量",
    "itemMinWeight": "允收最小重量",
    "validDateTimestamp": "效期時間戳記",
    "results": "資料清單",
    "total": "總筆數",
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


def api_type_from_db_type(raw):
    text = str(raw or "").upper()
    if any(token in text for token in ("INT", "BIGINT", "TINYINT", "SMALLINT")):
        return "Integer"
    if any(token in text for token in ("FLOAT", "DOUBLE", "DECIMAL", "NUMERIC")):
        return "Float"
    if any(token in text for token in ("CHAR", "TEXT", "VARCHAR", "LONGTEXT", "MEDIUMTEXT")):
        return "String"
    if "BOOL" in text:
        return "Boolean"
    if "JSON" in text:
        return "String"
    return "String"


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


def table_structure(table, db_fields):
    fields = {
        field: meta
        for (table_name, field), meta in db_fields.items()
        if table_name == table
    }
    return {
        field: api_type_from_db_type(meta.get("type"))
        for field, meta in fields.items()
    }


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


def literal_value(node):
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Dict):
        return {
            literal_value(key): literal_value(value)
            for key, value in zip(node.keys, node.values)
            if key is not None
        }
    if isinstance(node, ast.List):
        return [literal_value(item) for item in node.elts]
    if isinstance(node, ast.Tuple):
        return [literal_value(item) for item in node.elts]
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        value = literal_value(node.operand)
        return -value if isinstance(value, (int, float)) else ast.unparse(node)
    if isinstance(node, (ast.Name, ast.Attribute)):
        return ast.unparse(node)
    return ast.unparse(node)


def literal_dict(node):
    value = literal_value(node)
    return value if isinstance(value, dict) else None


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


def schema_structure(spec):
    if not isinstance(spec, dict):
        return "Need Review"
    raw_type = spec.get("type", "object")
    if raw_type == "object":
        return {name: schema_structure(child) for name, child in spec.get("properties", {}).items()}
    if raw_type == "array":
        return [schema_structure(spec.get("items", {}))]
    return type_from_schema(raw_type)


def schema_field_rows(spec, prefix=""):
    if not isinstance(spec, dict):
        return []
    raw_type = spec.get("type", "object")
    rows = []
    if raw_type == "object":
        required = set(spec.get("required", []))
        for name, child in spec.get("properties", {}).items():
            child = child if isinstance(child, dict) else {}
            path = f"{prefix}.{name}" if prefix else name
            child_type = type_from_schema(child.get("type", "object"))
            is_required = (
                name in required
                or child.get("required") is True
                or child.get("minLength", 0) > 0
                or child.get("minItems", 0) > 0
            )
            enum_values = child.get("enum", "")
            rows.append(
                {
                    "path": path,
                    "type": child_type,
                    "required": "YES" if is_required else "NO",
                    "description": PARAM_LABELS.get(name, f"{name} 欄位"),
                    "enum": ", ".join(str(item) for item in enum_values) if isinstance(enum_values, list) else "",
                }
            )
            if child.get("type") == "array":
                rows.extend(schema_field_rows(child.get("items", {}), path + "[]"))
            elif child.get("type", "object") == "object":
                rows.extend(schema_field_rows(child, path))
    return rows


def schema_fields(schema):
    if not isinstance(schema, dict):
        return [], {}
    return schema_field_rows(schema), schema_structure(schema)


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


def tuple_result_name(target):
    if isinstance(target, ast.Tuple) and target.elts:
        last = target.elts[-1]
        if isinstance(last, ast.Name):
            return last.id
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


def query_tables_from_node(node, table_map):
    tables = []
    for sub in ast.walk(node):
        if not isinstance(sub, ast.Call):
            continue
        if not isinstance(sub.func, ast.Attribute) or sub.func.attr != "query":
            continue
        for arg in sub.args:
            if isinstance(arg, ast.Name) and arg.id in table_map:
                tables.append(table_map[arg.id])
            elif isinstance(arg, ast.Attribute) and isinstance(arg.value, ast.Name) and arg.value.id in table_map:
                tables.append(table_map[arg.value.id])
            elif isinstance(arg, ast.Tuple):
                for item in arg.elts:
                    if isinstance(item, ast.Name) and item.id in table_map:
                        tables.append(table_map[item.id])
                    elif isinstance(item, ast.Attribute) and isinstance(item.value, ast.Name) and item.value.id in table_map:
                        tables.append(table_map[item.value.id])
    result = []
    for table in tables:
        if table not in result:
            result.append(table)
    return result


def object_as_dict_structure(node, var_tables, db_fields):
    if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name) or node.func.id != "object_as_dict":
        return None
    if not node.args:
        return None
    arg = node.args[0]
    table = None
    if isinstance(arg, ast.Name):
        value = var_tables.get(arg.id)
        if isinstance(value, str):
            table = value
        elif isinstance(value, list) and value:
            table = value[0]
    elif isinstance(arg, ast.Subscript) and isinstance(arg.value, ast.Name):
        value = var_tables.get(arg.value.id)
        if isinstance(value, list):
            idx = arg.slice
            if isinstance(idx, ast.Constant) and isinstance(idx.value, int) and idx.value < len(value):
                table = value[idx.value]
    if table:
        return table_structure(table, db_fields)
    return None


def infer_ordered_function_structures(function_node, table_map, db_fields):
    local_structures = {}
    var_tables = {}
    list_structures = {}

    def set_target_table(target, tables):
        if isinstance(target, ast.Name):
            var_tables[target.id] = tables[0] if len(tables) == 1 else tables
        elif isinstance(target, ast.Tuple):
            for idx, item in enumerate(target.elts):
                if isinstance(item, ast.Name) and idx < len(tables):
                    var_tables[item.id] = tables[idx]

    def scan_stmt(stmt):
        if isinstance(stmt, ast.Assign):
            tables = query_tables_from_node(stmt.value, table_map)
            service_class, service_method = service_call_name(stmt.value)
            service_structure = service_return_structure(service_class, service_method)
            for target in stmt.targets:
                name = assign_name(target)
                tuple_name = tuple_result_name(target)
                if tuple_name and service_structure is not None:
                    local_structures[tuple_name] = service_structure
                    list_structures[tuple_name] = service_structure
                if tables and name:
                    var_tables[name] = tables
                obj_struct = object_as_dict_structure(stmt.value, var_tables, db_fields)
                if name and obj_struct:
                    local_structures[name] = obj_struct
                elif name and isinstance(stmt.value, ast.Dict):
                    local_structures[name] = dict_structure_from_ast(stmt.value, local_structures)
                elif name and isinstance(stmt.value, ast.ListComp):
                    comp = stmt.value
                    if (
                        comp.generators
                        and isinstance(comp.elt, ast.Call)
                        and isinstance(comp.generators[0].iter, ast.Name)
                    ):
                        iter_tables = var_tables.get(comp.generators[0].iter.id)
                        if isinstance(iter_tables, list) and iter_tables:
                            set_target_table(comp.generators[0].target, iter_tables)
                            obj_struct = object_as_dict_structure(comp.elt, var_tables, db_fields)
                            if obj_struct:
                                local_structures[name] = [obj_struct]
                                list_structures[name] = [obj_struct]
                if (
                    isinstance(target, ast.Subscript)
                    and isinstance(target.value, ast.Name)
                    and isinstance(target.slice, ast.Constant)
                    and isinstance(target.slice.value, str)
                ):
                    container = target.value.id
                    key = target.slice.value
                    value = None
                    if isinstance(stmt.value, ast.Name):
                        value = local_structures.get(stmt.value.id, list_structures.get(stmt.value.id))
                    elif isinstance(stmt.value, ast.Dict):
                        value = dict_structure_from_ast(stmt.value, local_structures)
                    elif isinstance(stmt.value, ast.Call):
                        value = object_as_dict_structure(stmt.value, var_tables, db_fields)
                    if value is not None:
                        current = local_structures.setdefault(container, {})
                        if isinstance(current, dict):
                            current[key] = value

        elif isinstance(stmt, ast.For):
            iter_tables = var_tables.get(stmt.iter.id) if isinstance(stmt.iter, ast.Name) else None
            if isinstance(iter_tables, list):
                set_target_table(stmt.target, iter_tables)
            elif isinstance(iter_tables, str):
                set_target_table(stmt.target, [iter_tables])
            for child in stmt.body:
                scan_stmt(child)

        for child_list_name in ("body", "orelse", "finalbody"):
            for child in getattr(stmt, child_list_name, []):
                if child is not stmt:
                    scan_stmt(child)
        for handler in getattr(stmt, "handlers", []):
            for child in handler.body:
                scan_stmt(child)

        if (
            isinstance(stmt, ast.Expr)
            and isinstance(stmt.value, ast.Call)
            and isinstance(stmt.value.func, ast.Attribute)
            and stmt.value.func.attr == "append"
            and stmt.value.args
        ):
            target = stmt.value.func.value
            value = stmt.value.args[0]
            value_struct = None
            if isinstance(value, ast.Name):
                value_struct = local_structures.get(value.id)
            elif isinstance(value, ast.Dict):
                value_struct = dict_structure_from_ast(value, local_structures)
            elif isinstance(value, ast.Call):
                value_struct = object_as_dict_structure(value, var_tables, db_fields)
            if value_struct is not None:
                if isinstance(target, ast.Name):
                    local_structures[target.id] = [value_struct]
                    list_structures[target.id] = [value_struct]
                elif (
                    isinstance(target, ast.Subscript)
                    and isinstance(target.value, ast.Name)
                    and isinstance(target.slice, ast.Constant)
                    and isinstance(target.slice.value, str)
                ):
                    container = local_structures.setdefault(target.value.id, {})
                    if isinstance(container, dict):
                        container[target.slice.value] = [value_struct]

    for stmt in function_node.body:
        scan_stmt(stmt)
    return local_structures


def service_call_name(node):
    if (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Call)
        and isinstance(node.func.value.func, ast.Name)
    ):
        return node.func.value.func.id, node.func.attr
    return "", ""


def service_return_structure(class_name, method_name):
    if (class_name, method_name) == ("CItems", "get"):
        item_batch = {
            "batchNo": "String",
            "validDateTimestamp": "Integer",
            "serialNos": [{"serialNo": "String", "value": "Number"}],
        }
        return [
            {
                "action": "Integer",
                "refNo": "String",
                "refNoSec": "String",
                "refDateTimestamp": "Integer",
                "refProcess": "Integer",
                "itemNo": "String",
                "itemName": "String",
                "itemVendor": "String",
                "itemType": "Integer",
                "itemCategory": "Integer",
                "itemAmount": "Number",
                "itemAmountUnit": "Integer",
                "itemComment": "String",
                "itemPageType": "Integer",
                "itemMaxWeight": "Number",
                "itemMinWeight": "Number",
                "itemBatchNo": [item_batch],
            }
        ]
    if (class_name, method_name) == ("COrderPayment", "get"):
        return [{
            "no": "String",
            "month": "String",
            "companyName": "String",
            "subOrderNos": ["String"],
            "totalAmount": "Float",
            "dueDate": "Integer",
            "records": [{
                "time": "Integer",
                "action": "Integer",
                "item_no": "String",
                "item_name": "String",
                "batch_number": "String",
                "serial_no": "String",
                "unit": "Integer",
                "count": "Float",
            }],
        }]
    if (class_name, method_name) == ("COrdersProcessMonth", "calculate"):
        return [{"date": "String", "oneProcess": "Integer", "secProcess": "Integer", "total": "Integer"}]
    if (class_name, method_name) in {("CContract", "get"), ("CQuotation", "get")}:
        base = {
            "id": "Integer",
            "no": "String",
            "date": "Integer",
            "category": "Integer",
            "type": "Integer",
            "itemStyle": "Integer",
            "item_ref_no": "String",
            "item_ref_displayName": "String",
            "item_no": "String",
            "item_name": "String",
            "unit": "Integer",
            "price": "Float",
            "count": "Float",
            "amount": "Float",
            "comment": "String",
            "creationTime": "Integer",
            "transItemCategory": "Integer",
            "transItemAttr": "Integer",
            "paymentType": "Integer",
            "paymentDate": "Integer",
            "paymentPeriod": "Integer",
            "unitWarehouse": "Integer",
        }
        if class_name == "CContract":
            base.update({"quotation_no": "String", "quotationDate": "Integer"})
        return [base]
    if (class_name, method_name) in {("CInventoryItemMonth", "retrieve_realTime"), ("CInventoryItemMonth", "calculate")}:
        batch = {
            "specified_no": "String",
            "specified_name": "String",
            "specified_ref_no": "String",
            "endCount": "Float",
            "endAmount": "Float",
            "validDate": "Integer",
            "itemType": "Integer",
        }
        return [{
            "kind": "Integer",
            "specified_no": "String",
            "specified_name": "String",
            "specified_ref_no": "String",
            "beginCount": "Float",
            "beginAmount": "Float",
            "inCount": "Float",
            "inAmount": "Float",
            "outCount": "Float",
            "outAmount": "Float",
            "endCount": "Float",
            "endAmount": "Float",
            "itemCategory": "Integer",
            "itemSubCategory": "Integer",
            "unit": "Integer",
            "price": "Float",
            "nearExpiryCount": "Float",
            "nearExpiryAmount": "Float",
            "expiredCount": "Float",
            "expiredAmount": "Float",
            "batchNo": [batch],
        }]
    return None


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
            elif isinstance(value, list):
                if value and isinstance(value[0], dict):
                    rows.extend(flatten_structure(path + "[]", value[0]))
                elif value:
                    rows.append((path + "[]", value[0]))
            else:
                rows.append((path, value))
    else:
        rows.append((prefix, obj))
    return rows


def merge_missing_structure(base, extra):
    if isinstance(base, dict) and isinstance(extra, dict):
        merged = dict(base)
        for key, value in extra.items():
            if key not in merged or is_unexpanded_value(merged[key]):
                merged[key] = value
            else:
                merged[key] = merge_missing_structure(merged[key], value)
        return merged
    if isinstance(base, list) and isinstance(extra, list):
        if not base:
            return extra
        if not extra:
            return base
        return [merge_missing_structure(base[0], extra[0])]
    return extra if is_unexpanded_value(base) else base


def is_unexpanded_value(value):
    return value in {"Need Review", "Object", "Array", "Dict", "List"} if isinstance(value, str) else value == []


def first_table_payload_structure(tables, db_fields):
    for table in tables:
        structure = table_structure(table, db_fields)
        if structure:
            return [structure]
    return []


def replace_unexpanded_payload(payload, tables, db_fields):
    result = {}
    for key, value in payload.items():
        if key in {"total", "count"} and (value in {"Need Review", "Integer"} if isinstance(value, str) else value == 0):
            result[key] = "Integer"
        elif key == "registerNo" and value == "Need Review":
            result[key] = "String"
        elif key == "results":
            if is_unexpanded_value(value) or value == {}:
                result[key] = first_table_payload_structure(tables, db_fields)
            else:
                result[key] = replace_unexpanded_payload_value(value, tables, db_fields)
        else:
            result[key] = replace_unexpanded_payload_value(value, tables, db_fields)
    return result


def replace_unexpanded_payload_value(value, tables, db_fields):
    if isinstance(value, dict):
        return replace_unexpanded_payload(value, tables, db_fields)
    if isinstance(value, list):
        if not value:
            return first_table_payload_structure(tables, db_fields)
        return [replace_unexpanded_payload_value(value[0], tables, db_fields)]
    if value in {"Need Review", "Object", "Dict", "Array", "List"}:
        if value in {"Array", "List"}:
            inferred = first_table_payload_structure(tables, db_fields)
            return inferred if inferred else []
        if value in {"Object", "Dict"}:
            return {}
        return "String"
    return value


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
        ordered_structures = infer_ordered_function_structures(stmt, table_map, db_fields)
        local_structures = dict(ordered_structures)
        payload = {}
        service_calls = []
        steps = []
        returns_tuple = False
        for sub in ast.walk(stmt):
            if isinstance(sub, ast.Name) and sub.id in table_map:
                tables.add(table_map[sub.id])
            if isinstance(sub, ast.Call) and isinstance(sub.func, ast.Attribute):
                service_class, service_method = service_call_name(sub)
                if service_class and service_method:
                    service_calls.append(f"{service_class}.{service_method}")
                    tables.update(service_tables.get((service_class, service_method), set()))
                if isinstance(sub.func.value, ast.Name) and sub.func.value.id == "self":
                    helper_names.add(sub.func.attr)
                    tables.update(helper_tables.get(sub.func.attr, set()))
            if isinstance(sub, ast.Assign):
                value_dict = literal_dict(sub.value)
                service_class, service_method = service_call_name(sub.value)
                service_structure = service_return_structure(service_class, service_method)
                for target in sub.targets:
                    name = assign_name(target)
                    tuple_name = tuple_result_name(target)
                    if tuple_name and service_structure is not None:
                        local_structures[tuple_name] = service_structure
                    if name in {"dict_schema", "schema"} and value_dict:
                        schemas.append(value_dict)
                    elif name:
                        if service_structure is not None:
                            local_structures[name] = service_structure
                        elif isinstance(sub.value, ast.Dict):
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

        local_structures = merge_missing_structure(local_structures, ordered_structures)
        payload = merge_missing_structure(payload, local_structures.get("dict_extra_data", {}))
        if class_node.name == "CItemDataGroup" and stmt.name == "get":
            payload["results"] = [{
                "group": "String",
                "batchNo": "String",
                "serialNos": ["String"],
            }]
        payload = replace_unexpanded_payload(payload, sorted(tables), db_fields)

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
    for service_dir in (AUTH_DIR, ITEMS_DIR, CONTRACT_DIR, ARAP_DIR, STATISTIC_DIR):
        if not service_dir.exists():
            continue
        for path in service_dir.glob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for cls in tree.body:
                if not isinstance(cls, ast.ClassDef):
                    continue
                class_tables = set()
                method_tables = {}
                for method in cls.body:
                    if not isinstance(method, ast.FunctionDef):
                        continue
                    tables = set()
                    for sub in ast.walk(method):
                        if isinstance(sub, ast.Name) and sub.id in table_map:
                            tables.add(table_map[sub.id])
                    if tables:
                        method_tables[method.name] = tables
                        class_tables.update(tables)
                for method_name, tables in method_tables.items():
                    usage[(cls.name, method_name)] = tables
                if cls.name == "CItems" and class_tables:
                    usage[(cls.name, "get")].update(class_tables)
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
    if module == "item":
        tail = [segment for segment in segments if segment != "item"]
        item_subjects = {
            ("data",): "設備料品資料",
            ("data", "group"): "設備料品棧板群組資料",
            ("purchase",): "設備採購入庫料品",
            ("manufacture",): "設備製造料品",
            ("sales",): "設備銷售出庫料品",
            ("other",): "設備其他庫存料品",
            ("info",): "設備批號資訊",
            ("groupInfo",): "設備棧板群組資訊",
        }
        subject = item_subjects.get(tuple(tail), "設備料品作業")
        if method == "GET":
            return f"查詢{subject}"
        if method == "POST":
            return f"新增{subject}"
        if method == "PUT":
            return f"更新{subject}"
        if method == "DELETE":
            return f"刪除{subject}"
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
        return {key: normalize_response_value(child) for key, child in value.items()}
    if isinstance(value, list):
        if not value:
            return []
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
    if module_name == "item":
        mapping = {
            "device": "確認設備註冊編號、硬體識別與設備角色，決定可執行的料品作業",
            "goods_receipt_note": "取得採購入庫與採購退回的待作業料品",
            "process_order": "取得領料、退料、餘料、廢料或產出相關製造作業料品",
            "shipping_order": "取得銷售出庫與銷售退回的待作業料品",
            "inventory_order": "取得其他庫存異動的待作業料品",
            "batch_number": "取得或確認料品批號、效期、料品類型與類別",
            "batchno_serialno": "取得或寫入批號流水號、預期數量與有效狀態",
            "batchno_serialno_group": "取得或建立棧板群組與批號流水號分派關係",
            "device_log": "記錄設備端料品作業送出的原始資料與處理結果",
        }
        if table in mapping:
            return mapping[table]
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
