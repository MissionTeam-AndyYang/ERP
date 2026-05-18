# coding=utf8
import threading


class CSingleton(type):
    _obj_instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._obj_instances:
            cls._obj_instances[cls] = super(CSingleton, cls).__call__(*args, **kwargs)
        return cls._obj_instances[cls]


class CLockBase(object):
    __metaclass__ = CSingleton

    def __init__(self):
        self.__m_obj_lock = threading.Lock()

    def acquire_lock(self):
        f_is_success = False
        if self.__m_obj_lock:
            try:
                f_is_success = self.__m_obj_lock.acquire()
            except:
                f_is_success = False
        return f_is_success

    def release_lock(self):
        f_is_success = False

        if self.__m_obj_lock:
            try:
                 self.__m_obj_lock.release()
                 f_is_success = True
            except Exception as error:
                f_is_success = False
        return f_is_success



class CLockARAPDelta(CLockBase):

    def __init__(self):
        super(CLockARAPDelta, self).__init__()


