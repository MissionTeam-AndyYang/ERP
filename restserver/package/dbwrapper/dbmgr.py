# coding=utf8
from .maria import CMaria
from sqlalchemy import create_engine, orm
from package.log.log import CLogger
from sqlalchemy.exc import IntegrityError
from package.common.common import *

obj_base = orm.declarative_base()

class CDBMgrTrans():
    __m_obj_engine = None
    __m_session = None
    def __init__(self, obj_db=CMaria()):
        if not CDBMgr.__m_obj_engine:
            str_db_url = obj_db.gen_connection_str()
            CDBMgr.__m_obj_engine = create_engine(str_db_url,
                                                  pool_size=10,  # 連線池大小
                                                  max_overflow=20,  # 額外允許的連線數
                                                  pool_timeout=30,  # 等待可用連線的秒數
                                                  pool_recycle=3600,  # 超過一小時就回收連線
                                                  pool_pre_ping=True,  # 查詢前先 ping 測試連線
                                                  echo=False
                                                  )
            obj_base.metadata.create_all(CDBMgr.__m_obj_engine)
            CDBMgr.__m_session = orm.sessionmaker(bind=CDBMgr.__m_obj_engine)
            #print("__init__")

    def __enter__(self):
        self.m_obj_session = CDBMgr.__m_session()
        # 開啟 transaction
        self.m_transaction = self.m_obj_session.begin()
        #print("__enter__")
       # return self.m_obj_session
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type:
                # 有例外 → rollback 整個 transaction
                self.m_transaction.rollback()
            else:
                # 沒例外 → commit
                self.m_transaction.commit()
        finally:
            self.m_obj_session.close()

    # --------- 基本操作 (不 commit, 交給外層 transaction) ---------
    def insert(self, obj_new_data):
        n_code = EErrorCode.ERROR_SUCCESS
        try:
            self.m_obj_session.add(obj_new_data)
            #self.m_obj_session.commit()
        except IntegrityError as e:
            #self.m_obj_session.rollback()  # Rollback the session to avoid leaving the database in an inconsistent state
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(e)))
            n_code = EErrorCode.ERROR_DB
        return n_code

    def update(self, obj_table, lst_where, obj_data):
        n_code = EErrorCode.ERROR_SUCCESS
        try:
            self.m_obj_session.query(obj_table).filter(*lst_where).update(obj_data, synchronize_session=False)
            #self.m_obj_session.commit()
        except IntegrityError as e:
            #self.m_obj_session.rollback()  # Rollback the session to avoid leaving the database in an inconsistent state
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(e)))
            n_code = EErrorCode.ERROR_DB
        return n_code

    def delete(self, obj_table, *filters):
        n_code = EErrorCode.ERROR_SUCCESS
        try:
            self.m_obj_session.query(obj_table).filter(*filters).delete(synchronize_session=False)
            #self.m_obj_session.commit()
        except IntegrityError as e:
            #self.m_obj_session.rollback()
            CLogger().log(CLogger.LOG_LEVELERROR, f"[{self.__class__.__name__}] delete error: {e}")
            n_code = EErrorCode.ERROR_DB
        return n_code

    def get_engine(self):
        return CDBMgr.__m_obj_engine

    def get_session(self):
        return self.m_obj_session




class CDBMgr():
    __m_obj_engine = None
    __m_session = None
    def __init__(self, obj_db=CMaria()):
        if not CDBMgr.__m_obj_engine:
            str_db_url = obj_db.gen_connection_str()
            CDBMgr.__m_obj_engine = create_engine(str_db_url,
                                                  pool_size=10,  # 連線池大小
                                                  max_overflow=20,  # 額外允許的連線數
                                                  pool_timeout=30,  # 等待可用連線的秒數
                                                  pool_recycle=3600,  # 超過一小時就回收連線
                                                  pool_pre_ping=True,  # 查詢前先 ping 測試連線
                                                  echo=False
                                                  )
            obj_base.metadata.create_all(CDBMgr.__m_obj_engine)
            CDBMgr.__m_session = orm.sessionmaker(bind=CDBMgr.__m_obj_engine)
            #print("__init__")

    def __enter__(self):
        self.m_obj_session = CDBMgr.__m_session()
        #print("__enter__")
       # return self.m_obj_session
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.m_obj_session.rollback()
        self.m_obj_session.close()
        #print("__exit__")

    def insert(self, obj_new_data):
        n_code = EErrorCode.ERROR_SUCCESS
        try:
            self.m_obj_session.add(obj_new_data)
            self.m_obj_session.commit()
        except IntegrityError as e:
            self.m_obj_session.rollback()  # Rollback the session to avoid leaving the database in an inconsistent state
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(e)))
            n_code = EErrorCode.ERROR_DB
        return n_code

    # merge 會自動檢查主鍵是否存在，存在就 update，不存在就 insert
    def merge(self, obj_data):
        n_code = EErrorCode.ERROR_SUCCESS
        try:
            self.m_obj_session.merge(obj_data)
            self.m_obj_session.commit()
        except IntegrityError as e:
            self.m_obj_session.rollback()  # Rollback the session to avoid leaving the database in an inconsistent state
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(e)))
            n_code = EErrorCode.ERROR_DB
        return n_code


    def update(self, obj_table, lst_where, obj_data):
        n_code = EErrorCode.ERROR_SUCCESS
        try:
            self.m_obj_session.query(obj_table).filter(*lst_where).update(obj_data, synchronize_session=False)
            self.m_obj_session.commit()
        except IntegrityError as e:
            self.m_obj_session.rollback()  # Rollback the session to avoid leaving the database in an inconsistent state
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(e)))
            n_code = EErrorCode.ERROR_DB
        return n_code

    def delete(self, obj_table, *filters):
        n_code = EErrorCode.ERROR_SUCCESS
        try:
            self.m_obj_session.query(obj_table).filter(*filters).delete(synchronize_session=False)
            self.m_obj_session.commit()
        except IntegrityError as e:
            self.m_obj_session.rollback()
            CLogger().log(CLogger.LOG_LEVELERROR, f"[{self.__class__.__name__}] delete error: {e}")
            n_code = EErrorCode.ERROR_DB
        return n_code

    def get_engine(self):
        return CDBMgr.__m_obj_engine

    def get_session(self):
        return self.m_obj_session

