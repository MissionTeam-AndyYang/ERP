from sqlalchemy import Column, Integer, String, Float, Time, JSON, orm, ForeignKey, Text, Date, DateTime, func, Index,and_
Base = orm.declarative_base()
from sqlalchemy.orm import relationship, foreign, remote

class CTableServer(Base):
    __tablename__ = 'server_info'
    id =Column(String(length=60), primary_key=True)
    timezone = Column(String(length=60))




class CTablePayment(Base):
    __tablename__ = 'payment'
    id =Column(String(length=60), primary_key=True)
    type = Column(Integer)
    source = Column(Integer)
    date = Column(Integer)
    period = Column(Integer)
    creationTime = Column(Integer)


class CTableBankAccount(Base):
    __tablename__ = 'bank_account'
    id =Column(String(length=60))
    displayName = Column(String(length=60))
    name = Column(String(length=60))
    branch = Column(String(length=60))
    account = Column(String(length=60))
    number = Column(String(length=60), primary_key=True)
    creationTime = Column(Integer)

class CTableEnterprise(Base):
    __tablename__ = 'enterprise'
    no = Column(String(length=20),primary_key=True)
    businessNo = Column(String(length=20))
    displayName = Column(String(length=60))
    name = Column(String(length=60))
    address = Column(String(length=100))
    phone = Column(String(length=100))
    fax = Column(String(length=20))
    lar = Column(String(length=60))
    department = Column(Integer)
    comment = Column(String(length=128))
    creationTime = Column(Integer)

class CTableCompany(Base):
    __tablename__ = 'company'

    no = Column(String(length=20),primary_key=True)
    businessNo = Column(String(length=20))
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
'''
class CTableCustomer(Base):
    __tablename__ = 'customer'
    id = Column(String(length=60))
    no = Column(String(length=20), unique=True, primary_key=True)
    category = Column(Integer)
    businessNo = Column(String(length=20))
    displayName = Column(String(length=60))
    name = Column(String(length=60))
    address = Column(String(length=100))
    phone = Column(String(length=100))
    fax = Column(String(length=20))
    contactName = Column(String(length=60))
    contactPhone = Column(JSON)
    contactTitle = Column(String(length=60))
    contactEmail = Column(String(length=60))
    payment_id = Column(String(length=60))
    bank_account_id = Column(String(length=60))
    comment = Column(String(length=128))
    creationTime = Column(Integer)


class CTableSupplier(Base):
    __tablename__ = 'supplier'
    id = Column(String(length=60))
    no = Column(String(length=20), unique=True,primary_key=True)
    category = Column(Integer)
    businessNo = Column(String(length=20))
    displayName = Column(String(length=60))
    name = Column(String(length=60))
    address = Column(String(length=100))
    phone = Column(String(length=100))
    fax = Column(String(length=20))
    contactName = Column(String(length=60))
    contactPhone = Column(JSON)
    contactTitle = Column(String(length=60))
    contactEmail = Column(String(length=60))
    payment_id = Column(String(length=60))
    bankDisplayName = Column(String(length=60))
    bankName = Column(String(length=60))
    bankBranch = Column(String(length=60))
    bankAccount = Column(String(length=60))
    bankNo = Column(String(length=60))
    comment = Column(String(length=128))
    creationTime = Column(Integer)


class CTableVendor(Base):
    __tablename__ = 'vendor'
    id = Column(String(length=60))
    no = Column(String(length=20), unique=True,primary_key=True)
    category = Column(Integer)
    businessNo = Column(String(length=20))
    displayName = Column(String(length=60))
    name = Column(String(length=60))
    address = Column(String(length=100))
    phone = Column(String(length=100))
    fax = Column(String(length=20))
    contactName = Column(String(length=60))
    contactPhone = Column(JSON)
    contactTitle = Column(String(length=60))
    contactEmail = Column(String(length=60))
    payment_id = Column(String(length=60))
    bankDisplayName = Column(String(length=60))
    bankName = Column(String(length=60))
    bankBranch = Column(String(length=60))
    bankAccount = Column(String(length=60))
    bankNo = Column(String(length=60))
    comment = Column(String(length=128))
    creationTime = Column(Integer)
'''
class CTableTransItems(Base):
    __tablename__ = 'trans_items'
    no = Column(String(length=20), primary_key=True)
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

class CTableTransItems2(Base):
    __tablename__ = 'trans_items2'
    no = Column(String(length=20), primary_key=True)
    name = Column(String(length=100))
    category = Column(Integer)
    attribute = Column(Integer)
    company_no = Column(String(length=60))
    company_displayName = Column(String(length=60))
    comment = Column(String(length=128))
    creationTime = Column(Integer)

class CTableMaterial(Base):
    __tablename__ = 'material'
    id = Column(String(length=60))
    no = Column(String(length=20), primary_key=True)
    category = Column(Integer)
    subCategory = Column(Integer)
    type = Column(Integer)
    name = Column(String(length=100))
    supplier_no = Column(String(length=60))
    supplier_displayName = Column(String(length=60))
    unitShipping = Column(Integer)
    unitWarehouse = Column(Integer)
    unitProduct = Column(Integer)
    package1Unit = Column(Integer)
    package12Count = Column(Float)
    package2Unit = Column(Integer)
    package23Count = Column(Float)
    package3Unit = Column(Integer)
    package34Count = Column(Float)
    package4Unit = Column(Integer)
    specUnitType = Column(Integer)
    specUnit = Column(Integer)
    specValue = Column(Float)
    comment = Column(String(length=128))
    creationTime = Column(Integer)

class CTableMaterialPrice(Base):
    __tablename__ = 'material_price'
    id = Column(String(length=60))
    item_no = Column(String(length=20), primary_key=True)
    date = Column(Integer)
    purchaseCount = Column(Float)
    purchaseUnit = Column(Integer)
    purchasePrice = Column(Float)
    purchaseWeightUnit = Column(Float)
    purchaseLengthUnit = Column(Float)
    purchaseCountUnit = Column(Float)
    warehouseUnitWeight = Column(Integer)
    warehousePriceWeight = Column(Float)
    warehouseUnitLength = Column(Integer)
    warehousePriceLength = Column(Float)
    warehouseUnitCount = Column(Integer)
    warehousePriceCount = Column(Float)
    costUnitWeight = Column(Integer)
    costPriceWeight = Column(Float)
    costUnitLength = Column(Integer)
    costPriceLength = Column(Float)
    costUnitCount = Column(Integer)
    costPriceCount = Column(Float)
    creationTime = Column(Float)


class CTableItemPrice(Base):
    __tablename__ = 'item_price'
    no = Column(String(length=60))
    item_no = Column(String(length=20), primary_key=True)
    item_name = Column(String(length=100))
    itemCategory = Column(Integer)
    date = Column(Integer, primary_key=True)
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
    item_no = Column(String(length=20), primary_key=True)
    itemCategory = Column(Integer)
    date = Column(Integer, primary_key=True)
    unit = Column(Integer)
    value = Column(Float)
    estValue = Column(Float)
    creationTime = Column(Float)

class CTableItemHours(Base):
    __tablename__ = 'item_hours'
    id = Column(Integer, primary_key=True, autoincrement=True)
    item_no = Column(String(length=20), unique=True)
    itemCategory = Column(Integer)
    date = Column(Integer, unique=True)
    unit = Column(Integer)
    value = Column(Float)
    estValue = Column(Float)
    creationTime = Column(Float)

class CTableSamplePrice(Base):
    __tablename__ = 'sample_price'
    item_no = Column(String(length=20), primary_key=True)
    itemVer = Column(Integer)
    date = Column(Integer, primary_key=True)
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
class CTableInproductPrice(Base):
    __tablename__ = 'inproduct_price'
    id = Column(String(length=60))
    item_no = Column(String(length=20), primary_key=True)
    date = Column(Integer, primary_key=True)
    warehouseUnit  = Column(Integer)
    warehousePrice  = Column(Float)
    costUnit = Column(Integer)
    costPrice = Column(Float)
    comment = Column(String(length=128))
    creationTime  = Column(Integer)


class CTableProductPrice(Base):
    __tablename__ = 'product_price'
    id = Column(String(length=60))
    item_no = Column(String(length=20), primary_key=True)
    date = Column(Integer, primary_key=True)
    warehouseUnit = Column(Integer)
    warehousePrice = Column(Float)
    costUnit = Column(Integer)
    costPrice = Column(Float)
    comment = Column(String(length=128))
    creationTime = Column(Integer)


class CTableProductSellPrice(Base):
    __tablename__ = 'product_sellprice'
    id = Column(String(length=60))
    item_no = Column(String(length=20), primary_key=True)
    quotation_no = Column(String(length=20), primary_key=True)
    date = Column(Integer)
    quantity  = Column(Integer)
    unit  = Column(Integer)
    price = Column(Float)
    comment = Column(String(length=128))
    creationTime = Column(Integer)

class CTableBatchNumber(Base):
    __tablename__ = 'batch_number'

    id = Column(String(length=60))
    date = Column(Integer)
    no = Column(String(length=20),  unique=True, primary_key=True, index=True)
    creator_id = Column(String(length=60))

    ref_no = Column(String(length=60), primary_key=True, index=True)
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
    batch_number = Column(String(length=60),ForeignKey('batch_number.no'), primary_key=True)
    serialNo = Column(String(length=60), primary_key=True)
    #batchno_data = relationship("CTableBatchNumber", back_populates="serialNo_data")
    ref_order_no = Column(String(length=60), primary_key=True)
    ref_order_no_category = Column(Integer)
    time = Column(Integer)
    unit = Column(Integer)
    expectedCount = Column(Float)
    count = Column(Float)
    validDate = Column(Integer)
    warehouse_no = Column(String(length=60))
    updatedTime = Column(Integer)

#CTableBatchNumber.serialNo_data = relationship("CTableBatchNoSerialNo", order_by=CTableBatchNoSerialNo.batch_number, back_populates="batchno_data")

class CTableInventoryOrder(Base):
    __tablename__ = 'inventory_order'
    no = Column(String(length=60),primary_key=True)
    creator_id = Column(String(length=60))
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
    result = Column(Integer)
    resultTime = Column(Integer)
    comment = Column(String(length=128))
    creationTime = Column(Integer)

class CTableInventoryRec(Base):
    __tablename__ = 'inventory_record'
    id = Column(String(length=60),primary_key=True)
    creator_id = Column(String(length=60))
    group = Column(String(length=60))
    refCategory = Column(Integer)
    ref_no = Column(String(length=60))
    warehouse_no = Column(String(length=60))
    warehouse_displayName = Column(String(length=60))
    date = Column(Integer)
    source = Column(Integer)
    category = Column(Integer)
    batchNumber = Column(String(length=60))
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
    no = Column(String(length=20), unique=True,primary_key=True)
    name = Column(String(length=60))
    category = Column(Integer)
    type = Column(Integer)
    creationTime = Column(Integer)

class CTableShipWarehouse(Base):
    __tablename__ = 'ship_wh'
    no = Column(String(length=20), unique=True,primary_key=True)
    company_no = Column(String(length=60))
    company_displayName = Column(String(length=60))
    name = Column(String(length=60))
    category = Column(Integer)
    attribute = Column(Integer)
    maxCapacity = Column(Integer)
    unit = Column(Integer)
    comment = Column(String(length=128))
    creationTime = Column(Integer)


class CTableShipWarehouseContract(Base):
    __tablename__ = 'ship_wh_contract'
    no = Column(String(length=20), unique=True,primary_key=True)
    date = Column(Integer,primary_key=True)
    displayName = Column(String(length=60))
    ref_no = Column(String(length=60))
    item_no = Column(String(length=60))
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

class CTableShipWarehouseQuotation(Base):
    __tablename__ = 'ship_wh_quotation'
    no = Column(String(length=20), unique=True,primary_key=True)
    date = Column(Integer,primary_key=True)
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

class CTableShippingRec(Base):
    __tablename__ = 'shipping_record'
    no = Column(String(length=20), unique=True,primary_key=True)
    date = Column(Integer,primary_key=True)
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
    expectedCount = Column(Float)
    checkedCount = Column(Float)
    comment = Column(String(length=128))
    creationTime = Column(Integer)


class CTableWarehouseRec(Base):
    __tablename__ = 'warehouse_record'
    no = Column(String(length=20), unique=True,primary_key=True)
    date = Column(Integer,primary_key=True)
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
'''
class CTableWarehousePrice(Base):
    __tablename__ = 'warehouse_price'
    no = Column(String(length=20), unique=True,primary_key=True)
    version = Column(Integer)
    date = Column(Integer)
    displayName = Column(String(length=60))
    warehouse_no = Column(String(length=60))
    category = Column(Integer)
    region = Column(Integer)
    type = Column(Integer)
    unit = Column(Integer)
    price = Column(Float)
    fee = Column(Float)
    comment = Column(String(length=128))
    creationTime = Column(Integer)
'''

class CTableProductOrder(Base):
    __tablename__ = 'product_order'
    id = Column(String(length=60))
    no = Column(String(length=20), primary_key=True)
    creator_id = Column(String(length=60))
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
    result = Column(Integer)
    resultTime = Column(Integer)
    comment = Column(String(length=128))
    creationTime = Column(Integer)

class CTableShippingOrder(Base):
    __tablename__ = 'shipping_order'
    id = Column(String(length=60))
    no = Column(String(length=20), primary_key=True)
    creator_id = Column(String(length=60))
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
    result = Column(Integer)
    resultTime = Column(Integer)
    comment = Column(String(length=128))
    creationTime = Column(Integer)


class CTablePurchaseOrder(Base):
    __tablename__ = 'purchase_order'
    id = Column(String(length=60))
    no = Column(String(length=20), primary_key=True)
    creator_id = Column(String(length=60))
    purchase_request_id = Column(String(length=60))
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
    result = Column(Integer)
    resultTime = Column(Integer)
    comment = Column(String(length=128))
    creationTime = Column(Integer)


class CTableGoodsReceiptNote (Base):
    __tablename__ = 'goods_receipt_note'
    id = Column(String(length=60))
    no = Column(String(length=20), primary_key=True, index=True)  # 建立索引

    creator_id = Column(String(length=60))
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
    result                = Column(Integer)
    resultTime            = Column(Integer)
    comment               = Column(String(length=128))
    creationTime          = Column(Integer)



class CTableWorkOrder(Base):
    __tablename__ = 'work_order'
    id = Column(String(length=60))
    date = Column(Integer)
    no = Column(String(length=20), primary_key=True)
    creator_id = Column(String(length=60))
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
    result = Column(Integer)
    resultTime = Column(Integer)
    comment = Column(String(length=128))
    creationTime = Column(Integer)

CTableProductOrder.work_order = relationship("CTableWorkOrder", order_by=CTableProductOrder.no, back_populates="product_order")



class CTableProductionData(Base):
    __tablename__ = 'production_data'

    id = Column(String(length=60))
    creator_id = Column(String(length=60))

    work_order_no = Column(String(length=60), ForeignKey('work_order.no'), primary_key=True)
    work_order = relationship("CTableWorkOrder", back_populates="production_data")

    product_order_no = Column(String(length=60))
    customer_no = Column(String(length=60))
    customer_displayName = Column(String(length=60))
    product_no = Column(String(length=60))
    product_name = Column(String(length=100))
    date = Column(Integer)
    product_line_no = Column(String(length=60))
    oneProcess = Column(Integer)
    secProcess = Column(Integer)
    preStartTime = Column(Integer, primary_key=True)
    preEndTime = Column(Integer, primary_key=True)
    postStartTime = Column(Integer, primary_key=True)
    postEndTime = Column(Integer, primary_key=True)
    item_no = Column(String(length=60))
    item_name = Column(String(length=100))
    unit = Column(Integer)
    count = Column(Float)
    materialLoss = Column(Float)
    grossWeight = Column(Float)
    comment = Column(String(length=128))
    creationTime = Column(Integer)

CTableWorkOrder.production_data = relationship("CTableProductionData", order_by=CTableProductionData.work_order_no, back_populates="work_order")


class CTableProductionDataInput(Base):
    __tablename__ = 'production_data_input'
    id                = Column(String(length=60), primary_key=True)
    production_data_id = Column(String(length=60), ForeignKey('production_data.id'))
    production_data = relationship("CTableProductionData", back_populates="input_data")
    work_order_no = Column(String(length=60))
    process_order_no = Column(String(length=60))
    group = Column(String(length=60))
    time            = Column(Integer)
    action            = Column(Integer, primary_key=True)
    item_no            = Column(String(length=60))
    item_name          = Column(String(length=100))
    category = Column(Integer) #itemCategory
    itemSubCategory    = Column(Integer)
    batch_number       = Column(String(length=60))
    serial_no          = Column(String(length=60))
    unit               = Column(Integer)
    count              = Column(Float)
    #receiveCount              = Column(Float)
    #returnCount              = Column(Float)
    #wasteCount              = Column(Float)
    avgLoss = Column(Float)
    comment = Column(String(length=128))

CTableProductionData.input_data = relationship("CTableProductionDataInput", order_by=CTableProductionDataInput.work_order_no, back_populates="production_data")


class CTableProductionDataOutput(Base):
    __tablename__ = 'production_data_output'
    id                = Column(String(length=60), primary_key=True)

    production_data_id = Column(String(length=60), ForeignKey('production_data.id'))
    production_data = relationship("CTableProductionData", back_populates="output_data")

    work_order_no = Column(String(length=60))
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

CTableProductionData.output_data = relationship("CTableProductionDataOutput", order_by=CTableProductionDataOutput.work_order_no, back_populates="production_data")

class CTableProductionDataReuse(Base):
    __tablename__ = 'production_data_reuse'
    id                = Column(String(length=60))
    production_data_id = Column(String(length=60), ForeignKey('production_data.id'), primary_key=True)
    work_order_no = Column(String(length=60))
    process_order_no = Column(String(length=60))
    production_data = relationship("CTableProductionData", back_populates="reuse_data")
    time            = Column(Integer)
    action            = Column(Integer, primary_key=True)
    item_no            = Column(String(length=60))
    item_name          = Column(String(length=100))
    itemSubCategory    = Column(Integer)
    category           = Column(Integer)
    batch_number       = Column(String(length=60), primary_key=True)
    serial_no          = Column(String(length=60), primary_key=True)
    unit               = Column(Integer)
    count              = Column(Float)
    comment = Column(String(length=128))

CTableProductionData.reuse_data = relationship("CTableProductionDataReuse", order_by=CTableProductionDataReuse.work_order_no, back_populates="production_data")

class CTableProductionDataLabor(Base):
    __tablename__ = 'production_data_labor'
    id                = Column(String(length=60))
    production_data_id = Column(String(length=60), ForeignKey('production_data.id'))
    work_order_no     = Column(String(length=60), primary_key=True)
    production_data = relationship("CTableProductionData", back_populates="labor_data")
    employee_no       = Column(String(length=60), primary_key=True)
    employee_name     = Column(String(length=100))
    employee_type     = Column(Integer)
    employee_jobTitle = Column(Integer)
    employee_level    = Column(Integer)
    station_no        = Column(String(length=60))
    action            = Column(Integer, primary_key=True)
    stationStage       = Column(Integer, primary_key=True)
    startTime     = Column(Integer, primary_key=True)
    endTime       = Column(Integer, primary_key=True)
    hours = Column(Integer)
CTableProductionData.labor_data = relationship("CTableProductionDataLabor", order_by=CTableProductionDataLabor.work_order_no, back_populates="production_data")


class CTableProductionDataMachine(Base):
    __tablename__ = 'production_data_machine'
    id                = Column(String(length=60), primary_key=True)
    production_data_id = Column(String(length=60), ForeignKey('production_data.id'))
    work_order_no     = Column(String(length=60))
    production_data = relationship("CTableProductionData", back_populates="machine_data")
    time             = Column(Integer)
    equipment_no       = Column(String(length=60))
    equipment_name     = Column(String(length=100))
    action             = Column(Integer, primary_key=True)
    temperature        = Column(Float)
    speed             = Column(Float)
    creationTime       = Column(Integer)
CTableProductionData.machine_data = relationship("CTableProductionDataMachine", order_by=CTableProductionDataMachine.work_order_no, back_populates="production_data")


class CTableLaborWage(Base):
    __tablename__ = 'labor_wage'
    id                = Column(Integer)
    date = Column(Integer, primary_key=True)
    type = Column(Integer, primary_key=True)
    level = Column(Integer, primary_key=True)
    hourly = Column(Integer)
    creationTime = Column(Integer)



class CTable2023ProductionData(Base):
    __tablename__ = '2023_production_data'

    #input_data = relationship("CTable2023ProductionDataInput", backref="2023_production_data")

    id = Column(String(length=60))
    creator_id = Column(String(length=60))
    work_order_no = Column(String(length=60), primary_key=True)
    product_order_no = Column(String(length=60))
    customer_no = Column(String(length=60))
    customer_displayName = Column(String(length=60))
    product_no = Column(String(length=60))
    product_name = Column(String(length=100))
    date = Column(Integer)
    product_line_id = Column(String(length=60))
    oneProcess = Column(Integer)
    secProcess = Column(Integer)
    startTime = Column(Integer, primary_key=True)
    endTime = Column(Integer, primary_key=True)
    preTotalTime = Column(Integer)
    postTotalTime = Column(Integer)
    laborCount = Column(Integer)
    laborList = Column(JSON)
    item_no = Column(String(length=60))
    item_name = Column(String(length=100))
    valid_date         = Column(String(length=60))
    valid_date_no      = Column(String(length=60))
    unit = Column(Integer)
    count = Column(Float)
    materialLoss = Column(Float)
    grossWeight = Column(Float)
    comment = Column(String(length=128))
    creationTime = Column(Integer)

class CTable2023ProductionDataInput(Base):
    __tablename__ = '2023_production_data_input'
    id                = Column(String(length=60), primary_key=True)
    production_data_id = Column(String(length=60), ForeignKey('2023_production_data.id'))
    production_data_2023 = relationship("CTable2023ProductionData", back_populates="input_data")

    work_order_no = Column(String(length=60))
    group = Column(String(length=60))
    item_id            = Column(String(length=60))
    item_name          = Column(String(length=100))
    category           = Column(Integer)
    batch_number       = Column(String(length=60))
    unit               = Column(Integer)
    count              = Column(Float)
    remainingCount     = Column(Float)
    wasteCount         = Column(Float)
    avgLoss            = Column(Float)


CTable2023ProductionData.input_data = relationship("CTable2023ProductionDataInput", order_by=CTable2023ProductionDataInput.id, back_populates="production_data_2023")


class CTable2023ProductionDataOutput(Base):
    __tablename__ = '2023_production_data_output'
    id                = Column(String(length=60), primary_key=True)
    production_data_id = Column(String(length=60))

    work_order_no = Column(String(length=60))
    group = Column(String(length=60))
    item_id            = Column(String(length=60))
    item_name          = Column(String(length=100))
    category           = Column(Integer)
    batch_number       = Column(String(length=60))
    valid_date         = Column(Integer)
    valid_date_no      = Column(String(length=60))
    unit               = Column(Integer)
    count              = Column(Float)


class CTableHourlyWage(Base):
    __tablename__ = 'hourly_wage'
    id = Column(String(length=60))
    date = Column(Integer, primary_key=True)
    monthly = Column(Integer)
    hourly = Column(Integer)
    creationTime = Column(Integer)

class CTableSession(Base):
    __tablename__ = 'session'
    id = Column(String(length=60), primary_key=True)
    token = Column(String(length=60))
    user_no = Column(String(length=60))
    expiredTime = Column(Integer)


class CTableMember(Base):
    __tablename__ = 'member'
    user_no = Column(String(length=60), primary_key=True)
    account = Column(String(length=60))
    password = Column(String(length=60))

class CTableUserGroup(Base):
    __tablename__ = 'user_group'
    id = Column(String(length=60), primary_key=True)
    name = Column(String(length=60))
    role = Column(Integer)
    users = Column(JSON)
    privileges = Column(JSON)


class CTableInproduct(Base):
    __tablename__ = 'inproduct'
    id = Column(String(length=60))
    no = Column(String(length=60), primary_key=True)

    category = Column(Integer)
    name = Column(String(length=100))
    customer_no = Column(String(length=60))
    customer_displayName = Column(String(length=60))
    unitShipping = Column(Integer)
    unitWarehouse = Column(Integer)
    unitProduct = Column(Integer)
    package3Unit = Column(Integer)
    package34Count = Column(Float)
    package4Unit = Column(Integer)
    version = Column(String(length=60))
    version_history = Column(JSON)
    comment = Column(String(length=128))
    creationTime = Column(Integer)

    bom_specs = relationship("CTableInproductBOMSpec", back_populates="inproduct_data", lazy='select')


class CTableProduct(Base):
    __tablename__ = 'product'
    id = Column(String(length=60))
    no = Column(String(length=20), primary_key=True)
    category = Column(Integer)
    name = Column(String(length=100))
    customer_no = Column(String(length=60))
    customer_displayName = Column(String(length=60))
    unitShipping = Column(Integer)
    unitWarehouse = Column(Integer)
    unitProduct = Column(Integer)
    package1Unit = Column(Integer)
    package12Count = Column(Float)
    package2Unit = Column(Integer)
    package23Count = Column(Float)
    version = Column(Integer)
    comment = Column(String(length=128))
    creationTime = Column(Integer)

class CTableGoods(Base):
    __tablename__ = 'goods'

    no = Column(String(length=20), primary_key=True)
    category = Column(Integer)
    subCategory = Column(Integer)
    name = Column(String(length=100))
    unitShipping = Column(Integer)
    unitWarehouse = Column(Integer)
    unitProduct = Column(Integer)
    comment = Column(String(length=128))
    creationTime = Column(Integer)

class CTableBOM(Base):
    __tablename__ = 'bom'
    id = Column(String(length=60))
    no = Column(String(length=20), primary_key=True)
    displayName = Column(String(length=60))
    date = Column(Integer)
    unit = Column(Integer)
    weight = Column(Float)
    version = Column(Float, primary_key=True)
    comment = Column(String(length=128))
    creationTime = Column(Integer)
    item_data = relationship("CTableBOMItem", order_by="CTableBOMItem.item_no", back_populates="bom_data", lazy='select')


class CTableBOMItem(Base):
    __tablename__ = 'bom_item'
    bom_id = Column(String(length=60), ForeignKey('bom.id'), primary_key=True)
    item_no = Column(String(length=60), primary_key=True)
    item_name = Column(String(length=60))
    unit = Column(Integer)
    weight = Column(Float)
    creationTime = Column(Integer)

    bom_data = relationship("CTableBOM", back_populates="item_data")


class CTableBOM1Number(Base):
    __tablename__ = 'bom1_number'
    id = Column(String(length=60))
    no = Column(String(length=20), primary_key=True)
    category = Column(Integer)
    displayName = Column(String(length=60))
    unit = Column(Integer)
    weight = Column(Float)
    bom_id = Column(String(length=60))
    bom_version = Column(Integer)
    comment = Column(String(length=128))
    creationTime = Column(Integer)


class CTableBOM1(Base):
    __tablename__ = 'bom1'
    id = Column(String(length=60), primary_key=True)
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


class CTableBOM2Number(Base):
    __tablename__ = 'bom2_number'

    #bom2_data = relationship("CTableInproductBOMSpec", backref="CTableBOM2Number")

    id = Column(String(length=60))
    no = Column(String(length=20), primary_key=True)
    category = Column(Integer)
    displayName = Column(String(length=60))
    unit = Column(Integer)
    weight = Column(Float)
    bom_id = Column(String(length=60))
    bom_version = Column(Integer)
    comment = Column(String(length=128))
    creationTime = Column(Integer)

class CTableBOM2(Base):
    __tablename__ = 'bom2'
    id = Column(String(length=60), primary_key=True)
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
    id = Column(String(length=60))
    inproduct_id = Column(String(length=60))
    inproduct_no = Column(String(length=60), ForeignKey('inproduct.no'), primary_key=True)
    category = Column(Integer)
    item_no = Column(String(length=60), primary_key=True)
    item_version = Column(Integer)
    bom12_no = Column(String(length=60))
    count = Column(Integer)
    unit = Column(Integer)
    weight = Column(Float)

    inproduct_data = relationship("CTableInproduct", back_populates="bom_specs", lazy='select')


class CTableProductSpec(Base):
    __tablename__ = 'product_spec'
    id = Column(String(length=60), primary_key=True)
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

class CTableProductBOMSpec(Base):
    __tablename__ = 'product_bom_spec'
    id = Column(String(length=60), primary_key=True)
    product_id = Column(String(length=60))
    product_no = Column(String(length=60))
    product_version = Column(Integer)
    level = Column(Integer)
    bom2_no = Column(String(length=60))
    count = Column(Integer)
    unit = Column(Integer)
    weight = Column(Float)

class CTableProcessOrder (Base):
    __tablename__ = 'process_order'

    no = Column(String(length=20), primary_key=True, index=True)  # 建立索引
    creator_id = Column(String(length=60))
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



class CTableBasicHistory(Base):
    __tablename__ = 'basic_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ref_no = Column(String(length=20))
    fieldName = Column(String(length=60), nullable=False)
    oldValue = Column(Text)
    newValue = Column(Text)
    modifiedBy = Column(String(length=60))
    modifiedAt = Column(Integer)


class CTableItemHistory(Base):
    __tablename__ = 'item_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ref_no = Column(String(length=20))
    fieldName = Column(String(length=60), nullable=False)
    oldValue = Column(Text)
    newValue = Column(Text)
    modifiedBy = Column(String(length=60))
    modifiedAt = Column(Integer)


class CTableItemPriceHistory(Base):
    __tablename__ = 'item_price_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ref_no = Column(String(length=20))
    fieldName = Column(String(length=60), nullable=False)
    oldValue = Column(Text)
    newValue = Column(Text)
    modifiedBy = Column(String(length=60))
    modifiedAt = Column(Integer)

class CTableBatchNoHistory(Base):
    __tablename__ = 'batchno_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ref_no = Column(String(length=20))
    fieldName = Column(String(length=60), nullable=False)
    oldValue = Column(Text)
    newValue = Column(Text)
    modifiedBy = Column(String(length=60))
    modifiedAt = Column(Integer)

class CTableWarehouseHistory(Base):
    __tablename__ = 'warehouse_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ref_no = Column(String(length=20))
    fieldName = Column(String(length=60), nullable=False)
    oldValue = Column(Text)
    newValue = Column(Text)
    modifiedBy = Column(String(length=60))
    modifiedAt = Column(Integer)

class CTableEmployee(Base):
    __tablename__ = 'employee'
    no = Column(String(length=20), primary_key=True)
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

class CTableProcess(Base):
    __tablename__ = 'process'
    no = Column(Integer, primary_key=True)
    oneProcess = Column(Integer)
    secProcess = Column(Integer)
    comment = Column(String(length=128))
    creationTime = Column(Integer)

class CTableFactory(Base):
    __tablename__ = 'factory'
    no = Column(String(length=60), primary_key=True)
    region = Column(String(length=60))
    location = Column(String(length=60))
    comment = Column(String(length=60))
    creationTime = Column(Integer)
    # 1(Factory) → 多(ProductLine)
    line_data = relationship("CTableProductLine", back_populates="factory_data")
class CTableProductLine(Base):
    __tablename__ = 'production_line'

    no = Column(String(length=60), primary_key=True)   # 改成 PK（正確）
    name = Column(String(length=60))
    process_no = Column(String(length=60))
    oneProcess = Column(Integer)
    secProcess = Column(Integer)
    factory_no = Column(String(60), ForeignKey("factory.no"))
    location = Column(String(60))
    equipment_id = Column(JSON)
    capacityUnit = Column(Integer)
    capacity = Column(Float)
    laborCount = Column(Integer)
    laborEfficiency = Column(Float)
    comment = Column(String(128))
    creationTime = Column(Integer)

    # 多(ProductLine) → 1(Factory)
    factory_data = relationship("CTableFactory", back_populates="line_data")

    # 1 → N station
    station_data = relationship("CTableStation", back_populates="line_data")

class CTableStation(Base):
    __tablename__ = 'station'

    no = Column(Integer, primary_key=True)
    production_line_no = Column(String(length=60), ForeignKey("production_line.no"))
    name = Column(String(length=60))
    stage = Column(Integer)
    comment = Column(String(length=128))
    creationTime = Column(Integer)

    # 多 → 1 (Station → ProductLine)
    line_data = relationship("CTableProductLine", back_populates="station_data")

    # 1 → N equipment
    equipment_data = relationship("CTableEquipment", back_populates="station_data")

class CTableEquipment(Base):
    __tablename__ = 'equipment'

    no = Column(Integer, primary_key=True)
    station_no = Column(Integer, ForeignKey("station.no"))  # station.no 是 Integer
    name = Column(String(length=60))
    model = Column(String(length=60))
    manufacturer = Column(String(length=60))
    purchaseDate = Column(Integer)
    appearance = Column(String(length=128))
    comment = Column(String(length=128))
    creationTime = Column(Integer)

    # 多 → 1 (Equipment → Station)
    station_data = relationship("CTableStation", back_populates="equipment_data")


class CTableProcessLabor(Base):
    __tablename__ = 'process_labor'
    date = Column(Integer)
    creator_id = Column(String(length=60))
    work_order_no = Column(String(60), primary_key=True)
    employee_no = Column(String(60), ForeignKey('employee.no'), primary_key=True)
    production_line_no = Column(String(60), ForeignKey('production_line.no'))
    station_no = Column(String(60), ForeignKey('station.no'))

    employee_data = relationship("CTableEmployee")
    production_line_data = relationship("CTableProductLine")
    station_data = relationship("CTableStation")

class CTableDevice(Base):
    __tablename__ = 'device'
    no = Column(String(length=60), primary_key=True)
    hardwareId = Column(String(length=128), primary_key=True)
    name = Column(String(length=60))
    role = Column(Integer)
    comment = Column(String(length=128))
    creationTime = Column(Integer)





class CTableBatchNoSerialNoGroup(Base):
    __tablename__ = 'batchno_serialno_group'

    time = Column(Integer)
    warehouse_no = Column(String(length=60))
    group = Column(String(length=60), primary_key=True)
    batch_number = Column(String(length=60), primary_key=True)
    serialNo = Column(String(length=60), primary_key=True)
    count = Column(Float)
    comment = Column(String(length=128))


class CTableDeviceLog(Base):
    __tablename__ = 'device_log'
    id = Column(Integer, primary_key=True, autoincrement=True)
    hardwareId = Column(String(length=60))
    role = Column(Integer)
    action = Column(Integer)
    data = Column(Text) # 實際儲存 JSON 字串

    creationTime = Column(Integer)

class CTableRWItems (Base):
    __tablename__ = 'rw_items'
    id = Column(Integer, primary_key=True)
    item_no = Column(String(length=60))


class CTablePSMonthStatistic (Base):
    __tablename__ = 'ps_month_statistic'
    id = Column(Integer, primary_key=True)
    year = Column(Integer)
    month = Column(Integer)
    kind = Column(Integer)
    category = Column(Integer)
    specified_no =  Column(String(length=60))
    specified_name = Column(String(length=60))
    amount = Column(Float)
    creationTime = Column(Integer)


class CTableInventoryDelta(Base):
    __tablename__ = 'inventory_delta'
    id = Column(String(length=60))
    warehouse_no = Column(String(length=60), primary_key=True)
    warehouse_displayName = Column(String(length=60))
    date = Column(Date, primary_key=True)
    timezone = Column(String(length=60), primary_key=True)
    kind = Column(Integer)
    category = Column(Integer)
    specified_no = Column(String(length=60), primary_key=True)
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

class CTableInventoryMonthStatistic(Base):
    __tablename__ = 'inventory_month_statistic'
    id = Column(String(length=60))
    warehouse_no = Column(String(length=60), primary_key=True)
    warehouse_displayName = Column(String(length=60))
    date = Column(Date, primary_key=True)
    timezone = Column(String(length=60), primary_key=True)
    category = Column(Integer, primary_key=True)
    startAmount = Column(Float)
    inPurchaseAmount = Column(Float)
    inAmount = Column(Float)
    outAmount = Column(Float)
    endAmount = Column(Float)
    creationTime = Column(Integer)

class CTableInventoryItemMonthStatistic(Base):
    __tablename__ = 'inventory_item_month_statistic'
    id = Column(String(length=60))
    warehouse_no = Column(String(length=60), primary_key=True)
    warehouse_displayName = Column(String(length=60))
    date = Column(Date, primary_key=True)
    timezone = Column(String(length=60), primary_key=True)
    kind = Column(Integer)
    category = Column(Integer)
    specified_no = Column(String(length=60), primary_key=True)
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


class CTableOrderItemMonthStatistic(Base):
    __tablename__ = 'order_item_month_statistic'
    id = Column(String(length=60))
    date = Column(Date, primary_key=True)
    timezone = Column(String(length=60))
    kind = Column(Integer, primary_key=True)
    category = Column(Integer, primary_key=True)
    subCategory = Column(Integer, primary_key=True)
    type = Column(Integer)
    specified_no = Column(String(length=60), primary_key=True)
    specified_name = Column(String(length=60))
    payment = Column(Float)
    amount = Column(Float)
    creationTime = Column(Integer)


class CTableOrderPayment(Base):
    __tablename__ = 'order_payment'
    id = Column(Integer, primary_key=True)
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
    amount = Column(Float)
    addDeleteAmount = Column(Integer)
    totalAmount = Column(Float)
    balance = Column(Float)
    creationTime = Column(Integer)


class CTableShippingPayment(Base):
    __tablename__ = 'shipping_payment'
    id = Column(Integer, primary_key=True)
    no = Column(String(length=60))
    group_no = Column(String(length=60))
    date = Column(Integer)
    arapType = Column(Integer)
    record_no = Column(String(length=60))
    refCategory = Column(Integer)
    ref_no = Column(String(length=60))
    ref_sub_no = Column(String(length=60))
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

class CTableWarehousePayment(Base):
    __tablename__ = 'warehouse_payment'
    id = Column(Integer, primary_key=True)
    no = Column(String(length=60))
    group_no = Column(String(length=60))
    date = Column(Integer)
    arapType = Column(Integer)
    record_no = Column(String(length=60))
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
class CTableQuotation(Base):
    __tablename__ = 'quotation'
    no = Column(String(length=60), primary_key=True)
    creator_id = Column(String(length=60))
    date = Column(Integer, primary_key=True)
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

class CTableContract(Base):
    __tablename__ = 'contract'
    no = Column(String(length=60), primary_key=True)
    ref_no = Column(String(length=60))
    creator_id = Column(String(length=60))
    date = Column(Integer, primary_key=True)
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



class CTableARAP(Base):
    __tablename__ = 'arap'
    no = Column(String(length=60), primary_key=True)
    type = Column(Integer)
    ref_no = Column(String(length=60))
    refCategory = Column(Integer)
    ref_sub_no = Column(String(length=60))
    month = Column(Date)
    itemRefCategory = Column(Integer)
    item_ref_no = Column(String(length=60))
    item_ref_displayName = Column(String(length=60))
    paymentType = Column(Integer)

    amount = Column(Float)
    pendingAmount = Column(Float)
    balance = Column(Float)
    arap_nos = Column(JSON)
    arapAmount = Column(Float)
    invoice = Column(JSON)
    comment = Column(String(length=128))
    creationTime = Column(Integer)



class CTableAPSQuantityItem(Base):
    __tablename__ = 'aps_quantity_item'
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_order_no = Column(String(length=60), unique=True)
    output_item_no = Column(String(length=60), unique=True)
    oneProcess = Column(Integer, unique=True)
    secProcess = Column(Integer, unique=True)
    #aps_quantity_id = Column(String(length=60), ForeignKey('APS_quantity.id'))
    item_no = Column(String(length=60), unique=True)
    item_name = Column(String(length=60))
    itemCategory = Column(Integer)
    unit = Column(Integer)
    count = Column(Float)
    #quantity_data = relationship("CTableAPSQuantity", back_populates="item_data")

class CTableAPSQuantity(Base):
    __tablename__ = 'aps_quantity'
    id = Column(Integer, primary_key=True, autoincrement=True)
    no = Column(String(length=60), unique=True)
    product_order_no = Column(String(length=60), unique=True)
    oneProcess = Column(Integer, unique=True)
    secProcess = Column(Integer, unique=True)
    item_no = Column(String(length=60), unique=True)
    item_name = Column(String(length=60))
    itemCategory = Column(Integer)
    amount = Column(Float)
    unit = Column(Integer)
    minutes = Column(Integer)
    laborCount = Column(Integer)
    creationTime = Column(Integer)

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



class CTableAPSQuantityHistory(Base):
    __tablename__ = 'aps_quantity_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ref_product_order_no = Column(String(length=60))
    ref_item_no = Column(String(length=60))
    ref_oneProcess = Column(Integer)
    fieldName = Column(String(length=60), nullable=False)
    oldValue = Column(Text)
    newValue = Column(Text)
    modifiedBy = Column(String(length=60))
    modifiedAt = Column(Integer)


class CTableAPSQuantityItemHistory(Base):
    __tablename__ = 'aps_quantity_item_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ref_product_order_no = Column(String(length=60))
    ref_item_no = Column(String(length=60))
    ref_oneProcess = Column(Integer)
    ref_sub_item_no = Column(String(length=60))
    fieldName = Column(String(length=60), nullable=False)
    oldValue = Column(Text)
    newValue = Column(Text)
    modifiedBy = Column(String(length=60))
    modifiedAt = Column(Integer)

class CTableTemp(Base):
    __tablename__ = 'temp'
    id = Column(Integer, primary_key=True, autoincrement=True)
    work_order_no = Column(String(length=20))
    date = Column(Integer)


class CTableProductProcess(Base):
    __tablename__ = 'product_process'
    no = Column(String(length=60), primary_key=True)
    item_no = Column(String(length=60))
    version = Column(Integer)
    date = Column(Integer)

    # 建立一對多關係
    flows = relationship(
        "CTableProcessFlow",
        back_populates="process",
        order_by="CTableProcessFlow.product_process_no"
    )


class CTableProcessCapacity(Base):
    __tablename__ = 'process_capacity'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Integer, unique=True)
    oneProcess = Column(Integer, unique=True)
    secProcess = Column(Integer, unique=True)
    unit = Column(Integer)
    hourlyOutput = Column(Float)
    laborCount = Column(Integer)
    comment = Column(String(length=128))
    creationTime = Column(Integer)

class CTableProcessFlow(Base):
    __tablename__ = 'process_flow'
    no = Column(String(length=60), primary_key=True)
    product_process_no = Column(String(length=60),
        ForeignKey("product_process.no"))
    order = Column(Integer)
    oneProcess = Column(Integer)
    secProcess = Column(Integer)
    process = relationship("CTableProductProcess", back_populates="flows")

class CTableProductVer(Base):
    __tablename__ = 'product_ver'
    no = Column(String(length=60), primary_key=True)
    item_no = Column(String(length=60))
    version = Column(Integer)
    date = Column(Integer)


class CTablePLManCapacity(Base):
    __tablename__ = 'pl_man_capacity'
    no = Column(String(length=60), primary_key=True)
    month = Column(Date)
    pl_no = Column(String(length=60))
    pl_name = Column(String(length=60))
    productCount = Column(Integer)
    laborCount = Column(Integer)
    unit = Column(Integer)
    hourlyOutput = Column(Float)
    creationTime = Column(Integer)


class CTablePLItemCapacity(Base):
    __tablename__ = 'pl_item_capacity'
    no = Column(String(length=60), primary_key=True)
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


class CTablePLItemLoss(Base):
    __tablename__ = 'pl_item_loss'
    no = Column(String(length=60), primary_key=True)
    month = Column(Date)
    pl_item_capacity_no = Column(String(length=60))
    item_no = Column(String(length=60))
    item_name = Column(String(length=60))
    itemCategory = Column(Integer)
    itemSubCategory = Column(Integer)
    weightRatio = Column(Float)
    lossRate = Column(Float)
    creationTime = Column(Integer)


'''
    class CTableProcessOrder1 (Base):
        __tablename__ = 'process_order1'
        id = Column(String(length=60))
        no = Column(String(length=20), primary_key=True)
        creator_id = Column(String(length=60))
        work_order_no = Column(String(length=60))
        date                  = Column(Integer)
        category                  = Column(Integer)
        result                = Column(Integer)
        resultTime            = Column(Integer)
        comment               = Column(String(length=128))
        creationTime          = Column(Integer)
        # 建立一對多關係
        items = relationship("CTableProcessOrderItem", backref="process_order", lazy="subquery")
    
    class CTableProcessOrderItem(Base):
        __tablename__ = 'process_order_item'
        id = Column(String(length=60), primary_key=True)
        process_order_no = Column(String(length=60), ForeignKey("process_order.no"))
        item_no = Column(String(length=60))
        item_name = Column(String(length=60))
        item_ref_no = Column(String(length=60))
        item_ref_displayName = Column(String(length=60))
        itemCategory = Column(Integer)
        batch_number = Column(String(length=60))
        unit = Column(Integer)
        count = Column(Float)
'''