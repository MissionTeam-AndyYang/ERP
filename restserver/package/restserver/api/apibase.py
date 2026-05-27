# coding=utf8
import json
from flask import Response
from flask import request
#from auth import CUserInfo
from abc import ABCMeta, abstractmethod
from package.auth.auth import CAuth

from package.common.common import EErrorCode
from package.log.log import CLogger

class CAPIBase(object):
    __metaclass__ = ABCMeta

    def run(self, str_id=''):
        str_message = 'success'
        n_code = EErrorCode.ERROR_SUCCESS
        n_status_code = 200
        dict_extra_data = {}
        CLogger().log(CLogger.LOG_LEVELINFO, "[%s] Request path received: %s, method: %s, parameters: %s"
                      % (self.__class__.__name__, request.path, request.method,  request.query_string))
        '''
         if self.__class__.__name__ != 'CHeartbeatURI':
            CLogger().log(CLogger.LOG_LEVELINFO, "[%s] Request path received: %s, method: %s, parameters: %s"
                          % (self.__class__.__name__, request.path, request.method,  request.query_string))
        '''
        try:
            obj_auth = None
            if self._is_reset_alive_time():
                obj_auth = CAuth()
            obj_executor = self._get_executor()
            str_content_type = request.headers['Content-Type'].rsplit(';', 1)[0] if 'Content-Type' in request.headers else ''
            header = request.headers.environ
            str_timezone = request.headers.environ['HTTP_X_TIMEZONE'] if 'HTTP_X_TIMEZONE' in request.headers.environ else ""
            if request.method in ['PUT', 'POST'] and str_content_type not in (
            'application/json', 'multipart/form-data'):
                n_status_code = 400
                n_code = EErrorCode.ERROR_OTHER_ERROR
                str_message = 'invalid content type'
            elif self._is_vaildate_param() and not request.get_json():
                n_status_code = 400
                n_code = EErrorCode.ERROR_OTHER_ERROR
                str_message = 'invalid parameter'
            elif self._is_vaildate_token() and 'HTTP_X_AUTH_TOKEN' not in request.headers.environ:
                n_status_code = 400
                n_code = EErrorCode.ERROR_INVAILD_TOKEN
                str_message = 'missing token parameter'
            elif self._is_reset_alive_time() and (not obj_auth or not obj_auth.reset_alive_time(request.headers.environ['HTTP_X_AUTH_TOKEN'])):
                CLogger().log(CLogger.LOG_LEVELERROR, "[%s] invaild token (token: %s)"
                              % (self.__class__.__name__, request.headers.environ['HTTP_X_AUTH_TOKEN']))
                n_status_code = 401
                n_code = EErrorCode.ERROR_INVAILD_TOKEN
                str_message = 'invaild token'
            else:
                f_is_allowed = True
                f_is_check_privilege = False
                lst_privileges = []
                if self._is_vaildate_token():
                    f_is_check_privilege = self._is_check_privilege()
                    #lst_privileges = CUserInfo().get_privileges(request.args.get('token'))
                if self._is_support_get() and request.method == 'GET':
                    if f_is_check_privilege:
                        f_is_allowed = obj_executor.is_allowed_for_get(lst_privileges)
                    if f_is_allowed:
                        CLogger().log(CLogger.LOG_LEVELDEBUG, '[%s] parameters (query_string: %s)' % (self.__class__.__name__, request.query_string))
                        n_status_code, n_code, str_message, dict_extra_data = obj_executor.get(str_timezone, str_id)
                elif self._is_support_post() and request.method == 'POST':
                    if f_is_check_privilege:
                        f_is_allowed = obj_executor.is_allowed_for_post(lst_privileges)
                    if f_is_allowed:
                        if self._is_vaildate_param():
                            CLogger().log(CLogger.LOG_LEVELINFO, '[%s] parameters (body: %s)' % (self.__class__.__name__, request.get_data(as_text=True)))
                        n_status_code, n_code, str_message, dict_extra_data = obj_executor.post(str_timezone, str_id)
                elif self._is_support_put() and request.method == 'PUT':
                    if f_is_check_privilege:
                        f_is_allowed = obj_executor.is_allowed_for_put(lst_privileges)
                    if f_is_allowed:
                        if self._is_vaildate_param():
                            CLogger().log(CLogger.LOG_LEVELDEBUG, '[%s] parameters (param: %s)' % (self.__class__.__name__, request.form.get('param')))
                        n_status_code, n_code, str_message, dict_extra_data = obj_executor.put(str_timezone, str_id)
                elif self._is_support_delete() and request.method == 'DELETE':
                    if f_is_check_privilege:
                        f_is_allowed = obj_executor.is_allowed_for_delete(lst_privileges)
                    if f_is_allowed:
                        if self._is_vaildate_param():
                            CLogger().log(CLogger.LOG_LEVELDEBUG, '[%s] parameters (param: %s)' % (self.__class__.__name__, request.form.get('param')))
                        n_status_code, n_code, str_message, dict_extra_data = obj_executor.delete(str_timezone, str_id)
                if not f_is_allowed:
                    n_status_code = 403
                    n_code = EErrorCode.ERROR_PERMISSION_DENIED
                    str_message = 'insufficient permissions'
        except Exception as error:
            n_status_code = 400
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = 'throw exception (error: %s)' % str(error)
            CLogger().log(CLogger.LOG_LEVELERROR, '[CAPIBase] throw exception (error: %s)'
                          % str(error))
        if self._is_customized_reponse():
            resp = Response(str_message)
        else:
            dict_reponse = {'code': n_code,
                            'message': str_message, 'payload': dict_extra_data}
            str_data = json.dumps(dict_reponse)
            resp = Response(response=str_data, mimetype='application/json')
        resp.status_code = n_status_code

        if n_code == EErrorCode.ERROR_SUCCESS:
            if request.method == 'GET':
                n_level = CLogger.LOG_LEVELDEBUG
            else:
                n_level = CLogger.LOG_LEVELINFO
        else:
            n_level = CLogger.LOG_LEVELERROR
        CLogger().log(n_level, '[%s] return information (status_code: %d, code: %d, message: %s, data: %s)' % (self.__class__.__name__, n_status_code, n_code, str_message, resp.data))
        return resp


    @abstractmethod
    def _get_executor(self):
        pass

    def _is_vaildate_token(self):
        return True


    def _is_reset_alive_time(self):
        import os
        if os.getenv("TOKEN_ENABLED", "0").lower() == "1":
            return False
        else:
            return True

    def _is_vaildate_param(self):
        return True if self._is_post_method() or self._is_put_method() else False

    def _is_support_get(self):
        return True

    def _is_support_post(self):
        return True

    def _is_support_put(self):
        return True

    def _is_support_delete(self):
        return True

    def _is_customized_reponse(self):
        return False

    def _is_get_method(self):
        return True if request.method == 'GET' else False

    def _is_post_method(self):
        return True if request.method == 'POST' else False

    def _is_put_method(self):
        return True if request.method == 'PUT' else False

    def _is_delete_method(self):
        return True if request.method == 'DELETE' else False

    def _is_check_privilege(self):
        #return True
        return False
