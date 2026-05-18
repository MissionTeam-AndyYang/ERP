# coding=utf8
import os
import signal
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../..")
from flask import Flask

from package.log.log import CLogger
from package.restserver.api.auth_uri import auth
from package.restserver.api.enterprise_uri import enterprise
from package.restserver.api.company_uri import company
from package.restserver.api.sale_uri import sale
from package.restserver.api.bom_uri import bom
from package.restserver.api.purchase_uri import purchase
from package.restserver.api.mix_uri import mix
from package.restserver.api.material_uri import material
from package.restserver.api.product_uri import product
from package.restserver.api.transitems_uri import transitems
from package.restserver.api.contract_uri import contract

from package.restserver.api.productline_uri import productline
from package.restserver.api.bankaccount_uri import bankaccount
from package.restserver.api.work_uri import work
from package.restserver.api.workorder_uri import workorder
from package.restserver.api.batchnumber_uri import batchnumber
from package.restserver.api.batchtrace_uri import batchtrace

from package.restserver.api.shipwarehouse_uri import shipwarehouse
from package.restserver.api.inventory_uri import inventory

from package.restserver.api.user_uri import user
from package.restserver.api.device_uri import device
from package.restserver.api.aps_uri import aps

from package.restserver.api.heartbeat_uri import heartbeat
from package.restserver.api.goods_uri import goods
from package.restserver.api.quotation_uri import quotation

from package.common.common import *

g_obj_flask = Flask(__name__)

g_obj_flask.register_blueprint(auth)
g_obj_flask.register_blueprint(enterprise)
g_obj_flask.register_blueprint(sale)
g_obj_flask.register_blueprint(purchase)
g_obj_flask.register_blueprint(company)
g_obj_flask.register_blueprint(mix)
g_obj_flask.register_blueprint(product)
g_obj_flask.register_blueprint(transitems)
g_obj_flask.register_blueprint(contract)

g_obj_flask.register_blueprint(productline)
g_obj_flask.register_blueprint(work)
g_obj_flask.register_blueprint(workorder)
g_obj_flask.register_blueprint(bankaccount)
g_obj_flask.register_blueprint(bom)
g_obj_flask.register_blueprint(material)
g_obj_flask.register_blueprint(batchnumber)
g_obj_flask.register_blueprint(shipwarehouse)
g_obj_flask.register_blueprint(inventory)
g_obj_flask.register_blueprint(batchtrace)

g_obj_flask.register_blueprint(user)
g_obj_flask.register_blueprint(device)
g_obj_flask.register_blueprint(aps)

g_obj_flask.register_blueprint(heartbeat)

g_obj_flask.register_blueprint(goods)
g_obj_flask.register_blueprint(quotation)

g_shutdown_count = 0


def _shutdown(signum, frame):
    global g_shutdown_count
    if not g_shutdown_count:
        g_shutdown_count += 1
        CLogger().log(CLogger.LOG_LEVELINFO, 'Receive signal %d' % signum)
        print ('Receive signal %d' % signum)
        #_cleanup()
        sys.exit(0)

if __name__ == "__main__":
    try:
        CLogger().set_level(CLogger.LOG_LEVELINFO)
        if os.name == 'nt':
            #import os

            #os.system("tzutil /s \"UTC\"");
            CLogger().set_target_file(os.path.dirname(os.path.abspath(__file__)) + '/restserver.log')
        else:
            #os.environ['TZ'] = 'UTC'
            #time.tzset()
            CLogger().set_target_file('/var/log/restserver.log')

        if os.name != 'nt':
            signal.signal(signal.SIGINT, _shutdown)
            signal.signal(signal.SIGTERM, _shutdown)

        # determine if application is a script file or frozen exe
        str_path = ''
        str_config_path = ''
        if getattr(sys, 'frozen', False):
            str_path = os.path.dirname(sys.executable)
        elif __file__:
            str_path = os.path.join(os.path.dirname(__file__), os.pardir)
            if str_path:
                str_path = os.path.join(str_path, 'config')
        if str_path:
            str_config_path = os.path.join(str_path, 'filestorage.ini')

        CLogger().log(CLogger.LOG_LEVELINFO, 'Rest server is running')
        g_obj_flask.run(host='0.0.0.0', threaded=True)

        # conutine to execute when press
        # crtl+c in windows/linux
        print ('Terminate')
        CLogger().log(CLogger.LOG_LEVELINFO, 'Rest server is terminate')
    except Exception as error:
        str_message = 'throw exception (error: %s)' % str(error)
        CLogger().log(CLogger.LOG_LEVELERROR, 'main thread throw exception (error: %s)' %error)