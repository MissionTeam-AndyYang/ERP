# coding=utf8
from sqlalchemy import create_engine, orm

class CMaria(object):

    def __init__(self, str_db='ewdb', str_host='localhost', n_port=3306, str_user='root', str_password='ew42885615'):
        self.__m_objDB = None
        self.__m_n_port = n_port
        self.__m_str_db = str_db
        self.__m_str_user = str_user
        self.__m_str_host = str_host
        self.__m_str_password = str_password

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