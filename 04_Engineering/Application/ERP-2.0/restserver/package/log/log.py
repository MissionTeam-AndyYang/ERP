# coding=utf8
import logging
import logging.handlers

class CSingleton(type):
    _obj_instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._obj_instances:
            cls._obj_instances[cls] = super(CSingleton, cls).__call__(*args, **kwargs)
        return cls._obj_instances[cls]


class CLogger(object):
    LOG_LEVELCRITICAL = logging.CRITICAL
    LOG_LEVELERROR = logging.ERROR
    LOG_LEVELWARNING = logging.WARNING
    LOG_LEVELINFO = logging.INFO
    LOG_LEVELDEBUG = logging.DEBUG
    LOG_LEVELOFF = logging.NOTSET

    __metaclass__ = CSingleton

    def __init__(self):
        self.__m_obj_logger = logging.getLogger(__name__)
        self.__m_obj_filehandler = None

    def set_target_file(self, str_file_path=''):
        if not str_file_path:
            raise ValueError
        else:
            if self.__m_obj_filehandler is not None:
                self.__m_obj_logger.removeHandler(self.__m_obj_filehandler)
                self.__m_obj_filehandler = None
            obj_formatter = logging.Formatter("%(asctime)s - %(thread)d - %(name)s - %(levelname)s - %(message)s")
            #self.__m_obj_filehandler = logging.FileHandler(str_file_path)
            self.__m_obj_filehandler = logging.handlers.RotatingFileHandler(str_file_path, mode='a',
                                                                            maxBytes=1024 * 1024 * 10,  # 10 MiB
                                                                            backupCount=20)
            self.__m_obj_filehandler.setFormatter(obj_formatter)
            self.__m_obj_logger.addHandler(self.__m_obj_filehandler)

    def set_level(self, n_level=LOG_LEVELINFO):
        self.__m_obj_logger.setLevel(n_level)

    def log(self, n_level, str_msg):
        self.__m_obj_logger.log(n_level, str_msg)

