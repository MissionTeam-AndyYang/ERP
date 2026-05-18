from pydantic import BaseModel, ConfigDict, Field


class ProductOrderBase(BaseModel):
    creator_no: str | None = Field(default=None, max_length=60)
    date: int | None = None
    ref_no: str | None = Field(default=None, max_length=60)
    item_ref_no: str | None = Field(default=None, max_length=60)
    item_ref_displayName: str | None = Field(default=None, max_length=60)
    item_no: str | None = Field(default=None, max_length=60)
    item_name: str | None = Field(default=None, max_length=60)
    unit: int | None = None
    price: float | None = None
    count: float | None = None
    preparedCount: float | None = None
    amount: float | None = None
    expectedDate: int | None = None
    address: str | None = Field(default=None, max_length=100)
    payment_type: int | None = None
    payment_source: int | None = None
    payment_date: int | None = None
    payment_period: int | None = None
    comment: str | None = Field(default=None, max_length=128)
    creationTime: int | None = None


class ProductOrderCreate(ProductOrderBase):
    no: str = Field(min_length=1, max_length=20)


class ProductOrderUpdate(ProductOrderBase):
    no: str | None = Field(default=None, min_length=1, max_length=20)


class ProductOrderRead(ProductOrderBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    no: str


class ProductOrderList(BaseModel):
    total: int
    items: list[ProductOrderRead]
