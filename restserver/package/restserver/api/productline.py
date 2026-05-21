# coding=utf8
import pytz
import json
import string
import validictory
from copy import deepcopy
from flask import request
from package.util.util import *
from package.common.common import *
from package.log.log import CLogger
from package.dbwrapper.table import *
from package.dbwrapper.dbmgr import CDBMgr
from sqlalchemy import func, cast, Numeric
from .util import *

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


class CProcess(CPrivilegeControl):

    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'total': 0, 'results': []}

        try:
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                lst_where = self.__fill_query_params()
                lst_obj_result = (
                    obj_session.query(CTableProcess)
                    .filter(*lst_where)
                    .order_by(CTableProcess.oneProcess.asc(), CTableProcess.secProcess.asc())
                    .all()
                )

                if lst_obj_result:
                    lst_result = []
                    for obj_row in lst_obj_result:
                        dict_row = {}
                        if obj_row:
                            dict_row["no"] = obj_row.no
                            dict_row["oneProcess"] = obj_row.oneProcess
                            dict_row["secProcess"] = obj_row.secProcess
                            dict_row["comment"] = obj_row.comment

                        lst_result.append(dict_row)
                    if lst_result:
                        dict_extra_data['total'] = len(lst_obj_result)
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

        return lst_where

class CProductLine(CPrivilegeControl):

    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'total': 0, 'results': []}

        try:
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                lst_where = self.__fill_query_params()
                lst_obj_result = (
                    obj_session.query(CTableProductLine)
                    .filter(*lst_where)
                    .order_by(CTableProductLine.oneProcess.asc(), CTableProductLine.secProcess.asc())
                    .all()
                )

                if lst_obj_result:
                    lst_result = []
                    for obj_row in lst_obj_result:
                        dict_row = {}
                        if obj_row:
                            dict_row["no"] = obj_row.no
                            dict_row["name"] = obj_row.name
                            dict_row["oneProcess"] = obj_row.oneProcess
                            dict_row["secProcess"] = obj_row.secProcess
                            dict_row["location"] = obj_row.location
                            dict_row["capacityUnit"] = obj_row.capacityUnit
                            dict_row["capacity"] = obj_row.capacity
                            dict_row["laborCount"] = obj_row.laborCount
                            dict_row["laborEfficiency"] = obj_row.laborEfficiency
                            dict_row["comment"] = obj_row.comment
                            dict_row["factory"] = {}
                            dict_row["stations"] = []
                            if obj_row.factory_data:
                                obj_factory = obj_row.factory_data
                                dict_row["factory"] = {"no": obj_factory.no,
                                                      "region": obj_factory.region,
                                                      "location": obj_factory.location,
                                                      "comment": obj_factory.comment}

                            if obj_row.station_data:
                                for obj_row2 in obj_row.station_data:
                                    dict_row2 = {"no": obj_row2.no, "name": obj_row2.name, "stage": obj_row2.stage, "comment": obj_row2.comment, "equipments":[]}
                                    if obj_row2.equipment_data:
                                        for obj_row3 in obj_row2.equipment_data:
                                            dict_row3 = {"no": obj_row3.no, "name": obj_row3.name, "appearance": obj_row3.appearance, "comment": obj_row3.comment}
                                            dict_row2["equipments"].append(dict_row3)
                                        dict_row["stations"].append(dict_row2)
                        lst_result.append(dict_row)
                    if lst_result:
                        dict_extra_data['total'] = len(lst_obj_result)
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
        if request.args.get('oneProcess'):
            lst_where.append(CTableProductLine.oneProcess == int(request.args.get('oneProcess')))
        return lst_where


class CStation(CPrivilegeControl):

    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'total': 0, 'results': []}

        try:
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                lst_where = self.__fill_query_params()
                lst_obj_result = (
                    obj_session.query(CTableStation)
                    .filter(*lst_where)
                    .order_by(CTableStation.production_line_no.asc())
                    .all()
                )

                if lst_obj_result:
                    lst_result = []
                    for obj_row in lst_obj_result:
                        dict_row = {}
                        if obj_row:
                            dict_row["no"] = obj_row.no
                            dict_row["name"] = obj_row.name
                            dict_row["stage"] = obj_row.stage
                            dict_row["comment"] = obj_row.comment
                            dict_row["productionLine"] = {}
                            if obj_row.line_data:
                                obj_line = obj_row.line_data
                                dict_row["productionLine"] = {"no": obj_line.no,
                                                              "name": obj_line.name,
                                                              "oneProcess": obj_line.oneProcess,
                                                              "secProcess": obj_line.secProcess}
                            lst_result.append(dict_row)
                    if lst_result:
                        dict_extra_data['total'] = len(lst_obj_result)
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
        return lst_where


class CEquipment(CPrivilegeControl):

    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'total': 0, 'results': []}

        try:
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                lst_where = self.__fill_query_params()
                lst_obj_result = (
                    obj_session.query(CTableEquipment)
                    .filter(*lst_where)
                    .order_by(CTableEquipment.station_no.asc())
                    .all()
                )

                if lst_obj_result:
                    lst_result = []
                    for obj_row in lst_obj_result:
                        dict_row = {}

                        if obj_row:
                            dict_row["no"] = obj_row.no
                            dict_row["name"] = obj_row.name
                            dict_row["appearance"] = obj_row.appearance
                            dict_row["comment"] = obj_row.comment
                            dict_row["station"] = {}
                            dict_row["productionLine"] = {}
                            if obj_row.station_data:
                                obj_station = obj_row.station_data
                                dict_row["station"] = {"no": obj_station.no,
                                                      "name": obj_station.name,
                                                      "stage": obj_station.stage,
                                                      "comment": obj_station.comment
                                                      }
                                if obj_station.line_data:
                                    obj_line = obj_station.line_data
                                    dict_row["productionLine"] = {"no": obj_line.no,
                                                                  "name": obj_line.name,
                                                                  "oneProcess": obj_line.oneProcess,
                                                                  "secProcess": obj_line.secProcess}
                            lst_result.append(dict_row)

                    if lst_result:
                        dict_extra_data['total'] = len(lst_obj_result)
                        dict_extra_data['results'] = lst_result
        except Exception as error:
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'throw exception (error: %s)' % str(error)
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return n_status_code, n_code, str_message, dict_extra_data

    def post(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}

        return n_status_code, n_code, str_message, dict_extra_data

    def put(self, str_timezone='', str_id=''):
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
        return lst_where




class CFactory(CPrivilegeControl):

    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {'total': 0, 'results': []}

        try:
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                lst_where = self.__fill_query_params()
                lst_obj_result = (
                    obj_session.query(CTableFactory)
                    .filter(*lst_where)
                    .all()
                )

                if lst_obj_result:
                    lst_result = []
                    for obj_row in lst_obj_result:
                        dict_row = {}
                        if obj_row:
                            dict_row["no"] = obj_row.no
                            dict_row["region"] = obj_row.region
                            dict_row["location"] = obj_row.location
                            dict_row["comment"] = obj_row.comment
                            lst_result.append(dict_row)
                    if lst_result:
                        dict_extra_data['total'] = len(lst_obj_result)
                        dict_extra_data['results'] = lst_result
        except Exception as error:
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'throw exception (error: %s)' % str(error)
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return n_status_code, n_code, str_message, dict_extra_data

    def post(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}

        return n_status_code, n_code, str_message, dict_extra_data

    def put(self, str_timezone='', str_id=''):
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
        return lst_where




