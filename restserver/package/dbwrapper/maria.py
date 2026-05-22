# coding=utf8
from sqlalchemy import create_engine, orm
import os
from dotenv import load_dotenv

class CMaria(object):

    def __init__(self):
        # 開發環境載入 .env
        if os.getenv("ENV", "dev") == "dev":
            load_dotenv("../config/.env.dev")
        self.__m_str_host = os.getenv("DB_HOST")
        self.__m_n_port = int(os.getenv("DB_PORT", 3306))
        self.__m_str_db = os.getenv("DB_NAME")
        self.__m_str_user = os.getenv("DB_USER")
        self.__m_str_password = os.getenv("DB_PASSWORD")


    def gen_connection_str(self):
        str_connection = 'mariadb+mariadbconnector://'
        if self.__m_str_user != '' and self.__m_str_password != '':
            str_connection += self.__m_str_user + ':' + self.__m_str_password + '@'
        str_connection += self.__m_str_host + ':' + str(self.__m_n_port)
        str_connection += '/' + str(self.__m_str_db)
        return str_connection

    def disconnect(self):
        self.__m_objDB().close()
        self.__m_objDB = None