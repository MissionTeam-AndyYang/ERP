from package.log.log import CLogger
from configparser import ConfigParser

class CSingleton(type):
    _obj_instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._obj_instances:
            cls._obj_instances[cls] = super(CSingleton, cls).__call__(*args, **kwargs)
        return cls._obj_instances[cls]


class CFileStorageConfig(object):
    __metaclass__ = CSingleton

    def __init__(self):
        self.m_str_url = ''
        self.m_str_root_path = ''
        self.m_str_work_folder = ''
        self.m_str_customer_folder = ''
        self.m_str_location_folder = ''
        self.m_str_program_path = ''
        self.m_str_layout_folder = ''
        self.m_n_ignore_time = 0
        self.__m_obj_cfgparser = ConfigParser()

    def read(self, str_file_path):
        f_is_success = False
        if str_file_path:
            try:
                self.__m_obj_cfgparser.read(str_file_path)
                self.__parse('web_server')
                self.__parse('work_folder')
                self.__parse('customer_folder')
                self.__parse('location_folder')
                self.__parse('report_path')
                self.__parse('option')
                f_is_success = True
            except Exception as error:
                CLogger().log(CLogger.LOG_LEVELERROR, '[%s] failed to read config(path: %s, error: %s)'
                              % (self.__class__.__name__, str_file_path, str(error)))
        return f_is_success

    def __parse(self, str_key):
        if str_key:
            try:
                if str_key == 'web_server':
                    self.m_str_url = self.__m_obj_cfgparser.get(str_key,'url')
                    self.m_str_root_path = self.__m_obj_cfgparser.get(str_key,'root_path')
                elif str_key == 'work_folder':
                    self.m_str_work_folder = self.__m_obj_cfgparser.get(str_key, 'folder_name')
                elif str_key == 'customer_folder':
                    self.m_str_customer_folder = self.__m_obj_cfgparser.get(str_key, 'folder_name')
                elif str_key == 'location_folder':
                    self.m_str_location_folder = self.__m_obj_cfgparser.get(str_key, 'folder_name')
                elif str_key == 'report_path':
                    self.m_str_program_path = self.__m_obj_cfgparser.get(str_key,'program_path')
                    self.m_str_layout_folder = self.__m_obj_cfgparser.get(str_key,'layout_folder')
                elif str_key == 'option':
                    self.m_n_ignore_time = int(self.__m_obj_cfgparser.get(str_key,'ignore_abatement'))
            except Exception as error:
                CLogger().log(CLogger.LOG_LEVELERROR, '[%s] failed to get value of key(ota_type: %s, error: %s)'
                              % (self.__class__.__name__, str_key, str(error)))

