# coding=utf8
import validictory
from package.processorder.processorder import *
from sqlalchemy import distinct

class CPrivilegeControl(object):

    def is_allowed_for_get(self, lst_privileges):
        return any(privilege['category'] == EPrivilegeCategory.SALE and privilege['action'] in (EPrivilegeAction.VIEW, EPrivilegeAction.REPORT)
                   for privilege in lst_privileges)

    def is_allowed_for_post(self, lst_privileges):
        return any(privilege['category'] == EPrivilegeCategory.SALE and privilege['action'] == EPrivilegeAction.CREATION
                   for privilege in lst_privileges)

    def is_allowed_for_put(self, lst_privileges):
        return any(privilege['category'] == EPrivilegeCategory.SALE and privilege['action'] == EPrivilegeAction.MODIFICATION
                   for privilege in lst_privileges)

    def is_allowed_for_delete(self, lst_privileges):
        return any(privilege['category'] == EPrivilegeCategory.SALE and privilege['action'] == EPrivilegeAction.CANCELLATION
                   for privilege in lst_privileges)

class CLaborHours(object):
    def get(self, lst_work_order_no):
        try:
            # 從產製數據角度查詢
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                n_total_product_hours = 0
                lst_labor = []
                if lst_work_order_no:
                    # 區分班長/員工 ?
                    lst_obj_labor = (obj_session.query(
                        CTableProductionDataLabor.action,
                        CTableProductionDataLabor.stationStage,
                        CTableProductionDataLabor.employee_level,
                        func.round(func.coalesce(func.sum(CTableProductionDataLabor.hours), 0), 2).label("labor_hours"),
                        func.count(distinct(CTableProductionDataLabor.employee_no)).label("labor_count")
                    )
                     .filter(CTableProductionDataLabor.work_order_no.in_(lst_work_order_no))
                     .group_by(
                        CTableProductionDataLabor.action,
                        CTableProductionDataLabor.stationStage,
                        CTableProductionDataLabor.employee_level
                    )
                    .order_by(CTableProductionDataLabor.action)
                    .all())

                    labor_groups = defaultdict(list)
                    for action, stationStage, employee_level, labor_hours, labor_count in lst_obj_labor:
                        str_key = (employee_level)
                        labor_groups[str_key].append({"action": action,
                                                      "stationStage": stationStage,
                                                      "employeeLevel": employee_level,
                                                      "count": labor_count,
                                                      "hours": labor_hours
                                                      })

                    dict_temp = {"workPreHours": 0, "workPostHours": 0, "workPreCount": 0,
                                 "workPostCount": 0,
                                 "restPreHours": 0, "restPostHours": 0, "restPreCount": 0,
                                 "restPostCount": 0,
                                 "cleanPreHours": 0, "cleanPostHours": 0, "cleanPreCount": 0,
                                 "cleanPostCount": 0,
                                 "employeeLevel": 0}

                    for tuple_key, lst_items in labor_groups.items():
                        dict_temp["employeeLevel"] = tuple_key
                        for dict_tmp in lst_items:
                            # action 1:工作 2:休息 3:清潔
                            # stationStage 1:前段 2:後段
                            n_action = dict_tmp["action"]
                            n_stationStage = dict_tmp["stationStage"]
                            if n_action == 1:
                                if n_stationStage == 1:
                                    dict_temp["workPreHours"] = dict_tmp["hours"]
                                    dict_temp["workPreCount"] = dict_tmp["count"]
                                elif n_stationStage == 2:
                                    dict_temp["workPostHours"] = dict_tmp["hours"]
                                    dict_temp["workPostCount"] = dict_tmp["count"]
                            elif n_action == 2:
                                if n_stationStage == 1:
                                    dict_temp["restPreHours"] = dict_tmp["hours"]
                                    dict_temp["restPreCount"] = dict_tmp["count"]
                                elif n_stationStage == 2:
                                    dict_temp["restPostHours"] = dict_tmp["hours"]
                                    dict_temp["restPostCount"] = dict_tmp["count"]
                            elif n_action == 3:
                                if n_stationStage == 1:
                                    dict_temp["cleanPreHours"] = dict_tmp["hours"]
                                    dict_temp["cleanPreCount"] = dict_tmp["count"]
                                elif n_stationStage == 2:
                                    dict_temp["cleanPostHours"] = dict_tmp["hours"]
                                    dict_temp["cleanPostCount"] = dict_tmp["count"]

                    lst_labor.append(dict_temp)
                    # 產出時
                    n_total_product_hours = self.__cal_totalProductHours(lst_labor)
        except Exception as error:
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'throw exception (error: %s)' % str(error)
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return n_total_product_hours, lst_labor

    def __cal_totalProductHours(self, lst_labors) -> int:
        # 計算產製總時數
        def get_metrics(pre_h, post_h, pre_c, post_c):
            # 使用 .get() 確保 key 不存在或為 None 時能安全處理
            hours = max(pre_h or 0, post_h or 0)
            count = max(pre_c or 0, post_c or 0)
            return {"hours": hours, "count": count, "total": hours * count}

        n_total_hours = 0
        for dict_labor in lst_labors:
            dict_work = get_metrics(dict_labor.get("workPreHours"), dict_labor.get("workPostHours"),
                               dict_labor.get("workPreCount"), dict_labor.get("workPostCount"))
            dict_rest = get_metrics(dict_labor.get("restPreHours"), dict_labor.get("restPostHours"),
                               dict_labor.get("restPreCount"), dict_labor.get("restPostCount"))
            dict_clean = get_metrics(dict_labor.get("cleanPreHours"), dict_labor.get("cleanPostHours"),
                                dict_labor.get("cleanPreCount"), dict_labor.get("cleanPostCount"))

            # 生產總時數 = 工作總時數 - 休息總時數 - 清潔總時數
            n_total_hours += dict_work["hours"] - dict_rest["hours"] - dict_clean["hours"]
        return n_total_hours


class CProcessOrder(CPrivilegeControl):
    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'total': 0, 'results': []}

        try:
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                lst_where = self.__fill_query_params()
                n_total = (
                    obj_session.query(
                        CTableProcessOrder
                    )
                    .outerjoin(CTableBatchNumber,
                               CTableProcessOrder.no == CTableBatchNumber.ref_no)  # LEFT JOIN，允許 NULL
                    .filter(*lst_where)
                    .filter(CTableBatchNumber.ref_no == None,
                            CTableProcessOrder.category.in_([EProcessOrderCategory.REMAIN, EProcessOrderCategory.WASTE, EProcessOrderCategory.PRODUCT]))  # 排除已經存在的 `process_order.no`
                    .count()
                )

                n_start = 0
                n_count = 0
                if request.args.get('start') and request.args.get('count'):
                    n_start = int(request.args.get('start'))
                    n_count = int(request.args.get('count'))
                if n_count:
                    lst_obj_result = (
                        obj_session.query(
                            CTableProcessOrder
                        )
                        .outerjoin(CTableBatchNumber,
                                   CTableProcessOrder.no == CTableBatchNumber.ref_no)  # LEFT JOIN，允許 NULL
                        .filter(*lst_where)
                        .filter(CTableBatchNumber.ref_no == None,
                                CTableProcessOrder.category.in_([EProcessOrderCategory.REMAIN, EProcessOrderCategory.WASTE, EProcessOrderCategory.PRODUCT]))  # 排除已經存在的 `process_order.no`
                        .order_by(CTableProcessOrder.date.desc())  # 依工單日期排序
                        .offset(n_start)  # 分頁：跳過前 offset 筆
                        .limit(n_count)  # 分頁：取 page_size 筆
                    )

                else:
                    lst_obj_result = (
                        obj_session.query(
                            CTableProcessOrder
                        )
                        .outerjoin(CTableBatchNumber,
                                   CTableProcessOrder.no == CTableBatchNumber.ref_no)  # LEFT JOIN，允許 NULL
                        .filter(*lst_where)
                        .filter(CTableBatchNumber.ref_no == None,
                                CTableProcessOrder.category.in_([EProcessOrderCategory.REMAIN, EProcessOrderCategory.WASTE, EProcessOrderCategory.PRODUCT]))  # 排除已經存在的 `process_order.no`
                        .order_by(CTableProcessOrder.date.desc())  # 依工單日期排序
                        .all()
                    )

                if lst_obj_result:
                    lst_result = [object_as_dict(obj_row) for obj_row in lst_obj_result]
                    if lst_result:
                        dict_extra_data['total'] = n_total
                        dict_extra_data['results'] = lst_result
        except Exception as error:
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'throw exception (error: %s)' % str(error)
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return n_status_code, n_code, str_message, dict_extra_data

    def post(self, str_timezone='' , str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}
        dict_schema = {
            'type': 'object',
            'properties': {
                'start_time': {'type': 'integer'},
                'end_time': {'type': 'integer'},

            },
            'required': ['start_time', 'end_time']
        }
        try:
            dict_param = request.get_json()
            validictory.validate(dict_param, dict_schema)
            if dict_param['work_order_no']:
                CCProcessOrder(str_timezone, dict_param['work_order_no']).gen_process_order(CCProcessOrder.TYPE_ALL)
            else:
                if dict_param['start_time'] and dict_param['end_time']:
                    # get the range of timestamp
                    n_start_day = util_convert_timestamp_to_date(dict_param['start_time'])
                    if dict_param['start_time'] ==  dict_param['end_time']:
                        n_end_day = util_convert_timestamp_to_date(n_start_day, 1) - 1
                    else:
                        n_end_day = util_convert_timestamp_to_date(dict_param['end_time'], 1) - 1
                    # 查找派工單
                    with CDBMgr() as obj_dbmgr:
                        obj_session = obj_dbmgr.get_session()
                        lst_obj_result = (
                            obj_session.query(
                                CTableWorkOrder
                            )
                            .filter(CTableWorkOrder.date.between(n_start_day, n_end_day))
                            .all()
                        )
                        for obj_result in lst_obj_result:
                            CCProcessOrder(str_timezone, obj_result.no).gen_process_order()

        except Exception as error:
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'throw exception (error: %s)' % str(error)
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))

        return n_status_code, n_code, str_message, dict_extra_data


    def put(self, str_timezone='' , str_id=''):
        dict_param = {}
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}
        dict_schema = {'type': 'object',
                       'properties': {}}

        return n_status_code, n_code, str_message, dict_extra_data

    def delete(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}

        return n_status_code, n_code, str_message, dict_extra_data

    def __fill_query_params(self):
        lst_where = []

        if request.args.get('item_no'):
            lst_where.append(CTableProcessOrder.no == request.args.get('item_no'))

        if request.args.get('item_ref_no'):
            lst_where.append(CTableProcessOrder.item_ref_no == request.args.get('item_ref_no'))

        if request.args.get('start_time') and request.args.get('end_time'):
            # get the range of timestamp
            n_start_day = util_convert_timestamp_to_date(int(request.args.get('start_time')))
            if int(request.args.get('start_time')) == int(request.args.get('end_time')):
                n_end_day = util_convert_timestamp_to_date(n_start_day, 1) - 1
            else:
                n_end_day = util_convert_timestamp_to_date(int(request.args.get('end_time')), 1) - 1
            lst_where.append(CTableProcessOrder.date.between(n_start_day, n_end_day))
        return lst_where

    def __gen_no(self, dict_param):
        from datetime import datetime
        str_date = datetime.fromtimestamp(dict_param["date"]).strftime('%y%m%d')
        str_no = "ZP%d%s" %(dict_param["category"], str_date) + util_random_code(3)
        return str_no


class CAssignment(CPrivilegeControl):
    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        #dict_extra_data = {'results': {"input": [], "output": [], "reuse": [], "labors": [], "machines": []}}
        dict_extra_data = {'total': 0, 'count': 0, 'results': []}
        try:
            lst_result = []
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                lst_where = self.__fill_query_params()
                obj_query_base = obj_session.query(CTableWorkOrder).filter(*lst_where)
                n_total = obj_query_base.count()
                n_start = int(request.args.get('start', 0))
                n_count = int(request.args.get('count', 0))

                if n_count > 0:
                    ids_query = (obj_session.query(CTableWorkOrder.no)
                                 .filter(*lst_where)
                                 .group_by(CTableWorkOrder.no)
                                 .order_by(CTableWorkOrder.date.desc())
                                 .offset(n_start).limit(n_count).all())

                else:
                    ids_query = (obj_session.query(CTableWorkOrder.no)
                                 .filter(*lst_where)
                                 .group_by(CTableWorkOrder.no)
                                 .order_by(CTableWorkOrder.date.desc())
                                 .all())
                lst_ids = [i[0] for i in ids_query]

                lst_obj_work = (
                    obj_session.query(CTableWorkOrder,
                                      CTableProductLine)
                    .outerjoin(CTableProductLine,
                               CTableProductLine.no == CTableWorkOrder.production_line_no)
                    .filter(CTableWorkOrder.no.in_(lst_ids))
                    .all()
                )

                for obj_work, obj_line in lst_obj_work:
                    dict_result = {"input": [], "output": [], "reuse": [], "labors": [], "machines": []}
                    str_work_no = obj_work.no if obj_work else ""
                    n_date = obj_work.date if obj_work else 0
                    str_productionLine_no = obj_line.no if obj_line else ''
                    str_productionLine_name = obj_line.name if obj_line else ''

                    # 取得分派投入物
                    lst_data1 = []
                    lst_input = (
                        obj_session.query(CTableProcessOrder, CTableBatchNoSerialNo, CTableBatchNumber)
                        .outerjoin(CTableBatchNoSerialNo,
                                   CTableProcessOrder.no == CTableBatchNoSerialNo.ref_order_no)
                        .outerjoin(CTableBatchNumber,
                                   CTableBatchNoSerialNo.batch_number == CTableBatchNumber.no)
                        .filter(CTableProcessOrder.work_order_no == str_work_no,
                                CTableProcessOrder.category == EProcessOrderCategory.RECEIVE)

                        .all()
                    )

                    for obj_data in lst_input:
                        dict_data = object_as_dict(obj_data[0])
                        dict_data2 = object_as_dict(obj_data[1]) if obj_data[1] else {}
                        dict_data3 = object_as_dict(obj_data[2]) if obj_data[2] else {}
                        dict_data = {
                            "workOrderDate": n_date,
                            "production_line_no": str_productionLine_no,
                            "productionLineName": str_productionLine_name,
                            "processDate": dict_data["date"],
                            "item_no": dict_data["item_no"],
                            "item_name": dict_data["item_name"],
                            "itemCategory": dict_data["itemCategory"],
                            "itemSubCategory": dict_data['itemSubCategory'],
                            "batch_number": dict_data2.get("batch_number", "") if dict_data2 else "",
                            "unit": dict_data2.get("unit", "") if dict_data2 else 0,
                            "count": dict_data2.get("expectedCount", 0) if dict_data2 else 0,
                            "itemType": dict_data3.get("itemType", 0) if dict_data3 else 0,
                            "validDate": dict_data3.get("validDate", 0) if dict_data3 else 0,
                        }
                        lst_data1.append(dict_data)
                    dict_result["input"] = lst_data1
                    # 取得產出物
                    lst_data2 = []
                    lst_output = (
                        obj_session.query(CTableProcessOrder, CTableBatchNumber)
                        .outerjoin(CTableBatchNumber,
                                   and_(
                                       CTableProcessOrder.no == CTableBatchNumber.ref_no,
                                       CTableProcessOrder.item_no == CTableBatchNumber.item_no
                                   ))
                        .filter(CTableProcessOrder.work_order_no == str_work_no,
                                CTableProcessOrder.category == EProcessOrderCategory.PRODUCT)
                        .all()
                    )
                    for obj_data in lst_output:
                        dict_data = object_as_dict(obj_data[0])
                        dict_data2 = object_as_dict(obj_data[1]) if obj_data[1] else {}

                        dict_data = {
                            "workOrderDate": n_date,
                            "production_line_no": str_productionLine_no,
                            "productionLineName": str_productionLine_name,
                            "processDate": dict_data["date"],
                            "item_no": dict_data["item_no"],
                            "item_name": dict_data["item_name"],
                            "itemCategory": dict_data["itemCategory"],
                            "itemSubCategory": dict_data['itemSubCategory'],
                            "itemType": dict_data2.get("itemType", 0) if dict_data2 else 0,
                            "batch_number": dict_data2.get("no", "") if dict_data2 else "",
                            "validDate": dict_data2.get("validDate", 0) if dict_data2 else 0,
                            "unit": dict_data["unit"],
                            "count": dict_data["expectedCount"]
                        }
                        lst_data2.append(dict_data)
                    dict_result["output"] = lst_data2

                    lst_data3 = []
                    lst_reuse = (
                        obj_session.query(CTableProcessOrder, CTableBatchNumber)
                        .outerjoin(CTableBatchNumber,
                                   and_(
                                       CTableProcessOrder.no == CTableBatchNumber.ref_no,
                                       CTableProcessOrder.item_no == CTableBatchNumber.item_no
                                   ))
                        .filter(CTableProcessOrder.work_order_no == str_work_no,
                                CTableProcessOrder.category.in_(
                                    [EProcessOrderCategory.REMAIN, EProcessOrderCategory.WASTE]))
                        .order_by(CTableProcessOrder.category)
                        .all()
                    )
                    for obj_data in lst_reuse:
                        dict_data = object_as_dict(obj_data[0])
                        dict_data2 = object_as_dict(obj_data[1]) if obj_data[1] else {}
                        dict_data = {
                            "workOrderDate": n_date,
                            "production_line_no": str_productionLine_no,
                            "productionLineName": str_productionLine_name,
                            "processDate": dict_data["date"],
                            "item_no": dict_data["item_no"],
                            "item_name": dict_data["item_name"],
                            "itemCategory": dict_data["itemCategory"],
                            "itemSubCategory": dict_data['itemSubCategory'],
                            "itemType": dict_data2.get("itemType", 0) if dict_data2 else 0,
                            "batch_number": dict_data2.get("no", "") if dict_data2 else "",
                            "validDate": dict_data2.get("validDate", 0) if dict_data2 else 0,
                            "unit": dict_data["unit"],
                            "count": dict_data["expectedCount"]
                        }
                        lst_data3.append(dict_data)

                    dict_result["reuse"] = lst_data3
                    # 取得分派人員
                    lst_data4 = []
                    lst_labor = (
                        obj_session.query(CTableProcessLabor)
                        .filter(CTableProcessLabor.work_order_no == str_work_no)
                        .all()
                    )
                    for obj_labor in lst_labor:
                        dict_data = {
                            "workOrderDate": n_date,
                            "processDate": obj_labor.date,
                            "production_line_no": obj_labor.production_line_no,
                            "productionLineName": obj_labor.production_line_data.name if obj_labor.production_line_data else "",
                            "station_no": obj_labor.station_no,
                            "stationName": obj_labor.station_data.name if obj_labor.station_data else "",
                            "stationStage": obj_labor.station_data.stage if obj_labor.station_data else 0,
                            "employee_no": obj_labor.employee_no,
                            "employeeName": obj_labor.employee_data.name if obj_labor.employee_data else "",
                            "employeeType": obj_labor.employee_data.type if obj_labor.employee_data else 0,
                            "employeeJobTitle": obj_labor.employee_data.jobTitle if obj_labor.employee_data else "",
                        }
                        lst_data4.append(dict_data)
                    dict_result["labors"] = lst_data4

                    print("")
                    # 取得分派產線
                    lst_data5 = []
                    lst_station = (
                        obj_session.query(CTableWorkOrder, CTableStation)
                        .select_from(CTableWorkOrder)  # 明確指定主表
                        .outerjoin(CTableStation,
                                   CTableStation.production_line_no == str_productionLine_no)
                        .filter(CTableWorkOrder.no == str_work_no)

                        .all()
                    )
                    for obj_station in lst_station:
                        dict_data1 = object_as_dict(obj_station[0]) if obj_station[0] else {}
                        dict_data2 = object_as_dict(obj_station[1]) if obj_station[1] else {}
                        if dict_data2:
                            lst_equ = (
                                obj_session.query(CTableEquipment)
                                .filter(CTableEquipment.station_no == dict_data2["no"])
                                .all()
                            )
                            for obj_equ in lst_equ:
                                dict_data = {
                                    "time": dict_data1["date"],
                                    "workOrderDate": n_date,
                                    "production_line_no": str_productionLine_no,
                                    "productionLineName": str_productionLine_name,
                                    "processDate": dict_data1["date"],
                                    "station_no": dict_data2["no"],
                                    "stationName": dict_data2["name"],
                                    "stationStage": dict_data2["stage"],
                                    "equipment_no": obj_equ.no if obj_equ else '',
                                    "equipmentName": obj_equ.name if obj_equ else ''
                                }
                                lst_data5.append(dict_data)
                    dict_result["machines"] = lst_data5
                    lst_result.append(dict_result)
                if lst_result:
                    dict_extra_data['total'] = n_total
                    dict_extra_data['count'] = len(lst_ids)  # 以派工單筆數為主
                    dict_extra_data['results'] = lst_result

        except Exception as error:
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'throw exception (error: %s)' % str(error)
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return n_status_code, n_code, str_message, dict_extra_data

    def __fill_query_params(self):
        lst_where = []
        if request.args.get('work_order_no'):
            lst_where.append(CTableWorkOrder.no == request.args.get('work_order_no'))
        return lst_where



class CProgress(CPrivilegeControl):
    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = { 'results': []}
        if not request.args.get("product_order_no") and not request.args.get("oneProcess"):
            n_status_code = 400
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'invalid parameter'
        else:
            try:
                lst_result = []
                with CDBMgr() as obj_dbmgr:
                    obj_session = obj_dbmgr.get_session()
                    n_oneProcess = int(request.args.get("oneProcess"))
                    str_product_order = request.args.get('product_order_no')

                    itemSubCategory = case(
                        (CTableAPSQuantity.itemCategory == EItemCategory.INPRODUCT, CTableInproduct.category),
                        else_=CTableProduct.category
                    ).label("itemSubcategory")
                    lst_obj_aps = (obj_session.query(CTableAPSQuantity.secProcess,
                                                    CTableAPSQuantity.item_no,
                                                    CTableAPSQuantity.item_name,
                                                    CTableAPSQuantity.itemCategory,
                                                    itemSubCategory,
                                                    CTableAPSQuantity.amount,
                                                    CTableAPSQuantity.minutes
                                     )
                                     .outerjoin(CTableInproduct, CTableInproduct.no == CTableAPSQuantity.item_no)
                                     .outerjoin(CTableProduct,
                                                  CTableProduct.no == CTableAPSQuantity.item_no)
                                     .filter(CTableAPSQuantity.product_order_no == str_product_order,
                                            CTableAPSQuantity.oneProcess == n_oneProcess)
                                    .order_by(CTableAPSQuantity.secProcess.asc())
                                    .all())

                    for n_secProcess, item_no, item_name, category, itemSubCategory, amount, minutes in lst_obj_aps:
                        obj_work_nos = (obj_session.query(CTableProductionData.work_order_no)
                                        .filter(CTableProductionData.product_order_no == str_product_order,
                                                CTableProductionData.item_no == item_no,
                                                CTableProductionData.oneProcess == n_oneProcess,
                                                CTableProductionData.secProcess == n_secProcess)
                                        .all())
                        lst_work_order_no = [row[0] for row in obj_work_nos]
                        if lst_work_order_no:
                            f_output_count = (obj_session.query(
                                                func.coalesce(func.round(func.sum(CTableProductionDataOutput.count), 2), 0.0)
                                            )
                                            .filter(CTableProductionDataOutput.work_order_no.in_(lst_work_order_no))
                                            .scalar())  # 使用 scalar 直接拿數字

                            '''
                            f_output_count = (
                                obj_session.query(
                                    func.coalesce(func.round(func.sum(CTableProductionDataOutput.count), 2), 0.0))
                                .join(CTableProductionData,
                                      CTableProductionData.work_order_no == CTableProductionDataOutput.work_order_no)
                                .filter(
                                    CTableProductionData.product_order_no == str_product_order,
                                    CTableProductionData.item_no == item_no,
                                    CTableProductionData.oneProcess == n_oneProcess,
                                    CTableProductionData.secProcess == n_secProcess
                                )
                                .scalar()
                            )
                            '''
                            f_hours, _ = CLaborHours().get(lst_work_order_no)
                            dict_data={
                                        "oneProcess": n_oneProcess,
                                        "secProcess": n_secProcess,
                                        "item_name": item_name,
                                        "itemCategory": category,
                                        "itemSubCategory": itemSubCategory,
                                        "bom":{ "count": 0,
                                               "amount": amount,
                                               "hours": round(minutes / 60, 2) if minutes else 0},
                                        "product": {"count": 0,
                                               "amount": f_output_count,
                                               "hours":f_hours}
                                       }
                            lst_result.append(dict_data)
                    dict_extra_data['results'] = lst_result
            except Exception as error:
                    n_code = EErrorCode.ERROR_OTHER_ERROR
                    str_message = 'throw exception (error: %s)' % str(error)
                    CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                                  % (self.__class__.__name__, str(error)))
        return n_status_code, n_code, str_message, dict_extra_data
class CProductData(CPrivilegeControl):

    TYPE_MATERIAL = 2
    TYPE_MACHINE = 4
    TYPE_LABOR = 8

    def __init__(self):
        self.__m_dict_bom = {}
        self.__m_dict_bom_weight = {}

    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}

        if not request.args.get("product_order_no") and not request.args.get("oneProcess"):
            n_status_code = 400
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'invalid parameter'
        else:
            try:
                # 從產製數據角度查詢
                with CDBMgr() as obj_dbmgr:
                    obj_session = obj_dbmgr.get_session()
                    n_oneProcess = int(request.args.get("oneProcess"))
                    str_product_order = request.args.get('product_order_no')
                    dict_extra_data = {"productLine": [], "productData":[], "records":{"input":[], "output": []}}
                    lst_all_workOrderNo = []
                    # 產線
                    lst_obj_production = (obj_session
                                          .query(
                                                func.group_concat(func.distinct(CTableProductionData.work_order_no)).label("workOrderNos"),
                                                CTableProductLine.name,
                                                func.count(CTableProductionData.production_line_no).label("lineCount")  # 計算筆數
                                                )
                                          .filter(CTableProductionData.product_order_no == str_product_order,
                                                  CTableProductionData.oneProcess == n_oneProcess)
                                          .outerjoin(CTableProductLine,
                                                     CTableProductLine.no == CTableProductionData.production_line_no)
                                          .group_by(CTableProductionData.production_line_no)
                                          .all())
                    for str_workOrderNos, name, lineCount in lst_obj_production:
                        dict_extra_data["productLine"].append({"name": name, "count": lineCount})
                        lst_nos = str_workOrderNos.split(",") if str_workOrderNos else []
                        lst_all_workOrderNo.extend(lst_nos)

                    if lst_all_workOrderNo:
                        # 投入物/產出物 出入產紀錄
                        lst_obj_work = (obj_session.query(CTableWorkOrder)
                                        .filter(CTableWorkOrder.no.in_(lst_all_workOrderNo))
                                        .all())
                        for obj_work in lst_obj_work:
                            dict_inoutRec = self.__fill_input_output_records(obj_session,
                                                                             obj_work.date,
                                                                             obj_work.production_data[
                                                                                 0].input_data,
                                                                             obj_work.production_data[
                                                                                 0].output_data)
                            if dict_inoutRec.get("input", []):
                                dict_extra_data["records"]["input"].extend(dict_inoutRec["input"])

                            if dict_inoutRec.get("output", []):
                                dict_extra_data["records"]["output"].extend(dict_inoutRec["output"])


                    lst_obj_process = (obj_session
                                       .query(
                                            CTableProductionData.oneProcess,
                                            CTableProductionData.secProcess,
                                            CTableProductionData.item_no,
                                            func.group_concat(func.distinct(CTableProductionData.work_order_no)).label("workOrderNos"),
                                        )
                                       .filter(CTableProductionData.product_order_no == str_product_order,
                                               CTableProductionData.oneProcess == n_oneProcess)
                                       .group_by(CTableProductionData.oneProcess, CTableProductionData.secProcess, CTableProductionData.item_no)
                                       .all())

                    # 製程/產製品分群
                    for n_oneProcess, n_secProcess, str_output_item_no, workOrderNos in lst_obj_process:
                        lst_work_order_no = workOrderNos.split(",") if workOrderNos else []
                        dict_data = {"oneProcess": n_oneProcess, "secProcess": n_secProcess, "input":[], "output":[], "labors":[]}

                        if lst_work_order_no:
                            lst_obj_input = (obj_session.query(
                                                        CTableProductionDataInput.item_no,
                                                        CTableProductionDataInput.item_name,
                                                        CTableProductionDataInput.category,
                                                        CTableProductionDataInput.itemSubCategory,
                                                        # 領料-退料
                                                        func.round(func.sum(case((CTableProductionDataInput.action == EInputAction.RECEIVE, CTableProductionDataInput.count),
                                                                else_=-CTableProductionDataInput.count)),2).label("input_count")
                                                    )
                                                  .filter(CTableProductionDataInput.work_order_no.in_(lst_work_order_no))
                                                  .group_by(
                                                        CTableProductionDataInput.item_no,
                                                        CTableProductionDataInput.item_name,
                                                        CTableProductionDataInput.category,
                                                        CTableProductionDataInput.itemSubCategory
                                                  )
                                                  .all())
                            for item_no, item_name, category, itemSubCategory, input_count in lst_obj_input:
                                # 查找投入物之預估/配方數量
                                obj_aps = (obj_session.query(
                                    CTableAPSQuantityItem.count,
                                )
                                .filter(CTableAPSQuantityItem.product_order_no == str_product_order,
                                        CTableAPSQuantityItem.output_item_no == str_output_item_no,
                                        CTableAPSQuantityItem.oneProcess == n_oneProcess,
                                        CTableAPSQuantityItem.secProcess == n_secProcess,
                                        CTableAPSQuantityItem.item_no == item_no)
                                        .first())

                                # 查找投入物之預估/配方損耗率
                                obj_aps_loss = (obj_session.query(
                                    CTableItemLoss.estValue,
                                )
                               .filter(CTableItemLoss.item_no == item_no)
                               .order_by(CTableItemLoss.date.desc())
                               .first())


                                # 使用 coalesce 確保沒資料時回傳 0.0 而不是 None
                                f_reuse_count = (
                                    obj_session.query(
                                        func.coalesce(
                                            func.round(func.sum(CTableProductionDataReuse.count), 2),
                                            0.0
                                        ).label("reuse_count")
                                    )
                                    .filter(
                                        CTableProductionDataReuse.work_order_no.in_(lst_work_order_no),
                                        CTableProductionDataReuse.category == EReuseCategory.WASTE,
                                        CTableProductionDataReuse.itemSubCategory == itemSubCategory
                                    )
                                    .scalar()  # 直接回傳數字 (如 123.45)，不再是 [(123.45,)]
                                )

                                # 補上配方 投入量/損耗量
                                dict_data["input"].append({ "item_name": item_name,
                                                            "itemCategory": category,
                                                            "itemSubCategory":itemSubCategory,
                                                            "count": input_count,
                                                            "bomCount": obj_aps.count if obj_aps else 0,
                                                            "loss": f_reuse_count,
                                                            "bomLoss": obj_aps_loss.estValue if obj_aps_loss else 0})

                            # 區分班長/員工 ?
                            lst_obj_labor = (obj_session.query(
                                CTableProductionDataLabor.action,
                                CTableProductionDataLabor.stationStage,
                                CTableProductionDataLabor.employee_level,
                                func.round(func.sum(CTableProductionDataLabor.hours), 2).label("labor_hours"),
                                func.count(CTableProductionDataLabor.employee_no).label("labor_count")
                            )
                             .filter(CTableProductionDataLabor.work_order_no.in_(lst_work_order_no))
                             .group_by(
                                CTableProductionDataLabor.action,
                                CTableProductionDataLabor.stationStage,
                                CTableProductionDataLabor.employee_level
                            )
                            .all())

                            labor_groups = defaultdict(list)
                            for action, stationStage, employee_level, labor_hours, labor_count in lst_obj_labor:
                                str_key = (employee_level)
                                labor_groups[str_key].append({"action": action,
                                                              "stationStage": stationStage,
                                                              "employeeLevel": employee_level,
                                                              "count": labor_count,
                                                              "hours": labor_hours
                                                              })

                            dict_temp = {"workPreHours": 0, "workPostHours": 0, "workPreCount": 0,
                                         "workPostCount": 0,
                                         "restPreHours": 0, "restPostHours": 0, "restPreCount": 0,
                                         "restPostCount": 0,
                                         "cleanPreHours": 0, "cleanPostHours": 0, "cleanPreCount": 0,
                                         "cleanPostCount": 0,
                                         "employeeLevel": 0}

                            for tuple_key, lst_items in labor_groups.items():
                                dict_temp["employeeLevel"] = tuple_key
                                for dict_tmp in lst_items:
                                    # action 1:工作 2:休息 3:清潔
                                    # stationStage 1:前段 2:後段
                                    n_action = dict_tmp["action"]
                                    n_stationStage = dict_tmp["stationStage"]
                                    if n_action == 1:
                                        if n_stationStage == 1:
                                            dict_temp["workPreHours"] = dict_tmp["hours"]
                                            dict_temp["workPreCount"] = dict_tmp["count"]
                                        elif n_stationStage == 2:
                                            dict_temp["workPostHours"] = dict_tmp["hours"]
                                            dict_temp["workPostCount"] = dict_tmp["count"]
                                    elif n_action == 2:
                                        if n_stationStage == 1:
                                            dict_temp["restPreHours"] = dict_tmp["hours"]
                                            dict_temp["restPreCount"] = dict_tmp["count"]
                                        elif n_stationStage == 2:
                                            dict_temp["restPostHours"] = dict_tmp["hours"]
                                            dict_temp["restPostCount"] = dict_tmp["count"]
                                    elif n_action == 3:
                                        if n_stationStage == 1:
                                            dict_temp["cleanPreHours"] = dict_tmp["hours"]
                                            dict_temp["cleanPreCount"] = dict_tmp["count"]
                                        elif n_stationStage == 2:
                                            dict_temp["cleanPostHours"] = dict_tmp["hours"]
                                            dict_temp["cleanPostCount"] = dict_tmp["count"]

                            dict_data["labors"].append(dict_temp)
                            # 產出時
                            n_total_product_hours = self.__cal_totalProductHours(dict_data["labors"])

                            # 產出物 製程
                            lst_obj_output = (obj_session.query(
                                CTableProductionDataOutput.item_no,
                                CTableProductionDataOutput.item_name,
                                CTableProductionDataOutput.category,
                                CTableProductionDataOutput.itemSubCategory,
                                func.round(func.sum(CTableProductionDataOutput.count), 2).label("output_count")
                            )
                             .filter(CTableProductionDataOutput.work_order_no.in_(lst_work_order_no))
                             .group_by(
                                CTableProductionDataOutput.item_no,
                                CTableProductionDataOutput.item_name,
                                CTableProductionDataOutput.category,
                                CTableProductionDataOutput.itemSubCategory,
                            )
                            .all())

                            obj_capacity = (obj_session.query(
                                CTableProcessCapacity.hourlyOutput
                            )
                            .filter(CTableProcessCapacity.oneProcess == n_oneProcess,
                                    CTableProcessCapacity.secProcess == n_secProcess)
                            .order_by(
                                CTableProcessCapacity.date.desc()
                            )
                            .first())

                            for item_no, item_name, category, itemSubCategory, output_count in lst_obj_output:
                                # 查找產出物之預估/配方數量
                                obj_aps_output = (obj_session.query(
                                    CTableAPSQuantity.amount,
                                )
                               .filter(CTableAPSQuantity.product_order_no == str_product_order,
                                       CTableAPSQuantity.item_no == item_no,
                                       CTableAPSQuantity.oneProcess == n_oneProcess,
                                       CTableAPSQuantity.secProcess == n_secProcess)
                               .first())

                                f_bom_hourlyCount = obj_capacity.hourlyOutput if obj_capacity else 0
                                n_bom_product_hours = round(output_count / obj_capacity.hourlyOutput, 2) if obj_capacity and output_count else 0
                                dict_data["output"].append({
                                                              "item_name": item_name,
                                                              "itemCategory": EItemCategory.INPRODUCT if category == EOutputCategory.INPRODUCT else EItemCategory.PRODUCT ,
                                                              "itemSubCategory": itemSubCategory,
                                                              "bom":{
                                                                  "count": obj_aps_output.amount if obj_aps_output else 0,
                                                                  "price": 0,
                                                                  "hours": n_bom_product_hours,
                                                                  "hourlyCount": f_bom_hourlyCount,
                                                                  "rawMaterialCost": 0,
                                                                  "materialCost": 0,
                                                                  "laborCost": 0,
                                                              },
                                                              "product": {
                                                                "count": output_count,
                                                                "price": 0,
                                                                "hours": n_total_product_hours,
                                                                "hourlyCount": round((output_count/n_total_product_hours), 2)  if output_count and n_total_product_hours else 0,
                                                                "rawMaterialCost": 0,
                                                                "materialCost": 0,
                                                                "laborCost": 0,
                                                              }})



                            dict_extra_data["productData"].append(dict_data)
            except Exception as error:
                n_code = EErrorCode.ERROR_OTHER_ERROR
                str_message = 'throw exception (error: %s)' % str(error)
                CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                              % (self.__class__.__name__, str(error)))
        return n_status_code, n_code, str_message, dict_extra_data

    def __cal_totalProductHours(self, lst_labors) -> int:
        # 計算產製總時數
        def get_metrics(pre_h, post_h, pre_c, post_c):
            # 使用 .get() 確保 key 不存在或為 None 時能安全處理
            hours = max(pre_h or 0, post_h or 0)
            count = max(pre_c or 0, post_c or 0)
            return {"hours": hours, "count": count, "total": hours * count}

        n_total_hours = 0
        for dict_labor in lst_labors:
            dict_work = get_metrics(dict_labor.get("workPreHours"), dict_labor.get("workPostHours"),
                               dict_labor.get("workPreCount"), dict_labor.get("workPostCount"))
            dict_rest = get_metrics(dict_labor.get("restPreHours"), dict_labor.get("restPostHours"),
                               dict_labor.get("restPreCount"), dict_labor.get("restPostCount"))
            dict_clean = get_metrics(dict_labor.get("cleanPreHours"), dict_labor.get("cleanPostHours"),
                                dict_labor.get("cleanPreCount"), dict_labor.get("cleanPostCount"))

            # 生產總時數 = 工作總時數 - 休息總時數 - 清潔總時數
            n_total_hours += dict_work["hours"] - dict_rest["hours"] - dict_clean["hours"]
        return n_total_hours


    def __fill_input_output(self, obj_session, n_date, list_data, f_isInput):
        lst_result = []

        lst_batchNos = list({obj_item.batch_number for obj_item in list_data})
        dict_record = self.__get_inventoryRec(obj_session, n_date, lst_batchNos, True if f_isInput else False)
        dict_batchNos = self.__get_batchNos_info(obj_session, lst_batchNos)

        for obj_item in list_data:
            dict_data = object_as_dict(obj_item)
            if f_isInput:
                if dict_data["action"] == EInputAction.RETURN:
                    continue
                n_category = dict_data["category"]
                n_subCategory = dict_data["itemSubCategory"]
            else:
                n_category, n_subCategory = get_output_item_info(dict_data["item_no"])

            lst_warehouse = dict_record.get(dict_data["batch_number"], [])
            lst_result.append({
                "workOrderDate": n_date,
                "item_no": dict_data["item_no"],
                "item_name": dict_data["item_name"],
                "itemCategory": n_category, # 原料/物料/在製品/在製品/製成品
                "itemSubCategory": n_subCategory, # 在製品/製成品的子類別
                "batch_number": dict_data["batch_number"],
                "itemType": dict_batchNos[dict_data["batch_number"]].get("itemType", 0) if dict_data[
                                                                                               "batch_number"] in dict_batchNos else 0,
                "validDate": dict_batchNos[dict_data["batch_number"]].get("validDate", 0) if dict_data[
                                                                                                 "batch_number"] in dict_batchNos else 0,
                "warehouses": lst_warehouse
            })

        return lst_result

    def __fill_input_output_records(self, obj_session, n_date, lst_input, lst_output):
        dict_data = {"input": [], "output":[]}
        # 取得出入產紀錄
        # n_type :
        # 1: input         # 2: output
        lst_tmp1 = self.__fill_input_output(obj_session, n_date, lst_input, True)
        lst_tmp2 = self.__fill_input_output(obj_session, n_date, lst_output, False)

        dict_data["input"] = sorted(lst_tmp1, key=lambda x: (x['workOrderDate'], x['itemType']))
        dict_data["output"] = sorted(lst_tmp2, key=lambda x: (x['workOrderDate'], x['itemType']))
        return dict_data

    def __get_inventoryRec(self, obj_session, n_date, lst_nos, f_out):
        dict_result = {}
        lst_where = []
        # 需修改filter改查找batchNumber+CTableInventoryRec.ref_no
        n_category = EInventoryCategory.OUT if f_out else EInventoryCategory.IN
        n_source = EInventorySrc.PURCHASE_RECEIVE if f_out else EInventorySrc.PRODUCT
        n_start = n_date
        n_end = util_convert_timestamp_to_date(n_start, 1) - 1

        lst_where.append(CTableInventoryRec.category == n_category)
        lst_where.append(CTableInventoryRec.source == n_source)
        if n_start and n_end:
            lst_where.append(CTableInventoryRec.date.between(n_start, n_end))
        if lst_nos:
            lst_where.append(CTableInventoryRec.batchNumber.in_(lst_nos))
            lst_result = (obj_session.query(
                CTableInventoryRec
            )
            .filter(*lst_where)
            .all()
            )
            for obj_result in lst_result:
                if obj_result.batchNumber not in dict_result:
                    dict_result[obj_result.batchNumber] = []
                dict_result[obj_result.batchNumber].append({"date": obj_result.date,
                                                      "warehouse_no": obj_result.warehouse_no,
                                                      "warehouse_displayName": obj_result.warehouse_displayName,
                                                      "unit": obj_result.unit,
                                                      "count": obj_result.count,
                                                      "packCount": 0
                                                      })

        return dict_result

    def __get_batchNos_info(self, obj_session, lst_nos):
        dict_result = {}
        if lst_nos:
            lst_result = (obj_session.query(
                CTableBatchNumber.no,
                CTableBatchNumber.validDate,
                CTableBatchNumber.itemType
            )
            .filter(CTableBatchNumber.no.in_(lst_nos))
            .all()
            )
            for obj_result in lst_result:
                dict_result[obj_result.no] = {"itemType": obj_result.itemType,
                                              "validDate": obj_result.validDate}

        return dict_result

class CRealTime(CPrivilegeControl):
    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'results': []}

        try:
            lst_result = []
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                lst_where = self.__fill_query_params()
                lst_detail = (
                    obj_session.query(CTableWorkOrder)
                    .filter(*lst_where)
                    .order_by(CTableWorkOrder.secProcess.desc())
                    .all()
                )
                for n_index, obj_detail in enumerate(lst_detail):
                    n_category, _ = get_output_item_info(obj_detail.output_item_no)
                    dict_data = {
                        'no': obj_detail.no,
                        'date': obj_detail.date,
                        'product_order': obj_detail.product_order_no,
                        'customer_displayName': obj_detail.customer_displayName,
                        'product_name': obj_detail.product_name,
                        'output_item_no': obj_detail.output_item_no,
                        'output_item_name': obj_detail.output_item_name,
                        'output_item_category': n_category,
                        'oneProcess': obj_detail.oneProcess,
                        'secProcess': obj_detail.secProcess,
                        'product_line': "",
                        'laborCount': obj_detail.laborCount,
                        'hours': float(obj_detail.processTime/60.0) if obj_detail.processTime else 0,
                        'unit': obj_detail.processUnit,
                        'count': obj_detail.processCount,
                        'progress': 0
                    }

                    obj_line = obj_session.query(CTableProductLine).filter(
                        CTableProductLine.no == obj_detail.production_line_no).first()
                    if obj_line:
                        dict_data["product_line"] = obj_line.location
                    f_total = 0
                    if len(obj_detail.production_data):
                        for obj_data in obj_detail.production_data[0].output_data:
                            f_total += obj_data.count
                    if obj_detail.processCount:
                        dict_data["progress"] = 100 if 100 < int(
                            float(f_total / obj_detail.processCount) * 100) else int(
                            float(f_total / obj_detail.processCount) * 100)

                    lst_result.append(dict_data)
            dict_extra_data["results"] = lst_result
        except Exception as error:
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'throw exception (error: %s)' % str(error)
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return n_status_code, n_code, str_message, dict_extra_data

    def __fill_query_params(self):
        lst_where = []

        if request.args.get('oneProcess'):
            lst_where.append(CTableWorkOrder.oneProcess == int(request.args.get('oneProcess')))

        if request.args.get('start_time') and request.args.get('end_time'):
            # get the range of timestamp
            n_start_day = util_convert_timestamp_to_date(int(request.args.get('start_time')))
            if int(request.args.get('start_time')) == int(request.args.get('end_time')):
                n_end_day = util_convert_timestamp_to_date(n_start_day, 1) - 1
            else:
                n_end_day = util_convert_timestamp_to_date(int(request.args.get('end_time')), 1) - 1
            lst_where.append(CTableWorkOrder.date.between(n_start_day, n_end_day))
        return lst_where

