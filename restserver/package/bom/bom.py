# coding=utf8
import pytz
import string
from copy import deepcopy
from package.util.util import *
from package.common.common import *
from package.log.log import CLogger
from package.dbwrapper.table import *
from package.dbwrapper.dbmgr import CDBMgr
from sqlalchemy import delete
from sqlalchemy import func, cast, Numeric
import uuid
from package.restserver.api.util import *
from collections import defaultdict
import random
from datetime import date, datetime, time
from zoneinfo import ZoneInfo

class EBomProc(object):
    PROCESS_BAKING = 1  # 烘烤
    PROCESS_STUFFING = 2  # 塞灌
    PROCESS_MIXING = 3  # 拌料
    PROCESS_PROCESSING = 4  # 加工
    PROCESS_PACKAGING = 5  # 包裝


from abc import ABC, abstractmethod

class IBomTree(ABC):

    @abstractmethod
    def retrieve(self, str_bom_no):
        pass


class CCBOMTree(IBomTree):

    def __init__(self):
        super().__init__()

    def retrieve(self, str_product_no, n_product_ver, str_inproduct_no=""):
        lst_data = []
        try:
            if str_product_no:
                lst_tmp = self.__get_bom_for_product( str_product_no, n_product_ver)
                if str_inproduct_no:
                    dict_tmp = self.__find_item_by_no(lst_tmp, str_inproduct_no)
                    if dict_tmp:
                        lst_data = [dict_tmp]
                else:
                    lst_data = lst_tmp

        except Exception as error:
            CLogger().log(CLogger.LOG_LEVELERROR, '[%s] throw exception (error: %s)'
                          % (self.__class__.__name__, str(error)))
        return lst_data

    def __find_item_by_no(self, data, str_inproduct_no):
        if isinstance(data, list):
            for item in data:
                result = self.__find_item_by_no(item, str_inproduct_no)
                if result:
                    return result
        elif isinstance(data, dict):
            if data.get("no") == str_inproduct_no:
                return data
            if "children" in data:
                return self.__find_item_by_no(data["children"], str_inproduct_no)
        return None
    def __get_bom_for_product(self, str_product_no, n_product_ver):
        lst_data = []
        with CDBMgr() as obj_dbmgr:
            obj_session = obj_dbmgr.get_session()
            obj_product, obj_bom, obj_prodcut_ver= self.__get_product( obj_session, str_product_no, n_product_ver)
            dict_process = self.__get_process(obj_session, str_product_no)

            dict_data = {"category": EItemCategory.PRODUCT,
                         "no": str_product_no,
                         "name": obj_product.name if obj_product else '',
                         "subCategory": obj_product.category,
                         "version": n_product_ver,
                         "count_unit": EUnit.CASE, #obj_product.package1Unit if obj_product else '', # 數量單位
                         "count": 1,
                         "unit": "",#重量單位
                         "weight": 0,
                         "total_weight": 0,#重量*規格
                         "process": EBomProc.PROCESS_PACKAGING,
                         "bom":{
                             "bomNo": obj_bom.bom_no if obj_bom else '',
                             "bomVer": obj_bom.bom_version if obj_bom else '',
                             "productVer_no": obj_prodcut_ver.no if obj_prodcut_ver else '',
                             "productVer": obj_prodcut_ver.version if obj_prodcut_ver else 0,
                             "productVerDate": obj_prodcut_ver.date if obj_prodcut_ver else 0,
                         },
                         "productProc": dict_process,
                         "children": []}
            # "箱規"的在製品/製成品;規格&BOM No
            lst_bom = self.__get_inproduct_bom_count(str_product_no, n_product_ver)

            # 取得在製品Bom組成物
            for dict_bom in lst_bom:
                #print("?組/箱", dict_bom["product_version"], dict_bom["inproduct_no"], dict_bom["inproduct_name"],
                #      dict_bom["product_per_package_count"])
                lst_b1_tree, _ = self.__retrieve_bom1( dict_bom["bom1_no"])
                dict_tmp0 = {  # ?組/箱 多建一層node
                    "category": EItemCategory.PRODUCT,
                    "no": dict_bom["product_no"],
                    "name": obj_product.name,
                    "subCategory": obj_product.category,
                    "count_unit": obj_product.package2Unit,
                    "count": dict_bom["product_per_package_count"],  # ?組/箱
                    "unit": "",
                    "weight": 0,
                    "total_weight": 0,
                    "process": EBomProc.PROCESS_PACKAGING,
                    "productProc": dict_process,
                    "expectedLoss": dict_bom["product_expectedLoss"],
                    "actualLoss": dict_bom["product_actualLoss"],
                    "children": []
                }
                dict_inproduct_proc = self.__get_process(obj_session, dict_bom["inproduct_no"])
                dict_tmp1 = {
                    "category": EItemCategory.INPRODUCT,
                    "no": dict_bom["inproduct_no"],
                    "name": dict_bom["inproduct_name"],
                    "count_unit": dict_bom["inproduct_per_package_unit"],
                    "count": dict_bom["inproduct_per_package_count"],  # ?個/組
                    "unit": "",  # 重量單位
                    "weight": 0,
                    "total_weight": 0,
                    "process": dict_bom["process"],
                    "productProc": dict_inproduct_proc,
                    "expectedLoss": dict_bom["inproduct_expectedLoss"],
                    "actualLoss": dict_bom["inproduct_actualLoss"],
                    "inproduct_unit": dict_bom["inproduct_unit"],  # ?入/式 單位
                    "inproduct_count": dict_bom["inproduct_count"],  # ?入/式
                    "children": []
                }

                '''
                if dict_bom["product_per_package_count"]:
                    # 加工
                    dict_tmp1 = {
                        "category": EItemCategory.INPRODUCT,
                        "no": dict_bom["inproduct_no"],
                        "name": dict_bom["inproduct_name"],
                        "count_unit": dict_bom["inproduct_per_package_unit"],
                        "count": dict_bom["inproduct_per_package_count"],  # ?個/組
                        "unit": "",  # 重量單位
                        "weight": 0,
                        "total_weight": 0,
                        "process": EBomProc.PROCESS_PROCESSING,
                        "inproduct_unit": dict_bom["inproduct_unit"],  # ?入/式 單位
                        "inproduct_count": dict_bom["inproduct_count"],  # ?入/式
                        "children": []
                    }
                else:
                    #前備-拌料 ?
                    dict_tmp1 = {
                        "category": EItemCategory.INPRODUCT,
                        "no": dict_bom["inproduct_no"],
                        "name": dict_bom["inproduct_name"],
                        "count_unit": dict_bom["inproduct_per_package_unit"],
                        "count": dict_bom["inproduct_per_package_count"],  # ?個/組
                        "unit": "",
                        "weight": 0,
                        "total_weight": 0,
                        "process": EBomProc.PROCESS_MIXING,
                        "inproduct_unit": dict_bom["inproduct_unit"],  # ?入/式 單位
                        "inproduct_count": dict_bom["inproduct_count"],  # ?入/式
                        "children": []
                    }
                '''
                #print("=========================")
                #print("?個/組", dict_bom["inproduct_no"], dict_bom["inproduct_name"],
                #      dict_bom["inproduct_per_package_count"])
                #print("?入/式", dict_bom["inproduct_no"], dict_bom["inproduct_name"],
                #      dict_bom["inproduct_count"])
                for dict_node in lst_b1_tree:
                    dict_b1_data =  self.__gen_bom_dict(obj_session, dict_node)
                    dict_tmp1['children'].append(dict_b1_data)
                for str_bom2 in dict_bom["bom2_no"]:
                    lst_b2_tree, lst_b2_nodes = self.__retrieve_bom2( str_bom2)
                    for dict_node in lst_b2_tree:
                        dict_b2_data = self.__gen_bom_dict(obj_session, dict_node, False)
                        dict_tmp1['children'].append(dict_b2_data)
                # 新增至list
                # 計算箱規/組規重量
                f_total1 = 0.0  # 原料
                f_total2 = 0.0  # 物料&膠捲

                for dict_data1 in dict_tmp1["children"]:
                    dict_tmp1["unit"] = dict_data1["unit"]
                    if dict_data1["category"] not in [EItemCategory.MA, EItemCategory.AF]:
                        f_total1 += dict_data1["total_weight"]
                    else:
                        f_total2 += dict_data1["total_weight"]

                # 計算在製品(不含膠捲) * 入數 * 個數 + 物料(含膠捲)  * 個數
                dict_tmp1["weight"] = round(f_total1 + f_total2, 2)
                dict_tmp1["total_weight"] = round(f_total1 * dict_tmp1["count"] * dict_tmp1["inproduct_count"],
                                                  2) + round(f_total2 * dict_tmp1["count"], 2)
                if dict_bom["product_per_package_count"]:
                    dict_tmp0['children'].append(dict_tmp1)
                    # 取得製成品Bom組成物(組裝)
                    lst_product_level2_bom2 = self.__get_product_bom2_count(n_product_ver,
                                                                                 dict_bom["product_no"])
                    for dict_bom2 in lst_product_level2_bom2:
                        lst_b2_tree, lst_b2_nodes = self.__retrieve_bom2( dict_bom2["bom2_no"])
                        for dict_node in lst_b2_tree:
                            dict_b2_data = self.__gen_bom_dict(obj_session, dict_node, False)
                            dict_tmp0['children'].append(dict_b2_data)
                    f_total = 0.0
                    for dict_data0 in dict_tmp0["children"]:
                        dict_tmp0["unit"] = dict_data0["unit"]
                        f_total += dict_data0["total_weight"]
                    dict_tmp0["weight"] = round(f_total, 2)
                    dict_tmp0["total_weight"] = round(
                        f_total * dict_tmp0["count"], 2)
                    dict_data['children'].append(dict_tmp0)
                else:
                    dict_data['children'].append(dict_tmp1)

            # 查詢製成品外箱物料
            # FPE0022014_1
            str_no = str_product_no + '_1'
            lst_product_level1_bom2 = self.__get_product_bom2_count(n_product_ver,
                                                                         str_no)
            for dict_bom2 in lst_product_level1_bom2:
                lst_b2_tree, lst_b2_nodes = self.__retrieve_bom2( dict_bom2["bom2_no"])
                #print("箱規物料=========================")
                #print(dict_bom2["bom2_no"])
                for dict_node in lst_b2_nodes:
                    dict_b2_data = self.__gen_bom_dict(obj_session, dict_node, False)
                    dict_data["children"].append(dict_b2_data)
            for dict_tmp in dict_data["children"]:
                dict_data["unit"] = dict_tmp["unit"]
                dict_data["weight"] = round(dict_data["weight"] + dict_tmp["weight"], 2)
                dict_data["total_weight"] = round(dict_data["total_weight"] + dict_tmp["total_weight"], 2)
            lst_data.append(dict_data)
        return lst_data

    def __get_product(self, obj_session, str_product_no, n_ver):
        # 商品配方   # 製成品版本 製成品工序
        obj_product = (
            obj_session.query(
                CTableProduct,
                CTableProductSpec,
                CTableProductVer
            )
            .filter(CTableProduct.no == str_product_no)
            .outerjoin(
                CTableProductSpec,
                and_(
                    CTableProductSpec.product_no == CTableProduct.no,
                    CTableProductSpec.product_version == n_ver
                )
            )
            .outerjoin(
                CTableProductVer,
                CTableProductVer.item_no == CTableProduct.no
            )
            .first()
        )

        if not obj_product:
            return None, None, None

        return obj_product[0], obj_product[1], obj_product[2]
    def __get_process(self, obj_session, str_product_no):
        dict_data = {}
        # 商品配方   # 製成品版本 製成品工序
        obj_process = (
            obj_session.query(
                CTableProductProcess
            )
            .filter(CTableProductProcess.item_no == str_product_no)
            .first()
        )

        if obj_process:
            dict_data = object_as_dict(obj_process)
            dict_data["flows"] = []
            for obj_flow in obj_process.flows:
                dict_flow = object_as_dict(obj_flow)
                dict_data["flows"].append(dict_flow)
        return dict_data


    def __get_inproduct_bom_count(self, str_product_no, n_product_ver):
        lst_bom = []
        lst_inproduct = []

        with CDBMgr() as obj_dbmgr:
            obj_session = obj_dbmgr.get_session()
            str_no = str_product_no + '_1'
            lst_result = (
                obj_session.query(CTableProductSpec)
                .filter(
                    CTableProductSpec.product_no == str_no,
                    CTableProductSpec.product_version == n_product_ver
                )
                .all()
            )
            # 取得在製品規格
            # 查詢 組規/箱規 "規格"
            for obj_spec in lst_result:
                if obj_spec.item_type == EOutputCategory.INPRODUCT: #在製品 散裝
                    lst_inproduct.append({"bom_no": obj_spec.bom_no,
                                          "bom_version": obj_spec.bom_version,
                                          "inproduct_no": obj_spec.item_no,
                                          "inproduct_unit": 0,
                                          "inproduct_count": 0,
                                          "inproduct_per_package_unit": obj_spec.unit,
                                          "inproduct_per_package_count": obj_spec.count, #1箱幾個在製品
                                          "inproduct_expectedLoss": obj_spec.expectedLoss,
                                          "inproduct_actualLoss": obj_spec.actualLoss,
                                          "product_no": str_product_no,
                                          "product_version": obj_spec.product_version,
                                          "product_per_package_unit": 0,
                                          "product_per_package_count": 0,
                                          "product_expectedLoss": 0,
                                          "product_actualLoss": 0
                                          })
                else: # 製成品(組裝), 尋找組規
                    lst_tmp = (
                        obj_session.query(
                            CTableProductSpec
                        )
                        .filter(
                            CTableProductSpec.product_no == str_product_no,
                            #CTableProductSpec.product_version == n_version,
                            CTableProductSpec.product_version == obj_spec.product_version
                        )
                        .all()
                    )
                    for obj_tmp in lst_tmp:
                        if obj_tmp.item_type == EOutputCategory.INPRODUCT:  # 在製品; 箱規組規
                            lst_inproduct.append({"bom_no": obj_tmp.bom_no,
                                                  "bom_version": obj_tmp.bom_version,
                                                  "inproduct_no": obj_tmp.item_no,
                                                  "inproduct_unit": 0,
                                                  "inproduct_count": 0,
                                                  "inproduct_per_package_unit": obj_tmp.unit,
                                                  "inproduct_per_package_count": obj_tmp.count, # 一組幾支
                                                  "inproduct_expectedLoss": obj_tmp.expectedLoss,
                                                  "inproduct_actualLoss": obj_tmp.actualLoss,
                                                  "product_no": str_product_no,
                                                  "product_version": obj_spec.product_version,
                                                  "product_per_package_unit": obj_spec.unit,
                                                  "product_per_package_count": obj_spec.count,
                                                  "product_expectedLoss": obj_spec.expectedLoss,
                                                  "product_actualLoss": obj_spec.actualLoss
                                                  })  # 一箱幾罐/盒..
            # 取得在製品bom表
            for dict_inproduct in lst_inproduct:
                # 取得原料BOM
                lst_tmp1 = obj_session.query(
                    CTableInproductBOMSpec.bom12_no,
                    CTableInproductBOMSpec.count
                ).filter(
                    CTableInproductBOMSpec.category == EBomCategory.PM, # bom 類別
                    CTableInproductBOMSpec.item_no == dict_inproduct["bom_no"],
                    CTableInproductBOMSpec.item_version == dict_inproduct["bom_version"],
                    CTableInproductBOMSpec.inproduct_no == dict_inproduct["inproduct_no"]
                ).all()

                # 取得物料BOM
                lst_tmp2 = obj_session.query(
                    CTableInproductBOMSpec.bom12_no
                ).filter(
                    CTableInproductBOMSpec.category == EBomCategory.MA_AP, # bom 類別
                    CTableInproductBOMSpec.item_no == str_product_no,
                    CTableInproductBOMSpec.item_version == dict_inproduct["product_version"],
                    CTableInproductBOMSpec.inproduct_no == dict_inproduct["inproduct_no"]
                ).all()

                lst_bom2 = [row.bom12_no for row in lst_tmp2] if lst_tmp2 else  []
                if lst_tmp1:
                    obj_inproduct = (
                        obj_session.query(
                            CTableInproduct
                        )
                        .filter(
                            CTableInproduct.no == dict_inproduct["inproduct_no"]
                        )
                        .first()
                    )
                    # 取得製程
                    obj_bom1_number = (
                        obj_session.query(
                            CTableBOM1Number
                        )
                        .filter(
                            CTableBOM1Number.no == lst_tmp1[0].bom12_no
                        )
                        .first()
                    )
                    dict_inproduct_proc = self.__get_process(obj_session, dict_inproduct["inproduct_no"])
                    lst_bom.append({"inproduct_no": dict_inproduct["inproduct_no"],
                                     "inproduct_name": obj_inproduct.name,
                                     "inproduct_unit": obj_inproduct.package4Unit,
                                     "inproduct_count": lst_tmp1[0].count,  # ?入/式,不是一包有幾支
                                     "inproduct_per_package_unit": obj_inproduct.package3Unit,
                                     "inproduct_per_package_count": dict_inproduct["inproduct_per_package_count"], # ?個/組
                                     "inproduct_expectedLoss": dict_inproduct["inproduct_expectedLoss"],
                                     "inproduct_actualLoss": dict_inproduct["inproduct_actualLoss"],
                                     "product_no": dict_inproduct["product_no"],
                                     "product_version": dict_inproduct["product_version"],
                                     "product_per_package_unit": dict_inproduct["product_per_package_unit"],
                                     "product_per_package_count": dict_inproduct["product_per_package_count"], # ?組/箱
                                     "product_expectedLoss": dict_inproduct["product_expectedLoss"],
                                     "product_actualLoss": dict_inproduct["product_actualLoss"],
                                     "process": obj_bom1_number.category if obj_bom1_number else 0,
                                     "productProc": dict_inproduct_proc,
                                     "bom1_no": lst_tmp1[0].bom12_no,
                                     "bom2_no": lst_bom2})
        return lst_bom


    def __get_product_bom2_count(self, n_product_ver, str_no):
        lst_bom = []
        with CDBMgr() as obj_dbmgr:
            obj_session = obj_dbmgr.get_session()
            lst_result = (
                obj_session.query(
                    CTableProductBOMSpec.bom2_no,
                    CTableProductBOMSpec.count
                )
                .filter(
                    CTableProductBOMSpec.product_no == str_no,
                    CTableProductBOMSpec.product_version == n_product_ver
                )
                .all()
            )
            for obj_spec in lst_result:
                lst_bom.append({"product_no": str_no,
                                "bom2_no": obj_spec.bom2_no,
                                "count": obj_spec.count})
        return lst_bom

    def __retrieve_bom1(self, str_bom1):
        lst_tree = []
        lst_all_nodes = []
        from sqlalchemy import text
        str_query = text("""
                          WITH RECURSIVE CTE AS (
                              SELECT  parent_no,
                                      parent_name,
                                      child_category,
                                      child_id,
                                      child_name,                                  
                                      childUnit,                                  
                                      weight, 
                                      expectedLoss,
                                      actualLoss,
                                      processWeight,           
                                      CONCAT(parent_name, '>', child_name) AS cte_show, 
                                      weight AS cte_weight,
                                      1 AS level
                              FROM bom1
                                WHERE parent_no = :parent_no
                              UNION ALL
                              SELECT 
                                  bom1.parent_no, 
                                  bom1.parent_name, 
                                  bom1.child_category,
                                  bom1.child_id, 
                                  bom1.child_name,                               
                                  bom1.childUnit,                                                                               
                                  bom1.weight, 
                                  bom1.expectedLoss,
                                  bom1.actualLoss,
                                  bom1.processWeight, 
                                  CONCAT(CTE.cte_show, '>', bom1.child_name) AS cte_show,
                                  bom1.weight * CTE.cte_weight AS cte_weight,
                                  CTE.level + 1
                              FROM bom1
                              JOIN CTE ON bom1.parent_no = CTE.child_id                          
                          )
                          SELECT *
                          FROM CTE
                          ORDER BY level ASC;
                      """)

        with CDBMgr().get_engine().connect() as obj_conn:
            #print(str_bom1)
            lst_result = obj_conn.execute(str_query, {'parent_no': str_bom1})
            if lst_result:
                lst_tree, lst_all_nodes = self.__convert_bom_result(lst_result, True)
        return lst_tree, lst_all_nodes

    def __retrieve_bom2(self, str_bom2):
        lst_tree = []
        lst_all_nodes = []

        from sqlalchemy import text
        str_query = text("""
                          WITH RECURSIVE CTE AS (
                              SELECT  parent_no,
                                       parent_name,
                                       child_category,
                                       child_id,
                                       child_name,                                 
                                       childUnit,
                                       weight,                                   
                                       childUnit2,
                                       length,
                                       expectedLoss,
                                       actualLoss,
                                       count,
                                       processCount,
                                       CONCAT(parent_name, '>', child_name) AS cte_show, 
                                       weight AS cte_weight,
                                       1 AS level
                              FROM bom2
                              WHERE parent_no = :parent_no

                              UNION ALL
                               SELECT 
                                       bom2.parent_no, 
                                       bom2.parent_name, 
                                       bom2.child_category,
                                       bom2.child_id, 
                                       bom2.child_name, 
                                       bom2.childUnit, 
                                       bom2.count, 
                                       bom2.processCount, 
                                       bom2.childUnit2, 
                                       bom2.length, 
                                       bom2.expectedLoss,
                                       bom2.actualLoss,                                                     
                                       bom2.weight, CONCAT(CTE.cte_show, '>', bom2.child_name) AS cte_show,
                                       bom2.weight * CTE.cte_weight AS cte_weight,
                                       CTE.level + 1
                              FROM bom2
                              JOIN CTE ON bom2.parent_no = CTE.child_id      

                          )
                          SELECT *
                          FROM CTE
                          ORDER BY level ASC;
                      """)
        with CDBMgr().get_engine().connect() as obj_conn:
            #print(str_bom2)
            lst_result = obj_conn.execute(str_query, {'parent_no': str_bom2 })
            if lst_result:
                lst_tree, lst_all_nodes = self.__convert_bom_result(lst_result, False)
        return lst_tree, lst_all_nodes

    def __convert_bom_result(self, lst_result, is_bom1=True):
        from collections import defaultdict
        dict_tree = defaultdict(list)

        with CDBMgr() as obj_dbmgr:
            obj_session = obj_dbmgr.get_session()

            for row in lst_result:
                fields = dict(row._mapping)
                dict_node = {
                    'parent_no': fields['parent_no'],
                    'parent_name': fields['parent_name'],
                    'child_category': fields['child_category'],
                    'child_id': fields['child_id'],
                    'child_name': fields['child_name'],
                    'childUnit': fields['childUnit'],
                    'weight': fields['weight'],
                    'expectedLoss': fields['expectedLoss'],
                     "actualLoss": fields["actualLoss"],
                    'cte_show': fields['cte_show'],
                    'cte_weight': fields['cte_weight'],
                    'level': fields['level'],
                    'children': []
                }

                if is_bom1:
                    n_process = 0
                    # 取得在製品名稱
                    obj_inproduct = obj_session.query(CTableInproductBOMSpec).filter(
                        CTableInproductBOMSpec.category == EBomCategory.PM,
                        CTableInproductBOMSpec.bom12_no == dict_node['child_id']
                    ).first()

                    if obj_inproduct:
                        obj_bom1No = obj_session.query(CTableBOM1Number).filter(
                            CTableBOM1Number.no == obj_inproduct.bom12_no
                        ).first()
                        n_process = obj_bom1No.category if obj_bom1No else 0

                    dict_node.update({
                        'processWeight': fields['processWeight'],
                        #'process': obj_inproduct.inproduct_data.category if obj_inproduct else 0, #改用bom製程?
                        'process': n_process,  # 改用bom製程?
                        'item_no': obj_inproduct.inproduct_no if obj_inproduct else "",
                    })
                else:
                    dict_node.update({
                        'childUnit2': fields['childUnit2'],
                        'length': fields['length'],
                        'count': fields['count'],
                        'processCount': fields['processCount'],
                        'process': 0,
                    })

                dict_tree[dict_node['level']].append(dict_node)

            lst_tree = self.__build_tree(dict_tree, dict_tree[1])
            lst_all_nodes = []
            for obj_node in lst_tree:
                _, nodes = self.__cal_node_weight(obj_node, [])
                lst_all_nodes.extend(nodes)
        return lst_tree, lst_all_nodes


    def __build_tree(self, dict_tree, lst_nodes, n_level=1):
        lst_result = []
        for obj_node in lst_nodes:
            lst_children = self.__build_tree(dict_tree, dict_tree[n_level + 1], n_level + 1) if (
                                                                                                     n_level + 1) in dict_tree else []
            obj_node['children'] = [child for child in lst_children if child['parent_no'] == obj_node['child_id']]
            lst_result.append(obj_node)
        return lst_result

    def __cal_node_weight(self, obj_node, lst_all_nodes, dict_parent_node=None, level=0):
        """
        計算節點權重，子節點需要檢查其母節點的 childUnit 是否為 150，並根據母節點的 weight 進行加權計算
        """
        # 如果沒有子節點，則處理當前節點的 weight
        if not obj_node['children']:
            # 如果母節點存在且母節點的 childUnit 為 150，則進行加權計算
            obj_node['new_weight'] = obj_node['weight']
            '''
            if dict_parent_node and dict_parent_node['child_category'] == 2:
                obj_node['new_weight'] = round(obj_node['weight'] * dict_parent_node['weight'], 2)
            else:
                obj_node['new_weight'] = obj_node['weight']
            '''
            # 將當前節點加入節點列表
            lst_all_nodes.append(obj_node)
            return obj_node['new_weight'], lst_all_nodes

        n_total = 0.0
        lst_child_weights = []

        # 遍歷所有子節點，計算子節點的權重，並檢查母節點的 childUnit 是否為 150
        for obj_child in obj_node['children']:
            f_child_weight, lst_all_nodes = self.__cal_node_weight(
                obj_child, lst_all_nodes, obj_node, level + 1
            )
            n_total += f_child_weight
            lst_child_weights.append(f_child_weight)  # 記錄子節點的權重

        # 處理母節點的權重
        obj_node['new_weight'] = round(n_total, 2)
        obj_node['child_weights'] = lst_child_weights
        # 將母節點加入節點列表
        lst_all_nodes.append(obj_node)
        return obj_node['new_weight'], lst_all_nodes

    def __gen_bom_dict(self, obj_session, dict_node, is_bom1=True):
        str_item_no = dict_node.get("item_no", dict_node["child_id"])
        _, n_subCategory, _, _ = self.__get_material_info(obj_session, str_item_no)
        if is_bom1:
            if dict_node["child_category"] == 2:  # 在製品
                dict_process = self.__get_process(obj_session, str_item_no)
                return {
                    "category": EItemCategory.INPRODUCT,
                    "no": dict_node.get("item_no", dict_node["child_id"]),
                    "name": dict_node["child_name"],
                    "subCategory": n_subCategory,
                    "count_unit": dict_node["childUnit"],
                    "count": int(dict_node["weight"] / dict_node["new_weight"]),
                    "unit": EUnit.GRAM,
                    "weight": dict_node["new_weight"],
                    "expectedLoss": dict_node["expectedLoss"],
                    "actualLoss": dict_node["actualLoss"],
                    "total_weight": dict_node["weight"],
                    "process": dict_node["process"], #self.__convert_process(dict_node["process"]),
                    "productProc": dict_process,
                    "children": [self.__gen_bom_dict(obj_session, child, is_bom1) for child in dict_node['children']]
                }
            else:
                return {
                    "category": EItemCategory.PM,
                    "no": dict_node["child_id"],
                    "name": dict_node["child_name"],
                    "subCategory": n_subCategory,
                    "count_unit": EUnit.ITEM,
                    "count": 1,
                    "unit": dict_node["childUnit"],
                    "weight": dict_node["new_weight"],
                    "expectedLoss": dict_node["expectedLoss"],
                    "actualLoss": dict_node["actualLoss"],
                    "total_weight": dict_node["new_weight"],
                    #"process": dict_node["process"]#self.__convert_process(dict_node["process"]) # 改成bom的category
                }
        else:
            return {
                "category": EItemCategory.MA if dict_node[
                                                     'child_category'] == EBom2ChildCategory.MA else EItemCategory.AF,
                "no": dict_node["child_id"],
                "name": dict_node["child_name"],
                "subCategory": n_subCategory,
                "count_unit": EUnit.ITEM,
                "count": dict_node["count"],
                "unit": dict_node["childUnit"],
                "weight": dict_node["new_weight"],
                "total_weight": dict_node["count"] * dict_node["new_weight"],
                "unit2": dict_node["childUnit2"],
                "length": dict_node["length"],
                "expectedLoss": dict_node["expectedLoss"],
                "actualLoss": dict_node["actualLoss"],
                "total_length": dict_node["count"] * dict_node["length"]
            }

    def __get_material_info(self, obj_session, str_item_no):
        n_category = 0
        n_subCategory = 0
        n_unitWarehouse = 0
        n_unitProduct = 0
        obj_material = (
            obj_session.query(CTableMaterial)
            .filter(CTableMaterial.no == str_item_no)
            .first()
        )
        if obj_material:
            n_category = obj_material.category
            n_subCategory = obj_material.subCategory
            n_unitWarehouse = obj_material.unitWarehouse
            n_unitProduct = obj_material.unitProduct
        return n_category, n_subCategory, n_unitWarehouse, n_unitProduct

