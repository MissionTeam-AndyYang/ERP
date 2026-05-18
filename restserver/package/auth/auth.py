# coding=utf8
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../..")
import time
import uuid
from package.common.common import *
from package.util.util import *
from package.log.log import CLogger
from datetime import datetime
from package.dbwrapper.table import *
from package.dbwrapper.dbmgr import CDBMgr
from sqlalchemy import delete

class CAuth(object):
    ALIVETIME = 60*60*8

    def reset_alive_time(self, str_token):
        f_result = False
        if str_token and self.__is_alive(str_token):
            n_time = util_retrieve_now_time() + self.ALIVETIME
            dict_set = {"expiredTime": n_time}
            with CDBMgr() as obj_dbmgr:
                try:
                    if obj_dbmgr.update(CTableSession, [CTableSession.token == str_token],
                                            dict_set) == EErrorCode.ERROR_SUCCESS:
                        f_result = True
                except Exception as error:
                    CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                                  % (self.__class__.__name__, error))
        return f_result

    def login(self, str_account, str_password):
        from argon2 import PasswordHasher
        from argon2.exceptions import VerifyMismatchError

        str_token = ''
        try:
            if str_account and str_password:
                with CDBMgr() as obj_dbmgr:
                    obj_session = obj_dbmgr.get_session()
                    obj_data = (
                        obj_session.query(CTableMember)
                        .filter(
                            CTableMember.account == str_account
                        )
                        .first()
                    )
                    # 建立雜湊器（可自定參數）
                    ph = PasswordHasher()
                    try:
                        if obj_data and obj_data.user_no:
                            ph.verify(obj_data.password, str_password)
                            # Generate token
                            str_uuid = str(uuid.uuid4()).replace("-", "")
                            str_tmp_token = str(uuid.uuid4()).replace('-', '')
                            n_time = util_retrieve_now_time() + self.ALIVETIME

                            new_data = CTableSession(
                                id=str_uuid,
                                token=str_tmp_token,
                                user_no=obj_data.user_no,
                                expiredTime=n_time
                            )
                            # Insert to session collection
                            if obj_dbmgr.insert(new_data) == EErrorCode.ERROR_SUCCESS:
                                str_id = str_uuid
                            if str_id:
                                str_token = str_tmp_token
                            else:
                                CLogger().log(CLogger.LOG_LEVELERROR, '[%s] failed to add record (account:%s, pwd: %s)'
                                              % (self.__class__.__name__, str_account, str_password))
                        else:
                            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] failed to retrieve data (account:%s, pwd: %s)'
                                          % (self.__class__.__name__, str_account, str_password))
                        print("密碼正確")
                    except VerifyMismatchError:
                        print("密碼錯誤")
                    except Exception as error:
                        CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                                      % (self.__class__.__name__, error))
                    '''
                    obj_data = (
                        obj_session.query(CTableMember)
                        .filter(
                                CTableMember.account == str_account,
                                CTableMember.password == str_password
                                )
                        .first()
                    )
                    

                    if obj_data and obj_data.user_no:
                        # Generate token
                        str_uuid = str(uuid.uuid4()).replace("-", "")
                        str_tmp_token = str(uuid.uuid4()).replace('-', '')
                        n_time = util_retrieve_now_time() + self.ALIVETIME

                        new_data = CTableSession(
                            id=str_uuid,
                            token=str_tmp_token,
                            user_no=obj_data.user_id,
                            expired_time=n_time
                        )
                        # Insert to session collection
                        if obj_dbmgr.insert(new_data) == EErrorCode.ERROR_SUCCESS:
                            str_id = str_uuid
                        if str_id:
                            str_token = str_tmp_token
                        else:
                            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] failed to add record (account:%s, pwd: %s)'
                                          % (self.__class__.__name__, str_account, str_password))
                    else:
                        CLogger().log(CLogger.LOG_LEVELERROR, '[%s] failed to retrieve data (account:%s, pwd: %s)'
                                      % (self.__class__.__name__, str_account, str_password))
                    '''
            else:
                CLogger().log(CLogger.LOG_LEVELERROR, '[%s] invalid data' % (self.__class__.__name__))
        except Exception as error:
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, error))
        return str_token

    def logout(self, str_token):
        f_result = False
        if str_token:
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                obj_delete = delete(CTableSession).where(CTableSession.token == str_token)
                obj_result = obj_session.execute(obj_delete)
                deleted_rows = obj_result.rowcount
                if deleted_rows:
                    f_result = True
                print(f"Deleted {deleted_rows} rows.")
                obj_session.commit()
        return f_result

    def __is_alive(self, str_token):
        f_result = False
        if str_token:
            with CDBMgr() as obj_dbmgr:
                obj_session = obj_dbmgr.get_session()
                obj_data = (
                    obj_session.query(CTableSession)
                    .filter(
                        CTableSession.token == str_token,
                        CTableSession.expiredTime >= util_retrieve_now_time()
                    )
                    .first()
                )
                if obj_data:
                    f_result = True
        return f_result


