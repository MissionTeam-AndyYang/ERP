# coding=utf8
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../..')

from enum import IntEnum

ERROR_COMMON = 1000
ERROR_AUTH = 2000

SYSTEM_ID = "999999999999"

class EUnit():
    NONE = 0        # 無單位
    GRAM = 1        # 公克
    KILOGRAM = 2    # 公斤
    TAIJIN = 3      # 台斤
    
    CM = 51          # 公分 50
    METER = 52       # 公尺 51

    ITEM =  101       # 個
    STRIP = 102       # 條
    SLICE = 103       # 片
    SHEET = 104       # 張
    CAN = 105        # 罐
    BAG = 106        # 包
    ROLL = 107      # 捲
    BARREL = 108     # 桶
    BOX = 109        # 盒
    SET = 110        # 組
    CASE = 111       # 箱
    ZHI = 112        # 支
    SHI = 113       # 式
    RU = 114        # 入
    DE = 115        # 袋
    PIECE = 116       # 顆 110
    BOTTLE = 117       # 瓶
    UNIT = 150      #單位

    BAN = 201      # 板
    PCS = 202      # 件
    CAR = 203      # 車
    TIMES = 204   # 次

class EPrivilegeCategory(object):
    SALE = 1
    PURCHASE = 2
    PRODUCT = 3
    FINANCE = 4
    INVENTORY = 5


class EPrivilegeAction(object):
    VIEW = 1
    CREATION = 2
    MODIFICATION = 3
    CANCELLATION = 4
    REPORT = 5

class EErrorCode(object):
    ERROR_SUCCESS = 0
    ERROR_NO_MORE_ITEMS = 1
    ERROR_OTHER_ERROR = ERROR_COMMON + 1
    ERROR_PATH_NOT_FOUND = ERROR_COMMON + 2
    ERROR_DB = ERROR_COMMON + 3
    ERROR_NOT_SUPPORTED = 3

    ERROR_REGISTERNONOTFOUND = 2001
    ERROR_EMPLOYEENOTFOUND = 2002
    ERROR_INCORRECT_ACCOUNTPWD = 2003
    ERROR_INVAILD_TOKEN = 2101
    ERROR_PERMISSION_DENIED = 2202
    ERROR_INVAILD_PARAM = 3001
    ERROR_INVAILD_BODY = 3002

    ERROR_WAREHOUSE_NOT_FOUND = 5001
    ERROR_STOCK_NOT_ENOUGH = 5001

class EProcCategory(object):
    PREPROCESS = 1 #前備
    PROCESS = 2
    PACKAGE = 3

class EMaterialType(object):
    NONE = 0
    PM = 1 #原料
    MA = 2
    AF = 3

class EPaymentType(object):
    NOW = 0
    MONTH = 1

class EPaymentSource(object):
    CASH = 0
    TRANSFER = 1
    TICKET = 2

class EBomCategory(object):
    NONE = 0
    PM = 1 #原料
    MA_AP = 2 #物料

class EItemCategory(object): # itemCategory
    NONE = 0
    PM = 1 #原料
    MA = 2
    AF = 3
    INPRODUCT = 4
    PRODUCT = 5
    GOODS = 6

class EItemType():
    NONE = 0
    NEW = 1 #新料
    REMAINING = 2 #餘料
    WASTE = 3 #廢料


class EBatchOrderCategory(object): # itemCategory
    NONE = 0
    PURCHASE = 1 #採購
    PRODUCT = 2 #產製
    SALE_RETURN = 3 #銷貨退回


class EReuseCategory():
    NONE = 0
    REMAINING = 1 #餘料
    WASTE = 2 #廢料


class EInventoryOrderCategory(object):
    PURCHASE = 1 #採購
    SALE = 2
    RECEIVE = 3
    RETURN = 4
    REMAIN = 5
    WASTE = 6
    PRODUCT = 7
    REC = 8

class EInventoryCategory(object):
    IN = 1 #入庫
    OUT = 2


class EInventorySubCategory(object):
    SCRAPPED= 1 #報廢
    GIVEAWAY = 2 #贈品
    RD = 3
    OTHER = 4


class ELaborType(object):
    WORK = 1
    REST = 2
    CLEAN = 3


class EInventorySrc(object):
    PURCHASE_RECEIVE = 1  # 採購 / 領料
    RETURN_SALE = 2         # 退料 / 銷售
    REMAINING_PRETURN = 3    # 餘料 / 採購退回
    WASTE_WASTE = 4          # 廢料 / 報廢
    PRODUCT = 5              # 產品
    SRETURN = 6              # 銷售退回


class EOutputCategory(object):
    INPRODUCT = 1 #在製品
    PRODUCT = 2 #製成品

class EActionType(object):
    NONE = 0
    PURCHASE = 1 #採購
    WORK = 2 #製造
    SALE = 3 #銷售


class EDevAction():
    IN = 1        #入庫/入產
    OUT = 2     # 出庫/出產

class EBatchTraceRefCategory():
    NONE = 0
    PURCHASE = 1 #採購
    SALE = 2 #銷售

class EBatchNoCategory():
    PURCHASE = 1 #採購
    WORK = 2 #製造
    SALE = 3 #銷售

class EInventoryDeltaKind():
    NONE = 0
    MATERIAL = 1 #原物料
    INPRODUCT = 2 #在製品
    PRODUCT = 3 #製成品
    BATCHNO = 4 #批號


class EOrderStatisticKind():
    NONE = 0
    PURCHASE = 1 #採購
    PRODUCT = 2 #訂購
    SHIPPING = 3 #物流
    WAREHOUSE = 4 #倉儲
    EXPENSE = 5 #費用


class EBom1ChildCategory():
    NONE = 0
    PM = 1 #原料
    INPRODUCT = 2 #在製品

class EBom2ChildCategory():
    NONE = 0
    MA = 1 #物料
    AF = 2 #膠捲


class ELaborAction():
    NONE = 0
    WORK = 1 #工作
    REST = 2 #休息
    CLEAN = 3 #清潔

class ELaborSubAction():
    NONE = 0
    PRE = 1 #前段
    POST = 2 #後段

class EEmployeeType():
    NONE = 0
    FULL_TIME = 1 #全職
    PART_TIME = 2 #兼職

#Device
class ELocationType():
    STORAGE = 1        #倉庫
    PREPARING1 = 2     # 前備1
    PREPARING2 = 3     # 前備2
    PROCESSING = 4     # 加工
    PACKAGING = 5      # 包裝

class EProcessOrderCategory():
    NONE = 0
    RECEIVE = 1        #領料
    RETURN = 2     # 退料
    REMAIN = 3     # 餘料
    WASTE = 4     # 廢料
    PRODUCT = 5      # 產品

class EInputAction():
    NONE = 0
    RECEIVE = 1        #領料
    RETURN = 2     # 退料

class EOutputAction():
    NONE = 0
    WORK = 1        #產製


class EReuseAction():
    NONE = 0
    WORK = 1  # 產製


class EDevRefCategory:
    NONE = 0
    PURCHASE = 1  # 採購
    SALE = 2  # 訂購
    WORK = 3  # 產製
    OTHER = 4  # 其他

class EInventoryRefCategory:
    NONE = 0
    PURCHASE = 1  # 採購
    SALE = 2  # 訂購
    WORK = 3  # 產製
    OTHER = 4  # 其他

class EOrderPaymentRefCategory:
    NONE = 0
    PURCHASE = 1  # 採購
    SALE = 2  # 訂購
    EXPENSE = 3  # 費用
    OTHER = 4  # 其他

class EGoodsReceiptNoteCategory:
    NORMAL = 0 # 進貨
    RETURN = 1  # 退回

class EShippingOrderCategory:
    NORMAL = 0
    RETURN = 1  # 退回


class EARAPType():
    NONE = 0
    AR = 1 #應收
    AP = 2 #應付

class ETransItemCat():
    NONE = 0
    GOODS = 1 # 貨品
    MATERIAL = 2 #材料
    PRODUCT = 3  # 產品


class ETransItem2Cat():
    NONE = 0
    CONSUMABLES = 1  # 耗品
    EQUIPMENT = 2  # 設備
    # 工程
    # 其他
class EQuotationCat():
    NONE = 0
    PURCHASE = 1 #採購
    SALE = 2 #銷售

class EItemStyle():
    NONE = 0
    GOODS = 1 # 貨品
    PRODUCT = 2 #產品
    MATERIAL = 3 #材料
    CONSUMABLES = 4  # 耗品
    EQUIPMENT = 5  # 設備

class EBSType():
    NONE = 0
    # 入庫
    PURCHASE_IN_S = 1        #採購入庫; 進貨
    PRODUCT_IN_S = 2         #產製入庫; 餘/廢/產
    PRODUCT_RETURN_IN_S = 3  # 產製退回入庫; 收料
    SALE_IN_S = 4            # 銷售退回入庫
    OTHER_IN_S = 5           # 其他入庫 ?

    # 出庫
    PURCHASE_OUT_S = 11        # 採購退回出庫
    PRODUCT_OUT_S = 12         # 產製出庫; 發料
    SALE_OUT_S = 13            # 銷售出庫
    OTHER_OUT_S = 14           # 其他出庫 ?

    # 產間
    PRODUCT_IN_P = 21         #產製入產; 領料
    PRODUCT_OUT_P = 22        #產製出產; 餘/廢/產
    PRODUCT_RETURN_OUT_P = 22   #產製出產; 退料

class EDepartment():
    '''
1: 管理部
2: 行政部
3: 業務部
4: 製造部
5: 品保部
6: 生管部
7: 倉庫部
8: 總務部
9: 採購部
10: 研發部
11: 財務部

    '''
    MANAGEMENT= 1
    ADMINISTRATION= 2
    SALES=  3
    PRODUCTION=  4
    QA= 5
    PLANNING=  6
    WAREHOUSE=  7
    GENERAL_AFFAIRS=  8
    PURCHASING=  9
    RD=  10
    FINANCE=  11


class EShipWarehouseCat(object):
    SHIP = 1  #物流
    WAREHOUSE = 2 #倉儲

