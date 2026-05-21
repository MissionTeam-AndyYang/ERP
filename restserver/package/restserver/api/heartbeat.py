# coding=utf8
from package.common.common import *
from package.log.log import CLogger
from package.util.util import *
from.util import *


class CHeartbeat(object):

    def get(self, str_timezone='', str_id=''):
        str_message = 'success'
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {"serverTimestamp": util_retrieve_now_time(),
                           "serverId": get_server_id()}

        return n_status_code, n_code, str_message, dict_extra_data
