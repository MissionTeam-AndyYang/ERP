# coding=utf8
import os
import signal
import sys
import threading
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../..")
import threading

g_obj_lock = None


def init_lock():
    global g_obj_lock
    g_obj_lock = threading.Lock()


def acquire_lock():
    f_is_success = False
    global g_obj_lock
    if g_obj_lock:
        try:
            f_is_success = g_obj_lock.acquire()
        except:
            f_is_success = False
    return f_is_success


def release_lock():
    f_is_success = False
    global g_obj_lock
    if g_obj_lock:
        try:
            f_is_success = g_obj_lock.release()
        except:
            f_is_success = False
    return f_is_success

