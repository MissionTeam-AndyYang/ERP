# coding=utf8
import sys
import time
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


RESTSERVER_ROOT = Path(__file__).resolve().parents[1]
if str(RESTSERVER_ROOT) not in sys.path:
    sys.path.insert(0, str(RESTSERVER_ROOT))

from package.common.common import EDataQualityCode, EItemCategory, EPaymentSource, EPaymentType, ETransItemTypeCode
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
from package.restserver.api.v2.transitems import CTransItemsMasterService


def build_session():
    obj_engine = create_engine("sqlite:///:memory:")
    for obj_table in [
        CTablePayment.__table__,
        CTableCompany.__table__,
        CTableTransItems.__table__,
        CTableContract.__table__,
        CTableMaterial.__table__,
        CTableInproduct.__table__,
        CTableProduct.__table__,
        CTableGoods.__table__,
    ]:
        obj_table.create(bind=obj_engine)
    return sessionmaker(bind=obj_engine)()


def seed_transitems(obj_session):
    n_now = int(time.time())
    obj_session.add_all([
        CTablePayment(id=1, type=EPaymentType.MONTH, source=EPaymentSource.TRANSFER, date=25, period=30, creationTime=n_now),
        CTablePayment(id=2, type=EPaymentType.NOW, source=EPaymentSource.CASH, date=0, period=0, creationTime=n_now),
        CTableCompany(
            no="CUST-001",
            businessNo="12345678",
            displayName="測試客戶",
            name="測試客戶股份有限公司",
            address="台北市",
            phone="02-11111111",
            contactName="王小明",
            contactPhone={"mobile": "0912000000"},
            contactTitle="採購",
            contactEmail="buyer@example.com",
            received_id=1,
            paid_id=2,
            creationTime=n_now,
        ),
        CTableMaterial(
            no="RM-001",
            category=EItemCategory.PM,
            subCategory=11,
            name="原料A",
            unitWarehouse=3,
            creationTime=n_now,
        ),
        CTableTransItems(
            no="TI-001",
            name="交易原料A",
            category=1,
            attribute=2,
            company_no="CUST-001",
            company_displayName="測試客戶",
            item_no="RM-001",
            item_name="原料A",
            comment="交易備註",
            creationTime=n_now,
        ),
        CTableTransItems(
            no="TI-MISSING",
            name="缺料品交易品項",
            category=1,
            attribute=1,
            company_no="CUST-001",
            company_displayName="測試客戶",
            item_no="",
            item_name="",
            creationTime=n_now,
        ),
        CTableContract(
            no="CON-001",
            date=n_now,
            displayName="測試合約",
            category=1,
            type=2,
            item_no="TI-001",
            item_name="交易原料A",
            itemCategory=EItemCategory.PM,
            item_ref_no="CUST-001",
            item_ref_displayName="測試客戶",
            unit=3,
            price=12.34567,
            shippingPrice=1.23456,
            unitConversion=2.5,
            creationTime=n_now,
        ),
    ])
    obj_session.commit()


def test_transitems_dashboard_returns_confirmed_fields():
    obj_session = build_session()
    seed_transitems(obj_session)
    dict_payload = CTransItemsMasterService()._CTransItemsMasterService__get_dashboard_with_session(
        obj_session, "", "", "", 0, False, False, 0, 50,
    )

    assert dict_payload["summary"]["companyCount"] == 1
    assert dict_payload["summary"]["customerCount"] == 0
    assert dict_payload["summary"]["supplierCount"] == 1
    assert dict_payload["summary"]["transItemCount"] == 2
    assert dict_payload["summary"]["linkedItemCount"] == 1
    assert dict_payload["summary"]["contractLinkedTransItemCount"] == 1
    assert "dataQualityIssueCount" not in dict_payload["summary"]
    assert dict_payload["summary"]["companyDataQualityIssueCount"] == 0
    assert dict_payload["summary"]["transItemDataQualityIssueCount"] == 1
    assert dict_payload["companies"][0]["receivablePayment"]["paymentTypeCode"] == "monthly"
    assert dict_payload["companies"][0]["receivablePayment"]["paymentSource"] == EPaymentSource.TRANSFER
    dict_rows = {dict_row["transItemNo"]: dict_row for dict_row in dict_payload["transactionItems"]}
    assert dict_rows["TI-001"]["transItemType"] == ETransItemTypeCode.TRANS_ITEMS
    assert dict_rows["TI-001"]["tradePrice"] == 12.3457
    assert dict_rows["TI-001"]["shippingPrice"] == 1.2346
    assert dict_rows["TI-001"]["itemCategory"] == EItemCategory.PM
    assert dict_rows["TI-MISSING"]["dataQualityCode"] == EDataQualityCode.MISSING_LINKED_ITEM


def test_transitems_dashboard_keyword_searches_contract_no():
    obj_session = build_session()
    seed_transitems(obj_session)
    dict_payload = CTransItemsMasterService()._CTransItemsMasterService__get_dashboard_with_session(
        obj_session, "CON-001", "", "", 0, False, False, 0, 50,
    )

    assert dict_payload["total"] == 1
    assert dict_payload["transactionItems"][0]["transItemNo"] == "TI-001"


def test_transitems_dashboard_filters_has_contract():
    obj_session = build_session()
    seed_transitems(obj_session)
    dict_payload = CTransItemsMasterService()._CTransItemsMasterService__get_dashboard_with_session(
        obj_session, "", "", "", 0, False, True, 0, 50,
    )

    assert dict_payload["total"] == 1
    assert dict_payload["transactionItems"][0]["transItemNo"] == "TI-001"


def test_transitems_company_detail_returns_payments_items_and_contracts():
    obj_session = build_session()
    seed_transitems(obj_session)
    dict_payload = CTransItemsMasterService()._CTransItemsMasterService__get_company_detail_with_session(
        obj_session, "CUST-001",
    )

    assert dict_payload["company"]["companyNo"] == "CUST-001"
    assert dict_payload["company"]["contactPhone"] == "0912000000"
    assert dict_payload["company"]["payablePayment"]["paymentTypeCode"] == "cash"
    assert len(dict_payload["transactionItems"]) == 2
    assert dict_payload["contracts"][0]["contractNo"] == "CON-001"
    assert dict_payload["contracts"][0]["transItemNo"] == "TI-001"


def test_transitems_trans_item_detail_returns_contracts_and_linked_items():
    obj_session = build_session()
    seed_transitems(obj_session)
    dict_payload = CTransItemsMasterService()._CTransItemsMasterService__get_trans_item_detail_with_session(
        obj_session, "TI-001",
    )

    assert dict_payload["transItem"]["transItemNo"] == "TI-001"
    assert dict_payload["transItem"]["companyDisplayName"] == "測試客戶"
    assert dict_payload["transItem"]["dataQualityCode"] == EDataQualityCode.READY
    assert dict_payload["contracts"][0]["tradePrice"] == 12.3457
    assert dict_payload["linkedItems"][0]["itemNo"] == "RM-001"
    assert dict_payload["linkedItems"][0]["unitWarehouse"] == 3


def test_transitems_detail_not_found_returns_none():
    obj_session = build_session()
    seed_transitems(obj_session)
    dict_payload = CTransItemsMasterService()._CTransItemsMasterService__get_trans_item_detail_with_session(
        obj_session, "NOT-FOUND",
    )

    assert dict_payload is None
