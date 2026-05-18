# coding=utf8
import json
import validictory
from flask import request
from package.common.common import *
from package.log.log import CLogger
from package.auth.auth import CAuth
from package.dbwrapper.dbmgr import CDBMgr
from package.dbwrapper.table import *
from package.util.util import *
from jsonschema import validate, ValidationError

import base64
from .util import *

class CPrivilegeControl(object):

    def is_allowed_for_get(self, lst_privileges):
        return True

    def is_allowed_for_post(self, lst_privileges):
        return True

    def is_allowed_for_put(self, lst_privileges):
        return True

    def is_allowed_for_delete(self, lst_privileges):
        return True


#********************************************
# Login
#********************************************
class CLogin(CPrivilegeControl):

    def post(self, str_timezone='' , str_id=''):
        n_code = EErrorCode.ERROR_SUCCESS
        str_message = 'success'
        n_status_code = 200
        dict_extra_data = {}
        dict_schema = {'type': 'object',
                       'properties': { 'username': {'type': 'string', "minLength": 1}, 'password': {'type': 'string', "minLength": 1}}}

        try:
            dict_body = request.get_json()
            validate(instance=dict_body, schema=dict_schema)
            # check

            obj_auth = CAuth()
            str_token = obj_auth.login(dict_body.get('username', ''), dict_body.get('password', ''))
            if not str_token:
                n_code = EErrorCode.ERROR_OTHER_ERROR
                str_message = 'failed to login'
            else:
                dict_extra_data = {'token': str_token,
                                   'user': {}}
                with CDBMgr() as obj_dbmgr:
                    obj_session = obj_dbmgr.get_session()
                    obj_data = (
                        obj_session.query(CTableSession)
                        .filter(
                            CTableSession.token == str_token
                        )
                        .first()
                    )
                    if obj_data:
                        dict_user = self.__find_user_info(obj_data.user_no)
                        dict_extra_data['user'] = dict_user

        except Exception as error:
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'throw exception (error: %s)' % str(error)
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return n_status_code, n_code, str_message, dict_extra_data

    def delete(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}
        try:
            #Ignore error code because token is deleted fit "time to live"
            CAuth().logout(request.args.get('token'))
        except Exception as error:
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'throw exception (error: %s)' % str(error)
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return n_status_code, n_code, str_message, dict_extra_data

    def __find_user_info(self, str_user_no):
        dict_extra_data = {}

        return dict_extra_data


class CDeviceLogin():

    def post(self, str_timezone='' , str_id=''):
        n_code = EErrorCode.ERROR_SUCCESS
        str_message = 'success'
        n_status_code = 200
        dict_extra_data = {"serverTimestamp": util_retrieve_now_time(),
                           "serverId": get_server_id(),
                           'user': {}}
        dict_schema = {'type': 'object',
                       'properties': {'registerNo': {'type': 'string', "minLength": 1},
                                      'username': {'type': 'string', "minLength": 1},
                                      'password': {'type': 'string', "minLength": 1}},
                       'required': ['registerNo', 'username', 'password']}

        try:
            str_body = request.get_data(as_text=True)
            dict_body = request.get_json()
            validate(instance=dict_body, schema=dict_schema)
            str_hardwareId, n_role = self.__retrieve_role(dict_body["registerNo"])
            if str_hardwareId and n_role:
                # check

                # base64編碼
                #original_text = "admin"
                #original_bytes = original_text.encode('utf-8')  # 轉成 bytes
                #encoded_bytes = base64.b64encode(original_bytes)
                #encoded_str = encoded_bytes.decode('utf-8')  # 轉回字串以便儲存或顯示

                # Base64 編碼過的字串
                str_pwd = dict_body.get('password', '')
                b_pwd = str_pwd.encode('utf-8')  # 轉成 bytes

                # 進行 Base64 解碼
                decoded_bytes = base64.b64decode(b_pwd)
                str_decoded_pwd = decoded_bytes.decode('utf-8')  # 轉回原本的字串

                obj_auth = CAuth()
                str_token = obj_auth.login(dict_body.get('username', ''), str_decoded_pwd)
                if not str_token:
                    n_code = EErrorCode.ERROR_INCORRECT_ACCOUNTPWD
                    str_message = 'incorrect account or password'
                else:
                    dict_user = {'token': str_token,
                                 'role': 0,
                                 'employee': {}}
                    with CDBMgr() as obj_dbmgr:
                        obj_session = obj_dbmgr.get_session()
                        obj_data = (
                            obj_session.query(CTableSession)
                            .filter(
                                CTableSession.token == str_token
                            )
                            .first()
                        )
                        if obj_data:
                            obj_employee = (
                                obj_session.query(CTableEmployee)
                                .filter(
                                    CTableEmployee.no == obj_data.user_no
                                )
                                .first()
                            )
                            if obj_employee:
                                f_isAllowed = False

                                if obj_employee.department == EDepartment.MANAGEMENT:
                                    f_isAllowed = True
                                else:
                                    if n_role == ELocationType.STORAGE:
                                        if obj_employee.department == EDepartment.WAREHOUSE:
                                            f_isAllowed = True
                                    elif n_role != ELocationType.STORAGE:
                                        if obj_employee.department == EDepartment.PRODUCTION:
                                            f_isAllowed = True
                                if f_isAllowed:
                                    obj_usergroup = self.__get_usergroup(obj_session, obj_data.user_no)
                                    dict_user["role"] = obj_usergroup.role if obj_usergroup else 0
                                    dict_user["employee"] = {
                                        "no": obj_employee.no,
                                        "name": obj_employee.name,
                                        "department": obj_employee.department
                                    }
                                    dict_extra_data['user'] = dict_user
                                else:
                                    n_code = EErrorCode.ERROR_PERMISSION_DENIED
                                    str_message = 'insufficient permissions'
                            else:
                                n_code = EErrorCode.ERROR_EMPLOYEENOTFOUND
                                str_message = 'employee not found'
            else:
                n_code = EErrorCode.ERROR_REGISTERNONOTFOUND
                str_message = 'registerNo not found'
        except ValidationError as e:
            n_code = EErrorCode.ERROR_INVAILD_BODY
            str_message = 'validated error: {0} {1}'.format(e.message, list(e.path))
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s, body: %s)'
                          % (self.__class__.__name__, str(e.message), str_body))
        except Exception as error:
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'throw exception (error: %s)' % str(error)
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s, body: %s)'
                          % (self.__class__.__name__, str(error), str_body))
        return n_status_code, n_code, str_message, dict_extra_data


    def __get_usergroup(self, obj_session, str_user_no):
        return (obj_session.query(CTableUserGroup)
                .filter(func.JSON_CONTAINS(CTableUserGroup.users, f'"{str_user_no}"'))
                .first())
    def __retrieve_role(self, str_registerNo):
        with CDBMgr() as obj_dbmgr:
            obj_session = obj_dbmgr.get_session()
            obj_result = (
                obj_session.query(CTableDevice)
                .filter(CTableDevice.no == str_registerNo)
                .first()
            )
        return obj_result.hardwareId if obj_result else "", obj_result.role if obj_result else 0


class CDeviceLogout():
    def delete(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}
        try:
            # Ignore error code because token is deleted fit "time to live"
            if 'HTTP_X_AUTH_TOKEN' in request.headers.environ:
                CAuth().logout(request.headers.environ['HTTP_X_AUTH_TOKEN'])
            else:
                n_code = EErrorCode.ERROR_INVAILD_TOKEN
                str_message = 'missing token parameter'
                CLogger().log(CLogger.LOG_LEVELERROR, '[%s] (error: %s)'
                              % (self.__class__.__name__, str_message))
        except Exception as error:
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'throw exception (error: %s)' % str(error)
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return n_status_code, n_code, str_message, dict_extra_data

