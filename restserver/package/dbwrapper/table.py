from sqlalchemy import Column, Integer, String, Float, Time, JSON, orm, ForeignKey, Text, Date, DateTime, func, UniqueConstraint, Index,and_
Base = orm.declarative_base()
from sqlalchemy.orm import relationship, foreign, remote

class CTablePayment(Base):
    __tablename__ = 'payment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Integer)
    source = Column(Integer)
    date = Column(Integer)
    period = Column(Integer)
    creationTime = Column(Integer)
    __table_args__ = (
        UniqueConstraint('type', 'source', 'date', 'period', name='uq_payment_composite'),
    )

class CTableBankAccount(Base):
    __tablename__ = 'bank_account'
    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(Integer)
    currency = Column(Integer)
    displayName = Column(String(length=60))
    name = Column(String(length=60))
    branch = Column(String(length=60))
    account = Column(String(length=60))
    number = Column(String(length=60), unique=True)
    creationTime = Column(Integer)

class CTableEnterprise(Base):
    __tablename__ = 'enterprise'
    id = Column(Integer, primary_key=True, autoincrement=True)
    no = Column(String(length=60))
    businessNo = Column(String(length=60))
    displayName = Column(String(length=60))
    name = Column(String(length=60))
    address = Column(String(length=100))
    phone = Column(String(length=100))
    fax = Column(String(length=20))
    lar = Column(String(length=60))
    department = Column(Integer)
    comment = Column(String(length=128))
    creationTime = Column(Integer)
    __table_args__ = (
        UniqueConstraint('no', 'businessNo', name='uq_enterprise_composite'),
    )

class CTableCompany(Base):
    __tablename__ = 'company'
    id = Column(Integer, primary_key=True, autoincrement=True)
    no = Column(String(length=60))
    businessNo = Column(String(length=60))
    displayName = Column(String(length=60))
    name = Column(String(length=60))
    address = Column(String(length=100))
    phone = Column(String(length=100))
    fax = Column(String(length=20))
    contactName = Column(String(length=60))
    contactPhone = Column(JSON)
    contactTitle = Column(String(length=60))
    contactEmail = Column(String(length=60))
    received_id = Column(String(length=60))
    paid_id = Column(String(length=60))
    bankCurrency = Column(Integer)
    bankDisplayName = Column(String(length=60))
    bankName = Column(String(length=60))
    bankBranch = Column(String(length=60))
    bankAccount = Column(String(length=60))
    bankNo = Column(String(length=60))
    comment = Column(String(length=128))
    creationTime = Column(Integer)
    __table_args__ = (
        UniqueConstraint('no', 'businessNo', name='uq_company_composite'),
    )

class CTableTransItems(Base):
    __tablename__ = 'trans_items'
    id = Column(Integer, primary_key=True, autoincrement=True)
    no = Column(String(length=60))
    name = Column(String(length=100))
    category = Column(Integer)
    attribute = Column(Integer)
    company_no = Column(String(length=60))
    company_displayName = Column(String(length=60))
    item_no = Column(String(length=60))
    item_name = Column(String(length=60))
    comment = Column(String(length=128))
    creationTime = Column(Integer)

    contracts = relationship(
        "CTableContract",
        primaryjoin="CTableTransItems.no == foreign(CTableContract.item_no)",
        uselist=True
    )

    __table_args__ = (
        UniqueConstraint('no', name='uq_trans_items_composite'),
    )

class CTableTransItems2(Base):
    __tablename__ = 'trans_items2'
    id = Column(Integer, primary_key=True, autoincrement=True)
    no = Column(String(length=60))
    name = Column(String(length=100))
    category = Column(Integer)
    attribute = Column(Integer)
    company_no = Column(String(length=60))
    company_displayName = Column(String(length=60))
    comment = Column(String(length=128))
    creationTime = Column(Integer)
    __table_args__ = (
        UniqueConstraint('no', name='uq_trans_items2_composite'),
    )
class CTableMaterial(Base):
    __tablename__ = 'material'
    id = Column(Integer, primary_key=True, autoincrement=True)
    no = Column(String(length=60))
    category = Column(Integer)
    subCategory = Column(Integer)
    name = Column(String(length=100))
    unitShipping = Column(Integer)
    unitWarehouse = Column(Integer)
    unitProduct = Column(Integer)
    comment = Column(String(length=128))
    creationTime = Column(Integer)
    __table_args__ = (
        UniqueConstraint('no', name='uq_material_composite'),
    )

class CTableItemPrice(Base):
    __tablename__ = 'item_price'
    id = Column(Integer, primary_key=True, autoincrement=True)
    item_no = Column(String(length=60))
    item_name = Column(String(length=100))
    itemCategory = Column(Integer)
    date = Column(Integer)
    whUnitWeight = Column(Integer)
    whUnitLength = Column(Integer)
    costUnitWeight = Column(Integer)
    costUnitLength = Column(Integer)
    estWHPriceWeight = Column(Float)
    estWHPriceWeight1 = Column(Float)
    estWHPriceWeight2 = Column(Float)
    estWHPriceLength = Column(Float)
    estCostPriceWeight = Column(Float)
    estCostPriceWeight1 = Column(Float)
    estCostPriceWeight2 = Column(Float)
    estCostPriceLength = Column(Float)
    estLaborCost = Column(Float)
    whPriceWeight = Column(Float)
    whPriceWeight1 = Column(Float)
    whPriceWeight2 = Column(Float)
    whPriceLength = Column(Float)
    costPriceWeight = Column(Float)
    costPriceWeight1 = Column(Float)
    costPriceWeight2 = Column(Float)
    costPriceLength = Column(Float)
    laborCost = Column(Float)
    creationTime = Column(Float)
    __table_args__ = (
        UniqueConstraint('item_no', 'date', name='uq_item_price_composite'),
    )

    # 1. 對應 Material ([1, 2, 3])
    material = relationship(
        "CTableMaterial",
        primaryjoin="CTableItemPrice.item_no == foreign(CTableMaterial.no)",
        uselist=False
    )

    # 2. 對應 InProduct (4)
    inproduct = relationship(
        "CTableInproduct",
        primaryjoin="CTableItemPrice.item_no == foreign(CTableInproduct.no)",
        uselist=False
    )

    # 3. 對應 Product (5)
    product = relationship(
        "CTableProduct",
        primaryjoin="CTableItemPrice.item_no == foreign(CTableProduct.no)",
        uselist=False
    )

    # 3. 對應 Product (6)
    goods = relationship(
        "CTableGoods",
        primaryjoin="CTableItemPrice.item_no == foreign(CTableGoods.no)",
        uselist=False
    )

    trans_items = relationship(
        "CTableTransItems",
        primaryjoin="CTableItemPrice.item_no == foreign(CTableTransItems.item_no)",
        uselist=True
    )


class CTableItemLoss(Base):
    __tablename__ = 'item_loss'
    id = Column(Integer, primary_key=True, autoincrement=True)
    item_no = Column(String(length=60))
    itemCategory = Column(Integer)
    date = Column(Integer)
    unit = Column(Integer)
    value = Column(Float)
    estValue = Column(Float)
    creationTime = Column(Float)
    __table_args__ = (
        UniqueConstraint('item_no', 'date', name='uq_item_loss_composite'),
    )


class CTableItemHours(Base):
    __tablename__ = 'item_hours'
    id = Column(Integer, primary_key=True, autoincrement=True)
    item_no = Column(String(length=60))
    itemCategory = Column(Integer)
    date = Column(Integer, unique=True)
    unit = Column(Integer)
    value = Column(Float)
    estValue = Column(Float)
    creationTime = Column(Float)
    __table_args__ = (
            UniqueConstraint('item_no', 'date', name='uq_item_hours_composite'),
        )
class CTableSamplePrice(Base):
    __tablename__ = 'sample_price'
    id = Column(Integer, primary_key=True, autoincrement=True)
    item_no = Column(String(length=60))
    date = Column(Integer)
    estWHUnitWeight = Column(Integer)
    estWHPriceWeight = Column(Float)
    estCostUnitWeight = Column(Integer)
    estCostPriceWeight = Column(Float)
    estLaborCost = Column(Float)
    whUnitWeight = Column(Integer)
    whPriceWeight = Column(Float)
    costUnitWeight = Column(Integer)
    costPriceWeight = Column(Float)
    laborCost = Column(Float)
    creationTime = Column(Float)
    __table_args__ = (
        UniqueConstraint('item_no', 'date', name='uq_sample_price_composite'),
    )


class CTableBatchNumber(Base):
    __tablename__ = 'batch_number'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Integer)
    no = Column(String(length=60))
    creator_no = Column(String(length=60))
    ref_no = Column(String(length=60))
    refCategory = Column(Integer)

    item_no = Column(String(length=60))
    item_name = Column(String(length=60))
    item_ref_no = Column(String(length=60))
    item_ref_displayName = Column(String(length=60))
    itemCategory = Column(Integer)
    itemSubCategory = Column(Integer)
    itemType = Column(Integer)
    unit = Column(Integer)
    expectedCount = Column(Float)
    checkedCount = Column(Float)
    validDays = Column(Integer)
    validDate = Column(Integer)
    validDateNo = Column(String(length=60))
    comment = Column(String(length=128))
    creationTime = Column(Integer)
    __table_args__ = (
        UniqueConstraint('no', 'ref_no', name='uq_batch_number_composite'),
    )
    serialNo_data = relationship(
        "CTableBatchNoSerialNo",
        backref=None,  # 不需要反向回去
        lazy="select",  # 預設延遲載入
        cascade="all, delete-orphan",
        foreign_keys="[CTableBatchNoSerialNo.batch_number]",
        primaryjoin="CTableBatchNumber.no == foreign(CTableBatchNoSerialNo.batch_number)"
    )


class CTableBatchNoSerialNo(Base):
    __tablename__ = 'batchno_serialno'
    id = Column(Integer, primary_key=True, autoincrement=True)
    batch_number = Column(String(length=60),ForeignKey('batch_number.no'))
    serialNo = Column(String(length=60))
    #batchno_data = relationship("CTableBatchNumber", back_populates="serialNo_data")
    ref_order_no = Column(String(length=60))
    ref_order_no_category = Column(Integer)
    time = Column(Integer)
    unit = Column(Integer)
    expectedCount = Column(Float)
    count = Column(Float)
    validDate = Column(Integer)
    warehouse_no = Column(String(length=60))
    updatedTime = Column(Integer)
    __table_args__ = (
        UniqueConstraint('batch_number', 'serialNo', 'ref_order_no', name='uq_batchno_serialno_composite'),
    )
#CTableBatchNumber.serialNo_data = relationship("CTableBatchNoSerialNo", order_by=CTableBatchNoSerialNo.batch_number, back_populates="batchno_data")

class CTableInventoryOrder(Base):
    __tablename__ = 'inventory_order'
    id = Column(Integer, primary_key=True, autoincrement=True)
    no = Column(String(length=60))
    creator_no = Column(String(length=60))
    date = Column(Integer)
    category = Column(Integer)
    subCategory = Column(Integer)
    item_no = Column(String(length=60))
    item_name = Column(String(length=60))
    item_ref_no = Column(String(length=60))
    item_ref_displayName = Column(String(length=60))
    itemCategory = Column(Integer)
    itemType = Column(Integer)
    unit = Column(Integer)
    price = Column(Float)
    expectedCount = Column(Float)
    checkedCount = Column(Float)
    amount = Column(Integer)
    comment = Column(String(length=128))
    creationTime = Column(Integer)
    __table_args__ = (
        UniqueConstraint('no', name='uq_inventory_order_composite'),
    )

class CTableInventoryRec(Base):
    __tablename__ = 'inventory_record'
    id = Column(Integer, primary_key=True, autoincrement=True)
    group = Column(String(length=60))
    creator_no = Column(String(length=60))
    refCategory = Column(Integer)
    ref_no = Column(String(length=60))
    warehouse_no = Column(String(length=60))
    warehouse_displayName = Column(String(length=60))
    date = Column(Integer)
    source = Column(Integer)
    category = Column(Integer)
    batchNumber = Column(String(length=20))
    serialNo = Column(String(length=60))
    item_no = Column(String(length=60))
    item_name = Column(String(length=60))
    item_ref_no = Column(String(length=60))
    item_ref_displayName = Column(String(length=60))
    itemCategory = Column(Integer)
    itemType = Column(Integer)
    unit = Column(Integer)
    count = Column(Float)
    price = Column(Float)
    amount = Column(Integer)
    comment = Column(String(length=128))
    creationTime = Column(Integer)
    registerDevId = Column(String(length=60))


class CTableShipWarehouseAlias(Base):
    __tablename__ = 'ship_wh_alias'
    id = Column(Integer, primary_key=True, autoincrement=True)
    no = Column(String(length=60))
    name = Column(String(length=60))
    category = Column(Integer)
    type = Column(Integer)
    creationTime = Column(Integer)
    __table_args__ = (
        UniqueConstraint('no', name='uq_ship_wh_alias_composite'),
    )
class CTableShipWarehouse(Base):
    __tablename__ = 'ship_wh'
    id = Column(Integer, primary_key=True, autoincrement=True)
    no = Column(String(length=60))
    company_no = Column(String(length=60))
    company_displayName = Column(String(length=60))
    name = Column(String(length=60))
    category = Column(Integer)
    attribute = Column(Integer)
    maxCapacity = Column(Integer)
    unit = Column(Integer)
    comment = Column(String(length=128))
    creationTime = Column(Integer)
    __table_args__ = (
        UniqueConstraint('no', name='uq_ship_wh_composite'),
    )

class CTableShipWarehouseContract(Base):
    __tablename__ = 'ship_wh_contract'
    id = Column(Integer, primary_key=True, autoincrement=True)
    no = Column(String(length=60), unique=True)
    date = Column(Integer)
    displayName = Column(String(length=60))
    ref_no = Column(String(length=60))
    sw_alias_no = Column(String(length=60))
    item_no = Column(String(length=60))
    item_name = Column(String(length=60))
    item_ref_no = Column(String(length=60))
    item_ref_displayName = Column(String(length=60))
    category = Column(Integer)
    type = Column(Integer)
    itemStyle = Column(Integer)
    region = Column(Integer)
    unit = Column(Integer)
    price = Column(Float)
    fee = Column(Float)
    comment = Column(String(length=128))
    creationTime = Column(Integer)
    __table_args__ = (
        UniqueConstraint('no', 'date', name='uq_ship_wh_contract_composite'),
    )
class CTableShipWarehouseQuotation(Base):
    __tablename__ = 'ship_wh_quotation'
    id = Column(Integer, primary_key=True, autoincrement=True)
    no = Column(String(length=60))
    date = Column(Integer)
    item_no = Column(String(length=60))
    item_name = Column(String(length=60))
    item_ref_no = Column(String(length=60))
    item_ref_displayName = Column(String(length=60))
    category = Column(Integer)
    type = Column(Integer)
    itemStyle = Column(Integer)
    region = Column(Integer)
    unit = Column(Integer)
    price = Column(Float)
    fee = Column(Float)
    comment = Column(String(length=128))
    creationTime = Column(Integer)
    __table_args__ = (
        UniqueConstraint('no', 'date', name='uq_ship_wh_quotation_composite'),
    )
class CTableShippingRec(Base):
    __tablename__ = 'shipping_record'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Integer)
    refCategory = Column(Integer)
    ref_no = Column(String(length=60))
    ref_parent_no = Column(String(length=60))
    sw_alias_no = Column(String(length=60))
    sw_alias_name = Column(String(length=60))
    item_no = Column(String(length=60))
    item_name = Column(String(length=60))
    item_ref_no = Column(String(length=60))
    item_ref_displayName = Column(String(length=60))
    contract_no = Column(String(length=60))
    unit = Column(Integer)
    price = Column(Float)
    count = Column(Integer)
    checkedCount = Column(Integer)
    comment = Column(String(length=128))
    creationTime = Column(Integer)


class CTableWarehouseRec(Base):
    __tablename__ = 'warehouse_record'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Integer)
    ref_no = Column(String(length=60))
    batch_no = Column(String(length=60))
    sw_alias_no = Column(String(length=60))
    sw_alias_name = Column(String(length=60))
    item_no = Column(String(length=60))
    item_name = Column(String(length=60))
    item_ref_no = Column(String(length=60))
    item_ref_displayName = Column(String(length=60))
    contract_no = Column(String(length=60))
    inboundTime = Column(Integer)
    unit = Column(Integer)
    price = Column(Float)
    count = Column(Float)
    days = Column(Float)
    comment = Column(String(length=128))
    creationTime = Column(Integer)


class CTableProductOrder(Base):
    __tablename__ = 'product_order'
    id = Column(Integer, primary_key=True, autoincrement=True)
    no = Column(String(length=60))
    creator_no = Column(String(length=60))
    date = Column(Integer)
    ref_no = Column(String(length=60))
    item_no = Column(String(length=60))
    item_name = Column(String(length=60))
    item_ref_no = Column(String(length=60))
    item_ref_displayName = Column(String(length=60))
    unit = Column(Integer)
    price = Column(Float)
    count = Column(Float)
    preparedCount = Column(Float)
    amount = Column(Integer)
    expectedDate = Column(Integer)
    address = Column(String(length=100))
    payment_type = Column(Integer)
    payment_source = Column(Integer)
    payment_date = Column(Integer)
    payment_period = Column(Integer)
    comment = Column(String(length=128))
    creationTime = Column(Integer)
    __table_args__ = (
        UniqueConstraint('no', name='uq_product_order_composite'),
    )

class CTableShippingOrder(Base):
    __tablename__ = 'shipping_order'
    id = Column(Integer, primary_key=True, autoincrement=True)
    no = Column(String(length=60))
    creator_no = Column(String(length=60))
    product_order_no = Column(String(length=60))
    date = Column(Integer)
    category = Column(Integer)
    item_no = Column(String(length=60))
    item_name = Column(String(length=60))
    item_ref_no = Column(String(length=60))
    item_ref_displayName = Column(String(length=60))
    itemCategory = Column(Integer)
    itemSubCategory = Column(Integer)
    unit = Column(Integer)
    price = Column(Float)
    expectedCount = Column(Float)
    checkedCount = Column(Float)
    feeCount = Column(Float) # 沒使用
    amount = Column(Integer)
    addDeleteAmount = Column(Integer)

    comment = Column(String(length=128))
    creationTime = Column(Integer)
    __table_args__ = (
        UniqueConstraint('no', name='uq_shipping_order_composite'),
    )





class CTablePurchaseRequest(Base):
    __tablename__ = 'purchase_request '
    id = Column(Integer, primary_key=True, autoincrement=True)
    no = Column(String(length=60))
    creator_no = Column(String(length=60))
    product_order_no = Column(String(length=60))
    date = Column(Integer)
    item_no = Column(String(length=60))
    unit = Column(Integer)
    count = Column(Float)
    expectedDate = Column(Integer)
    comment = Column(String(length=128))
    creationTime = Column(Integer)
    __table_args__ = (
        UniqueConstraint('no','product_order_no','item_no', name='uq_purchase_request_composite'),
    )


class CTablePurchaseOrder(Base):
    __tablename__ = 'purchase_order'
    id = Column(Integer, primary_key=True, autoincrement=True)
    no = Column(String(length=60))
    creator_no = Column(String(length=60))
    purchase_request_no = Column(String(length=60))
    date = Column(Integer)
    ref_no = Column(String(length=60))
    item_ref_no           = Column(String(length=60))
    item_ref_displayName  = Column(String(length=60))
    item_no           = Column(String(length=60))
    item_name         = Column(String(length=60))
    unit = Column(Integer)
    price = Column(Float)
    count = Column(Float)
    amount = Column(Integer)
    expectedDate = Column(Integer)
    address = Column(String(length=100))
    payment_type = Column(Integer)
    payment_source = Column(Integer)
    payment_date = Column(Integer)
    payment_period = Column(Integer)
    comment = Column(String(length=128))
    creationTime = Column(Integer)
    __table_args__ = (
        UniqueConstraint('no', name='uq_purchase_order_composite'),
    )

class CTableGoodsReceiptNote (Base):
    __tablename__ = 'goods_receipt_note'
    id = Column(Integer, primary_key=True, autoincrement=True)
    no = Column(String(length=60))
    creator_no = Column(String(length=60))
    purchase_order_no = Column(String(length=60))
    date                  = Column(Integer)
    category              = Column(Integer)
    item_ref_no           = Column(String(length=60))
    item_ref_displayName  = Column(String(length=60))
    item_no           = Column(String(length=60))
    item_name         = Column(String(length=60))
    itemCategory = Column(Integer)
    itemSubCategory = Column(Integer)
    unit                  = Column(Integer)
    price                 =  Column(Float)
    expectedCount         =  Column(Float)
    checkedCount = Column(Float)
    feeCount = Column(Float) # 沒使用
    amount= Column(Integer)
    addDeleteAmount= Column(Integer)

    comment               = Column(String(length=128))
    creationTime          = Column(Integer)
    __table_args__ = (
        UniqueConstraint('no', name='uq_goods_receipt_note_composite'),
    )


class CTableWorkOrder(Base):
    __tablename__ = 'work_order'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Integer)
    no = Column(String(length=60))
    creator_no = Column(String(length=60))
    product_order_no = Column(String(length=60), ForeignKey('product_order.no'))
    product_order = relationship("CTableProductOrder", back_populates="work_order")
    aps_no = Column(String(length=60))
    customer_no = Column(String(length=60))
    customer_displayName = Column(String(length=60))
    product_no = Column(String(length=60))
    product_name = Column(String(length=100))
    output_item_no = Column(String(length=60))
    output_item_name = Column(String(length=100))
    production_line_no = Column(String(length=60))
    oneProcess = Column(Integer)
    secProcess = Column(Integer)
    startTime = Column(Integer)
    endTime = Column(Integer)
    processUnit = Column(Integer)
    processTime = Column(Integer)
    processCount = Column(Float)
    laborCount = Column(Integer)
    laborList = Column(JSON)

    comment = Column(String(length=128))
    creationTime = Column(Integer)
    __table_args__ = (
        UniqueConstraint('no', name='uq_work_order_composite'),
    )
CTableProductOrder.work_order = relationship("CTableWorkOrder", order_by=CTableProductOrder.no, back_populates="product_order")



class CTableProductionData(Base):
    __tablename__ = 'production_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    creator_no = Column(String(length=60))

    work_order_no = Column(String(length=60), ForeignKey('work_order.no'))
    work_order = relationship("CTableWorkOrder", back_populates="production_data")

    product_order_no = Column(String(length=60))
    customer_no = Column(String(length=60))
    customer_displayName = Column(String(length=60))
    product_no = Column(String(length=60))
    product_name = Column(String(length=100))
    date = Column(Integer)
    production_line_no = Column(String(length=60))
    oneProcess = Column(Integer)
    secProcess = Column(Integer)
    item_no = Column(String(length=60))
    item_name = Column(String(length=100))
    materialLoss = Column(Float)
    creationTime = Column(Integer)
    __table_args__ = (
        UniqueConstraint('work_order_no', name='uq_production_data_composite'),
    )
CTableWorkOrder.production_data = relationship("CTableProductionData", order_by=CTableProductionData.work_order_no, back_populates="work_order")


class CTableProductionDataInput(Base):
    __tablename__ = 'production_data_input'
    id = Column(Integer, primary_key=True, autoincrement=True)

    work_order_no = Column(String(length=60), ForeignKey('production_data.work_order_no'))
    production_data = relationship("CTableProductionData", back_populates="input_data")
    process_order_no = Column(String(length=60))
    group = Column(String(length=60))
    time            = Column(Integer)
    action            = Column(Integer)
    item_no            = Column(String(length=60))
    item_name          = Column(String(length=100))
    category = Column(Integer) #itemCategory
    itemSubCategory    = Column(Integer)
    batch_number       = Column(String(length=60))
    serial_no          = Column(String(length=60))
    unit               = Column(Integer)
    count              = Column(Float)
    comment = Column(String(length=128))

    __table_args__ = (
        UniqueConstraint('work_order_no', 'group', 'action', 'item_no', 'batch_number', 'serial_no', name='uq_production_data_input_composite'),
    )
CTableProductionData.input_data = relationship("CTableProductionDataInput", order_by=CTableProductionDataInput.work_order_no, back_populates="production_data")


class CTableProductionDataOutput(Base):
    __tablename__ = 'production_data_output'
    id = Column(Integer, primary_key=True, autoincrement=True)
    work_order_no = Column(String(length=60), ForeignKey('production_data.work_order_no'))
    production_data = relationship("CTableProductionData", back_populates="output_data")
    process_order_no = Column(String(length=60))

    time            = Column(Integer)
    action            = Column(Integer)
    group = Column(String(length=60))
    item_no            = Column(String(length=60))
    item_name          = Column(String(length=100))
    category           = Column(Integer)
    itemSubCategory    = Column(Integer)
    batch_number       = Column(String(length=60))
    serial_no          = Column(String(length=60))
    unit               = Column(Integer)
    count              = Column(Float)
    valid_date         = Column(Integer)
    valid_date_no      = Column(String(length=60))
    comment = Column(String(length=128))
    __table_args__ = (
        UniqueConstraint('work_order_no', 'group', 'action', 'item_no', 'batch_number', 'serial_no',
                         name='uq_production_data_output_composite'),
    )
CTableProductionData.output_data = relationship("CTableProductionDataOutput", order_by=CTableProductionDataOutput.work_order_no, back_populates="production_data")

class CTableProductionDataReuse(Base):
    __tablename__ = 'production_data_reuse'
    id = Column(Integer, primary_key=True, autoincrement=True)
    work_order_no = Column(String(length=60), ForeignKey('production_data.work_order_no'))
    process_order_no = Column(String(length=60))
    production_data = relationship("CTableProductionData", back_populates="reuse_data")
    group = Column(String(length=60))
    time            = Column(Integer)
    action            = Column(Integer)
    item_no            = Column(String(length=60))
    item_name          = Column(String(length=100))
    itemSubCategory    = Column(Integer)
    category           = Column(Integer)
    batch_number       = Column(String(length=60))
    serial_no          = Column(String(length=60))
    unit               = Column(Integer)
    count              = Column(Float)
    comment = Column(String(length=128))
    __table_args__ = (
        UniqueConstraint('work_order_no',  'group', 'action', 'item_no', 'batch_number', 'serial_no', 'category', name='uq_production_data_reuse_composite'),
    )
CTableProductionData.reuse_data = relationship("CTableProductionDataReuse", order_by=CTableProductionDataReuse.work_order_no, back_populates="production_data")

class CTableProductionDataLabor(Base):
    __tablename__ = 'production_data_labor'
    id = Column(Integer, primary_key=True, autoincrement=True)

    work_order_no     = Column(String(length=60), ForeignKey('production_data.work_order_no'))
    production_data = relationship("CTableProductionData", back_populates="labor_data")
    employee_no       = Column(String(length=60))
    employee_name     = Column(String(length=100))
    employee_type     = Column(Integer)
    employee_jobTitle = Column(Integer)
    employee_level    = Column(Integer)
    station_no        = Column(String(length=60))
    action            = Column(Integer)
    stationStage       = Column(Integer)
    startTime     = Column(Integer)
    endTime       = Column(Integer)
    hours = Column(Float)
    __table_args__ = (
        UniqueConstraint('work_order_no', 'employee_no', 'stationStage', 'action', 'startTime', 'endTime', name='uq_production_data_labor_composite'),
    )
CTableProductionData.labor_data = relationship("CTableProductionDataLabor", order_by=CTableProductionDataLabor.work_order_no, back_populates="production_data")


class CTableProductionDataMachine(Base):
    __tablename__ = 'production_data_machine'
    id = Column(Integer, primary_key=True, autoincrement=True)
    work_order_no     = Column(String(length=60), ForeignKey('production_data.work_order_no'))
    production_data = relationship("CTableProductionData", back_populates="machine_data")
    time             = Column(Integer)
    equipment_no       = Column(String(length=60))
    equipment_name     = Column(String(length=100))
    action             = Column(Integer)
    temperature        = Column(Float)
    speed             = Column(Float)
    creationTime       = Column(Integer)
    __table_args__ = (
        UniqueConstraint('work_order_no', 'equipment_no', 'action', name='uq_production_data_machine_composite'),
    )
CTableProductionData.machine_data = relationship("CTableProductionDataMachine", order_by=CTableProductionDataMachine.work_order_no, back_populates="production_data")



class CTableSession(Base):
    __tablename__ = 'session'
    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String(length=60))
    user_no = Column(String(length=60))
    expiredTime = Column(Integer)


class CTableMember(Base):
    __tablename__ = 'member'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_no = Column(String(length=60), unique=True)
    account = Column(String(length=60))
    password = Column(String(length=100))
    __table_args__ = (
        UniqueConstraint('user_no', name='uq_member_composite'),
    )
class CTableUserGroup(Base):
    __tablename__ = 'user_group'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=60))
    role = Column(Integer)
    users = Column(JSON)
    privileges = Column(JSON)
    __table_args__ = (
        UniqueConstraint('name', name='uq_user_group_composite'),
    )

class CTableInproduct(Base):
    __tablename__ = 'inproduct'
    id = Column(Integer, primary_key=True, autoincrement=True)
    no = Column(String(length=60))
    category = Column(Integer)
    name = Column(String(length=100))
    unitShipping = Column(Integer)
    unitWarehouse = Column(Integer)
    unitProduct = Column(Integer)
    comment = Column(String(length=128))
    creationTime = Column(Integer)
    __table_args__ = (
        UniqueConstraint('no', name='uq_inproduct_composite'),
    )
    bom_specs = relationship("CTableInproductBOMSpec", back_populates="inproduct_data", lazy='select')


class CTableProduct(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True, autoincrement=True)
    no = Column(String(length=60))
    category = Column(Integer)
    name = Column(String(length=100))
    unitShipping = Column(Integer)
    unitWarehouse = Column(Integer)
    unitProduct = Column(Integer)
    version = Column(Integer)
    comment = Column(String(length=128))
    creationTime = Column(Integer)
    __table_args__ = (
        UniqueConstraint('no', name='uq_product_composite'),
    )
class CTableGoods(Base):
    __tablename__ = 'goods'
    id = Column(Integer, primary_key=True, autoincrement=True)
    no = Column(String(length=60))
    category = Column(Integer)
    subCategory = Column(Integer)
    name = Column(String(length=100))
    unitShipping = Column(Integer)
    unitWarehouse = Column(Integer)
    unitProduct = Column(Integer)
    comment = Column(String(length=128))
    creationTime = Column(Integer)
    __table_args__ = (
        UniqueConstraint('no', name='uq_goods_composite'),
    )
class CTableBOM(Base):
    __tablename__ = 'bom'
    id = Column(Integer, primary_key=True, autoincrement=True)
    no = Column(String(length=60))
    displayName = Column(String(length=60))
    date = Column(Integer)
    unit = Column(Integer)
    weight = Column(Float)
    version = Column(Float)
    comment = Column(String(length=128))
    creationTime = Column(Integer)
    item_data = relationship("CTableBOMItem", order_by="CTableBOMItem.item_no", back_populates="bom_data", lazy='select')
    __table_args__ = (
        UniqueConstraint('no', 'version', name='uq_bom_composite'),
    )

class CTableBOMItem(Base):
    __tablename__ = 'bom_item'
    id = Column(Integer, primary_key=True, autoincrement=True)
    bom_no = Column(String(length=60), ForeignKey('bom.no'))
    item_no = Column(String(length=60))
    item_name = Column(String(length=60))
    unit = Column(Integer)
    weight = Column(Float)
    creationTime = Column(Integer)
    __table_args__ = (
        UniqueConstraint('bom_no', 'item_no', name='uq_bom_item_composite'),
    )
    bom_data = relationship("CTableBOM", back_populates="item_data")


class CTableBOM1Number(Base):
    __tablename__ = 'bom1_number'
    id = Column(Integer, primary_key=True, autoincrement=True)
    no = Column(String(length=60))
    displayName = Column(String(length=60))
    unit = Column(Integer)
    weight = Column(Float)
    bom_no = Column(String(length=60))
    bom_version = Column(Integer)
    comment = Column(String(length=128))
    creationTime = Column(Integer)
    __table_args__ = (
        UniqueConstraint('no', name='uq_bom1_number_composite'),
    )

class CTableBOM1(Base):
    __tablename__ = 'bom1'
    id = Column(Integer, primary_key=True, autoincrement=True)
    parent_no = Column(String(length=60))
    parent_name = Column(String(length=60))
    child_category = Column(Integer)
    child_id = Column(String(length=60))
    child_name = Column(String(length=60))
    childUnit = Column(Integer)
    weight = Column(Float)
    expectedLoss = Column(Float)
    actualLoss = Column(Float)
    processWeight = Column(Float)
    comment = Column(String(length=128))
    creationTime = Column(Integer)
    __table_args__ = (
        UniqueConstraint('parent_no', 'child_id', 'weight', name='uq_bom1_composite'),
    )

class CTableBOM2Number(Base):
    __tablename__ = 'bom2_number'
    id = Column(Integer, primary_key=True, autoincrement=True)
    #bom2_data = relationship("CTableInproductBOMSpec", backref="CTableBOM2Number")
    no = Column(String(length=60))
    displayName = Column(String(length=60))
    unit = Column(Integer)
    weight = Column(Float)
    bom_no = Column(String(length=60))
    bom_version = Column(Integer)
    comment = Column(String(length=128))
    creationTime = Column(Integer)
    __table_args__ = (
        UniqueConstraint('no', name='uq_bom2_number_composite'),
    )

class CTableBOM2(Base):
    __tablename__ = 'bom2'
    id = Column(Integer, primary_key=True, autoincrement=True)
    parent_no = Column(String(length=60))
    parent_name = Column(String(length=60))
    child_category = Column(Integer)
    child_id = Column(String(length=60))
    child_name = Column(String(length=60))
    childUnit = Column(Integer)
    count = Column(Integer)
    childUnit2 = Column(Integer)
    weight = Column(Float)
    length = Column(Float)
    expectedLoss = Column(Float)
    actualLoss = Column(Float)
    processCount = Column(Float)
    comment = Column(String(length=128))
    creationTime = Column(Integer)


class CTableInproductBOMSpec(Base):
    __tablename__ = 'inproduct_bom_spec'
    id = Column(Integer, primary_key=True, autoincrement=True)
    inproduct_no = Column(String(length=60), ForeignKey('inproduct.no'))
    category = Column(Integer)
    item_no = Column(String(length=60))
    item_version = Column(Integer)
    bom12_no = Column(String(length=60))
    count = Column(Integer)
    unit = Column(Integer)
    weight = Column(Float)
    __table_args__ = (
        UniqueConstraint('inproduct_no', 'item_no', 'item_version', 'bom12_no', name='uq_inproduct_bom_spec_composite'),
    )
    inproduct_data = relationship("CTableInproduct", back_populates="bom_specs", lazy='select')


class CTableProductSpec(Base):
    __tablename__ = 'product_spec'
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_no = Column(String(length=60))
    product_version = Column(Integer)
    bom_no = Column(String(length=60))
    bom_version = Column(Integer)
    level = Column(Integer)
    item_type = Column(Integer)
    item_no = Column(String(length=60))
    count = Column(Integer)
    unit = Column(Integer)
    weight = Column(Float)
    expectedLoss = Column(Float)
    actualLoss = Column(Float)
    __table_args__ = (
        UniqueConstraint('product_no', 'product_version', 'item_no', name='uq_product_spec_composite'),
    )

class CTableProductBOMSpec(Base):
    __tablename__ = 'product_bom_spec'
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_no = Column(String(length=60))
    product_version = Column(Integer)
    level = Column(Integer)
    bom2_no = Column(String(length=60))
    count = Column(Integer)
    unit = Column(Integer)
    weight = Column(Float)
    __table_args__ = (
        UniqueConstraint('product_no', 'product_version', 'bom2_no', name='uq_product_bom_spec_composite'),
    )

class CTableProcessOrder (Base):
    __tablename__ = 'process_order'
    id = Column(Integer, primary_key=True, autoincrement=True)
    no = Column(String(length=60))
    creator_no = Column(String(length=60))
    work_order_no = Column(String(length=60))
    refProcess = Column(Integer)
    date = Column(Integer)
    category = Column(Integer)
    item_no = Column(String(length=60))
    item_name = Column(String(length=60))
    item_ref_no = Column(String(length=60))
    item_ref_displayName = Column(String(length=60))
    itemCategory = Column(Integer)
    itemSubCategory = Column(Integer)

    unit = Column(Integer)
    expectedCount = Column(Float)
    count = Column(Float)
    comment = Column(String(length=128))
    creationTime = Column(Integer)
    __table_args__ = (
        UniqueConstraint('no', name='uq_process_order_composite'),
    )

class CTableEmployee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True, autoincrement=True)
    no = Column(String(length=60))
    name = Column(String(length=60))
    type = Column(Integer)
    level = Column(Integer)
    category = Column(Integer)
    sex = Column(Integer)
    department = Column(Integer)
    jobTitle = Column(String(length=60))
    joinedDate = Column(Integer)
    leftDate = Column(Integer)
    identityId = Column(String(length=60))
    country = Column(String(length=60))
    birthday = Column(Integer)
    phone = Column(String(length=60))
    address = Column(String(length=100))

    comment = Column(String(length=60))
    creationTime = Column(Integer)
    __table_args__ = (
        UniqueConstraint('no', name='uq_employee_composite'),
    )

class CTableProcess(Base):
    __tablename__ = 'process'
    id = Column(Integer, primary_key=True, autoincrement=True)
    no = Column(String(length=60))
    oneProcess = Column(Integer)
    secProcess = Column(Integer)
    comment = Column(String(length=128))
    creationTime = Column(Integer)
    __table_args__ = (
        UniqueConstraint('no', name='uq_process_composite'),
    )

class CTableFactory(Base):
    __tablename__ = 'factory'
    id = Column(Integer, primary_key=True, autoincrement=True)
    no = Column(String(length=60))
    region = Column(String(length=60))
    location = Column(String(length=60))
    comment = Column(String(length=128))

    __table_args__ = (
        UniqueConstraint('no', name='uq_factory_composite'),
    )
    # 1(Factory) → 多(ProductLine)
    line_data = relationship("CTableProductLine", back_populates="factory_data")
class CTableProductLine(Base):
    __tablename__ = 'production_line'
    id = Column(Integer, primary_key=True, autoincrement=True)
    no = Column(String(length=60))
    name = Column(String(length=60))
    process_no = Column(String(length=60))
    oneProcess = Column(Integer)
    secProcess = Column(Integer)
    factory_no = Column(String(60), ForeignKey("factory.no"))
    location = Column(String(60))
    capacityUnit = Column(Integer)
    capacity = Column(Float)
    laborCount = Column(Integer)
    laborEfficiency = Column(Float)
    comment = Column(String(128))
    creationTime = Column(Integer)
    __table_args__ = (
        UniqueConstraint('no', name='uq_production_line_composite'),
    )

    # 多(ProductLine) → 1(Factory)
    factory_data = relationship("CTableFactory", back_populates="line_data")

    # 1 → N station
    station_data = relationship("CTableStation", back_populates="line_data")

class CTableStation(Base):
    __tablename__ = 'station'
    id = Column(Integer, primary_key=True, autoincrement=True)
    no = Column(String(length=60))
    production_line_no = Column(String(length=60), ForeignKey("production_line.no"))
    name = Column(String(length=60))
    stage = Column(Integer)
    comment = Column(String(length=128))
    creationTime = Column(Integer)
    __table_args__ = (
        UniqueConstraint('no', name='uq_station_composite'),
    )
    # 多 → 1 (Station → ProductLine)
    line_data = relationship("CTableProductLine", back_populates="station_data")

    # 1 → N equipment
    equipment_data = relationship("CTableEquipment", back_populates="station_data")

class CTableEquipment(Base):
    __tablename__ = 'equipment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    no = Column(String(length=60))
    station_no = Column(String(length=60), ForeignKey("station.no"))  # station.no 是 Integer
    name = Column(String(length=60))
    model = Column(String(length=60))
    manufacturer = Column(String(length=60))
    purchaseDate = Column(Integer)
    appearance = Column(String(length=128))
    comment = Column(String(length=128))
    creationTime = Column(Integer)
    __table_args__ = (
        UniqueConstraint('no', name='uq_equipment_composite'),
    )
    # 多 → 1 (Equipment → Station)
    station_data = relationship("CTableStation", back_populates="equipment_data")


class CTableProcessLabor(Base):
    __tablename__ = 'process_labor'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Integer)
    creator_no = Column(String(length=60))
    work_order_no = Column(String(60))
    employee_no = Column(String(60), ForeignKey('employee.no'))
    production_line_no = Column(String(60), ForeignKey('production_line.no'))
    station_no = Column(String(60), ForeignKey('station.no'))

    employee_data = relationship("CTableEmployee")
    production_line_data = relationship("CTableProductLine")
    station_data = relationship("CTableStation")
    __table_args__ = (
        UniqueConstraint('work_order_no', 'employee_no', name='uq_process_labor_composite'),
    )
class CTableDevice(Base):
    __tablename__ = 'device'
    id = Column(Integer, primary_key=True, autoincrement=True)
    no = Column(String(length=60))
    hardwareId = Column(String(length=128))
    name = Column(String(length=60))
    role = Column(Integer)
    comment = Column(String(length=128))
    creationTime = Column(Integer)
    __table_args__ = (
        UniqueConstraint('no', 'hardwareId', name='uq_device_composite'),
    )

class CTableDeviceLog(Base):
    __tablename__ = 'device_log'
    id = Column(Integer, primary_key=True, autoincrement=True)
    hardwareId = Column(String(length=60))
    role = Column(Integer)
    action = Column(Integer)
    data = Column(Text) # 實際儲存 JSON 字串
    creationTime = Column(Integer)


class CTableBatchNoSerialNoGroup(Base):
    __tablename__ = 'batchno_serialno_group'
    id = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(Integer)
    warehouse_no = Column(String(length=60))
    group = Column(String(length=60))
    batch_number = Column(String(length=60))
    serialNo = Column(String(length=60))
    count = Column(Float)
    comment = Column(String(length=128))
    __table_args__ = (
        UniqueConstraint('group', 'batch_number', 'serialNo', name='uq_batchno_serialno_group_composite'),
    )




class CTableInventoryDelta(Base):
    __tablename__ = 'inventory_delta'
    id = Column(Integer, primary_key=True, autoincrement=True)

    warehouse_no = Column(String(length=60))
    warehouse_displayName = Column(String(length=60))
    date = Column(Date)
    timezone = Column(String(length=60))
    kind = Column(Integer)
    category = Column(Integer)
    specified_no = Column(String(length=60))
    specified_name = Column(String(length=60))
    specified_ref_no = Column(String(length=60))
    specified_ref_name = Column(String(length=60))
    in_ref_id = Column(JSON)
    out_ref_id = Column(JSON)
    inPurchaseCount = Column(Float)
    inPurchaseAmount = Column(Float)
    inCount = Column(Float)
    inAmount = Column(Float)
    outCount = Column(Float)
    outAmount = Column(Float)
    creationTime = Column(Integer)
    __table_args__ = (
        UniqueConstraint('warehouse_no', 'date', 'timezone', 'specified_no', name='uq_inventory_delta_composite'),
    )
class CTableInventoryMonthStatistic(Base):
    __tablename__ = 'inventory_month_statistic'
    id = Column(Integer, primary_key=True, autoincrement=True)

    warehouse_no = Column(String(length=60))
    warehouse_displayName = Column(String(length=60))
    date = Column(Date)
    timezone = Column(String(length=60))
    category = Column(Integer)
    startAmount = Column(Float)
    inPurchaseAmount = Column(Float)
    inAmount = Column(Float)
    outAmount = Column(Float)
    endAmount = Column(Float)
    creationTime = Column(Integer)
    __table_args__ = (
        UniqueConstraint('warehouse_no', 'date', 'timezone', 'category', name='uq_Inventory_month_statistic_composite'),
    )
class CTableInventoryItemMonthStatistic(Base):
    __tablename__ = 'inventory_item_month_statistic'
    id = Column(Integer, primary_key=True, autoincrement=True)

    warehouse_no = Column(String(length=60))
    warehouse_displayName = Column(String(length=60))
    date = Column(Date)
    timezone = Column(String(length=60))
    kind = Column(Integer)
    category = Column(Integer)
    specified_no = Column(String(length=60))
    specified_name = Column(String(length=60))
    specified_ref_no = Column(String(length=60))
    specified_ref_name = Column(String(length=60))
    unit = Column(Integer)
    startCount = Column(Float)
    startAmount = Column(Float)
    inCount = Column(Float)
    inAmount = Column(Float)
    endCount = Column(Float)
    endAmount = Column(Float)
    creationTime = Column(Integer)
    __table_args__ = (
        UniqueConstraint('warehouse_no', 'date', 'timezone', 'specified_no', 'specified_ref_no', name='uq_Inventory_item_month_statistic_composite'),
    )

class CTableOrderItemMonthStatistic(Base):
    __tablename__ = 'order_item_month_statistic'
    id = Column(Integer, primary_key=True, autoincrement=True)

    date = Column(Date)
    timezone = Column(String(length=60))
    kind = Column(Integer)
    category = Column(Integer)
    subCategory = Column(Integer)
    type = Column(Integer)
    specified_no = Column(String(length=60))
    specified_name = Column(String(length=60))
    payment = Column(Float)
    amount = Column(Float)
    creationTime = Column(Integer)
    __table_args__ = (
        UniqueConstraint('date', 'kind', 'specified_no', 'category', 'subCategory',
                         name='uq_order_item_month_statistic_composite'),
    )

class CTableOrderPayment(Base):
    __tablename__ = 'order_payment'
    id = Column(Integer, primary_key=True, autoincrement=True)

    no = Column(String(length=60))
    group_no = Column(String(length=60))
    date = Column(Integer)
    arapType = Column(Integer)
    refCategory = Column(Integer)
    ref_no = Column(String(length=60))
    ref_sub_no = Column(String(length=60))
    item_ref_no = Column(String(length=60))
    item_ref_displayName = Column(String(length=60))
    itemCategory = Column(Integer)
    itemSubCategory = Column(Integer)
    paymentType = Column(Integer)
    month = Column(Date)
    price = Column(Float)
    count = Column(Float)
    amount = Column(Integer)
    addDeleteAmount = Column(Integer)
    totalAmount = Column(Integer)
    balance = Column(Integer)
    creationTime = Column(Integer)
    __table_args__ = (
        UniqueConstraint('no', 'date', name='uq_order_payment_composite'),
    )

class CTableShippingPayment(Base):
    __tablename__ = 'shipping_payment'
    id = Column(Integer, primary_key=True, autoincrement=True)

    no = Column(String(length=60))
    group_no = Column(String(length=60))
    date = Column(Integer)
    arapType = Column(Integer)
    record_no = Column(Integer)
    refCategory = Column(Integer)
    ref_no = Column(String(length=60))
    ref_sub_no = Column(String(length=60))
    item_ref_no = Column(String(length=60))
    item_ref_displayName = Column(String(length=60))
    paymentType = Column(Integer)
    month = Column(Date)
    price = Column(Float)
    count = Column(Float)
    amount = Column(Integer)
    addDeleteAmount = Column(Integer)
    totalAmount = Column(Integer)
    balance = Column(Integer)
    creationTime = Column(Integer)
    __table_args__ = (
        UniqueConstraint('no', 'date', name='uq_shipping_payment_composite'),
    )

class CTableWarehousePayment(Base):
    __tablename__ = 'warehouse_payment'
    id = Column(Integer, primary_key=True, autoincrement=True)

    no = Column(String(length=60))
    group_no = Column(String(length=60))
    date = Column(Integer)
    arapType = Column(Integer)
    record_no = Column(Integer)
    batch_no = Column(String(length=60))
    item_ref_no = Column(String(length=60))
    item_ref_displayName = Column(String(length=60))
    paymentType = Column(Integer)
    month = Column(Date)
    price = Column(Float)
    count = Column(Float)
    amount = Column(Float)
    addDeleteAmount = Column(Integer)
    totalAmount = Column(Float)
    balance = Column(Float)
    creationTime = Column(Integer)
    __table_args__ = (
        UniqueConstraint('no', 'date', name='uq_warehouse_payment_composite'),
    )

class CTableQuotation(Base):
    __tablename__ = 'quotation'
    id = Column(Integer, primary_key=True, autoincrement=True)

    no = Column(String(length=60))
    creator_no = Column(String(length=60))
    date = Column(Integer)
    category = Column(Integer)
    type = Column(Integer)
    itemStyle = Column(Integer)
    item_no = Column(String(length=60))
    item_name = Column(String(length=60))
    item_ref_no = Column(String(length=60))
    item_ref_displayName = Column(String(length=60))
    unit = Column(Integer)
    price = Column(Float)
    unitConversion = Column(Float)
    comment = Column(String(length=128))
    creationTime = Column(Integer)
    __table_args__ = (
        UniqueConstraint('no', name='uq_quotation_composite'),
    )


class CTableContract(Base):
    __tablename__ = 'contract'
    id = Column(Integer, primary_key=True, autoincrement=True)

    no = Column(String(length=60))
    ref_no = Column(String(length=60))
    creator_no = Column(String(length=60))
    date = Column(Integer)
    displayName = Column(String(length=60))
    category = Column(Integer)
    type = Column(Integer)
    itemStyle = Column(Integer)
    item_no = Column(String(length=60))
    item_name = Column(String(length=60))
    itemCategory = Column(Integer)
    itemSubCategory = Column(Integer)
    item_ref_no = Column(String(length=60))
    item_ref_displayName = Column(String(length=60))
    payment_id = Column(String(length=60))
    unit = Column(Integer)
    price = Column(Float)
    shippingPrice = Column(Float)
    unitConversion = Column(Float)
    comment = Column(String(length=128))
    creationTime = Column(Integer)
    __table_args__ = (
        UniqueConstraint('no', 'date', name='uq_contract_composite'),
    )

class CTableAPSQuantityItem(Base):
    __tablename__ = 'aps_quantity_item'
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_order_no = Column(String(length=60))
    output_item_no = Column(String(length=60))
    oneProcess = Column(Integer)
    secProcess = Column(Integer)
    #aps_quantity_id = Column(String(length=60), ForeignKey('APS_quantity.id'))
    item_no = Column(String(length=60))
    item_name = Column(String(length=60))
    itemCategory = Column(Integer)
    unit = Column(Integer)
    count = Column(Float)
    creationTime = Column(Integer)
    #quantity_data = relationship("CTableAPSQuantity", back_populates="item_data")
    __table_args__ = (
        UniqueConstraint('product_order_no', 'oneProcess', 'secProcess', 'item_no', name='uq_aps_quantity_item_composite'),
    )
class CTableAPSQuantity(Base):
    __tablename__ = 'aps_quantity'
    id = Column(Integer, primary_key=True, autoincrement=True)
    no = Column(String(length=60))
    product_order_no = Column(String(length=60))
    oneProcess = Column(Integer)
    secProcess = Column(Integer)
    item_no = Column(String(length=60))
    item_name = Column(String(length=60))
    itemCategory = Column(Integer)
    amount = Column(Float)
    unit = Column(Integer)
    minutes = Column(Integer)
    laborCount = Column(Integer)
    creationTime = Column(Integer)
    __table_args__ = (
        UniqueConstraint('product_order_no', 'oneProcess', 'secProcess', 'item_no',
                         name='uq_aps_quantity_composite'),
    )
    item_data = relationship(
        "CTableAPSQuantityItem",
        primaryjoin=and_(
            product_order_no == foreign(CTableAPSQuantityItem.product_order_no),
            oneProcess == foreign(CTableAPSQuantityItem.oneProcess),
            item_no == foreign(CTableAPSQuantityItem.output_item_no),
        ),
        viewonly=True,
        lazy='select'  # 或 selectinload, joined 依需求
    )
    #item_data = relationship("CTableAPSQuantityItem", order_by="CTableAPSQuantityItem.aps_quantity_id", back_populates="quantity_data", lazy='select')

class CTableProductProcess(Base):
    __tablename__ = 'product_process'
    id = Column(Integer, primary_key=True, autoincrement=True)

    no = Column(String(length=60))
    item_no = Column(String(length=60))
    version = Column(Integer)
    date = Column(Integer)
    __table_args__ = (
        UniqueConstraint('no', 'version',  'item_no',
                         name='uq_product_process_composite'),
    )
    # 建立一對多關係
    flows = relationship(
        "CTableProcessFlow",
        back_populates="process",
        order_by="CTableProcessFlow.product_process_no"
    )


class CTableProcessCapacity(Base):
    __tablename__ = 'process_capacity'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Integer)
    oneProcess = Column(Integer)
    secProcess = Column(Integer)
    unit = Column(Integer)
    hourlyOutput = Column(Float)
    laborCount = Column(Integer)
    comment = Column(String(length=128))
    creationTime = Column(Integer)
    __table_args__ = (
        UniqueConstraint('date', 'oneProcess', 'secProcess', name='uq_process_capacity_composite'),
    )

class CTableProcessFlow(Base):
    __tablename__ = 'process_flow'
    id = Column(Integer, primary_key=True, autoincrement=True)

    no = Column(String(length=60))
    product_process_no = Column(String(length=60),
        ForeignKey("product_process.no"))
    order = Column(Integer)
    oneProcess = Column(Integer)
    secProcess = Column(Integer)
    process = relationship("CTableProductProcess", back_populates="flows")
    __table_args__ = (
        UniqueConstraint('no', 'product_process_no', 'order', name='uq_process_flow_composite'),
    )

class CTableProductVer(Base):
    __tablename__ = 'product_ver'
    id = Column(Integer, primary_key=True, autoincrement=True)

    no = Column(String(length=60))
    item_no = Column(String(length=60))
    version = Column(Integer)
    date = Column(Integer)
    __table_args__ = (
        UniqueConstraint('no', 'version',  'item_no', name='uq_product_ver_composite'),
    )

class CTablePLManCapacity(Base):
    __tablename__ = 'pl_man_capacity'
    id = Column(Integer, primary_key=True, autoincrement=True)
    month = Column(Date)
    pl_no = Column(String(length=60))
    pl_name = Column(String(length=60))
    productCount = Column(Integer)
    laborCount = Column(Integer)
    unit = Column(Integer)
    hourlyOutput = Column(Float)
    creationTime = Column(Integer)
    __table_args__ = (
        UniqueConstraint('month', 'pl_no', name='uq_pl_man_capacity_composite'),
    )

class CTablePLItemCapacity(Base):
    __tablename__ = 'pl_item_capacity'
    id = Column(Integer, primary_key=True, autoincrement=True)
    month = Column(Date)
    pl_no = Column(String(length=60))
    pl_name = Column(String(length=60))
    item_no = Column(String(length=60))
    item_name = Column(String(length=60))
    assembly_no = Column(String(length=60))
    assemblyVer = Column(Integer)
    bomWeight = Column(Float)
    bomUnit = Column(Integer)
    productCount = Column(Integer)
    hours = Column(Integer)
    count = Column(Float)
    unit = Column(Integer)
    hourlyOutput = Column(Float)
    price = Column(Float)
    rawMaterialCost = Column(Float)
    materialCost = Column(Float)
    laborCost = Column(Float)
    creationTime = Column(Integer)
    __table_args__ = (
        UniqueConstraint('month', 'item_no', 'pl_no', name='uq_pl_item_capacity_composite'),
    )

class CTablePLItemLoss(Base):
    __tablename__ = 'pl_item_loss'
    id = Column(Integer, primary_key=True, autoincrement=True)
    month = Column(Date)
    pl_item_capacity_no = Column(String(length=60))
    item_no = Column(String(length=60))
    item_name = Column(String(length=60))
    itemCategory = Column(Integer)
    itemSubCategory = Column(Integer)
    weightRatio = Column(Float)
    lossRate = Column(Float)
    creationTime = Column(Integer)
    __table_args__ = (
        UniqueConstraint('month', 'item_no', name='uq_pl_item_loss_composite'),
    )

class CTableLaborWage(Base):
    __tablename__ = 'labor_wage'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Integer)
    type = Column(Integer)
    level = Column(Integer)
    hourly = Column(Integer)
    creationTime = Column(Integer)
    __table_args__ = (
        UniqueConstraint('date', 'type', 'level', name='uq_labor_wage_composite'),
    )

class CTableRWItems (Base):
    __tablename__ = 'rw_items'
    id = Column(Integer, primary_key=True, autoincrement=True)
    item_no = Column(String(length=60))
