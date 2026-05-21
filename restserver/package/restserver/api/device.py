# coding=utf8
import pytz
import json
import string

from copy import deepcopy
from flask import request
from .util import *
from package.common.common import *
from package.log.log import CLogger
from package.dbwrapper.table import *
from package.dbwrapper.dbmgr import CDBMgr
from package.util.util import *
from jsonschema import validate, ValidationError
from package.auth.auth import CAuth

class CDevice(object):

    def post(self, str_timezone='' , str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}
        dict_schema = {'type': 'object',
                       'properties': {
                           "deviceId": {'type': 'string', "minLength": 1},
                           "deviceName": {'type': 'string', "minLength": 1},
                           "deviceRole": {'type': 'integer', 'enum': [ELocationType.STORAGE,
                                                                      ELocationType.PREPARING1,
                                                                      ELocationType.PREPARING2,
                                                                      ELocationType.PROCESSING,
                                                                      ELocationType.PACKAGING
                                                                      ]},
                           "deviceComment": {'type': 'string'}
                       },
                       "required": ["deviceId", "deviceName", "deviceRole", "deviceComment"]
                       }

        try:
            str_body = request.get_data(as_text=True)
            dict_body = request.get_json()
            validate(instance=dict_body, schema=dict_schema)
            with CDBMgr() as obj_dbmgr:
                str_no = self.__gen_no(dict_body["deviceRole"])
                new_data = CTableDevice(
                    no=str_no,
                    hardwareId=dict_body["deviceId"],
                    name=dict_body["deviceName"],
                    role=dict_body["deviceRole"],
                    comment=dict_body["deviceComment"],
                    creationTime=util_retrieve_now_time()
                )
                if obj_dbmgr.insert(new_data) != EErrorCode.ERROR_SUCCESS:
                    CLogger().log(CLogger.LOG_LEVELWARNING,
                                  '[%s] DeviceId existed %s' % (self.__class__.__name__, str_body))
                    dict_update = {"no": str_no,
                                   "name": dict_body["deviceName"],
                                   "role": dict_body["deviceRole"],
                                   "comment": dict_body["deviceComment"],
                                   "creationTime": util_retrieve_now_time()
                                   }
                    if obj_dbmgr.update(CTableDevice,
                                        [CTableDevice.hardwareId == dict_body["deviceId"]],
                                        dict_update) != EErrorCode.ERROR_SUCCESS:
                        n_code = EErrorCode.ERROR_OTHER_ERROR
                        str_message = 'failed to register device'
                        CLogger().log(CLogger.LOG_LEVELERROR, '[%s] %s %s' % (self.__class__.__name__, str_message, str_body))
                if n_code == EErrorCode.ERROR_SUCCESS:
                    dict_extra_data = {
                        "serverTimestamp": util_retrieve_now_time(),
                        "serverId": get_server_id(),
                        "registerNo": str_no
                    }
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


    def __gen_no(self, n_role):
        if n_role == ELocationType.STORAGE:
            str_type = 'S'
        else:
            str_type = 'P'
        str_no = "DEV%s" %(str_type) + util_random_code(6)
        return str_no

