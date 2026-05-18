# coding=utf8
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../..")
URL_PATH = '/api/v1'
URL_PATH_V0 = '/api/v0'
URL_PATH_DEVICE = '/'
from package.common.common import *

class TaiwanCity():
    OTHER = 0       # 其他
    TAIPEI = 1      # 台北
    NEW_TAIPEI = 2  # 新北
    TAOYUAN = 3     # 桃園
    TAICHUNG = 4    # 台中
    TAINAN = 5      # 台南
    KAOHSIUNG = 6   # 高雄
    KEELUNG = 7     # 基隆
    HSINCHU = 8     # 新竹
    MIAOLI = 9      # 苗栗
    CHANGHUA = 10   # 彰化
    NANTOU = 11     # 南投
    YUNLIN = 12     # 雲林
    CHIAYI = 13     # 嘉義
    PINGTUNG = 14   # 屏東
    YILAN = 15      # 宜蘭
    HUALIEN = 16    # 花蓮
    TAITUNG = 17    # 台東


def unit_to_string(n_value):
    # 創建數值到字串的映射
    unit_dict = {
        EUnit.NONE: "無",
        EUnit.GRAM: "公克",
        EUnit.TAIJIN: "台斤",
        EUnit.KILOGRAM: "公斤",
        EUnit.CM: "公分",
        EUnit.METER: "公尺",
        EUnit.PIECE: "顆",
        EUnit.ITEM: "個",
        EUnit.STRIP: "條",
        EUnit.SLICE: "片",
        EUnit.SHEET: "張",
        EUnit.CAN: "罐",
        EUnit.BAG: "包",
        EUnit.ROLL: "捲",
        EUnit.BARREL: "桶",
        EUnit.BOX: "盒",
        EUnit.SET: "組",
        EUnit.CASE: "箱",
        EUnit.ZHI: "支",
        EUnit.SHI: "式",
        EUnit.RU: "入",
        EUnit.UNIT: "配方"
    }

    # 返回對應的字串，如果沒有匹配則返回 "未知單位"
    return unit_dict.get(n_value, "未知單位")



