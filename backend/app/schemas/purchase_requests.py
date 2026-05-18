from pydantic import BaseModel, ConfigDict, Field


class PurchaseRequestItemBase(BaseModel):
    item_no: str | None = Field(default=None, max_length=60)
    unit: int | None = None
    count: float | None = None
    expectedDate: int | None = None
    comment: str | None = Field(default=None, max_length=128)
    creationTime: int | None = None


class PurchaseRequestItemCreate(PurchaseRequestItemBase):
    pass


class PurchaseRequestItemRead(PurchaseRequestItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    purchase_request_no: str


class PurchaseRequestBase(BaseModel):
    creator_no: str | None = Field(default=None, max_length=60)
    product_order_no: str | None = Field(default=None, max_length=60)
    date: int | None = None
    comment: str | None = Field(default=None, max_length=128)
    creationTime: int | None = None


class PurchaseRequestCreate(PurchaseRequestBase):
    no: str = Field(min_length=1, max_length=20)
    items: list[PurchaseRequestItemCreate] = Field(default_factory=list)


class PurchaseRequestUpdate(PurchaseRequestBase):
    no: str | None = Field(default=None, min_length=1, max_length=20)


class PurchaseRequestRead(PurchaseRequestBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    no: str
    items: list[PurchaseRequestItemRead] = Field(default_factory=list)


class PurchaseRequestList(BaseModel):
    total: int
    items: list[PurchaseRequestRead]
