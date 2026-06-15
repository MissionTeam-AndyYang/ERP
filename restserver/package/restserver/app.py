# coding=utf8
import os
import sys
from flask import Flask

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../..")

from package.log.log import CLogger
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
from package.restserver.api.plstatistics_uri import plstatistics
from package.restserver.api.item_uri import item
from package.restserver.api.v2.warehouse_uri import warehouse_v2

def create_app():
    app = Flask(__name__)

    lst_blueprints = [
        enterprise,
        sale,
        purchase,
        company,
        mix,
        product,
        transitems,
        contract,
        productline,
        work,
        workorder,
        bankaccount,
        bom,
        material,
        batchnumber,
        shipwarehouse,
        inventory,
        batchtrace,
        user,
        device,
        aps,
        heartbeat,
        goods,
        quotation,
        plstatistics,
        item,
        warehouse_v2
    ]

    for obj_bp in lst_blueprints:
        app.register_blueprint(obj_bp)
    CLogger().log(
        CLogger.LOG_LEVELINFO,
        "Rest server initialized"
    )

    return app
