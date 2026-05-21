# coding=utf8
import pytz
import json
import string
import validictory
from copy import deepcopy
import math
from flask import request
from package.util.util import *
from .common import *
from package.common.common import *
from package.log.log import CLogger
from package.dbwrapper.table import *
from package.dbwrapper.dbmgr import CDBMgr
from package.util.util import *
from .util import *
from sqlalchemy import delete, func, select, case
from package.bom.bom import *
from collections import defaultdict
from package.statistic.workOrderStatistic import COrdersProcessMonth


def util_process_to_str(n_oneProcess, n_secProcess):
    str_name = ''
    if n_oneProcess == 1:
        if n_secProcess == 1:
            str_name = '前備-混拌料'
        elif n_secProcess == 2:
            str_name = '前備-塞灌料'
        elif n_secProcess == 3:
            str_name = '前備-烘烤料'
    elif n_oneProcess == 2:
        str_name = '加工'
    elif n_oneProcess == 3:
        str_name = '包裝'
    return str_name


def util_minutes_to_hhmm(n_minutes):
    hours = n_minutes // 60
    remaining_minutes = n_minutes % 60
    return f"{hours:02}:{remaining_minutes:02}"


def util_float_to_str2(f_value):
    return f"{f_value:.2f}"

def util_float_to_str2_comma(f_value):
    return f"{f_value:,.2f}"
def util_int_comma(n_value):
    return f"{n_value:,}"

class CPrivilegeControl(object):
    def is_allowed_for_get(self, lst_privileges):
        return any(privilege['category'] == EPrivilegeCategory.PURCHASE and privilege['action'] in (EPrivilegeAction.VIEW, EPrivilegeAction.REPORT)
                   for privilege in lst_privileges)

    def is_allowed_for_post(self, lst_privileges):
        return any(privilege['category'] == EPrivilegeCategory.PURCHASE and privilege['action'] == EPrivilegeAction.CREATION
                   for privilege in lst_privileges)

    def is_allowed_for_put(self, lst_privileges):
        return any(privilege['category'] == EPrivilegeCategory.PURCHASE and privilege['action'] == EPrivilegeAction.MODIFICATION
                   for privilege in lst_privileges)

    def is_allowed_for_delete(self, lst_privileges):
        return any(privilege['category'] == EPrivilegeCategory.PURCHASE and privilege['action'] == EPrivilegeAction.CANCELLATION
                   for privilege in lst_privileges)


class CWorkOrder(CPrivilegeControl):

    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'total': 0, 'count': 0, 'results': []}

        try:
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                lst_where = self.__fill_query_params()
                n_total = (
                    obj_session.query(CTableWorkOrder)
                    .filter(*lst_where)
                    .order_by(CTableWorkOrder.date.desc())
                    .count()
                )
                lst_result = self.__retrieve(obj_session, lst_where)
                if lst_result:
                    dict_extra_data['total'] = n_total
                    dict_extra_data['count'] = len(lst_result)
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
        if request.args.get('start_time') and request.args.get('end_time'):
            # get the range of timestamp
            n_start_day = util_convert_timestamp_to_date(int(request.args.get('start_time')))
            if int(request.args.get('start_time')) == int(request.args.get('end_time')):
                n_end_day = util_convert_timestamp_to_date(n_start_day, 1) - 1
            else:
                n_end_day = util_convert_timestamp_to_date(int(request.args.get('end_time')), 1) - 1
            lst_where.append(CTableWorkOrder.date.between(n_start_day, n_end_day))

        if request.args.get('aps_no'):
            lst_where.append(CTableWorkOrder.aps_no == request.args.get('aps_no'))

        if request.args.get('work_order_no'):
            lst_where.append(CTableWorkOrder.no == request.args.get('work_order_no'))

        if request.args.get('oneProcess'):
            lst_where.append(CTableWorkOrder.oneProcess == int(request.args.get('oneProcess')))

        return lst_where

    def __retrieve(self, obj_session, lst_where):
        lst_data = []

        n_start = 0
        n_count = 0
        if request.args.get('start') and request.args.get('count'):
            n_start = int(request.args.get('start'))
            n_count = int(request.args.get('count'))

        if n_count:
            ids_query = (obj_session.query(
                         CTableWorkOrder.no)
                         .filter(*lst_where)
                         .order_by(CTableWorkOrder.date.desc())
                         .offset(n_start)
                         .limit(n_count)
                         )

            ids = [id[0] for id in ids_query.all()]
            lst_detail = (
                obj_session.query(CTableWorkOrder)
                .filter(CTableWorkOrder.no.in_(ids))
                .order_by(CTableWorkOrder.date.desc())
                .all()
            )
            #print("")
        else:
            lst_detail = (
                obj_session.query(CTableWorkOrder)
                .filter(*lst_where)
                .order_by(CTableWorkOrder.date.desc())
                .all()
            )

        for n_index, obj_work in enumerate(lst_detail):
            # 取得產製數據
            obj_output = obj_session.query(
                func.round(func.sum(CTableProductionDataOutput.count), 2)
            ).filter(CTableProductionDataOutput.work_order_no == obj_work.no).first()

            n_laborCount, f_hours = self.__get_productiondata_hours(obj_session, obj_work.no)
            n_category, n_subCategory = get_output_item_info(obj_work.output_item_no)

            # 取得product規格
            dict_tmp = {
                'no': obj_work.no,
                'date': obj_work.date,
                'product_order': obj_work.product_order_no,
                'customer_no': obj_work.customer_no,
                'customer_displayName': obj_work.customer_displayName,
                'product_no': obj_work.product_no,
                'product_name': obj_work.product_name,
                'product_package':  self.__get_product_package(obj_session, obj_work.product_no),
                'output_item_no': obj_work.output_item_no,
                'output_item_name': obj_work.output_item_name,
                'output_item_category': n_category,
                'output_item_subCategory': n_subCategory,
                'oneProcess': obj_work.oneProcess,
                'secProcess': obj_work.secProcess,
                'product_line': self.__retrieve_productline(obj_session, obj_work.production_line_no),

                'laborCount': obj_work.laborCount,
                'processTime': obj_work.processTime,
                'hours': float(obj_work.processTime / 60.0) if obj_work.processTime else 0,

                'productiondata_output': obj_output[0] if obj_output else 0,
                'productiondata_laborCount': n_laborCount,
                'productiondata_hours': f_hours,

                'unit': obj_work.processUnit,
                'count': obj_work.processCount,
            }
            lst_data.append(dict_tmp)
        return lst_data

    def __get_productiondata_hours(self, obj_session, str_work_order_no ):
        from sqlalchemy import func, case
        n_laborCount = 0
        f_hours = 0
        lst_labor = (
            obj_session.query(
                CTableProductionDataLabor.stationStage,
                func.count().label("count"),
                func.max(func.count()).over().label("max_count")
            )
            .filter(
                CTableProductionDataLabor.work_order_no == str_work_order_no,
                CTableProductionDataLabor.action == ELaborType.WORK
            )
            .group_by(CTableProductionDataLabor.stationStage)
            .all()
        )

        if lst_labor:
            n_laborCount = lst_labor[0].max_count  # max_count 每筆都一樣，取一筆即可



        lst_hours = (
            obj_session.query(
                CTableProductionDataLabor.stationStage,
                func.sum(
                    case(
                        (CTableProductionDataLabor.action == ELaborType.WORK, CTableProductionDataLabor.hours),
                        else_=0
                    )
                ).label("work_hours"),
                func.sum(
                    case(
                        (CTableProductionDataLabor.action == ELaborType.CLEAN, CTableProductionDataLabor.hours),
                        else_=0
                    )
                ).label("clean_hours"),
                func.sum(
                    case(
                        (CTableProductionDataLabor.action == ELaborType.REST, CTableProductionDataLabor.hours),
                        else_=0
                    )
                ).label("rest_hours"),
                # 淨時數 = 工作 - 休息
                (
                        func.sum(
                            case((CTableProductionDataLabor.action == ELaborType.WORK, CTableProductionDataLabor.hours),
                                 else_=0)
                        )

                        - func.sum(
                    case((CTableProductionDataLabor.action == ELaborType.REST, CTableProductionDataLabor.hours),
                         else_=0)
                )
                ).label("net_hours"),
                # 取全部 subAction 中的 net_hours 最大值
                func.max(
                    func.sum(
                        case((CTableProductionDataLabor.action == ELaborType.WORK, CTableProductionDataLabor.hours),
                             else_=0)
                    )
                    - func.sum(
                        case((CTableProductionDataLabor.action == ELaborType.REST, CTableProductionDataLabor.hours),
                             else_=0)
                    )
                ).over().label("max_net_hours"),
            )
            .filter(CTableProductionDataLabor.work_order_no == str_work_order_no)
            .group_by(CTableProductionDataLabor.stationStage) #前段/後段
            .all()
        )
        if lst_hours:
            f_hours = round(lst_hours[0].max_net_hours/n_laborCount, 2) if n_laborCount else 0# max_net_hours 每筆都一樣，取一筆即可
        return n_laborCount, f_hours

    def __retrieve_productline(self, obj_session, str_id):
        str_name = ''
        if str_id:
            lst_result = (obj_session.query(
                CTableProductLine.name
            )
            .filter(CTableProductLine.no == str_id)
            .all()
             )
            if lst_result:
                str_name = lst_result[0].name
        return str_name

    def __get_product_package(self, obj_session, str_no):
        n_package = 0
        if str_no:
            obj_product = obj_session.query(CTableProduct).filter(
                CTableProduct.no == str_no
            ).first()
            n_package = obj_product.category if obj_product else 0
        return n_package


class CStatistic(CPrivilegeControl):

    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {
                           'count': 0,
                           'results': []
                           }

        try:
            f_isCommit = False
            if request.args.get('start_time') and request.args.get('end_time'):
                # get the range of timestamp
                n_start = int(request.args.get('start_time'))
                n_end = int(request.args.get('end_time'))

                if request.args.get('commit'):
                    f_isCommit = True
                lst_result = COrdersProcessMonth(str_timezone).calculate(n_start, n_end, f_isCommit)
                dict_extra_data['count'] = len(lst_result)
                dict_extra_data['results'] = lst_result
        except Exception as error:
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'throw exception (error: %s)' % str(error)
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return n_status_code, n_code, str_message, dict_extra_data





# 產製製令-實際製造數據
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
        dict_extra_data = {'total': 0, 'count': 0, 'results': []}

        try:
            lst_result = []
            n_type = int(request.args.get('type')) if request.args.get('type') else 0
            if n_type:
                with CDBMgr() as obj_dbmgr:
                    obj_session = obj_dbmgr.get_session()
                    lst_where = self.__fill_query_params()

                    # 建立基礎查詢物件
                    obj_base = (
                        obj_session.query(CTableWorkOrder, CTableProductLine)
                        .outerjoin(CTableProductLine, CTableProductLine.no == CTableWorkOrder.production_line_no)
                        .filter(*lst_where)
                    )
                    # 計算總數
                    n_total = obj_base.count()
                    n_start = int(request.args.get('start', 0))
                    n_count = int(request.args.get('count', 0))

                    # 組合最終查詢
                    obj_query = obj_base.order_by(CTableWorkOrder.date.desc())

                    if n_count > 0:
                        obj_query = obj_query.offset(n_start).limit(n_count)

                    # 5. 執行查詢
                    lst_obj_result = obj_query.all()
                    for obj_work, obj_line in lst_obj_result:
                        dict_data = {
                            'no': obj_work.no,
                            'date': obj_work.date,
                            "production_line_no": obj_line.no if obj_line else "",
                            "productionLineName": obj_line.name if obj_line else "",
                            "output_item_no": obj_work.output_item_no,
                            "output_item_name": obj_work.output_item_name,
                            "oneProcess": obj_work.oneProcess,
                            "secProcess": obj_work.secProcess,
                            'input': [],
                            'output': [],
                            'reuse': [],
                            'labor': [],
                            'labors': {},
                            'machine': [],
                            'machineRec': []
                        }

                        if n_type & self.TYPE_MATERIAL:
                            dict_data["input"], dict_data["output"], dict_data["reuse"], dict_data["inoutRec"], \
                            dict_data["inputLoss"] = self.__get_input_output(obj_session, obj_work)

                        if n_type & self.TYPE_LABOR:
                            dict_data["labor"], dict_data["labors"] = self.__get_labor(obj_session, obj_work)
                        if n_type & self.TYPE_MACHINE:
                            dict_data['machine'], dict_data['machineRec'] = self.__get_machine(obj_session, obj_work)

                        lst_result.append(dict_data)

            if lst_result:
                dict_extra_data['total'] = n_total
                dict_extra_data['count'] = len(lst_result)
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

        if request.args.get('start_time') and request.args.get('end_time'):
            # get the range of timestamp
            n_start_day = util_convert_timestamp_to_date(int(request.args.get('start_time')))
            if int(request.args.get('start_time')) == int(request.args.get('end_time')):
                n_end_day = util_convert_timestamp_to_date(n_start_day, 1) - 1
            else:
                n_end_day = util_convert_timestamp_to_date(int(request.args.get('end_time')), 1) - 1
            lst_where.append(CTableWorkOrder.date.between(n_start_day, n_end_day))
        return lst_where

    def __get_details(self, obj_session, obj_work, dict_data):
        if len(obj_work.production_data):
            # need to revise code
            # 機具
            # 補上完整程式
            dict_data["machine"], dict_data["machineRec"] =  self.__get_machine(obj_session, obj_work)

            # 員工
            dict_data["labor"], dict_data["labors"] = self.__get_labor(obj_session, obj_work)

            # 投入物
            dict_data["input"] = self.__grouped_input( obj_session, obj_work.production_data[0].input_data, 1)

            # 產出物
            n_version = 1
            lst_bom = CCBOMTree().retrieve(obj_work.product_no, n_version)
            dict_data["output"] = self.__grouped_output_reuse(obj_session, obj_work.production_data[0].output_data, 1, True, lst_bom)
            # 餘廢料
            dict_data["reuse"] = self.__grouped_output_reuse(obj_session, obj_work.production_data[0].reuse_data, 1, False)

            # 投入物/產出物/餘廢料 出入產紀錄
            dict_data["inoutRec"] = self.__fill_input_output_reuse_records(obj_session, obj_work.production_data[0].input_data,
                                                                           obj_work.production_data[0].output_data, obj_work.production_data[0].reuse_data)
    def __get_labor(self, obj_session, obj_work):
        lst_result = []
        dict_labors = {}
        if len(obj_work.production_data):
            # 補上站號
            for obj_data in obj_work.production_data:
                for obj_labor in obj_data.labor_data:
                    obj_result = (
                        obj_session.query(
                            CTableStation.name.label('stationName'),
                            CTableProductLine.no.label('productionLineNo'),
                            CTableProductLine.name.label('productionLineName'),
                            CTableProductLine
                        )
                        .outerjoin(CTableProductLine,
                                   CTableProductLine.no == CTableStation.production_line_no)
                        .filter(CTableStation.no == obj_labor.station_no)
                        .first()
                    )

                    obj_employee = (
                        obj_session.query(
                            CTableEmployee
                        )
                        .filter(CTableEmployee.no == obj_labor.employee_no)
                        .first()
                    )
                    dict_temp = object_as_dict(obj_labor)
                    dict_temp["productionLineNo"] = obj_result.productionLineNo if obj_result else ''
                    dict_temp["productionLineName"] = obj_result.productionLineName if obj_result else ''
                    dict_temp["stationName"] = obj_result.stationName if obj_result else ''
                    dict_temp["employee_name"] = obj_employee.name if obj_employee else ''
                    dict_temp["employee_type"] = obj_employee.type if obj_employee else 0
                    dict_temp["employee_level"] = obj_employee.level if obj_employee else 0
                    dict_temp["employee_jobTitle"] = obj_employee.jobTitle if obj_employee else ''

                    lst_result.append(dict_temp)

            dict_labors = self.__retrieve_labor_time(obj_session, obj_work.date, lst_result)
        return lst_result, dict_labors

    def __get_input_output(self, obj_session, obj_work):
        lst_input = []
        lst_output = []
        lst_reuse = []
        lst_inoutRec = []
        dict_inputLoss = {}

        if len(obj_work.production_data):
            # 投入物
            lst_input = self.__grouped_input(obj_session, obj_work.production_data[0].input_data, 1)
            # 產出物 Enhance performance
            if obj_work.product_no in self.__m_dict_bom:
                lst_bom = self.__m_dict_bom[obj_work.product_no]
            else:
                n_version = 1
                lst_bom = CCBOMTree().retrieve(obj_work.product_no, n_version)
                self.__m_dict_bom[obj_work.product_no] = deepcopy(lst_bom)
            lst_output = self.__grouped_output_reuse(obj_session, obj_work.production_data[0].output_data, 1, True,
                                                              lst_bom)
            # 餘廢料
            lst_reuse = self.__grouped_output_reuse(obj_session, obj_work.production_data[0].reuse_data, 1, False)

            # 投入物/產出物/餘廢料 出入產紀錄
            lst_inoutRec = self.__fill_input_output_reuse_records(obj_session,
                                                                           obj_work.production_data[0].input_data,
                                                                           obj_work.production_data[0].output_data,
                                                                           obj_work.production_data[0].reuse_data)

            dict_inputLoss = self.__fill_input_loss(lst_input, lst_reuse)
        return lst_input, lst_output, lst_reuse, lst_inoutRec, dict_inputLoss

    def __get_machine(self, obj_session, obj_work):
        lst_machine = []
        lst_machineRec = []
        if len(obj_work.production_data):
            # need to revise code
            # 機具
            # 補上完整程式
            lst_machine = self.__fill_machine(obj_session, obj_work.production_data[0].machine_data)
            lst_machineRec = self.__fill_machine_rec(obj_session, obj_work.production_data[0].machine_data)
        return lst_machine, lst_machineRec

    def __fill_machine_rec(self, obj_session, lst_data):
        lst_result = []
        if len(lst_data) > 0:
            for obj_data in lst_data:
                obj_result = (
                    obj_session.query(
                        CTableStation.no.label('stationNo'),
                        CTableStation.name.label('stationName'),
                        CTableStation.stage.label('stationStage'),
                        CTableProductLine.no.label('productionLineNo'),
                        CTableProductLine.name.label('productionLineName')
                    )
                    .join(CTableEquipment, CTableEquipment.station_no == CTableStation.no)
                    .outerjoin(CTableProductLine,
                               CTableProductLine.no == CTableStation.production_line_no)
                    .filter(CTableEquipment.no == obj_data.equipment_no)
                    .first()
                )

                dict_item = {
                    "time": obj_data.time,
                    "action": obj_data.action,
                    "equipment_no": obj_data.equipment_no,
                    "equipmentName": obj_data.equipment_name,
                    "productionLineNo": obj_result.productionLineNo if obj_result else '',
                    "productionLineName": obj_result.productionLineName if obj_result else '',
                    "stationNo": obj_result.stationNo if obj_result else '',
                    "stationName": obj_result.stationName if obj_result else '',
                    "stationStage": obj_result.stationStage if obj_result else 0,
                    "speed": obj_data.speed,
                    "temperature": obj_data.temperature
                }

                lst_result.append(dict_item)
        return lst_result

    def __fill_machine(self, obj_session, lst_data):
        lst_result = []
        if len(lst_data) > 0:
            lst_tmp  =[]
            for obj_data in lst_data:
                dict_temp = object_as_dict(obj_data)
                lst_tmp.append(dict_temp)

            # Step 1: 分群
            grouped = defaultdict(list)
            for item in lst_tmp:
                grouped[item['equipment_no']].append(item)

            # Step 2: 計算每群最大值與 time 差距，並寫入每筆資料
            lst_result = []
            for str_equipment_no, items in grouped.items():
                obj_result = (
                    obj_session.query(
                        CTableStation.no.label('stationNo'),
                        CTableStation.name.label('stationName'),
                        CTableStation.stage.label('stationStage'),
                        CTableProductLine.no.label('productionLineNo'),
                        CTableProductLine.name.label('productionLineName'),
                        CTableProductLine
                    )
                    .join(CTableEquipment, CTableEquipment.station_no == CTableStation.no)
                    .outerjoin(CTableProductLine,
                               CTableProductLine.no == CTableStation.production_line_no)
                    .filter(CTableEquipment.no == str_equipment_no)
                    .first()
                )
                dict_item = {"equipment_no": str_equipment_no,
                             "equipment_name": items[0]["equipment_name"] if items else "",
                             "productionLineNo": obj_result.productionLineNo if obj_result else '',
                             "productionLineName": obj_result.productionLineName if obj_result else '',
                             "stationNo": obj_result.stationNo if obj_result else '',
                             "stationName": obj_result.stationName if obj_result else '',
                             "stationStage": obj_result.stationStage if obj_result else 0,
                             "workHours":0,
                             "workSpeed": 0,
                             "workTemperature": 0,
                             "idleHours": 0,
                             "idleSpeed": 0,
                             "idleTemperature": 0,
                             }
                max_temp = max(i['temperature'] for i in items)
                max_speed = max(i['speed'] for i in items)
                time_span = max(i['time'] for i in items) - min(i['time'] for i in items)
                dict_item['workTemperature'] = max_temp
                dict_item['workSpeed'] = max_speed
                dict_item['workHours'] = round(time_span/3600, 2)
                lst_result.append(dict_item)
        return lst_result

    def __fill_input_records(self, obj_session, lst_data, n_type):
        lst_result = []
        lst_batchNos = list({obj_item.batch_number for obj_item in lst_data})
        dict_batchNos = self.__get_batchNos_info(obj_session, lst_batchNos)

        for obj_item in lst_data:
            dict_data = object_as_dict(obj_item)
            dict_tmp = {
                "time": dict_data["time"],
                "type": n_type, #投入物/產出物/餘廢料
                "action": EDevAction.IN if dict_data["action"] == 1 else EDevAction.OUT,
                "item_no": dict_data["item_no"],
                "item_name": dict_data["item_name"],
                "itemCategory": dict_data["category"],
                "itemSubCategory": dict_data["itemSubCategory"],
                "batch_number": dict_data["batch_number"],
                "itemType": dict_batchNos[dict_data["batch_number"]].get("itemType", 0) if dict_data[
                                                                                               "batch_number"] in dict_batchNos else 0,
                "validDate": dict_batchNos[dict_data["batch_number"]].get("validDate", 0) if dict_data[
                                                                                                 "batch_number"] in dict_batchNos else 0,
                "serial_no": dict_data["serial_no"],
                "unit": dict_data["unit"],
                "count": dict_data["count"],
                "subCategory": 0  # 與output/reuse統一格式
            }
            lst_result.append(dict_tmp)

        return lst_result

    def __fill_output_reuse_records(self, obj_session, list_data, n_type):
        lst_result = []

        lst_batchNos = list({obj_item.batch_number for obj_item in list_data})
        dict_batchNos = self.__get_batchNos_info(obj_session, lst_batchNos)

        for obj_item in list_data:
            dict_data = object_as_dict(obj_item)
            n_category, n_subCategory = get_output_item_info(dict_data["item_no"])
            lst_result.append({
                "time": dict_data["time"],
                "action":  EDevAction.OUT if dict_data["action"] == 1 else EDevAction.IN,
                "type": n_type,  # 投入物/產出物/餘廢料
                "item_no": dict_data["item_no"],
                "item_name": dict_data["item_name"],
                "itemCategory": n_category, # 原料/物料/在製品/在製品/製成品
                "itemSubCategory": n_subCategory, # 在製品/製成品的子類別
                "subCategory": 0 if n_type == 2 else dict_data["itemSubCategory"], #餘廢料的子類別
                "batch_number": dict_data["batch_number"],
                "itemType": dict_batchNos[dict_data["batch_number"]].get("itemType", 0) if dict_data[
                                                                                               "batch_number"] in dict_batchNos else 0,
                # "itemType": EItemType.NEW if f_output else EItemType.REMAINING if dict_data["category"] == EReuseCategory.REMAINING else EItemType.WASTE,
                "validDate": dict_batchNos[dict_data["batch_number"]].get("validDate", 0) if dict_data[
                                                                                                 "batch_number"] in dict_batchNos else 0,

                "serial_no": "" if n_type == 1 else dict_data["serial_no"],
                "unit": dict_data["unit"],
                "count": dict_data["count"]
            })

        return lst_result

    def __fill_input_output_reuse_records(self, obj_session, lst_input, lst_output , lst_reuse):
        # 取得出入產紀錄
        # n_type :
        # 1: input         # 2: output         # 3: reuse
        lst_result = []
        lst_tmp1 = self.__fill_input_records(obj_session, lst_input, 1)
        lst_tmp2 = self.__fill_output_reuse_records(obj_session, lst_output, 2)
        lst_tmp3 = self.__fill_output_reuse_records(obj_session, lst_reuse, 3)
        lst_result = lst_tmp1 + lst_tmp2 + lst_tmp3
        lst_result = sorted(lst_result, key=lambda x: (x['time'], x['itemType']))

        return lst_result

    def __grouped_input(self,obj_session, list_data, n_type):
        lst_result = []
        batch_groups = defaultdict(list)
        lst_batchNos = list({obj_item.batch_number for obj_item in list_data})
        dict_batchNos = self.__get_batchNos_info(obj_session, lst_batchNos)
        # batch_number 分群
        for obj_item in list_data:
            dict_item = object_as_dict(obj_item)
            key = (dict_item['item_no'], dict_item['batch_number'], dict_item['serial_no'])
            batch_groups[key].append(dict_item)

        for str_key, lst_items in batch_groups.items():
            f_total1 = sum(dict_item['count'] for dict_item in lst_items if dict_item['action'] == 1)
            f_total2 = sum(dict_item['count'] for dict_item in lst_items if dict_item['action'] == 2)
            f_count = f_total1 - f_total2

            # 取第一筆資料作為代表
            dict_data = lst_items[0]
            dict_tmp = {
                    "item_no": dict_data["item_no"],
                    "item_name": dict_data["item_name"],

                    "itemSubCategory": dict_data["itemSubCategory"],
                    "itemCategory": dict_data["category"],
                    "batch_number": dict_data["batch_number"],
                    "itemType": dict_batchNos[dict_data["batch_number"]].get("itemType", 0) if dict_data[
                                                                                                   "batch_number"] in dict_batchNos else 0,
                    "validDate": dict_batchNos[dict_data["batch_number"]].get("validDate", 0) if dict_data[
                                                                                                   "batch_number"] in dict_batchNos else 0,
                    "serial_no": dict_data["serial_no"],
                    "unit": dict_data["unit"],
                    "subCategory": 0 #與output/reuse統一格式
            }
            if n_type == 1:
                dict_tmp["count"] = f_count
                dict_tmp["receiveCount"] = f_total1
                dict_tmp["returnCount"] = f_total2
            else:
                dict_tmp["time"] = dict_data["time"]
                dict_tmp["action"] = dict_data["action"]
                dict_tmp["count"] = f_total1 if dict_data["action"] == 1 else f_total2
            lst_result.append(dict_tmp)
        lst_result = sorted(lst_result, key=lambda x: x['itemCategory'])
        return lst_result

    def __grouped_output_reuse(self, obj_session, list_data, n_type, f_output, lst_bom=[]):
        '''
        n_type
        1: group by batch_no
        2: group by batch_no+serial_no
        '''
        lst_result = []
        batch_groups = defaultdict(list)
        lst_batchNos = list({obj_item.batch_number for obj_item in list_data})
        dict_batchNos = self.__get_batchNos_info(obj_session, lst_batchNos)
        # batch_number 分群
        for obj_item in list_data:
            dict_item = object_as_dict(obj_item)
            if n_type == 1:
                str_key = (dict_item['item_no'], dict_item['batch_number'])
            else:
                str_key = (dict_item['item_no'], dict_item['batch_number'], dict_item['serial_no'])
            batch_groups[str_key].append(dict_item)

        for key, lst_items in batch_groups.items():
            f_total = sum(dict_item['count'] for dict_item in lst_items)
            # 取第一筆資料作為代表
            dict_data = lst_items[0]
            n_bomWeight = 0.0

            if lst_bom:
                if dict_data["item_no"] in self.__m_dict_bom_weight:
                    n_bomWeight = self.__m_dict_bom_weight[dict_data["item_no"]]
                else:
                    dict_bom = self.find_by_itemno(lst_bom[0], dict_data["item_no"])
                    if dict_bom:
                        n_bomWeight = dict_bom["weight"]
                    self.__m_dict_bom_weight[dict_data["item_no"]] = dict_bom["weight"] if dict_bom else 0
            n_category, n_subCategory = get_output_item_info(dict_data["item_no"])
            lst_result.append({
                "time": dict_data["time"],
                "action": dict_data["action"],
                "item_no": dict_data["item_no"],
                "item_name": dict_data["item_name"],
                "itemCategory": n_category, # 原料/物料/在製品/在製品/製成品
                "itemSubCategory": n_subCategory, # 在製品/製成品的子類別
                "subCategory": 0 if f_output else dict_data["itemSubCategory"], #餘廢料的子類別
                "batch_number": dict_data["batch_number"],
                "itemType": dict_batchNos[dict_data["batch_number"]].get("itemType", 0) if dict_data[
                                                                                               "batch_number"] in dict_batchNos else 0,
                # "itemType": EItemType.NEW if f_output else EItemType.REMAINING if dict_data["category"] == EReuseCategory.REMAINING else EItemType.WASTE,
                "validDate": dict_batchNos[dict_data["batch_number"]].get("validDate", 0) if dict_data[
                                                                                                 "batch_number"] in dict_batchNos else 0,

                "serial_no": "" if n_type == 1 else dict_data["serial_no"],
                "unit": dict_data["unit"],
                "count": f_total,
                "bomWeight": n_bomWeight
            })
        lst_result = sorted(lst_result, key=lambda x: x['itemType'])
        return lst_result

    def find_by_itemno(self, dict_node, str_item_no):
        if dict_node.get("no") == str_item_no:
            return dict_node

        for dict_child in dict_node.get("children", []):
            dict_result = self.find_by_itemno(dict_child, str_item_no)
            if dict_result:
                return dict_result

        return None  # 找不到
    '''
    def __fill_input_loss(self, lst_input, lst_reuse):
        for dict_input in lst_input:
            f_waste = 0
            for dict_reuse in lst_reuse:
                if (dict_input["itemSubCategory"] == dict_reuse["itemSubCategory"]) and (dict_reuse["itemType"] == EItemType.WASTE):
                    f_waste += dict_reuse["count"]
            if dict_input["count"]:
                # 計算損耗數量而非損耗率
                #dict_input["loss"] = round(float((f_waste / (dict_input["receiveCount"] - dict_input["returnCount"]))*100),2)
                dict_input["loss"] = f_waste
            else:
                dict_input["loss"] = 0
    '''
    def __fill_input_loss(self, lst_input, lst_reuse):
        dict_temp = {}
        for dict_reuse in lst_reuse:
            for dict_input in lst_input:
                if (dict_input["itemSubCategory"] == dict_reuse["itemSubCategory"]) and (
                        dict_reuse["itemType"] == EItemType.WASTE):
                    dict_temp[dict_input["item_no"]] = dict_reuse["count"]
                    break
        return dict_temp

    def __retrieve_labor_time(self, obj_session, n_date, lst_labor):
        dict_temp = {"workPreHours": 0, "workPostHours": 0, "workPreCount": 0, "workPostCount": 0,
                       "restPreHours": 0, "restPostHours": 0, "restPreCount": 0, "restPostCount": 0,
                       "cleanPreHours": 0, "cleanPostHours": 0, "cleanPreCount": 0, "cleanPostCount": 0,
                       "laborWage": 0
                       }
        grouped = defaultdict(list)

        # 分群：以 (action, subAction) 為 key
        for item in lst_labor:
            key = (item['action'], item.get('stationStage', 0))  # 預設 subAction 為 0
            grouped[key].append(item)

        dict_result = {}

        for (action, stationStage), items in grouped.items():
            hours = [i['hours'] for i in items if i['hours'] > 0]
            max_end = max(hours) if hours else 0

            dict_result[(action, stationStage)] = {
                "hours": max_end,
                "records": items
            }

        for tuple_action, dict_tmp in dict_result.items():
            n_action = tuple_action[0]
            n_stationStage = tuple_action[1]
            if n_action == 1:
                if n_stationStage == 1:
                    dict_temp["workPreHours"] = dict_tmp["hours"]
                    dict_temp["workPreCount"] = len(dict_tmp["records"])
                elif n_stationStage == 2:
                    dict_temp["workPostHours"] = dict_tmp["hours"]
                    dict_temp["workPostCount"] = len(dict_tmp["records"])
            elif n_action == 2:
                if n_stationStage == 1:
                    dict_temp["restPreHours"] = dict_tmp["hours"]
                    dict_temp["restPreCount"] = len(dict_tmp["records"])
                elif n_stationStage == 2:
                    dict_temp["restPostHours"] = dict_tmp["hours"]
                    dict_temp["restPostCount"] = len(dict_tmp["records"])
            elif n_action == 3:
                if n_stationStage == 1:
                    dict_temp["cleanPreHours"] = dict_tmp["hours"]
                    dict_temp["cleanPreCount"] = len(dict_tmp["records"])
                elif n_stationStage == 2:
                    dict_temp["cleanPostHours"] = dict_tmp["hours"]
                    dict_temp["cleanPostCount"] = len(dict_tmp["records"])
        '''
        if dict_temp["workPreHours"]:
            dict_temp["workPreHours"] = dict_temp["workPreHours"] - dict_temp["restPreHours"]
        if dict_temp["workPostHours"]:
            dict_temp["workPostHours"] = dict_temp["workPostHours"] - dict_temp["restPostHours"]
        '''
        lst_wage = (
            obj_session.query(CTableLaborWage)
            .filter(CTableLaborWage.date <= n_date)
            .all()
        )
        n_wage = 0
        for obj_wage in lst_wage:
            if obj_wage.type == EEmployeeType.PART_TIME and obj_wage.level == 1:
                n_wage =obj_wage.hourly
        f_totalHours = round(((dict_temp["workPreCount"] * dict_temp["workPreHours"]) + (dict_temp["workPostCount"] * dict_temp["workPostHours"])) * n_wage, 2)
        dict_temp["laborWage"] = f_totalHours
        return dict_temp

    def __retrieve_productline(self, obj_session, str_id):
        str_name = ''
        if str_id:
            lst_result = (obj_session.query(
                CTableProductLine.location
            )
            .filter(CTableProductLine.no == str_id)
            .all()
             )
            if lst_result:
                str_name = lst_result[0].location
        return str_name

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

# 投入物/餘廢料/ 產出物預估的數量
class CExpectedData(CPrivilegeControl):

    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
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
                    lst_obj_query = (obj_session.query(CTableWorkOrder, CTableProductLine)
                                 .filter(*lst_where)
                                 .outerjoin(CTableProductLine,
                                            CTableProductLine.no == CTableWorkOrder.production_line_no)
                                 .group_by(CTableWorkOrder.no)
                                 .order_by(CTableWorkOrder.date.asc())
                                 .offset(n_start).limit(n_count).all())
                else:
                    lst_obj_query = (obj_session.query(CTableWorkOrder, CTableProductLine)
                                 .filter(*lst_where)
                                 .outerjoin(CTableProductLine,
                                                CTableProductLine.no == CTableWorkOrder.production_line_no)
                                 .group_by(CTableWorkOrder.no)
                                 .order_by(CTableWorkOrder.date.asc())
                                 .all())
                lst_ids = []
                dict_workOrder = {}
                for obj_work, obj_line in lst_obj_query:
                    lst_ids.append(obj_work.no)
                    dict_workOrder[obj_work.no] = {"date": obj_work.date,
                                                   "productLine_no": obj_line.no if obj_line else "",
                                                   "productLineName": obj_line.name if obj_line else "",
                                                  }
                lst_obj_input = (
                    obj_session.query(
                        CTableProcessOrder.work_order_no,
                        CTableProcessOrder.no,
                        CTableProcessOrder.category,
                        CTableProcessOrder.item_no,
                        CTableProcessOrder.item_name,
                        CTableProcessOrder.itemCategory,
                        CTableProcessOrder.itemSubCategory,
                        CTableBatchNoSerialNo,
                        CTableBatchNumber.itemType
                    )
                    .filter(CTableProcessOrder.work_order_no.in_(lst_ids),
                            CTableProcessOrder.category.in_(
                                [EProcessOrderCategory.RECEIVE, EProcessOrderCategory.RETURN]))
                    .outerjoin(CTableBatchNoSerialNo,
                               CTableProcessOrder.no == CTableBatchNoSerialNo.ref_order_no)
                    .outerjoin(CTableBatchNumber,
                               CTableBatchNoSerialNo.batch_number == CTableBatchNumber.no)
                    .all()
                )

                # 投入物預期資料
                dict_result = {}
                for str_work_order_no, str_no, n_category, item_no, item_name, itemCategory, itemSubCategory, obj_batchNo, itemType in lst_obj_input:
                    if not obj_batchNo: continue
                    # 複合 Key 包含 Order 資訊與 Batch 資訊
                    obj_key = (str_work_order_no, n_category, item_no, obj_batchNo.batch_number)

                    if obj_key not in dict_result:
                        dict_result[obj_key] = {
                            "date": obj_batchNo.time,
                            "item_no": item_no,
                            "item_name": item_name,
                            "itemCategory": itemCategory,
                            "itemSubCategory": itemSubCategory,
                            "itemType": itemType if itemType else 0,
                            "unit": obj_batchNo.unit,
                            "total": 0,  # 整體批號總數
                            "batchInfo": obj_batchNo,  # 批號序號資訊
                        }
                    dict_result[obj_key]["total"] += (obj_batchNo.expectedCount or 0)

                dict_temp = {}
                for (str_work_order_no, n_category, item_no, str_batch_no), dict_data1 in dict_result.items():
                    obj_key = (str_work_order_no, n_category, item_no)
                    if obj_key not in dict_temp:
                        dict_temp[obj_key] = {
                            "category": n_category,
                            "date": dict_data1['date'],
                            "item_no": item_no,
                            "item_name": dict_data1['item_name'],
                            "itemCategory": dict_data1['itemCategory'],
                            "itemSubCategory": dict_data1['itemSubCategory'],
                            "itemType": dict_data1['itemType'],
                            "unit": dict_data1['unit'],
                            "total": 0,  # 整體品項數量總數
                            "batch_number": []
                        }
                    dict_temp[obj_key]["total"] += (dict_data1['total'] or 0)
                    dict_temp[obj_key]["batch_number"].append({"batch_number": dict_data1['batchInfo'].batch_number,
                                                               "validDate": dict_data1['batchInfo'].validDate,
                                                               "itemType": dict_data1['itemType'],
                                                               "expectedCount": dict_data1[
                                                                   'batchInfo'].expectedCount,
                                                               })

                for (str_work_order_no, n_category, item_no), dict_data in dict_temp.items():
                    dict_order = dict_workOrder[str_work_order_no]
                    dict_tmp = {
                        "workOrderDate": dict_order.get("date", 0),
                        "production_line_no": dict_order.get("productLine_no", ""),
                        "productionLineName": dict_order.get("productLineName", ""),
                        "category": n_category,
                        "date": dict_data['date'],
                        "item_no": item_no,
                        "item_name": dict_data['item_name'],
                        "itemCategory": dict_data['itemCategory'],
                        "itemSubCategory": dict_data['itemSubCategory'],
                        "unit": dict_data['unit'],
                        "totalExpectedCount": dict_data['total'],
                        "batch_number": dict_data['batch_number'],
                    }
                    lst_result.append(dict_tmp)


                # 產出物預期資料
                lst_obj_output = (
                    obj_session.query(
                        CTableProcessOrder,
                        CTableBatchNumber
                    )
                    .filter(CTableProcessOrder.work_order_no.in_(lst_ids),
                            CTableProcessOrder.category.in_(
                                [EProcessOrderCategory.REMAIN, EProcessOrderCategory.WASTE,
                                 EProcessOrderCategory.PRODUCT]))
                    .outerjoin(CTableBatchNumber,
                               CTableProcessOrder.no == CTableBatchNumber.ref_no)
                    .all()
                )

                dict_result2 = {}
                for obj_order, obj_batchNo in lst_obj_output:
                    # 複合 Key 包含 Order 資訊與 Batch 資訊
                    obj_key = (obj_order.work_order_no, obj_order.category, obj_order.item_no)

                    if obj_key not in dict_result:
                        dict_result2[obj_key] = {
                            "category": obj_order.category,
                            "date": obj_order.date,
                            "item_no": obj_order.item_no,
                            "item_name": obj_order.item_name,
                            "itemCategory": obj_order.itemCategory,
                            "itemSubCategory": obj_order.itemSubCategory,
                            "unit": obj_order.unit,
                            "total": 0,  # 整體品項數量總數
                            "batch_number": []
                        }
                    dict_result2[obj_key]["total"] += (obj_order.expectedCount or 0)
                    dict_result2[obj_key]["batch_number"].append({"batch_number": obj_batchNo.no,
                                                                  "validDate": obj_batchNo.validDate,
                                                                  "itemType": obj_batchNo.itemType,
                                                                  "expectedCount": obj_batchNo.expectedCount,
                                                                  })

                for (str_work_order_no, n_category, item_no), dict_row in dict_result2.items():
                    dict_order = dict_workOrder[str_work_order_no]
                    dict_tmp = {
                        "workOrderDate": dict_order.get("date", 0),
                        "production_line_no": dict_order.get("productLine_no", ""),
                        "productionLineName": dict_order.get("productLineName", ""),
                        "category": dict_row["category"],
                        "date": dict_row['date'],
                        "item_no": dict_row["item_no"],
                        "item_name": dict_row['item_name'],
                        "itemCategory": dict_row['itemCategory'],
                        "itemSubCategory": dict_row['itemSubCategory'],
                        "unit": dict_row['unit'],
                        "totalExpectedCount": dict_row['total'],
                        "batch_number": dict_row["batch_number"],
                    }
                    lst_result.append(dict_tmp)
            if lst_result:
                dict_extra_data['total'] = n_total
                dict_extra_data['count'] = len(lst_ids) # 以派工單筆數為主
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