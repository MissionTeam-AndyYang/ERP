from __future__ import annotations

from datetime import date

from sqlalchemy import BigInteger, Date, Double, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Enterprise(Base):
    __tablename__ = "enterprise"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    no: Mapped[str] = mapped_column(String(60), nullable=False)
    businessNo: Mapped[str] = mapped_column(String(20), nullable=False)
    displayName: Mapped[str | None] = mapped_column(String(60), nullable=True)
    name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    address: Mapped[str | None] = mapped_column(String(100), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(100), nullable=True)
    fax: Mapped[str | None] = mapped_column(String(100), nullable=True)
    department: Mapped[int | None] = mapped_column(Integer, nullable=True)
    lar: Mapped[str | None] = mapped_column(String(100), nullable=True)
    comment: Mapped[str | None] = mapped_column(String(128), nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class Company(Base):
    __tablename__ = "company"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    no: Mapped[str] = mapped_column(String(60), nullable=False)
    businessNo: Mapped[str] = mapped_column(String(20), nullable=False)
    displayName: Mapped[str | None] = mapped_column(String(60), nullable=True)
    name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    address: Mapped[str | None] = mapped_column(String(60), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(60), nullable=True)
    fax: Mapped[str | None] = mapped_column(String(60), nullable=True)
    contactName: Mapped[str | None] = mapped_column(String(60), nullable=True)
    contactPhone: Mapped[str | None] = mapped_column(String(60), nullable=True)
    contactTitle: Mapped[str | None] = mapped_column(String(60), nullable=True)
    contactEmail: Mapped[str | None] = mapped_column(String(60), nullable=True)
    received_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("payment.id", name="fk_company_received_id"), nullable=True
    )
    paid_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("payment.id", name="fk_company_paid_id"), nullable=True
    )
    bankDisplayName: Mapped[str | None] = mapped_column(String(60), nullable=True)
    bankName: Mapped[str | None] = mapped_column(String(60), nullable=True)
    bankCurrency: Mapped[int | None] = mapped_column(Integer, nullable=True)
    bankBranch: Mapped[str | None] = mapped_column(String(60), nullable=True)
    bankAccount: Mapped[str | None] = mapped_column(String(60), nullable=True)
    bankNo: Mapped[str | None] = mapped_column(String(60), nullable=True)
    comment: Mapped[str | None] = mapped_column(String(128), nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class BankAccount(Base):
    __tablename__ = "bank_account"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    category: Mapped[int | None] = mapped_column(Integer, nullable=True)
    currency: Mapped[int | None] = mapped_column(Integer, nullable=True)
    displayName: Mapped[str | None] = mapped_column(String(60), nullable=True)
    name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    branch: Mapped[str | None] = mapped_column(String(60), nullable=True)
    account: Mapped[str | None] = mapped_column(String(60), nullable=True)
    number: Mapped[str] = mapped_column(String(60), nullable=False)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class Payment(Base):
    __tablename__ = "payment"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    source: Mapped[int] = mapped_column(Integer, nullable=False)
    date: Mapped[int] = mapped_column(Integer, nullable=False)
    period: Mapped[int] = mapped_column(Integer, nullable=False)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class Material(Base):
    __tablename__ = "material"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    no: Mapped[str] = mapped_column(String(20), nullable=False)
    category: Mapped[int | None] = mapped_column(Integer, nullable=True)
    subCategory: Mapped[int | None] = mapped_column(Integer, nullable=True)
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    unitShipping: Mapped[int | None] = mapped_column(Integer, nullable=True)
    unitWarehouse: Mapped[int | None] = mapped_column(Integer, nullable=True)
    unitProduct: Mapped[int | None] = mapped_column(Integer, nullable=True)
    comment: Mapped[str | None] = mapped_column(String(128), nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class Inproduct(Base):
    __tablename__ = "inproduct"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    no: Mapped[str] = mapped_column(String(20), nullable=False)
    category: Mapped[int | None] = mapped_column(Integer, nullable=True)
    name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    unitShipping: Mapped[int | None] = mapped_column(Integer, nullable=True)
    unitWarehouse: Mapped[int | None] = mapped_column(Integer, nullable=True)
    unitProduct: Mapped[int | None] = mapped_column(Integer, nullable=True)
    comment: Mapped[str | None] = mapped_column(String(128), nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class InproductBomSpec(Base):
    __tablename__ = "inproduct_bom_spec"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    inproduct_no: Mapped[str] = mapped_column(
        String(60),
        ForeignKey("inproduct.no", name="fk_inproduct_bom_spec_inproduct_no"),
        nullable=False,
    )
    category: Mapped[int | None] = mapped_column(Integer, nullable=True)
    item_no: Mapped[str] = mapped_column(String(60), nullable=False)
    item_version: Mapped[int] = mapped_column(Integer, nullable=False)
    bom12_no: Mapped[str] = mapped_column(String(60), nullable=False)
    count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    unit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    weight: Mapped[float | None] = mapped_column(Float, nullable=True)


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    no: Mapped[str] = mapped_column(String(20), nullable=False)
    category: Mapped[int | None] = mapped_column(Integer, nullable=True)
    name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    unitShipping: Mapped[int | None] = mapped_column(Integer, nullable=True)
    unitWarehouse: Mapped[int | None] = mapped_column(Integer, nullable=True)
    unitProduct: Mapped[int | None] = mapped_column(Integer, nullable=True)
    version: Mapped[int | None] = mapped_column(Integer, nullable=True)
    comment: Mapped[str | None] = mapped_column(String(128), nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class ProductVer(Base):
    __tablename__ = "product_ver"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    no: Mapped[str] = mapped_column(String(60), nullable=False)
    item_no: Mapped[str] = mapped_column(
        String(60), ForeignKey("product.no", name="fk_product_ver_item_no"), nullable=False
    )
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    date: Mapped[int | None] = mapped_column(Integer, nullable=True)


class ProductSpec(Base):
    __tablename__ = "product_spec"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    product_no: Mapped[str] = mapped_column(
        String(60), ForeignKey("product.no", name="fk_product_spec_product_no"), nullable=False
    )
    product_version: Mapped[int] = mapped_column(Integer, nullable=False)
    bom_no: Mapped[str | None] = mapped_column(String(60), nullable=True)
    bom_version: Mapped[int | None] = mapped_column(Integer, nullable=True)
    level: Mapped[int | None] = mapped_column(Integer, nullable=True)
    item_type: Mapped[int | None] = mapped_column(Integer, nullable=True)
    item_no: Mapped[str] = mapped_column(String(60), nullable=False)
    count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    unit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    weight: Mapped[float | None] = mapped_column(Float, nullable=True)


class ProductBomSpec(Base):
    __tablename__ = "product_bom_spec"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    product_no: Mapped[str] = mapped_column(
        String(60), ForeignKey("product.no", name="fk_product_bom_spec_product_no"), nullable=False
    )
    product_version: Mapped[int] = mapped_column(Integer, nullable=False)
    level: Mapped[int | None] = mapped_column(Integer, nullable=True)
    bom2_no: Mapped[str] = mapped_column(
        String(60), ForeignKey("bom2_number.no", name="fk_product_bom_spec_bom2_no"), nullable=False
    )
    count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    unit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    weight: Mapped[float | None] = mapped_column(Float, nullable=True)


class Goods(Base):
    __tablename__ = "goods"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    no: Mapped[str] = mapped_column(String(20), nullable=False)
    category: Mapped[int | None] = mapped_column(Integer, nullable=True)
    subCategory: Mapped[int | None] = mapped_column(Integer, nullable=True)
    name: Mapped[int | None] = mapped_column(Integer, nullable=True)
    unitShipping: Mapped[int | None] = mapped_column(Integer, nullable=True)
    unitWarehouse: Mapped[int | None] = mapped_column(Integer, nullable=True)
    unitProduct: Mapped[int | None] = mapped_column(Integer, nullable=True)
    comment: Mapped[str | None] = mapped_column(String(128), nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class TransItems(Base):
    __tablename__ = "trans_items"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    no: Mapped[str] = mapped_column(String(20), nullable=False)
    name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    category: Mapped[int | None] = mapped_column(Integer, nullable=True)
    attribute: Mapped[int | None] = mapped_column(Integer, nullable=True)
    company_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("company.no", name="fk_trans_items_company_no"), nullable=True
    )
    company_displayName: Mapped[str | None] = mapped_column(String(60), nullable=True)
    item_no: Mapped[str | None] = mapped_column(String(60), nullable=True)
    item_name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    comment: Mapped[str | None] = mapped_column(String(128), nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class TransItems2(Base):
    __tablename__ = "trans_items2"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    no: Mapped[str] = mapped_column(String(20), nullable=False)
    name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    category: Mapped[int | None] = mapped_column(Integer, nullable=True)
    attribute: Mapped[int | None] = mapped_column(Integer, nullable=True)
    company_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("company.no", name="fk_trans_items2_company_no"), nullable=True
    )
    company_displayName: Mapped[str | None] = mapped_column(String(60), nullable=True)
    comment: Mapped[str | None] = mapped_column(String(128), nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class ShipWhAlias(Base):
    __tablename__ = "ship_wh_alias"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    no: Mapped[str] = mapped_column(String(20), nullable=False)
    name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    category: Mapped[int | None] = mapped_column(Integer, nullable=True)
    type: Mapped[int | None] = mapped_column(Integer, nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class ShipWh(Base):
    __tablename__ = "ship_wh"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    no: Mapped[str] = mapped_column(String(60), nullable=False)
    company_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("company.no", name="fk_ship_wh_company_no"), nullable=True
    )
    company_displayName: Mapped[str | None] = mapped_column(String(60), nullable=True)
    name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    category: Mapped[int | None] = mapped_column(Integer, nullable=True)
    attribute: Mapped[int | None] = mapped_column(Integer, nullable=True)
    unit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    maxCapacity: Mapped[int | None] = mapped_column(Integer, nullable=True)
    comment: Mapped[str | None] = mapped_column(String(128), nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class Bom(Base):
    __tablename__ = "bom"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    no: Mapped[str] = mapped_column(String(60), nullable=False)
    displayName: Mapped[str | None] = mapped_column(String(60), nullable=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    date: Mapped[int | None] = mapped_column(Integer, nullable=True)
    unit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    weight: Mapped[float | None] = mapped_column(Float, nullable=True)
    comment: Mapped[str | None] = mapped_column(String(128), nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class BomItem(Base):
    __tablename__ = "bom_item"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    bom_no: Mapped[str] = mapped_column(
        String(60), ForeignKey("bom.no", name="fk_bom_item_bom_no"), nullable=False
    )
    item_no: Mapped[str] = mapped_column(
        String(60), ForeignKey("material.no", name="fk_bom_item_item_no"), nullable=False
    )
    item_name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    unit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    weight: Mapped[float | None] = mapped_column(Float, nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class Bom1Number(Base):
    __tablename__ = "bom1_number"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    no: Mapped[str] = mapped_column(String(60), nullable=False)
    displayName: Mapped[str | None] = mapped_column(String(60), nullable=True)
    unit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    weight: Mapped[float | None] = mapped_column(Float, nullable=True)
    bom_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("bom.no", name="fk_bom1_number_bom_no"), nullable=True
    )
    bom_version: Mapped[int | None] = mapped_column(Integer, nullable=True)
    comment: Mapped[str | None] = mapped_column(String(128), nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class Bom1(Base):
    __tablename__ = "bom1"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    parent_no: Mapped[str] = mapped_column(
        String(60), ForeignKey("bom1_number.no", name="fk_bom1_parent_no"), nullable=False
    )
    parent_name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    child_category: Mapped[int | None] = mapped_column(Integer, nullable=True)
    child_id: Mapped[str] = mapped_column(String(60), nullable=False)
    child_name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    childUnit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    weight: Mapped[float] = mapped_column(Float, nullable=False)
    expectedLoss: Mapped[float | None] = mapped_column(Float, nullable=True)
    actualLoss: Mapped[float | None] = mapped_column(Float, nullable=True)
    comment: Mapped[str | None] = mapped_column(String(128), nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class Bom2Number(Base):
    __tablename__ = "bom2_number"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    no: Mapped[str] = mapped_column(String(60), nullable=False)
    displayName: Mapped[str | None] = mapped_column(String(60), nullable=True)
    unit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    weight: Mapped[float | None] = mapped_column(Float, nullable=True)
    bom_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("product.no", name="fk_bom2_number_bom_no"), nullable=True
    )
    bom_version: Mapped[int | None] = mapped_column(Integer, nullable=True)
    comment: Mapped[str | None] = mapped_column(String(128), nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class Bom2(Base):
    __tablename__ = "bom2"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    parent_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("bom2_number.no", name="fk_bom2_parent_no"), nullable=True
    )
    parent_name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    child_category: Mapped[int | None] = mapped_column(Integer, nullable=True)
    child_id: Mapped[str | None] = mapped_column(String(60), nullable=True)
    child_name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    childUnit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    weight: Mapped[float | None] = mapped_column(Float, nullable=True)
    childUnit2: Mapped[int | None] = mapped_column(Integer, nullable=True)
    length: Mapped[float | None] = mapped_column(Float, nullable=True)
    count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    expectedLoss: Mapped[float | None] = mapped_column(Float, nullable=True)
    actualLoss: Mapped[float | None] = mapped_column(Float, nullable=True)
    comment: Mapped[str | None] = mapped_column(String(128), nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class SamplePrice(Base):
    __tablename__ = "sample_price"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    item_no: Mapped[str] = mapped_column(
        String(60), ForeignKey("bom.no", name="fk_sample_price_item_no"), nullable=False
    )
    date: Mapped[date] = mapped_column(Date, nullable=False)
    estWHUnitWeight: Mapped[int | None] = mapped_column(Integer, nullable=True)
    estWHPriceWeight: Mapped[float | None] = mapped_column(Double, nullable=True)
    estCostUnitWeight: Mapped[int | None] = mapped_column(Integer, nullable=True)
    estCostPriceWeight: Mapped[float | None] = mapped_column(Double, nullable=True)
    estLaborCost: Mapped[float | None] = mapped_column(Double, nullable=True)
    whUnitWeight: Mapped[int | None] = mapped_column(Integer, nullable=True)
    whPriceWeight: Mapped[float | None] = mapped_column(Double, nullable=True)
    costUnitWeight: Mapped[int | None] = mapped_column(Integer, nullable=True)
    costPriceWeight: Mapped[float | None] = mapped_column(Double, nullable=True)
    laborCost: Mapped[float | None] = mapped_column(Double, nullable=True)
    comment: Mapped[str | None] = mapped_column(String(128), nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class ItemPrice(Base):
    __tablename__ = "item_price"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    item_no: Mapped[str] = mapped_column(String(60), nullable=False)
    item_name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    itemCategory: Mapped[int | None] = mapped_column(Integer, nullable=True)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    whUnitWeight: Mapped[int | None] = mapped_column(Integer, nullable=True)
    costUnitWeight: Mapped[int | None] = mapped_column(Integer, nullable=True)
    estWHPriceWeight: Mapped[float | None] = mapped_column(Double, nullable=True)
    estWHPriceWeight1: Mapped[float | None] = mapped_column(Double, nullable=True)
    estWHPriceWeight2: Mapped[float | None] = mapped_column(Double, nullable=True)
    estCostPriceWeight: Mapped[float | None] = mapped_column(Double, nullable=True)
    estCostPriceWeight1: Mapped[float | None] = mapped_column(Double, nullable=True)
    estCostPriceWeight2: Mapped[float | None] = mapped_column(Double, nullable=True)
    estLaborCost: Mapped[float | None] = mapped_column(Double, nullable=True)
    whPriceWeight: Mapped[float | None] = mapped_column(Double, nullable=True)
    whPriceWeight1: Mapped[float | None] = mapped_column(Double, nullable=True)
    whPriceWeight2: Mapped[float | None] = mapped_column(Double, nullable=True)
    costPriceWeight: Mapped[float | None] = mapped_column(Double, nullable=True)
    costPriceWeight1: Mapped[float | None] = mapped_column(Double, nullable=True)
    costPriceWeight2: Mapped[float | None] = mapped_column(Double, nullable=True)
    laborCost: Mapped[float | None] = mapped_column(Double, nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class ItemLoss(Base):
    __tablename__ = "item_loss"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    item_no: Mapped[str] = mapped_column(String(60), nullable=False)
    itemCategory: Mapped[int | None] = mapped_column(Integer, nullable=True)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    unit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    estValue: Mapped[float | None] = mapped_column(Double, nullable=True)
    value: Mapped[float | None] = mapped_column(Double, nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class ItemHours(Base):
    __tablename__ = "item_hours"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    item_no: Mapped[str] = mapped_column(String(60), nullable=False)
    itemCategory: Mapped[int | None] = mapped_column(Integer, nullable=True)
    date: Mapped[int] = mapped_column(Integer, nullable=False)
    unit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    estValue: Mapped[float | None] = mapped_column(Double, nullable=True)
    value: Mapped[float | None] = mapped_column(Double, nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class ProcessCapacity(Base):
    __tablename__ = "process_capacity"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    oneProcess: Mapped[int] = mapped_column(Integer, nullable=False)
    secProcess: Mapped[int] = mapped_column(Integer, nullable=False)
    unit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    hourlyOutput: Mapped[float | None] = mapped_column(Double, nullable=True)
    laborCount: Mapped[int | None] = mapped_column(Integer, nullable=True)
    comment: Mapped[str | None] = mapped_column(String(128), nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class ProcessFlow(Base):
    __tablename__ = "process_flow"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    no: Mapped[str] = mapped_column(String(60), nullable=False)
    product_process_no: Mapped[str] = mapped_column(
        String(60),
        ForeignKey("product_process.no", name="fk_process_flow_product_process_no"),
        nullable=False,
    )
    order: Mapped[int] = mapped_column(Integer, nullable=False)
    oneProcess: Mapped[int | None] = mapped_column(Integer, nullable=True)
    secProcess: Mapped[int | None] = mapped_column(Integer, nullable=True)


class ProductProcess(Base):
    __tablename__ = "product_process"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    no: Mapped[str] = mapped_column(String(20), nullable=False)
    item_no: Mapped[str] = mapped_column(String(60), nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    date: Mapped[int | None] = mapped_column(Integer, nullable=True)


class BatchNumber(Base):
    __tablename__ = "batch_number"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    date: Mapped[int | None] = mapped_column(Integer, nullable=True)
    no: Mapped[str] = mapped_column(String(60), nullable=False)
    creator_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("employee.no", name="fk_batch_number_creator_no"), nullable=True
    )
    ref_no: Mapped[str] = mapped_column(String(60), nullable=False)
    refCategory: Mapped[int | None] = mapped_column(Integer, nullable=True)
    item_no: Mapped[str | None] = mapped_column(String(60), nullable=True)
    item_name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    item_ref_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("company.no", name="fk_batch_number_item_ref_no"), nullable=True
    )
    item_ref_displayName: Mapped[str | None] = mapped_column(String(60), nullable=True)
    itemCategory: Mapped[int | None] = mapped_column(Integer, nullable=True)
    itemSubCategory: Mapped[int | None] = mapped_column(Integer, nullable=True)
    itemType: Mapped[int | None] = mapped_column(Integer, nullable=True)
    unit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    expectedCount: Mapped[float | None] = mapped_column(Float, nullable=True)
    checkedCount: Mapped[float | None] = mapped_column(Float, nullable=True)
    validDays: Mapped[int | None] = mapped_column(Integer, nullable=True)
    validDate: Mapped[int | None] = mapped_column(Integer, nullable=True)
    validDateNo: Mapped[str | None] = mapped_column(String(60), nullable=True)
    comment: Mapped[str | None] = mapped_column(String(128), nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class BatchnoSerialno(Base):
    __tablename__ = "batchno_serialno"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    batch_number: Mapped[str] = mapped_column(String(60), nullable=False)
    serialNo: Mapped[str] = mapped_column(String(60), nullable=False)
    ref_order_no_category: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ref_order_no: Mapped[str] = mapped_column(String(60), nullable=False)
    warehouse_no: Mapped[str | None] = mapped_column(String(60), nullable=True)
    time: Mapped[int | None] = mapped_column(Integer, nullable=True)
    unit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    expectedCount: Mapped[float | None] = mapped_column(Float, nullable=True)
    count: Mapped[float | None] = mapped_column(Float, nullable=True)
    vaildDate: Mapped[int | None] = mapped_column(Integer, nullable=True)
    updatedTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class InventoryOrder(Base):
    __tablename__ = "inventory_order"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    no: Mapped[str] = mapped_column(String(60), nullable=False)
    creator_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("employee.no", name="fk_inventory_order_creator_no"), nullable=True
    )
    date: Mapped[int | None] = mapped_column(Integer, nullable=True)
    category: Mapped[int | None] = mapped_column(Integer, nullable=True)
    subCategory: Mapped[int | None] = mapped_column(Integer, nullable=True)
    item_no: Mapped[str | None] = mapped_column(String(60), nullable=True)
    item_name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    item_ref_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("company.no", name="fk_inventory_order_item_ref_no"), nullable=True
    )
    item_ref_displayName: Mapped[str | None] = mapped_column(String(60), nullable=True)
    itemCategory: Mapped[int | None] = mapped_column(Integer, nullable=True)
    itemType: Mapped[int | None] = mapped_column(Integer, nullable=True)
    unit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    price: Mapped[float | None] = mapped_column(Float, nullable=True)
    expectedCount: Mapped[float | None] = mapped_column(Float, nullable=True)
    checkedCount: Mapped[float | None] = mapped_column(Float, nullable=True)
    comment: Mapped[str | None] = mapped_column(String(128), nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class InventoryRecord(Base):
    __tablename__ = "inventory_record"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    group: Mapped[str | None] = mapped_column(String(60), nullable=True)
    refCategory: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ref_no: Mapped[str | None] = mapped_column(String(60), nullable=True)
    warehouse_no: Mapped[str | None] = mapped_column(
        String(60),
        ForeignKey("ship_wh_alias.no", name="fk_inventory_record_warehouse_no"),
        nullable=True,
    )
    warehouse_displayName: Mapped[str | None] = mapped_column(String(60), nullable=True)
    date: Mapped[int | None] = mapped_column(Integer, nullable=True)
    category: Mapped[int | None] = mapped_column(Integer, nullable=True)
    source: Mapped[int | None] = mapped_column(Integer, nullable=True)
    batchNumber: Mapped[str | None] = mapped_column(String(20), nullable=True)
    serialNo: Mapped[str | None] = mapped_column(String(20), nullable=True)
    item_no: Mapped[str | None] = mapped_column(String(60), nullable=True)
    item_name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    item_ref_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("company.no", name="fk_inventory_record_item_ref_no"), nullable=True
    )
    item_ref_displayName: Mapped[str | None] = mapped_column(String(60), nullable=True)
    itemCategory: Mapped[int | None] = mapped_column(Integer, nullable=True)
    itemType: Mapped[int | None] = mapped_column(Integer, nullable=True)
    unit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    count: Mapped[float | None] = mapped_column(Float, nullable=True)
    price: Mapped[float | None] = mapped_column(Float, nullable=True)
    amount: Mapped[float | None] = mapped_column(Float, nullable=True)
    comment: Mapped[str | None] = mapped_column(String(128), nullable=True)
    registerDevId: Mapped[str | None] = mapped_column(String(60), nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class InventoryDelta(Base):
    __tablename__ = "inventory_delta"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    warehouse_no: Mapped[str | None] = mapped_column(
        String(60),
        ForeignKey("ship_wh_alias.no", name="fk_inventory_delta_warehouse_no"),
        nullable=True,
    )
    warehouse_displayName: Mapped[str] = mapped_column(String(60), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    timezone: Mapped[str] = mapped_column(String(60), nullable=False)
    kind: Mapped[int | None] = mapped_column(Integer, nullable=True)
    category: Mapped[int | None] = mapped_column(Integer, nullable=True)
    specified_no: Mapped[str] = mapped_column(String(60), nullable=False)
    specified_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    specified_ref_no: Mapped[str | None] = mapped_column(String(60), nullable=True)
    specified_ref_name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    in_ref_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    out_ref_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    inCount: Mapped[float | None] = mapped_column(Float, nullable=True)
    inAmount: Mapped[float | None] = mapped_column(Double, nullable=True)
    inPurchaseCount: Mapped[float | None] = mapped_column(Float, nullable=True)
    inPurchaseAmount: Mapped[float | None] = mapped_column(Double, nullable=True)
    outCount: Mapped[float | None] = mapped_column(Float, nullable=True)
    outAmount: Mapped[float | None] = mapped_column(Double, nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class InventoryMonthStatistic(Base):
    __tablename__ = "Inventory_month_statistic"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    warehouse_no: Mapped[str | None] = mapped_column(
        String(60),
        ForeignKey("ship_wh_alias.no", name="fk_Inventory_month_statistic_warehouse_no"),
        nullable=True,
    )
    warehouse_displayName: Mapped[str] = mapped_column(String(60), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    timezone: Mapped[str] = mapped_column(String(60), nullable=False)
    category: Mapped[int | None] = mapped_column(Integer, nullable=True)
    startAmount: Mapped[float | None] = mapped_column(Double, nullable=True)
    inAmount: Mapped[float | None] = mapped_column(Double, nullable=True)
    outAmount: Mapped[float | None] = mapped_column(Double, nullable=True)
    inPurchaseAmount: Mapped[float | None] = mapped_column(Double, nullable=True)
    endAmount: Mapped[float | None] = mapped_column(Double, nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class InventoryItemMonthStatistic(Base):
    __tablename__ = "Inventory_item_month_statistic"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    warehouse_no: Mapped[str | None] = mapped_column(
        String(60),
        ForeignKey("ship_wh_alias.no", name="fk_Inventory_item_month_statistic_warehouse_no"),
        nullable=True,
    )
    warehouse_displayName: Mapped[str] = mapped_column(String(60), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    timezone: Mapped[str] = mapped_column(String(60), nullable=False)
    kind: Mapped[int | None] = mapped_column(Integer, nullable=True)
    category: Mapped[int | None] = mapped_column(Integer, nullable=True)
    specified_no: Mapped[str] = mapped_column(String(60), nullable=False)
    specified_name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    specified_ref_no: Mapped[str] = mapped_column(String(60), nullable=False)
    specified_ref_name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    unit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    startCount: Mapped[float | None] = mapped_column(Float, nullable=True)
    startAmount: Mapped[float | None] = mapped_column(Double, nullable=True)
    inCount: Mapped[int | None] = mapped_column(Integer, nullable=True)
    inAmount: Mapped[float | None] = mapped_column(Double, nullable=True)
    endCount: Mapped[int | None] = mapped_column(Integer, nullable=True)
    endAmount: Mapped[float | None] = mapped_column(Double, nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class Quotation(Base):
    __tablename__ = "quotation"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    no: Mapped[str] = mapped_column(String(20), nullable=False)
    creator_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("employee.no", name="fk_quotation_creator_no"), nullable=True
    )
    date: Mapped[int | None] = mapped_column(Integer, nullable=True)
    category: Mapped[int | None] = mapped_column(Integer, nullable=True)
    type: Mapped[int | None] = mapped_column(Integer, nullable=True)
    itemStyle: Mapped[int | None] = mapped_column(Integer, nullable=True)
    item_no: Mapped[str | None] = mapped_column(String(255), nullable=True)
    item_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    item_ref_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("company.no", name="fk_quotation_item_ref_no"), nullable=True
    )
    item_ref_displayName: Mapped[str | None] = mapped_column(String(60), nullable=True)
    unit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    price: Mapped[str | None] = mapped_column(String(255), nullable=True)
    unitConversion: Mapped[str | None] = mapped_column(String(255), nullable=True)
    comment: Mapped[str | None] = mapped_column(String(128), nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class ShipWhQuotation(Base):
    __tablename__ = "ship_wh_quotation"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    no: Mapped[str] = mapped_column(String(60), nullable=False)
    date: Mapped[int] = mapped_column(Integer, nullable=False)
    item_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("ship_wh.no", name="fk_ship_wh_quotation_item_no"), nullable=True
    )
    item_name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    item_ref_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("company.no", name="fk_ship_wh_quotation_item_ref_no"), nullable=True
    )
    item_ref_displayName: Mapped[str | None] = mapped_column(String(60), nullable=True)
    category: Mapped[int | None] = mapped_column(Integer, nullable=True)
    type: Mapped[int | None] = mapped_column(Integer, nullable=True)
    itemStyle: Mapped[int | None] = mapped_column(Integer, nullable=True)
    region: Mapped[int | None] = mapped_column(Integer, nullable=True)
    unit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    price: Mapped[float | None] = mapped_column(Float, nullable=True)
    fee: Mapped[float | None] = mapped_column(Float, nullable=True)
    comment: Mapped[str | None] = mapped_column(String(128), nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class Contract(Base):
    __tablename__ = "contract"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    no: Mapped[str] = mapped_column(String(20), nullable=False)
    ref_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("quotation.no", name="fk_contract_ref_no"), nullable=True
    )
    creator_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("employee.no", name="fk_contract_creator_no"), nullable=True
    )
    date: Mapped[int] = mapped_column(Integer, nullable=False)
    displayName: Mapped[str | None] = mapped_column(String(60), nullable=True)
    category: Mapped[int | None] = mapped_column(Integer, nullable=True)
    type: Mapped[int | None] = mapped_column(Integer, nullable=True)
    itemStyle: Mapped[int | None] = mapped_column(Integer, nullable=True)
    item_no: Mapped[str | None] = mapped_column(String(60), nullable=True)
    item_name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    itemCategory: Mapped[int | None] = mapped_column(Integer, nullable=True)
    itemSubCategory: Mapped[int | None] = mapped_column(Integer, nullable=True)
    item_ref_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("company.no", name="fk_contract_item_ref_no"), nullable=True
    )
    item_ref_displayName: Mapped[str | None] = mapped_column(String(60), nullable=True)
    payment_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("payment.id", name="fk_contract_payment_id"), nullable=True
    )
    unit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    price: Mapped[float | None] = mapped_column(Double, nullable=True)
    shippingPrice: Mapped[float | None] = mapped_column(Double, nullable=True)
    unitConversion: Mapped[float | None] = mapped_column(Double, nullable=True)
    comment: Mapped[str | None] = mapped_column(String(128), nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class ShipWhContract(Base):
    __tablename__ = "ship_wh_contract"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    no: Mapped[str] = mapped_column(String(60), nullable=False)
    date: Mapped[int] = mapped_column(Integer, nullable=False)
    ref_no: Mapped[str | None] = mapped_column(
        String(60),
        ForeignKey("ship_wh_quotation.no", name="fk_ship_wh_contract_ref_no"),
        nullable=True,
    )
    sw_alias_no: Mapped[str | None] = mapped_column(
        String(60),
        ForeignKey("ship_wh_alias.no", name="fk_ship_wh_contract_sw_alias_no"),
        nullable=True,
    )
    displayName: Mapped[str | None] = mapped_column(String(60), nullable=True)
    item_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("ship_wh.no", name="fk_ship_wh_contract_item_no"), nullable=True
    )
    item_name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    item_ref_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("company.no", name="fk_ship_wh_contract_item_ref_no"), nullable=True
    )
    item_ref_displayName: Mapped[str | None] = mapped_column(String(60), nullable=True)
    category: Mapped[int | None] = mapped_column(Integer, nullable=True)
    type: Mapped[int | None] = mapped_column(Integer, nullable=True)
    itemStyle: Mapped[int | None] = mapped_column(Integer, nullable=True)
    region: Mapped[int | None] = mapped_column(Integer, nullable=True)
    unit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    price: Mapped[float | None] = mapped_column(Double, nullable=True)
    fee: Mapped[float | None] = mapped_column(Double, nullable=True)
    comment: Mapped[str | None] = mapped_column(String(128), nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class ProductOrder(Base):
    __tablename__ = "product_order"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    no: Mapped[str] = mapped_column(String(20), nullable=False)
    creator_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("employee.no", name="fk_product_order_creator_no"), nullable=True
    )
    date: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ref_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("contract.no", name="fk_product_order_ref_no"), nullable=True
    )
    item_ref_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("company.no", name="fk_product_order_item_ref_no"), nullable=True
    )
    item_ref_displayName: Mapped[str | None] = mapped_column(String(60), nullable=True)
    item_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("trans_items.no", name="fk_product_order_item_no"), nullable=True
    )
    item_name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    unit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    price: Mapped[float | None] = mapped_column(Float, nullable=True)
    count: Mapped[float | None] = mapped_column(Float, nullable=True)
    preparedCount: Mapped[float | None] = mapped_column(Float, nullable=True)
    amount: Mapped[float | None] = mapped_column(Float, nullable=True)
    expectedDate: Mapped[int | None] = mapped_column(Integer, nullable=True)
    address: Mapped[str | None] = mapped_column(String(100), nullable=True)
    payment_type: Mapped[int | None] = mapped_column(Integer, nullable=True)
    payment_source: Mapped[int | None] = mapped_column(Integer, nullable=True)
    payment_date: Mapped[int | None] = mapped_column(Integer, nullable=True)
    payment_period: Mapped[int | None] = mapped_column(Integer, nullable=True)
    comment: Mapped[str | None] = mapped_column(String(128), nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class ShippingOrder(Base):
    __tablename__ = "shipping_order"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    no: Mapped[str] = mapped_column(String(20), nullable=False)
    creator_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("employee.no", name="fk_shipping_order_creator_no"), nullable=True
    )
    product_order_no: Mapped[str | None] = mapped_column(
        String(60),
        ForeignKey("product_order.no", name="fk_shipping_order_product_order_no"),
        nullable=True,
    )
    date: Mapped[int | None] = mapped_column(Integer, nullable=True)
    category: Mapped[int | None] = mapped_column(Integer, nullable=True)
    item_ref_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("company.no", name="fk_shipping_order_item_ref_no"), nullable=True
    )
    item_ref_displayName: Mapped[str | None] = mapped_column(String(60), nullable=True)
    item_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("trans_items.no", name="fk_shipping_order_item_no"), nullable=True
    )
    item_name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    itemCategory: Mapped[int | None] = mapped_column(Integer, nullable=True)
    itemSubCategory: Mapped[int | None] = mapped_column(Integer, nullable=True)
    unit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    price: Mapped[float | None] = mapped_column(Double, nullable=True)
    expectedCount: Mapped[float | None] = mapped_column(Float, nullable=True)
    checkedCount: Mapped[float | None] = mapped_column(Float, nullable=True)
    feeCount: Mapped[float | None] = mapped_column(Float, nullable=True)
    amount: Mapped[int | None] = mapped_column(Integer, nullable=True)
    addDeleteAmount: Mapped[int | None] = mapped_column(Integer, nullable=True)
    comment: Mapped[str | None] = mapped_column(String(128), nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class PurchaseRequest(Base):
    __tablename__ = "purchase_request"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    no: Mapped[str] = mapped_column(String(20), nullable=False)
    creator_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("employee.no", name="fk_purchase_request_creator_no"), nullable=True
    )
    product_order_no: Mapped[str | None] = mapped_column(
        String(60),
        ForeignKey("product_order.no", name="fk_purchase_request_product_order_no"),
        nullable=True,
    )
    date: Mapped[int | None] = mapped_column(Integer, nullable=True)
    comment: Mapped[str | None] = mapped_column(String(128), nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class PurchaseRequestItem(Base):
    __tablename__ = "purchase_request_item"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    purchase_request_no: Mapped[str] = mapped_column(
        String(60),
        ForeignKey("purchase_request.no", name="fk_purchase_request_item_purchase_request_no"),
        nullable=False,
    )
    item_no: Mapped[str | None] = mapped_column(
        String(60),
        ForeignKey("material.no", name="fk_purchase_request_item_item_no"),
        nullable=True,
    )
    unit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    count: Mapped[float | None] = mapped_column(Float, nullable=True)
    expectedDate: Mapped[int | None] = mapped_column(Integer, nullable=True)
    comment: Mapped[str | None] = mapped_column(String(128), nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class PurchaseOrder(Base):
    __tablename__ = "purchase_order"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    no: Mapped[str] = mapped_column(String(20), nullable=False)
    creator_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("employee.no", name="fk_purchase_order_creator_no"), nullable=True
    )
    purchase_request_no: Mapped[str | None] = mapped_column(
        String(60),
        ForeignKey("purchase_request.no", name="fk_purchase_order_purchase_request_no"),
        nullable=True,
    )
    date: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ref_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("contract.no", name="fk_purchase_order_ref_no"), nullable=True
    )
    item_ref_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("company.no", name="fk_purchase_order_item_ref_no"), nullable=True
    )
    item_ref_displayName: Mapped[str | None] = mapped_column(String(60), nullable=True)
    item_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("trans_items.no", name="fk_purchase_order_item_no"), nullable=True
    )
    item_name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    unit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    price: Mapped[float | None] = mapped_column(Double, nullable=True)
    count: Mapped[float | None] = mapped_column(Float, nullable=True)
    amount: Mapped[float | None] = mapped_column(Float, nullable=True)
    expectedDate: Mapped[int | None] = mapped_column(Integer, nullable=True)
    address: Mapped[str | None] = mapped_column(String(100), nullable=True)
    payment_type: Mapped[int | None] = mapped_column(Integer, nullable=True)
    payment_source: Mapped[int | None] = mapped_column(Integer, nullable=True)
    payment_date: Mapped[int | None] = mapped_column(Integer, nullable=True)
    payment_period: Mapped[int | None] = mapped_column(Integer, nullable=True)
    comment: Mapped[str | None] = mapped_column(String(128), nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class GoodsReceiptNote(Base):
    __tablename__ = "goods_receipt_note"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    no: Mapped[str] = mapped_column(String(20), nullable=False)
    creator_no: Mapped[str | None] = mapped_column(
        String(60),
        ForeignKey("employee.no", name="fk_goods_receipt_note_creator_no"),
        nullable=True,
    )
    purchase_order_no: Mapped[str | None] = mapped_column(
        String(60),
        ForeignKey("purchase_order.no", name="fk_goods_receipt_note_purchase_order_no"),
        nullable=True,
    )
    date: Mapped[int | None] = mapped_column(Integer, nullable=True)
    category: Mapped[int | None] = mapped_column(Integer, nullable=True)
    item_ref_no: Mapped[str | None] = mapped_column(
        String(60),
        ForeignKey("company.no", name="fk_goods_receipt_note_item_ref_no"),
        nullable=True,
    )
    item_ref_displayName: Mapped[str | None] = mapped_column(String(60), nullable=True)
    item_no: Mapped[str | None] = mapped_column(
        String(255),
        ForeignKey("trans_items.no", name="fk_goods_receipt_note_item_no"),
        nullable=True,
    )
    item_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    itemCategory: Mapped[int | None] = mapped_column(Integer, nullable=True)
    itemSubCategory: Mapped[int | None] = mapped_column(Integer, nullable=True)
    unit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    price: Mapped[float | None] = mapped_column(Double, nullable=True)
    expectedCount: Mapped[float | None] = mapped_column(Float, nullable=True)
    checkedCount: Mapped[float | None] = mapped_column(Float, nullable=True)
    feeCount: Mapped[float | None] = mapped_column(Float, nullable=True)
    amount: Mapped[int | None] = mapped_column(Integer, nullable=True)
    addDeleteAmount: Mapped[int | None] = mapped_column(Integer, nullable=True)
    comment: Mapped[str | None] = mapped_column(String(128), nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class OrderPayment(Base):
    __tablename__ = "order_payment"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    no: Mapped[str | None] = mapped_column(String(60), nullable=True)
    group_no: Mapped[str | None] = mapped_column(String(60), nullable=True)
    date: Mapped[int | None] = mapped_column(Integer, nullable=True)
    arapType: Mapped[int | None] = mapped_column(Integer, nullable=True)
    refCategory: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ref_no: Mapped[str | None] = mapped_column(String(60), nullable=True)
    ref_sub_no: Mapped[str | None] = mapped_column(String(60), nullable=True)
    item_ref_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("company.no", name="fk_order_payment_item_ref_no"), nullable=True
    )
    item_ref_displayName: Mapped[str | None] = mapped_column(String(60), nullable=True)
    itemCategory: Mapped[int | None] = mapped_column(Integer, nullable=True)
    itemSubCategory: Mapped[int | None] = mapped_column(Integer, nullable=True)
    paymentType: Mapped[int | None] = mapped_column(Integer, nullable=True)
    month: Mapped[date | None] = mapped_column(Date, nullable=True)
    price: Mapped[float | None] = mapped_column(Double, nullable=True)
    count: Mapped[float | None] = mapped_column(Float, nullable=True)
    amount: Mapped[int | None] = mapped_column(Integer, nullable=True)
    addDeleteAmount: Mapped[int | None] = mapped_column(Integer, nullable=True)
    totalAmount: Mapped[int | None] = mapped_column(Integer, nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class ShippingRecord(Base):
    __tablename__ = "shipping_record"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    date: Mapped[int | None] = mapped_column(Integer, nullable=True)
    refCategory: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ref_no: Mapped[str | None] = mapped_column(String(60), nullable=True)
    ref_parent_no: Mapped[str | None] = mapped_column(String(60), nullable=True)
    contract_no: Mapped[str | None] = mapped_column(
        String(60),
        ForeignKey("ship_wh_contract.no", name="fk_shipping_record_contract_no"),
        nullable=True,
    )
    sw_alias_no: Mapped[str | None] = mapped_column(
        String(60),
        ForeignKey("ship_wh_alias.no", name="fk_shipping_record_sw_alias_no"),
        nullable=True,
    )
    sw_alias_name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    item_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("ship_wh.no", name="fk_shipping_record_item_no"), nullable=True
    )
    item_name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    item_ref_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("company.no", name="fk_shipping_record_item_ref_no"), nullable=True
    )
    item_ref_displayName: Mapped[str | None] = mapped_column(String(60), nullable=True)
    unit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    price: Mapped[float | None] = mapped_column(Double, nullable=True)
    expectedCount: Mapped[int | None] = mapped_column(Integer, nullable=True)
    checkedCount: Mapped[int | None] = mapped_column(Integer, nullable=True)
    comment: Mapped[str | None] = mapped_column(String(128), nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class WarehouseRecord(Base):
    __tablename__ = "warehouse_record"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    date: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ref_no: Mapped[int | None] = mapped_column(Integer, nullable=True)
    batch_no: Mapped[str | None] = mapped_column(
        String(20),
        ForeignKey("batch_number.no", name="fk_warehouse_record_batch_no"),
        nullable=True,
    )
    contract_no: Mapped[str | None] = mapped_column(
        String(60),
        ForeignKey("ship_wh_contract.no", name="fk_warehouse_record_contract_no"),
        nullable=True,
    )
    sw_alias_no: Mapped[str | None] = mapped_column(
        String(60),
        ForeignKey("ship_wh_alias.no", name="fk_warehouse_record_sw_alias_no"),
        nullable=True,
    )
    sw_alias_name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    item_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("ship_wh.no", name="fk_warehouse_record_item_no"), nullable=True
    )
    item_name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    item_ref_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("company.no", name="fk_warehouse_record_item_ref_no"), nullable=True
    )
    item_ref_displayName: Mapped[str | None] = mapped_column(String(60), nullable=True)
    inboundTime: Mapped[int | None] = mapped_column(Integer, nullable=True)
    unit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    price: Mapped[float | None] = mapped_column(Double, nullable=True)
    count: Mapped[float | None] = mapped_column(Float, nullable=True)
    days: Mapped[float | None] = mapped_column(Float, nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class ShippingPayment(Base):
    __tablename__ = "shipping_payment"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    no: Mapped[str] = mapped_column(String(60), nullable=False)
    group_no: Mapped[str | None] = mapped_column(String(60), nullable=True)
    date: Mapped[int] = mapped_column(Integer, nullable=False)
    arapType: Mapped[int | None] = mapped_column(Integer, nullable=True)
    record_no: Mapped[str | None] = mapped_column(String(60), nullable=True)
    refCategory: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ref_no: Mapped[str | None] = mapped_column(String(60), nullable=True)
    ref_sub_no: Mapped[str | None] = mapped_column(String(60), nullable=True)
    item_ref_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("company.no", name="fk_shipping_payment_item_ref_no"), nullable=True
    )
    item_ref_displayName: Mapped[str | None] = mapped_column(String(60), nullable=True)
    paymentType: Mapped[int | None] = mapped_column(Integer, nullable=True)
    month: Mapped[date | None] = mapped_column(Date, nullable=True)
    price: Mapped[float | None] = mapped_column(Double, nullable=True)
    count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    amount: Mapped[int | None] = mapped_column(Integer, nullable=True)
    addDeleteAmount: Mapped[int | None] = mapped_column(Integer, nullable=True)
    totalAmount: Mapped[int | None] = mapped_column(Integer, nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class WarehousePayment(Base):
    __tablename__ = "warehouse_payment"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    no: Mapped[str] = mapped_column(String(60), nullable=False)
    group_no: Mapped[str | None] = mapped_column(String(60), nullable=True)
    date: Mapped[int] = mapped_column(Integer, nullable=False)
    arapType: Mapped[int | None] = mapped_column(Integer, nullable=True)
    batch_no: Mapped[str | None] = mapped_column(
        String(60),
        ForeignKey("batch_number.no", name="fk_warehouse_payment_batch_no"),
        nullable=True,
    )
    record_no: Mapped[str | None] = mapped_column(String(60), nullable=True)
    item_ref_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("company.no", name="fk_warehouse_payment_item_ref_no"), nullable=True
    )
    item_ref_displayName: Mapped[str | None] = mapped_column(String(60), nullable=True)
    paymentType: Mapped[int | None] = mapped_column(Integer, nullable=True)
    month: Mapped[date | None] = mapped_column(Date, nullable=True)
    price: Mapped[float | None] = mapped_column(Double, nullable=True)
    count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    amount: Mapped[int | None] = mapped_column(Integer, nullable=True)
    addDeleteAmount: Mapped[int | None] = mapped_column(Integer, nullable=True)
    totalAmount: Mapped[int | None] = mapped_column(Integer, nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class OrderItemMonthStatistic(Base):
    __tablename__ = "order_item_month_statistic"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    timezone: Mapped[str | None] = mapped_column(String(60), nullable=True)
    kind: Mapped[int] = mapped_column(Integer, nullable=False)
    category: Mapped[int] = mapped_column(Integer, nullable=False)
    subCategory: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[int | None] = mapped_column(Integer, nullable=True)
    specified_no: Mapped[str] = mapped_column(
        String(60),
        ForeignKey("company.no", name="fk_order_item_month_statistic_specified_no"),
        nullable=False,
    )
    specified_name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    payment: Mapped[int | None] = mapped_column(Integer, nullable=True)
    amount: Mapped[int | None] = mapped_column(Integer, nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class Factory(Base):
    __tablename__ = "factory"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    no: Mapped[str] = mapped_column(String(60), nullable=False)
    region: Mapped[str | None] = mapped_column(String(60), nullable=True)
    location: Mapped[str | None] = mapped_column(String(60), nullable=True)
    comment: Mapped[str | None] = mapped_column(String(128), nullable=True)


class Process(Base):
    __tablename__ = "process"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    no: Mapped[str] = mapped_column(String(20), nullable=False)
    oneProcess: Mapped[int | None] = mapped_column(Integer, nullable=True)
    secProcess: Mapped[int | None] = mapped_column(Integer, nullable=True)
    comment: Mapped[str | None] = mapped_column(String(128), nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class ProductionLine(Base):
    __tablename__ = "production_line"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    no: Mapped[str] = mapped_column(String(60), nullable=False)
    name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    process_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("process.no", name="fk_production_line_process_no"), nullable=True
    )
    oneProcess: Mapped[int | None] = mapped_column(Integer, nullable=True)
    secProcess: Mapped[int | None] = mapped_column(Integer, nullable=True)
    factory_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("factory.no", name="fk_production_line_factory_no"), nullable=True
    )
    location: Mapped[str | None] = mapped_column(String(60), nullable=True)
    capacityUnit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    capacity: Mapped[float | None] = mapped_column(Float, nullable=True)
    laborCount: Mapped[int | None] = mapped_column(Integer, nullable=True)
    laborEfficiency: Mapped[float | None] = mapped_column(Float, nullable=True)
    comment: Mapped[str | None] = mapped_column(String(128), nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class Station(Base):
    __tablename__ = "station"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    no: Mapped[str] = mapped_column(String(60), nullable=False)
    productionline_no: Mapped[str | None] = mapped_column(
        String(60),
        ForeignKey("production_line.no", name="fk_station_productionline_no"),
        nullable=True,
    )
    name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    stage: Mapped[int | None] = mapped_column(Integer, nullable=True)
    comment: Mapped[str | None] = mapped_column(String(128), nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class Equipment(Base):
    __tablename__ = "equipment"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    no: Mapped[str] = mapped_column(String(60), nullable=False)
    station_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("station.no", name="fk_equipment_station_no"), nullable=True
    )
    name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    model: Mapped[str | None] = mapped_column(String(60), nullable=True)
    manufacturer: Mapped[str | None] = mapped_column(String(60), nullable=True)
    purchaseDate: Mapped[int | None] = mapped_column(Integer, nullable=True)
    appearance: Mapped[str | None] = mapped_column(String(128), nullable=True)
    comment: Mapped[str | None] = mapped_column(String(128), nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class ApsQuantity(Base):
    __tablename__ = "aps_quantity"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    no: Mapped[str] = mapped_column(String(60), nullable=False)
    product_order_no: Mapped[str] = mapped_column(
        String(60),
        ForeignKey("product_order.no", name="fk_aps_quantity_product_order_no"),
        nullable=False,
    )
    oneProcess: Mapped[int] = mapped_column(Integer, nullable=False)
    secProcess: Mapped[int] = mapped_column(Integer, nullable=False)
    item_no: Mapped[str] = mapped_column(String(60), nullable=False)
    item_name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    itemCategory: Mapped[int | None] = mapped_column(Integer, nullable=True)
    unit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    amount: Mapped[float | None] = mapped_column(Float, nullable=True)
    minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    laborCount: Mapped[int | None] = mapped_column(Integer, nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class ApsQuantityItem(Base):
    __tablename__ = "aps_quantity_item"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    product_order_no: Mapped[str] = mapped_column(
        String(60),
        ForeignKey("product_order.no", name="fk_aps_quantity_item_product_order_no"),
        nullable=False,
    )
    oneProcess: Mapped[int] = mapped_column(Integer, nullable=False)
    secProcess: Mapped[int] = mapped_column(Integer, nullable=False)
    item_no: Mapped[str] = mapped_column(
        String(60), ForeignKey("material.no", name="fk_aps_quantity_item_item_no"), nullable=False
    )
    item_name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    itemCategory: Mapped[int | None] = mapped_column(Integer, nullable=True)
    unit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    count: Mapped[float | None] = mapped_column(Float, nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class WorkOrder(Base):
    __tablename__ = "work_order"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    no: Mapped[str] = mapped_column(String(20), nullable=False)
    creator_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("employee.no", name="fk_work_order_creator_no"), nullable=True
    )
    product_order_no: Mapped[str | None] = mapped_column(
        String(60),
        ForeignKey("product_order.no", name="fk_work_order_product_order_no"),
        nullable=True,
    )
    aps_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("aps_quantity.no", name="fk_work_order_aps_no"), nullable=True
    )
    date: Mapped[int | None] = mapped_column(Integer, nullable=True)
    product_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("product.no", name="fk_work_order_product_no"), nullable=True
    )
    product_name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    customer_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("company.no", name="fk_work_order_customer_no"), nullable=True
    )
    customer_displayName: Mapped[str | None] = mapped_column(String(60), nullable=True)
    output_item_no: Mapped[str | None] = mapped_column(String(255), nullable=True)
    output_item_name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    production_line_no: Mapped[str | None] = mapped_column(
        String(60),
        ForeignKey("production_line.no", name="fk_work_order_production_line_no"),
        nullable=True,
    )
    oneProcess: Mapped[int | None] = mapped_column(Integer, nullable=True)
    secProcess: Mapped[int | None] = mapped_column(Integer, nullable=True)
    startTime: Mapped[int | None] = mapped_column(Integer, nullable=True)
    endTime: Mapped[int | None] = mapped_column(Integer, nullable=True)
    processUnit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    processCount: Mapped[float | None] = mapped_column(Float, nullable=True)
    processTime: Mapped[int | None] = mapped_column(Integer, nullable=True)
    laborCount: Mapped[int | None] = mapped_column(Integer, nullable=True)
    laborList: Mapped[str | None] = mapped_column(Text, nullable=True)
    comment: Mapped[str | None] = mapped_column(String(128), nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class ProcessOrder(Base):
    __tablename__ = "process_order"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    no: Mapped[str] = mapped_column(String(20), nullable=False)
    creator_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("employee.no", name="fk_process_order_creator_no"), nullable=True
    )
    work_order_no: Mapped[str | None] = mapped_column(
        String(60),
        ForeignKey("work_order.no", name="fk_process_order_work_order_no"),
        nullable=True,
    )
    refProcess: Mapped[int | None] = mapped_column(Integer, nullable=True)
    date: Mapped[int | None] = mapped_column(Integer, nullable=True)
    category: Mapped[int | None] = mapped_column(Integer, nullable=True)
    item_no: Mapped[str | None] = mapped_column(String(60), nullable=True)
    item_name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    itemCategory: Mapped[int | None] = mapped_column(Integer, nullable=True)
    itemSubCategory: Mapped[int | None] = mapped_column(Integer, nullable=True)
    item_ref_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("company.no", name="fk_process_order_item_ref_no"), nullable=True
    )
    item_ref_displayName: Mapped[str | None] = mapped_column(String(60), nullable=True)
    unit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    expectedCount: Mapped[float | None] = mapped_column(Float, nullable=True)
    count: Mapped[float | None] = mapped_column(Float, nullable=True)
    comment: Mapped[str | None] = mapped_column(String(128), nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class ProcessLabor(Base):
    __tablename__ = "process_labor"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    date: Mapped[int | None] = mapped_column(Integer, nullable=True)
    creator_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("employee.no", name="fk_process_labor_creator_no"), nullable=True
    )
    work_order_no: Mapped[str] = mapped_column(
        String(60),
        ForeignKey("work_order.no", name="fk_process_labor_work_order_no"),
        nullable=False,
    )
    employee_no: Mapped[str] = mapped_column(
        String(60), ForeignKey("employee.no", name="fk_process_labor_employee_no"), nullable=False
    )
    production_line_no: Mapped[str | None] = mapped_column(
        String(60),
        ForeignKey("production_line.no", name="fk_process_labor_production_line_no"),
        nullable=True,
    )
    station_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("station.no", name="fk_process_labor_station_no"), nullable=True
    )


class ProductionData(Base):
    __tablename__ = "production_data"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    creator_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("employee.no", name="fk_production_data_creator_no"), nullable=True
    )
    work_order_no: Mapped[str] = mapped_column(
        String(60),
        ForeignKey("work_order.no", name="fk_production_data_work_order_no"),
        nullable=False,
    )
    product_order_no: Mapped[str | None] = mapped_column(
        String(60),
        ForeignKey("product_order.no", name="fk_production_data_product_order_no"),
        nullable=True,
    )
    customer_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("company.no", name="fk_production_data_customer_no"), nullable=True
    )
    customer_displayName: Mapped[str | None] = mapped_column(String(60), nullable=True)
    product_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("product.no", name="fk_production_data_product_no"), nullable=True
    )
    product_name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    date: Mapped[int | None] = mapped_column(Integer, nullable=True)
    production_line_no: Mapped[str | None] = mapped_column(
        String(60),
        ForeignKey("production_line.no", name="fk_production_data_production_line_no"),
        nullable=True,
    )
    oneProcess: Mapped[int | None] = mapped_column(Integer, nullable=True)
    secProcess: Mapped[int | None] = mapped_column(Integer, nullable=True)
    item_no: Mapped[str | None] = mapped_column(String(255), nullable=True)
    item_name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    materialLoss: Mapped[float | None] = mapped_column(Float, nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class ProductionDataOutput(Base):
    __tablename__ = "production_data_output"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    work_order_no: Mapped[str] = mapped_column(
        String(60),
        ForeignKey("work_order.no", name="fk_production_data_output_work_order_no"),
        nullable=False,
    )
    process_order_no: Mapped[str | None] = mapped_column(
        String(60),
        ForeignKey("process_order.no", name="fk_production_data_output_process_order_no"),
        nullable=True,
    )
    group: Mapped[str] = mapped_column(String(60), nullable=False)
    time: Mapped[int | None] = mapped_column(Integer, nullable=True)
    action: Mapped[int] = mapped_column(Integer, nullable=False)
    item_no: Mapped[str] = mapped_column(String(60), nullable=False)
    item_name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    category: Mapped[int | None] = mapped_column(Integer, nullable=True)
    itemSubCategory: Mapped[int | None] = mapped_column(Integer, nullable=True)
    batch_number: Mapped[str] = mapped_column(String(60), nullable=False)
    serial_no: Mapped[str] = mapped_column(String(60), nullable=False)
    valid_date: Mapped[int | None] = mapped_column(Integer, nullable=True)
    valid_date_no: Mapped[str] = mapped_column(String(60), nullable=False)
    unit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    count: Mapped[float | None] = mapped_column(Float, nullable=True)
    comment: Mapped[str | None] = mapped_column(String(128), nullable=True)


class ProductionDataInput(Base):
    __tablename__ = "production_data_input"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    work_order_no: Mapped[str] = mapped_column(
        String(60),
        ForeignKey("work_order.no", name="fk_production_data_input_work_order_no"),
        nullable=False,
    )
    process_order_no: Mapped[str | None] = mapped_column(
        String(60),
        ForeignKey("process_order.no", name="fk_production_data_input_process_order_no"),
        nullable=True,
    )
    group: Mapped[str] = mapped_column(String(60), nullable=False)
    time: Mapped[int | None] = mapped_column(Integer, nullable=True)
    action: Mapped[int] = mapped_column(Integer, nullable=False)
    item_no: Mapped[str] = mapped_column(String(60), nullable=False)
    item_name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    category: Mapped[int | None] = mapped_column(Integer, nullable=True)
    itemSubCategory: Mapped[int | None] = mapped_column(Integer, nullable=True)
    batch_number: Mapped[str] = mapped_column(String(60), nullable=False)
    serial_no: Mapped[str] = mapped_column(String(60), nullable=False)
    unit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    count: Mapped[float | None] = mapped_column(Float, nullable=True)
    comment: Mapped[str | None] = mapped_column(String(128), nullable=True)


class ProductionDataReuse(Base):
    __tablename__ = "production_data_reuse"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    work_order_no: Mapped[str] = mapped_column(
        String(60),
        ForeignKey("work_order.no", name="fk_production_data_reuse_work_order_no"),
        nullable=False,
    )
    process_order_no: Mapped[str] = mapped_column(
        String(60),
        ForeignKey("process_order.no", name="fk_production_data_reuse_process_order_no"),
        nullable=False,
    )
    group: Mapped[str] = mapped_column(String(60), nullable=False)
    time: Mapped[int | None] = mapped_column(Integer, nullable=True)
    action: Mapped[int] = mapped_column(Integer, nullable=False)
    item_no: Mapped[str] = mapped_column(
        String(60),
        ForeignKey("inproduct.no", name="fk_production_data_reuse_item_no"),
        nullable=False,
    )
    item_name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    category: Mapped[int] = mapped_column(Integer, nullable=False)
    itemSubCategory: Mapped[int | None] = mapped_column(Integer, nullable=True)
    batch_number: Mapped[str] = mapped_column(String(60), nullable=False)
    serial_no: Mapped[str] = mapped_column(String(60), nullable=False)
    unit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    count: Mapped[float | None] = mapped_column(Float, nullable=True)
    comment: Mapped[str | None] = mapped_column(String(128), nullable=True)


class ProductionDataMachine(Base):
    __tablename__ = "production_data_machine"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    work_order_no: Mapped[str] = mapped_column(
        String(60),
        ForeignKey("work_order.no", name="fk_production_data_machine_work_order_no"),
        nullable=False,
    )
    equipment_no: Mapped[str] = mapped_column(
        String(60),
        ForeignKey("equipment.no", name="fk_production_data_machine_equipment_no"),
        nullable=False,
    )
    equipment_name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    time: Mapped[int | None] = mapped_column(Integer, nullable=True)
    action: Mapped[str] = mapped_column(String(60), nullable=False)
    speed: Mapped[float | None] = mapped_column(Float, nullable=True)
    temperature: Mapped[float | None] = mapped_column(Float, nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class ProductionDataLabor(Base):
    __tablename__ = "production_data_labor"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    work_order_no: Mapped[str] = mapped_column(
        String(60),
        ForeignKey("work_order.no", name="fk_production_data_labor_work_order_no"),
        nullable=False,
    )
    employee_no: Mapped[str] = mapped_column(
        String(60),
        ForeignKey("employee.no", name="fk_production_data_labor_employee_no"),
        nullable=False,
    )
    employee_name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    employee_type: Mapped[int | None] = mapped_column(Integer, nullable=True)
    employee_jobTitle: Mapped[int | None] = mapped_column(Integer, nullable=True)
    employee_level: Mapped[int | None] = mapped_column(Integer, nullable=True)
    station_no: Mapped[str | None] = mapped_column(
        String(60),
        ForeignKey("station.no", name="fk_production_data_labor_station_no"),
        nullable=True,
    )
    stationStage: Mapped[int] = mapped_column(Integer, nullable=False)
    action: Mapped[int] = mapped_column(Integer, nullable=False)
    startTime: Mapped[int] = mapped_column(Integer, nullable=False)
    endTime: Mapped[int] = mapped_column(Integer, nullable=False)
    hours: Mapped[float | None] = mapped_column(Float, nullable=True)


class PlManCapacity(Base):
    __tablename__ = "pl_man_capacity"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    month: Mapped[date] = mapped_column(Date, nullable=False)
    pl_no: Mapped[str] = mapped_column(
        String(60),
        ForeignKey("production_line.no", name="fk_pl_man_capacity_pl_no"),
        nullable=False,
    )
    pl_name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    productCount: Mapped[int | None] = mapped_column(Integer, nullable=True)
    laborCount: Mapped[int | None] = mapped_column(Integer, nullable=True)
    unit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    hourlyOutput: Mapped[float | None] = mapped_column(Double, nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class PlItemCapacity(Base):
    __tablename__ = "pl_item_capacity"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    month: Mapped[date] = mapped_column(Date, nullable=False)
    pl_no: Mapped[str] = mapped_column(
        String(60),
        ForeignKey("production_line.no", name="fk_pl_item_capacity_pl_no"),
        nullable=False,
    )
    pl_name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    item_no: Mapped[str] = mapped_column(String(60), nullable=False)
    item_name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    assembly_no: Mapped[str | None] = mapped_column(String(60), nullable=True)
    assemblyVer: Mapped[int | None] = mapped_column(Integer, nullable=True)
    bomWeight: Mapped[float | None] = mapped_column(Double, nullable=True)
    bomUnit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    productCount: Mapped[int | None] = mapped_column(Integer, nullable=True)
    hours: Mapped[float | None] = mapped_column(Float, nullable=True)
    count: Mapped[float | None] = mapped_column(Float, nullable=True)
    unit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    hourlyOutput: Mapped[float | None] = mapped_column(Double, nullable=True)
    price: Mapped[float | None] = mapped_column(Double, nullable=True)
    rawMaterialCost: Mapped[float | None] = mapped_column(Double, nullable=True)
    materialCost: Mapped[float | None] = mapped_column(Double, nullable=True)
    laborCost: Mapped[float | None] = mapped_column(Double, nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class PlItemLoss(Base):
    __tablename__ = "pl_item_loss"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    month: Mapped[date] = mapped_column(Date, nullable=False)
    pl_item_capacity_no: Mapped[str | None] = mapped_column(String(60), nullable=True)
    item_no: Mapped[str] = mapped_column(String(60), nullable=False)
    item_name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    itemCategory: Mapped[int | None] = mapped_column(Integer, nullable=True)
    itemSubCategory: Mapped[int | None] = mapped_column(Integer, nullable=True)
    weightRatio: Mapped[float | None] = mapped_column(Double, nullable=True)
    lossRate: Mapped[float | None] = mapped_column(Double, nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class Employee(Base):
    __tablename__ = "employee"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    no: Mapped[str] = mapped_column(String(20), nullable=False)
    name: Mapped[str | None] = mapped_column(String(60), nullable=True)
    sex: Mapped[int | None] = mapped_column(Integer, nullable=True)
    department: Mapped[int | None] = mapped_column(Integer, nullable=True)
    level: Mapped[int | None] = mapped_column(Integer, nullable=True)
    jobTitle: Mapped[str | None] = mapped_column(String(60), nullable=True)
    joinedDate: Mapped[int | None] = mapped_column(Integer, nullable=True)
    leftDate: Mapped[int | None] = mapped_column(Integer, nullable=True)
    identityId: Mapped[str | None] = mapped_column(String(60), nullable=True)
    country: Mapped[str | None] = mapped_column(String(60), nullable=True)
    birthday: Mapped[int | None] = mapped_column(Integer, nullable=True)
    phone: Mapped[str | None] = mapped_column(String(60), nullable=True)
    address: Mapped[str | None] = mapped_column(String(100), nullable=True)
    type: Mapped[int | None] = mapped_column(Integer, nullable=True)
    category: Mapped[int | None] = mapped_column(Integer, nullable=True)
    comment: Mapped[str | None] = mapped_column(String(128), nullable=True)
    creationTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class Member(Base):
    __tablename__ = "member"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_no: Mapped[str] = mapped_column(
        String(60), ForeignKey("employee.no", name="fk_member_user_no"), nullable=False
    )
    account: Mapped[str | None] = mapped_column(String(60), nullable=True)
    password: Mapped[str | None] = mapped_column(String(100), nullable=True)


class Session(Base):
    __tablename__ = "session"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_no: Mapped[str | None] = mapped_column(
        String(60), ForeignKey("employee.no", name="fk_session_user_no"), nullable=True
    )
    token: Mapped[str | None] = mapped_column(String(60), nullable=True)
    expiredTime: Mapped[int | None] = mapped_column(Integer, nullable=True)


class UserGroup(Base):
    __tablename__ = "user_group"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(60), nullable=False)
    role: Mapped[int | None] = mapped_column(Integer, nullable=True)
    users: Mapped[str | None] = mapped_column(Text, nullable=True)
