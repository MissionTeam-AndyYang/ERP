# coding=utf8
from flask import Blueprint
from .auth import *
from .common import *
from .apibase import CAPIBase

SUBKEY = 'auth'
auth = Blueprint('auth', __name__)


