from pydantic import BaseModel, ConfigDict, Field


class InventoryRecordBase(BaseModel):
    group: str | None = Field(default=None, max_length=60)
    refCategory: int | None = None
    ref_no: str | None = Field(default=None, max_length=60)
    warehouse_no: str | None = Field(default=None, max_length=60)
    warehouse_displayName: str | None = Field(default=None, max_length=60)
    date: int | None = None
    category: int | None = None
    source: int | None = None
    batchNumber: str | None = Field(default=None, max_length=20)
    serialNo: str | None = Field(default=None, max_length=20)
    item_no: str | None = Field(default=None, max_length=60)
    item_name: str | None = Field(default=None, max_length=60)
    item_ref_no: str | None = Field(default=None, max_length=60)
    item_ref_displayName: str | None = Field(default=None, max_length=60)
    itemCategory: int | None = None
    itemType: int | None = None
    unit: int | None = None
    count: float | None = None
    price: float | None = None
    amount: float | None = None
    comment: str | None = Field(default=None, max_length=128)
    registerDevId: str | None = Field(default=None, max_length=60)
    creationTime: int | None = None


class InventoryRecordCreate(InventoryRecordBase):
    pass


class InventoryRecordUpdate(InventoryRecordBase):
    pass


class InventoryRecordRead(InventoryRecordBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class InventoryRecordList(BaseModel):
    total: int
    items: list[InventoryRecordRead]
