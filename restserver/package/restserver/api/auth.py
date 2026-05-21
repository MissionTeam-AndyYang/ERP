# coding=utf8
import json
import validictory
from flask import request
from package.common.common import *
from package.log.log import CLogger
from package.auth.auth import CAuth
from package.dbwrapper.dbmgr import CDBMgr
from package.dbwrapper.table import *


class CPrivilegeControl(object):

    def is_allowed_for_get(self, lst_privileges):
        return any(privilege['category'] == EPrivilegeCategory.PROPERTY and privilege['action'] in (EPrivilegeAction.VIEW, EPrivilegeAction.REPORT)
                   for privilege in lst_privileges)

    def is_allowed_for_post(self, lst_privileges):
        return any(privilege['category'] == EPrivilegeCategory.PROPERTY and privilege['action'] == EPrivilegeAction.CREATION
                   for privilege in lst_privileges)

    def is_allowed_for_put(self, lst_privileges):
        return any(privilege['category'] == EPrivilegeCategory.PROPERTY and privilege['action'] == EPrivilegeAction.MODIFICATION
                   for privilege in lst_privileges)

    def is_allowed_for_delete(self, lst_privileges):
        return any(privilege['category'] == EPrivilegeCategory.PROPERTY and privilege['action'] == EPrivilegeAction.CANCELLATION
                   for privilege in lst_privileges)
