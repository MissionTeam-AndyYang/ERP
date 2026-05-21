# coding=utf8
from package.util.util import *
from package.log.log import CLogger
from package.restserver.api.util import *
from sqlalchemy import case

class CContract(object):
    SALES, PURCHASE, PURCHASE_C, PURCHASE_E, SHIPPING, WAREHOUSE = 1, 2, 3, 4, 5, 6

    def __init__(self, n_type):
        self.__n_type = n_type
        # 配置表：{類型: (主表, 關聯項目表, Category, ItemStyle)}
        self.__obj_config = {
            self.SALES: (CTableContract, CTableTransItems, CTableQuotation, None, EQuotationCat.SALE, None),
            self.PURCHASE: (
                CTableContract, CTableTransItems, CTableQuotation, None, EQuotationCat.PURCHASE, [EItemStyle.GOODS, EItemStyle.MATERIAL]),
            self.PURCHASE_C: (CTableContract, CTableTransItems2, CTableQuotation, None, EQuotationCat.PURCHASE, [EItemStyle.CONSUMABLES]),
            self.PURCHASE_E: (CTableContract, CTableTransItems2, CTableQuotation, None, EQuotationCat.PURCHASE, [EItemStyle.EQUIPMENT]),
            self.SHIPPING: (CTableShipWarehouseContract, CTableShipWarehouse, CTableShipWarehouseQuotation, CTableShipWarehouseAlias, EShipWarehouseCat.SHIP, None),
            self.WAREHOUSE: (CTableShipWarehouseContract, CTableShipWarehouse, CTableShipWarehouseQuotation, CTableShipWarehouseAlias, EShipWarehouseCat.WAREHOUSE, None)
        }

    def get(self, n_start, n_count, dict_where):
        try:
            n_total = 0
            lst_result = []
            obj_cfg = self.__obj_config.get(self.__n_type)
            if obj_cfg:
                contract_table, item_table, quotation_table, alias_table, cat, styles = obj_cfg
                dict_where.update({"category": cat, "itemStyle": styles})

                with CDBMgr() as obj_dbmgr:
                    obj_session = obj_dbmgr.get_session()
                    lst_where = self.__fill_query_params(contract_table, dict_where)

                    # 1. 總數查詢
                    n_total = obj_session.query(contract_table).filter(*lst_where).count()

                    # 2. 一次 Join 完所有需要的 Table
                    # 基本回傳：主表、公司、支付方式
                    query = obj_session.query(contract_table, CTableCompany, CTablePayment, quotation_table)

                    # 動態加入項目表 (CTableTransItems / CTableTransItems2 / CTableShipWarehouse)
                    if item_table:
                        query = query.add_entity(item_table).outerjoin(item_table,
                                                                       contract_table.item_no == item_table.no)
                    # 動態加入alias表 (CTableShipWarehouseAlias)
                    if alias_table:
                        query = query.add_entity(alias_table).outerjoin(alias_table,
                                                                       contract_table.sw_alias_no == alias_table.no)

                    # 處理公司與支付的
                    query = (query.outerjoin(CTableCompany, contract_table.item_ref_no == CTableCompany.no)
                             .outerjoin(CTablePayment, CTablePayment.id == case(
                        (contract_table.category == self.PURCHASE, CTableCompany.received_id),
                        else_=CTableCompany.paid_id))
                             .outerjoin(quotation_table, contract_table.ref_no == quotation_table.no)
                             .filter(*lst_where)
                             .order_by(contract_table.date.desc()))

                    if n_count:
                        query = query.offset(n_start).limit(n_count)

                    # 3. 執行查詢並格式化結果
                    lst_result = [self._format_row(obj_session, obj_row) for obj_row in query.all()]
            return n_total, lst_result

        except Exception as error:
            CLogger().log(CLogger.LOG_LEVELERROR, f'[{self.__class__.__name__}] {error}')
            raise ValueError(f'throw exception (error: {error})')

    def _format_row(self, obj_session, row):
        # row 的結構會根據 add_entity 的數量動態變化
        # 基本：(main, company, payment, quotation, [item])
        contract, company, payment, quotation = row[0], row[1], row[2], row[3]
        obj_item = row[4] if len(row) > 4 else None
        obj_alias = row[5] if len(row) > 5 else None

        dict_data = object_as_dict(contract)
        dict_pay = object_as_dict(payment) if payment else {}

        # 處理特殊的 SALES
        if self.__n_type in [self.SALES, self.PURCHASE] and obj_item:
            name, cat, sub, _, _ = util_new_get_item_info(obj_item.item_no)
            dict_data["item"] = {"itemCategory": cat,
                                 "itemSubCategory": sub,
                                 "item_no": obj_item.item_no,
                                 "item_name": name}
            from datetime import datetime

            # 1. 將 Timestamp 轉換為 datetime 物件
            target_dt = datetime.fromtimestamp(dict_data["date"])

            # 2. 取得該月份的第一天
            first_day_of_month = target_dt.replace(day=1).date()

            # 3. 執行查詢
            price_query = (
                obj_session.query(CTableItemPrice)
                .filter(
                    CTableItemPrice.item_no == dict_data["item_no"],
                    # 資料庫日期 >= 目標月份第一天，即包含當月與未來月份
                    CTableItemPrice.date >= first_day_of_month
                )
                .order_by(CTableItemPrice.date.desc())

            )
            dict_data["itemPrice"] = {}
            for obj_price in price_query.all():
                str_month = obj_price.date.strftime("%Y/%m")
                dict_data["itemPrice"][str_month] = {
                    "unit": obj_price.whUnitLength if obj_price.whUnitLength else obj_price.whUnitWeight,
                    "price": obj_price.estWHPriceLength if obj_price.whUnitLength else obj_price.estWHPriceWeight }

        if self.__n_type in [self.SHIPPING, self.WAREHOUSE] and obj_alias:
            dict_data.update({
                "alias_no": obj_alias.no if obj_alias else 0,
                "aliasName": obj_alias.name if obj_alias else "",
            })
        # 直接使用從 SQL 帶回來的 obj_item，不再查詢資料庫
        dict_data.update({
            "transItemCategory": obj_item.category if obj_item else 0,
            "transItemAttr": obj_item.attribute if obj_item else 0,
            "paymentType": dict_pay.get("type", 0),
            "paymentDate": dict_pay.get("date", 0),
            "paymentPeriod": dict_pay.get("period", 0),
            "quotation_no": quotation.no if quotation else "",
            "quotationDate": quotation.date if quotation else 0,
            "unitWarehouse": get_item_unitWarehouse(dict_data["item_no"]) if dict_data.get("item_no") else 0
        })
        return dict_data

    def __fill_query_params(self, table, dict_where):
        lst_where = []
        t1 = dict_where.get("start_time")
        t2 = dict_where.get("end_time")

        # 1. 處理時間區間邏輯
        if t1 and t2:
            lst_where.append(table.date.between(t1, t2))
        elif t1:
            lst_where.append(table.date >= t1)  # 只有 start_time
        elif t2:
            lst_where.append(table.date <= t2)  # 只有 end_time

        # 2. 定義過濾映射表
        filter_map = {
            'item_no': lambda v: table.item_no == v,
            'category': lambda v: table.category == v,
            'itemStyle': lambda v: table.itemStyle.in_(v) if isinstance(v, (list, tuple)) else None
        }

        # 3. 遍歷其餘參數
        for k, v in dict_where.items():
            if k in filter_map and v is not None:
                obj_condition = filter_map[k](v)
                if obj_condition is not None:
                    lst_where.append(obj_condition)
        return lst_where

class CQuotation(object):
    SALES, PURCHASE, PURCHASE_C, PURCHASE_E, SHIPPING, WAREHOUSE = 1, 2, 3, 4, 5, 6

    def __init__(self, n_type):
        self.__n_type = n_type
        # 配置表：{類型: (主表, 關聯項目表, Category, ItemStyle)}
        self.__obj_config = {
            self.SALES: (CTableQuotation, CTableTransItems, EQuotationCat.SALE, None),
            self.PURCHASE: (
                CTableQuotation, CTableTransItems, EQuotationCat.PURCHASE, [EItemStyle.GOODS, EItemStyle.MATERIAL]),
            self.PURCHASE_C: (CTableQuotation, CTableTransItems2, EQuotationCat.PURCHASE, [EItemStyle.CONSUMABLES]),
            self.PURCHASE_E: (CTableQuotation, CTableTransItems2, EQuotationCat.PURCHASE, [EItemStyle.EQUIPMENT]),
            self.SHIPPING: (CTableShipWarehouseQuotation, CTableShipWarehouse, EShipWarehouseCat.SHIP, None),
            self.WAREHOUSE: (CTableShipWarehouseQuotation, CTableShipWarehouse, EShipWarehouseCat.WAREHOUSE, None)
        }

    def get(self, n_start, n_count, dict_where):
        try:
            n_total = 0
            lst_result = []
            obj_cfg = self.__obj_config.get(self.__n_type)
            if obj_cfg:
                quotation_table, item_table, cat, styles = obj_cfg
                dict_where.update({"category": cat, "itemStyle": styles})

                with CDBMgr() as obj_dbmgr:
                    obj_session = obj_dbmgr.get_session()
                    lst_where = self.__fill_query_params(quotation_table, dict_where)

                    # 1. 總數查詢 (維持在主表上 count 以確保效能)
                    n_total = obj_session.query(quotation_table).filter(*lst_where).count()

                    # 2. 構建「大寬表」查詢 (一次 Join 完所有需要的 Table)
                    # 基本回傳：主表、公司、支付方式
                    query = obj_session.query(quotation_table, CTableCompany, CTablePayment)

                    # 動態加入項目表 (CTableTransItems / CTableTransItems2 / CTableShipWarehouse)
                    if item_table:
                        query = query.add_entity(item_table).outerjoin(item_table,
                                                                       quotation_table.item_no == item_table.no)

                    # 處理公司與支付的 Join 邏輯 (區分一般報價與物流報價)
                    '''
                    com_join_col = item_table.company_no if self.__n_type in [self.SHIPPING,
                                                                              self.WAREHOUSE] else quotation_table.item_ref_no
                    '''
                    obj_col_company = quotation_table.item_ref_no
                    query = (query.outerjoin(CTableCompany, obj_col_company == CTableCompany.no)
                             .outerjoin(CTablePayment, CTablePayment.id == case(
                        (quotation_table.category == self.PURCHASE, CTableCompany.received_id),
                        else_=CTableCompany.paid_id))
                             .filter(*lst_where)
                             .order_by(quotation_table.date.desc()))

                    if n_count:
                        query = query.offset(n_start).limit(n_count)

                    # 3. 執行查詢並格式化結果 (此時 row 內已包含所有物件，不需再 query)
                    lst_result = [self._format_row(row) for row in query.all()]
            return n_total, lst_result

        except Exception as error:
            CLogger().log(CLogger.LOG_LEVELERROR, f'[{self.__class__.__name__}] {error}')
            raise ValueError(f'throw exception (error: {error})')

    def _format_row(self, row):
        # row 的結構會根據 add_entity 的數量動態變化
        # 基本：(main, company, payment, [item])
        quotation, company, payment = row[0], row[1], row[2]
        obj_item = row[3] if len(row) > 3 else None

        dict_data = object_as_dict(quotation)
        dict_pay = object_as_dict(payment) if payment else {}

        # 處理SALES
        if self.__n_type == self.SALES and obj_item and obj_item.category == ETransItemCat.PRODUCT:
            name, cat, sub, _, _ = util_new_get_item_info(obj_item.item_no)
            dict_data["item"] = {"itemCategory": cat, "itemSubCategory": sub, "item_no": obj_item.item_no,
                                 "item_name": name}

        # 直接使用從 SQL 帶回來的 obj_item，不再查詢資料庫
        dict_data.update({
            "transItemCategory": obj_item.category if obj_item else 0,
            "transItemAttr": obj_item.attribute if obj_item else 0,
            "paymentType": dict_pay.get("type", 0),
            "paymentDate": dict_pay.get("date", 0),
            "paymentPeriod": dict_pay.get("period", 0),
            "unitWarehouse": get_item_unitWarehouse(dict_data["item_no"]) if dict_data.get("item_no") else 0
        })
        return dict_data

    def __fill_query_params(self, table, dict_where):
        t1, t2 = dict_where.get("start_time"), dict_where.get("end_time")
        lst_where = [table.date.between(t1, t2)] if t1 and t2 else []
        filter_map = {
            'item_no': lambda v: table.item_no == v,
            'category': lambda v: table.category == v,
            'itemStyle': lambda v: table.itemStyle.in_(v) if isinstance(v, (list, tuple)) else None
        }
        for k, v in dict_where.items():
            if k in filter_map and v is not None:
                lst_where.append(filter_map[k](v))
        return lst_where


