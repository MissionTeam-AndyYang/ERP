# coding=utf8
import time
from collections import defaultdict

from flask import request
from sqlalchemy import or_

from package.common.common import (
    EDataQualityCode,
    EErrorCode,
    EItemCategory,
    EPaymentType,
    EPaymentTypeCode,
    ETransItemTypeCode,
)
from package.dbwrapper.dbmgr import CDBMgr
from package.dbwrapper.table import (
    CTableCompany,
    CTableContract,
    CTableGoods,
    CTableInproduct,
    CTableMaterial,
    CTablePayment,
    CTableProduct,
    CTableTransItems,
)
from package.log.log import CLogger
from package.util.util import util_round_price, util_safe_float, util_safe_int


class CTransItemsMasterService(object):
    def get_dashboard(
        self,
        str_keyword="",
        str_company_no="",
        str_trans_item_type="",
        n_trans_item_category=0,
        b_has_linked_item=False,
        b_has_contract=False,
        n_start=0,
        n_count=50,
    ):
        with CDBMgr() as obj_dbmgr:
            return self.__get_dashboard_with_session(
                obj_dbmgr.get_session(),
                str_keyword,
                str_company_no,
                str_trans_item_type,
                n_trans_item_category,
                b_has_linked_item,
                b_has_contract,
                n_start,
                n_count,
            )

    def get_company_detail(self, str_company_no):
        with CDBMgr() as obj_dbmgr:
            return self.__get_company_detail_with_session(obj_dbmgr.get_session(), str_company_no)

    def get_trans_item_detail(self, str_trans_item_no):
        with CDBMgr() as obj_dbmgr:
            return self.__get_trans_item_detail_with_session(obj_dbmgr.get_session(), str_trans_item_no)

    def __get_dashboard_with_session(
        self,
        obj_session,
        str_keyword,
        str_company_no,
        str_trans_item_type,
        n_trans_item_category,
        b_has_linked_item,
        b_has_contract,
        n_start,
        n_count,
    ):
        n_start, n_count = self.__normalize_page(n_start, n_count)
        obj_query = self.__build_trans_items_query(
            obj_session,
            str_keyword,
            str_company_no,
            str_trans_item_type,
            n_trans_item_category,
            b_has_linked_item,
            b_has_contract,
        )
        n_total = obj_query.count()
        lst_page_items = (
            obj_query.order_by(CTableTransItems.category.asc(), CTableTransItems.no.asc())
            .offset(n_start)
            .limit(n_count)
            .all()
        )
        lst_summary_refs = self.__query_trans_item_summary_refs(obj_query)
        lst_company_nos = self.__clean_list([obj_row.company_no for obj_row in lst_summary_refs])
        lst_trans_item_nos = self.__clean_list([obj_row.no for obj_row in lst_summary_refs])
        dict_companies = self.__query_companies_by_no(obj_session, lst_company_nos)
        dict_contracts = self.__query_contracts_by_trans_item_no(obj_session, lst_trans_item_nos)
        dict_items = self.__query_linked_items(obj_session, self.__clean_list([obj_row.item_no for obj_row in lst_page_items]))
        dict_payments = self.__query_payments_for_companies(obj_session, dict_companies.values())

        lst_company_rows = self.__build_company_rows(
            dict_companies,
            lst_summary_refs,
            dict_contracts,
            dict_payments,
        )
        lst_trans_item_rows = [
            self.__build_trans_item_row(
                obj_row,
                dict_companies.get(obj_row.company_no or ""),
                self.__latest_contract(dict_contracts.get(obj_row.no or "", [])),
                dict_items,
            )
            for obj_row in lst_page_items
        ]
        return {
            "serverTimestamp": util_safe_int(time.time()),
            "summary": self.__build_summary(lst_company_rows, lst_summary_refs, dict_contracts),
            "companies": lst_company_rows,
            "transactionItems": lst_trans_item_rows,
            "total": n_total,
            "start": n_start,
            "count": len(lst_trans_item_rows),
        }

    def __get_company_detail_with_session(self, obj_session, str_company_no):
        str_company_no = (str_company_no or "").strip()
        if not str_company_no:
            return None
        obj_company = obj_session.query(CTableCompany).filter(CTableCompany.no == str_company_no).first()
        if not obj_company:
            return None
        lst_trans_items = (
            obj_session.query(CTableTransItems)
            .filter(CTableTransItems.company_no == str_company_no)
            .order_by(CTableTransItems.category.asc(), CTableTransItems.no.asc())
            .all()
        )
        lst_trans_item_nos = self.__clean_list([obj_row.no for obj_row in lst_trans_items])
        dict_contracts = self.__query_contracts_by_trans_item_no(obj_session, lst_trans_item_nos)
        dict_payment = self.__query_payments_by_id(obj_session, [obj_company.received_id, obj_company.paid_id])
        return {
            "serverTimestamp": util_safe_int(time.time()),
            "company": self.__build_company_detail(obj_company, dict_payment),
            "transactionItems": [
                self.__build_company_trans_item_row(obj_row, self.__latest_contract(dict_contracts.get(obj_row.no or "", [])))
                for obj_row in lst_trans_items
            ],
            "contracts": [
                self.__build_contract_row(obj_contract)
                for obj_contract in self.__flatten_contracts(dict_contracts)
            ],
        }

    def __get_trans_item_detail_with_session(self, obj_session, str_trans_item_no):
        str_trans_item_no = (str_trans_item_no or "").strip()
        if not str_trans_item_no:
            return None
        obj_trans_item = obj_session.query(CTableTransItems).filter(CTableTransItems.no == str_trans_item_no).first()
        if not obj_trans_item:
            return None
        obj_company = None
        if obj_trans_item.company_no:
            obj_company = obj_session.query(CTableCompany).filter(CTableCompany.no == obj_trans_item.company_no).first()
        lst_contracts = self.__query_contracts_by_trans_item_no(obj_session, [str_trans_item_no]).get(str_trans_item_no, [])
        dict_items = self.__query_linked_items(obj_session, [obj_trans_item.item_no])
        return {
            "serverTimestamp": util_safe_int(time.time()),
            "transItem": self.__build_trans_item_detail(obj_trans_item, obj_company, lst_contracts, dict_items),
            "contracts": [self.__build_trans_item_contract_row(obj_contract) for obj_contract in lst_contracts],
            "linkedItems": self.__build_linked_items(obj_trans_item, dict_items),
        }

    def __build_trans_items_query(
        self,
        obj_session,
        str_keyword,
        str_company_no,
        str_trans_item_type,
        n_trans_item_category,
        b_has_linked_item,
        b_has_contract,
    ):
        obj_query = obj_session.query(CTableTransItems)
        if str_trans_item_type and str_trans_item_type != ETransItemTypeCode.TRANS_ITEMS:
            return obj_query.filter(CTableTransItems.no == None)
        if str_company_no:
            obj_query = obj_query.filter(CTableTransItems.company_no == str_company_no)
        if n_trans_item_category:
            obj_query = obj_query.filter(CTableTransItems.category == n_trans_item_category)
        if b_has_linked_item:
            obj_query = obj_query.filter(CTableTransItems.item_no.isnot(None), CTableTransItems.item_no != "")
        str_keyword = (str_keyword or "").strip()
        if str_keyword:
            str_like = "%%%s%%" % str_keyword
            lst_contract_item_nos = [
                obj_row.item_no
                for obj_row in obj_session.query(CTableContract.item_no)
                .filter(or_(CTableContract.no.ilike(str_like), CTableContract.displayName.ilike(str_like)))
                .all()
                if obj_row.item_no
            ]
            lst_conditions = [
                CTableTransItems.no.ilike(str_like),
                CTableTransItems.name.ilike(str_like),
                CTableTransItems.company_no.ilike(str_like),
                CTableTransItems.company_displayName.ilike(str_like),
                CTableTransItems.item_no.ilike(str_like),
                CTableTransItems.item_name.ilike(str_like),
            ]
            if lst_contract_item_nos:
                lst_conditions.append(CTableTransItems.no.in_(self.__clean_list(lst_contract_item_nos)))
            obj_query = obj_query.filter(or_(*lst_conditions))
        if b_has_contract:
            obj_contract_query = obj_session.query(CTableContract.item_no).filter(CTableContract.item_no.isnot(None), CTableContract.item_no != "")
            obj_query = obj_query.filter(CTableTransItems.no.in_(obj_contract_query))
        return obj_query

    def __query_trans_item_summary_refs(self, obj_query):
        return obj_query.with_entities(
            CTableTransItems.no.label("no"),
            CTableTransItems.company_no.label("company_no"),
            CTableTransItems.item_no.label("item_no"),
        ).all()

    def __query_companies_by_no(self, obj_session, lst_company_nos):
        lst_company_nos = self.__clean_list(lst_company_nos)
        if not lst_company_nos:
            return {}
        return {
            obj_row.no or "": obj_row
            for obj_row in obj_session.query(CTableCompany).filter(CTableCompany.no.in_(lst_company_nos)).all()
        }

    def __query_contracts_by_trans_item_no(self, obj_session, lst_trans_item_nos):
        lst_trans_item_nos = self.__clean_list(lst_trans_item_nos)
        if not lst_trans_item_nos:
            return {}
        lst_rows = (
            obj_session.query(CTableContract)
            .filter(CTableContract.item_no.in_(lst_trans_item_nos))
            .order_by(CTableContract.item_no.asc(), CTableContract.date.desc(), CTableContract.creationTime.desc(), CTableContract.no.asc())
            .all()
        )
        dict_result = defaultdict(list)
        for obj_row in lst_rows:
            dict_result[obj_row.item_no or ""].append(obj_row)
        return dict_result

    def __query_linked_items(self, obj_session, lst_item_nos):
        lst_item_nos = self.__clean_list(lst_item_nos)
        if not lst_item_nos:
            return {}
        dict_result = {}
        for obj_row in obj_session.query(CTableMaterial).filter(CTableMaterial.no.in_(lst_item_nos)).all():
            dict_result[obj_row.no or ""] = self.__item_dict(obj_row, util_safe_int(obj_row.category), 0, obj_row.unitWarehouse)
        for obj_row in obj_session.query(CTableInproduct).filter(CTableInproduct.no.in_(lst_item_nos)).all():
            dict_result[obj_row.no or ""] = self.__item_dict(obj_row, EItemCategory.INPRODUCT, util_safe_int(obj_row.category), obj_row.unitWarehouse)
        for obj_row in obj_session.query(CTableProduct).filter(CTableProduct.no.in_(lst_item_nos)).all():
            dict_result[obj_row.no or ""] = self.__item_dict(obj_row, EItemCategory.PRODUCT, util_safe_int(obj_row.category), obj_row.unitWarehouse)
        for obj_row in obj_session.query(CTableGoods).filter(CTableGoods.no.in_(lst_item_nos)).all():
            dict_result[obj_row.no or ""] = self.__item_dict(obj_row, EItemCategory.GOODS, util_safe_int(obj_row.subCategory), obj_row.unitWarehouse)
        return dict_result

    def __query_payments_for_companies(self, obj_session, lst_companies):
        lst_payment_ids = []
        for obj_company in lst_companies:
            lst_payment_ids.extend([obj_company.received_id, obj_company.paid_id])
        return self.__query_payments_by_id(obj_session, lst_payment_ids)

    def __query_payments_by_id(self, obj_session, lst_payment_ids):
        lst_payment_ids = [util_safe_int(n_id) for n_id in lst_payment_ids if util_safe_int(n_id)]
        if not lst_payment_ids:
            return {}
        return {
            util_safe_int(obj_row.id): obj_row
            for obj_row in obj_session.query(CTablePayment).filter(CTablePayment.id.in_(lst_payment_ids)).all()
        }

    def __build_company_rows(self, dict_companies, lst_trans_items, dict_contracts, dict_payments):
        dict_trans_count = defaultdict(int)
        dict_contract_count = defaultdict(int)
        for obj_row in lst_trans_items:
            if obj_row.company_no:
                dict_trans_count[obj_row.company_no] += 1
        for lst_contracts in dict_contracts.values():
            for obj_contract in lst_contracts:
                if obj_contract.item_ref_no:
                    dict_contract_count[obj_contract.item_ref_no] += 1
        return [
            {
                "companyNo": obj_company.no or "",
                "companyDisplayName": obj_company.displayName or "",
                "companyName": obj_company.name or "",
                "businessNo": obj_company.businessNo or "",
                "transItemCount": util_safe_int(dict_trans_count.get(obj_company.no or "")),
                "contractCount": util_safe_int(dict_contract_count.get(obj_company.no or "")),
                "contactName": obj_company.contactName or "",
                "contactPhone": self.__contact_phone(obj_company.contactPhone),
                "receivablePayment": self.__payment_dict(dict_payments.get(util_safe_int(obj_company.received_id))),
                "payablePayment": self.__payment_dict(dict_payments.get(util_safe_int(obj_company.paid_id))),
                "dataQualityCode": self.__company_data_quality_code(obj_company),
            }
            for obj_company in sorted(dict_companies.values(), key=lambda obj_row: obj_row.no or "")
        ]

    def __build_summary(self, lst_company_rows, lst_trans_items, dict_contracts):
        n_linked_count = len([obj_row for obj_row in lst_trans_items if obj_row.item_no])
        n_contract_linked_count = len([obj_row for obj_row in lst_trans_items if dict_contracts.get(obj_row.no or "")])
        n_company_data_quality_issue_count = len([
            dict_row for dict_row in lst_company_rows
            if dict_row.get("dataQualityCode") != EDataQualityCode.READY
        ])
        n_trans_item_data_quality_issue_count = len([
            obj_row for obj_row in lst_trans_items
            if self.__trans_item_data_quality_code(obj_row, dict_contracts.get(obj_row.no or "", [])) != EDataQualityCode.READY
        ])
        set_customer_company_nos = set()
        set_supplier_company_nos = set()
        for lst_contracts in dict_contracts.values():
            for obj_contract in lst_contracts:
                str_company_no = obj_contract.item_ref_no or ""
                if not str_company_no:
                    continue
                if util_safe_int(obj_contract.category) == 2:
                    set_customer_company_nos.add(str_company_no)
                elif util_safe_int(obj_contract.category) == 1:
                    set_supplier_company_nos.add(str_company_no)
        return {
            "companyCount": len(lst_company_rows),
            "customerCount": len(set_customer_company_nos),
            "supplierCount": len(set_supplier_company_nos),
            "transItemCount": len(lst_trans_items),
            "linkedItemCount": n_linked_count,
            "contractLinkedTransItemCount": n_contract_linked_count,
            "companyDataQualityIssueCount": n_company_data_quality_issue_count,
            "transItemDataQualityIssueCount": n_trans_item_data_quality_issue_count,
        }

    def __build_trans_item_row(self, obj_trans_item, obj_company, obj_contract, dict_items):
        dict_item = dict_items.get(obj_trans_item.item_no or "", {})
        return {
            "transItemNo": obj_trans_item.no or "",
            "transItemName": obj_trans_item.name or "",
            "transItemType": ETransItemTypeCode.TRANS_ITEMS,
            "transItemCategory": util_safe_int(obj_trans_item.category),
            "transItemAttribute": util_safe_int(obj_trans_item.attribute),
            "companyNo": obj_trans_item.company_no or getattr(obj_company, "no", "") or "",
            "companyDisplayName": obj_trans_item.company_displayName or getattr(obj_company, "displayName", "") or "",
            "itemNo": obj_trans_item.item_no or "",
            "itemName": obj_trans_item.item_name or dict_item.get("itemName", ""),
            "itemCategory": util_safe_int(dict_item.get("itemCategory") or getattr(obj_contract, "itemCategory", 0)),
            "contractNo": getattr(obj_contract, "no", "") or "",
            "contractCategory": util_safe_int(getattr(obj_contract, "category", 0)),
            "contractType": util_safe_int(getattr(obj_contract, "type", 0)),
            "tradeUnit": util_safe_int(getattr(obj_contract, "unit", 0)),
            "tradePrice": util_round_price(getattr(obj_contract, "price", 0)),
            "shippingPrice": util_round_price(getattr(obj_contract, "shippingPrice", 0)),
            "unitConversion": util_safe_float(getattr(obj_contract, "unitConversion", 0)),
            "dataQualityCode": self.__trans_item_data_quality_code(obj_trans_item, [obj_contract] if obj_contract else []),
        }

    def __build_company_detail(self, obj_company, dict_payment):
        return {
            "companyNo": obj_company.no or "",
            "businessNo": obj_company.businessNo or "",
            "companyDisplayName": obj_company.displayName or "",
            "companyName": obj_company.name or "",
            "address": obj_company.address or "",
            "phone": obj_company.phone or "",
            "contactName": obj_company.contactName or "",
            "contactPhone": self.__contact_phone(obj_company.contactPhone),
            "contactTitle": obj_company.contactTitle or "",
            "contactEmail": obj_company.contactEmail or "",
            "receivablePayment": self.__payment_dict(dict_payment.get(util_safe_int(obj_company.received_id))),
            "payablePayment": self.__payment_dict(dict_payment.get(util_safe_int(obj_company.paid_id))),
            "dataQualityCode": self.__company_data_quality_code(obj_company),
        }

    def __build_company_trans_item_row(self, obj_trans_item, obj_contract):
        return {
            "transItemNo": obj_trans_item.no or "",
            "transItemName": obj_trans_item.name or "",
            "transItemType": ETransItemTypeCode.TRANS_ITEMS,
            "transItemCategory": util_safe_int(obj_trans_item.category),
            "transItemAttribute": util_safe_int(obj_trans_item.attribute),
            "itemNo": obj_trans_item.item_no or "",
            "itemName": obj_trans_item.item_name or "",
            "contractNo": getattr(obj_contract, "no", "") or "",
            "tradeUnit": util_safe_int(getattr(obj_contract, "unit", 0)),
            "tradePrice": util_round_price(getattr(obj_contract, "price", 0)),
            "dataQualityCode": self.__trans_item_data_quality_code(obj_trans_item, [obj_contract] if obj_contract else []),
        }

    def __build_contract_row(self, obj_contract):
        return {
            "contractNo": obj_contract.no or "",
            "contractDisplayName": obj_contract.displayName or "",
            "contractCategory": util_safe_int(obj_contract.category),
            "contractType": util_safe_int(obj_contract.type),
            "effectiveDate": util_safe_int(obj_contract.date),
            "transItemNo": obj_contract.item_no or "",
            "transItemName": obj_contract.item_name or "",
        }

    def __build_trans_item_detail(self, obj_trans_item, obj_company, lst_contracts, dict_items):
        obj_contract = self.__latest_contract(lst_contracts)
        dict_item = dict_items.get(obj_trans_item.item_no or "", {})
        return {
            "transItemNo": obj_trans_item.no or "",
            "transItemName": obj_trans_item.name or "",
            "transItemType": ETransItemTypeCode.TRANS_ITEMS,
            "transItemCategory": util_safe_int(obj_trans_item.category),
            "transItemAttribute": util_safe_int(obj_trans_item.attribute),
            "companyNo": obj_trans_item.company_no or getattr(obj_company, "no", "") or "",
            "companyDisplayName": obj_trans_item.company_displayName or getattr(obj_company, "displayName", "") or "",
            "itemNo": obj_trans_item.item_no or "",
            "itemName": obj_trans_item.item_name or dict_item.get("itemName", ""),
            "itemCategory": util_safe_int(dict_item.get("itemCategory") or getattr(obj_contract, "itemCategory", 0)),
            "comment": obj_trans_item.comment or "",
            "creationTime": util_safe_int(obj_trans_item.creationTime),
            "dataQualityCode": self.__trans_item_data_quality_code(obj_trans_item, lst_contracts),
        }

    def __build_trans_item_contract_row(self, obj_contract):
        return {
            "contractNo": obj_contract.no or "",
            "contractDisplayName": obj_contract.displayName or "",
            "contractCategory": util_safe_int(obj_contract.category),
            "contractType": util_safe_int(obj_contract.type),
            "tradeUnit": util_safe_int(obj_contract.unit),
            "tradePrice": util_round_price(obj_contract.price),
            "shippingPrice": util_round_price(obj_contract.shippingPrice),
            "unitConversion": util_safe_float(obj_contract.unitConversion),
            "effectiveDate": util_safe_int(obj_contract.date),
        }

    def __build_linked_items(self, obj_trans_item, dict_items):
        dict_item = dict_items.get(obj_trans_item.item_no or "")
        if not dict_item:
            return []
        return [dict_item]

    def __item_dict(self, obj_row, n_item_category, n_sub_category, n_unit_warehouse):
        return {
            "itemNo": obj_row.no or "",
            "itemName": obj_row.name or "",
            "itemCategory": util_safe_int(n_item_category),
            "unitWarehouse": util_safe_int(n_unit_warehouse),
        }

    def __payment_dict(self, obj_payment):
        return {
            "paymentTypeCode": self.__payment_type_code(obj_payment),
            "paymentDate": util_safe_int(getattr(obj_payment, "date", 0)),
            "paymentPeriod": util_safe_int(getattr(obj_payment, "period", 0)),
            "paymentSource": util_safe_int(getattr(obj_payment, "source", 0)),
        }

    def __payment_type_code(self, obj_payment):
        if not obj_payment:
            return EPaymentTypeCode.UNKNOWN
        if util_safe_int(obj_payment.type) == EPaymentType.MONTH:
            return EPaymentTypeCode.MONTHLY
        if util_safe_int(obj_payment.type) == EPaymentType.NOW:
            return EPaymentTypeCode.CASH
        return EPaymentTypeCode.UNKNOWN

    def __company_data_quality_code(self, obj_company):
        if not obj_company:
            return EDataQualityCode.MISSING_COMPANY
        if not obj_company.received_id and not obj_company.paid_id:
            return EDataQualityCode.MISSING_PAYMENT_TERMS
        if not obj_company.contactName and not obj_company.contactPhone:
            return EDataQualityCode.UNKNOWN
        return EDataQualityCode.READY

    def __trans_item_data_quality_code(self, obj_trans_item, lst_contracts):
        if not obj_trans_item.company_no:
            return EDataQualityCode.MISSING_COMPANY
        if not obj_trans_item.item_no:
            return EDataQualityCode.MISSING_LINKED_ITEM
        if not lst_contracts or not self.__latest_contract(lst_contracts) or util_safe_float(self.__latest_contract(lst_contracts).price) <= 0:
            return EDataQualityCode.MISSING_CONTRACT_PRICE
        return EDataQualityCode.READY

    def __latest_contract(self, lst_contracts):
        if not lst_contracts:
            return None
        return sorted(lst_contracts, key=lambda obj_row: (util_safe_int(obj_row.date), util_safe_int(obj_row.creationTime), obj_row.no or ""), reverse=True)[0]

    def __flatten_contracts(self, dict_contracts):
        lst_result = []
        for lst_contracts in dict_contracts.values():
            lst_result.extend(lst_contracts)
        return sorted(lst_result, key=lambda obj_row: (obj_row.item_no or "", -util_safe_int(obj_row.date), obj_row.no or ""))

    def __contact_phone(self, obj_contact_phone):
        if isinstance(obj_contact_phone, list):
            return str(obj_contact_phone[0]) if obj_contact_phone else ""
        if isinstance(obj_contact_phone, dict):
            for str_key in ["phone", "mobile", "value", "number"]:
                if obj_contact_phone.get(str_key):
                    return str(obj_contact_phone.get(str_key))
            return ""
        return str(obj_contact_phone or "")

    def __clean_list(self, lst_values):
        return list({str_value for str_value in lst_values if str_value})

    def __normalize_page(self, n_start, n_count):
        n_start = max(util_safe_int(n_start), 0)
        n_count = min(max(util_safe_int(n_count), 1), 100)
        return n_start, n_count


class CTransItemsDashboard(object):
    def get(self, str_timezone="", str_id=""):
        str_message = "success"
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}
        try:
            dict_extra_data = CTransItemsMasterService().get_dashboard(
                str_keyword=request.args.get("keyword", "", type=str),
                str_company_no=request.args.get("companyNo", "", type=str),
                str_trans_item_type=request.args.get("transItemType", "", type=str),
                n_trans_item_category=request.args.get("transItemCategory", 0, type=int),
                b_has_linked_item=request.args.get("hasLinkedItem", "false", type=str).lower() == "true",
                b_has_contract=request.args.get("hasContract", "false", type=str).lower() == "true",
                n_start=request.args.get("start", 0, type=int),
                n_count=request.args.get("count", 50, type=int),
            )
        except Exception as obj_error:
            n_status_code = 400
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = "throw exception (error: %s)" % str(obj_error)
            CLogger().log(CLogger.LOG_LEVELERROR, "[CTransItemsDashboard] throw exception (error: %s)" % str(obj_error))
        return n_status_code, n_code, str_message, dict_extra_data


class CTransItemsCompanyDetail(object):
    def get(self, str_timezone="", str_id=""):
        str_message = "success"
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}
        try:
            dict_extra_data = CTransItemsMasterService().get_company_detail(str_id)
            if dict_extra_data is None:
                n_status_code = 400
                n_code = EErrorCode.ERROR_NO_MORE_ITEMS
                str_message = "record not found"
                dict_extra_data = {}
        except Exception as obj_error:
            n_status_code = 400
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = "throw exception (error: %s)" % str(obj_error)
            CLogger().log(CLogger.LOG_LEVELERROR, "[CTransItemsCompanyDetail] throw exception (error: %s)" % str(obj_error))
        return n_status_code, n_code, str_message, dict_extra_data


class CTransItemsTransItemDetail(object):
    def get(self, str_timezone="", str_id=""):
        str_message = "success"
        n_status_code = 200
        n_code = EErrorCode.ERROR_SUCCESS
        dict_extra_data = {}
        try:
            dict_extra_data = CTransItemsMasterService().get_trans_item_detail(str_id)
            if dict_extra_data is None:
                n_status_code = 400
                n_code = EErrorCode.ERROR_NO_MORE_ITEMS
                str_message = "record not found"
                dict_extra_data = {}
        except Exception as obj_error:
            n_status_code = 400
            n_code = EErrorCode.ERROR_OTHER_ERROR
            str_message = "throw exception (error: %s)" % str(obj_error)
            CLogger().log(CLogger.LOG_LEVELERROR, "[CTransItemsTransItemDetail] throw exception (error: %s)" % str(obj_error))
        return n_status_code, n_code, str_message, dict_extra_data
